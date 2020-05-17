# 增加日志查看
from django.contrib.admin.models import LogEntry

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
import requests
from django.contrib.auth import get_permission_codename # 权限

from .models import Post,Category,Tag
from .adminforms import PostAdminForm
from typeidea.base_admin import BaseOwnerAdmin
from typeidea.custom_site import custom_site #增加站点

# 权限api地址
PERMISSION_API = "http://permission.sso.com/has_perm?user={}@perm_code={}"

# 实现分类页面直接编辑文章
class PostInline(admin.TabularInline): #StackedInline 样式不同
    fields = ('title','desc') # ,'content'
    extra = 1 # 控制额外多几个
    model = Post


# 分类管理
@admin.register(Category,site=custom_site)
class CategoryAdmin(BaseOwnerAdmin):
    inlines = [PostInline, ] #在分类编辑页面配置文章编辑页面
    # 查询展示字段
    list_display =  ('name', 'status', 'is_nav', 'create_time','post_count')#
    # 录入时的显示字段
    fields = ('name', 'status', 'is_nav') #, 'owner' 作者改为自动获取当前登陆人

    def post_count(self,obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'

    # 重写ModelAdmin 的save_model 方法，作用是保存数据到数据库中
    """此处功能封装在BaseOwnerAdmin.py中"""
    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user
    #     return super(CategoryAdmin, self).save_model(request,obj,form,change)

# 标签管理
@admin.register(Tag,site=custom_site)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name','status','create_time')
    fields = ('name', 'status')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(TagAdmin, self).save_model(request,obj,form,change)

# 定义分类过滤器
class CategoryOwnerFilter(admin.SimpleListFilter):
    """ 自定义过滤器只展示当前用户分类"""

    title = '分类过滤器'
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id','name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=category_id)
        return queryset


# 文章 的admin
@admin.register(Post,site=custom_site)
class PostAdmin(BaseOwnerAdmin):
    #重写has_add_permission
    # def has_add_permission(self, request):
    #     opts = self.opts
    #     codename = get_permission_codename('add',opts)
    #     perm_code = "%s.%s"%(opts.app_label,codename)
    #     resp = requests.get(PERMISSION_API.format(request.user.username,perm_code))
    #     if resp.status_code == 200:
    #         return True
    #     else:
    #         return False
    
    # 将adminforms的代码配置在此处
    form = PostAdminForm

    list_display = [
        'title', 'category', 'status',
        'create_time', 'operator','owner'
    ]
    list_display_links = []

    list_filter = ['category','create_time','title']
    list_filter = [CategoryOwnerFilter]
    search_fields = ['title','category','category_name','create_time']

    actions_on_top = True
    actions_on_bottom = True

    # 编辑界面
    save_on_top = True

    # 自动赋值owner=当前用户
    exclude = ('owner',)

    #用 fieldsets替换fields 实现
    # fields = (
    #     ('category','title'),
    #     'desc',
    #     'status',
    #     'content',
    #     'tag',
    # )

    fieldsets = (
        ('基础配置', {
            'description':'基础配置描述',
            'fields':(
                ('title','category'),'status',
            )
        }),
        ('内容',{
            'fields':(
                'desc',
                'content',
            ),
        }),
        ('额外信息',{
            'classes':('collapse',), # 'collapse', 隐藏，'wide' 显示
            'fields':('tag',),
        })

    )

    # filter_horizontal 和 filter_vertical 用法
    filter_horizontal = ('tag',)
    # filter_vertical = ('tag',)

    def operator(self,obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('cus_admin:blog_post_change', args=(obj.id,))
        )
    operator.short_description = '操作'
    #operator.short_description = '明细'
    
    """此处功能封装在BaseOwnerAdmin.py中"""
    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user
    #     return super(PostAdmin,self).save_model(request,obj,form,change)
    # 
    # def get_queryset(self, request):
    #     qs = super(PostAdmin, self).get_queryset(request)
    #     return qs.filter(owner=request.user)

    # 给页面增加JavaScript脚本来完成某些前端操作
    class Media:
        # cdn.bootcss.com挂了。国内访问不到，怎么办？
        # cdn.bootcss.com替换成cdn.bootcdn.net/ajax/libs/twitter-bootstrap
        # css = {
        #     # 'all':("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css",),
        #     'all':("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.css",),
        # }
        js = ('https://cdn.bootcdn.net/ajax/libs/twitter-bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js',)


#增加日志查看功能
@admin.register(LogEntry,site = custom_site)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['object_repr','object_id','action_flag','user',
                    'change_message']
