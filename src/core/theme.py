#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Theme Manager
مدير السمات
"""

import customtkinter as ctk
from typing import Dict, Any
import tkinter.font as tkfont
from pathlib import Path
import os
import platform

from src.utils.logger import get_logger

logger = get_logger(__name__)

class ThemeManager:
    """Theme manager for consistent UI styling"""

    def __init__(self, settings_manager):
        """Initialize theme manager"""
        self.settings_manager = settings_manager
        
        # Initialize font names with defaults first
        self.arabic_font_name = "Tahoma"
        self.header_font_name = "Tahoma"

        # Color schemes
        self.themes = {
            "dark": {
                "bg_primary": "#1a1a1a",
                "bg_secondary": "#2b2b2b",
                "bg_tertiary": "#3c3c3c",
                "text_primary": "#ffffff",
                "text_secondary": "#cccccc",
                "accent": "#3B8ED0",
                "accent_hover": "#2980b9",
                "success": "#27ae60",
                "warning": "#f39c12",
                "danger": "#e74c3c",
                "border": "#4a4a4a",
                "entry_bg": "#343638",
                "button_bg": "#1f538d",
                "button_hover": "#14375e"
            },
            "light": {
                "bg_primary": "#ffffff",
                "bg_secondary": "#f8f9fa",
                "bg_tertiary": "#e9ecef",
                "text_primary": "#2c3e50",
                "text_secondary": "#6c757d",
                "accent": "#3B8ED0",
                "accent_hover": "#2980b9",
                "success": "#27ae60",
                "warning": "#f39c12",
                "danger": "#e74c3c",
                "border": "#dee2e6",
                "entry_bg": "#ffffff",
                "button_bg": "#3b82f6",
                "button_hover": "#2563eb"
            }
        }

        # Initialize current_theme and apply basic theme
        self.current_theme = self.settings_manager.get_setting("display", "theme", "dark")
        
        self.apply_theme()
        logger.info("Theme manager initialized successfully")

    def _setup_custom_fonts(self):
        """Setup custom Arabic fonts"""
        # Font paths
        fonts_dir = Path("assets/fonts")
        hayah_path = fonts_dir / "Hayah.otf"
        shorooq_path = fonts_dir / "Shorooq.ttf"

        try:
            # Register fonts if files exist
            if hayah_path.exists():
                if platform.system() == "Windows":
                    import ctypes
                    from ctypes import wintypes
                    gdi32 = ctypes.windll.gdi32
                    gdi32.AddFontResourceW.argtypes = [wintypes.LPCWSTR]
                    gdi32.AddFontResourceW(str(hayah_path))
                    logger.info("Hayah font registered successfully")
                else:
                    # For Linux/Mac, font registration might require different steps
                    # or simply ensuring the font is available in the system.
                    # For now, we log that the path is available.
                    logger.info("Hayah font path available (registration may differ on non-Windows)")

            if shorooq_path.exists():
                if platform.system() == "Windows":
                    gdi32.AddFontResourceW(str(shorooq_path))
                    logger.info("Shorooq font registered successfully")
                else:
                    logger.info("Shorooq font path available (registration may differ on non-Windows)")

        except Exception as e:
            logger.warning(f"Could not register custom fonts: {e}")
            # Fallback to system fonts if registration fails
            self.arabic_font_name = "Arial"
            self.header_font_name = "Arial"
        
        # Set default font names, falling back if registration failed or files are missing
        if self._is_font_registered("Hayah"):
             self.arabic_font_name = "Hayah"
        else:
             self.arabic_font_name = self._find_best_arabic_font()

        if self._is_font_registered("Shorooq"):
            self.header_font_name = "Shorooq"
        else:
            self.header_font_name = self.arabic_font_name # Fallback header to general Arabic font


        logger.info(f"Using general Arabic font: {self.arabic_font_name}")
        logger.info(f"Using header Arabic font: {self.header_font_name}")

    def _is_font_registered(self, font_name: str) -> bool:
        """Check if a font is available in the system."""
        try:
            # Using tkinter.font to check for font families
            font_families = tkfont.families()
            return font_name in font_families
        except Exception as e:
            logger.warning(f"Error checking font availability for {font_name}: {e}")
            return False

    def _find_best_arabic_font(self) -> str:
        """Find the best available Arabic font from a list of preferred fonts."""
        arabic_fonts = [
            "Cairo", "Amiri", "Scheherazade New", "Noto Sans Arabic",
            "Traditional Arabic", "Arabic Typesetting", "Tahoma", "Segoe UI"
        ]
        available_fonts = tkfont.families()
        for font in arabic_fonts:
            if font in available_fonts:
                return font
        return "Tahoma"  # fallback

    def initialize_fonts(self):
        """Initialize fonts after main window is created"""
        try:
            self._setup_custom_fonts()
            logger.info("Fonts initialized successfully")
        except Exception as e:
            logger.warning(f"Failed to initialize custom fonts: {e}")
            # Keep default fallback fonts
            pass

    def _setup_fonts(self):
        """Setup Arabic fonts based on availability."""
        # This method is kept for compatibility but logic moved to initialize_fonts
        pass


    def apply_theme(self):
        """Apply current theme"""
        theme_name = self.settings_manager.get_setting("display", "theme", "dark")
        if theme_name in self.themes:
            self.current_theme = theme_name
        else:
            self.current_theme = "dark" # Default to dark if invalid theme name

        # Apply theme to CustomTkinter
        ctk.set_appearance_mode(self.current_theme)
        # ctk.set_default_color_theme("blue") # Removed as per changes, it's not in the snippet

    def get_colors(self) -> Dict[str, str]:
        """Get current theme colors"""
        return self.themes.get(self.current_theme, self.themes["dark"])

    def get_font_config(self, size: int = 12, weight: str = "normal") -> ctk.CTkFont:
        """Get font configuration for Arabic text"""
        return ctk.CTkFont(
            family=self.arabic_font_name,
            size=size,
            weight=weight
        )

    def get_header_font_config(self, size: int = 16, weight: str = "bold") -> ctk.CTkFont:
        """Get font configuration for Arabic headers"""
        return ctk.CTkFont(
            family=self.header_font_name,
            size=size,
            weight=weight
        )

    def get_english_font_config(self, size: int = 12, weight: str = "normal") -> tuple:
        """Get font configuration for English text"""
        return ("Segoe UI", size, weight)

    def switch_theme(self, theme_name: str):
        """Switch to a different theme"""
        if theme_name in ["dark", "light"]:
            self.settings_manager.update_setting("display", "theme", theme_name)
            self.apply_theme()
            logger.info(f"Switched to theme: {theme_name}")
            return True
        return False

    def get_icon_path(self, icon_name: str) -> str:
        """Get icon path"""
        icon_path = Path(f"assets/icons/{icon_name}")
        if icon_path.exists():
            return str(icon_path)
        return ""