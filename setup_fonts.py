#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Font Setup Script for Mobile Shop Management System
سكريبت إعداد الخطوط لنظام إدارة محل الموبايلات
"""

import os
import sys
import shutil
import platform
import urllib.request
import zipfile
from pathlib import Path

def create_fonts_directory():
    """Create fonts directory if it doesn't exist"""
    fonts_dir = Path("fonts")
    fonts_dir.mkdir(exist_ok=True)
    print(f"✓ تم إنشاء مجلد الخطوط: {fonts_dir.absolute()}")
    return fonts_dir

def download_noto_arabic():
    """Download Noto Sans Arabic font (free font)"""
    try:
        fonts_dir = Path("fonts")
        font_url = "https://github.com/googlefonts/noto-fonts/raw/main/hinted/ttf/NotoSansArabic/NotoSansArabic-Regular.ttf"
        font_path = fonts_dir / "NotoSansArabic-Regular.ttf"
        
        if font_path.exists():
            print(f"✓ خط نوتو العربي موجود مسبقاً: {font_path}")
            return True
        
        print("📥 جاري تحميل خط نوتو العربي...")
        urllib.request.urlretrieve(font_url, font_path)
        print(f"✓ تم تحميل خط نوتو العربي: {font_path}")
        return True
        
    except Exception as e:
        print(f"❌ خطأ في تحميل خط نوتو العربي: {e}")
        return False

def find_system_fonts():
    """Find available Arabic fonts in the system"""
    system = platform.system()
    system_fonts = []
    
    if system == "Windows":
        fonts_paths = [
            Path("C:/Windows/Fonts"),
            Path(os.path.expanduser("~/AppData/Local/Microsoft/Windows/Fonts"))
        ]
    elif system == "Darwin":  # macOS
        fonts_paths = [
            Path("/System/Library/Fonts"),
            Path("/Library/Fonts"),
            Path(os.path.expanduser("~/Library/Fonts"))
        ]
    else:  # Linux
        fonts_paths = [
            Path("/usr/share/fonts"),
            Path("/usr/local/share/fonts"),
            Path(os.path.expanduser("~/.fonts")),
            Path(os.path.expanduser("~/.local/share/fonts"))
        ]
    
    arabic_fonts = [
        "Tahoma.ttf", "tahoma.ttf", "TAHOMA.TTF",
        "arial.ttf", "Arial.ttf", "ARIAL.TTF",
        "ArialUnicodeMS.ttf", "Arial Unicode MS.ttf",
        "seguiui.ttf", "Segoe UI.ttf", "SEGUIUI.TTF"
    ]
    
    for fonts_path in fonts_paths:
        if fonts_path.exists():
            for font_file in arabic_fonts:
                font_path = fonts_path / font_file
                if font_path.exists():
                    system_fonts.append(font_path)
    
    return system_fonts

def copy_system_fonts():
    """Copy system fonts to fonts directory"""
    fonts_dir = Path("fonts")
    system_fonts = find_system_fonts()
    
    if not system_fonts:
        print("⚠️  لم يتم العثور على خطوط عربية في النظام")
        return False
    
    copied_count = 0
    for font_path in system_fonts:
        try:
            dest_path = fonts_dir / font_path.name
            if not dest_path.exists():
                shutil.copy2(font_path, dest_path)
                print(f"✓ تم نسخ الخط: {font_path.name}")
                copied_count += 1
            else:
                print(f"○ الخط موجود مسبقاً: {font_path.name}")
                
        except Exception as e:
            print(f"❌ خطأ في نسخ الخط {font_path.name}: {e}")
    
    print(f"✓ تم نسخ {copied_count} خط إلى مجلد الخطوط")
    return copied_count > 0

def test_fonts():
    """Test if fonts are properly loaded"""
    try:
        from utils.font_loader import list_available_fonts
        print("\n=== اختبار تحميل الخطوط ===")
        custom_fonts = list_available_fonts()
        
        if custom_fonts:
            print(f"✓ تم تحميل {len(custom_fonts)} خط مخصص بنجاح")
            return True
        else:
            print("⚠️  لم يتم تحميل أي خطوط مخصصة")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في اختبار الخطوط: {e}")
        return False

def create_install_script():
    """Create a batch/shell script for easy font installation"""
    system = platform.system()
    
    if system == "Windows":
        script_content = """@echo off
echo Installing Arabic fonts for Mobile Shop Management System...
echo تثبيت الخطوط العربية لنظام إدارة محل الموبايلات...

python setup_fonts.py

echo.
echo Done! Press any key to exit...
echo تم الانتهاء! اضغط أي زر للخروج...
pause
"""
        with open("install_fonts.bat", "w", encoding="utf-8") as f:
            f.write(script_content)
        print("✓ تم إنشاء ملف install_fonts.bat")
        
    else:  # Unix-like systems
        script_content = """#!/bin/bash
echo "Installing Arabic fonts for Mobile Shop Management System..."
echo "تثبيت الخطوط العربية لنظام إدارة محل الموبايلات..."

python3 setup_fonts.py

echo "Done!"
echo "تم الانتهاء!"
"""
        with open("install_fonts.sh", "w", encoding="utf-8") as f:
            f.write(script_content)
        
        # Make it executable
        os.chmod("install_fonts.sh", 0o755)
        print("✓ تم إنشاء ملف install_fonts.sh")

def main():
    """Main setup function"""
    print("🚀 إعداد الخطوط العربية لنظام إدارة محل الموبايلات")
    print("=" * 50)
    
    # Create fonts directory
    fonts_dir = create_fonts_directory()
    
    # Download free fonts
    print("\n📥 تحميل الخطوط المجانية...")
    download_noto_arabic()
    
    # Copy system fonts
    print("\n📋 البحث عن خطوط النظام...")
    copy_system_fonts()
    
    # Test fonts
    print("\n🧪 اختبار الخطوط...")
    if test_fonts():
        print("\n✅ تم إعداد الخطوط بنجاح!")
    else:
        print("\n⚠️  قد تحتاج إلى إضافة خطوط عربية يدوياً")
    
    # Create install script
    print("\n📝 إنشاء سكريبت التثبيت...")
    create_install_script()
    
    print("\n" + "=" * 50)
    print("📖 للمزيد من المعلومات، راجع ملف INSTALL_FONTS.md")
    print("🎯 مجلد الخطوط:", fonts_dir.absolute())

if __name__ == "__main__":
    main()