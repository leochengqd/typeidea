from django.contrib import admin

from .models import Link,SideBar
from typeidea.base_admin import BaseOwnerAdmin
from typeidea.custom_site import custom_site #增加站点

@admin.register(Link,site=custom_site)
class LinkAmin(BaseOwnerAdmin):
    list_display = ('title','href','status','weight','create_time')
    fields = ('title','href','status','weight')

    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user
    #     return super(LinkAmin, self).save_model(request,obj, form, change)


@admin.register(SideBar,site=custom_site)
class SideBarAdmin(BaseOwnerAdmin):
    list_display = ('title','display_type','content','create_time')
    fields = ('title','display_type','content')

    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user
    #     return super(SideBarAdmin, self).save_model(request, obj, form ,change)
