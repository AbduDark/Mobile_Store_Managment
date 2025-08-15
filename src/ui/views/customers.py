
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
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=colors["accent"]
        )
        title_label.grid(row=0, column=0, padx=(0, 20))
        
        # Search section
        search_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        search_frame.grid(row=0, column=1, sticky="ew")
        
        # Search entry
        self.search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="البحث في العملاء...",
            textvariable=self.search_var,
            width=300,
            font=ctk.CTkFont(size=12)
        )
        search_entry.pack(side="left", padx=(0, 10))
        
        # Add customer button
        add_btn = ctk.CTkButton(
            header_frame,
            text="+ إضافة عميل",
            font=ctk.CTkFont(size=12, weight="bold"),
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
            width=100
        )
        edit_btn.pack(side="left", padx=(0, 10))
        
        delete_btn = ctk.CTkButton(
            actions_frame,
            text="حذف",
            command=self._delete_selected_customer,
            fg_color=colors["danger"],
            hover_color="#c0392b",
            width=100
        )
        delete_btn.pack(side="left", padx=(0, 10))
        
        # Customer details button
        details_btn = ctk.CTkButton(
            actions_frame,
            text="تفاصيل العميل",
            command=self._show_customer_details,
            width=120
        )
        details_btn.pack(side="left", padx=(0, 10))
        
        refresh_btn = ctk.CTkButton(
            actions_frame,
            text="تحديث",
            command=self._load_customers,
            width=100
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
                self.after(0, lambda: messagebox.showerror("خطأ", f"حدث خطأ في تحميل العملاء: {e}"))
        
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
    
    def _show_add_customer_dialog(self):
        """Show add customer dialog"""
        messagebox.showinfo("قريباً", "نافذة إضافة العميل قيد التطوير")
    
    def _edit_selected_customer(self):
        """Edit selected customer"""
        selection = self.customers_tree.selection()
        if not selection:
            messagebox.showwarning("تحذير", "يرجى اختيار عميل للتعديل")
            return
        
        messagebox.showinfo("قريباً", "نافذة تعديل العميل قيد التطوير")
    
    def _delete_selected_customer(self):
        """Delete selected customer"""
        selection = self.customers_tree.selection()
        if not selection:
            messagebox.showwarning("تحذير", "يرجى اختيار عميل للحذف")
            return
        
        if messagebox.askyesno("تأكيد الحذف", "هل تريد حذف العميل المحدد؟"):
            messagebox.showinfo("قريباً", "حذف العميل قيد التطوير")
    
    def _show_customer_details(self):
        """Show customer purchase history and details"""
        selection = self.customers_tree.selection()
        if not selection:
            messagebox.showwarning("تحذير", "يرجى اختيار عميل لعرض التفاصيل")
            return
        
        messagebox.showinfo("قريباً", "نافذة تفاصيل العميل قيد التطوير")
    
    def _on_customer_double_click(self, event):
        """Handle customer double click"""
        self._show_customer_details()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Customers View
عرض العملاء
"""

import customtkinter as ctk

class CustomersView(ctk.CTkFrame):
    """Customers management view"""
    
    def __init__(self, parent, db_manager, theme_manager):
        super().__init__(parent)
        
        self.db_manager = db_manager
        self.theme_manager = theme_manager
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create customers view widgets"""
        title_label = ctk.CTkLabel(
            self,
            text="إدارة العملاء",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(0, 20))
        
        info_label = ctk.CTkLabel(
            self,
            text="صفحة إدارة العملاء قيد التطوير...",
            font=ctk.CTkFont(size=16)
        )
        info_label.pack(expand=True)
