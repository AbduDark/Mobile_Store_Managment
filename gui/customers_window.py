#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Customers Management Window for Mobile Shop Management System
نافذة إدارة العملاء لنظام إدارة محل الموبايلات
"""

import customtkinter as ctk
from tkinter import messagebox
import sys
import os
from datetime import datetime

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class CustomersWindow(ctk.CTkFrame):
    """Customers management window"""
    
    def __init__(self, parent, db_manager):
        super().__init__(parent)
        self.db_manager = db_manager
        self.customers = []
        self.selected_customer = None
        
        self.create_widgets()
        self.refresh_customers()
    
    def create_widgets(self):
        """Create the customers management interface"""
        # Title
        self.title_label = ctk.CTkLabel(
            self,
            text="إدارة العملاء",
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
        
        # Customers list frame
        self.create_customers_list()
        
        # Customer form frame
        self.create_customer_form()
    
    def create_customers_list(self):
        """Create customers list with search and controls"""
        # Left frame for customers list
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
            placeholder_text="بحث العملاء...",
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
            text="إضافة عميل جديد",
            command=self.add_new_customer,
            font=ctk.CTkFont(size=14),
            height=35
        )
        self.add_btn.pack(side="left", padx=(0, 10))
        
        # Edit button
        self.edit_btn = ctk.CTkButton(
            self.buttons_frame,
            text="تعديل",
            command=self.edit_selected_customer,
            font=ctk.CTkFont(size=14),
            height=35,
            state="disabled"
        )
        self.edit_btn.pack(side="left", padx=5)
        
        # Delete button
        self.delete_btn = ctk.CTkButton(
            self.buttons_frame,
            text="حذف",
            command=self.delete_selected_customer,
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
            command=self.refresh_customers,
            font=ctk.CTkFont(size=14),
            height=35
        )
        self.refresh_btn.pack(side="right")
        
        # Customers scrollable frame
        self.customers_scroll = ctk.CTkScrollableFrame(self.list_frame)
        self.customers_scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    
    def create_customer_form(self):
        """Create customer form for adding/editing"""
        # Right frame for customer form
        self.form_frame = ctk.CTkFrame(self.main_container)
        self.form_frame.grid(row=0, column=1, padx=(10, 0), pady=0, sticky="nsew")
        
        # Form title
        self.form_title = ctk.CTkLabel(
            self.form_frame,
            text="إضافة عميل جديد",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.form_title.pack(pady=(20, 10))
        
        # Form scrollable frame
        self.form_scroll = ctk.CTkScrollableFrame(self.form_frame)
        self.form_scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Customer name
        self.name_label = ctk.CTkLabel(self.form_scroll, text="اسم العميل *", anchor="w")
        self.name_label.pack(fill="x", pady=(10, 5))
        
        self.name_entry = ctk.CTkEntry(
            self.form_scroll,
            placeholder_text="أدخل اسم العميل",
            font=ctk.CTkFont(size=14)
        )
        self.name_entry.pack(fill="x", pady=(0, 10))
        
        # Phone
        self.phone_label = ctk.CTkLabel(self.form_scroll, text="رقم الهاتف *", anchor="w")
        self.phone_label.pack(fill="x", pady=(10, 5))
        
        self.phone_entry = ctk.CTkEntry(
            self.form_scroll,
            placeholder_text="أدخل رقم الهاتف",
            font=ctk.CTkFont(size=14)
        )
        self.phone_entry.pack(fill="x", pady=(0, 10))
        
        # Email
        self.email_label = ctk.CTkLabel(self.form_scroll, text="البريد الإلكتروني", anchor="w")
        self.email_label.pack(fill="x", pady=(10, 5))
        
        self.email_entry = ctk.CTkEntry(
            self.form_scroll,
            placeholder_text="أدخل البريد الإلكتروني (اختياري)",
            font=ctk.CTkFont(size=14)
        )
        self.email_entry.pack(fill="x", pady=(0, 10))
        
        # Address
        self.address_label = ctk.CTkLabel(self.form_scroll, text="العنوان", anchor="w")
        self.address_label.pack(fill="x", pady=(10, 5))
        
        self.address_text = ctk.CTkTextbox(
            self.form_scroll,
            height=80,
            font=ctk.CTkFont(size=14)
        )
        self.address_text.pack(fill="x", pady=(0, 10))
        
        # Notes
        self.notes_label = ctk.CTkLabel(self.form_scroll, text="ملاحظات", anchor="w")
        self.notes_label.pack(fill="x", pady=(10, 5))
        
        self.notes_text = ctk.CTkTextbox(
            self.form_scroll,
            height=80,
            font=ctk.CTkFont(size=14)
        )
        self.notes_text.pack(fill="x", pady=(0, 10))
        
        # Customer statistics (read-only)
        self.stats_frame = ctk.CTkFrame(self.form_scroll)
        self.stats_frame.pack(fill="x", pady=(20, 0))
        
        self.stats_title = ctk.CTkLabel(
            self.stats_frame,
            text="إحصائيات العميل",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.stats_title.pack(pady=(15, 10))
        
        # Total purchases
        self.total_purchases_label = ctk.CTkLabel(
            self.stats_frame,
            text="إجمالي المشتريات: 0.00 ريال",
            font=ctk.CTkFont(size=14)
        )
        self.total_purchases_label.pack(pady=5)
        
        # Loyalty points
        self.loyalty_points_label = ctk.CTkLabel(
            self.stats_frame,
            text="نقاط الولاء: 0",
            font=ctk.CTkFont(size=14)
        )
        self.loyalty_points_label.pack(pady=5)
        
        # Join date
        self.join_date_label = ctk.CTkLabel(
            self.stats_frame,
            text="تاريخ الانضمام: -",
            font=ctk.CTkFont(size=14)
        )
        self.join_date_label.pack(pady=(5, 15))
        
        # Form buttons
        self.form_buttons_frame = ctk.CTkFrame(self.form_scroll)
        self.form_buttons_frame.pack(fill="x", pady=20)
        
        self.save_btn = ctk.CTkButton(
            self.form_buttons_frame,
            text="حفظ",
            command=self.save_customer,
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
        
        # View purchases button
        self.view_purchases_btn = ctk.CTkButton(
            self.form_buttons_frame,
            text="عرض المشتريات",
            command=self.view_customer_purchases,
            font=ctk.CTkFont(size=14),
            height=35,
            state="disabled"
        )
        self.view_purchases_btn.pack(side="bottom", padx=10, pady=(0, 10))
    
    def refresh_customers(self):
        """Refresh customers list"""
        try:
            self.customers = self.db_manager.get_all_customers()
            self.display_customers()
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ في تحديث العملاء: {e}")
    
    def display_customers(self, customers=None):
        """Display customers in the list"""
        # Clear existing customers
        for widget in self.customers_scroll.winfo_children():
            widget.destroy()
        
        customers_to_show = customers if customers is not None else self.customers
        
        if not customers_to_show:
            no_customers_label = ctk.CTkLabel(
                self.customers_scroll,
                text="لا يوجد عملاء",
                font=ctk.CTkFont(size=16)
            )
            no_customers_label.pack(pady=50)
            return
        
        for customer in customers_to_show:
            self.create_customer_card(customer)
    
    def create_customer_card(self, customer):
        """Create a customer card widget"""
        card_frame = ctk.CTkFrame(self.customers_scroll)
        card_frame.pack(fill="x", pady=5)
        
        # Customer info
        info_frame = ctk.CTkFrame(card_frame)
        info_frame.pack(fill="x", padx=10, pady=10)
        
        # Name and phone
        name_label = ctk.CTkLabel(
            info_frame,
            text=f"{customer['name']}",
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w"
        )
        name_label.pack(fill="x", padx=10, pady=(10, 5))
        
        # Phone
        phone_label = ctk.CTkLabel(
            info_frame,
            text=f"📞 {customer['phone']}",
            font=ctk.CTkFont(size=14),
            anchor="w"
        )
        phone_label.pack(fill="x", padx=10, pady=2)
        
        # Email (if available)
        if customer['email']:
            email_label = ctk.CTkLabel(
                info_frame,
                text=f"📧 {customer['email']}",
                font=ctk.CTkFont(size=12),
                anchor="w"
            )
            email_label.pack(fill="x", padx=10, pady=2)
        
        # Statistics
        stats_text = f"المشتريات: {customer['total_purchases']:.2f} ريال | نقاط الولاء: {customer['loyalty_points']}"
        stats_label = ctk.CTkLabel(
            info_frame,
            text=stats_text,
            font=ctk.CTkFont(size=12),
            anchor="w",
            text_color="green"
        )
        stats_label.pack(fill="x", padx=10, pady=(5, 10))
        
        # Click handler
        def on_card_click(event, cust=customer):
            self.select_customer(cust)
        
        # Bind click events to all card components
        for widget in [card_frame, info_frame, name_label, phone_label, stats_label]:
            widget.bind("<Button-1>", on_card_click)
            widget.configure(cursor="hand2")
    
    def select_customer(self, customer):
        """Select a customer and load it in the form"""
        self.selected_customer = customer
        self.load_customer_in_form(customer)
        
        # Enable edit, delete, and view purchases buttons
        self.edit_btn.configure(state="normal")
        self.delete_btn.configure(state="normal")
        self.view_purchases_btn.configure(state="normal")
        
        # Update form title
        self.form_title.configure(text=f"تعديل: {customer['name']}")
    
    def load_customer_in_form(self, customer):
        """Load customer data into the form"""
        self.name_entry.delete(0, "end")
        self.name_entry.insert(0, customer['name'])
        
        self.phone_entry.delete(0, "end")
        self.phone_entry.insert(0, customer['phone'] or "")
        
        self.email_entry.delete(0, "end")
        self.email_entry.insert(0, customer['email'] or "")
        
        self.address_text.delete("1.0", "end")
        self.address_text.insert("1.0", customer['address'] or "")
        
        self.notes_text.delete("1.0", "end")
        self.notes_text.insert("1.0", customer['notes'] or "")
        
        # Update statistics
        self.total_purchases_label.configure(
            text=f"إجمالي المشتريات: {customer['total_purchases']:.2f} ريال"
        )
        self.loyalty_points_label.configure(
            text=f"نقاط الولاء: {customer['loyalty_points']}"
        )
        
        # Format join date
        if customer['created_at']:
            try:
                created_date = datetime.fromisoformat(customer['created_at'].replace('Z', '+00:00'))
                formatted_date = created_date.strftime('%Y-%m-%d')
                self.join_date_label.configure(text=f"تاريخ الانضمام: {formatted_date}")
            except:
                self.join_date_label.configure(text="تاريخ الانضمام: -")
        else:
            self.join_date_label.configure(text="تاريخ الانضمام: -")
    
    def add_new_customer(self):
        """Prepare form for adding new customer"""
        self.selected_customer = None
        self.clear_form()
        self.form_title.configure(text="إضافة عميل جديد")
        
        # Disable edit, delete, and view purchases buttons
        self.edit_btn.configure(state="disabled")
        self.delete_btn.configure(state="disabled")
        self.view_purchases_btn.configure(state="disabled")
    
    def edit_selected_customer(self):
        """Edit the selected customer"""
        if not self.selected_customer:
            messagebox.showwarning("تحذير", "يرجى اختيار عميل للتعديل")
            return
        
        # Form is already loaded with customer data
        pass
    
    def delete_selected_customer(self):
        """Delete the selected customer"""
        if not self.selected_customer:
            messagebox.showwarning("تحذير", "يرجى اختيار عميل للحذف")
            return
        
        if messagebox.askyesno("تأكيد الحذف", f"هل تريد حذف العميل '{self.selected_customer['name']}'؟\n\nملاحظة: سيتم الاحتفاظ بسجل المبيعات السابقة"):
            try:
                # Delete customer
                query = "DELETE FROM customers WHERE id = ?"
                self.db_manager.execute_non_query(query, (self.selected_customer['id'],))
                
                messagebox.showinfo("نجح", "تم حذف العميل بنجاح")
                self.refresh_customers()
                self.clear_form()
            except Exception as e:
                messagebox.showerror("خطأ", f"حدث خطأ في حذف العميل: {e}")
    
    def save_customer(self):
        """Save the customer (add or update)"""
        try:
            # Validate required fields
            if not self.name_entry.get().strip():
                messagebox.showerror("خطأ", "اسم العميل مطلوب")
                return
            
            if not self.phone_entry.get().strip():
                messagebox.showerror("خطأ", "رقم الهاتف مطلوب")
                return
            
            # Check for duplicate phone number (except for current customer)
            phone = self.phone_entry.get().strip()
            existing_customer = self.db_manager.get_customer_by_phone(phone)
            if existing_customer and (not self.selected_customer or existing_customer['id'] != self.selected_customer['id']):
                messagebox.showerror("خطأ", "رقم الهاتف مستخدم بالفعل من عميل آخر")
                return
            
            # Prepare customer data
            customer_data = {
                'name': self.name_entry.get().strip(),
                'phone': phone,
                'email': self.email_entry.get().strip(),
                'address': self.address_text.get("1.0", "end").strip(),
                'notes': self.notes_text.get("1.0", "end").strip()
            }
            
            if self.selected_customer:
                # Update existing customer
                query = '''
                    UPDATE customers SET name=?, phone=?, email=?, address=?, notes=?,
                                       updated_at=CURRENT_TIMESTAMP
                    WHERE id=?
                '''
                params = (
                    customer_data['name'],
                    customer_data['phone'],
                    customer_data['email'],
                    customer_data['address'],
                    customer_data['notes'],
                    self.selected_customer['id']
                )
                self.db_manager.execute_non_query(query, params)
                messagebox.showinfo("نجح", "تم تحديث العميل بنجاح")
            else:
                # Add new customer
                self.db_manager.add_customer(customer_data)
                messagebox.showinfo("نجح", "تم إضافة العميل بنجاح")
            
            self.refresh_customers()
            self.clear_form()
            
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ في حفظ العميل: {e}")
    
    def clear_form(self):
        """Clear the customer form"""
        self.name_entry.delete(0, "end")
        self.phone_entry.delete(0, "end")
        self.email_entry.delete(0, "end")
        self.address_text.delete("1.0", "end")
        self.notes_text.delete("1.0", "end")
        self.selected_customer = None
        
        # Reset statistics
        self.total_purchases_label.configure(text="إجمالي المشتريات: 0.00 ريال")
        self.loyalty_points_label.configure(text="نقاط الولاء: 0")
        self.join_date_label.configure(text="تاريخ الانضمام: -")
        
        # Update form title
        self.form_title.configure(text="إضافة عميل جديد")
        
        # Disable edit, delete, and view purchases buttons
        self.edit_btn.configure(state="disabled")
        self.delete_btn.configure(state="disabled")
        self.view_purchases_btn.configure(state="disabled")
    
    def view_customer_purchases(self):
        """View customer purchase history"""
        if not self.selected_customer:
            messagebox.showwarning("تحذير", "يرجى اختيار عميل لعرض مشترياته")
            return
        
        try:
            # Get customer purchases
            query = '''
                SELECT s.*, GROUP_CONCAT(p.name || ' (x' || si.quantity || ')', ' | ') as items
                FROM sales s
                LEFT JOIN sale_items si ON s.id = si.sale_id
                LEFT JOIN products p ON si.product_id = p.id
                WHERE s.customer_id = ?
                GROUP BY s.id
                ORDER BY s.sale_date DESC
            '''
            purchases = self.db_manager.execute_query(query, (self.selected_customer['id'],))
            
            # Create purchases window
            self.show_purchases_window(purchases)
            
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ في جلب المشتريات: {e}")
    
    def show_purchases_window(self, purchases):
        """Show customer purchases in a new window"""
        # Create purchases window
        purchases_window = ctk.CTkToplevel(self)
        purchases_window.title(f"مشتريات العميل: {self.selected_customer['name']}")
        purchases_window.geometry("800x600")
        purchases_window.transient(self)
        purchases_window.grab_set()
        
        # Title
        title_label = ctk.CTkLabel(
            purchases_window,
            text=f"مشتريات العميل: {self.selected_customer['name']}",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=20)
        
        if not purchases:
            no_purchases_label = ctk.CTkLabel(
                purchases_window,
                text="لا توجد مشتريات لهذا العميل",
                font=ctk.CTkFont(size=16)
            )
            no_purchases_label.pack(pady=50)
            return
        
        # Purchases list
        purchases_scroll = ctk.CTkScrollableFrame(purchases_window)
        purchases_scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        total_amount = 0
        for purchase in purchases:
            # Purchase card
            card_frame = ctk.CTkFrame(purchases_scroll)
            card_frame.pack(fill="x", pady=5)
            
            # Purchase info
            info_frame = ctk.CTkFrame(card_frame)
            info_frame.pack(fill="x", padx=10, pady=10)
            
            # Date and amount
            try:
                purchase_date = datetime.fromisoformat(purchase['sale_date'].replace('Z', '+00:00'))
                formatted_date = purchase_date.strftime('%Y-%m-%d %H:%M')
            except:
                formatted_date = purchase['sale_date']
            
            date_amount_label = ctk.CTkLabel(
                info_frame,
                text=f"التاريخ: {formatted_date} | المبلغ: {purchase['total_amount']:.2f} ريال",
                font=ctk.CTkFont(size=14, weight="bold"),
                anchor="w"
            )
            date_amount_label.pack(fill="x", padx=10, pady=5)
            
            # Items
            if purchase['items']:
                items_label = ctk.CTkLabel(
                    info_frame,
                    text=f"العناصر: {purchase['items']}",
                    font=ctk.CTkFont(size=12),
                    anchor="w",
                    wraplength=700
                )
                items_label.pack(fill="x", padx=10, pady=2)
            
            # Payment method
            payment_label = ctk.CTkLabel(
                info_frame,
                text=f"طريقة الدفع: {purchase['payment_method']} | الحالة: {purchase['payment_status']}",
                font=ctk.CTkFont(size=12),
                anchor="w"
            )
            payment_label.pack(fill="x", padx=10, pady=(2, 10))
            
            total_amount += purchase['total_amount']
        
        # Summary
        summary_frame = ctk.CTkFrame(purchases_window)
        summary_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        summary_label = ctk.CTkLabel(
            summary_frame,
            text=f"إجمالي عدد المشتريات: {len(purchases)} | إجمالي المبلغ: {total_amount:.2f} ريال",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        summary_label.pack(pady=15)
        
        # Close button
        close_btn = ctk.CTkButton(
            purchases_window,
            text="إغلاق",
            command=purchases_window.destroy,
            width=100
        )
        close_btn.pack(pady=(0, 20))
    
    def on_search_change(self, *args):
        """Handle search input change"""
        search_term = self.search_var.get().lower()
        
        if not search_term:
            self.display_customers()
            return
        
        # Filter customers based on search term
        filtered_customers = []
        for customer in self.customers:
            if (search_term in customer['name'].lower() or
                search_term in (customer['phone'] or "").lower() or
                search_term in (customer['email'] or "").lower()):
                filtered_customers.append(customer)
        
        self.display_customers(filtered_customers)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Customers Window for Mobile Shop Management System
نافذة العملاء لنظام إدارة محل الموبايلات
"""

import customtkinter as ctk
from tkinter import messagebox
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.arabic_support import create_title_font, create_heading_font, create_button_font, create_body_font

class CustomersWindow(ctk.CTkFrame):
    """Customers management window"""

    def __init__(self, parent, db_manager):
        super().__init__(parent)
        self.db_manager = db_manager
        self.create_widgets()
        self.load_customers()

    def create_widgets(self):
        """Create the customers interface"""
        # Title
        self.title_label = ctk.CTkLabel(
            self,
            text="إدارة العملاء",
            font=create_title_font(28)
        )
        self.title_label.pack(pady=(0, 20))

        # Controls frame
        self.controls_frame = ctk.CTkFrame(self)
        self.controls_frame.pack(fill="x", padx=20, pady=(0, 20))

        # Add customer button
        self.add_button = ctk.CTkButton(
            self.controls_frame,
            text="إضافة عميل جديد",
            command=self.add_customer,
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
            placeholder_text="البحث في العملاء...",
            width=200
        )
        self.search_entry.pack(side="left", padx=5, pady=5)

        self.search_button = ctk.CTkButton(
            self.search_frame,
            text="بحث",
            command=self.search_customers,
            width=80
        )
        self.search_button.pack(side="left", padx=5, pady=5)

        # Customers list
        self.customers_frame = ctk.CTkScrollableFrame(self, label_text="قائمة العملاء")
        self.customers_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def load_customers(self):
        """Load customers from database"""
        try:
            customers = self.db_manager.get_all_customers()
            
            # Clear existing widgets
            for widget in self.customers_frame.winfo_children():
                widget.destroy()

            if not customers:
                no_customers_label = ctk.CTkLabel(
                    self.customers_frame,
                    text="لا توجد عملاء. انقر على 'إضافة عميل جديد' لإضافة عميل.",
                    font=create_body_font(14)
                )
                no_customers_label.pack(pady=50)
                return

            # Create customer cards
            for customer in customers:
                self.create_customer_card(customer)

        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ في تحميل العملاء: {e}")

    def create_customer_card(self, customer):
        """Create a customer card widget"""
        card_frame = ctk.CTkFrame(self.customers_frame)
        card_frame.pack(fill="x", padx=10, pady=5)

        # Customer info
        info_frame = ctk.CTkFrame(card_frame)
        info_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Name
        name_label = ctk.CTkLabel(
            info_frame,
            text=customer['name'],
            font=create_heading_font(16),
            anchor="w"
        )
        name_label.pack(fill="x", padx=10, pady=(10, 5))

        # Details
        phone = customer.get('phone', 'غير محدد')
        total_purchases = customer.get('total_purchases', 0)
        details_text = f"الهاتف: {phone} | إجمالي المشتريات: {total_purchases:.2f} ريال"
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
            command=lambda c=customer: self.edit_customer(c),
            width=80,
            height=30
        )
        edit_button.pack(padx=5, pady=2)

        view_button = ctk.CTkButton(
            buttons_frame,
            text="عرض المشتريات",
            command=lambda c=customer: self.view_customer_purchases(c),
            width=120,
            height=30
        )
        view_button.pack(padx=5, pady=2)

    def add_customer(self):
        """Add new customer"""
        messagebox.showinfo("قريباً", "ستتم إضافة نافذة إضافة العملاء قريباً")

    def edit_customer(self, customer):
        """Edit customer"""
        messagebox.showinfo("قريباً", f"ستتم إضافة نافذة تعديل العميل: {customer['name']}")

    def view_customer_purchases(self, customer):
        """View customer purchases"""
        messagebox.showinfo("مشتريات العميل", f"عرض مشتريات العميل: {customer['name']}")

    def search_customers(self):
        """Search customers"""
        search_term = self.search_entry.get().strip()
        if not search_term:
            self.load_customers()
            return

        try:
            # Simple search implementation
            all_customers = self.db_manager.get_all_customers()
            filtered_customers = [
                customer for customer in all_customers
                if search_term.lower() in customer['name'].lower() or
                   (customer.get('phone') and search_term in customer['phone'])
            ]

            # Clear existing widgets
            for widget in self.customers_frame.winfo_children():
                widget.destroy()

            if not filtered_customers:
                no_results_label = ctk.CTkLabel(
                    self.customers_frame,
                    text=f"لا توجد نتائج للبحث: {search_term}",
                    font=create_body_font(14)
                )
                no_results_label.pack(pady=50)
            else:
                for customer in filtered_customers:
                    self.create_customer_card(customer)

        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ في البحث: {e}")
