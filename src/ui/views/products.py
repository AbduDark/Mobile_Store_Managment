
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Products View
عرض المنتجات
"""

import customtkinter as ctk
from tkinter import messagebox, filedialog
from tkinter import ttk
import threading

from src.utils.logger import get_logger

logger = get_logger(__name__)

class ProductsView(ctk.CTkFrame):
    """Products management view"""
    
    def __init__(self, parent, db_manager, theme_manager):
        super().__init__(parent, fg_color="transparent")
        
        self.db_manager = db_manager
        self.theme_manager = theme_manager
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self.products_data = []
        self.categories_data = []
        
        self._setup_ui()
        self._load_data()
    
    def _setup_ui(self):
        """Setup products view UI"""
        colors = self.theme_manager.get_colors()
        
        # Header section
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Title
        title_label = ctk.CTkLabel(
            header_frame,
            text="📱 إدارة المنتجات",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=colors["accent"]
        )
        title_label.grid(row=0, column=0, padx=(0, 20))
        
        # Search and filter section
        search_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        search_frame.grid(row=0, column=1, sticky="ew")
        search_frame.grid_columnconfigure(1, weight=1)
        
        # Search entry
        self.search_var = ctk.StringVar()
        self.search_var.trace("w", self._on_search_change)
        
        search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="البحث في المنتجات...",
            textvariable=self.search_var,
            width=250,
            font=ctk.CTkFont(size=12)
        )
        search_entry.grid(row=0, column=0, padx=(0, 10))
        
        # Category filter
        self.category_var = ctk.StringVar(value="جميع الفئات")
        category_combo = ctk.CTkComboBox(
            search_frame,
            variable=self.category_var,
            values=["جميع الفئات"],
            width=150,
            command=self._on_category_change
        )
        category_combo.grid(row=0, column=1, padx=(0, 10))
        
        # Add new product button
        add_btn = ctk.CTkButton(
            header_frame,
            text="+ إضافة منتج",
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self._show_add_product_dialog,
            width=120,
            height=32
        )
        add_btn.grid(row=0, column=2, padx=(20, 0))
        
        # Products table section
        table_frame = ctk.CTkFrame(self, corner_radius=10)
        table_frame.grid(row=1, column=0, sticky="nsew")
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)
        
        # Create treeview for products
        self._create_products_table(table_frame)
        
        # Actions section
        actions_frame = ctk.CTkFrame(self, fg_color="transparent")
        actions_frame.grid(row=2, column=0, sticky="ew", pady=(20, 0))
        
        # Action buttons
        edit_btn = ctk.CTkButton(
            actions_frame,
            text="تعديل",
            command=self._edit_selected_product,
            width=100
        )
        edit_btn.pack(side="left", padx=(0, 10))
        
        delete_btn = ctk.CTkButton(
            actions_frame,
            text="حذف",
            command=self._delete_selected_product,
            fg_color=colors["danger"],
            hover_color="#c0392b",
            width=100
        )
        delete_btn.pack(side="left", padx=(0, 10))
        
        refresh_btn = ctk.CTkButton(
            actions_frame,
            text="تحديث",
            command=self._load_data,
            width=100
        )
        refresh_btn.pack(side="right")
    
    def _create_products_table(self, parent):
        """Create products table with treeview"""
        # Create treeview
        columns = ("id", "name", "brand", "category", "price", "stock", "status")
        
        self.products_tree = ttk.Treeview(
            parent,
            columns=columns,
            show="headings",
            height=15
        )
        
        # Configure columns
        self.products_tree.heading("id", text="الرقم")
        self.products_tree.heading("name", text="اسم المنتج")
        self.products_tree.heading("brand", text="العلامة التجارية")
        self.products_tree.heading("category", text="الفئة")
        self.products_tree.heading("price", text="السعر")
        self.products_tree.heading("stock", text="المخزون")
        self.products_tree.heading("status", text="الحالة")
        
        # Configure column widths
        self.products_tree.column("id", width=60, anchor="center")
        self.products_tree.column("name", width=200, anchor="w")
        self.products_tree.column("brand", width=120, anchor="w")
        self.products_tree.column("category", width=120, anchor="w")
        self.products_tree.column("price", width=80, anchor="center")
        self.products_tree.column("stock", width=80, anchor="center")
        self.products_tree.column("status", width=80, anchor="center")
        
        # Add scrollbars
        v_scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.products_tree.yview)
        h_scrollbar = ttk.Scrollbar(parent, orient="horizontal", command=self.products_tree.xview)
        
        self.products_tree.configure(yscrollcommand=v_scrollbar.set)
        self.products_tree.configure(xscrollcommand=h_scrollbar.set)
        
        # Grid layout
        self.products_tree.grid(row=0, column=0, sticky="nsew", padx=(10, 0), pady=10)
        v_scrollbar.grid(row=0, column=1, sticky="ns", pady=10)
        h_scrollbar.grid(row=1, column=0, sticky="ew", padx=(10, 0))
        
        # Bind double click event
        self.products_tree.bind("<Double-1>", self._on_product_double_click)
    
    def _load_data(self):
        """Load products and categories data"""
        def load_products():
            try:
                # Load products
                products = self.db_manager.execute_query("""
                    SELECT p.id, p.name, p.brand, c.name as category_name,
                           p.selling_price, p.stock_quantity, p.status
                    FROM products p
                    LEFT JOIN categories c ON p.category_id = c.id
                    WHERE p.status = 'active'
                    ORDER BY p.name
                """)
                
                # Load categories
                categories = self.db_manager.execute_query("""
                    SELECT id, name FROM categories 
                    WHERE status = 'active' 
                    ORDER BY sort_order, name
                """)
                
                # Update UI in main thread
                self.after(0, lambda: self._update_products_display(products, categories))
                
            except Exception as e:
                logger.error(f"Error loading products data: {e}")
                self.after(0, lambda: messagebox.showerror("خطأ", f"حدث خطأ في تحميل البيانات: {e}"))
        
        # Load in background thread
        threading.Thread(target=load_products, daemon=True).start()
    
    def _update_products_display(self, products, categories):
        """Update products display"""
        try:
            # Store data
            self.products_data = products
            self.categories_data = categories
            
            # Update products table
            # Clear existing items
            for item in self.products_tree.get_children():
                self.products_tree.delete(item)
            
            # Insert products
            for product in products:
                status_text = "نشط" if product['status'] == 'active' else "غير نشط"
                
                self.products_tree.insert("", "end", values=(
                    product['id'],
                    product['name'],
                    product['brand'],
                    product['category_name'] or 'غير محدد',
                    f"{product['selling_price']:.2f}",
                    product['stock_quantity'],
                    status_text
                ))
            
            # Update category filter
            category_names = ["جميع الفئات"] + [cat['name'] for cat in categories]
            # Note: In a real implementation, you'd update the combobox values here
            
        except Exception as e:
            logger.error(f"Error updating products display: {e}")
    
    def _on_search_change(self, *args):
        """Handle search input change"""
        # Implementation for search filtering
        pass
    
    def _on_category_change(self, value):
        """Handle category filter change"""
        # Implementation for category filtering
        pass
    
    def _show_add_product_dialog(self):
        """Show add new product dialog"""
        # Implementation for add product dialog
        messagebox.showinfo("قريباً", "نافذة إضافة المنتج قيد التطوير")
    
    def _edit_selected_product(self):
        """Edit selected product"""
        selection = self.products_tree.selection()
        if not selection:
            messagebox.showwarning("تحذير", "يرجى اختيار منتج للتعديل")
            return
        
        # Implementation for edit product dialog
        messagebox.showinfo("قريباً", "نافذة تعديل المنتج قيد التطوير")
    
    def _delete_selected_product(self):
        """Delete selected product"""
        selection = self.products_tree.selection()
        if not selection:
            messagebox.showwarning("تحذير", "يرجى اختيار منتج للحذف")
            return
        
        if messagebox.askyesno("تأكيد الحذف", "هل تريد حذف المنتج المحدد؟"):
            # Implementation for delete product
            messagebox.showinfo("قريباً", "حذف المنتج قيد التطوير")
    
    def _on_product_double_click(self, event):
        """Handle product double click"""
        self._edit_selected_product()
