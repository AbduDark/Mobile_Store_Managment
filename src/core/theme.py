
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
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Theme Manager
مدير المظاهر
"""

import customtkinter as ctk
from typing import Dict, Any

from src.utils.logger import get_logger

logger = get_logger(__name__)

class ThemeManager:
    """Theme management class"""
    
    def __init__(self, settings_manager):
        """Initialize theme manager"""
        self.settings_manager = settings_manager
        self.current_theme = "dark"
        
        # Theme colors
        self.themes = {
            "dark": {
                "bg_color": "#212121",
                "fg_color": "#2b2b2b", 
                "text_color": "#ffffff",
                "text_color_disabled": "#6b6b6b",
                "button_color": "#1f538d",
                "button_hover_color": "#14375e",
                "entry_color": "#343638",
                "frame_color": "#2b2b2b",
                "scrollbar_color": "#343638",
                "accent_color": "#1f538d"
            },
            "light": {
                "bg_color": "#f0f0f0",
                "fg_color": "#ffffff",
                "text_color": "#000000", 
                "text_color_disabled": "#6b6b6b",
                "button_color": "#3b82f6",
                "button_hover_color": "#2563eb",
                "entry_color": "#ffffff",
                "frame_color": "#ffffff",
                "scrollbar_color": "#c0c0c0",
                "accent_color": "#3b82f6"
            }
        }
        
        self._apply_theme()
    
    def _apply_theme(self):
        """Apply current theme"""
        theme_name = self.settings_manager.get_setting("theme", "dark")
        self.set_theme(theme_name)
    
    def set_theme(self, theme_name: str):
        """Set application theme"""
        if theme_name in self.themes:
            self.current_theme = theme_name
            
            # Set CustomTkinter appearance mode
            ctk.set_appearance_mode(theme_name)
            
            # Update settings
            self.settings_manager.update_setting("theme", theme_name)
            
            logger.info(f"Applied theme: {theme_name}")
        else:
            logger.warning(f"Unknown theme: {theme_name}")
    
    def get_color(self, color_key: str) -> str:
        """Get color from current theme"""
        return self.themes[self.current_theme].get(color_key, "#ffffff")
    
    def get_all_colors(self) -> Dict[str, str]:
        """Get all colors from current theme"""
        return self.themes[self.current_theme].copy()
    
    def toggle_theme(self):
        """Toggle between dark and light themes"""
        new_theme = "light" if self.current_theme == "dark" else "dark"
        self.set_theme(new_theme)
