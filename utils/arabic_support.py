#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Arabic Font Support for Mobile Shop Management System
دعم الخطوط العربية لنظام إدارة محل الموبايلات
"""

import customtkinter as ctk
from tkinter import font as tkFont
import platform
import os
import sys

class ArabicFontManager:
    """Manages Arabic fonts for the application"""

    def __init__(self):
        self.available_fonts = []
        self.custom_fonts = []
        self.primary_font = None  # For titles - Hacen-Tunisia
        self.secondary_font = None  # For general text - Ya-ModernPro-Bold
        self._load_custom_fonts()
        self._detect_available_fonts()

    def _load_custom_fonts(self):
        """Load custom fonts from fonts directory"""
        try:
            # Get the fonts directory path
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(current_dir)
            fonts_dir = os.path.join(project_root, "fonts")

            if not os.path.exists(fonts_dir):
                print(f"مجلد الخطوط غير موجود: {fonts_dir}")
                return

            font_extensions = ['.ttf', '.otf', '.TTF', '.OTF']

            # Get all font files
            font_files = []
            for file in os.listdir(fonts_dir):
                if any(file.endswith(ext) for ext in font_extensions):
                    font_path = os.path.join(fonts_dir, file)
                    font_files.append((file, font_path))

            if not font_files:
                print("لم يتم العثور على ملفات خطوط في المجلد")
                return

            # Load fonts for tkinter
            for font_file, font_path in font_files:
                try:
                    # Try to load the font
                    if platform.system() == "Windows":
                        import ctypes
                        ctypes.windll.gdi32.AddFontResourceW(font_path)

                    font_name = os.path.splitext(font_file)[0]

                    # Set primary and secondary fonts
                    if "Hacen-Tunisia" in font_file:
                        self.primary_font = font_name
                        print(f"تم تحديد الخط الأساسي: {font_name}")
                    elif "Ya-ModernPro" in font_file:
                        self.secondary_font = font_name
                        print(f"تم تحديد الخط الفرعي: {font_name}")

                    self.custom_fonts.append({
                        'name': font_name,
                        'path': font_path,
                        'file': font_file
                    })
                    print(f"تم تحميل الخط: {font_name}")

                except Exception as e:
                    print(f"خطأ في تحميل الخط {font_file}: {e}")

        except Exception as e:
            print(f"خطأ في تحميل الخطوط المخصصة: {e}")

    def _detect_available_fonts(self):
        """Detect available system fonts"""
        try:
            # Get system fonts
            import tkinter as tk
            root = tk.Tk()
            root.withdraw()
            system_fonts = list(tkFont.families())
            root.destroy()

            # Combine custom and system fonts
            self.available_fonts = [f['name'] for f in self.custom_fonts] + system_fonts

            # Set fallback fonts if custom fonts not found
            if not self.primary_font:
                arabic_fonts = ['Tahoma', 'Arial Unicode MS', 'Segoe UI', 'Calibri']
                for font in arabic_fonts:
                    if font in system_fonts:
                        self.primary_font = font
                        break
                else:
                    self.primary_font = 'TkDefaultFont'

            if not self.secondary_font:
                arabic_fonts = ['Tahoma', 'Arial Unicode MS', 'Segoe UI', 'Times New Roman']
                for font in arabic_fonts:
                    if font in system_fonts:
                        self.secondary_font = font
                        break
                else:
                    self.secondary_font = 'TkDefaultFont'

            print(f"الخطوط المتاحة: {self.available_fonts[:8]}")  # Show first 8
            print(f"الخط الأساسي: {self.primary_font}")
            print(f"الخط الفرعي: {self.secondary_font}")

        except Exception as e:
            print(f"خطأ في اكتشاف الخطوط: {e}")
            self.available_fonts = ['TkDefaultFont']
            if not self.primary_font:
                self.primary_font = 'TkDefaultFont'
            if not self.secondary_font:
                self.secondary_font = 'TkDefaultFont'

    def get_primary_font(self, size: int = 16, weight: str = "bold") -> ctk.CTkFont:
        """Get primary font for titles (Hacen-Tunisia)"""
        return ctk.CTkFont(family=self.primary_font, size=size, weight=weight)

    def get_secondary_font(self, size: int = 12, weight: str = "normal") -> ctk.CTkFont:
        """Get secondary font for general text (Ya-ModernPro)"""
        return ctk.CTkFont(family=self.secondary_font, size=size, weight=weight)

    def get_font_family(self, is_title: bool = False) -> str:
        """Get font family name"""
        return self.primary_font if is_title else self.secondary_font

# Global font manager instance
_font_manager = None

def get_font_manager() -> ArabicFontManager:
    """Get the global font manager instance"""
    global _font_manager
    if _font_manager is None:
        _font_manager = ArabicFontManager()
    return _font_manager

def setup_arabic_font():
    """Setup Arabic font support for the application"""
    font_manager = get_font_manager()
    return font_manager

def create_arabic_font(size: int = 12, weight: str = "normal", is_title: bool = False) -> ctk.CTkFont:
    """Create a CustomTkinter font with Arabic support"""
    font_manager = get_font_manager()

    if is_title:
        return font_manager.get_primary_font(size, weight)
    else:
        return font_manager.get_secondary_font(size, weight)

def create_title_font(size: int = 24) -> ctk.CTkFont:
    """Create font for titles"""
    return create_arabic_font(size, "bold", True)

def create_heading_font(size: int = 18) -> ctk.CTkFont:
    """Create font for headings"""
    return create_arabic_font(size, "bold", True)

def create_body_font(size: int = 12) -> ctk.CTkFont:
    """Create font for body text"""
    return create_arabic_font(size, "normal", False)

def create_button_font(size: int = 14) -> ctk.CTkFont:
    """Create font for buttons"""
    return create_arabic_font(size, "normal", False)

def format_arabic_text(text: str, max_length: int = None) -> str:
    """Format Arabic text for display"""
    if not text:
        return ""

    # Remove extra whitespace
    text = ' '.join(text.split())

    if max_length is None:
        return text

    # If text is too long, truncate it
    if len(text) > max_length:
        return text[:max_length-3] + "..."

    return text

def configure_widget_for_arabic(widget, font_size: int = 12, is_title: bool = False):
    """Configure a widget for optimal Arabic text display"""
    try:
        arabic_font = create_arabic_font(font_size, is_title=is_title)

        if hasattr(widget, 'configure'):
            widget.configure(font=arabic_font)

            # Set text alignment for RTL if supported
            if hasattr(widget, 'configure') and 'justify' in widget.configure():
                widget.configure(justify='right')

    except Exception as e:
        print(f"خطأ في تكوين الواجهة للعربية: {e}")

def create_arabic_label(parent, text: str, is_title: bool = False, **kwargs) -> ctk.CTkLabel:
    """Create a label optimized for Arabic text"""
    font_size = kwargs.pop('font_size', 14 if not is_title else 20)
    font = create_arabic_font(font_size, is_title=is_title)

    return ctk.CTkLabel(
        parent,
        text=text,
        font=font,
        justify='right',
        **kwargs
    )

def create_arabic_button(parent, text: str, **kwargs) -> ctk.CTkButton:
    """Create a button optimized for Arabic text"""
    font_size = kwargs.pop('font_size', 14)
    font = create_button_font(font_size)

    return ctk.CTkButton(
        parent,
        text=text,
        font=font,
        **kwargs
    )