from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.

@admin.register(CustomUser)
class CustomUserModelAdmin(BaseUserAdmin):
    pass

# admin.site.register(CustomUser)