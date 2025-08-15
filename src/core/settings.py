
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Settings Manager
مدير الإعدادات
"""

import json
from pathlib import Path
from typing import Dict, Any
from dataclasses import dataclass, asdict

from src.utils.logger import get_logger

logger = get_logger(__name__)

@dataclass
class ShopSettings:
    """Shop information settings"""
    name: str = "المحل الذكي"
    name_english: str = "Smart Shop"
    address: str = ""
    phone: str = ""
    email: str = ""
    website: str = ""
    tax_number: str = ""
    commercial_record: str = ""
    logo_path: str = ""
    currency: str = "ريال سعودي"
    currency_symbol: str = "ر.س"

@dataclass
class DisplaySettings:
    """Display and UI settings"""
    theme: str = "dark"
    language: str = "ar"
    font_size: int = 12
    show_sidebar: bool = True
    show_toolbar: bool = True
    auto_refresh: bool = True
    refresh_interval: int = 30

@dataclass
class BusinessSettings:
    """Business logic settings"""
    tax_rate: float = 15.0
    default_payment_method: str = "نقد"
    enable_loyalty_points: bool = True
    loyalty_points_rate: float = 1.0
    min_stock_alert: bool = True
    auto_backup: bool = True
    backup_interval_hours: int = 24

class SettingsManager:
    """Settings manager for application configuration"""
    
    def __init__(self, settings_file: str = None):
        """Initialize settings manager"""
        if settings_file is None:
            settings_file = Path("data/settings.json")
        
        self.settings_file = Path(settings_file)
        self.settings_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize settings
        self.shop = ShopSettings()
        self.display = DisplaySettings()
        self.business = BusinessSettings()
        
        # Load existing settings
        self.load_settings()
        
        logger.info("Settings manager initialized")
    
    def load_settings(self):
        """Load settings from file"""
        try:
            if not self.settings_file.exists():
                self.save_settings()
                return
            
            with open(self.settings_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Load shop settings
            if 'shop' in data:
                shop_data = data['shop']
                self.shop = ShopSettings(**{k: v for k, v in shop_data.items() 
                                          if k in ShopSettings.__dataclass_fields__})
            
            # Load display settings
            if 'display' in data:
                display_data = data['display']
                self.display = DisplaySettings(**{k: v for k, v in display_data.items() 
                                                if k in DisplaySettings.__dataclass_fields__})
            
            # Load business settings
            if 'business' in data:
                business_data = data['business']
                self.business = BusinessSettings(**{k: v for k, v in business_data.items() 
                                                  if k in BusinessSettings.__dataclass_fields__})
            
            logger.info("Settings loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading settings: {e}")
            # Use default settings if loading fails
    
    def save_settings(self):
        """Save current settings to file"""
        try:
            settings_data = {
                'shop': asdict(self.shop),
                'display': asdict(self.display),
                'business': asdict(self.business),
                'last_updated': str(Path(__file__).stat().st_mtime)
            }
            
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings_data, f, ensure_ascii=False, indent=2)
            
            logger.info("Settings saved successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error saving settings: {e}")
            return False
    
    def get_all_settings(self) -> Dict[str, Any]:
        """Get all settings as dictionary"""
        return {
            'shop': asdict(self.shop),
            'display': asdict(self.display),
            'business': asdict(self.business)
        }
    
    def update_shop_settings(self, **kwargs):
        """Update shop settings"""
        for key, value in kwargs.items():
            if hasattr(self.shop, key):
                setattr(self.shop, key, value)
        self.save_settings()
    
    def update_display_settings(self, **kwargs):
        """Update display settings"""
        for key, value in kwargs.items():
            if hasattr(self.display, key):
                setattr(self.display, key, value)
        self.save_settings()
    
    def update_business_settings(self, **kwargs):
        """Update business settings"""
        for key, value in kwargs.items():
            if hasattr(self.business, key):
                setattr(self.business, key, value)
        self.save_settings()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Settings Manager
مدير الإعدادات
"""

import json
import os
from pathlib import Path
from typing import Dict, Any
from dataclasses import dataclass, asdict

from src.utils.logger import get_logger

logger = get_logger(__name__)

@dataclass
class AppSettings:
    """Application settings data model"""
    # Shop information
    shop_name: str = "المحل الذكي"
    shop_address: str = ""
    shop_phone: str = ""
    shop_email: str = ""
    
    # Display settings
    theme: str = "dark"  # dark, light, system
    language: str = "ar"  # ar, en
    font_size: int = 12
    
    # Business settings
    currency: str = "ريال"
    tax_rate: float = 0.15
    default_discount: float = 0.0
    
    # System settings
    backup_enabled: bool = True
    auto_backup_days: int = 7
    max_recent_items: int = 50

class SettingsManager:
    """Settings management class"""
    
    def __init__(self, settings_file: str = "data/settings.json"):
        """Initialize settings manager"""
        self.settings_file = settings_file
        self.settings = AppSettings()
        
        # Ensure data directory exists
        Path(self.settings_file).parent.mkdir(parents=True, exist_ok=True)
        
        self.load_settings()
    
    def load_settings(self):
        """Load settings from file"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    settings_dict = json.load(f)
                    
                # Update settings with loaded values
                for key, value in settings_dict.items():
                    if hasattr(self.settings, key):
                        setattr(self.settings, key, value)
                
                logger.info("Settings loaded successfully")
            else:
                # Create default settings file
                self.save_settings()
                logger.info("Created default settings file")
                
        except Exception as e:
            logger.error(f"Error loading settings: {e}")
            # Use default settings on error
    
    def save_settings(self):
        """Save settings to file"""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(self.settings), f, ensure_ascii=False, indent=2)
            
            logger.info("Settings saved successfully")
            
        except Exception as e:
            logger.error(f"Error saving settings: {e}")
    
    def get_setting(self, key: str, default=None):
        """Get a specific setting value"""
        return getattr(self.settings, key, default)
    
    def update_setting(self, key: str, value: Any):
        """Update a specific setting"""
        if hasattr(self.settings, key):
            setattr(self.settings, key, value)
            self.save_settings()
            logger.info(f"Updated setting {key} to {value}")
        else:
            logger.warning(f"Unknown setting key: {key}")
    
    def update_multiple_settings(self, settings_dict: Dict[str, Any]):
        """Update multiple settings at once"""
        for key, value in settings_dict.items():
            if hasattr(self.settings, key):
                setattr(self.settings, key, value)
        
        self.save_settings()
        logger.info("Updated multiple settings")
    
    def reset_to_defaults(self):
        """Reset all settings to defaults"""
        self.settings = AppSettings()
        self.save_settings()
        logger.info("Settings reset to defaults")
