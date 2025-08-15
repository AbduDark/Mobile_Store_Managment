
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sales View
عرض المبيعات
"""

import customtkinter as ctk
from tkinter import messagebox, ttk
import threading
from datetime import datetime

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
        
        # Cart items
        self.cart_items = []
        self.total_amount = 0.0
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup sales view UI"""
        colors = self.theme_manager.get_colors()
        
        # Left section - Product selection and cart
        left_frame = ctk.CTkFrame(self, corner_radius=10)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        left_frame.grid_columnconfigure(0, weight=1)
        left_frame.grid_rowconfigure(2, weight=1)
        
        # Header
        header_label = ctk.CTkLabel(
            left_frame,
            text="🛒 نقطة البيع",
            font=self.theme_manager.get_header_font_config(20),
            text_color=colors["accent"]
        )
        header_label.grid(row=0, column=0, pady=20)
        
        # Search section
        search_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        search_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 20))
        search_frame.grid_columnconfigure(1, weight=1)
        
        # Barcode entry
        barcode_label = ctk.CTkLabel(search_frame, text="الباركود:", font=self.theme_manager.get_font_config(12))
        barcode_label.grid(row=0, column=0, sticky="w", pady=(0, 10))
        
        self.barcode_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="امسح أو ادخل الباركود...",
            font=self.theme_manager.get_font_config(12)
        )
        self.barcode_entry.grid(row=0, column=1, sticky="ew", padx=(10, 0), pady=(0, 10))
        self.barcode_entry.bind("<Return>", self._on_barcode_enter)
        
        # Product search
        search_label = ctk.CTkLabel(search_frame, text="البحث:", font=self.theme_manager.get_font_config(12))
        search_label.grid(row=1, column=0, sticky="w")
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="ابحث عن منتج...",
            font=self.theme_manager.get_font_config(12)
        )
        self.search_entry.grid(row=1, column=1, sticky="ew", padx=(10, 0))
        self.search_entry.bind("<KeyRelease>", self._on_search_product)
        
        # Products list
        products_label = ctk.CTkLabel(
            left_frame,
            text="المنتجات المتاحة",
            font=self.theme_manager.get_font_config(14, "bold")
        )
        products_label.grid(row=2, column=0, pady=(10, 5), sticky="w", padx=20)
        
        # Products frame
        self.products_frame = ctk.CTkScrollableFrame(left_frame, height=200)
        self.products_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 20))
        
        # Load sample products
        self._load_sample_products()
        
        # Cart section
        cart_label = ctk.CTkLabel(
            left_frame,
            text="سلة التسوق",
            font=self.theme_manager.get_font_config(16, "bold")
        )
        cart_label.grid(row=4, column=0, pady=(20, 10))
        
        # Cart items
        self.cart_frame = ctk.CTkScrollableFrame(left_frame, height=250)
        self.cart_frame.grid(row=5, column=0, sticky="ew", padx=20, pady=(0, 20))
        
        # Right section - Customer and payment
        right_frame = ctk.CTkFrame(self, corner_radius=10)
        right_frame.grid(row=0, column=1, sticky="nsew")
        right_frame.grid_columnconfigure(0, weight=1)
        
        # Customer section
        customer_label = ctk.CTkLabel(
            right_frame,
            text="👤 معلومات العميل",
            font=self.theme_manager.get_font_config(16, "bold")
        )
        customer_label.grid(row=0, column=0, pady=(20, 10))
        
        customer_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        customer_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 20))
        customer_frame.grid_columnconfigure(1, weight=1)
        
        # Customer selection
        ctk.CTkLabel(customer_frame, text="العميل:", font=self.theme_manager.get_font_config(12)).grid(row=0, column=0, sticky="w", pady=5)
        
        self.customer_combo = ctk.CTkComboBox(
            customer_frame,
            values=["عميل عادي", "أحمد محمد - 0501234567", "فاطمة علي - 0509876543"],
            width=200,
            font=self.theme_manager.get_font_config(11)
        )
        self.customer_combo.grid(row=0, column=1, sticky="ew", padx=(10, 0), pady=5)
        
        # Phone entry
        ctk.CTkLabel(customer_frame, text="الهاتف:", font=self.theme_manager.get_font_config(12)).grid(row=1, column=0, sticky="w", pady=5)
        
        self.phone_entry = ctk.CTkEntry(customer_frame, placeholder_text="رقم الهاتف", font=self.theme_manager.get_font_config(12))
        self.phone_entry.grid(row=1, column=1, sticky="ew", padx=(10, 0), pady=5)
        
        # Payment section
        payment_label = ctk.CTkLabel(
            right_frame,
            text="💳 الدفع",
            font=self.theme_manager.get_font_config(16, "bold")
        )
        payment_label.grid(row=2, column=0, pady=(20, 10))
        
        payment_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        payment_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 20))
        payment_frame.grid_columnconfigure(1, weight=1)
        
        # Payment method
        ctk.CTkLabel(payment_frame, text="طريقة الدفع:", font=self.theme_manager.get_font_config(12)).grid(row=0, column=0, sticky="w", pady=5)
        
        self.payment_combo = ctk.CTkComboBox(
            payment_frame,
            values=["نقد", "بطاقة ائتمان", "تحويل بنكي"],
            width=150,
            font=self.theme_manager.get_font_config(11)
        )
        self.payment_combo.grid(row=0, column=1, sticky="ew", padx=(10, 0), pady=5)
        
        # Discount
        ctk.CTkLabel(payment_frame, text="الخصم (%):", font=self.theme_manager.get_font_config(12)).grid(row=1, column=0, sticky="w", pady=5)
        
        self.discount_entry = ctk.CTkEntry(payment_frame, placeholder_text="0", font=self.theme_manager.get_font_config(12))
        self.discount_entry.grid(row=1, column=1, sticky="ew", padx=(10, 0), pady=5)
        self.discount_entry.bind("<KeyRelease>", self._update_total)
        
        # Total section
        self.total_frame = ctk.CTkFrame(right_frame)
        self.total_frame.grid(row=4, column=0, sticky="ew", padx=20, pady=(0, 20))
        self.total_frame.grid_columnconfigure(1, weight=1)
        
        # Subtotal
        ctk.CTkLabel(self.total_frame, text="المجموع الفرعي:", font=self.theme_manager.get_font_config(12)).grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.subtotal_label = ctk.CTkLabel(self.total_frame, text="0.00 ر.س", font=self.theme_manager.get_font_config(12, "bold"))
        self.subtotal_label.grid(row=0, column=1, sticky="e", padx=10, pady=5)
        
        # Discount amount
        ctk.CTkLabel(self.total_frame, text="قيمة الخصم:", font=self.theme_manager.get_font_config(12)).grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.discount_label = ctk.CTkLabel(self.total_frame, text="0.00 ر.س", font=self.theme_manager.get_font_config(12))
        self.discount_label.grid(row=1, column=1, sticky="e", padx=10, pady=5)
        
        # Tax
        ctk.CTkLabel(self.total_frame, text="الضريبة (15%):", font=self.theme_manager.get_font_config(12)).grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.tax_label = ctk.CTkLabel(self.total_frame, text="0.00 ر.س", font=self.theme_manager.get_font_config(12))
        self.tax_label.grid(row=2, column=1, sticky="e", padx=10, pady=5)
        
        # Total
        ctk.CTkLabel(self.total_frame, text="المجموع الكلي:", font=self.theme_manager.get_font_config(14, "bold")).grid(row=3, column=0, sticky="w", padx=10, pady=10)
        self.total_label = ctk.CTkLabel(self.total_frame, text="0.00 ر.س", font=self.theme_manager.get_font_config(16, "bold"), text_color=colors["accent"])
        self.total_label.grid(row=3, column=1, sticky="e", padx=10, pady=10)
        
        # Action buttons
        buttons_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        buttons_frame.grid(row=5, column=0, sticky="ew", padx=20, pady=(0, 20))
        
        # Complete sale button
        complete_btn = ctk.CTkButton(
            buttons_frame,
            text="إتمام البيع",
            font=self.theme_manager.get_font_config(14, "bold"),
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
            command=self._clear_cart,
            font=self.theme_manager.get_font_config(12)
        )
        clear_btn.pack(fill="x")
    
    def _load_sample_products(self):
        """Load sample products"""
        sample_products = [
            {"name": "iPhone 15 Pro", "price": 4500.0, "stock": 10, "barcode": "123456789"},
            {"name": "Galaxy S24", "price": 3200.0, "stock": 5, "barcode": "987654321"},
            {"name": "AirPods Pro", "price": 950.0, "stock": 15, "barcode": "555666777"},
            {"name": "Samsung Charger", "price": 85.0, "stock": 25, "barcode": "111222333"},
            {"name": "Phone Case", "price": 45.0, "stock": 30, "barcode": "444555666"}
        ]
        
        for product in sample_products:
            self._create_product_card(product)
    
    def _create_product_card(self, product):
        """Create a product card"""
        colors = self.theme_manager.get_colors()
        
        card = ctk.CTkFrame(self.products_frame, height=80)
        card.pack(fill="x", pady=5)
        card.grid_columnconfigure(1, weight=1)
        
        # Product info
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        
        name_label = ctk.CTkLabel(
            info_frame,
            text=product["name"],
            font=self.theme_manager.get_font_config(12, "bold")
        )
        name_label.pack(anchor="w")
        
        price_label = ctk.CTkLabel(
            info_frame,
            text=f"{product['price']:.2f} ر.س",
            font=self.theme_manager.get_font_config(11),
            text_color=colors["accent"]
        )
        price_label.pack(anchor="w")
        
        stock_label = ctk.CTkLabel(
            info_frame,
            text=f"المخزون: {product['stock']}",
            font=self.theme_manager.get_font_config(10)
        )
        stock_label.pack(anchor="w")
        
        # Add button
        add_btn = ctk.CTkButton(
            card,
            text="إضافة",
            width=60,
            height=30,
            command=lambda p=product: self._add_to_cart(p),
            font=self.theme_manager.get_font_config(11)
        )
        add_btn.grid(row=0, column=1, sticky="e", padx=10, pady=10)
    
    def _add_to_cart(self, product):
        """Add product to cart"""
        # Check if product already in cart
        for item in self.cart_items:
            if item['name'] == product['name']:
                item['quantity'] += 1
                item['total'] = item['quantity'] * item['price']
                self._update_cart_display()
                self._update_total()
                return
        
        # Add new item to cart
        cart_item = {
            'name': product['name'],
            'price': product['price'],
            'quantity': 1,
            'total': product['price']
        }
        self.cart_items.append(cart_item)
        self._update_cart_display()
        self._update_total()
    
    def _update_cart_display(self):
        """Update cart display"""
        # Clear current display
        for widget in self.cart_frame.winfo_children():
            widget.destroy()
        
        # Add cart items
        for i, item in enumerate(self.cart_items):
            self._create_cart_item_widget(item, i)
    
    def _create_cart_item_widget(self, item, index):
        """Create cart item widget"""
        colors = self.theme_manager.get_colors()
        
        item_frame = ctk.CTkFrame(self.cart_frame)
        item_frame.pack(fill="x", pady=2)
        item_frame.grid_columnconfigure(1, weight=1)
        
        # Product info
        info_label = ctk.CTkLabel(
            item_frame,
            text=item['name'],
            font=self.theme_manager.get_font_config(11, "bold")
        )
        info_label.grid(row=0, column=0, columnspan=3, sticky="w", padx=10, pady=(5, 0))
        
        # Quantity controls
        qty_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        qty_frame.grid(row=1, column=0, sticky="w", padx=10, pady=5)
        
        minus_btn = ctk.CTkButton(
            qty_frame,
            text="-",
            width=25,
            height=25,
            command=lambda i=index: self._decrease_quantity(i),
            font=self.theme_manager.get_font_config(12, "bold")
        )
        minus_btn.pack(side="left")
        
        qty_label = ctk.CTkLabel(
            qty_frame,
            text=str(item['quantity']),
            font=self.theme_manager.get_font_config(11),
            width=30
        )
        qty_label.pack(side="left", padx=5)
        
        plus_btn = ctk.CTkButton(
            qty_frame,
            text="+",
            width=25,
            height=25,
            command=lambda i=index: self._increase_quantity(i),
            font=self.theme_manager.get_font_config(12, "bold")
        )
        plus_btn.pack(side="left")
        
        # Price and total
        price_label = ctk.CTkLabel(
            item_frame,
            text=f"{item['price']:.2f} ر.س",
            font=self.theme_manager.get_font_config(10)
        )
        price_label.grid(row=1, column=1, padx=5, pady=5)
        
        total_label = ctk.CTkLabel(
            item_frame,
            text=f"{item['total']:.2f} ر.س",
            font=self.theme_manager.get_font_config(11, "bold"),
            text_color=colors["accent"]
        )
        total_label.grid(row=1, column=2, sticky="e", padx=10, pady=5)
        
        # Remove button
        remove_btn = ctk.CTkButton(
            item_frame,
            text="×",
            width=25,
            height=25,
            fg_color=colors["danger"],
            hover_color="#c0392b",
            command=lambda i=index: self._remove_from_cart(i),
            font=self.theme_manager.get_font_config(14, "bold")
        )
        remove_btn.grid(row=0, column=3, rowspan=2, sticky="ne", padx=10, pady=5)
    
    def _increase_quantity(self, index):
        """Increase item quantity"""
        if index < len(self.cart_items):
            self.cart_items[index]['quantity'] += 1
            self.cart_items[index]['total'] = self.cart_items[index]['quantity'] * self.cart_items[index]['price']
            self._update_cart_display()
            self._update_total()
    
    def _decrease_quantity(self, index):
        """Decrease item quantity"""
        if index < len(self.cart_items) and self.cart_items[index]['quantity'] > 1:
            self.cart_items[index]['quantity'] -= 1
            self.cart_items[index]['total'] = self.cart_items[index]['quantity'] * self.cart_items[index]['price']
            self._update_cart_display()
            self._update_total()
    
    def _remove_from_cart(self, index):
        """Remove item from cart"""
        if index < len(self.cart_items):
            self.cart_items.pop(index)
            self._update_cart_display()
            self._update_total()
    
    def _update_total(self, *args):
        """Update total calculations"""
        subtotal = sum(item['total'] for item in self.cart_items)
        
        # Calculate discount
        try:
            discount_percent = float(self.discount_entry.get() or 0)
        except ValueError:
            discount_percent = 0
        
        discount_amount = subtotal * (discount_percent / 100)
        after_discount = subtotal - discount_amount
        
        # Calculate tax
        tax_amount = after_discount * 0.15
        total = after_discount + tax_amount
        
        # Update labels
        self.subtotal_label.configure(text=f"{subtotal:.2f} ر.س")
        self.discount_label.configure(text=f"{discount_amount:.2f} ر.س")
        self.tax_label.configure(text=f"{tax_amount:.2f} ر.س")
        self.total_label.configure(text=f"{total:.2f} ر.س")
        
        self.total_amount = total
    
    def _on_barcode_enter(self, event):
        """Handle barcode entry"""
        barcode = self.barcode_entry.get().strip()
        if barcode:
            # Simple barcode lookup (in real app, search in database)
            sample_products = {
                "123456789": {"name": "iPhone 15 Pro", "price": 4500.0, "stock": 10},
                "987654321": {"name": "Galaxy S24", "price": 3200.0, "stock": 5},
                "555666777": {"name": "AirPods Pro", "price": 950.0, "stock": 15},
            }
            
            if barcode in sample_products:
                self._add_to_cart(sample_products[barcode])
                messagebox.showinfo("تم العثور", f"تم إضافة {sample_products[barcode]['name']} للسلة")
            else:
                messagebox.showwarning("غير موجود", f"لم يتم العثور على منتج بالباركود: {barcode}")
            
            self.barcode_entry.delete(0, "end")
    
    def _on_search_product(self, event):
        """Handle product search"""
        # This would filter the products list in a real implementation
        pass
    
    def _complete_sale(self):
        """Complete the sale"""
        if not self.cart_items:
            messagebox.showwarning("تحذير", "السلة فارغة! يرجى إضافة منتجات للبيع")
            return
        
        if messagebox.askyesno("تأكيد البيع", f"هل تريد إتمام عملية البيع بمبلغ {self.total_amount:.2f} ر.س؟"):
            # Here you would save the sale to database
            customer = self.customer_combo.get()
            payment_method = self.payment_combo.get()
            
            # Generate receipt
            receipt_text = f"""
فاتورة البيع
التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M')}
العميل: {customer}
طريقة الدفع: {payment_method}

المنتجات:
"""
            for item in self.cart_items:
                receipt_text += f"{item['name']} × {item['quantity']} = {item['total']:.2f} ر.س\n"
            
            receipt_text += f"\nالمجموع الإجمالي: {self.total_amount:.2f} ر.س"
            
            messagebox.showinfo("تم البيع بنجاح", "تم إتمام عملية البيع بنجاح!\nتم إنشاء الفاتورة.")
            
            # Clear cart
            self._clear_cart()
    
    def _clear_cart(self):
        """Clear the shopping cart"""
        if not self.cart_items:
            return
        
        if messagebox.askyesno("تأكيد المسح", "هل تريد مسح جميع المنتجات من السلة؟"):
            self.cart_items.clear()
            self._update_cart_display()
            self._update_total()
            messagebox.showinfo("تم المسح", "تم مسح السلة بنجاح!")
