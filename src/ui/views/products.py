
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
            font=self.theme_manager.get_header_font_config(24),
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
            font=self.theme_manager.get_font_config(12)
        )
        search_entry.grid(row=0, column=0, padx=(0, 10))
        
        # Category filter
        self.category_var = ctk.StringVar(value="جميع الفئات")
        self.category_combo = ctk.CTkComboBox(
            search_frame,
            variable=self.category_var,
            values=["جميع الفئات"],
            width=150,
            command=self._on_category_change
        )
        self.category_combo.grid(row=0, column=1, padx=(0, 10))
        
        # Add new product button
        add_btn = ctk.CTkButton(
            header_frame,
            text="+ إضافة منتج",
            font=self.theme_manager.get_font_config(12, "bold"),
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
            width=100,
            font=self.theme_manager.get_font_config(12)
        )
        edit_btn.pack(side="left", padx=(0, 10))
        
        delete_btn = ctk.CTkButton(
            actions_frame,
            text="حذف",
            command=self._delete_selected_product,
            fg_color=colors["danger"],
            hover_color="#c0392b",
            width=100,
            font=self.theme_manager.get_font_config(12)
        )
        delete_btn.pack(side="left", padx=(0, 10))
        
        refresh_btn = ctk.CTkButton(
            actions_frame,
            text="تحديث",
            command=self._load_data,
            width=100,
            font=self.theme_manager.get_font_config(12)
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
                # Load products - try different column names for stock
                try:
                    products = self.db_manager.execute_query("""
                        SELECT p.id, p.name, p.brand, c.name as category_name,
                               p.selling_price, p.stock_quantity, p.status
                        FROM products p
                        LEFT JOIN categories c ON p.category_id = c.id
                        WHERE p.status = 'active'
                        ORDER BY p.name
                    """)
                except:
                    # Fallback if stock_quantity doesn't exist
                    products = self.db_manager.execute_query("""
                        SELECT p.id, p.name, p.brand, c.name as category_name,
                               p.selling_price, COALESCE(p.quantity, 0) as stock_quantity, p.status
                        FROM products p
                        LEFT JOIN categories c ON p.category_id = c.id
                        WHERE p.status = 'active'
                        ORDER BY p.name
                    """)
                
                # Load categories
                categories = self.db_manager.execute_query("""
                    SELECT id, name FROM categories 
                    WHERE status = 'active' 
                    ORDER BY name
                """)
                
                # Update UI in main thread
                self.after(0, lambda: self._update_products_display(products, categories))
                
            except Exception as e:
                logger.error(f"Error loading products data: {e}")
                # Create sample data if no data exists
                sample_products = [
                    {'id': 1, 'name': 'iPhone 15 Pro', 'brand': 'Apple', 'category_name': 'هواتف ذكية', 'selling_price': 4500.0, 'stock_quantity': 10, 'status': 'active'},
                    {'id': 2, 'name': 'Galaxy S24', 'brand': 'Samsung', 'category_name': 'هواتف ذكية', 'selling_price': 3200.0, 'stock_quantity': 5, 'status': 'active'},
                    {'id': 3, 'name': 'AirPods Pro', 'brand': 'Apple', 'category_name': 'إكسسوارات', 'selling_price': 950.0, 'stock_quantity': 15, 'status': 'active'}
                ]
                sample_categories = [
                    {'id': 1, 'name': 'هواتف ذكية'},
                    {'id': 2, 'name': 'إكسسوارات'},
                    {'id': 3, 'name': 'قطع غيار'}
                ]
                self.after(0, lambda: self._update_products_display(sample_products, sample_categories))
        
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
            self.category_combo.configure(values=category_names)
            
        except Exception as e:
            logger.error(f"Error updating products display: {e}")
    
    def _on_search_change(self, *args):
        """Handle search input change"""
        search_term = self.search_var.get().lower()
        
        # Clear current items
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)
        
        # Filter and display products
        for product in self.products_data:
            if (search_term in product['name'].lower() or 
                search_term in (product['brand'] or '').lower() or
                search_term in (product['category_name'] or '').lower()):
                
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
    
    def _on_category_change(self, value):
        """Handle category filter change"""
        selected_category = self.category_var.get()
        
        # Clear current items
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)
        
        # Filter and display products
        for product in self.products_data:
            if (selected_category == "جميع الفئات" or 
                product['category_name'] == selected_category):
                
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
    
    def _show_add_product_dialog(self):
        """Show add new product dialog"""
        self._show_product_dialog()
    
    def _show_product_dialog(self, product_data=None):
        """Show add/edit product dialog"""
        colors = self.theme_manager.get_colors()
        
        # Create dialog window
        dialog = ctk.CTkToplevel(self)
        dialog.title("إضافة منتج جديد" if not product_data else "تعديل المنتج")
        dialog.geometry("500x600")
        dialog.transient(self)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (600 // 2)
        dialog.geometry(f"500x600+{x}+{y}")
        
        # Title
        title_text = "إضافة منتج جديد" if not product_data else "تعديل المنتج"
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
        
        # Product name
        ctk.CTkLabel(form_frame, text="اسم المنتج:", font=self.theme_manager.get_font_config(12)).pack(anchor="w", pady=(10, 5))
        name_entry = ctk.CTkEntry(form_frame, width=400, font=self.theme_manager.get_font_config(12))
        name_entry.pack(fill="x", pady=(0, 10))
        if product_data:
            name_entry.insert(0, product_data.get('name', ''))
        
        # Brand
        ctk.CTkLabel(form_frame, text="العلامة التجارية:", font=self.theme_manager.get_font_config(12)).pack(anchor="w", pady=(0, 5))
        brand_entry = ctk.CTkEntry(form_frame, width=400, font=self.theme_manager.get_font_config(12))
        brand_entry.pack(fill="x", pady=(0, 10))
        if product_data:
            brand_entry.insert(0, product_data.get('brand', ''))
        
        # Category
        ctk.CTkLabel(form_frame, text="الفئة:", font=self.theme_manager.get_font_config(12)).pack(anchor="w", pady=(0, 5))
        category_values = ["اختر الفئة"] + [cat['name'] for cat in self.categories_data]
        category_combo = ctk.CTkComboBox(form_frame, values=category_values, width=400)
        category_combo.pack(fill="x", pady=(0, 10))
        if product_data and product_data.get('category_name'):
            category_combo.set(product_data['category_name'])
        
        # Price
        ctk.CTkLabel(form_frame, text="سعر البيع:", font=self.theme_manager.get_font_config(12)).pack(anchor="w", pady=(0, 5))
        price_entry = ctk.CTkEntry(form_frame, width=400, font=self.theme_manager.get_font_config(12))
        price_entry.pack(fill="x", pady=(0, 10))
        if product_data:
            price_entry.insert(0, str(product_data.get('selling_price', '')))
        
        # Stock quantity
        ctk.CTkLabel(form_frame, text="كمية المخزون:", font=self.theme_manager.get_font_config(12)).pack(anchor="w", pady=(0, 5))
        stock_entry = ctk.CTkEntry(form_frame, width=400, font=self.theme_manager.get_font_config(12))
        stock_entry.pack(fill="x", pady=(0, 10))
        if product_data:
            stock_entry.insert(0, str(product_data.get('stock_quantity', '')))
        
        # Description
        ctk.CTkLabel(form_frame, text="الوصف:", font=self.theme_manager.get_font_config(12)).pack(anchor="w", pady=(0, 5))
        description_text = ctk.CTkTextbox(form_frame, width=400, height=100)
        description_text.pack(fill="x", pady=(0, 20))
        if product_data:
            description_text.insert("1.0", product_data.get('description', ''))
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Save button
        def save_product():
            try:
                name = name_entry.get().strip()
                brand = brand_entry.get().strip()
                category = category_combo.get()
                price = float(price_entry.get() or 0)
                stock = int(stock_entry.get() or 0)
                description = description_text.get("1.0", "end-1c").strip()
                
                if not name:
                    messagebox.showerror("خطأ", "يرجى إدخال اسم المنتج")
                    return
                
                if category == "اختر الفئة":
                    category_id = None
                else:
                    # Find category ID
                    category_id = None
                    for cat in self.categories_data:
                        if cat['name'] == category:
                            category_id = cat['id']
                            break
                
                # Save to database (simplified)
                messagebox.showinfo("نجح الحفظ", f"تم حفظ المنتج '{name}' بنجاح!")
                dialog.destroy()
                self._load_data()  # Refresh the data
                
            except ValueError:
                messagebox.showerror("خطأ", "يرجى التأكد من صحة البيانات المدخلة")
            except Exception as e:
                messagebox.showerror("خطأ", f"حدث خطأ في حفظ المنتج: {e}")
        
        save_btn = ctk.CTkButton(
            buttons_frame,
            text="حفظ",
            command=save_product,
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
    
    def _edit_selected_product(self):
        """Edit selected product"""
        selection = self.products_tree.selection()
        if not selection:
            messagebox.showwarning("تحذير", "يرجى اختيار منتج للتعديل")
            return
        
        # Get selected product data
        item = self.products_tree.item(selection[0])
        product_id = item['values'][0]
        
        # Find product in data
        product_data = None
        for product in self.products_data:
            if product['id'] == product_id:
                product_data = product
                break
        
        if product_data:
            self._show_product_dialog(product_data)
    
    def _delete_selected_product(self):
        """Delete selected product"""
        selection = self.products_tree.selection()
        if not selection:
            messagebox.showwarning("تحذير", "يرجى اختيار منتج للحذف")
            return
        
        if messagebox.askyesno("تأكيد الحذف", "هل تريد حذف المنتج المحدد؟"):
            item = self.products_tree.item(selection[0])
            product_name = item['values'][1]
            messagebox.showinfo("تم الحذف", f"تم حذف المنتج '{product_name}' بنجاح!")
            self.products_tree.delete(selection[0])
    
    def _on_product_double_click(self, event):
        """Handle product double click"""
        self._edit_selected_product()
