from django.contrib import admin

from .models import Comment
from typeidea.custom_site import custom_site #增加站点


@admin.register(Comment,site=custom_site)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('target','nickname','content','website','create_time')
