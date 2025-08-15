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
        self.custom_fonts = {}
        self.primary_font_path = None  # For titles - Hacen-Tunisia
        self.secondary_font_path = None  # For general text - Ya-ModernPro-Bold
        self.primary_font_name = None
        self.secondary_font_name = None
        self._load_custom_fonts()
        self._detect_available_fonts()

    def _get_font_path(self, font_name):
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

    def _load_custom_fonts(self):
        """Load custom fonts from fonts directory"""
        try:
            # Get specific font paths
            self.primary_font_path = self._get_font_path('Hacen-Tunisia.ttf')
            self.secondary_font_path = self._get_font_path('Ya-ModernPro-Bold.otf')

            if self.primary_font_path:
                # Register font for Windows if needed
                if platform.system() == "Windows":
                    try:
                        import ctypes
                        ctypes.windll.gdi32.AddFontResourceW(self.primary_font_path)
                    except:
                        pass

                # Extract font name for reference
                self.primary_font_name = "Hacen-Tunisia"
                print(f"تم تحديد الخط الأساسي: {self.primary_font_name}")
                print(f"مسار الخط: {self.primary_font_path}")

            if self.secondary_font_path:
                # Register font for Windows if needed
                if platform.system() == "Windows":
                    try:
                        import ctypes
                        ctypes.windll.gdi32.AddFontResourceW(self.secondary_font_path)
                    except:
                        pass

                # Extract font name for reference
                self.secondary_font_name = "Ya-ModernPro-Bold"
                print(f"تم تحديد الخط الفرعي: {self.secondary_font_name}")
                print(f"مسار الخط: {self.secondary_font_path}")

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

            # Set fallback fonts if custom fonts not found
            if not self.primary_font_path:
                arabic_fonts = ['Tahoma', 'Arial Unicode MS', 'Segoe UI', 'Calibri']
                for font in arabic_fonts:
                    if font in system_fonts:
                        self.primary_font_name = font
                        break
                else:
                    self.primary_font_name = 'TkDefaultFont'

            if not self.secondary_font_path:
                arabic_fonts = ['Tahoma', 'Arial Unicode MS', 'Segoe UI', 'Times New Roman']
                for font in arabic_fonts:
                    if font in system_fonts:
                        self.secondary_font_name = font
                        break
                else:
                    self.secondary_font_name = 'TkDefaultFont'

            print(f"الخط الأساسي: {self.primary_font_name}")
            print(f"الخط الفرعي: {self.secondary_font_name}")

        except Exception as e:
            print(f"خطأ في اكتشاف الخطوط: {e}")
            if not self.primary_font_name:
                self.primary_font_name = 'TkDefaultFont'
            if not self.secondary_font_name:
                self.secondary_font_name = 'TkDefaultFont'

    def get_primary_font(self, size: int = 16, weight: str = "bold") -> ctk.CTkFont:
        """Get primary font for titles (Hacen-Tunisia)"""
        if self.primary_font_path:
            # Use font file directly
            return ctk.CTkFont(family=self.primary_font_path, size=size, weight=weight)
        else:
            # Fallback to font name
            return ctk.CTkFont(family=self.primary_font_name, size=size, weight=weight)

    def get_secondary_font(self, size: int = 12, weight: str = "normal") -> ctk.CTkFont:
        """Get secondary font for general text (Ya-ModernPro)"""
        if self.secondary_font_path:
            # Use font file directly
            return ctk.CTkFont(family=self.secondary_font_path, size=size, weight=weight)
        else:
            # Fallback to font name
            return ctk.CTkFont(family=self.secondary_font_name, size=size, weight=weight)

    def get_font_family(self, is_title: bool = False) -> str:
        """Get font family name"""
        if is_title:
            return self.primary_font_path if self.primary_font_path else self.primary_font_name
        else:
            return self.secondary_font_path if self.secondary_font_path else self.secondary_font_name

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

def create_title_font(size=24):
    """Create title font for Arabic text"""
    try:
        font_manager = get_font_manager()
        return ctk.CTkFont(
            family=font_manager.primary_font,
            size=size,
            weight="bold"
        )
    except Exception as e:
        print(f"خطأ في إنشاء خط العنوان: {e}")
        return ctk.CTkFont(size=size, weight="bold")

def create_heading_font(size=18):
    """Create heading font for Arabic text"""
    try:
        font_manager = get_font_manager()
        return ctk.CTkFont(
            family=font_manager.primary_font,
            size=size,
            weight="bold"
        )
    except Exception as e:
        print(f"خطأ في إنشاء خط العنوان الفرعي: {e}")
        return ctk.CTkFont(size=size, weight="bold")

def create_body_font(size=12):
    """Create body font for Arabic text"""
    try:
        font_manager = get_font_manager()
        return ctk.CTkFont(
            family=font_manager.primary_font,
            size=size,
            weight="normal"
        )
    except Exception as e:
        print(f"خطأ في إنشاء خط النص: {e}")
        return ctk.CTkFont(size=size, weight="normal")

def create_button_font(size=14):
    """Create button font for Arabic text"""
    try:
        font_manager = get_font_manager()
        return ctk.CTkFont(
            family=font_manager.primary_font,
            size=size,
            weight="normal"
        )
    except Exception as e:
        print(f"خطأ في إنشاء خط الأزرار: {e}")
        return ctk.CTkFont(size=size, weight="normal")


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