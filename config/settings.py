#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Application Settings and Configuration for Mobile Shop Management System
إعدادات وتكوين التطبيق لنظام إدارة محل الموبايلات
"""

import os
import json
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class ShopSettings:
    """Shop information settings - إعدادات معلومات المحل"""
    name: str = "محل الموبايلات"
    name_english: str = "Mobile Shop"
    address: str = ""
    phone: str = ""
    email: str = ""
    tax_number: str = ""
    commercial_record: str = ""
    logo_path: str = ""

@dataclass
class CurrencySettings:
    """Currency settings - إعدادات العملة"""
    symbol: str = "ريال"
    code: str = "SAR"
    decimal_places: int = 2
    thousands_separator: str = "،"
    decimal_separator: str = "."

@dataclass
class TaxSettings:
    """Tax configuration - إعدادات الضريبة"""
    vat_rate: float = 15.0  # VAT rate in percentage
    vat_enabled: bool = True
    include_tax_in_price: bool = False
    tax_number: str = ""

@dataclass
class DisplaySettings:
    """Display and UI settings - إعدادات العرض والواجهة"""
    theme: str = "dark"  # dark, light, system
    language: str = "ar"  # ar, en
    font_family: str = "Tahoma"
    font_size: int = 12
    show_arabic_numbers: bool = True
    date_format: str = "%Y-%m-%d"
    time_format: str = "%H:%M"

@dataclass
class InventorySettings:
    """Inventory management settings - إعدادات إدارة المخزون"""
    low_stock_threshold: int = 5
    enable_low_stock_alerts: bool = True
    allow_negative_stock: bool = False
    auto_generate_barcode: bool = True
    barcode_prefix: str = "MB"

@dataclass
class SalesSettings:
    """Sales configuration - إعدادات المبيعات"""
    default_payment_method: str = "نقداً"
    enable_customer_loyalty: bool = True
    loyalty_points_rate: float = 1.0  # Points per currency unit
    loyalty_redemption_rate: float = 0.1  # Currency per point
    enable_discounts: bool = True
    max_discount_percent: float = 50.0
    require_customer_info: bool = False

@dataclass
class PrintingSettings:
    """Printing configuration - إعدادات الطباعة"""
    printer_name: str = ""
    paper_size: str = "A4"  # A4, A5, 80mm, 58mm
    print_logo: bool = True
    print_barcode: bool = True
    copies_count: int = 1
    auto_print: bool = False

@dataclass
class BackupSettings:
    """Backup configuration - إعدادات النسخ الاحتياطي"""
    auto_backup: bool = True
    backup_interval_days: int = 7
    backup_location: str = ""
    max_backups_count: int = 10
    cloud_backup_enabled: bool = False
    cloud_service: str = ""  # google_drive, onedrive

@dataclass
class SecuritySettings:
    """Security configuration - إعدادات الأمان"""
    require_login: bool = False
    session_timeout_minutes: int = 60
    encrypt_backup: bool = False
    audit_log_enabled: bool = True
    password_min_length: int = 6

class AppSettings:
    """Main application settings manager"""
    
    def __init__(self, config_dir: str = None):
        if config_dir is None:
            # Default config directory in user's documents
            config_dir = os.path.join(os.path.expanduser("~"), "Documents", "MobileShop")
        
        self.config_dir = config_dir
        self.config_file = os.path.join(config_dir, "settings.json")
        
        # Initialize settings with defaults
        self.shop = ShopSettings()
        self.currency = CurrencySettings()
        self.tax = TaxSettings()
        self.display = DisplaySettings()
        self.inventory = InventorySettings()
        self.sales = SalesSettings()
        self.printing = PrintingSettings()
        self.backup = BackupSettings()
        self.security = SecuritySettings()
        
        # Load settings from file if exists
        self.load_settings()
    
    def ensure_config_directory(self):
        """Ensure configuration directory exists"""
        try:
            os.makedirs(self.config_dir, exist_ok=True)
            return True
        except Exception as e:
            print(f"خطأ في إنشاء مجلد الإعدادات: {e}")
            return False
    
    def load_settings(self):
        """Load settings from configuration file"""
        try:
            if not os.path.exists(self.config_file):
                # Create default settings file
                self.save_settings()
                return
            
            with open(self.config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Load each settings section
            if 'shop' in data:
                self.shop = ShopSettings(**data['shop'])
            
            if 'currency' in data:
                self.currency = CurrencySettings(**data['currency'])
            
            if 'tax' in data:
                self.tax = TaxSettings(**data['tax'])
            
            if 'display' in data:
                self.display = DisplaySettings(**data['display'])
            
            if 'inventory' in data:
                self.inventory = InventorySettings(**data['inventory'])
            
            if 'sales' in data:
                self.sales = SalesSettings(**data['sales'])
            
            if 'printing' in data:
                self.printing = PrintingSettings(**data['printing'])
            
            if 'backup' in data:
                self.backup = BackupSettings(**data['backup'])
                # Set default backup location if empty
                if not self.backup.backup_location:
                    self.backup.backup_location = os.path.join(self.config_dir, "backups")
            
            if 'security' in data:
                self.security = SecuritySettings(**data['security'])
            
            print("تم تحميل الإعدادات بنجاح")
            
        except Exception as e:
            print(f"خطأ في تحميل الإعدادات: {e}")
            # Use default settings if loading fails
            self._reset_to_defaults()
    
    def save_settings(self):
        """Save current settings to configuration file"""
        try:
            if not self.ensure_config_directory():
                return False
            
            # Convert settings to dictionary
            settings_data = {
                'shop': asdict(self.shop),
                'currency': asdict(self.currency),
                'tax': asdict(self.tax),
                'display': asdict(self.display),
                'inventory': asdict(self.inventory),
                'sales': asdict(self.sales),
                'printing': asdict(self.printing),
                'backup': asdict(self.backup),
                'security': asdict(self.security),
                'last_updated': datetime.now().isoformat()
            }
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(settings_data, f, ensure_ascii=False, indent=2)
            
            print("تم حفظ الإعدادات بنجاح")
            return True
            
        except Exception as e:
            print(f"خطأ في حفظ الإعدادات: {e}")
            return False
    
    def _reset_to_defaults(self):
        """Reset all settings to defaults"""
        self.shop = ShopSettings()
        self.currency = CurrencySettings()
        self.tax = TaxSettings()
        self.display = DisplaySettings()
        self.inventory = InventorySettings()
        self.sales = SalesSettings()
        self.printing = PrintingSettings()
        self.backup = BackupSettings()
        self.security = SecuritySettings()
        
        # Set default backup location
        self.backup.backup_location = os.path.join(self.config_dir, "backups")
    
    def get_backup_directory(self) -> str:
        """Get the backup directory path"""
        if not self.backup.backup_location:
            self.backup.backup_location = os.path.join(self.config_dir, "backups")
        
        # Ensure backup directory exists
        os.makedirs(self.backup.backup_location, exist_ok=True)
        return self.backup.backup_location
    
    def get_invoice_template_data(self) -> Dict[str, Any]:
        """Get data for invoice template"""
        return {
            'shop_name': self.shop.name,
            'shop_name_english': self.shop.name_english,
            'shop_address': self.shop.address,
            'shop_phone': self.shop.phone,
            'shop_email': self.shop.email,
            'tax_number': self.tax.tax_number or self.shop.tax_number,
            'commercial_record': self.shop.commercial_record,
            'currency_symbol': self.currency.symbol,
            'vat_rate': self.tax.vat_rate,
            'vat_enabled': self.tax.vat_enabled,
            'include_tax_in_price': self.tax.include_tax_in_price
        }
    
    def get_display_settings(self) -> Dict[str, Any]:
        """Get display settings for UI configuration"""
        return {
            'theme': self.display.theme,
            'language': self.display.language,
            'font_family': self.display.font_family,
            'font_size': self.display.font_size,
            'show_arabic_numbers': self.display.show_arabic_numbers,
            'date_format': self.display.date_format,
            'time_format': self.display.time_format
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
    
    def update_tax_settings(self, **kwargs):
        """Update tax settings"""
        for key, value in kwargs.items():
            if hasattr(self.tax, key):
                setattr(self.tax, key, value)
        self.save_settings()
    
    def update_inventory_settings(self, **kwargs):
        """Update inventory settings"""
        for key, value in kwargs.items():
            if hasattr(self.inventory, key):
                setattr(self.inventory, key, value)
        self.save_settings()
    
    def is_first_run(self) -> bool:
        """Check if this is the first run of the application"""
        return not os.path.exists(self.config_file)
    
    def export_settings(self, export_path: str) -> bool:
        """Export settings to a file"""
        try:
            settings_data = {
                'shop': asdict(self.shop),
                'currency': asdict(self.currency),
                'tax': asdict(self.tax),
                'display': asdict(self.display),
                'inventory': asdict(self.inventory),
                'sales': asdict(self.sales),
                'printing': asdict(self.printing),
                'backup': asdict(self.backup),
                'security': asdict(self.security),
                'export_date': datetime.now().isoformat(),
                'version': "1.0"
            }
            
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(settings_data, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"خطأ في تصدير الإعدادات: {e}")
            return False
    
    def import_settings(self, import_path: str) -> bool:
        """Import settings from a file"""
        try:
            if not os.path.exists(import_path):
                return False
            
            with open(import_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Import each settings section (excluding sensitive data)
            safe_sections = ['shop', 'currency', 'tax', 'display', 'inventory', 'sales', 'printing']
            
            for section in safe_sections:
                if section in data:
                    section_class = getattr(self, section).__class__
                    setattr(self, section, section_class(**data[section]))
            
            # Save imported settings
            self.save_settings()
            return True
            
        except Exception as e:
            print(f"خطأ في استيراد الإعدادات: {e}")
            return False

# Global settings instance
_app_settings = None

def get_app_settings() -> AppSettings:
    """Get the global application settings instance"""
    global _app_settings
    if _app_settings is None:
        _app_settings = AppSettings()
    return _app_settings

def initialize_settings(config_dir: str = None) -> AppSettings:
    """Initialize application settings with custom config directory"""
    global _app_settings
    _app_settings = AppSettings(config_dir)
    return _app_settings

# Constants for application
APP_NAME = "نظام إدارة محل الموبايلات"
APP_NAME_ENGLISH = "Mobile Shop Management System"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Mobile Shop Management Team"

# Default categories and data
DEFAULT_CATEGORIES = [
    "هواتف ذكية جديدة",
    "هواتف مستعملة",
    "إكسسوارات",
    "قطع غيار",
    "بطاقات شحن",
    "أخرى"
]

DEFAULT_BRANDS = [
    "Apple",
    "Samsung",
    "Xiaomi",
    "Huawei",
    "Oppo",
    "Vivo",
    "OnePlus",
    "Nokia",
    "Realme",
    "Honor",
    "أخرى"
]

DEFAULT_PAYMENT_METHODS = [
    "نقداً",
    "تحويل",
    "بطاقة ائتمان",
    "تقسيط",
    "نقاط الولاء"
]

DEFAULT_PHONE_CONDITIONS = [
    "جديد",
    "مستعمل ممتاز",
    "مستعمل جيد",
    "مستعمل عادي",
    "يحتاج صيانة"
]
