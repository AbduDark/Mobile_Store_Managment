#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Data Models for Mobile Shop Management System
نماذج البيانات لنظام إدارة محل الموبايلات
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

@dataclass
class Product:
    """Product model - نموذج المنتج"""
    id: Optional[int] = None
    name: str = ""
    brand: str = ""
    model: str = ""
    category: str = ""
    purchase_price: float = 0.0
    selling_price: float = 0.0
    quantity: int = 0
    min_quantity: int = 5
    barcode: str = ""
    description: str = ""
    color: str = ""
    storage: str = ""
    condition: str = "new"
    image_path: str = ""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    @property
    def profit_margin(self) -> float:
        """Calculate profit margin percentage"""
        if self.purchase_price == 0:
            return 0
        return ((self.selling_price - self.purchase_price) / self.purchase_price) * 100
    
    @property
    def is_low_stock(self) -> bool:
        """Check if product is low on stock"""
        return self.quantity <= self.min_quantity

@dataclass
class Customer:
    """Customer model - نموذج العميل"""
    id: Optional[int] = None
    name: str = ""
    phone: str = ""
    email: str = ""
    address: str = ""
    total_purchases: float = 0.0
    loyalty_points: int = 0
    notes: str = ""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

@dataclass
class Sale:
    """Sale model - نموذج البيع"""
    id: Optional[int] = None
    customer_id: Optional[int] = None
    total_amount: float = 0.0
    discount: float = 0.0
    tax: float = 0.0
    payment_method: str = "cash"
    payment_status: str = "paid"
    notes: str = ""
    sale_date: Optional[datetime] = None
    items: List['SaleItem'] = None
    
    def __post_init__(self):
        if self.items is None:
            self.items = []

@dataclass
class SaleItem:
    """Sale item model - نموذج عنصر البيع"""
    id: Optional[int] = None
    sale_id: Optional[int] = None
    product_id: int = 0
    quantity: int = 0
    unit_price: float = 0.0
    total_price: float = 0.0
    product_name: str = ""  # For display purposes

@dataclass
class Service:
    """Service/Repair model - نموذج الصيانة"""
    id: Optional[int] = None
    customer_id: Optional[int] = None
    device_type: str = ""
    device_model: str = ""
    problem_description: str = ""
    estimated_cost: Optional[float] = None
    actual_cost: Optional[float] = None
    status: str = "received"
    technician: str = ""
    received_date: Optional[datetime] = None
    completed_date: Optional[datetime] = None
    notes: str = ""

# Product categories - فئات المنتجات
PRODUCT_CATEGORIES = [
    "هواتف ذكية جديدة",
    "هواتف مستعملة", 
    "إكسسوارات",
    "قطع غيار",
    "بطاقات شحن",
    "أخرى"
]

# Phone brands - العلامات التجارية
PHONE_BRANDS = [
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

# Phone conditions - حالة الهاتف
PHONE_CONDITIONS = [
    "جديد",
    "مستعمل ممتاز",
    "مستعمل جيد", 
    "مستعمل عادي",
    "يحتاج صيانة"
]

# Payment methods - طرق الدفع
PAYMENT_METHODS = [
    "نقداً",
    "تحويل",
    "بطاقة ائتمان",
    "تقسيط",
    "نقاط الولاء"
]

# Service statuses - حالات الصيانة
SERVICE_STATUSES = [
    "مستلم",
    "قيد الفحص",
    "قيد الإصلاح",
    "في انتظار القطع",
    "مكتمل",
    "مُسلم",
    "ملغي"
]
