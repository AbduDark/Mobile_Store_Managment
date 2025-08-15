#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Database Manager
مدير قاعدة البيانات
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime, date
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict
import uuid

from src.utils.logger import get_logger

logger = get_logger(__name__)

@dataclass
class Product:
    """Product data model"""
    id: Optional[int] = None
    name: str = ""
    brand: str = ""
    model: str = ""
    price: float = 0.0
    cost: float = 0.0
    stock_quantity: int = 0
    min_stock: int = 0
    category: str = ""
    description: str = ""
    barcode: str = ""
    image_path: str = ""
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

@dataclass
class Customer:
    """Customer data model"""
    id: Optional[int] = None
    name: str = ""
    phone: str = ""
    email: str = ""
    address: str = ""
    notes: str = ""
    total_purchases: float = 0.0
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

@dataclass
class Sale:
    """Sale data model"""
    id: Optional[int] = None
    customer_id: Optional[int] = None
    customer_name: str = ""
    total_amount: float = 0.0
    discount: float = 0.0
    tax: float = 0.0
    final_amount: float = 0.0
    payment_method: str = "cash"
    notes: str = ""
    created_at: Optional[str] = None

@dataclass
class SaleItem:
    """Sale item data model"""
    id: Optional[int] = None
    sale_id: int = 0
    product_id: int = 0
    product_name: str = ""
    quantity: int = 0
    unit_price: float = 0.0
    total_price: float = 0.0

class DatabaseManager:
    """Database manager for SQLite operations"""

    def __init__(self, db_path: str = "data/database/shop.db"):
        """Initialize database manager"""
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        self._init_database()
        logger.info(f"Database initialized: {self.db_path}")

    def _init_database(self):
        """Initialize database tables"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Products table
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    brand TEXT,
                    model TEXT,
                    price REAL NOT NULL DEFAULT 0,
                    cost REAL NOT NULL DEFAULT 0,
                    stock_quantity INTEGER NOT NULL DEFAULT 0,
                    min_stock INTEGER DEFAULT 0,
                    category TEXT,
                    description TEXT,
                    barcode TEXT UNIQUE,
                    image_path TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
                """)

                # Customers table
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS customers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    phone TEXT,
                    email TEXT,
                    address TEXT,
                    notes TEXT,
                    total_purchases REAL DEFAULT 0,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
                """)

                # Sales table
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS sales (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_id INTEGER,
                    customer_name TEXT,
                    total_amount REAL NOT NULL DEFAULT 0,
                    discount REAL DEFAULT 0,
                    tax REAL DEFAULT 0,
                    final_amount REAL NOT NULL DEFAULT 0,
                    payment_method TEXT DEFAULT 'cash',
                    notes TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (customer_id) REFERENCES customers (id)
                )
                """)

                # Sale items table
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS sale_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sale_id INTEGER NOT NULL,
                    product_id INTEGER NOT NULL,
                    product_name TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    unit_price REAL NOT NULL,
                    total_price REAL NOT NULL,
                    FOREIGN KEY (sale_id) REFERENCES sales (id),
                    FOREIGN KEY (product_id) REFERENCES products (id)
                )
                """)

                conn.commit()
                logger.info("Database tables created successfully")

        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            raise

    # Product operations
    def add_product(self, product: Product) -> bool:
        """Add new product"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cursor.execute("""
                INSERT INTO products (name, brand, model, price, cost, stock_quantity, 
                                    min_stock, category, description, barcode, image_path)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (product.name, product.brand, product.model, product.price,
                      product.cost, product.stock_quantity, product.min_stock,
                      product.category, product.description, product.barcode,
                      product.image_path))

                conn.commit()
                logger.info(f"Product added: {product.name}")
                return True

        except sqlite3.IntegrityError as e:
            logger.error(f"Product with barcode {product.barcode} already exists")
            return False
        except Exception as e:
            logger.error(f"Error adding product: {e}")
            return False

    def get_all_products(self) -> List[Product]:
        """Get all products"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()

                cursor.execute("SELECT * FROM products ORDER BY name")
                rows = cursor.fetchall()

                return [Product(**dict(row)) for row in rows]

        except Exception as e:
            logger.error(f"Error getting products: {e}")
            return []

    def update_product(self, product: Product) -> bool:
        """Update product"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cursor.execute("""
                UPDATE products SET name=?, brand=?, model=?, price=?, cost=?,
                                  stock_quantity=?, min_stock=?, category=?,
                                  description=?, barcode=?, image_path=?,
                                  updated_at=CURRENT_TIMESTAMP
                WHERE id=?
                """, (product.name, product.brand, product.model, product.price,
                      product.cost, product.stock_quantity, product.min_stock,
                      product.category, product.description, product.barcode,
                      product.image_path, product.id))

                conn.commit()
                logger.info(f"Product updated: {product.name}")
                return cursor.rowcount > 0

        except Exception as e:
            logger.error(f"Error updating product: {e}")
            return False

    def delete_product(self, product_id: int) -> bool:
        """Delete product"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cursor.execute("DELETE FROM products WHERE id=?", (product_id,))
                conn.commit()

                logger.info(f"Product deleted: {product_id}")
                return cursor.rowcount > 0

        except Exception as e:
            logger.error(f"Error deleting product: {e}")
            return False

    def search_products(self, search_term: str) -> List[Product]:
        """Search products by name, brand, or model"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()

                search_pattern = f"%{search_term}%"
                cursor.execute("""
                SELECT * FROM products 
                WHERE name LIKE ? OR brand LIKE ? OR model LIKE ?
                ORDER BY name
                """, (search_pattern, search_pattern, search_pattern))

                rows = cursor.fetchall()
                return [Product(**dict(row)) for row in rows]

        except Exception as e:
            logger.error(f"Error searching products: {e}")
            return []

    # Customer operations
    def add_customer(self, customer: Customer) -> bool:
        """Add new customer"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cursor.execute("""
                INSERT INTO customers (name, phone, email, address, notes)
                VALUES (?, ?, ?, ?, ?)
                """, (customer.name, customer.phone, customer.email,
                      customer.address, customer.notes))

                conn.commit()
                logger.info(f"Customer added: {customer.name}")
                return True

        except Exception as e:
            logger.error(f"Error adding customer: {e}")
            return False

    def get_all_customers(self) -> List[Customer]:
        """Get all customers"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()

                cursor.execute("SELECT * FROM customers ORDER BY name")
                rows = cursor.fetchall()

                return [Customer(**dict(row)) for row in rows]

        except Exception as e:
            logger.error(f"Error getting customers: {e}")
            return []

    # Sales operations
    def create_sale(self, sale: Sale, items: List[SaleItem]) -> Optional[int]:
        """Create new sale with items"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Insert sale
                cursor.execute("""
                INSERT INTO sales (customer_id, customer_name, total_amount,
                                 discount, tax, final_amount, payment_method, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (sale.customer_id, sale.customer_name, sale.total_amount,
                      sale.discount, sale.tax, sale.final_amount,
                      sale.payment_method, sale.notes))

                sale_id = cursor.lastrowid

                # Insert sale items and update stock
                for item in items:
                    cursor.execute("""
                    INSERT INTO sale_items (sale_id, product_id, product_name,
                                          quantity, unit_price, total_price)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """, (sale_id, item.product_id, item.product_name,
                          item.quantity, item.unit_price, item.total_price))

                    # Update product stock
                    cursor.execute("""
                    UPDATE products SET stock_quantity = stock_quantity - ?
                    WHERE id = ?
                    """, (item.quantity, item.product_id))

                # Update customer total purchases
                if sale.customer_id:
                    cursor.execute("""
                    UPDATE customers SET total_purchases = total_purchases + ?
                    WHERE id = ?
                    """, (sale.final_amount, sale.customer_id))

                conn.commit()
                logger.info(f"Sale created: {sale_id}")
                return sale_id

        except Exception as e:
            logger.error(f"Error creating sale: {e}")
            return None

    def get_recent_sales(self, limit: int = 50) -> List[Tuple[Sale, List[SaleItem]]]:
        """Get recent sales with items"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()

                # Get sales
                cursor.execute("""
                SELECT * FROM sales 
                ORDER BY created_at DESC LIMIT ?
                """, (limit,))

                sales_rows = cursor.fetchall()
                sales_with_items = []

                for sale_row in sales_rows:
                    sale = Sale(**dict(sale_row))

                    # Get items for this sale
                    cursor.execute("""
                    SELECT * FROM sale_items WHERE sale_id = ?
                    """, (sale.id,))

                    items_rows = cursor.fetchall()
                    items = [SaleItem(**dict(item_row)) for item_row in items_rows]

                    sales_with_items.append((sale, items))

                return sales_with_items

        except Exception as e:
            logger.error(f"Error getting recent sales: {e}")
            return []

    # Statistics
    def get_dashboard_stats(self) -> Dict[str, Any]:
        """Get dashboard statistics"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                stats = {}

                # Get basic stats
                total_products_result = self.execute_query("SELECT COUNT(*) FROM products")
                total_customers_result = self.execute_query("SELECT COUNT(*) FROM customers")
                
                total_products = total_products_result[0][0] if total_products_result else 0
                total_customers = total_customers_result[0][0] if total_customers_result else 0

                # Today's sales
                today = datetime.now().strftime('%Y-%m-%d')
                today_sales_result = self.execute_query("""
                    SELECT COUNT(*), COALESCE(SUM(final_amount), 0) 
                    FROM sales 
                    WHERE DATE(created_at) = ?
                """, (today,))

                today_sales_count = 0
                today_sales_total = 0
                if today_sales_result:
                    today_sales_count, today_sales_total = today_sales_result[0]

                # Low stock products
                low_stock_result = self.execute_query("SELECT COUNT(*) FROM products WHERE stock_quantity <= min_stock")
                low_stock_count = low_stock_result[0][0] if low_stock_result else 0

                # Inventory stats
                inventory_result = self.execute_query("""
                    SELECT COUNT(*), COALESCE(SUM(stock_quantity), 0), COALESCE(SUM(price * stock_quantity), 0)
                    FROM products
                """)

                total_products_count = 0
                total_stock = 0
                inventory_value = 0
                if inventory_result:
                    total_products_count, total_stock, inventory_value = inventory_result[0]

                stats['total_products'] = total_products
                stats['total_customers'] = total_customers
                stats['today_sales'] = today_sales_count
                stats['today_revenue'] = today_sales_total
                stats['low_stock'] = low_stock_count
                stats['inventory_value'] = inventory_value
                stats['total_stock'] = total_stock

                return stats

        except Exception as e:
            logger.error(f"Error getting dashboard stats: {e}")
            return {
                'total_products': 0,
                'total_customers': 0,
                'today_sales': 0,
                'today_revenue': 0,
                'low_stock': 0,
                'inventory_value': 0,
                'total_stock': 0
            }

    def get_low_stock_products(self) -> List[Product]:
        """Get products with low stock"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()

                cursor.execute("""
                SELECT * FROM products 
                WHERE stock_quantity <= min_stock 
                ORDER BY stock_quantity ASC
                """)

                rows = cursor.fetchall()
                return [Product(**dict(row)) for row in rows]

        except Exception as e:
            logger.error(f"Error getting low stock products: {e}")
            return []

    # Helper method to execute queries, used internally by get_dashboard_stats
    def execute_query(self, query: str, params: Tuple = ()) -> List[Tuple]:
        """Execute a query and return results"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                return cursor.fetchall()
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            return []