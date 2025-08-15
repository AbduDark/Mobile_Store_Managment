
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced Database Manager
مدير قاعدة البيانات المتقدم
"""

import sqlite3
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Union
from pathlib import Path
import threading
from contextlib import contextmanager

from src.utils.logger import get_logger

logger = get_logger(__name__)

class DatabaseManager:
    """Advanced database manager with connection pooling and transactions"""
    
    def __init__(self, db_path: str = None):
        """Initialize database manager"""
        if db_path is None:
            db_path = Path("data/database/shop.db")
        
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        self._connection_lock = threading.Lock()
        self._connections = {}
        
        self._initialize_database()
        logger.info(f"Database manager initialized with path: {self.db_path}")
    
    @contextmanager
    def get_connection(self):
        """Get database connection with proper cleanup"""
        conn = None
        try:
            with self._connection_lock:
                thread_id = threading.get_ident()
                if thread_id not in self._connections:
                    conn = sqlite3.connect(
                        str(self.db_path),
                        check_same_thread=False,
                        timeout=30.0
                    )
                    conn.row_factory = sqlite3.Row
                    conn.execute("PRAGMA foreign_keys = ON")
                    conn.execute("PRAGMA journal_mode = WAL")
                    self._connections[thread_id] = conn
                else:
                    conn = self._connections[thread_id]
            
            yield conn
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Database error: {e}")
            raise
    
    def _initialize_database(self):
        """Initialize database tables and indexes"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Products table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS products (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        brand TEXT NOT NULL,
                        model TEXT,
                        category_id INTEGER,
                        purchase_price DECIMAL(10,2) NOT NULL DEFAULT 0,
                        selling_price DECIMAL(10,2) NOT NULL DEFAULT 0,
                        stock_quantity INTEGER NOT NULL DEFAULT 0,
                        min_stock_level INTEGER DEFAULT 5,
                        max_stock_level INTEGER DEFAULT 100,
                        barcode TEXT UNIQUE,
                        sku TEXT UNIQUE,
                        description TEXT,
                        specifications JSON,
                        images JSON,
                        status TEXT DEFAULT 'active',
                        location TEXT,
                        supplier_id INTEGER,
                        warranty_period INTEGER DEFAULT 0,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (category_id) REFERENCES categories(id),
                        FOREIGN KEY (supplier_id) REFERENCES suppliers(id)
                    )
                ''')
                
                # Categories table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS categories (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL UNIQUE,
                        name_en TEXT,
                        parent_id INTEGER,
                        description TEXT,
                        icon TEXT,
                        sort_order INTEGER DEFAULT 0,
                        status TEXT DEFAULT 'active',
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (parent_id) REFERENCES categories(id)
                    )
                ''')
                
                # Customers table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS customers (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        customer_code TEXT UNIQUE,
                        name TEXT NOT NULL,
                        phone TEXT UNIQUE,
                        email TEXT,
                        address TEXT,
                        city TEXT,
                        country TEXT DEFAULT 'Saudi Arabia',
                        date_of_birth DATE,
                        gender TEXT,
                        total_purchases DECIMAL(10,2) DEFAULT 0,
                        total_orders INTEGER DEFAULT 0,
                        loyalty_points INTEGER DEFAULT 0,
                        discount_rate DECIMAL(5,2) DEFAULT 0,
                        credit_limit DECIMAL(10,2) DEFAULT 0,
                        notes TEXT,
                        status TEXT DEFAULT 'active',
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Sales table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS sales (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        invoice_number TEXT UNIQUE NOT NULL,
                        customer_id INTEGER,
                        user_id INTEGER,
                        subtotal DECIMAL(10,2) NOT NULL DEFAULT 0,
                        discount_amount DECIMAL(10,2) DEFAULT 0,
                        discount_percentage DECIMAL(5,2) DEFAULT 0,
                        tax_amount DECIMAL(10,2) DEFAULT 0,
                        total_amount DECIMAL(10,2) NOT NULL,
                        paid_amount DECIMAL(10,2) DEFAULT 0,
                        payment_method TEXT DEFAULT 'cash',
                        payment_status TEXT DEFAULT 'pending',
                        sale_status TEXT DEFAULT 'completed',
                        notes TEXT,
                        sale_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                        due_date DATE,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (customer_id) REFERENCES customers(id),
                        FOREIGN KEY (user_id) REFERENCES users(id)
                    )
                ''')
                
                # Sale items table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS sale_items (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        sale_id INTEGER NOT NULL,
                        product_id INTEGER NOT NULL,
                        quantity INTEGER NOT NULL,
                        unit_price DECIMAL(10,2) NOT NULL,
                        discount_amount DECIMAL(10,2) DEFAULT 0,
                        total_price DECIMAL(10,2) NOT NULL,
                        cost_price DECIMAL(10,2),
                        serial_numbers JSON,
                        warranty_end_date DATE,
                        notes TEXT,
                        FOREIGN KEY (sale_id) REFERENCES sales(id) ON DELETE CASCADE,
                        FOREIGN KEY (product_id) REFERENCES products(id)
                    )
                ''')
                
                # Suppliers table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS suppliers (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        contact_person TEXT,
                        phone TEXT,
                        email TEXT,
                        address TEXT,
                        city TEXT,
                        country TEXT,
                        website TEXT,
                        tax_number TEXT,
                        payment_terms TEXT,
                        notes TEXT,
                        status TEXT DEFAULT 'active',
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Expenses table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS expenses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        category TEXT NOT NULL,
                        description TEXT NOT NULL,
                        amount DECIMAL(10,2) NOT NULL,
                        payment_method TEXT DEFAULT 'cash',
                        receipt_number TEXT,
                        supplier_id INTEGER,
                        user_id INTEGER,
                        expense_date DATE DEFAULT (DATE('now')),
                        notes TEXT,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (supplier_id) REFERENCES suppliers(id),
                        FOREIGN KEY (user_id) REFERENCES users(id)
                    )
                ''')
                
                # Users table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        email TEXT UNIQUE,
                        password_hash TEXT NOT NULL,
                        full_name TEXT NOT NULL,
                        role TEXT NOT NULL DEFAULT 'employee',
                        phone TEXT,
                        is_active BOOLEAN DEFAULT 1,
                        last_login DATETIME,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Stock movements table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS stock_movements (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        product_id INTEGER NOT NULL,
                        movement_type TEXT NOT NULL,
                        quantity INTEGER NOT NULL,
                        unit_cost DECIMAL(10,2),
                        reference_type TEXT,
                        reference_id INTEGER,
                        reason TEXT,
                        user_id INTEGER,
                        movement_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                        notes TEXT,
                        FOREIGN KEY (product_id) REFERENCES products(id),
                        FOREIGN KEY (user_id) REFERENCES users(id)
                    )
                ''')
                
                # Create indexes
                self._create_indexes(cursor)
                
                # Insert default data
                self._insert_default_data(cursor)
                
                conn.commit()
                logger.info("Database initialized successfully")
                
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            raise
    
    def _create_indexes(self, cursor):
        """Create database indexes for better performance"""
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_products_barcode ON products(barcode)",
            "CREATE INDEX IF NOT EXISTS idx_products_category ON products(category_id)",
            "CREATE INDEX IF NOT EXISTS idx_products_status ON products(status)",
            "CREATE INDEX IF NOT EXISTS idx_customers_phone ON customers(phone)",
            "CREATE INDEX IF NOT EXISTS idx_customers_code ON customers(customer_code)",
            "CREATE INDEX IF NOT EXISTS idx_sales_date ON sales(sale_date)",
            "CREATE INDEX IF NOT EXISTS idx_sales_customer ON sales(customer_id)",
            "CREATE INDEX IF NOT EXISTS idx_sales_status ON sales(sale_status)",
            "CREATE INDEX IF NOT EXISTS idx_stock_movements_product ON stock_movements(product_id)",
            "CREATE INDEX IF NOT EXISTS idx_stock_movements_date ON stock_movements(movement_date)"
        ]
        
        for index in indexes:
            cursor.execute(index)
    
    def _insert_default_data(self, cursor):
        """Insert default categories and sample data"""
        try:
            # Insert default categories
            default_categories = [
                ("هواتف ذكية", "Smartphones", None, "الهواتف الذكية الحديثة", "📱", 1),
                ("هواتف مستعملة", "Used Phones", None, "الهواتف المستعملة", "♻️", 2),
                ("إكسسوارات", "Accessories", None, "إكسسوارات الهواتف", "🔌", 3),
                ("قطع غيار", "Spare Parts", None, "قطع غيار للهواتف", "🔧", 4),
                ("بطاقات شحن", "Top-up Cards", None, "بطاقات الشحن", "💳", 5)
            ]
            
            for category in default_categories:
                cursor.execute('''
                    INSERT OR IGNORE INTO categories 
                    (name, name_en, parent_id, description, icon, sort_order)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', category)
            
            # Insert sample products if none exist
            cursor.execute("SELECT COUNT(*) FROM products")
            if cursor.fetchone()[0] == 0:
                sample_products = [
                    ("iPhone 15 Pro", "Apple", "iPhone 15 Pro", 1, 4500, 5200, 10, 2, "IP15PRO001", "IP15PRO001", "أحدث هاتف من آبل مع كاميرا محسّنة", '{"storage": "256GB", "color": "أسود تيتانيوم", "condition": "جديد"}', '[]', "active", "A1", None, 12),
                    ("Galaxy S24", "Samsung", "Galaxy S24", 1, 3200, 3800, 8, 2, "GS24001", "GS24001", "هاتف سامسونج الرائد الجديد", '{"storage": "128GB", "color": "أزرق", "condition": "جديد"}', '[]', "active", "A2", None, 12),
                    ("iPhone 13", "Apple", "iPhone 13", 2, 2800, 3200, 5, 1, "IP13USED001", "IP13USED001", "آيفون 13 حالة ممتازة", '{"storage": "128GB", "color": "أبيض", "condition": "مستعمل ممتاز"}', '[]', "active", "B1", None, 6),
                    ("شاحن لاسلكي", "Anker", "PowerWave", 3, 120, 180, 15, 3, "ANK001", "ANK001", "شاحن لاسلكي سريع 15 واط", '{"power": "15W", "color": "أسود", "condition": "جديد"}', '[]', "active", "C1", None, 12),
                    ("جراب حماية", "OtterBox", "Defender", 3, 80, 150, 20, 5, "OTB001", "OTB001", "جراب حماية قوي ضد الصدمات", '{"compatibility": "iPhone 15", "color": "شفاف", "condition": "جديد"}', '[]', "active", "C2", None, 12)
                ]
                
                for product in sample_products:
                    cursor.execute('''
                        INSERT INTO products 
                        (name, brand, model, category_id, purchase_price, selling_price, 
                         stock_quantity, min_stock_level, barcode, sku, description, 
                         specifications, images, status, location, supplier_id, warranty_period)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', product)
            
            # Insert sample customers if none exist
            cursor.execute("SELECT COUNT(*) FROM customers")
            if cursor.fetchone()[0] == 0:
                sample_customers = [
                    ("CUST001", "أحمد محمد العلي", "0501234567", "ahmed@email.com", "شارع الملك فهد، الرياض", "الرياض", "السعودية", None, "male", 0, 0, 0, 0, 0, "عميل مميز", "active"),
                    ("CUST002", "فاطمة أحمد السعد", "0507654321", "fatima@email.com", "حي النزهة، جدة", "جدة", "السعودية", None, "female", 0, 0, 0, 5, 5000, "عميلة دائمة", "active"),
                    ("CUST003", "محمد علي الغامدي", "0551234567", "", "شارع الأمير محمد، الدمام", "الدمام", "السعودية", None, "male", 0, 0, 0, 0, 0, "", "active")
                ]
                
                for customer in sample_customers:
                    cursor.execute('''
                        INSERT INTO customers 
                        (customer_code, name, phone, email, address, city, country, 
                         date_of_birth, gender, total_purchases, total_orders, 
                         loyalty_points, discount_rate, credit_limit, notes, status)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', customer)
            
        except Exception as e:
            logger.error(f"Error inserting default data: {e}")
    
    def close(self):
        """Close all database connections"""
        try:
            with self._connection_lock:
                for conn in self._connections.values():
                    conn.close()
                self._connections.clear()
            logger.info("Database connections closed")
        except Exception as e:
            logger.error(f"Error closing database connections: {e}")
    
    # Query methods
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict]:
        """Execute SELECT query and return results"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                columns = [description[0] for description in cursor.description]
                rows = cursor.fetchall()
                return [dict(zip(columns, row)) for row in rows]
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            raise
    
    def execute_non_query(self, query: str, params: tuple = ()) -> int:
        """Execute INSERT/UPDATE/DELETE query"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
                return cursor.rowcount
        except Exception as e:
            logger.error(f"Error executing non-query: {e}")
            raise
    
    def get_dashboard_stats(self) -> Dict[str, Any]:
        """Get comprehensive dashboard statistics"""
        try:
            stats = {}
            
            # Today's sales
            today = datetime.now().strftime('%Y-%m-%d')
            today_sales = self.execute_query('''
                SELECT COUNT(*) as count, COALESCE(SUM(total_amount), 0) as total 
                FROM sales 
                WHERE DATE(sale_date) = ? AND sale_status = 'completed'
            ''', (today,))
            
            stats['today_sales'] = {
                'count': today_sales[0]['count'],
                'total': float(today_sales[0]['total'])
            }
            
            # This month's sales
            month_start = datetime.now().replace(day=1).strftime('%Y-%m-%d')
            month_sales = self.execute_query('''
                SELECT COUNT(*) as count, COALESCE(SUM(total_amount), 0) as total 
                FROM sales 
                WHERE DATE(sale_date) >= ? AND sale_status = 'completed'
            ''', (month_start,))
            
            stats['month_sales'] = {
                'count': month_sales[0]['count'],
                'total': float(month_sales[0]['total'])
            }
            
            # Inventory stats
            inventory_stats = self.execute_query('''
                SELECT 
                    COUNT(*) as total_products,
                    COALESCE(SUM(stock_quantity), 0) as total_stock,
                    COALESCE(SUM(stock_quantity * purchase_price), 0) as inventory_value
                FROM products 
                WHERE status = 'active'
            ''')
            
            stats['inventory'] = {
                'total_products': inventory_stats[0]['total_products'],
                'total_stock': inventory_stats[0]['total_stock'],
                'inventory_value': float(inventory_stats[0]['inventory_value'])
            }
            
            # Low stock products
            low_stock = self.execute_query('''
                SELECT COUNT(*) as count 
                FROM products 
                WHERE stock_quantity <= min_stock_level AND status = 'active'
            ''')
            
            stats['low_stock_count'] = low_stock[0]['count']
            
            # Customer stats
            customer_stats = self.execute_query('''
                SELECT 
                    COUNT(*) as total_customers,
                    COALESCE(AVG(total_purchases), 0) as avg_purchase
                FROM customers 
                WHERE status = 'active'
            ''')
            
            stats['customers'] = {
                'total_customers': customer_stats[0]['total_customers'],
                'avg_purchase': float(customer_stats[0]['avg_purchase'])
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting dashboard stats: {e}")
            return {}
