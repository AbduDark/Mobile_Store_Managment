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

def load_custom_fonts():
    """Load custom fonts from fonts directory"""
    try:
        # Get the fonts directory path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        fonts_dir = os.path.join(project_root, "fonts")
        
        if not os.path.exists(fonts_dir):
            print(f"مجلد الخطوط غير موجود: {fonts_dir}")
            return []
        
        loaded_fonts = []
        font_extensions = ['.ttf', '.otf', '.TTF', '.OTF']
        
        # Get all font files
        font_files = []
        for file in os.listdir(fonts_dir):
            if any(file.endswith(ext) for ext in font_extensions):
                font_files.append(os.path.join(fonts_dir, file))
        
        if not font_files:
            print("لم يتم العثور على ملفات خطوط في المجلد")
            return []
        
        # Load fonts for matplotlib
        for font_file in font_files:
            try:
                # Add font to matplotlib font manager
                fm.fontManager.addfont(font_file)
                font_name = os.path.splitext(os.path.basename(font_file))[0]
                loaded_fonts.append({
                    'name': font_name,
                    'path': font_file,
                    'family': font_name
                })
                print(f"تم تحميل الخط: {font_name}")
                
            except Exception as e:
                print(f"خطأ في تحميل الخط {font_file}: {e}")
        
        # Update matplotlib font list
        if loaded_fonts:
            font_names = [f['name'] for f in loaded_fonts]
            # Set the first custom font as default for matplotlib
            plt.rcParams['font.family'] = font_names + ['DejaVu Sans', 'Arial']
            print(f"تم تحديث خطوط matplotlib: {font_names}")
        
        return loaded_fonts
        
    except Exception as e:
        print(f"خطأ في تحميل الخطوط المخصصة: {e}")
        return []

def get_best_arabic_font():
    """Get the best available Arabic font"""
    # Load custom fonts first
    custom_fonts = load_custom_fonts()
    
    if custom_fonts:
        # Return the first custom font if available
        return custom_fonts[0]['name']
    
    # Fallback to system fonts
    system = platform.system()
    
    if system == 'Windows':
        return 'Segoe UI'
    elif system == 'Darwin':  # macOS
        return 'SF Arabic'
    else:  # Linux
        return 'DejaVu Sans'

def configure_matplotlib_arabic():
    """Configure matplotlib for Arabic support"""
    try:
        # Load custom fonts
        load_custom_fonts()
        
        # Set RTL support
        plt.rcParams['axes.unicode_minus'] = False
        
        # Set font for different matplotlib components
        best_font = get_best_arabic_font()
        plt.rcParams['font.family'] = [best_font, 'DejaVu Sans', 'Arial']
        plt.rcParams['font.size'] = 12
        
        print(f"تم تكوين matplotlib للعربية بالخط: {best_font}")
        
    except Exception as e:
        print(f"خطأ في تكوين matplotlib للعربية: {e}")

def list_available_fonts():
    """List all available fonts in the system and custom fonts"""
    print("=== الخطوط المتاحة في النظام ===")
    
    # System fonts
    try:
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()
        system_fonts = sorted(tkFont.families())
        root.destroy()
        
        print(f"عدد خطوط النظام: {len(system_fonts)}")
        for i, font in enumerate(system_fonts[:10], 1):  # Show first 10
            print(f"{i}. {font}")
        if len(system_fonts) > 10:
            print(f"... و {len(system_fonts) - 10} خط آخر")
            
    except Exception as e:
        print(f"خطأ في قراءة خطوط النظام: {e}")
    
    print("\n=== الخطوط المخصصة ===")
    custom_fonts = load_custom_fonts()
    if custom_fonts:
        for i, font in enumerate(custom_fonts, 1):
            print(f"{i}. {font['name']} - {font['path']}")
    else:
        print("لا توجد خطوط مخصصة")
    
    return custom_fonts

if __name__ == "__main__":
    # Test the font loading
    print("اختبار تحميل الخطوط...")
    configure_matplotlib_arabic()
    list_available_fonts()