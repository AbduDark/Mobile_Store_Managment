#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Helper Utilities for Mobile Shop Management System
أدوات مساعدة لنظام إدارة محل الموبايلات
"""

import os
import json
import re
from datetime import datetime, date
from typing import Any, Dict, List, Optional, Union
from decimal import Decimal, InvalidOperation

def format_currency(amount: Union[float, int, Decimal], currency: str = "ريال") -> str:
    """
    Format currency amount with proper Arabic formatting
    تنسيق المبلغ المالي بالتنسيق العربي المناسب
    """
    try:
        if isinstance(amount, str):
            amount = float(amount)
        return f"{amount:.2f} {currency}"
    except (ValueError, TypeError):
        return f"0.00 {currency}"

def format_phone_number(phone: str) -> str:
    """
    Format phone number for Saudi Arabia
    تنسيق رقم الهاتف للمملكة العربية السعودية
    """
    if not phone:
        return ""
    
    # Remove all non-digit characters
    phone = re.sub(r'\D', '', phone)
    
    # If starts with 966, format as international
    if phone.startswith('966'):
        return f"+{phone[:3]} {phone[3:5]} {phone[5:8]} {phone[8:]}"
    
    # If starts with 05, format as local
    if phone.startswith('05') and len(phone) == 10:
        return f"{phone[:3]} {phone[3:6]} {phone[6:]}"
    
    # Return as is if doesn't match patterns
    return phone

def validate_email(email: str) -> bool:
    """
    Validate email address format
    التحقق من صحة تنسيق البريد الإلكتروني
    """
    if not email:
        return True  # Empty email is acceptable
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone_number(phone: str) -> bool:
    """
    Validate Saudi phone number format
    التحقق من صحة تنسيق رقم الهاتف السعودي
    """
    if not phone:
        return False
    
    # Remove all non-digit characters
    phone = re.sub(r'\D', '', phone)
    
    # Check for Saudi mobile patterns
    # 05XXXXXXXX (10 digits starting with 05)
    # 9665XXXXXXXX (12 digits starting with 9665)
    saudi_patterns = [
        r'^05\d{8}$',      # 05XXXXXXXX
        r'^9665\d{8}$'     # 9665XXXXXXXX
    ]
    
    return any(re.match(pattern, phone) for pattern in saudi_patterns)

def validate_barcode(barcode: str) -> bool:
    """
    Validate barcode format (basic validation)
    التحقق من صحة تنسيق الباركود
    """
    if not barcode:
        return True  # Empty barcode is acceptable
    
    # Basic validation: alphanumeric, length between 4-20
    return re.match(r'^[A-Za-z0-9]{4,20}$', barcode) is not None

def validate_price(price: Union[str, float, int]) -> bool:
    """
    Validate price value
    التحقق من صحة قيمة السعر
    """
    try:
        price_val = float(price) if isinstance(price, str) else price
        return price_val >= 0
    except (ValueError, TypeError):
        return False

def format_datetime(dt: Union[datetime, str], format_type: str = "full") -> str:
    """
    Format datetime for Arabic display
    تنسيق التاريخ والوقت للعرض بالعربية
    """
    if isinstance(dt, str):
        try:
            # Try to parse ISO format
            if 'T' in dt:
                dt = datetime.fromisoformat(dt.replace('Z', '+00:00'))
            else:
                dt = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return dt
    
    if not isinstance(dt, datetime):
        return str(dt)
    
    if format_type == "date":
        return dt.strftime('%Y-%m-%d')
    elif format_type == "time":
        return dt.strftime('%H:%M')
    elif format_type == "short":
        return dt.strftime('%Y-%m-%d %H:%M')
    else:  # full
        return dt.strftime('%Y-%m-%d %H:%M:%S')

def calculate_profit_margin(selling_price: float, purchase_price: float) -> float:
    """
    Calculate profit margin percentage
    حساب نسبة هامش الربح
    """
    try:
        if purchase_price == 0:
            return 0.0
        return ((selling_price - purchase_price) / purchase_price) * 100
    except (ValueError, TypeError, ZeroDivisionError):
        return 0.0

def calculate_discount_amount(original_price: float, discount_percent: float) -> float:
    """
    Calculate discount amount from percentage
    حساب مبلغ الخصم من النسبة المئوية
    """
    try:
        return (original_price * discount_percent) / 100
    except (ValueError, TypeError):
        return 0.0

def generate_barcode() -> str:
    """
    Generate a simple barcode based on timestamp
    إنشاء باركود بسيط بناءً على الوقت الحالي
    """
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    return f"MB{timestamp}"

def export_to_json(data: Any, filepath: str) -> bool:
    """
    Export data to JSON file
    تصدير البيانات إلى ملف JSON
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Custom JSON encoder for datetime objects
        def json_serializer(obj):
            if isinstance(obj, (datetime, date)):
                return obj.isoformat()
            elif isinstance(obj, Decimal):
                return float(obj)
            raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2, default=json_serializer)
        
        return True
    except Exception:
        return False

def import_from_json(filepath: str) -> Optional[Any]:
    """
    Import data from JSON file
    استيراد البيانات من ملف JSON
    """
    try:
        if not os.path.exists(filepath):
            return None
        
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None

def clean_text_input(text: str) -> str:
    """
    Clean and normalize text input
    تنظيف وتطبيع النص المدخل
    """
    if not text:
        return ""
    
    # Remove extra whitespace and normalize
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Remove potentially harmful characters
    text = re.sub(r'[<>\"\'&]', '', text)
    
    return text

def is_arabic_text(text: str) -> bool:
    """
    Check if text contains Arabic characters
    التحقق من وجود نص عربي
    """
    if not text:
        return False
    
    arabic_pattern = r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]'
    return bool(re.search(arabic_pattern, text))

def get_file_size(filepath: str) -> str:
    """
    Get human-readable file size
    الحصول على حجم الملف بصيغة قابلة للقراءة
    """
    try:
        if not os.path.exists(filepath):
            return "غير موجود"
        
        size = os.path.getsize(filepath)
        
        if size < 1024:
            return f"{size} بايت"
        elif size < 1024**2:
            return f"{size/1024:.1f} كيلوبايت"
        elif size < 1024**3:
            return f"{size/(1024**2):.1f} ميجابايت"
        else:
            return f"{size/(1024**3):.1f} جيجابايت"
    except Exception:
        return "غير معروف"

def backup_database(db_path: str, backup_dir: str) -> Optional[str]:
    """
    Create a backup copy of the database
    إنشاء نسخة احتياطية من قاعدة البيانات
    """
    try:
        if not os.path.exists(db_path):
            return None
        
        # Create backup directory if it doesn't exist
        os.makedirs(backup_dir, exist_ok=True)
        
        # Generate backup filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f"mobile_shop_backup_{timestamp}.db"
        backup_path = os.path.join(backup_dir, backup_filename)
        
        # Copy database file
        import shutil
        shutil.copy2(db_path, backup_path)
        
        return backup_path
    except Exception:
        return None

def parse_csv_line(line: str, delimiter: str = ',') -> List[str]:
    """
    Parse CSV line handling quoted fields
    تحليل سطر CSV مع معالجة الحقول المقتبسة
    """
    import csv
    from io import StringIO
    
    try:
        reader = csv.reader(StringIO(line), delimiter=delimiter)
        return next(reader)
    except Exception:
        return line.split(delimiter)

def format_number_arabic(number: Union[int, float]) -> str:
    """
    Format number with Arabic/Middle Eastern formatting
    تنسيق الرقم بالتنسيق العربي/الشرق أوسطي
    """
    try:
        # Convert to float for consistent formatting
        num = float(number)
        
        # Format with thousands separator
        if num == int(num):
            return f"{int(num):,}".replace(',', '،')
        else:
            return f"{num:,.2f}".replace(',', '،')
    except (ValueError, TypeError):
        return str(number)

def get_stock_status_text(quantity: int, min_quantity: int) -> tuple[str, str]:
    """
    Get stock status text and color based on quantity
    الحصول على نص ولون حالة المخزون بناءً على الكمية
    
    Returns:
        tuple: (status_text, color)
    """
    if quantity == 0:
        return ("نفد المخزون", "red")
    elif quantity <= min_quantity:
        return ("مخزون منخفض", "orange")
    else:
        return ("متوفر", "green")

def truncate_text(text: str, max_length: int = 50, suffix: str = "...") -> str:
    """
    Truncate text to specified length with suffix
    اقتطاع النص إلى طول محدد مع إضافة لاحقة
    """
    if not text or len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix

def create_directory_if_not_exists(directory: str) -> bool:
    """
    Create directory if it doesn't exist
    إنشاء مجلد إذا لم يكن موجوداً
    """
    try:
        os.makedirs(directory, exist_ok=True)
        return True
    except Exception:
        return False

def safe_float_conversion(value: Any, default: float = 0.0) -> float:
    """
    Safely convert value to float with default fallback
    تحويل آمن للقيمة إلى رقم عشري مع قيمة افتراضية
    """
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (ValueError, TypeError):
        return default

def safe_int_conversion(value: Any, default: int = 0) -> int:
    """
    Safely convert value to integer with default fallback
    تحويل آمن للقيمة إلى رقم صحيح مع قيمة افتراضية
    """
    try:
        if value is None or value == "":
            return default
        return int(float(value))  # Convert to float first to handle "10.0"
    except (ValueError, TypeError):
        return default
