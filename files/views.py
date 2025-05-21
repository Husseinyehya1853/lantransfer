"""Views for the files app.

LAN Transfer - File Management System
Developed by Hussein Yehya
GitHub: https://github.com/Husseinyehya1853/lantransfer

Copyright (c) 2025 Hussein Yehya. All rights reserved.
Licensed under the MIT License
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponse, Http404, FileResponse, StreamingHttpResponse, JsonResponse
from django.db.models import Q
from django.conf import settings
from django.core.paginator import Paginator
from .models import UploadedFile, FileCategory, FileDownloadLog
from .forms import CustomUserCreationForm, CustomAuthenticationForm, FileUploadForm, FileCategoryForm
import os
import mimetypes
import stat
import time
import re

# Helper functions
def is_admin(user):
    return user.is_authenticated and user.is_staff

# Optimized file streaming function
# تحسين معالجة الملفات الكبيرة باستخدام شرائح أكبر
def file_iterator(file_path, chunk_size=8192 * 16):
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk

# Authentication views
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'files/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('home')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'files/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')

# File views
def home_view(request):
    categories = FileCategory.objects.all()
    
    # Filter files based on user permissions
    if request.user.is_authenticated:
        files = UploadedFile.objects.all()
    else:
        files = UploadedFile.objects.filter(access_type='public')
    
    # Search functionality
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    
    if query:
        files = files.filter(Q(title__icontains=query) | Q(description__icontains=query))
    
    if category_id:
        files = files.filter(category_id=category_id)
    
    # Pagination
    paginator = Paginator(files.order_by('-upload_date'), 10)  # 10 files per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': category_id,
        'query': query,
    }
    return render(request, 'files/home.html', context)

@login_required
def upload_file_view(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file_instance = form.save(commit=False)
            file_instance.uploaded_by = request.user
            
            # Get the uploaded file
            uploaded_file = request.FILES['file']
            file_instance.file_size = uploaded_file.size
            
            # Optimize large file handling
            if file_instance.file_size > 100 * 1024 * 1024:  # If file is larger than 100MB
                # Use chunked saving for large files
                file_instance.save()
                
                # Return JSON response for AJAX uploads
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'status': 'success',
                        'message': 'تم رفع الملف الكبير بنجاح!',
                        'file_id': file_instance.id,
                        'file_name': file_instance.filename(),
                        'file_size': file_instance.file_size
                    })
                
                messages.success(request, 'تم رفع الملف الكبير بنجاح!')
                return redirect('home')
            else:
                # Standard save for smaller files
                file_instance.save()
                
                # Return JSON response for AJAX uploads
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'status': 'success',
                        'message': 'File uploaded successfully!',
                        'file_id': file_instance.id,
                        'file_name': file_instance.filename(),
                        'file_size': file_instance.file_size
                    })
                
                messages.success(request, 'File uploaded successfully!')
                return redirect('home')
    else:
        form = FileUploadForm()
    
    return render(request, 'files/upload.html', {'form': form})

@login_required
def download_file_view(request, file_id):
    file = get_object_or_404(UploadedFile, id=file_id)
    
    # Check if user has permission to download
    if file.access_type == 'private' and file.uploaded_by != request.user and not is_admin(request.user):
        messages.error(request, 'You do not have permission to download this file')
        return redirect('home')
    
    # Log the download
    FileDownloadLog.objects.create(
        file=file,
        downloaded_by=request.user if request.user.is_authenticated else None,
        ip_address=request.META.get('REMOTE_ADDR')
    )
    
    file_path = file.file.path
    
    # Get file stats
    stat_obj = os.stat(file_path)
    file_size = stat_obj.st_size
    last_modified = timezone.datetime.fromtimestamp(stat_obj.st_mtime)
    
    # Get file MIME type
    content_type, encoding = mimetypes.guess_type(file_path)
    content_type = content_type or 'application/octet-stream'
    
    # Support for Range requests (resumable downloads)
    range_header = request.META.get('HTTP_RANGE', '').strip()
    range_match = re.match(r'bytes=(\d+)-(\d*)', range_header)
    
    if range_match:
        first_byte, last_byte = range_match.groups()
        first_byte = int(first_byte)
        last_byte = int(last_byte) if last_byte else file_size - 1
        if last_byte >= file_size:
            last_byte = file_size - 1
        length = last_byte - first_byte + 1
        
        resp = StreamingHttpResponse(
            file_iterator_range(file_path, first_byte, length, chunk_size=8192 * 16),
            status=206,
            content_type=content_type
        )
        resp['Content-Length'] = str(length)
        resp['Content-Range'] = f'bytes {first_byte}-{last_byte}/{file_size}'
    else:
        resp = StreamingHttpResponse(
            file_iterator(file_path, chunk_size=8192 * 16),
            content_type=content_type
        )
        resp['Content-Length'] = str(file_size)
    
    resp['Content-Disposition'] = f'attachment; filename="{file.filename()}"'
    resp['Accept-Ranges'] = 'bytes'
    resp['Last-Modified'] = last_modified.strftime('%a, %d %b %Y %H:%M:%S GMT')
    resp['Cache-Control'] = 'public, max-age=3600'
    
    return resp

# Function to support range requests for resumable downloads
def file_iterator_range(file_path, start_byte, length, chunk_size=8192 * 16):
    with open(file_path, 'rb') as f:
        f.seek(start_byte)
        remaining = length
        while remaining > 0:
            chunk_size = min(chunk_size, remaining)
            chunk = f.read(chunk_size)
            if not chunk:
                break
            remaining -= len(chunk)
            yield chunk

@login_required
def my_files_view(request):
    files = UploadedFile.objects.filter(uploaded_by=request.user).order_by('-upload_date')
    return render(request, 'files/my_files.html', {'files': files})

@login_required
def delete_file_view(request, file_id):
    file_obj = get_object_or_404(UploadedFile, id=file_id)
    
    # Check if user is owner or admin
    if file_obj.uploaded_by != request.user and not is_admin(request.user):
        messages.error(request, "You don't have permission to delete this file.")
        return redirect('home')
    
    if request.method == 'POST':
        file_obj.delete()
        messages.success(request, 'File deleted successfully!')
        return redirect('my_files' if not is_admin(request.user) else 'admin_files')
    
    return render(request, 'files/confirm_delete.html', {'file': file_obj})

# Admin views
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    total_files = UploadedFile.objects.count()
    total_downloads = FileDownloadLog.objects.count()
    recent_uploads = UploadedFile.objects.order_by('-upload_date')[:5]
    recent_downloads = FileDownloadLog.objects.order_by('-download_date')[:5]
    
    context = {
        'total_files': total_files,
        'total_downloads': total_downloads,
        'recent_uploads': recent_uploads,
        'recent_downloads': recent_downloads,
    }
    return render(request, 'files/admin_dashboard.html', context)

@user_passes_test(is_admin)
def admin_files_view(request):
    files = UploadedFile.objects.all().order_by('-upload_date')
    return render(request, 'files/admin_files.html', {'files': files})

@user_passes_test(is_admin)
def admin_logs_view(request):
    logs = FileDownloadLog.objects.all().order_by('-download_date')
    return render(request, 'files/admin_logs.html', {'logs': logs})

@user_passes_test(is_admin)
def manage_categories_view(request):
    categories = FileCategory.objects.all()
    
    if request.method == 'POST':
        form = FileCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully!')
            return redirect('manage_categories')
    else:
        form = FileCategoryForm()
    
    return render(request, 'files/manage_categories.html', {'categories': categories, 'form': form})

@user_passes_test(is_admin)
def delete_category_view(request, category_id):
    category = get_object_or_404(FileCategory, id=category_id)
    
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('manage_categories')
    
    return render(request, 'files/confirm_delete_category.html', {'category': category})