#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Theme Manager
مدير الموضوع والألوان
"""

import customtkinter as ctk
from typing import Dict, Any
import tkinter.font as tkfont
from pathlib import Path

from src.utils.logger import get_logger

logger = get_logger(__name__)

class ThemeManager:
    """Theme manager for consistent UI styling"""

    def __init__(self, settings_manager):
        """Initialize theme manager"""
        self.settings_manager = settings_manager

        # Configure Arabic fonts
        self._setup_fonts()

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

        self.apply_theme()
        logger.info("Theme manager initialized")

    def _setup_fonts(self):
        """Setup Arabic fonts"""
        # Arabic fonts in order of preference
        arabic_fonts = [
            "Cairo",
            "Amiri",
            "Scheherazade New",
            "Noto Sans Arabic",
            "Traditional Arabic",
            "Arabic Typesetting",
            "Tahoma",
            "Segoe UI"
        ]

        # Get available fonts
        available_fonts = tkfont.families()

        # Find best Arabic font
        self.arabic_font = "Tahoma"  # fallback
        for font in arabic_fonts:
            if font in available_fonts:
                self.arabic_font = font
                break

        logger.info(f"Using Arabic font: {self.arabic_font}")

    def apply_theme(self):
        """Apply current theme"""
        theme_name = self.settings_manager.get_setting("theme", "dark")

        # Set CustomTkinter theme
        ctk.set_appearance_mode(theme_name)
        ctk.set_default_color_theme("blue")

    def get_colors(self) -> Dict[str, str]:
        """Get current theme colors"""
        theme_name = self.settings_manager.get_setting("theme", "dark")
        return self.themes.get(theme_name, self.themes["dark"])

    def get_font_config(self, size: int = 12, weight: str = "normal") -> tuple:
        """Get font configuration for Arabic text"""
        return (self.arabic_font, size, weight)

    def get_english_font_config(self, size: int = 12, weight: str = "normal") -> tuple:
        """Get font configuration for English text"""
        return ("Segoe UI", size, weight)

    def switch_theme(self, theme_name: str):
        """Switch to a different theme"""
        if theme_name in ["dark", "light"]:
            self.settings_manager.update_setting("theme", theme_name)
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