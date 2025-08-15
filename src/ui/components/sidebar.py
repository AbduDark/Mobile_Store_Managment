
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modern Sidebar Component
شريط جانبي حديث
"""

import customtkinter as ctk
from typing import Callable, Optional

class Sidebar(ctk.CTkFrame):
    """Modern sidebar with navigation buttons"""
    
    def __init__(self, parent, on_view_change: Callable, theme_manager):
        super().__init__(parent, width=250, corner_radius=0)
        
        self.on_view_change = on_view_change
        self.theme_manager = theme_manager
        self.active_button = None
        
        # Prevent frame from shrinking
        self.grid_propagate(False)
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup sidebar UI"""
        # Logo/Title section
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.grid(row=0, column=0, sticky="ew", padx=15, pady=(20, 30))
        title_frame.grid_columnconfigure(0, weight=1)
        
        # App title
        title_label = ctk.CTkLabel(
            title_frame,
            text="المحل الذكي",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=self.theme_manager.get_colors()["accent"]
        )
        title_label.grid(row=0, column=0)
        
        # Subtitle
        subtitle_label = ctk.CTkLabel(
            title_frame,
            text="Smart Shop v2.0",
            font=ctk.CTkFont(size=12),
            text_color=self.theme_manager.get_colors()["text_secondary"]
        )
        subtitle_label.grid(row=1, column=0, pady=(5, 0))
        
        # Navigation buttons
        nav_frame = ctk.CTkFrame(self, fg_color="transparent")
        nav_frame.grid(row=1, column=0, sticky="ew", padx=15, pady=10)
        nav_frame.grid_columnconfigure(0, weight=1)
        
        # Button configurations
        buttons_config = [
            ("dashboard", "🏠 الرئيسية", "Dashboard"),
            ("products", "📱 المنتجات", "Products"),
            ("sales", "🛒 المبيعات", "Sales"),
            ("customers", "👥 العملاء", "Customers"),
            ("reports", "📊 التقارير", "Reports"),
            ("settings", "⚙️ الإعدادات", "Settings")
        ]
        
        self.nav_buttons = {}
        
        for i, (view_name, text, tooltip) in enumerate(buttons_config):
            btn = ctk.CTkButton(
                nav_frame,
                text=text,
                height=45,
                font=ctk.CTkFont(size=14, weight="normal"),
                corner_radius=8,
                anchor="w",
                command=lambda v=view_name: self._on_button_click(v)
            )
            btn.grid(row=i, column=0, sticky="ew", pady=5)
            self.nav_buttons[view_name] = btn
        
        # Footer
        footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        footer_frame.grid(row=2, column=0, sticky="ews", padx=15, pady=20)
        footer_frame.grid_columnconfigure(0, weight=1)
        
        # Version info
        version_label = ctk.CTkLabel(
            footer_frame,
            text="الإصدار 2.0.0",
            font=ctk.CTkFont(size=10),
            text_color=self.theme_manager.get_colors()["text_secondary"]
        )
        version_label.grid(row=0, column=0)
        
        # Configure row weights
        self.grid_rowconfigure(1, weight=1)
    
    def _on_button_click(self, view_name: str):
        """Handle button click"""
        self.on_view_change(view_name)
    
    def set_active_button(self, view_name: str):
        """Set active button visual state"""
        colors = self.theme_manager.get_colors()
        
        # Reset all buttons
        for btn_name, btn in self.nav_buttons.items():
            if btn_name == view_name:
                # Active button
                btn.configure(
                    fg_color=colors["accent"],
                    hover_color=colors["accent_hover"],
                    text_color="white"
                )
                self.active_button = btn
            else:
                # Inactive buttons
                btn.configure(
                    fg_color="transparent",
                    hover_color=colors["bg_tertiary"],
                    text_color=colors["text_primary"]
                )
