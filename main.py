
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
المحل الذكي - نظام إدارة محل الموبايلات المتطور
Smart Shop - Advanced Mobile Shop Management System
Version 2.0
"""

import sys
import os
import logging
from pathlib import Path
import customtkinter as ctk

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def setup_application():
    """Setup application environment"""
    try:
        # Set CustomTkinter theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Create necessary directories
        directories = [
            'data/database',
            'data/exports',
            'data/backups',
            'data/images',
            'assets/icons',
            'assets/fonts',
            'logs'
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
            
        logger.info("Application setup completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error during application setup: {e}")
        return False

def main():
    """Main application entry point"""
    try:
        logger.info("Starting Smart Mobile Shop Management System v2.0")
        
        # Setup application environment
        if not setup_application():
            logger.error("Failed to setup application environment")
            return 1
        
        # Import and start the main application
        from src.app import SmartShopApp
        
        app = SmartShopApp()
        app.run()
        
        return 0
        
    except Exception as e:
        logger.error(f"Critical error in main application: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
