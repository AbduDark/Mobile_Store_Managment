
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sample Data Generator
مولد البيانات التجريبية
"""

import sqlite3
import random
from pathlib import Path
from datetime import datetime, timedelta

def add_sample_data():
    """Add sample data to the database"""
    db_path = Path("data/database/shop.db")
    
    # Remove existing database to start fresh
    if db_path.exists():
        db_path.unlink()
        print("Removed existing database")
    
    # Ensure directory exists
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        
        # Create tables
        print("Creating database tables...")
        
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

        print("Tables created successfully")
        
        # Sample products
        print("Adding sample products...")
        products = [
            ("iPhone 15 Pro", "Apple", "15 Pro", 4500.0, 4000.0, 15, 5, "هواتف ذكية", "هاتف أيفون 15 برو", "IP15PRO001"),
            ("Galaxy S24 Ultra", "Samsung", "S24 Ultra", 4200.0, 3700.0, 12, 3, "هواتف ذكية", "هاتف جالكسي إس 24 ألترا", "GS24ULT001"),
            ("iPhone 14", "Apple", "14", 3200.0, 2800.0, 20, 5, "هواتف ذكية", "هاتف أيفون 14", "IP14001"),
            ("Galaxy A54", "Samsung", "A54", 1800.0, 1500.0, 25, 5, "هواتف ذكية", "هاتف جالكسي أي 54", "GA54001"),
            ("شاحن سريع", "Anker", "PowerPort", 150.0, 100.0, 50, 10, "إكسسوارات", "شاحن سريع 65 واط", "ANK001"),
            ("سماعات AirPods", "Apple", "Pro 2", 1200.0, 1000.0, 8, 3, "إكسسوارات", "سماعات أيربودز برو 2", "APR2001"),
            ("كفر حماية", "OtterBox", "Defender", 200.0, 120.0, 30, 10, "إكسسوارات", "كفر حماية قوي", "OTB001"),
            ("شاشة حماية", "Belkin", "Screen Guard", 80.0, 50.0, 100, 20, "إكسسوارات", "شاشة حماية زجاجية", "BLK001"),
            ("باور بانك", "Xiaomi", "20000mAh", 180.0, 140.0, 35, 8, "إكسسوارات", "بطارية محمولة 20000 مللي أمبير", "XMI001"),
            ("سماعات لاسلكية", "JBL", "Tune 230NC", 350.0, 280.0, 22, 5, "إكسسوارات", "سماعات لاسلكية مع إلغاء الضوضاء", "JBL001"),
            ("Huawei P60 Pro", "Huawei", "P60 Pro", 3800.0, 3300.0, 10, 3, "هواتف ذكية", "هاتف هواوي بي 60 برو", "HWP60001"),
            ("OnePlus 11", "OnePlus", "11", 2900.0, 2500.0, 18, 4, "هواتف ذكية", "هاتف ون بلس 11", "OP11001")
        ]
        
        for product in products:
            try:
                cursor.execute("""
                INSERT INTO products (name, brand, model, price, cost, stock_quantity, min_stock, category, description, barcode)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, product)
            except sqlite3.IntegrityError:
                pass  # Product already exists
        
        print(f"Added {len(products)} products")
        
        # Sample customers
        print("Adding sample customers...")
        customers = [
            ("أحمد محمد العلي", "0501234567", "ahmed@email.com", "الرياض، حي النخيل", "عميل مميز"),
            ("فاطمة سالم", "0509876543", "fatima@email.com", "جدة، حي الصفا", ""),
            ("محمد عبدالله", "0551234567", "mohammed@email.com", "الدمام، حي الشاطئ", "يفضل التوصيل"),
            ("نورا أحمد", "0558765432", "nora@email.com", "الطائف، حي السلامة", ""),
            ("خالد السعيد", "0561234567", "khalid@email.com", "المدينة المنورة", "عميل منذ سنتين"),
            ("سارة محمد", "0571234567", "sara@email.com", "أبها، حي المنصور", "تفضل الدفع الإلكتروني"),
            ("عبدالعزيز أحمد", "0581234567", "abdulaziz@email.com", "القصيم، بريدة", ""),
            ("ليلى عبدالله", "0591234567", "layla@email.com", "الخبر، حي الراكة", "عميلة جديدة")
        ]
        
        for customer in customers:
            try:
                cursor.execute("""
                INSERT INTO customers (name, phone, email, address, notes)
                VALUES (?, ?, ?, ?, ?)
                """, customer)
            except:
                pass
        
        print(f"Added {len(customers)} customers")
        
        # Sample sales (recent)
        print("Adding sample sales...")
        cursor.execute("SELECT id, name, price FROM products")
        products_data = cursor.fetchall()
        
        cursor.execute("SELECT id, name FROM customers")
        customers_data = cursor.fetchall()
        
        # Create some sales for today and past few days
        total_sales = 0
        for day_offset in range(7):  # Last 7 days
            sale_date = datetime.now() - timedelta(days=day_offset)
            daily_sales = random.randint(2, 8)  # 2-8 sales per day
            
            for _ in range(daily_sales):
                if products_data and customers_data:
                    customer = random.choice(customers_data)
                    
                    # Create sale
                    total_amount = 0
                    sale_items = []
                    
                    # Add 1-4 items to each sale
                    num_items = random.randint(1, 4)
                    selected_products = random.sample(products_data, min(num_items, len(products_data)))
                    
                    for product in selected_products:
                        quantity = random.randint(1, 3)
                        unit_price = product[2]
                        item_total = unit_price * quantity
                        total_amount += item_total
                        sale_items.append((product[0], product[1], quantity, unit_price, item_total))
                    
                    discount = random.randint(0, int(total_amount * 0.1))  # Up to 10% discount
                    tax = (total_amount - discount) * 0.15  # 15% tax
                    final_amount = total_amount - discount + tax
                    
                    payment_methods = ['cash', 'card', 'transfer']
                    payment_method = random.choice(payment_methods)
                    
                    # Insert sale
                    cursor.execute("""
                    INSERT INTO sales (customer_id, customer_name, total_amount, discount, tax, final_amount, payment_method, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (customer[0], customer[1], total_amount, discount, tax, final_amount, payment_method, sale_date.strftime('%Y-%m-%d %H:%M:%S')))
                    
                    sale_id = cursor.lastrowid
                    total_sales += 1
                    
                    # Insert sale items
                    for product_id, product_name, quantity, unit_price, item_total in sale_items:
                        cursor.execute("""
                        INSERT INTO sale_items (sale_id, product_id, product_name, quantity, unit_price, total_price)
                        VALUES (?, ?, ?, ?, ?, ?)
                        """, (sale_id, product_id, product_name, quantity, unit_price, item_total))
                        
                        # Update product stock
                        cursor.execute("""
                        UPDATE products SET stock_quantity = stock_quantity - ?
                        WHERE id = ?
                        """, (quantity, product_id))
                    
                    # Update customer total purchases
                    cursor.execute("""
                    UPDATE customers SET total_purchases = total_purchases + ?
                    WHERE id = ?
                    """, (final_amount, customer[0]))
        
        print(f"Added {total_sales} sales with items")
        
        conn.commit()
        print("Sample data added successfully!")
        print(f"Database location: {db_path.absolute()}")

if __name__ == "__main__":
    add_sample_data()
