#!/usr/bin/env python
"""
بناء ملف تنفيذي لتطبيق LAN Transfer
حقوق النشر (c) Hussein Yehya
مرخص بموجب رخصة MIT
"""

import os
import sys
import subprocess
import shutil

def build_executable():
    print("بدء بناء الملف التنفيذي لـ LAN Transfer...")
    
    # التأكد من تثبيت PyInstaller
    try:
        import PyInstaller
    except ImportError:
        print("تثبيت PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "PyInstaller"])
    
    # إنشاء ملف spec
    spec_content = """
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['manage.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('files/static', 'files/static'),
        ('files/templates', 'files/templates'),
        ('media', 'media'),
    ],
    hiddenimports=[
        'django',
        'files',
        'filemanager',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='lantransfer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='lantransfer',
)
"""
    
    with open("lantransfer.spec", "w") as f:
        f.write(spec_content)
    
    # بناء الملف التنفيذي
    print("بناء الملف التنفيذي...")
    subprocess.check_call([sys.executable, "-m", "PyInstaller", "lantransfer.spec"])
    
    # إنشاء ملف batch للتشغيل
    batch_content = """
@echo off
cd %~dp0\dist\lantransfer
start lantransfer.exe runserver 0.0.0.0:8000
echo تم تشغيل LAN Transfer على العنوان http://localhost:8000
echo اضغط أي مفتاح لإيقاف الخادم...
pause > nul
taskkill /f /im lantransfer.exe
"""
    
    with open("dist\\lantransfer.bat", "w") as f:
        f.write(batch_content)
    
    print("\nتم بناء الملف التنفيذي بنجاح!")
    print("يمكنك تشغيل التطبيق باستخدام الملف: dist\lantransfer.bat")

if __name__ == "__main__":
    build_executable()