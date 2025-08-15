#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main Window for Mobile Shop Management System
النافذة الرئيسية لنظام إدارة محل الموبايلات
"""

import customtkinter as ctk
from tkinter import messagebox
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gui.dashboard import Dashboard
from gui.products_window import ProductsWindow
from gui.sales_window import SalesWindow
from gui.customers_window import CustomersWindow
from gui.reports_window import ReportsWindow
from gui.settings_window import SettingsWindow
from database.db_manager import DatabaseManager
from utils.arabic_support import (
    setup_arabic_font, create_title_font, create_heading_font, 
    create_button_font, create_body_font, get_font_manager
)
from config.settings import get_app_settings

class MobileShopApp(ctk.CTk):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        
        # Initialize database and settings
        self.db_manager = DatabaseManager()
        self.app_settings = get_app_settings()
        
        # Configure window
        self.title("نظام إدارة محل الموبايلات - Mobile Shop Management")
        self.geometry("1400x900")
        self.minsize(1200, 800)
        
        # Configure grid weight
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Setup Arabic font support
        setup_arabic_font()
        
        # Set initial theme from settings
        ctk.set_appearance_mode(self.app_settings.display.theme)
        
        # Create UI
        self.create_sidebar()
        self.create_main_content()
        
        # Show dashboard by default
        self.show_dashboard()
    
    def create_sidebar(self):
        """Create the sidebar navigation"""
        # Sidebar frame
        self.sidebar_frame = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(8, weight=1)
        
        # Logo/Title with enhanced styling
        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="محل الموبايلات",
            font=create_title_font(32),
            text_color=("#1f538d", "#3b8ed0")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(25, 10))
        
        # Subtitle with better font
        self.subtitle_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="نظام الإدارة المتكامل",
            font=create_body_font(14),
            text_color=("gray50", "gray70")
        )
        self.subtitle_label.grid(row=1, column=0, padx=20, pady=(0, 25))
        
        # Navigation buttons with enhanced styling
        self.dashboard_button = ctk.CTkButton(
            self.sidebar_frame,
            text="🏠 الرئيسية",
            command=self.show_dashboard,
            font=create_button_font(16),
            height=50,
            corner_radius=15,
            hover_color=("#106ba3", "#144870"),
            fg_color=("#3B8ED0", "#1F6AA5"),
            text_color=("white", "white")
        )
        self.dashboard_button.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        
        self.products_button = ctk.CTkButton(
            self.sidebar_frame,
            text="📱 المنتجات",
            command=self.show_products,
            font=create_button_font(16),
            height=50,
            corner_radius=15,
            hover_color=("#106ba3", "#144870"),
            fg_color=("#3B8ED0", "#1F6AA5"),
            text_color=("white", "white")
        )
        self.products_button.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        
        self.sales_button = ctk.CTkButton(
            self.sidebar_frame,
            text="💰 المبيعات",
            command=self.show_sales,
            font=create_button_font(16),
            height=50,
            corner_radius=15,
            hover_color=("#106ba3", "#144870"),
            fg_color=("#3B8ED0", "#1F6AA5"),
            text_color=("white", "white")
        )
        self.sales_button.grid(row=4, column=0, padx=20, pady=10, sticky="ew")
        
        self.customers_button = ctk.CTkButton(
            self.sidebar_frame,
            text="👥 العملاء",
            command=self.show_customers,
            font=create_button_font(16),
            height=50,
            corner_radius=15,
            hover_color=("#106ba3", "#144870"),
            fg_color=("#3B8ED0", "#1F6AA5"),
            text_color=("white", "white")
        )
        self.customers_button.grid(row=5, column=0, padx=20, pady=10, sticky="ew")
        
        self.reports_button = ctk.CTkButton(
            self.sidebar_frame,
            text="📊 التقارير",
            command=self.show_reports,
            font=create_button_font(16),
            height=50,
            corner_radius=15,
            hover_color=("#106ba3", "#144870"),
            fg_color=("#3B8ED0", "#1F6AA5"),
            text_color=("white", "white")
        )
        self.reports_button.grid(row=6, column=0, padx=20, pady=10, sticky="ew")
        
        # Settings button
        self.settings_button = ctk.CTkButton(
            self.sidebar_frame,
            text="⚙️ الإعدادات",
            command=self.show_settings,
            font=create_button_font(16),
            height=50,
            corner_radius=15,
            hover_color=("#106ba3", "#144870"),
            fg_color=("#3B8ED0", "#1F6AA5"),
            text_color=("white", "white")
        )
        self.settings_button.grid(row=7, column=0, padx=20, pady=10, sticky="ew")
        
        # Settings section
        self.settings_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="التحكم",
            font=create_heading_font(18)
        )
        self.settings_label.grid(row=8, column=0, padx=20, pady=(40, 20))
        
        # Theme switch with better styling
        self.theme_switch = ctk.CTkSwitch(
            self.sidebar_frame,
            text="المظهر الداكن",
            command=self.toggle_theme,
            font=create_body_font(14),
            switch_width=60,
            switch_height=30,
            progress_color=("#3B8ED0", "#1F6AA5")
        )
        
        # Set initial switch state
        if self.app_settings.display.theme == "dark":
            self.theme_switch.select()
        else:
            self.theme_switch.deselect()
            
        self.theme_switch.grid(row=9, column=0, padx=20, pady=10, sticky="s")
        
        # Version info
        self.version_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="الإصدار 1.0.0",
            font=create_button_font(10),
            text_color=("gray50", "gray60")
        )
        self.version_label.grid(row=10, column=0, padx=20, pady=(20, 20))
    
    def create_main_content(self):
        """Create the main content area"""
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        # Current content frame
        self.current_frame = None
    
    def clear_main_content(self):
        """Clear the main content area"""
        if self.current_frame:
            self.current_frame.destroy()
            self.current_frame = None
    
    def show_dashboard(self):
        """Show the dashboard"""
        self.clear_main_content()
        self.current_frame = Dashboard(self.main_frame, self.db_manager)
        self.current_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.update_button_states("dashboard")
    
    def show_products(self):
        """Show the products window"""
        self.clear_main_content()
        self.current_frame = ProductsWindow(self.main_frame, self.db_manager)
        self.current_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.update_button_states("products")
    
    def show_sales(self):
        """Show the sales window"""
        self.clear_main_content()
        self.current_frame = SalesWindow(self.main_frame, self.db_manager)
        self.current_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.update_button_states("sales")
    
    def show_customers(self):
        """Show the customers window"""
        self.clear_main_content()
        self.current_frame = CustomersWindow(self.main_frame, self.db_manager)
        self.current_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.update_button_states("customers")
    
    def show_reports(self):
        """Show the reports window"""
        self.clear_main_content()
        self.current_frame = ReportsWindow(self.main_frame, self.db_manager)
        self.current_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.update_button_states("reports")
    
    def show_settings(self):
        """Show the settings window"""
        self.clear_main_content()
        self.current_frame = SettingsWindow(self.main_frame, self.app_settings, self)
        self.current_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.update_button_states("settings")
    
    def update_button_states(self, active_button):
        """Update button states to show which is active"""
        buttons = {
            "dashboard": self.dashboard_button,
            "products": self.products_button,
            "sales": self.sales_button,
            "customers": self.customers_button,
            "reports": self.reports_button,
            "settings": self.settings_button
        }
        
        for name, button in buttons.items():
            if name == active_button:
                # Active button style
                button.configure(
                    fg_color=("#2b2b2b", "#4a4a4a"),
                    text_color=("#FFFFFF", "#FFFFFF")
                )
            else:
                # Inactive button style
                button.configure(
                    fg_color=("#3B8ED0", "#1F6AA5"),
                    text_color=("white", "white")
                )
    
    def toggle_theme(self):
        """Toggle between dark and light theme"""
        try:
            if self.theme_switch.get():
                new_mode = "dark"
            else:
                new_mode = "light"
            
            # Update appearance
            ctk.set_appearance_mode(new_mode)
            
            # Save to settings
            self.app_settings.display.theme = new_mode
            self.app_settings.save_settings()
            
            # Refresh the interface if needed
            self.after(100, self.refresh_ui_after_theme_change)
            
            print(f"تم تغيير المظهر إلى: {new_mode}")
            
        except Exception as e:
            print(f"خطأ في تغيير المظهر: {e}")
    
    def refresh_ui_after_theme_change(self):
        """Refresh UI elements after theme change"""
        try:
            # Force update the current frame if it exists
            if self.current_frame and hasattr(self.current_frame, 'refresh_theme'):
                self.current_frame.refresh_theme()
        except Exception as e:
            print(f"خطأ في تحديث الواجهة: {e}")
    
    def refresh_theme(self):
        """Refresh the theme from settings"""
        theme = self.app_settings.display.theme
        ctk.set_appearance_mode(theme)
        
        # Update switch state
        if theme == "dark":
            self.theme_switch.select()
        else:
            self.theme_switch.deselect()
    
    def on_closing(self):
        """Handle application closing"""
        if messagebox.askokcancel("إغلاق التطبيق", "هل تريد إغلاق التطبيق؟"):
            self.destroy()

if __name__ == "__main__":
    app = MobileShopApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
