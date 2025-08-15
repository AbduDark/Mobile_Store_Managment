#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Settings Manager
مدير الإعدادات
"""

import json
from pathlib import Path
from typing import Any, Dict
from dataclasses import dataclass, asdict
from datetime import datetime

from src.utils.logger import get_logger

logger = get_logger(__name__)

@dataclass
class ShopInfo:
    """Shop information settings"""
    name: str = "المحل الذكي"
    owner: str = ""
    phone: str = ""
    email: str = ""
    address: str = ""
    tax_number: str = ""
    logo_path: str = ""

@dataclass
class DisplaySettings:
    """Display settings"""
    theme: str = "dark"
    language: str = "ar"
    font_size: int = 12
    show_grid: bool = True
    items_per_page: int = 50

@dataclass
class BusinessSettings:
    """Business settings"""
    currency: str = "ريال"
    currency_symbol: str = "ر.س"
    tax_rate: float = 15.0
    default_discount: float = 0.0
    backup_interval_days: int = 7
    low_stock_alert: bool = True

class SettingsManager:
    """Settings management class"""

    def __init__(self, settings_file: str = "data/settings.json"):
        """Initialize settings manager"""
        self.settings_file = Path(settings_file)
        self.settings_file.parent.mkdir(parents=True, exist_ok=True)

        # Default settings
        self.shop_info = ShopInfo()
        self.display = DisplaySettings()
        self.business = BusinessSettings()

        self._load_settings()
        logger.info("Settings manager initialized")

    def _load_settings(self):
        """Load settings from file"""
        try:
            if self.settings_file.exists():
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                # Load shop info
                if 'shop_info' in data:
                    shop_data = data['shop_info']
                    for key, value in shop_data.items():
                        if hasattr(self.shop_info, key):
                            setattr(self.shop_info, key, value)

                # Load display settings
                if 'display' in data:
                    display_data = data['display']
                    for key, value in display_data.items():
                        if hasattr(self.display, key):
                            setattr(self.display, key, value)

                # Load business settings
                if 'business' in data:
                    business_data = data['business']
                    for key, value in business_data.items():
                        if hasattr(self.business, key):
                            setattr(self.business, key, value)

                logger.info("Settings loaded successfully")
            else:
                # Create default settings file
                self._save_settings()
                logger.info("Created default settings file")

        except Exception as e:
            logger.error(f"Error loading settings: {e}")
            # Use default settings

    def _save_settings(self):
        """Save settings to file"""
        try:
            settings_data = {
                'shop_info': asdict(self.shop_info),
                'display': asdict(self.display),
                'business': asdict(self.business),
                'last_updated': datetime.now().isoformat()
            }

            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings_data, f, indent=2, ensure_ascii=False)

            logger.info("Settings saved successfully")

        except Exception as e:
            logger.error(f"Error saving settings: {e}")

    def update_shop_info(self, **kwargs):
        """Update shop information"""
        for key, value in kwargs.items():
            if hasattr(self.shop_info, key):
                setattr(self.shop_info, key, value)
        self._save_settings()

    def update_display_settings(self, **kwargs):
        """Update display settings"""
        for key, value in kwargs.items():
            if hasattr(self.display, key):
                setattr(self.display, key, value)
        self._save_settings()

    def update_business_settings(self, **kwargs):
        """Update business settings"""
        for key, value in kwargs.items():
            if hasattr(self.business, key):
                setattr(self.business, key, value)
        self._save_settings()

    def get_setting(self, category: str, key: str, default: Any = None) -> Any:
        """Get specific setting value"""
        try:
            if category == "shop_info":
                return getattr(self.shop_info, key, default)
            elif category == "display":
                return getattr(self.display, key, default)
            elif category == "business":
                return getattr(self.business, key, default)
            else:
                return default
        except:
            return default

    def update_setting(self, key: str, value: Any):
        """Update a single setting (for backward compatibility)"""
        # Try to find the setting in different categories
        if hasattr(self.display, key):
            setattr(self.display, key, value)
        elif hasattr(self.business, key):
            setattr(self.business, key, value)
        elif hasattr(self.shop_info, key):
            setattr(self.shop_info, key, value)

        self._save_settings()

    def get_all_settings(self) -> Dict[str, Any]:
        """Get all settings as dictionary"""
        return {
            'shop_info': asdict(self.shop_info),
            'display': asdict(self.display),
            'business': asdict(self.business)
        }

    def reset_to_defaults(self):
        """Reset all settings to defaults"""
        self.shop_info = ShopInfo()
        self.display = DisplaySettings()
        self.business = BusinessSettings()
        self._save_settings()
        logger.info("Settings reset to defaults")