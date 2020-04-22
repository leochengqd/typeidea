from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Post,Category,Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # 查询展示字段
    list_display =  ('name', 'status', 'is_nav', 'create_time','post_count')#
    # 录入时的显示字段
    fields = ('name', 'status', 'is_nav') #, 'owner' 作者改为自动获取当前登陆人

    def post_count(self,obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'

    # 重写ModelAdmin 的save_model 方法，作用是保存数据到数据库中
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(CategoryAdmin, self).save_model(request,obj,form,change)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name','status','create_time')
    fields = ('name', 'status')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(TagAdmin, self).save_model(request,obj,form,change)

# POST 的admin
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'category', 'status',
        'create_time', 'operator'
    ]
    list_display_links = []

    list_filter = ['category','create_time','title']
    search_fields = ['title','category','category_name','create_time']

    actions_on_top = True
    actions_on_bottom = True

    # 编辑界面
    save_on_top = True

    fields = (
        ('category','title'),
        'desc',
        'status',
        'content',
        'tag',
    )

    def operator(self,obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('admin:blog_post_change', args=(obj.id,))
        )
    operator.short_description = '操作'
    #operator.short_description = '明细'

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(PostAdmin,self).save_model(request,obj,form,change)