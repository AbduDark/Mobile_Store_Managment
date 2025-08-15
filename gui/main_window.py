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
from database.db_manager import DatabaseManager
from utils.arabic_support import setup_arabic_font

class MobileShopApp(ctk.CTk):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        
        # Initialize database
        self.db_manager = DatabaseManager()
        
        # Configure window
        self.title("نظام إدارة محل الموبايلات - Mobile Shop Management")
        self.geometry("1400x900")
        self.minsize(1200, 800)
        
        # Configure grid weight
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Setup Arabic font support
        setup_arabic_font()
        
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
        
        # Logo/Title
        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="محل الموبايلات",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # Subtitle
        self.subtitle_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="نظام الإدارة المتكامل",
            font=ctk.CTkFont(size=14)
        )
        self.subtitle_label.grid(row=1, column=0, padx=20, pady=(0, 20))
        
        # Navigation buttons
        self.dashboard_button = ctk.CTkButton(
            self.sidebar_frame,
            text="🏠 الرئيسية",
            command=self.show_dashboard,
            font=ctk.CTkFont(size=16),
            height=40
        )
        self.dashboard_button.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        
        self.products_button = ctk.CTkButton(
            self.sidebar_frame,
            text="📱 المنتجات",
            command=self.show_products,
            font=ctk.CTkFont(size=16),
            height=40
        )
        self.products_button.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        
        self.sales_button = ctk.CTkButton(
            self.sidebar_frame,
            text="💰 المبيعات",
            command=self.show_sales,
            font=ctk.CTkFont(size=16),
            height=40
        )
        self.sales_button.grid(row=4, column=0, padx=20, pady=10, sticky="ew")
        
        self.customers_button = ctk.CTkButton(
            self.sidebar_frame,
            text="👥 العملاء",
            command=self.show_customers,
            font=ctk.CTkFont(size=16),
            height=40
        )
        self.customers_button.grid(row=5, column=0, padx=20, pady=10, sticky="ew")
        
        self.reports_button = ctk.CTkButton(
            self.sidebar_frame,
            text="📊 التقارير",
            command=self.show_reports,
            font=ctk.CTkFont(size=16),
            height=40
        )
        self.reports_button.grid(row=6, column=0, padx=20, pady=10, sticky="ew")
        
        # Settings section
        self.settings_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="الإعدادات",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.settings_label.grid(row=7, column=0, padx=20, pady=(20, 10))
        
        # Theme switch
        self.theme_switch = ctk.CTkSwitch(
            self.sidebar_frame,
            text="المظهر الداكن",
            command=self.toggle_theme,
            font=ctk.CTkFont(size=12)
        )
        self.theme_switch.grid(row=8, column=0, padx=20, pady=10, sticky="s")
        
        # Version info
        self.version_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="الإصدار 1.0",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        self.version_label.grid(row=9, column=0, padx=20, pady=(10, 20))
    
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
    
    def update_button_states(self, active_button):
        """Update button states to show which is active"""
        buttons = {
            "dashboard": self.dashboard_button,
            "products": self.products_button,
            "sales": self.sales_button,
            "customers": self.customers_button,
            "reports": self.reports_button
        }
        
        for name, button in buttons.items():
            if name == active_button:
                button.configure(fg_color=("gray75", "gray25"))
            else:
                button.configure(fg_color=["#3B8ED0", "#1F6AA5"])
    
    def toggle_theme(self):
        """Toggle between dark and light theme"""
        current_mode = ctk.get_appearance_mode()
        new_mode = "light" if current_mode == "dark" else "dark"
        ctk.set_appearance_mode(new_mode)
    
    def on_closing(self):
        """Handle application closing"""
        if messagebox.askokcancel("إغلاق التطبيق", "هل تريد إغلاق التطبيق؟"):
            self.destroy()

if __name__ == "__main__":
    app = MobileShopApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
