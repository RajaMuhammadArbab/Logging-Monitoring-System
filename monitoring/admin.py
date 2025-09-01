from django.contrib import admin
from .models import ActivityLog, ErrorLog

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'user', 'action', 'method', 'path', 'status_code', 'ip_address')
    list_filter = ('action', 'method', 'status_code', 'timestamp')
    search_fields = ('path', 'user__username')

@admin.register(ErrorLog)
class ErrorLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'user', 'message', 'status_code', 'endpoint', 'ip_address')
    list_filter = ('status_code', 'timestamp')
    search_fields = ('message', 'endpoint', 'user__username')
