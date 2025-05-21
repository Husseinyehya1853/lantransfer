"""Forms for the files app.

LAN Transfer - File Management System
Developed by Hussein Yehya
GitHub: https://github.com/Husseinyehya1853/lantransfer

Copyright (c) 2025 Hussein Yehya. All rights reserved.
Licensed under the MIT License
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UploadedFile, FileCategory

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['title', 'description', 'file', 'category', 'access_type']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'access_type': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def save(self, commit=True, user=None):
        instance = super().save(commit=False)
        if user:
            instance.uploaded_by = user
        
        # Calculate file size
        if instance.file:
            instance.file_size = instance.file.size
        
        if commit:
            instance.save()
        return instance

class FileCategoryForm(forms.ModelForm):
    class Meta:
        model = FileCategory
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }