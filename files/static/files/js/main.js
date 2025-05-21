/**
 * LAN Transfer - File Management System
 * Developed by Hussein Yehya
 * GitHub: https://github.com/Husseinyehya1853/lantransfer
 * 
 * Copyright (c) 2025 Hussein Yehya. All rights reserved.
 * Licensed under the MIT License
 */

// Main JavaScript file for File Manager System

// Auto-hide alerts after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide alerts
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // File upload form validation
    const fileUploadForm = document.getElementById('fileUploadForm');
    if (fileUploadForm) {
        fileUploadForm.addEventListener('submit', function(event) {
            const fileInput = document.getElementById('id_file');
            const titleInput = document.getElementById('id_title');
            
            // Check if file is selected
            if (fileInput.files.length === 0) {
                event.preventDefault();
                alert('Please select a file to upload');
                return false;
            }
            
            // Check file size (max 5GB)
            const maxSize = 5 * 1024 * 1024 * 1024; // 5GB in bytes
            if (fileInput.files[0].size > maxSize) {
                event.preventDefault();
                alert('حجم الملف يتجاوز الحد الأقصى (5 جيجابايت)');
                return false;
            }
            
            // Check if title is provided
            if (titleInput.value.trim() === '') {
                event.preventDefault();
                alert('Please provide a title for the file');
                return false;
            }
            
            // Show loading indicator
            showLoadingIndicator();
            return true;
        });
        
        // Auto-fill title from filename
        const fileInput = document.getElementById('id_file');
        if (fileInput) {
            fileInput.addEventListener('change', function() {
                const titleInput = document.getElementById('id_title');
                if (fileInput.files.length > 0 && titleInput.value.trim() === '') {
                    let fileName = fileInput.files[0].name;
                    // Remove extension
                    fileName = fileName.split('.').slice(0, -1).join('.');
                    titleInput.value = fileName;
                }
            });
        }
    }
    
    // Confirm delete actions
    const deleteButtons = document.querySelectorAll('.delete-confirm');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(event) {
            if (!confirm('Are you sure you want to delete this item?')) {
                event.preventDefault();
            }
        });
    });
});

// Add loading indicator for file downloads
document.addEventListener('DOMContentLoaded', function() {
    // Create loading overlay if it doesn't exist
    if (!document.querySelector('.loading-overlay')) {
        const loadingOverlay = document.createElement('div');
        loadingOverlay.className = 'loading-overlay';
        
        const spinner = document.createElement('div');
        spinner.className = 'loading-spinner';
        
        loadingOverlay.appendChild(spinner);
        document.body.appendChild(loadingOverlay);
    }
    
    // Add click event to all download buttons
    const downloadButtons = document.querySelectorAll('.download-btn');
    downloadButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            showLoadingIndicator();
            
            // Hide loading indicator after file download starts (after 2 seconds)
            setTimeout(function() {
                hideLoadingIndicator();
            }, 2000);
        });
    });
});

// Show loading indicator
function showLoadingIndicator() {
    const loadingOverlay = document.querySelector('.loading-overlay');
    if (loadingOverlay) {
        loadingOverlay.classList.add('active');
    }
}

// Hide loading indicator
function hideLoadingIndicator() {
    const loadingOverlay = document.querySelector('.loading-overlay');
    if (loadingOverlay) {
        loadingOverlay.classList.remove('active');
    }
}

// Add file transfer speed calculation
document.addEventListener('DOMContentLoaded', function() {
    // Add data attributes to download links for tracking
    const downloadLinks = document.querySelectorAll('a[href^="/download/"]');
    downloadLinks.forEach(function(link) {
        link.setAttribute('data-start-time', '0');
        link.setAttribute('data-file-size', link.getAttribute('data-size') || '0');
        
        link.addEventListener('click', function() {
            this.setAttribute('data-start-time', Date.now().toString());
            // We'll calculate the transfer speed when the download completes
            // but this is challenging in a browser environment without additional APIs
        });
    });
});

// Developer information
// Add copyright notice to console
console.log('%c LAN Transfer - File Management System', 'font-weight: bold; font-size: 14px; color: #007bff;');
console.log('%c Developed by Hussein Yehya | https://github.com/Husseinyehya1853/lantransfer', 'font-size: 12px; color: #6c757d;');
console.log('%c © 2025 Hussein Yehya. All rights reserved.', 'font-size: 12px; color: #6c757d;');