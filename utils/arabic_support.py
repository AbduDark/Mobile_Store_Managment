#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Arabic Language Support Utilities for Mobile Shop Management System
أدوات دعم اللغة العربية لنظام إدارة محل الموبايلات
"""

import tkinter as tk
import customtkinter as ctk
from tkinter import font
import platform
import os
from typing import Optional, Dict, Any

class ArabicFontManager:
    """Manager for Arabic font support across the application"""
    
    def __init__(self):
        self.default_fonts = {
            'Windows': ['Segoe UI', 'Tahoma', 'Arial Unicode MS'],
            'Darwin': ['SF Arabic', 'Al Nile', 'Damascus', 'Arial Unicode MS'],  # macOS
            'Linux': ['Noto Sans Arabic', 'DejaVu Sans', 'Liberation Sans']
        }
        self.system = platform.system()
        self.available_fonts = []
        self.selected_font = None
        self._detect_available_fonts()
    
    def _detect_available_fonts(self):
        """Detect available Arabic-supporting fonts on the system"""
        try:
            # Get all available font families
            root = tk.Tk()
            root.withdraw()  # Hide the window
            
            all_fonts = font.families(root)
            
            # Check system-specific fonts first
            system_fonts = self.default_fonts.get(self.system, [])
            
            for font_name in system_fonts:
                if font_name in all_fonts:
                    self.available_fonts.append(font_name)
            
            # Add other common Arabic fonts if available
            other_arabic_fonts = [
                'Traditional Arabic',
                'Simplified Arabic',
                'Arabic Typesetting',
                'Microsoft Sans Serif',
                'Calibri'
            ]
            
            for font_name in other_arabic_fonts:
                if font_name in all_fonts and font_name not in self.available_fonts:
                    self.available_fonts.append(font_name)
            
            # Fallback to system default if no specific fonts found
            if not self.available_fonts:
                self.available_fonts = ['TkDefaultFont']
            
            # Select the first available font as default
            self.selected_font = self.available_fonts[0]
            
            root.destroy()
            
        except Exception as e:
            print(f"خطأ في اكتشاف الخطوط: {e}")
            self.available_fonts = ['TkDefaultFont']
            self.selected_font = 'TkDefaultFont'
    
    def get_font(self, size: int = 12, weight: str = "normal") -> tuple:
        """Get Arabic-supporting font tuple"""
        return (self.selected_font, size, weight)
    
    def get_font_family(self) -> str:
        """Get the selected Arabic font family name"""
        return self.selected_font
    
    def set_font(self, font_name: str) -> bool:
        """Set the Arabic font if it's available"""
        if font_name in self.available_fonts:
            self.selected_font = font_name
            return True
        return False
    
    def get_available_fonts(self) -> list:
        """Get list of available Arabic-supporting fonts"""
        return self.available_fonts.copy()

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
    
    try:
        # Configure CustomTkinter with Arabic font
        arabic_font_family = font_manager.get_font_family()
        
        # Set default font for CustomTkinter
        ctk.set_default_color_theme("blue")
        
        # Note: CustomTkinter doesn't directly support changing default font
        # But we can return the font info to be used in widgets
        return arabic_font_family
        
    except Exception as e:
        print(f"خطأ في إعداد الخط العربي: {e}")
        return "TkDefaultFont"

def create_arabic_font(size: int = 12, weight: str = "normal") -> ctk.CTkFont:
    """Create a CustomTkinter font with Arabic support"""
    font_manager = get_font_manager()
    font_family = font_manager.get_font_family()
    
    return ctk.CTkFont(family=font_family, size=size, weight=weight)

def is_rtl_text(text: str) -> bool:
    """Check if text should be displayed right-to-left"""
    if not text:
        return False
    
    # Unicode ranges for Arabic and other RTL languages
    rtl_ranges = [
        (0x0590, 0x05FF),  # Hebrew
        (0x0600, 0x06FF),  # Arabic
        (0x0700, 0x074F),  # Syriac
        (0x0750, 0x077F),  # Arabic Supplement
        (0x0780, 0x07BF),  # Thaana
        (0x08A0, 0x08FF),  # Arabic Extended-A
        (0xFB1D, 0xFB4F),  # Hebrew Presentation Forms
        (0xFB50, 0xFDFF),  # Arabic Presentation Forms-A
        (0xFE70, 0xFEFF),  # Arabic Presentation Forms-B
    ]
    
    rtl_count = 0
    total_chars = 0
    
    for char in text:
        char_code = ord(char)
        total_chars += 1
        
        for start, end in rtl_ranges:
            if start <= char_code <= end:
                rtl_count += 1
                break
    
    # If more than 30% of characters are RTL, consider the text RTL
    return total_chars > 0 and (rtl_count / total_chars) > 0.3

def format_mixed_text(text: str, max_length: int = 50) -> str:
    """Format mixed Arabic/English text for better display"""
    if not text:
        return text
    
    # If text is too long, truncate it
    if len(text) > max_length:
        return text[:max_length-3] + "..."
    
    return text

def configure_widget_for_arabic(widget, font_size: int = 12):
    """Configure a widget for optimal Arabic text display"""
    try:
        arabic_font = create_arabic_font(font_size)
        
        if hasattr(widget, 'configure'):
            widget.configure(font=arabic_font)
            
            # Set text alignment for RTL if supported
            if hasattr(widget, 'configure') and 'justify' in widget.configure():
                widget.configure(justify='right')
    
    except Exception as e:
        print(f"خطأ في تكوين الواجهة للعربية: {e}")

def get_text_direction(text: str) -> str:
    """Get text direction (ltr or rtl) based on content"""
    if is_rtl_text(text):
        return "rtl"
    else:
        return "ltr"

class ArabicText:
    """Helper class for Arabic text handling"""
    
    @staticmethod
    def normalize_text(text: str) -> str:
        """Normalize Arabic text (remove diacritics, normalize characters)"""
        if not text:
            return text
        
        # Common Arabic character normalizations
        normalizations = {
            'ي': 'ي',  # Normalize different forms of Ya
            'ك': 'ك',  # Normalize different forms of Kaf
            'ة': 'ه',  # Normalize Tah Marbuta to Hah for search purposes
        }
        
        normalized = text
        for old_char, new_char in normalizations.items():
            normalized = normalized.replace(old_char, new_char)
        
        return normalized
    
    @staticmethod
    def remove_diacritics(text: str) -> str:
        """Remove Arabic diacritics from text"""
        if not text:
            return text
        
        # Arabic diacritics Unicode range
        diacritics = [
            '\u064B',  # Fathatan
            '\u064C',  # Dammatan  
            '\u064D',  # Kasratan
            '\u064E',  # Fatha
            '\u064F',  # Damma
            '\u0650',  # Kasra
            '\u0651',  # Shadda
            '\u0652',  # Sukun
            '\u0653',  # Maddah
            '\u0654',  # Hamza above
            '\u0655',  # Hamza below
            '\u0656',  # Subscript alef
            '\u0657',  # Inverted damma
            '\u0658',  # Mark noon ghunna
            '\u0659',  # Zwarakay
            '\u065A',  # Vowel sign small v
            '\u065B',  # Vowel sign inverted small v
            '\u065C',  # Vowel sign dot below
            '\u065D',  # Reversed damma
            '\u065E',  # Fatha with two dots
            '\u065F',  # Wavy hamza below
            '\u0670',  # Superscript alef
        ]
        
        for diacritic in diacritics:
            text = text.replace(diacritic, '')
        
        return text
    
    @staticmethod
    def is_arabic_number(text: str) -> bool:
        """Check if text contains Arabic-Indic numerals"""
        arabic_numerals = '٠١٢٣٤٥٦٧٨٩'
        return any(char in arabic_numerals for char in text)
    
    @staticmethod
    def convert_arabic_numbers_to_english(text: str) -> str:
        """Convert Arabic-Indic numerals to English numerals"""
        arabic_to_english = {
            '٠': '0', '١': '1', '٢': '2', '٣': '3', '٤': '4',
            '٥': '5', '٦': '6', '٧': '7', '٨': '8', '٩': '9'
        }
        
        result = text
        for arabic_num, english_num in arabic_to_english.items():
            result = result.replace(arabic_num, english_num)
        
        return result
    
    @staticmethod
    def convert_english_numbers_to_arabic(text: str) -> str:
        """Convert English numerals to Arabic-Indic numerals"""
        english_to_arabic = {
            '0': '٠', '1': '١', '2': '٢', '3': '٣', '4': '٤',
            '5': '٥', '6': '٦', '7': '٧', '8': '٨', '9': '٩'
        }
        
        result = text
        for english_num, arabic_num in english_to_arabic.items():
            result = result.replace(english_num, arabic_num)
        
        return result

def create_rtl_entry(parent, **kwargs) -> ctk.CTkEntry:
    """Create a CustomTkinter Entry widget optimized for RTL text"""
    entry = ctk.CTkEntry(parent, **kwargs)
    
    # Configure for Arabic
    configure_widget_for_arabic(entry, kwargs.get('font_size', 12))
    
    return entry

def create_rtl_label(parent, text: str = "", **kwargs) -> ctk.CTkLabel:
    """Create a CustomTkinter Label widget optimized for RTL text"""
    # Determine text direction
    if is_rtl_text(text):
        kwargs['anchor'] = kwargs.get('anchor', 'e')  # Right align for RTL
    
    label = ctk.CTkLabel(parent, text=text, **kwargs)
    
    # Configure for Arabic
    configure_widget_for_arabic(label, kwargs.get('font_size', 12))
    
    return label

def create_rtl_button(parent, text: str = "", **kwargs) -> ctk.CTkButton:
    """Create a CustomTkinter Button widget optimized for RTL text"""
    button = ctk.CTkButton(parent, text=text, **kwargs)
    
    # Configure for Arabic
    configure_widget_for_arabic(button, kwargs.get('font_size', 12))
    
    return button

def setup_window_for_arabic(window):
    """Setup window for Arabic interface"""
    try:
        # Set window to support RTL layout conceptually
        # Note: Tkinter/CustomTkinter doesn't have native RTL support,
        # but we can configure elements individually
        
        # Configure default font
        arabic_font = create_arabic_font()
        
        # Set window properties for Arabic
        if hasattr(window, 'option_add'):
            window.option_add('*Font', arabic_font)
    
    except Exception as e:
        print(f"خطأ في إعداد النافذة للعربية: {e}")

# Initialize font manager when module is imported
get_font_manager()
