from django.contrib import admin
from django.contrib.admin import register

from . import models


@register(models.User)
class UserAdmin(admin.ModelAdmin):
    fields = ("username", "first_name", "last_name", "email")
    search_fields = ("username",)


@register(models.Follow)
class FollowAdmin(admin.ModelAdmin):
    fields = ("user", "following")
    search_fields = ("user",)
