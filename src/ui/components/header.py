
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Header Bar Component
شريط العنوان العلوي
"""

import customtkinter as ctk
from datetime import datetime
from typing import Optional

class HeaderBar(ctk.CTkFrame):
    """Header bar with title, time, and controls"""
    
    def __init__(self, parent, settings_manager, theme_manager):
        super().__init__(parent, height=60, corner_radius=0)
        
        self.settings_manager = settings_manager
        self.theme_manager = theme_manager
        
        # Prevent frame from shrinking
        self.grid_propagate(False)
        
        # Configure grid
        self.grid_columnconfigure(1, weight=1)
        
        self._setup_ui()
        self._start_time_update()
    
    def _setup_ui(self):
        """Setup header UI"""
        colors = self.theme_manager.get_colors()
        
        # Left section - Shop info
        left_frame = ctk.CTkFrame(self, fg_color="transparent")
        left_frame.grid(row=0, column=0, sticky="w", padx=20, pady=10)
        
        shop_name = ctk.CTkLabel(
            left_frame,
            text=self.settings_manager.shop.name,
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=colors["text_primary"]
        )
        shop_name.grid(row=0, column=0)
        
        # Center section - Page title (will be updated by views)
        self.page_title = ctk.CTkLabel(
            self,
            text="لوحة التحكم",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=colors["accent"]
        )
        self.page_title.grid(row=0, column=1, pady=10)
        
        # Right section - Time and controls
        right_frame = ctk.CTkFrame(self, fg_color="transparent")
        right_frame.grid(row=0, column=2, sticky="e", padx=20, pady=10)
        
        # Current time
        self.time_label = ctk.CTkLabel(
            right_frame,
            text="",
            font=ctk.CTkFont(size=12),
            text_color=colors["text_secondary"]
        )
        self.time_label.grid(row=0, column=0, padx=(0, 15))
        
        # Theme toggle
        self.theme_switch = ctk.CTkSwitch(
            right_frame,
            text="الوضع الداكن",
            font=ctk.CTkFont(size=11),
            command=self._toggle_theme,
            switch_width=50,
            switch_height=25
        )
        self.theme_switch.grid(row=0, column=1)
        
        # Set initial switch state
        if self.settings_manager.display.theme == "dark":
            self.theme_switch.select()
    
    def _start_time_update(self):
        """Start time update timer"""
        self._update_time()
    
    def _update_time(self):
        """Update time display"""
        try:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.time_label.configure(text=current_time)
            
            # Schedule next update
            self.after(1000, self._update_time)
        except:
            pass
    
    def _toggle_theme(self):
        """Toggle application theme"""
        try:
            new_theme = "dark" if self.theme_switch.get() else "light"
            self.theme_manager.switch_theme(new_theme)
            
            # Update colors
            self._update_colors()
            
        except Exception as e:
            print(f"Error toggling theme: {e}")
    
    def _update_colors(self):
        """Update header colors after theme change"""
        colors = self.theme_manager.get_colors()
        
        # Update component colors
        for widget in self.winfo_children():
            if isinstance(widget, ctk.CTkLabel):
                widget.configure(text_color=colors["text_primary"])
    
    def set_page_title(self, title: str):
        """Set page title"""
        self.page_title.configure(text=title)
