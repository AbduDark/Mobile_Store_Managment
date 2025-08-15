#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Products Management Window for Mobile Shop Management System
نافذة إدارة المنتجات لنظام إدارة محل الموبايلات
"""

import customtkinter as ctk
from tkinter import messagebox, filedialog
import sys
import os
from PIL import Image, ImageTk

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.models import PRODUCT_CATEGORIES, PHONE_BRANDS, PHONE_CONDITIONS

class ProductsWindow(ctk.CTkFrame):
    """Products management window"""
    
    def __init__(self, parent, db_manager):
        super().__init__(parent)
        self.db_manager = db_manager
        self.products = []
        self.selected_product = None
        self.selected_image_path = ""
        
        self.create_widgets()
        self.refresh_products()
    
    def create_widgets(self):
        """Create the products management interface"""
        # Title
        self.title_label = ctk.CTkLabel(
            self,
            text="إدارة المنتجات",
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
        
        # Products list frame
        self.create_products_list()
        
        # Product form frame
        self.create_product_form()
    
    def create_products_list(self):
        """Create products list with search and controls"""
        # Left frame for products list
        self.list_frame = ctk.CTkFrame(self.main_container)
        self.list_frame.grid(row=0, column=0, padx=(0, 10), pady=0, sticky="nsew")
        
        # Search and controls frame
        self.controls_frame = ctk.CTkFrame(self.list_frame)
        self.controls_frame.pack(fill="x", padx=20, pady=20)
        
        # Search entry
        self.search_var = ctk.StringVar()
        self.search_var.trace("w", self.on_search_change)
        
        self.search_entry = ctk.CTkEntry(
            self.controls_frame,
            placeholder_text="بحث المنتجات...",
            textvariable=self.search_var,
            font=ctk.CTkFont(size=14),
            height=35
        )
        self.search_entry.pack(fill="x", pady=(0, 10))
        
        # Buttons frame
        self.buttons_frame = ctk.CTkFrame(self.controls_frame)
        self.buttons_frame.pack(fill="x", pady=(10, 0))
        
        # Add button
        self.add_btn = ctk.CTkButton(
            self.buttons_frame,
            text="إضافة منتج جديد",
            command=self.add_new_product,
            font=ctk.CTkFont(size=14),
            height=35
        )
        self.add_btn.pack(side="left", padx=(0, 10))
        
        # Edit button
        self.edit_btn = ctk.CTkButton(
            self.buttons_frame,
            text="تعديل",
            command=self.edit_selected_product,
            font=ctk.CTkFont(size=14),
            height=35,
            state="disabled"
        )
        self.edit_btn.pack(side="left", padx=5)
        
        # Delete button
        self.delete_btn = ctk.CTkButton(
            self.buttons_frame,
            text="حذف",
            command=self.delete_selected_product,
            font=ctk.CTkFont(size=14),
            height=35,
            fg_color="red",
            hover_color="darkred",
            state="disabled"
        )
        self.delete_btn.pack(side="left", padx=(10, 0))
        
        # Refresh button
        self.refresh_btn = ctk.CTkButton(
            self.buttons_frame,
            text="تحديث",
            command=self.refresh_products,
            font=ctk.CTkFont(size=14),
            height=35
        )
        self.refresh_btn.pack(side="right")
        
        # Products scrollable frame
        self.products_scroll = ctk.CTkScrollableFrame(self.list_frame)
        self.products_scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    
    def create_product_form(self):
        """Create product form for adding/editing"""
        # Right frame for product form
        self.form_frame = ctk.CTkFrame(self.main_container)
        self.form_frame.grid(row=0, column=1, padx=(10, 0), pady=0, sticky="nsew")
        
        # Form title
        self.form_title = ctk.CTkLabel(
            self.form_frame,
            text="إضافة منتج جديد",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.form_title.pack(pady=(20, 10))
        
        # Form scrollable frame
        self.form_scroll = ctk.CTkScrollableFrame(self.form_frame)
        self.form_scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Product name
        self.name_label = ctk.CTkLabel(self.form_scroll, text="اسم المنتج *", anchor="w")
        self.name_label.pack(fill="x", pady=(10, 5))
        
        self.name_entry = ctk.CTkEntry(
            self.form_scroll,
            placeholder_text="أدخل اسم المنتج",
            font=ctk.CTkFont(size=14)
        )
        self.name_entry.pack(fill="x", pady=(0, 10))
        
        # Brand
        self.brand_label = ctk.CTkLabel(self.form_scroll, text="العلامة التجارية *", anchor="w")
        self.brand_label.pack(fill="x", pady=(10, 5))
        
        self.brand_combo = ctk.CTkComboBox(
            self.form_scroll,
            values=PHONE_BRANDS,
            font=ctk.CTkFont(size=14)
        )
        self.brand_combo.pack(fill="x", pady=(0, 10))
        
        # Model
        self.model_label = ctk.CTkLabel(self.form_scroll, text="الموديل", anchor="w")
        self.model_label.pack(fill="x", pady=(10, 5))
        
        self.model_entry = ctk.CTkEntry(
            self.form_scroll,
            placeholder_text="أدخل موديل الجهاز",
            font=ctk.CTkFont(size=14)
        )
        self.model_entry.pack(fill="x", pady=(0, 10))
        
        # Category
        self.category_label = ctk.CTkLabel(self.form_scroll, text="الفئة *", anchor="w")
        self.category_label.pack(fill="x", pady=(10, 5))
        
        self.category_combo = ctk.CTkComboBox(
            self.form_scroll,
            values=PRODUCT_CATEGORIES,
            font=ctk.CTkFont(size=14)
        )
        self.category_combo.pack(fill="x", pady=(0, 10))
        
        # Prices frame
        self.prices_frame = ctk.CTkFrame(self.form_scroll)
        self.prices_frame.pack(fill="x", pady=(10, 0))
        
        # Purchase price
        self.purchase_price_label = ctk.CTkLabel(self.prices_frame, text="سعر الشراء *")
        self.purchase_price_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        self.purchase_price_entry = ctk.CTkEntry(
            self.prices_frame,
            placeholder_text="0.00",
            font=ctk.CTkFont(size=14)
        )
        self.purchase_price_entry.pack(fill="x", padx=10, pady=(0, 10))
        
        # Selling price
        self.selling_price_label = ctk.CTkLabel(self.prices_frame, text="سعر البيع *")
        self.selling_price_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        self.selling_price_entry = ctk.CTkEntry(
            self.prices_frame,
            placeholder_text="0.00",
            font=ctk.CTkFont(size=14)
        )
        self.selling_price_entry.pack(fill="x", padx=10, pady=(0, 10))
        
        # Quantity frame
        self.quantity_frame = ctk.CTkFrame(self.form_scroll)
        self.quantity_frame.pack(fill="x", pady=(10, 0))
        
        # Quantity
        self.quantity_label = ctk.CTkLabel(self.quantity_frame, text="الكمية *")
        self.quantity_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        self.quantity_entry = ctk.CTkEntry(
            self.quantity_frame,
            placeholder_text="0",
            font=ctk.CTkFont(size=14)
        )
        self.quantity_entry.pack(fill="x", padx=10, pady=(0, 10))
        
        # Min quantity
        self.min_quantity_label = ctk.CTkLabel(self.quantity_frame, text="أقل كمية للتنبيه")
        self.min_quantity_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        self.min_quantity_entry = ctk.CTkEntry(
            self.quantity_frame,
            placeholder_text="5",
            font=ctk.CTkFont(size=14)
        )
        self.min_quantity_entry.pack(fill="x", padx=10, pady=(0, 10))
        
        # Additional details frame
        self.details_frame = ctk.CTkFrame(self.form_scroll)
        self.details_frame.pack(fill="x", pady=(10, 0))
        
        # Color
        self.color_label = ctk.CTkLabel(self.details_frame, text="اللون")
        self.color_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        self.color_entry = ctk.CTkEntry(
            self.details_frame,
            placeholder_text="أدخل اللون",
            font=ctk.CTkFont(size=14)
        )
        self.color_entry.pack(fill="x", padx=10, pady=(0, 10))
        
        # Storage
        self.storage_label = ctk.CTkLabel(self.details_frame, text="الذاكرة")
        self.storage_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        self.storage_entry = ctk.CTkEntry(
            self.details_frame,
            placeholder_text="مثال: 128GB",
            font=ctk.CTkFont(size=14)
        )
        self.storage_entry.pack(fill="x", padx=10, pady=(0, 10))
        
        # Condition
        self.condition_label = ctk.CTkLabel(self.details_frame, text="الحالة")
        self.condition_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        self.condition_combo = ctk.CTkComboBox(
            self.details_frame,
            values=PHONE_CONDITIONS,
            font=ctk.CTkFont(size=14)
        )
        self.condition_combo.pack(fill="x", padx=10, pady=(0, 10))
        
        # Barcode
        self.barcode_label = ctk.CTkLabel(self.form_scroll, text="الباركود", anchor="w")
        self.barcode_label.pack(fill="x", pady=(10, 5))
        
        self.barcode_entry = ctk.CTkEntry(
            self.form_scroll,
            placeholder_text="أدخل الباركود (اختياري)",
            font=ctk.CTkFont(size=14)
        )
        self.barcode_entry.pack(fill="x", pady=(0, 10))
        
        # Description
        self.description_label = ctk.CTkLabel(self.form_scroll, text="الوصف", anchor="w")
        self.description_label.pack(fill="x", pady=(10, 5))
        
        self.description_text = ctk.CTkTextbox(
            self.form_scroll,
            height=80,
            font=ctk.CTkFont(size=14)
        )
        self.description_text.pack(fill="x", pady=(0, 10))
        
        # Image selection
        self.image_frame = ctk.CTkFrame(self.form_scroll)
        self.image_frame.pack(fill="x", pady=(10, 0))
        
        self.image_label = ctk.CTkLabel(self.image_frame, text="صورة المنتج")
        self.image_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        self.image_btn = ctk.CTkButton(
            self.image_frame,
            text="اختيار صورة",
            command=self.select_image,
            font=ctk.CTkFont(size=14)
        )
        self.image_btn.pack(padx=10, pady=(0, 10))
        
        # Form buttons
        self.form_buttons_frame = ctk.CTkFrame(self.form_scroll)
        self.form_buttons_frame.pack(fill="x", pady=20)
        
        self.save_btn = ctk.CTkButton(
            self.form_buttons_frame,
            text="حفظ",
            command=self.save_product,
            font=ctk.CTkFont(size=16),
            height=40
        )
        self.save_btn.pack(side="left", padx=10, pady=10)
        
        self.cancel_btn = ctk.CTkButton(
            self.form_buttons_frame,
            text="إلغاء",
            command=self.clear_form,
            font=ctk.CTkFont(size=16),
            height=40,
            fg_color="gray",
            hover_color="darkgray"
        )
        self.cancel_btn.pack(side="right", padx=10, pady=10)
    
    def refresh_products(self):
        """Refresh products list"""
        try:
            self.products = self.db_manager.get_all_products()
            self.display_products()
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ في تحديث المنتجات: {e}")
    
    def display_products(self, products=None):
        """Display products in the list"""
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
        
        for product in products_to_show:
            self.create_product_card(product)
    
    def create_product_card(self, product):
        """Create a product card widget"""
        card_frame = ctk.CTkFrame(self.products_scroll)
        card_frame.pack(fill="x", pady=5)
        
        # Product info
        info_frame = ctk.CTkFrame(card_frame)
        info_frame.pack(fill="x", padx=10, pady=10)
        
        # Name and brand
        name_label = ctk.CTkLabel(
            info_frame,
            text=f"{product['name']} - {product['brand']}",
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w"
        )
        name_label.pack(fill="x", padx=10, pady=(10, 5))
        
        # Details
        details_text = f"الفئة: {product['category']} | الكمية: {product['quantity']} | السعر: {product['selling_price']} ريال"
        details_label = ctk.CTkLabel(
            info_frame,
            text=details_text,
            font=ctk.CTkFont(size=12),
            anchor="w"
        )
        details_label.pack(fill="x", padx=10, pady=(0, 5))
        
        # Stock status
        if product['quantity'] <= product['min_quantity']:
            status_text = "⚠️ مخزون منخفض"
            status_color = "red"
        else:
            status_text = "✅ متوفر"
            status_color = "green"
        
        status_label = ctk.CTkLabel(
            info_frame,
            text=status_text,
            font=ctk.CTkFont(size=12),
            text_color=status_color,
            anchor="w"
        )
        status_label.pack(fill="x", padx=10, pady=(0, 10))
        
        # Click handler
        def on_card_click(event, prod=product):
            self.select_product(prod)
        
        # Bind click events to all card components
        for widget in [card_frame, info_frame, name_label, details_label, status_label]:
            widget.bind("<Button-1>", on_card_click)
            widget.configure(cursor="hand2")
    
    def select_product(self, product):
        """Select a product and load it in the form"""
        self.selected_product = product
        self.load_product_in_form(product)
        
        # Enable edit and delete buttons
        self.edit_btn.configure(state="normal")
        self.delete_btn.configure(state="normal")
        
        # Update form title
        self.form_title.configure(text=f"تعديل: {product['name']}")
    
    def load_product_in_form(self, product):
        """Load product data into the form"""
        self.name_entry.delete(0, "end")
        self.name_entry.insert(0, product['name'])
        
        self.brand_combo.set(product['brand'])
        
        self.model_entry.delete(0, "end")
        self.model_entry.insert(0, product['model'] or "")
        
        self.category_combo.set(product['category'])
        
        self.purchase_price_entry.delete(0, "end")
        self.purchase_price_entry.insert(0, str(product['purchase_price']))
        
        self.selling_price_entry.delete(0, "end")
        self.selling_price_entry.insert(0, str(product['selling_price']))
        
        self.quantity_entry.delete(0, "end")
        self.quantity_entry.insert(0, str(product['quantity']))
        
        self.min_quantity_entry.delete(0, "end")
        self.min_quantity_entry.insert(0, str(product['min_quantity']))
        
        self.color_entry.delete(0, "end")
        self.color_entry.insert(0, product['color'] or "")
        
        self.storage_entry.delete(0, "end")
        self.storage_entry.insert(0, product['storage'] or "")
        
        self.condition_combo.set(product['condition'] or "جديد")
        
        self.barcode_entry.delete(0, "end")
        self.barcode_entry.insert(0, product['barcode'] or "")
        
        self.description_text.delete("1.0", "end")
        self.description_text.insert("1.0", product['description'] or "")
        
        self.selected_image_path = product['image_path'] or ""
    
    def add_new_product(self):
        """Prepare form for adding new product"""
        self.selected_product = None
        self.clear_form()
        self.form_title.configure(text="إضافة منتج جديد")
        
        # Disable edit and delete buttons
        self.edit_btn.configure(state="disabled")
        self.delete_btn.configure(state="disabled")
    
    def edit_selected_product(self):
        """Edit the selected product"""
        if not self.selected_product:
            messagebox.showwarning("تحذير", "يرجى اختيار منتج للتعديل")
            return
        
        # Form is already loaded with product data
        pass
    
    def delete_selected_product(self):
        """Delete the selected product"""
        if not self.selected_product:
            messagebox.showwarning("تحذير", "يرجى اختيار منتج للحذف")
            return
        
        if messagebox.askyesno("تأكيد الحذف", f"هل تريد حذف المنتج '{self.selected_product['name']}'؟"):
            try:
                self.db_manager.delete_product(self.selected_product['id'])
                messagebox.showinfo("نجح", "تم حذف المنتج بنجاح")
                self.refresh_products()
                self.clear_form()
            except Exception as e:
                messagebox.showerror("خطأ", f"حدث خطأ في حذف المنتج: {e}")
    
    def save_product(self):
        """Save the product (add or update)"""
        try:
            # Validate required fields
            if not self.name_entry.get().strip():
                messagebox.showerror("خطأ", "اسم المنتج مطلوب")
                return
            
            if not self.brand_combo.get():
                messagebox.showerror("خطأ", "العلامة التجارية مطلوبة")
                return
            
            if not self.category_combo.get():
                messagebox.showerror("خطأ", "الفئة مطلوبة")
                return
            
            # Validate numeric fields
            try:
                purchase_price = float(self.purchase_price_entry.get() or 0)
                selling_price = float(self.selling_price_entry.get() or 0)
                quantity = int(self.quantity_entry.get() or 0)
                min_quantity = int(self.min_quantity_entry.get() or 5)
            except ValueError:
                messagebox.showerror("خطأ", "يرجى إدخال قيم صحيحة للأسعار والكميات")
                return
            
            # Prepare product data
            product_data = {
                'name': self.name_entry.get().strip(),
                'brand': self.brand_combo.get(),
                'model': self.model_entry.get().strip(),
                'category': self.category_combo.get(),
                'purchase_price': purchase_price,
                'selling_price': selling_price,
                'quantity': quantity,
                'min_quantity': min_quantity,
                'color': self.color_entry.get().strip(),
                'storage': self.storage_entry.get().strip(),
                'condition': self.condition_combo.get() or "جديد",
                'barcode': self.barcode_entry.get().strip(),
                'description': self.description_text.get("1.0", "end").strip(),
                'image_path': self.selected_image_path
            }
            
            if self.selected_product:
                # Update existing product
                self.db_manager.update_product(self.selected_product['id'], product_data)
                messagebox.showinfo("نجح", "تم تحديث المنتج بنجاح")
            else:
                # Add new product
                self.db_manager.add_product(product_data)
                messagebox.showinfo("نجح", "تم إضافة المنتج بنجاح")
            
            self.refresh_products()
            self.clear_form()
            
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ في حفظ المنتج: {e}")
    
    def clear_form(self):
        """Clear the product form"""
        self.name_entry.delete(0, "end")
        self.brand_combo.set("")
        self.model_entry.delete(0, "end")
        self.category_combo.set("")
        self.purchase_price_entry.delete(0, "end")
        self.selling_price_entry.delete(0, "end")
        self.quantity_entry.delete(0, "end")
        self.min_quantity_entry.delete(0, "end")
        self.color_entry.delete(0, "end")
        self.storage_entry.delete(0, "end")
        self.condition_combo.set("جديد")
        self.barcode_entry.delete(0, "end")
        self.description_text.delete("1.0", "end")
        self.selected_image_path = ""
        self.selected_product = None
        
        # Update form title
        self.form_title.configure(text="إضافة منتج جديد")
        
        # Disable edit and delete buttons
        self.edit_btn.configure(state="disabled")
        self.delete_btn.configure(state="disabled")
    
    def select_image(self):
        """Select an image for the product"""
        file_path = filedialog.askopenfilename(
            title="اختر صورة المنتج",
            filetypes=[
                ("صور", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("جميع الملفات", "*.*")
            ]
        )
        
        if file_path:
            self.selected_image_path = file_path
            self.image_btn.configure(text=f"تم اختيار: {os.path.basename(file_path)}")
    
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
                search_term in product['category'].lower() or
                search_term in (product['barcode'] or "").lower()):
                filtered_products.append(product)
        
        self.display_products(filtered_products)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Products Window for Mobile Shop Management System
نافذة المنتجات لنظام إدارة محل الموبايلات
"""

import customtkinter as ctk
from tkinter import messagebox, filedialog
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.arabic_support import create_title_font, create_heading_font, create_button_font, create_body_font

class ProductsWindow(ctk.CTkFrame):
    """Products management window"""

    def __init__(self, parent, db_manager):
        super().__init__(parent)
        self.db_manager = db_manager
        self.create_widgets()
        self.load_products()

    def create_widgets(self):
        """Create the products interface"""
        # Title
        self.title_label = ctk.CTkLabel(
            self,
            text="إدارة المنتجات",
            font=create_title_font(28)
        )
        self.title_label.pack(pady=(0, 20))

        # Controls frame
        self.controls_frame = ctk.CTkFrame(self)
        self.controls_frame.pack(fill="x", padx=20, pady=(0, 20))

        # Add product button
        self.add_button = ctk.CTkButton(
            self.controls_frame,
            text="إضافة منتج جديد",
            command=self.add_product,
            font=create_button_font(14),
            width=150,
            height=40
        )
        self.add_button.pack(side="left", padx=10, pady=10)

        # Search frame
        self.search_frame = ctk.CTkFrame(self.controls_frame)
        self.search_frame.pack(side="right", padx=10, pady=10)

        self.search_entry = ctk.CTkEntry(
            self.search_frame,
            placeholder_text="البحث في المنتجات...",
            width=200
        )
        self.search_entry.pack(side="left", padx=5, pady=5)

        self.search_button = ctk.CTkButton(
            self.search_frame,
            text="بحث",
            command=self.search_products,
            width=80
        )
        self.search_button.pack(side="left", padx=5, pady=5)

        # Products list
        self.products_frame = ctk.CTkScrollableFrame(self, label_text="قائمة المنتجات")
        self.products_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def load_products(self):
        """Load products from database"""
        try:
            products = self.db_manager.get_all_products()
            
            # Clear existing widgets
            for widget in self.products_frame.winfo_children():
                widget.destroy()

            if not products:
                no_products_label = ctk.CTkLabel(
                    self.products_frame,
                    text="لا توجد منتجات. انقر على 'إضافة منتج جديد' لإضافة منتج.",
                    font=create_body_font(14)
                )
                no_products_label.pack(pady=50)
                return

            # Create product cards
            for product in products:
                self.create_product_card(product)

        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ في تحميل المنتجات: {e}")

    def create_product_card(self, product):
        """Create a product card widget"""
        card_frame = ctk.CTkFrame(self.products_frame)
        card_frame.pack(fill="x", padx=10, pady=5)

        # Product info
        info_frame = ctk.CTkFrame(card_frame)
        info_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Name and brand
        name_label = ctk.CTkLabel(
            info_frame,
            text=f"{product['name']} - {product['brand']}",
            font=create_heading_font(16),
            anchor="w"
        )
        name_label.pack(fill="x", padx=10, pady=(10, 5))

        # Details
        details_text = f"الفئة: {product['category']} | الكمية: {product['quantity']} | السعر: {product['selling_price']:.2f} ريال"
        details_label = ctk.CTkLabel(
            info_frame,
            text=details_text,
            font=create_body_font(12),
            anchor="w"
        )
        details_label.pack(fill="x", padx=10, pady=(0, 10))

        # Buttons frame
        buttons_frame = ctk.CTkFrame(card_frame)
        buttons_frame.pack(side="right", padx=10, pady=10)

        edit_button = ctk.CTkButton(
            buttons_frame,
            text="تعديل",
            command=lambda p=product: self.edit_product(p),
            width=80,
            height=30
        )
        edit_button.pack(padx=5, pady=2)

        delete_button = ctk.CTkButton(
            buttons_frame,
            text="حذف",
            command=lambda p=product: self.delete_product(p),
            width=80,
            height=30,
            fg_color="red",
            hover_color="darkred"
        )
        delete_button.pack(padx=5, pady=2)

    def add_product(self):
        """Add new product"""
        messagebox.showinfo("قريباً", "ستتم إضافة نافذة إضافة المنتجات قريباً")

    def edit_product(self, product):
        """Edit product"""
        messagebox.showinfo("قريباً", f"ستتم إضافة نافذة تعديل المنتج: {product['name']}")

    def delete_product(self, product):
        """Delete product"""
        if messagebox.askyesno("تأكيد الحذف", f"هل تريد حذف المنتج: {product['name']}؟"):
            try:
                self.db_manager.delete_product(product['id'])
                self.load_products()
                messagebox.showinfo("نجح", "تم حذف المنتج بنجاح")
            except Exception as e:
                messagebox.showerror("خطأ", f"حدث خطأ في حذف المنتج: {e}")

    def search_products(self):
        """Search products"""
        search_term = self.search_entry.get().strip()
        if not search_term:
            self.load_products()
            return

        try:
            # Simple search implementation
            all_products = self.db_manager.get_all_products()
            filtered_products = [
                product for product in all_products
                if search_term.lower() in product['name'].lower() or
                   search_term.lower() in product['brand'].lower()
            ]

            # Clear existing widgets
            for widget in self.products_frame.winfo_children():
                widget.destroy()

            if not filtered_products:
                no_results_label = ctk.CTkLabel(
                    self.products_frame,
                    text=f"لا توجد نتائج للبحث: {search_term}",
                    font=create_body_font(14)
                )
                no_results_label.pack(pady=50)
            else:
                for product in filtered_products:
                    self.create_product_card(product)

        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ في البحث: {e}")
