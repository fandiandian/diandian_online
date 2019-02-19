# _*_ coding: utf-8 _*_

from django.contrib import admin
from .models import UserProfiles


class UserProfilesAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserProfiles, UserProfilesAdmin)


