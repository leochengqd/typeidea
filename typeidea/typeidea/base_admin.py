from django.contrib import admin

class BaseOwnerAdmin(admin.ModelAdmin):
    """
    1.重写save方法，设置对象owner；
    2.重写get_queryset 方法，让列表页展示文章或者分类时只能展示当前用户的数据
    """
    exclude = ('owner',)

    def get_queryset(self, request):
        qs = super(BaseOwnerAdmin, self).get_queryset(request)
        return qs.filter(owner = request.user)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(BaseOwnerAdmin, self).save_model(request, obj, form, change)