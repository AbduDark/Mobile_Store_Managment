
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sales View
عرض المبيعات
"""

import customtkinter as ctk
from tkinter import messagebox
import threading

from src.utils.logger import get_logger

logger = get_logger(__name__)

class SalesView(ctk.CTkFrame):
    """Sales management and POS view"""
    
    def __init__(self, parent, db_manager, theme_manager):
        super().__init__(parent, fg_color="transparent")
        
        self.db_manager = db_manager
        self.theme_manager = theme_manager
        
        # Configure grid
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup sales view UI"""
        colors = self.theme_manager.get_colors()
        
        # Left section - Product selection and cart
        left_frame = ctk.CTkFrame(self, corner_radius=10)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        left_frame.grid_columnconfigure(0, weight=1)
        left_frame.grid_rowconfigure(1, weight=1)
        
        # Header
        header_label = ctk.CTkLabel(
            left_frame,
            text="🛒 نقطة البيع",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=colors["accent"]
        )
        header_label.grid(row=0, column=0, pady=20)
        
        # Search section
        search_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        search_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 20))
        search_frame.grid_columnconfigure(1, weight=1)
        
        # Barcode entry
        barcode_label = ctk.CTkLabel(search_frame, text="الباركود:")
        barcode_label.grid(row=0, column=0, sticky="w", pady=(0, 10))
        
        self.barcode_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="امسح أو ادخل الباركود...",
            font=ctk.CTkFont(size=12)
        )
        self.barcode_entry.grid(row=0, column=1, sticky="ew", padx=(10, 0), pady=(0, 10))
        self.barcode_entry.bind("<Return>", self._on_barcode_enter)
        
        # Product search
        search_label = ctk.CTkLabel(search_frame, text="البحث:")
        search_label.grid(row=1, column=0, sticky="w")
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="ابحث عن منتج...",
            font=ctk.CTkFont(size=12)
        )
        self.search_entry.grid(row=1, column=1, sticky="ew", padx=(10, 0))
        
        # Cart section
        cart_label = ctk.CTkLabel(
            left_frame,
            text="سلة التسوق",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        cart_label.grid(row=2, column=0, pady=(20, 10))
        
        # Cart items (placeholder)
        cart_frame = ctk.CTkScrollableFrame(left_frame, height=300)
        cart_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 20))
        
        # Sample cart items
        for i in range(3):
            item_frame = ctk.CTkFrame(cart_frame)
            item_frame.pack(fill="x", pady=5)
            item_frame.grid_columnconfigure(1, weight=1)
            
            # Product info
            ctk.CTkLabel(item_frame, text=f"منتج تجريبي {i+1}").grid(row=0, column=0, padx=10, pady=5)
            ctk.CTkLabel(item_frame, text="الكمية: 1").grid(row=0, column=1, padx=10, pady=5)
            ctk.CTkLabel(item_frame, text="100 ر.س").grid(row=0, column=2, padx=10, pady=5)
        
        # Right section - Customer and payment
        right_frame = ctk.CTkFrame(self, corner_radius=10)
        right_frame.grid(row=0, column=1, sticky="nsew")
        right_frame.grid_columnconfigure(0, weight=1)
        
        # Customer section
        customer_label = ctk.CTkLabel(
            right_frame,
            text="👤 معلومات العميل",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        customer_label.grid(row=0, column=0, pady=(20, 10))
        
        customer_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        customer_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 20))
        customer_frame.grid_columnconfigure(1, weight=1)
        
        # Customer selection
        ctk.CTkLabel(customer_frame, text="العميل:").grid(row=0, column=0, sticky="w", pady=5)
        
        self.customer_combo = ctk.CTkComboBox(
            customer_frame,
            values=["عميل عادي", "أحمد محمد - 0501234567"],
            width=200
        )
        self.customer_combo.grid(row=0, column=1, sticky="ew", padx=(10, 0), pady=5)
        
        # Phone entry
        ctk.CTkLabel(customer_frame, text="الهاتف:").grid(row=1, column=0, sticky="w", pady=5)
        
        self.phone_entry = ctk.CTkEntry(customer_frame, placeholder_text="رقم الهاتف")
        self.phone_entry.grid(row=1, column=1, sticky="ew", padx=(10, 0), pady=5)
        
        # Payment section
        payment_label = ctk.CTkLabel(
            right_frame,
            text="💳 الدفع",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        payment_label.grid(row=2, column=0, pady=(20, 10))
        
        payment_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        payment_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 20))
        payment_frame.grid_columnconfigure(1, weight=1)
        
        # Payment method
        ctk.CTkLabel(payment_frame, text="طريقة الدفع:").grid(row=0, column=0, sticky="w", pady=5)
        
        self.payment_combo = ctk.CTkComboBox(
            payment_frame,
            values=["نقد", "بطاقة ائتمان", "تحويل"],
            width=150
        )
        self.payment_combo.grid(row=0, column=1, sticky="ew", padx=(10, 0), pady=5)
        
        # Total section
        total_frame = ctk.CTkFrame(right_frame)
        total_frame.grid(row=4, column=0, sticky="ew", padx=20, pady=(0, 20))
        total_frame.grid_columnconfigure(1, weight=1)
        
        # Subtotal
        ctk.CTkLabel(total_frame, text="المجموع الفرعي:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        ctk.CTkLabel(total_frame, text="300.00 ر.س", font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, sticky="e", padx=10, pady=5)
        
        # Tax
        ctk.CTkLabel(total_frame, text="الضريبة (15%):").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        ctk.CTkLabel(total_frame, text="45.00 ر.س").grid(row=1, column=1, sticky="e", padx=10, pady=5)
        
        # Total
        ctk.CTkLabel(total_frame, text="المجموع الكلي:", font=ctk.CTkFont(size=14, weight="bold")).grid(row=2, column=0, sticky="w", padx=10, pady=10)
        ctk.CTkLabel(total_frame, text="345.00 ر.س", font=ctk.CTkFont(size=16, weight="bold"), text_color=colors["accent"]).grid(row=2, column=1, sticky="e", padx=10, pady=10)
        
        # Action buttons
        buttons_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        buttons_frame.grid(row=5, column=0, sticky="ew", padx=20, pady=(0, 20))
        
        # Complete sale button
        complete_btn = ctk.CTkButton(
            buttons_frame,
            text="إتمام البيع",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            fg_color=colors["success"],
            hover_color="#229954",
            command=self._complete_sale
        )
        complete_btn.pack(fill="x", pady=(0, 10))
        
        # Clear cart button
        clear_btn = ctk.CTkButton(
            buttons_frame,
            text="مسح السلة",
            fg_color=colors["warning"],
            hover_color="#d68910",
            command=self._clear_cart
        )
        clear_btn.pack(fill="x")
    
    def _on_barcode_enter(self, event):
        """Handle barcode entry"""
        barcode = self.barcode_entry.get().strip()
        if barcode:
            # Implementation for barcode lookup
            messagebox.showinfo("قريباً", f"البحث عن المنتج بالباركود: {barcode}")
            self.barcode_entry.delete(0, "end")
    
    def _complete_sale(self):
        """Complete the sale"""
        if messagebox.askyesno("تأكيد البيع", "هل تريد إتمام عملية البيع؟"):
            messagebox.showinfo("قريباً", "إتمام البيع قيد التطوير")
    
    def _clear_cart(self):
        """Clear the shopping cart"""
        if messagebox.askyesno("تأكيد المسح", "هل تريد مسح جميع المنتجات من السلة؟"):
            messagebox.showinfo("قريباً", "مسح السلة قيد التطوير")
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sales View
عرض المبيعات
"""

import customtkinter as ctk

class SalesView(ctk.CTkFrame):
    """Sales management view"""
    
    def __init__(self, parent, db_manager, theme_manager):
        super().__init__(parent)
        
        self.db_manager = db_manager
        self.theme_manager = theme_manager
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create sales view widgets"""
        title_label = ctk.CTkLabel(
            self,
            text="إدارة المبيعات",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(0, 20))
        
        info_label = ctk.CTkLabel(
            self,
            text="صفحة إدارة المبيعات قيد التطوير...",
            font=ctk.CTkFont(size=16)
        )
        info_label.pack(expand=True)
