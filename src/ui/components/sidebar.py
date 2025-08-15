
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sidebar Component
شريط جانبي
"""

import customtkinter as ctk
from typing import Callable
from PIL import Image, ImageTk
from pathlib import Path

from src.utils.logger import get_logger

logger = get_logger(__name__)

class Sidebar(ctk.CTkFrame):
    """Sidebar navigation component"""
    
    def __init__(self, parent, on_view_change: Callable, theme_manager):
        super().__init__(parent, width=250, corner_radius=0)
        
        self.on_view_change = on_view_change
        self.theme_manager = theme_manager
        self.active_button = None
        
        # Configure grid
        self.grid_rowconfigure(8, weight=1)  # Spacer
        
        # Navigation items
        self.nav_items = [
            ("dashboard", "لوحة التحكم", "dashboard.png"),
            ("products", "المنتجات", "products.png"),
            ("sales", "المبيعات", "sales.png"),
            ("customers", "العملاء", "customers.png"),
            ("reports", "التقارير", "reports.png"),
            ("settings", "الإعدادات", "settings.png")
        ]
        
        self.buttons = {}
        self._create_navigation()
        
        logger.info("Sidebar component initialized")
    
    def _load_icon(self, icon_name: str, size: tuple = (24, 24)) -> ctk.CTkImage:
        """Load and resize icon"""
        try:
            icon_path = Path(f"assets/icons/{icon_name}")
            if icon_path.exists():
                image = Image.open(icon_path)
                return ctk.CTkImage(light_image=image, dark_image=image, size=size)
            else:
                # Return empty image if icon not found
                return ctk.CTkImage(Image.new('RGBA', size, (0, 0, 0, 0)), size=size)
        except Exception as e:
            logger.warning(f"Could not load icon {icon_name}: {e}")
            return ctk.CTkImage(Image.new('RGBA', size, (0, 0, 0, 0)), size=size)
    
    def _create_navigation(self):
        """Create navigation buttons"""
        colors = self.theme_manager.get_colors()
        font = self.theme_manager.get_font_config(14, "bold")
        
        # Logo/Title
        title_label = ctk.CTkLabel(
            self,
            text="المحل الذكي",
            font=self.theme_manager.get_font_config(18, "bold"),
            text_color=colors["accent"]
        )
        title_label.grid(row=0, column=0, padx=20, pady=(20, 30), sticky="ew")
        
        # Navigation buttons
        for i, (view_name, label, icon_name) in enumerate(self.nav_items, 1):
            icon = self._load_icon(icon_name)
            
            button = ctk.CTkButton(
                self,
                text=f"  {label}",
                image=icon,
                compound="left",
                anchor="w",
                font=font,
                height=50,
                fg_color="transparent",
                text_color=colors["text_secondary"],
                hover_color=colors["bg_tertiary"],
                command=lambda v=view_name: self._on_button_click(v)
            )
            button.grid(row=i, column=0, padx=10, pady=5, sticky="ew")
            
            self.buttons[view_name] = button
        
        # Spacer
        spacer = ctk.CTkFrame(self, height=1, fg_color="transparent")
        spacer.grid(row=8, column=0, sticky="ew")
        
        # Footer info
        footer_label = ctk.CTkLabel(
            self,
            text="الإصدار 2.0",
            font=self.theme_manager.get_font_config(10),
            text_color=colors["text_secondary"]
        )
        footer_label.grid(row=9, column=0, padx=20, pady=(10, 20))
    
    def _on_button_click(self, view_name: str):
        """Handle button click"""
        self.on_view_change(view_name)
    
    def set_active_button(self, view_name: str):
        """Set active button styling"""
        colors = self.theme_manager.get_colors()
        
        # Reset all buttons
        for button in self.buttons.values():
            button.configure(
                fg_color="transparent",
                text_color=colors["text_secondary"]
            )
        
        # Set active button
        if view_name in self.buttons:
            self.buttons[view_name].configure(
                fg_color=colors["accent"],
                text_color=colors["text_primary"]
            )
            self.active_button = view_name
    
    def update_theme(self):
        """Update theme colors"""
        colors = self.theme_manager.get_colors()
        
        # Update button colors
        for view_name, button in self.buttons.items():
            if view_name == self.active_button:
                button.configure(
                    fg_color=colors["accent"],
                    text_color=colors["text_primary"],
                    hover_color=colors["accent_hover"]
                )
            else:
                button.configure(
                    fg_color="transparent",
                    text_color=colors["text_secondary"],
                    hover_color=colors["bg_tertiary"]
                )
