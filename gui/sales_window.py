#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sales Window for Mobile Shop Management System
نافذة المبيعات لنظام إدارة محل الموبايلات
"""

import customtkinter as ctk
from tkinter import messagebox, ttk
import sys
import os
from datetime import datetime

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.models import PAYMENT_METHODS

class SalesWindow(ctk.CTkFrame):
    """Sales and POS window"""
    
    def __init__(self, parent, db_manager):
        super().__init__(parent)
        self.db_manager = db_manager
        self.cart_items = []
        self.selected_customer = None
        self.total_amount = 0.0
        
        self.create_widgets()
        self.refresh_products()
    
    def create_widgets(self):
        """Create the sales interface"""
        # Title
        self.title_label = ctk.CTkLabel(
            self,
            text="نقطة البيع - POS",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        self.title_label.pack(pady=(0, 20))
        
        # Main container
        self.main_container = ctk.CTkFrame(self)
        self.main_container.pack(fill="both", expand=True)
        
        # Configure grid
        self.main_container.grid_columnconfigure(0, weight=2)
        self.main_container.grid_columnconfigure(1, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)
        
        # Products selection frame
        self.create_products_selection()
        
        # Cart and checkout frame
        self.create_cart_checkout()
    
    def create_products_selection(self):
        """Create products selection area"""
        # Left frame for products
        self.products_frame = ctk.CTkFrame(self.main_container)
        self.products_frame.grid(row=0, column=0, padx=(0, 10), pady=0, sticky="nsew")
        
        # Search frame
        self.search_frame = ctk.CTkFrame(self.products_frame)
        self.search_frame.pack(fill="x", padx=20, pady=20)
        
        # Search entry
        self.search_var = ctk.StringVar()
        self.search_var.trace("w", self.on_search_change)
        
        self.search_entry = ctk.CTkEntry(
            self.search_frame,
            placeholder_text="بحث المنتجات أو الباركود...",
            textvariable=self.search_var,
            font=ctk.CTkFont(size=16),
            height=40
        )
        self.search_entry.pack(fill="x", padx=10, pady=10)
        
        # Quick add by barcode
        self.barcode_frame = ctk.CTkFrame(self.search_frame)
        self.barcode_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        self.barcode_entry = ctk.CTkEntry(
            self.barcode_frame,
            placeholder_text="أدخل الباركود للإضافة السريعة...",
            font=ctk.CTkFont(size=14)
        )
        self.barcode_entry.pack(side="left", fill="x", expand=True, padx=(10, 5), pady=10)
        
        self.barcode_add_btn = ctk.CTkButton(
            self.barcode_frame,
            text="إضافة",
            command=self.add_by_barcode,
            width=80
        )
        self.barcode_add_btn.pack(side="right", padx=(5, 10), pady=10)
        
        # Products grid
        self.products_scroll = ctk.CTkScrollableFrame(self.products_frame)
        self.products_scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    
    def create_cart_checkout(self):
        """Create cart and checkout area"""
        # Right frame for cart
        self.cart_frame = ctk.CTkFrame(self.main_container)
        self.cart_frame.grid(row=0, column=1, padx=(10, 0), pady=0, sticky="nsew")
        
        # Cart title
        self.cart_title = ctk.CTkLabel(
            self.cart_frame,
            text="سلة المشتريات",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.cart_title.pack(pady=(20, 10))
        
        # Customer selection
        self.customer_frame = ctk.CTkFrame(self.cart_frame)
        self.customer_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        self.customer_label = ctk.CTkLabel(
            self.customer_frame,
            text="العميل:",
            font=ctk.CTkFont(size=14)
        )
        self.customer_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        self.customer_var = ctk.StringVar(value="عميل عادي")
        self.customer_combo = ctk.CTkComboBox(
            self.customer_frame,
            variable=self.customer_var,
            values=["عميل عادي"],
            command=self.on_customer_select
        )
        self.customer_combo.pack(fill="x", padx=10, pady=(0, 10))
        
        # Cart items
        self.cart_scroll = ctk.CTkScrollableFrame(self.cart_frame, height=300)
        self.cart_scroll.pack(fill="x", padx=20, pady=(0, 10))
        
        # Totals frame
        self.totals_frame = ctk.CTkFrame(self.cart_frame)
        self.totals_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        # Subtotal
        self.subtotal_label = ctk.CTkLabel(
            self.totals_frame,
            text="المجموع الفرعي: 0.00 ريال",
            font=ctk.CTkFont(size=14)
        )
        self.subtotal_label.pack(anchor="w", padx=10, pady=5)
        
        # Discount
        self.discount_frame = ctk.CTkFrame(self.totals_frame)
        self.discount_frame.pack(fill="x", padx=10, pady=5)
        
        self.discount_label = ctk.CTkLabel(
            self.discount_frame,
            text="خصم:",
            font=ctk.CTkFont(size=12)
        )
        self.discount_label.pack(side="left", padx=(10, 5), pady=10)
        
        self.discount_entry = ctk.CTkEntry(
            self.discount_frame,
            placeholder_text="0.00",
            width=80,
            font=ctk.CTkFont(size=12)
        )
        self.discount_entry.pack(side="left", padx=5, pady=10)
        self.discount_entry.bind("<KeyRelease>", self.calculate_total)
        
        # Tax
        self.tax_frame = ctk.CTkFrame(self.totals_frame)
        self.tax_frame.pack(fill="x", padx=10, pady=5)
        
        self.tax_label = ctk.CTkLabel(
            self.tax_frame,
            text="ضريبة:",
            font=ctk.CTkFont(size=12)
        )
        self.tax_label.pack(side="left", padx=(10, 5), pady=10)
        
        self.tax_entry = ctk.CTkEntry(
            self.tax_frame,
            placeholder_text="0.00",
            width=80,
            font=ctk.CTkFont(size=12)
        )
        self.tax_entry.pack(side="left", padx=5, pady=10)
        self.tax_entry.bind("<KeyRelease>", self.calculate_total)
        
        # Total
        self.total_label = ctk.CTkLabel(
            self.totals_frame,
            text="الإجمالي: 0.00 ريال",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.total_label.pack(anchor="w", padx=10, pady=5)
        
        # Payment method
        self.payment_frame = ctk.CTkFrame(self.cart_frame)
        self.payment_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        self.payment_label = ctk.CTkLabel(
            self.payment_frame,
            text="طريقة الدفع:",
            font=ctk.CTkFont(size=14)
        )
        self.payment_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        self.payment_combo = ctk.CTkComboBox(
            self.payment_frame,
            values=PAYMENT_METHODS
        )
        self.payment_combo.pack(fill="x", padx=10, pady=(0, 10))
        self.payment_combo.set("نقداً")
        
        # Buttons frame
        self.buttons_frame = ctk.CTkFrame(self.cart_frame)
        self.buttons_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Complete sale button
        self.complete_sale_btn = ctk.CTkButton(
            self.buttons_frame,
            text="إتمام البيع",
            command=self.complete_sale,
            font=ctk.CTkFont(size=16),
            height=50,
            fg_color="green",
            hover_color="darkgreen"
        )
        self.complete_sale_btn.pack(fill="x", padx=10, pady=10)
        
        # Clear cart button
        self.clear_cart_btn = ctk.CTkButton(
            self.buttons_frame,
            text="مسح السلة",
            command=self.clear_cart,
            font=ctk.CTkFont(size=14),
            height=40,
            fg_color="red",
            hover_color="darkred"
        )
        self.clear_cart_btn.pack(fill="x", padx=10, pady=(0, 10))
    
    def refresh_products(self):
        """Refresh products list"""
        try:
            self.products = self.db_manager.get_all_products()
            self.customers = self.db_manager.get_all_customers()
            self.display_products()
            self.update_customer_combo()
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ في تحديث البيانات: {e}")
    
    def display_products(self, products=None):
        """Display products in grid layout"""
        # Clear existing products
        for widget in self.products_scroll.winfo_children():
            widget.destroy()
        
        products_to_show = products if products is not None else self.products
        
        if not products_to_show:
            no_products_label = ctk.CTkLabel(
                self.products_scroll,
                text="لا توجد منتجات",
                font=ctk.CTkFont(size=16)
            )
            no_products_label.pack(pady=50)
            return
        
        # Create product cards in grid
        for i, product in enumerate(products_to_show):
            if product['quantity'] > 0:  # Only show products in stock
                self.create_product_card(product, i)
    
    def create_product_card(self, product, index):
        """Create a product card for selection"""
        # Calculate grid position (2 columns)
        row = index // 2
        col = index % 2
        
        card_frame = ctk.CTkFrame(self.products_scroll)
        card_frame.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
        
        # Configure grid weights
        self.products_scroll.grid_columnconfigure(0, weight=1)
        self.products_scroll.grid_columnconfigure(1, weight=1)
        
        # Product name
        name_label = ctk.CTkLabel(
            card_frame,
            text=f"{product['name']}",
            font=ctk.CTkFont(size=14, weight="bold"),
            wraplength=150
        )
        name_label.pack(padx=10, pady=(10, 5))
        
        # Brand and model
        brand_label = ctk.CTkLabel(
            card_frame,
            text=f"{product['brand']} {product['model']}",
            font=ctk.CTkFont(size=12)
        )
        brand_label.pack(padx=10, pady=2)
        
        # Price
        price_label = ctk.CTkLabel(
            card_frame,
            text=f"{product['selling_price']} ريال",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="green"
        )
        price_label.pack(padx=10, pady=2)
        
        # Stock
        stock_label = ctk.CTkLabel(
            card_frame,
            text=f"متوفر: {product['quantity']}",
            font=ctk.CTkFont(size=11)
        )
        stock_label.pack(padx=10, pady=2)
        
        # Add button
        add_btn = ctk.CTkButton(
            card_frame,
            text="إضافة",
            command=lambda p=product: self.add_to_cart(p),
            width=100,
            height=30
        )
        add_btn.pack(padx=10, pady=(5, 10))
    
    def add_to_cart(self, product, quantity=1):
        """Add product to cart"""
        if product['quantity'] < quantity:
            messagebox.showerror("خطأ", "الكمية المطلوبة غير متوفرة")
            return
        
        # Check if product already in cart
        for item in self.cart_items:
            if item['product_id'] == product['id']:
                # Update quantity
                new_quantity = item['quantity'] + quantity
                if new_quantity > product['quantity']:
                    messagebox.showerror("خطأ", "الكمية المطلوبة تتجاوز المتوفر")
                    return
                item['quantity'] = new_quantity
                item['total_price'] = item['quantity'] * item['unit_price']
                break
        else:
            # Add new item
            cart_item = {
                'product_id': product['id'],
                'product_name': product['name'],
                'unit_price': product['selling_price'],
                'quantity': quantity,
                'total_price': quantity * product['selling_price']
            }
            self.cart_items.append(cart_item)
        
        self.display_cart()
        self.calculate_total()
    
    def add_by_barcode(self):
        """Add product to cart by barcode"""
        barcode = self.barcode_entry.get().strip()
        if not barcode:
            return
        
        # Find product by barcode
        product = None
        for p in self.products:
            if p['barcode'] == barcode:
                product = p
                break
        
        if product:
            self.add_to_cart(product)
            self.barcode_entry.delete(0, "end")
        else:
            messagebox.showerror("خطأ", "لم يتم العثور على منتج بهذا الباركود")
    
    def display_cart(self):
        """Display cart items"""
        # Clear existing cart items
        for widget in self.cart_scroll.winfo_children():
            widget.destroy()
        
        if not self.cart_items:
            empty_label = ctk.CTkLabel(
                self.cart_scroll,
                text="السلة فارغة",
                font=ctk.CTkFont(size=14)
            )
            empty_label.pack(pady=20)
            return
        
        for i, item in enumerate(self.cart_items):
            self.create_cart_item(item, i)
    
    def create_cart_item(self, item, index):
        """Create a cart item widget"""
        item_frame = ctk.CTkFrame(self.cart_scroll)
        item_frame.pack(fill="x", padx=5, pady=2)
        
        # Product name
        name_label = ctk.CTkLabel(
            item_frame,
            text=item['product_name'],
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        )
        name_label.pack(fill="x", padx=10, pady=(10, 2))
        
        # Quantity controls
        qty_frame = ctk.CTkFrame(item_frame)
        qty_frame.pack(fill="x", padx=10, pady=2)
        
        # Decrease button
        decrease_btn = ctk.CTkButton(
            qty_frame,
            text="-",
            command=lambda idx=index: self.change_quantity(idx, -1),
            width=30,
            height=25
        )
        decrease_btn.pack(side="left", padx=2)
        
        # Quantity label
        qty_label = ctk.CTkLabel(
            qty_frame,
            text=str(item['quantity']),
            font=ctk.CTkFont(size=12)
        )
        qty_label.pack(side="left", padx=5)
        
        # Increase button
        increase_btn = ctk.CTkButton(
            qty_frame,
            text="+",
            command=lambda idx=index: self.change_quantity(idx, 1),
            width=30,
            height=25
        )
        increase_btn.pack(side="left", padx=2)
        
        # Remove button
        remove_btn = ctk.CTkButton(
            qty_frame,
            text="حذف",
            command=lambda idx=index: self.remove_item(idx),
            width=50,
            height=25,
            fg_color="red",
            hover_color="darkred"
        )
        remove_btn.pack(side="right", padx=5)
        
        # Price info
        price_label = ctk.CTkLabel(
            item_frame,
            text=f"{item['unit_price']:.2f} × {item['quantity']} = {item['total_price']:.2f} ريال",
            font=ctk.CTkFont(size=11),
            anchor="w"
        )
        price_label.pack(fill="x", padx=10, pady=(2, 10))
    
    def change_quantity(self, index, change):
        """Change quantity of cart item"""
        if 0 <= index < len(self.cart_items):
            item = self.cart_items[index]
            new_quantity = item['quantity'] + change
            
            if new_quantity <= 0:
                self.remove_item(index)
                return
            
            # Check stock availability
            product = next((p for p in self.products if p['id'] == item['product_id']), None)
            if product and new_quantity > product['quantity']:
                messagebox.showerror("خطأ", "الكمية المطلوبة تتجاوز المتوفر")
                return
            
            item['quantity'] = new_quantity
            item['total_price'] = item['quantity'] * item['unit_price']
            
            self.display_cart()
            self.calculate_total()
    
    def remove_item(self, index):
        """Remove item from cart"""
        if 0 <= index < len(self.cart_items):
            del self.cart_items[index]
            self.display_cart()
            self.calculate_total()
    
    def calculate_total(self, event=None):
        """Calculate total amount"""
        subtotal = sum(item['total_price'] for item in self.cart_items)
        
        # Get discount and tax
        try:
            discount = float(self.discount_entry.get() or 0)
            tax = float(self.tax_entry.get() or 0)
        except ValueError:
            discount = 0
            tax = 0
        
        total = subtotal - discount + tax
        self.total_amount = max(0, total)
        
        # Update labels
        self.subtotal_label.configure(text=f"المجموع الفرعي: {subtotal:.2f} ريال")
        self.total_label.configure(text=f"الإجمالي: {self.total_amount:.2f} ريال")
    
    def clear_cart(self):
        """Clear all items from cart"""
        if self.cart_items and messagebox.askyesno("تأكيد", "هل تريد مسح جميع العناصر من السلة؟"):
            self.cart_items.clear()
            self.display_cart()
            self.calculate_total()
    
    def complete_sale(self):
        """Complete the sale transaction"""
        if not self.cart_items:
            messagebox.showerror("خطأ", "السلة فارغة")
            return
        
        if self.total_amount <= 0:
            messagebox.showerror("خطأ", "مبلغ البيع يجب أن يكون أكبر من صفر")
            return
        
        try:
            # Get discount and tax
            discount = float(self.discount_entry.get() or 0)
            tax = float(self.tax_entry.get() or 0)
            
            # Prepare sale data
            sale_data = {
                'customer_id': self.selected_customer['id'] if self.selected_customer else None,
                'total_amount': self.total_amount,
                'discount': discount,
                'tax': tax,
                'payment_method': self.payment_combo.get(),
                'payment_status': 'paid',
                'notes': ''
            }
            
            # Create sale with items
            sale_id = self.db_manager.create_sale(sale_data, self.cart_items)
            
            messagebox.showinfo("نجح", f"تمت عملية البيع بنجاح\nرقم الفاتورة: {sale_id}")
            
            # Clear cart and refresh
            self.cart_items.clear()
            self.display_cart()
            self.calculate_total()
            self.refresh_products()
            
            # Reset form
            self.discount_entry.delete(0, "end")
            self.tax_entry.delete(0, "end")
            self.customer_combo.set("عميل عادي")
            self.selected_customer = None
            
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ في إتمام البيع: {e}")
    
    def update_customer_combo(self):
        """Update customer combo box"""
        customer_names = ["عميل عادي"]
        for customer in self.customers:
            customer_names.append(f"{customer['name']} - {customer['phone']}")
        
        self.customer_combo.configure(values=customer_names)
    
    def on_customer_select(self, value):
        """Handle customer selection"""
        if value == "عميل عادي":
            self.selected_customer = None
        else:
            # Find customer by the displayed format
            for customer in self.customers:
                if f"{customer['name']} - {customer['phone']}" == value:
                    self.selected_customer = customer
                    break
    
    def on_search_change(self, *args):
        """Handle search input change"""
        search_term = self.search_var.get().lower()
        
        if not search_term:
            self.display_products()
            return
        
        # Filter products based on search term
        filtered_products = []
        for product in self.products:
            if (search_term in product['name'].lower() or
                search_term in product['brand'].lower() or
                search_term in product['model'].lower() or
                search_term in (product['barcode'] or "").lower()):
                filtered_products.append(product)
        
        self.display_products(filtered_products)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sales Window for Mobile Shop Management System
نافذة المبيعات لنظام إدارة محل الموبايلات
"""

import customtkinter as ctk
from tkinter import messagebox
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.arabic_support import create_title_font, create_heading_font, create_button_font, create_body_font

class SalesWindow(ctk.CTkFrame):
    """Sales management window"""

    def __init__(self, parent, db_manager):
        super().__init__(parent)
        self.db_manager = db_manager
        self.create_widgets()
        self.load_sales()

    def create_widgets(self):
        """Create the sales interface"""
        # Title
        self.title_label = ctk.CTkLabel(
            self,
            text="إدارة المبيعات",
            font=create_title_font(28)
        )
        self.title_label.pack(pady=(0, 20))

        # Controls frame
        self.controls_frame = ctk.CTkFrame(self)
        self.controls_frame.pack(fill="x", padx=20, pady=(0, 20))

        # New sale button
        self.new_sale_button = ctk.CTkButton(
            self.controls_frame,
            text="بيعة جديدة",
            command=self.new_sale,
            font=create_button_font(14),
            width=150,
            height=40
        )
        self.new_sale_button.pack(side="left", padx=10, pady=10)

        # Sales stats frame
        self.stats_frame = ctk.CTkFrame(self.controls_frame)
        self.stats_frame.pack(side="right", padx=10, pady=10)

        # Today's sales
        self.today_sales_label = ctk.CTkLabel(
            self.stats_frame,
            text="مبيعات اليوم: 0.00 ريال",
            font=create_body_font(12)
        )
        self.today_sales_label.pack(padx=10, pady=5)

        # Sales list
        self.sales_frame = ctk.CTkScrollableFrame(self, label_text="سجل المبيعات")
        self.sales_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def load_sales(self):
        """Load sales from database"""
        try:
            # Get recent sales (last 30 days)
            from datetime import datetime, timedelta
            end_date = datetime.now().strftime('%Y-%m-%d')
            start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
            
            sales = self.db_manager.get_sales_report(start_date, end_date)
            
            # Clear existing widgets
            for widget in self.sales_frame.winfo_children():
                widget.destroy()

            if not sales:
                no_sales_label = ctk.CTkLabel(
                    self.sales_frame,
                    text="لا توجد مبيعات حتى الآن. انقر على 'بيعة جديدة' لإضافة أول عملية بيع.",
                    font=create_body_font(14)
                )
                no_sales_label.pack(pady=50)
                return

            # Create sales cards
            for sale in sales:
                self.create_sale_card(sale)

            # Update stats
            self.update_stats()

        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ في تحميل المبيعات: {e}")

    def create_sale_card(self, sale):
        """Create a sale card widget"""
        card_frame = ctk.CTkFrame(self.sales_frame)
        card_frame.pack(fill="x", padx=10, pady=5)

        # Sale info
        info_frame = ctk.CTkFrame(card_frame)
        info_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Sale number and date
        header_text = f"فاتورة رقم: {sale['id']} - {sale['sale_date'][:10]}"
        header_label = ctk.CTkLabel(
            info_frame,
            text=header_text,
            font=create_heading_font(14),
            anchor="w"
        )
        header_label.pack(fill="x", padx=10, pady=(10, 5))

        # Details
        customer_name = sale.get('customer_name', 'عميل عادي')
        details_text = f"العميل: {customer_name} | المبلغ: {sale['total_amount']:.2f} ريال | الدفع: {sale['payment_method']}"
        details_label = ctk.CTkLabel(
            info_frame,
            text=details_text,
            font=create_body_font(12),
            anchor="w"
        )
        details_label.pack(fill="x", padx=10, pady=(0, 10))

        # View button
        view_button = ctk.CTkButton(
            card_frame,
            text="عرض التفاصيل",
            command=lambda s=sale: self.view_sale_details(s),
            width=120,
            height=40
        )
        view_button.pack(side="right", padx=10, pady=10)

    def update_stats(self):
        """Update sales statistics"""
        try:
            stats = self.db_manager.get_dashboard_stats()
            today_total = stats.get('today_sales_total', 0)
            self.today_sales_label.configure(text=f"مبيعات اليوم: {today_total:.2f} ريال")
        except Exception as e:
            print(f"خطأ في تحديث الإحصائيات: {e}")

    def new_sale(self):
        """Create new sale"""
        messagebox.showinfo("قريباً", "ستتم إضافة نافذة البيع قريباً")

    def view_sale_details(self, sale):
        """View sale details"""
        messagebox.showinfo("تفاصيل البيعة", f"تفاصيل الفاتورة رقم: {sale['id']}\nالمبلغ: {sale['total_amount']:.2f} ريال")
