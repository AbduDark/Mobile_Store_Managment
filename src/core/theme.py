
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Theme Manager
مدير الموضوع والألوان
"""

import customtkinter as ctk
from typing import Dict, Any

class ThemeManager:
    """Theme manager for consistent UI styling"""
    
    def __init__(self, settings_manager):
        """Initialize theme manager"""
        self.settings_manager = settings_manager
        
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
                "border": "#4a4a4a"
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
                "border": "#dee2e6"
            }
        }
        
        self.apply_theme()
    
    def apply_theme(self):
        """Apply current theme"""
        theme_name = self.settings_manager.display.theme
        
        # Set CustomTkinter theme
        ctk.set_appearance_mode(theme_name)
        
        if theme_name in ["blue", "green", "dark-blue"]:
            ctk.set_default_color_theme(theme_name)
        else:
            ctk.set_default_color_theme("blue")
    
    def get_colors(self) -> Dict[str, str]:
        """Get current theme colors"""
        theme_name = self.settings_manager.display.theme
        return self.themes.get(theme_name, self.themes["dark"])
    
    def get_font_config(self, size: int = 12, weight: str = "normal") -> tuple:
        """Get font configuration"""
        font_family = "Segoe UI" if self.settings_manager.display.language == "en" else "Tahoma"
        return (font_family, size, weight)
    
    def switch_theme(self, theme_name: str):
        """Switch to a different theme"""
        if theme_name in ["dark", "light"]:
            self.settings_manager.update_display_settings(theme=theme_name)
            self.apply_theme()
            return True
        return False
