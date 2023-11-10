from django.contrib import admin
from .models import UserLoginLog


class UserLoginLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'login_time')


admin.site.register(UserLoginLog, UserLoginLogAdmin)
