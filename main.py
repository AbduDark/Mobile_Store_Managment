#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام إدارة محل الموبايلات
Mobile Shop Management System
Main application entry point
"""

import customtkinter as ctk
import sys
import os
from datetime import datetime

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.db_manager import DatabaseManager
from gui.main_window import MobileShopApp
from config.settings import AppSettings

# Configure CustomTkinter appearance
ctk.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

def main():
    """Main application entry point"""
    try:
        # Initialize database
        print("تهيئة قاعدة البيانات...")
        db_manager = DatabaseManager()
        
        # Create main application
        print("بدء تشغيل التطبيق...")
        app = MobileShopApp()
        
        # Start the application
        app.mainloop()
        
    except Exception as e:
        print(f"خطأ في تشغيل التطبيق: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
