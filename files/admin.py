from django.contrib import admin
from .models import FileCategory, UploadedFile, FileDownloadLog

@admin.register(FileCategory)
class FileCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'uploaded_by', 'upload_date', 'access_type', 'file_size_display')
    list_filter = ('access_type', 'category', 'upload_date')
    search_fields = ('title', 'description', 'uploaded_by__username')
    date_hierarchy = 'upload_date'
    
    def file_size_display(self, obj):
        # Convert bytes to appropriate unit
        size_bytes = obj.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0 or unit == 'GB':
                break
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} {unit}"
    
    file_size_display.short_description = 'File Size'

@admin.register(FileDownloadLog)
class FileDownloadLogAdmin(admin.ModelAdmin):
    list_display = ('file', 'downloaded_by', 'download_date', 'ip_address')
    list_filter = ('download_date',)
    search_fields = ('file__title', 'downloaded_by__username', 'ip_address')
    date_hierarchy = 'download_date'
