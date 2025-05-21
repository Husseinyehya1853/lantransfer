"""Models for the files app.

LAN Transfer - File Management System
Developed by Hussein Yehya
GitHub: https://github.com/Husseinyehya1853/lantransfer

Copyright (c) 2025 Hussein Yehya. All rights reserved.
Licensed under the MIT License
"""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class FileCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

class UploadedFile(models.Model):
    FILE_ACCESS_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='uploads/%Y/%m/%d/')
    category = models.ForeignKey(FileCategory, on_delete=models.SET_NULL, null=True, blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_files')
    upload_date = models.DateTimeField(default=timezone.now)
    access_type = models.CharField(max_length=10, choices=FILE_ACCESS_CHOICES, default='public')
    file_size = models.BigIntegerField(default=0)  # Size in bytes
    
    def __str__(self):
        return self.title
    
    def filename(self):
        return self.file.name.split('/')[-1]

class FileDownloadLog(models.Model):
    file = models.ForeignKey(UploadedFile, on_delete=models.CASCADE, related_name='download_logs')
    downloaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='download_logs', null=True, blank=True)
    download_date = models.DateTimeField(default=timezone.now)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    def __str__(self):
        user = self.downloaded_by.username if self.downloaded_by else 'Anonymous'
        return f"{self.file.title} downloaded by {user} on {self.download_date}"
