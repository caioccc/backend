from django.contrib import admin

# Register your models here.
from app.models import Task, Category, SharedTask


class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'category', 'status', 'created_at', 'updated_at', 'user')
    list_filter = ('category', 'status', 'created_at', 'updated_at')
    search_fields = ('name', 'description', 'category', 'user')
    ordering = ('status', 'created_at')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at', 'user')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'user')
    ordering = ('created_at',)


class SharedTaskAdmin(admin.ModelAdmin):
    list_display = ('task', 'user', 'status', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('task', 'status', 'user')
    ordering = ('created_at',)


admin.site.register(Task, TaskAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SharedTask, SharedTaskAdmin)
