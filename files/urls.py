"""URLs for the files app.

LAN Transfer - File Management System
Developed by Hussein Yehya
GitHub: https://github.com/Husseinyehya1853/lantransfer

Copyright (c) 2025 Hussein Yehya. All rights reserved.
Licensed under the MIT License
"""
from django.urls import path
from . import views

urlpatterns = [
    # Authentication URLs
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # File management URLs
    path('', views.home_view, name='home'),
    path('upload/', views.upload_file_view, name='upload_file'),
    path('download/<int:file_id>/', views.download_file_view, name='download_file'),
    path('my-files/', views.my_files_view, name='my_files'),
    path('delete/<int:file_id>/', views.delete_file_view, name='delete_file'),
    
    # Admin URLs
    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('admin-files/', views.admin_files_view, name='admin_files'),
    path('admin-logs/', views.admin_logs_view, name='admin_logs'),
    path('manage-categories/', views.manage_categories_view, name='manage_categories'),
    path('delete-category/<int:category_id>/', views.delete_category_view, name='delete_category'),
]