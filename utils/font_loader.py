
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Font Loader for Custom Fonts in Mobile Shop Management System
محمل الخطوط المخصصة لنظام إدارة محل الموبايلات
"""

import os
import sys
import platform
from tkinter import font as tkFont
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib import rcParams

def load_custom_fonts():
    """Load custom fonts from fonts directory"""
    try:
        # Get the fonts directory path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        fonts_dir = os.path.join(project_root, "fonts")
        
        if not os.path.exists(fonts_dir):
            print(f"مجلد الخطوط غير موجود: {fonts_dir}")
            return {}
        
        loaded_fonts = {}
        font_extensions = ['.ttf', '.otf', '.TTF', '.OTF']
        
        # Get all font files
        font_files = []
        for file in os.listdir(fonts_dir):
            if any(file.endswith(ext) for ext in font_extensions):
                font_path = os.path.join(fonts_dir, file)
                font_files.append((file, font_path))
        
        if not font_files:
            print("لم يتم العثور على ملفات خطوط في المجلد")
            return {}
        
        # Load fonts for matplotlib
        for font_file, font_path in font_files:
            try:
                # Add font to matplotlib font manager
                fm.fontManager.addfont(font_path)
                
                # Get the actual font name from the file
                font_props = fm.FontProperties(fname=font_path)
                font_name = font_props.get_name()
                
                # Store both file name and actual font name
                loaded_fonts[font_file] = {
                    'name': font_name,
                    'path': font_path,
                    'file': font_file
                }
                print(f"تم تحميل الخط: {font_name} من {font_file}")
                
            except Exception as e:
                print(f"خطأ في تحميل الخط {font_file}: {e}")
        
        return loaded_fonts
        
    except Exception as e:
        print(f"خطأ في تحميل الخطوط المخصصة: {e}")
        return {}

def get_font_path(font_name):
    """Get the full path to a font file"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    fonts_dir = os.path.join(project_root, "fonts")
    
    # Check for exact file name
    font_path = os.path.join(fonts_dir, font_name)
    if os.path.exists(font_path):
        return font_path
    
    # Check for font name with extensions
    for ext in ['.ttf', '.otf', '.TTF', '.OTF']:
        font_path = os.path.join(fonts_dir, f"{font_name}{ext}")
        if os.path.exists(font_path):
            return font_path
    
    return None

def configure_matplotlib_arabic():
    """Configure matplotlib for Arabic support"""
    try:
        # Load custom fonts
        loaded_fonts = load_custom_fonts()
        
        # Set up custom fonts for matplotlib
        primary_font_path = get_font_path('Hacen-Tunisia.ttf')
        secondary_font_path = get_font_path('Ya-ModernPro-Bold.otf')
        
        font_paths = []
        if primary_font_path:
            font_paths.append(primary_font_path)
        if secondary_font_path:
            font_paths.append(secondary_font_path)
        
        # Add fonts to matplotlib
        for font_path in font_paths:
            fm.fontManager.addfont(font_path)
        
        # Configure matplotlib to use our fonts
        if primary_font_path:
            primary_props = fm.FontProperties(fname=primary_font_path)
            plt.rcParams['font.family'] = primary_props.get_name()
        
        # Set RTL support and other Arabic-friendly settings
        plt.rcParams['axes.unicode_minus'] = False
        plt.rcParams['font.size'] = 12
        
        print(f"تم تكوين matplotlib للعربية")
        
    except Exception as e:
        print(f"خطأ في تكوين matplotlib للعربية: {e}")

def get_best_arabic_font():
    """Get the best available Arabic font"""
    # Try to get custom fonts first
    primary_font_path = get_font_path('Hacen-Tunisia.ttf')
    if primary_font_path:
        font_props = fm.FontProperties(fname=primary_font_path)
        return font_props.get_name()
    
    # Fallback to system fonts
    system = platform.system()
    
    if system == 'Windows':
        return 'Tahoma'
    elif system == 'Darwin':  # macOS
        return 'SF Arabic'
    else:  # Linux
        return 'DejaVu Sans'

def list_available_fonts():
    """List all available fonts in the system and custom fonts"""
    print("=== الخطوط المخصصة ===")
    custom_fonts = load_custom_fonts()
    if custom_fonts:
        for file, font_info in custom_fonts.items():
            print(f"الملف: {file} - الاسم: {font_info['name']}")
    else:
        print("لا توجد خطوط مخصصة")
    
    return custom_fonts

if __name__ == "__main__":
    # Test the font loading
    print("اختبار تحميل الخطوط...")
    configure_matplotlib_arabic()
    list_available_fonts()
