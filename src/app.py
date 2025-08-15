
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main Application Class
فئة التطبيق الرئيسية
"""

import customtkinter as ctk
from tkinter import messagebox
import sys
from pathlib import Path

from src.core.database import DatabaseManager
from src.core.settings import SettingsManager
from src.core.theme import ThemeManager
from src.ui.main_window import MainWindow
from src.utils.logger import get_logger

logger = get_logger(__name__)

class SmartShopApp:
    """Main application class"""
    
    def __init__(self):
        """Initialize the application"""
        self.db_manager = None
        self.settings_manager = None
        self.theme_manager = None
        self.main_window = None
        
        self._initialize_core_components()
    
    def _initialize_core_components(self):
        """Initialize core application components"""
        try:
            # Initialize settings manager
            self.settings_manager = SettingsManager()
            logger.info("Settings manager initialized")
            
            # Initialize database manager
            self.db_manager = DatabaseManager()
            logger.info("Database manager initialized")
            
            # Initialize theme manager
            self.theme_manager = ThemeManager(self.settings_manager)
            logger.info("Theme manager initialized")
            
        except Exception as e:
            logger.error(f"Error initializing core components: {e}")
            raise
    
    def run(self):
        """Run the application"""
        try:
            # Create and show main window
            self.main_window = MainWindow(
                db_manager=self.db_manager,
                settings_manager=self.settings_manager,
                theme_manager=self.theme_manager
            )
            
            logger.info("Application started successfully")
            self.main_window.mainloop()
            
        except Exception as e:
            logger.error(f"Error running application: {e}")
            messagebox.showerror(
                "خطأ في التطبيق",
                f"حدث خطأ في تشغيل التطبيق:\n{e}"
            )
        finally:
            self._cleanup()
    
    def _cleanup(self):
        """Cleanup resources before closing"""
        try:
            if self.db_manager:
                self.db_manager.close()
            logger.info("Application cleanup completed")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
