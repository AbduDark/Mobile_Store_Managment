#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Database Manager for Mobile Shop Management System
إدارة قاعدة البيانات لنظام إدارة محل الموبايلات
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Any, Optional

class DatabaseManager:
    """Database manager class for handling all database operations"""
    
    def __init__(self, db_name: str = "mobile_shop.db"):
        """Initialize database manager"""
        self.db_name = db_name
        self.db_path = os.path.join(os.path.dirname(__file__), "..", self.db_name)
        self.create_tables()
    
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        return conn
    
    def create_tables(self):
        """Create all necessary database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Products table - جدول المنتجات
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    brand TEXT NOT NULL,
                    model TEXT,
                    category TEXT NOT NULL,
                    purchase_price REAL NOT NULL DEFAULT 0,
                    selling_price REAL NOT NULL DEFAULT 0,
                    quantity INTEGER NOT NULL DEFAULT 0,
                    min_quantity INTEGER DEFAULT 5,
                    barcode TEXT UNIQUE,
                    description TEXT,
                    color TEXT,
                    storage TEXT,
                    condition TEXT DEFAULT 'new',
                    image_path TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Customers table - جدول العملاء
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS customers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    phone TEXT UNIQUE,
                    email TEXT,
                    address TEXT,
                    total_purchases REAL DEFAULT 0,
                    loyalty_points INTEGER DEFAULT 0,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Sales table - جدول المبيعات
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sales (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_id INTEGER,
                    total_amount REAL NOT NULL,
                    discount REAL DEFAULT 0,
                    tax REAL DEFAULT 0,
                    payment_method TEXT DEFAULT 'cash',
                    payment_status TEXT DEFAULT 'paid',
                    notes TEXT,
                    sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (customer_id) REFERENCES customers (id)
                )
            ''')
            
            # Sale items table - جدول عناصر المبيعات
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sale_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sale_id INTEGER NOT NULL,
                    product_id INTEGER NOT NULL,
                    quantity INTEGER NOT NULL,
                    unit_price REAL NOT NULL,
                    total_price REAL NOT NULL,
                    FOREIGN KEY (sale_id) REFERENCES sales (id) ON DELETE CASCADE,
                    FOREIGN KEY (product_id) REFERENCES products (id)
                )
            ''')
            
            # Services/Repairs table - جدول الصيانة
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS services (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_id INTEGER,
                    device_type TEXT NOT NULL,
                    device_model TEXT,
                    problem_description TEXT NOT NULL,
                    estimated_cost REAL,
                    actual_cost REAL,
                    status TEXT DEFAULT 'received',
                    technician TEXT,
                    received_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    completed_date TIMESTAMP,
                    notes TEXT,
                    FOREIGN KEY (customer_id) REFERENCES customers (id)
                )
            ''')
            
            # Expenses table - جدول المصروفات
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    description TEXT NOT NULL,
                    amount REAL NOT NULL,
                    category TEXT NOT NULL,
                    expense_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    notes TEXT
                )
            ''')
            
            # Suppliers table - جدول الموردين
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS suppliers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    phone TEXT,
                    email TEXT,
                    address TEXT,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Stock movements table - جدول حركة المخزون
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS stock_movements (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_id INTEGER NOT NULL,
                    movement_type TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    reference_id INTEGER,
                    reference_type TEXT,
                    notes TEXT,
                    movement_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (product_id) REFERENCES products (id)
                )
            ''')
            
            # Create indexes for better performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_products_barcode ON products(barcode)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_customers_phone ON customers(phone)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_sales_date ON sales(sale_date)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_stock_movements_product ON stock_movements(product_id)')
            
            conn.commit()
            print("تم إنشاء جداول قاعدة البيانات بنجاح")
            
        except sqlite3.Error as e:
            print(f"خطأ في إنشاء جداول قاعدة البيانات: {e}")
            conn.rollback()
        finally:
            conn.close()
    
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict]:
        """Execute a SELECT query and return results"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            columns = [description[0] for description in cursor.description]
            rows = cursor.fetchall()
            return [dict(zip(columns, row)) for row in rows]
        finally:
            conn.close()
    
    def execute_non_query(self, query: str, params: tuple = ()) -> int:
        """Execute INSERT, UPDATE, DELETE queries and return affected rows"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount
        except sqlite3.Error as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def get_last_insert_id(self, query: str, params: tuple = ()) -> int:
        """Execute INSERT query and return the last inserted ID"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    # Product management methods
    def add_product(self, product_data: Dict[str, Any]) -> int:
        """Add a new product to the database"""
        query = '''
            INSERT INTO products (name, brand, model, category, purchase_price, 
                                selling_price, quantity, min_quantity, barcode, 
                                description, color, storage, condition, image_path)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        params = (
            product_data.get('name'),
            product_data.get('brand'),
            product_data.get('model', ''),
            product_data.get('category'),
            product_data.get('purchase_price', 0),
            product_data.get('selling_price', 0),
            product_data.get('quantity', 0),
            product_data.get('min_quantity', 5),
            product_data.get('barcode', ''),
            product_data.get('description', ''),
            product_data.get('color', ''),
            product_data.get('storage', ''),
            product_data.get('condition', 'new'),
            product_data.get('image_path', '')
        )
        return self.get_last_insert_id(query, params)
    
    def get_all_products(self) -> List[Dict]:
        """Get all products from the database"""
        query = "SELECT * FROM products ORDER BY name"
        return self.execute_query(query)
    
    def get_product_by_id(self, product_id: int) -> Optional[Dict]:
        """Get a product by its ID"""
        query = "SELECT * FROM products WHERE id = ?"
        results = self.execute_query(query, (product_id,))
        return results[0] if results else None
    
    def update_product(self, product_id: int, product_data: Dict[str, Any]) -> int:
        """Update a product in the database"""
        query = '''
            UPDATE products SET name=?, brand=?, model=?, category=?, 
                              purchase_price=?, selling_price=?, quantity=?, 
                              min_quantity=?, barcode=?, description=?, 
                              color=?, storage=?, condition=?, image_path=?,
                              updated_at=CURRENT_TIMESTAMP
            WHERE id=?
        '''
        params = (
            product_data.get('name'),
            product_data.get('brand'),
            product_data.get('model', ''),
            product_data.get('category'),
            product_data.get('purchase_price', 0),
            product_data.get('selling_price', 0),
            product_data.get('quantity', 0),
            product_data.get('min_quantity', 5),
            product_data.get('barcode', ''),
            product_data.get('description', ''),
            product_data.get('color', ''),
            product_data.get('storage', ''),
            product_data.get('condition', 'new'),
            product_data.get('image_path', ''),
            product_id
        )
        return self.execute_non_query(query, params)
    
    def delete_product(self, product_id: int) -> int:
        """Delete a product from the database"""
        query = "DELETE FROM products WHERE id = ?"
        return self.execute_non_query(query, (product_id,))
    
    def get_low_stock_products(self) -> List[Dict]:
        """Get products with low stock"""
        query = "SELECT * FROM products WHERE quantity <= min_quantity ORDER BY quantity"
        return self.execute_query(query)
    
    # Customer management methods
    def add_customer(self, customer_data: Dict[str, Any]) -> int:
        """Add a new customer to the database"""
        query = '''
            INSERT INTO customers (name, phone, email, address, notes)
            VALUES (?, ?, ?, ?, ?)
        '''
        params = (
            customer_data.get('name'),
            customer_data.get('phone', ''),
            customer_data.get('email', ''),
            customer_data.get('address', ''),
            customer_data.get('notes', '')
        )
        return self.get_last_insert_id(query, params)
    
    def get_all_customers(self) -> List[Dict]:
        """Get all customers from the database"""
        query = "SELECT * FROM customers ORDER BY name"
        return self.execute_query(query)
    
    def get_customer_by_phone(self, phone: str) -> Optional[Dict]:
        """Get a customer by phone number"""
        query = "SELECT * FROM customers WHERE phone = ?"
        results = self.execute_query(query, (phone,))
        return results[0] if results else None
    
    # Sales management methods
    def create_sale(self, sale_data: Dict[str, Any], items: List[Dict[str, Any]]) -> int:
        """Create a new sale with items"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            
            # Insert sale record
            sale_query = '''
                INSERT INTO sales (customer_id, total_amount, discount, tax, 
                                 payment_method, payment_status, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            '''
            sale_params = (
                sale_data.get('customer_id'),
                sale_data.get('total_amount', 0),
                sale_data.get('discount', 0),
                sale_data.get('tax', 0),
                sale_data.get('payment_method', 'cash'),
                sale_data.get('payment_status', 'paid'),
                sale_data.get('notes', '')
            )
            cursor.execute(sale_query, sale_params)
            sale_id = cursor.lastrowid
            
            # Insert sale items and update product quantities
            for item in items:
                # Insert sale item
                item_query = '''
                    INSERT INTO sale_items (sale_id, product_id, quantity, unit_price, total_price)
                    VALUES (?, ?, ?, ?, ?)
                '''
                item_params = (
                    sale_id,
                    item['product_id'],
                    item['quantity'],
                    item['unit_price'],
                    item['total_price']
                )
                cursor.execute(item_query, item_params)
                
                # Update product quantity
                update_qty_query = '''
                    UPDATE products SET quantity = quantity - ? WHERE id = ?
                '''
                cursor.execute(update_qty_query, (item['quantity'], item['product_id']))
                
                # Add stock movement record
                stock_query = '''
                    INSERT INTO stock_movements (product_id, movement_type, quantity, 
                                               reference_id, reference_type, notes)
                    VALUES (?, 'out', ?, ?, 'sale', 'بيع')
                '''
                cursor.execute(stock_query, (item['product_id'], item['quantity'], sale_id))
            
            # Update customer total purchases if customer exists
            if sale_data.get('customer_id'):
                update_customer_query = '''
                    UPDATE customers SET total_purchases = total_purchases + ?,
                                       loyalty_points = loyalty_points + ?
                    WHERE id = ?
                '''
                loyalty_points = int(sale_data.get('total_amount', 0) / 10)  # 1 point per 10 currency units
                cursor.execute(update_customer_query, (
                    sale_data.get('total_amount', 0),
                    loyalty_points,
                    sale_data.get('customer_id')
                ))
            
            conn.commit()
            return sale_id
            
        except sqlite3.Error as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def get_sales_report(self, start_date: str = None, end_date: str = None) -> List[Dict]:
        """Get sales report for a date range"""
        query = '''
            SELECT s.*, c.name as customer_name 
            FROM sales s 
            LEFT JOIN customers c ON s.customer_id = c.id
        '''
        params = []
        
        if start_date and end_date:
            query += " WHERE DATE(s.sale_date) BETWEEN ? AND ?"
            params = [start_date, end_date]
        elif start_date:
            query += " WHERE DATE(s.sale_date) >= ?"
            params = [start_date]
        elif end_date:
            query += " WHERE DATE(s.sale_date) <= ?"
            params = [end_date]
        
        query += " ORDER BY s.sale_date DESC"
        return self.execute_query(query, tuple(params))
    
    def get_dashboard_stats(self) -> Dict[str, Any]:
        """Get dashboard statistics"""
        stats = {}
        
        # Today's sales
        today = datetime.now().strftime('%Y-%m-%d')
        today_sales = self.execute_query(
            "SELECT COUNT(*) as count, COALESCE(SUM(total_amount), 0) as total FROM sales WHERE DATE(sale_date) = ?",
            (today,)
        )
        stats['today_sales_count'] = today_sales[0]['count']
        stats['today_sales_total'] = today_sales[0]['total']
        
        # This month's sales
        month_start = datetime.now().replace(day=1).strftime('%Y-%m-%d')
        month_sales = self.execute_query(
            "SELECT COUNT(*) as count, COALESCE(SUM(total_amount), 0) as total FROM sales WHERE DATE(sale_date) >= ?",
            (month_start,)
        )
        stats['month_sales_count'] = month_sales[0]['count']
        stats['month_sales_total'] = month_sales[0]['total']
        
        # Total products
        product_stats = self.execute_query(
            "SELECT COUNT(*) as total_products, COALESCE(SUM(quantity), 0) as total_quantity FROM products"
        )
        stats['total_products'] = product_stats[0]['total_products']
        stats['total_quantity'] = product_stats[0]['total_quantity']
        
        # Low stock count
        low_stock = self.execute_query(
            "SELECT COUNT(*) as count FROM products WHERE quantity <= min_quantity"
        )
        stats['low_stock_count'] = low_stock[0]['count']
        
        # Total customers
        customer_stats = self.execute_query("SELECT COUNT(*) as count FROM customers")
        stats['total_customers'] = customer_stats[0]['count']
        
        return stats
