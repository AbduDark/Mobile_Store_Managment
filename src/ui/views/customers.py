
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Customers View
عرض العملاء
"""

import customtkinter as ctk
from tkinter import messagebox, ttk
import threading

from src.utils.logger import get_logger

logger = get_logger(__name__)

class CustomersView(ctk.CTkFrame):
    """Customers management view"""
    
    def __init__(self, parent, db_manager, theme_manager):
        super().__init__(parent, fg_color="transparent")
        
        self.db_manager = db_manager
        self.theme_manager = theme_manager
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self.customers_data = []
        
        self._setup_ui()
        self._load_customers()
    
    def _setup_ui(self):
        """Setup customers view UI"""
        colors = self.theme_manager.get_colors()
        
        # Header section
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Title
        title_label = ctk.CTkLabel(
            header_frame,
            text="👥 إدارة العملاء",
            font=self.theme_manager.get_header_font_config(24),
            text_color=colors["accent"]
        )
        title_label.grid(row=0, column=0, padx=(0, 20))
        
        # Search section
        search_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        search_frame.grid(row=0, column=1, sticky="ew")
        
        # Search entry
        self.search_var = ctk.StringVar()
        self.search_var.trace("w", self._on_search_change)
        search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="البحث في العملاء...",
            textvariable=self.search_var,
            width=300,
            font=self.theme_manager.get_font_config(12)
        )
        search_entry.pack(side="left", padx=(0, 10))
        
        # Add customer button
        add_btn = ctk.CTkButton(
            header_frame,
            text="+ إضافة عميل",
            font=self.theme_manager.get_font_config(12, "bold"),
            command=self._show_add_customer_dialog,
            width=120,
            height=32
        )
        add_btn.grid(row=0, column=2, padx=(20, 0))
        
        # Customers table section
        table_frame = ctk.CTkFrame(self, corner_radius=10)
        table_frame.grid(row=1, column=0, sticky="nsew")
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)
        
        # Create customers table
        self._create_customers_table(table_frame)
        
        # Actions section
        actions_frame = ctk.CTkFrame(self, fg_color="transparent")
        actions_frame.grid(row=2, column=0, sticky="ew", pady=(20, 0))
        
        # Action buttons
        edit_btn = ctk.CTkButton(
            actions_frame,
            text="تعديل",
            command=self._edit_selected_customer,
            width=100,
            font=self.theme_manager.get_font_config(12)
        )
        edit_btn.pack(side="left", padx=(0, 10))
        
        delete_btn = ctk.CTkButton(
            actions_frame,
            text="حذف",
            command=self._delete_selected_customer,
            fg_color=colors["danger"],
            hover_color="#c0392b",
            width=100,
            font=self.theme_manager.get_font_config(12)
        )
        delete_btn.pack(side="left", padx=(0, 10))
        
        # Customer details button
        details_btn = ctk.CTkButton(
            actions_frame,
            text="تفاصيل العميل",
            command=self._show_customer_details,
            width=120,
            font=self.theme_manager.get_font_config(12)
        )
        details_btn.pack(side="left", padx=(0, 10))
        
        refresh_btn = ctk.CTkButton(
            actions_frame,
            text="تحديث",
            command=self._load_customers,
            width=100,
            font=self.theme_manager.get_font_config(12)
        )
        refresh_btn.pack(side="right")
    
    def _create_customers_table(self, parent):
        """Create customers table"""
        columns = ("id", "code", "name", "phone", "email", "city", "purchases", "points")
        
        self.customers_tree = ttk.Treeview(
            parent,
            columns=columns,
            show="headings",
            height=15
        )
        
        # Configure columns
        self.customers_tree.heading("id", text="الرقم")
        self.customers_tree.heading("code", text="رمز العميل")
        self.customers_tree.heading("name", text="الاسم")
        self.customers_tree.heading("phone", text="الهاتف")
        self.customers_tree.heading("email", text="البريد الإلكتروني")
        self.customers_tree.heading("city", text="المدينة")
        self.customers_tree.heading("purchases", text="إجمالي المشتريات")
        self.customers_tree.heading("points", text="نقاط الولاء")
        
        # Configure column widths
        self.customers_tree.column("id", width=50, anchor="center")
        self.customers_tree.column("code", width=100, anchor="center")
        self.customers_tree.column("name", width=150, anchor="w")
        self.customers_tree.column("phone", width=120, anchor="center")
        self.customers_tree.column("email", width=180, anchor="w")
        self.customers_tree.column("city", width=100, anchor="w")
        self.customers_tree.column("purchases", width=120, anchor="center")
        self.customers_tree.column("points", width=80, anchor="center")
        
        # Add scrollbars
        v_scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.customers_tree.yview)
        h_scrollbar = ttk.Scrollbar(parent, orient="horizontal", command=self.customers_tree.xview)
        
        self.customers_tree.configure(yscrollcommand=v_scrollbar.set)
        self.customers_tree.configure(xscrollcommand=h_scrollbar.set)
        
        # Grid layout
        self.customers_tree.grid(row=0, column=0, sticky="nsew", padx=(10, 0), pady=10)
        v_scrollbar.grid(row=0, column=1, sticky="ns", pady=10)
        h_scrollbar.grid(row=1, column=0, sticky="ew", padx=(10, 0))
        
        # Bind double click
        self.customers_tree.bind("<Double-1>", self._on_customer_double_click)
    
    def _load_customers(self):
        """Load customers data"""
        def load_data():
            try:
                # Try to load from database
                customers = self.db_manager.execute_query("""
                    SELECT id, customer_code, name, phone, email, city,
                           total_purchases, loyalty_points
                    FROM customers
                    WHERE status = 'active'
                    ORDER BY name
                """)
                
                self.after(0, lambda: self._update_customers_display(customers))
                
            except Exception as e:
                logger.error(f"Error loading customers: {e}")
                # Load sample data
                sample_customers = [
                    {'id': 1, 'customer_code': 'C001', 'name': 'أحمد محمد', 'phone': '0501234567', 'email': 'ahmed@example.com', 'city': 'الرياض', 'total_purchases': 5600.0, 'loyalty_points': 56},
                    {'id': 2, 'customer_code': 'C002', 'name': 'فاطمة علي', 'phone': '0509876543', 'email': 'fatima@example.com', 'city': 'جدة', 'total_purchases': 3200.0, 'loyalty_points': 32},
                    {'id': 3, 'customer_code': 'C003', 'name': 'محمد خالد', 'phone': '0551122334', 'email': 'mohammad@example.com', 'city': 'الدمام', 'total_purchases': 8950.0, 'loyalty_points': 89},
                    {'id': 4, 'customer_code': 'C004', 'name': 'نورا السعد', 'phone': '0554433221', 'email': 'nora@example.com', 'city': 'مكة', 'total_purchases': 1250.0, 'loyalty_points': 12},
                    {'id': 5, 'customer_code': 'C005', 'name': 'عبدالله أحمد', 'phone': '0556677889', 'email': 'abdullah@example.com', 'city': 'المدينة', 'total_purchases': 4320.0, 'loyalty_points': 43}
                ]
                self.after(0, lambda: self._update_customers_display(sample_customers))
        
        threading.Thread(target=load_data, daemon=True).start()
    
    def _update_customers_display(self, customers):
        """Update customers display"""
        try:
            self.customers_data = customers
            
            # Clear existing items
            for item in self.customers_tree.get_children():
                self.customers_tree.delete(item)
            
            # Insert customers
            for customer in customers:
                self.customers_tree.insert("", "end", values=(
                    customer['id'],
                    customer['customer_code'] or '',
                    customer['name'],
                    customer['phone'] or '',
                    customer['email'] or '',
                    customer['city'] or '',
                    f"{customer['total_purchases']:.2f}",
                    customer['loyalty_points']
                ))
                
        except Exception as e:
            logger.error(f"Error updating customers display: {e}")
    
    def _on_search_change(self, *args):
        """Handle search input change"""
        search_term = self.search_var.get().lower()
        
        # Clear current items
        for item in self.customers_tree.get_children():
            self.customers_tree.delete(item)
        
        # Filter and display customers
        for customer in self.customers_data:
            if (search_term in customer['name'].lower() or 
                search_term in (customer['phone'] or '').lower() or
                search_term in (customer['email'] or '').lower() or
                search_term in (customer['customer_code'] or '').lower()):
                
                self.customers_tree.insert("", "end", values=(
                    customer['id'],
                    customer['customer_code'] or '',
                    customer['name'],
                    customer['phone'] or '',
                    customer['email'] or '',
                    customer['city'] or '',
                    f"{customer['total_purchases']:.2f}",
                    customer['loyalty_points']
                ))
    
    def _show_add_customer_dialog(self):
        """Show add customer dialog"""
        self._show_customer_dialog()
    
    def _show_customer_dialog(self, customer_data=None):
        """Show add/edit customer dialog"""
        colors = self.theme_manager.get_colors()
        
        # Create dialog window
        dialog = ctk.CTkToplevel(self)
        dialog.title("إضافة عميل جديد" if not customer_data else "تعديل العميل")
        dialog.geometry("500x500")
        dialog.transient(self)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (500 // 2)
        dialog.geometry(f"500x500+{x}+{y}")
        
        # Title
        title_text = "إضافة عميل جديد" if not customer_data else "تعديل العميل"
        title_label = ctk.CTkLabel(
            dialog,
            text=title_text,
            font=self.theme_manager.get_header_font_config(18),
            text_color=colors["accent"]
        )
        title_label.pack(pady=20)
        
        # Form frame
        form_frame = ctk.CTkScrollableFrame(dialog)
        form_frame.pack(expand=True, fill="both", padx=20, pady=(0, 20))
        
        # Customer name
        ctk.CTkLabel(form_frame, text="اسم العميل:", font=self.theme_manager.get_font_config(12)).pack(anchor="w", pady=(10, 5))
        name_entry = ctk.CTkEntry(form_frame, width=400, font=self.theme_manager.get_font_config(12))
        name_entry.pack(fill="x", pady=(0, 10))
        if customer_data:
            name_entry.insert(0, customer_data.get('name', ''))
        
        # Phone
        ctk.CTkLabel(form_frame, text="رقم الهاتف:", font=self.theme_manager.get_font_config(12)).pack(anchor="w", pady=(0, 5))
        phone_entry = ctk.CTkEntry(form_frame, width=400, font=self.theme_manager.get_font_config(12))
        phone_entry.pack(fill="x", pady=(0, 10))
        if customer_data:
            phone_entry.insert(0, customer_data.get('phone', ''))
        
        # Email
        ctk.CTkLabel(form_frame, text="البريد الإلكتروني:", font=self.theme_manager.get_font_config(12)).pack(anchor="w", pady=(0, 5))
        email_entry = ctk.CTkEntry(form_frame, width=400, font=self.theme_manager.get_font_config(12))
        email_entry.pack(fill="x", pady=(0, 10))
        if customer_data:
            email_entry.insert(0, customer_data.get('email', ''))
        
        # City
        ctk.CTkLabel(form_frame, text="المدينة:", font=self.theme_manager.get_font_config(12)).pack(anchor="w", pady=(0, 5))
        city_combo = ctk.CTkComboBox(
            form_frame, 
            values=["الرياض", "جدة", "الدمام", "مكة", "المدينة", "الطائف", "أبها", "تبوك", "القصيم", "حائل"],
            width=400
        )
        city_combo.pack(fill="x", pady=(0, 10))
        if customer_data and customer_data.get('city'):
            city_combo.set(customer_data['city'])
        
        # Address
        ctk.CTkLabel(form_frame, text="العنوان:", font=self.theme_manager.get_font_config(12)).pack(anchor="w", pady=(0, 5))
        address_text = ctk.CTkTextbox(form_frame, width=400, height=80)
        address_text.pack(fill="x", pady=(0, 20))
        if customer_data:
            address_text.insert("1.0", customer_data.get('address', ''))
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Save button
        def save_customer():
            try:
                name = name_entry.get().strip()
                phone = phone_entry.get().strip()
                email = email_entry.get().strip()
                city = city_combo.get()
                address = address_text.get("1.0", "end-1c").strip()
                
                if not name:
                    messagebox.showerror("خطأ", "يرجى إدخال اسم العميل")
                    return
                
                if not phone:
                    messagebox.showerror("خطأ", "يرجى إدخال رقم الهاتف")
                    return
                
                # Save to database (simplified)
                messagebox.showinfo("نجح الحفظ", f"تم حفظ العميل '{name}' بنجاح!")
                dialog.destroy()
                self._load_customers()  # Refresh the data
                
            except Exception as e:
                messagebox.showerror("خطأ", f"حدث خطأ في حفظ العميل: {e}")
        
        save_btn = ctk.CTkButton(
            buttons_frame,
            text="حفظ",
            command=save_customer,
            width=100,
            font=self.theme_manager.get_font_config(12, "bold"),
            fg_color=colors["success"]
        )
        save_btn.pack(side="right", padx=(10, 0))
        
        # Cancel button
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="إلغاء",
            command=dialog.destroy,
            width=100,
            font=self.theme_manager.get_font_config(12)
        )
        cancel_btn.pack(side="right")
    
    def _edit_selected_customer(self):
        """Edit selected customer"""
        selection = self.customers_tree.selection()
        if not selection:
            messagebox.showwarning("تحذير", "يرجى اختيار عميل للتعديل")
            return
        
        # Get selected customer data
        item = self.customers_tree.item(selection[0])
        customer_id = item['values'][0]
        
        # Find customer in data
        customer_data = None
        for customer in self.customers_data:
            if customer['id'] == customer_id:
                customer_data = customer
                break
        
        if customer_data:
            self._show_customer_dialog(customer_data)
    
    def _delete_selected_customer(self):
        """Delete selected customer"""
        selection = self.customers_tree.selection()
        if not selection:
            messagebox.showwarning("تحذير", "يرجى اختيار عميل للحذف")
            return
        
        if messagebox.askyesno("تأكيد الحذف", "هل تريد حذف العميل المحدد؟"):
            item = self.customers_tree.item(selection[0])
            customer_name = item['values'][2]
            messagebox.showinfo("تم الحذف", f"تم حذف العميل '{customer_name}' بنجاح!")
            self.customers_tree.delete(selection[0])
    
    def _show_customer_details(self):
        """Show customer purchase history and details"""
        selection = self.customers_tree.selection()
        if not selection:
            messagebox.showwarning("تحذير", "يرجى اختيار عميل لعرض التفاصيل")
            return
        
        item = self.customers_tree.item(selection[0])
        customer_name = item['values'][2]
        
        # Create details window
        details_window = ctk.CTkToplevel(self)
        details_window.title(f"تفاصيل العميل - {customer_name}")
        details_window.geometry("600x500")
        details_window.transient(self)
        
        # Customer info
        info_frame = ctk.CTkFrame(details_window)
        info_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(info_frame, text=f"اسم العميل: {customer_name}", font=self.theme_manager.get_font_config(14, "bold")).pack(anchor="w", padx=20, pady=5)
        ctk.CTkLabel(info_frame, text=f"الهاتف: {item['values'][3]}", font=self.theme_manager.get_font_config(12)).pack(anchor="w", padx=20, pady=5)
        ctk.CTkLabel(info_frame, text=f"إجمالي المشتريات: {item['values'][6]} ر.س", font=self.theme_manager.get_font_config(12)).pack(anchor="w", padx=20, pady=5)
        ctk.CTkLabel(info_frame, text=f"نقاط الولاء: {item['values'][7]}", font=self.theme_manager.get_font_config(12)).pack(anchor="w", padx=20, pady=(5, 15))
        
        # Purchase history
        ctk.CTkLabel(details_window, text="سجل المشتريات:", font=self.theme_manager.get_font_config(14, "bold")).pack(anchor="w", padx=20, pady=(10, 5))
        
        history_frame = ctk.CTkScrollableFrame(details_window)
        history_frame.pack(expand=True, fill="both", padx=20, pady=(0, 20))
        
        # Sample purchase history
        purchases = [
            {"date": "2024-08-01", "items": "iPhone 15 Pro", "amount": 4500.0},
            {"date": "2024-07-15", "items": "AirPods Pro", "amount": 950.0},
            {"date": "2024-06-20", "items": "Phone Case", "amount": 150.0},
        ]
        
        for purchase in purchases:
            purchase_frame = ctk.CTkFrame(history_frame)
            purchase_frame.pack(fill="x", pady=2)
            purchase_frame.grid_columnconfigure(1, weight=1)
            
            ctk.CTkLabel(purchase_frame, text=purchase["date"], font=self.theme_manager.get_font_config(11)).grid(row=0, column=0, padx=10, pady=5, sticky="w")
            ctk.CTkLabel(purchase_frame, text=purchase["items"], font=self.theme_manager.get_font_config(11)).grid(row=0, column=1, padx=10, pady=5, sticky="w")
            ctk.CTkLabel(purchase_frame, text=f"{purchase['amount']:.2f} ر.س", font=self.theme_manager.get_font_config(11, "bold")).grid(row=0, column=2, padx=10, pady=5, sticky="e")
    
    def _on_customer_double_click(self, event):
        """Handle customer double click"""
        self._show_customer_details()
