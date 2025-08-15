
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Header Bar Component
شريط العنوان العلوي
"""

import customtkinter as ctk
from datetime import datetime
from typing import Optional
import threading
import time

from src.utils.logger import get_logger

logger = get_logger(__name__)

class HeaderBar(ctk.CTkFrame):
    """Header bar component with shop info and controls"""
    
    def __init__(self, parent, settings_manager, theme_manager):
        super().__init__(parent, height=80, corner_radius=0)
        
        self.settings_manager = settings_manager
        self.theme_manager = theme_manager
        
        # Configure grid
        self.grid_columnconfigure(1, weight=1)
        
        # Variables
        self.current_time = ctk.StringVar()
        self.current_date = ctk.StringVar()
        
        self._create_header()
        self._start_clock()
        
        logger.info("Header bar component initialized")
    
    def _create_header(self):
        """Create header elements"""
        colors = self.theme_manager.get_colors()
        font = self.theme_manager.get_font_config(12)
        title_font = self.theme_manager.get_font_config(16, "bold")
        
        # Left section - Shop info
        left_frame = ctk.CTkFrame(self, fg_color="transparent")
        left_frame.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        
        shop_name = ctk.CTkLabel(
            left_frame,
            text=self.settings_manager.shop_info.name,
            font=title_font,
            text_color=colors["accent"]
        )
        shop_name.grid(row=0, column=0, sticky="w")
        
        if self.settings_manager.shop_info.owner:
            owner_label = ctk.CTkLabel(
                left_frame,
                text=f"المالك: {self.settings_manager.shop_info.owner}",
                font=font,
                text_color=colors["text_secondary"]
            )
            owner_label.grid(row=1, column=0, sticky="w")
        
        # Center section - Search (placeholder)
        center_frame = ctk.CTkFrame(self, fg_color="transparent")
        center_frame.grid(row=0, column=1, padx=20, pady=10, sticky="ew")
        
        # Right section - Date/Time and controls
        right_frame = ctk.CTkFrame(self, fg_color="transparent")
        right_frame.grid(row=0, column=2, padx=20, pady=10, sticky="e")
        
        # Date and time
        self.time_label = ctk.CTkLabel(
            right_frame,
            textvariable=self.current_time,
            font=self.theme_manager.get_english_font_config(14, "bold"),
            text_color=colors["text_primary"]
        )
        self.time_label.grid(row=0, column=0, padx=(0, 20))
        
        self.date_label = ctk.CTkLabel(
            right_frame,
            textvariable=self.current_date,
            font=font,
            text_color=colors["text_secondary"]
        )
        self.date_label.grid(row=1, column=0, padx=(0, 20))
        
        # Theme toggle button
        theme_button = ctk.CTkButton(
            right_frame,
            text="🌙" if self.theme_manager.get_colors() == self.theme_manager.themes["dark"] else "☀️",
            width=40,
            height=40,
            font=("Arial", 16),
            command=self._toggle_theme
        )
        theme_button.grid(row=0, column=1, rowspan=2, padx=10)
    
    def _start_clock(self):
        """Start the clock update thread"""
        def update_clock():
            while True:
                try:
                    now = datetime.now()
                    
                    # Format time (24-hour format)
                    time_str = now.strftime("%H:%M:%S")
                    self.current_time.set(time_str)
                    
                    # Format date in Arabic
                    months_ar = [
                        "يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو",
                        "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"
                    ]
                    
                    days_ar = [
                        "الاثنين", "الثلاثاء", "الأربعاء", "الخميس", 
                        "الجمعة", "السبت", "الأحد"
                    ]
                    
                    day_name = days_ar[now.weekday()]
                    month_name = months_ar[now.month - 1]
                    date_str = f"{day_name}, {now.day} {month_name} {now.year}"
                    
                    self.current_date.set(date_str)
                    
                    time.sleep(1)
                    
                except Exception as e:
                    logger.error(f"Error updating clock: {e}")
                    time.sleep(5)
        
        clock_thread = threading.Thread(target=update_clock, daemon=True)
        clock_thread.start()
    
    def _toggle_theme(self):
        """Toggle between dark and light themes"""
        try:
            current_theme = self.settings_manager.display.theme
            new_theme = "light" if current_theme == "dark" else "dark"
            
            self.theme_manager.switch_theme(new_theme)
            
            # Update theme button icon
            theme_button = None
            for child in self.winfo_children():
                if isinstance(child, ctk.CTkFrame):
                    for grandchild in child.winfo_children():
                        if isinstance(grandchild, ctk.CTkButton) and grandchild.cget("width") == 40:
                            theme_button = grandchild
                            break
            
            if theme_button:
                new_icon = "🌙" if new_theme == "dark" else "☀️"
                theme_button.configure(text=new_icon)
            
            logger.info(f"Theme toggled to: {new_theme}")
            
        except Exception as e:
            logger.error(f"Error toggling theme: {e}")
    
    def update_shop_info(self):
        """Update shop information display"""
        try:
            # Update shop name if changed
            for child in self.winfo_children():
                if isinstance(child, ctk.CTkFrame):
                    for grandchild in child.winfo_children():
                        if isinstance(grandchild, ctk.CTkLabel):
                            # Update the first label (shop name)
                            grandchild.configure(text=self.settings_manager.shop_info.name)
                            break
                    break
        except Exception as e:
            logger.error(f"Error updating shop info: {e}")
