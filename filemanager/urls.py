"""URLs for the filemanager project.

LAN Transfer - File Management System
Developed by Hussein Yehya
GitHub: https://github.com/Husseinyehya1853/lantransfer

Copyright (c) 2025 Hussein Yehya. All rights reserved.
Licensed under the MIT License
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('files.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
