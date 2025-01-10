from django.contrib import admin

# Register your models here.
from app.models import Task, Category, SharedTask, LocalUser, Weather


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


class LocalUserAdmin(admin.ModelAdmin):
    list_display = ('ip', 'country_name', 'country_code', 'city', 'latitude', 'longitude', 'country_flag', 'user')
    list_filter = ('country_name', 'country_code', 'city')
    search_fields = ('ip', 'country_name', 'country_code', 'city', 'latitude', 'longitude', 'country_flag', 'user')
    ordering = ('country_name', 'country_code', 'city', 'latitude', 'longitude', 'country_flag')


class WeatherAdmin(admin.ModelAdmin):
    list_display = ('city', 'source_photo', 'temperature', 'description', 'created_at', 'user')
    list_filter = ('city',)
    search_fields = ('city', 'temperature', 'description', 'user')
    ordering = ('city', 'temperature', 'description', 'created_at')


admin.site.register(Task, TaskAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SharedTask, SharedTaskAdmin)
admin.site.register(LocalUser, LocalUserAdmin)
admin.site.register(Weather, WeatherAdmin)
