from django.contrib import admin

from .models import User, Like


class UserAdmin(admin.ModelAdmin):
    pass


class LikeAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, UserAdmin)
admin.site.register(Like, LikeAdmin)
