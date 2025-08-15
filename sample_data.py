
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sample Data Generator
مولد البيانات التجريبية
"""

import sqlite3
from pathlib import Path
import json
from datetime import datetime, timedelta
import random

def add_sample_data():
    """Add sample data to the database"""
    db_path = Path("data/database/shop.db")
    
    if not db_path.exists():
        print("Database file not found!")
        return
    
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        
        # Sample products
        products = [
            ("iPhone 15 Pro", "Apple", "15 Pro", 4500.0, 4000.0, 15, 5, "هواتف ذكية", "هاتف أيفون 15 برو", "IP15PRO001"),
            ("Galaxy S24 Ultra", "Samsung", "S24 Ultra", 4200.0, 3700.0, 12, 3, "هواتف ذكية", "هاتف جالكسي إس 24 ألترا", "GS24ULT001"),
            ("iPhone 14", "Apple", "14", 3200.0, 2800.0, 20, 5, "هواتف ذكية", "هاتف أيفون 14", "IP14001"),
            ("Galaxy A54", "Samsung", "A54", 1800.0, 1500.0, 25, 5, "هواتف ذكية", "هاتف جالكسي أي 54", "GA54001"),
            ("شاحن سريع", "Anker", "PowerPort", 150.0, 100.0, 50, 10, "إكسسوارات", "شاحن سريع 65 واط", "ANK001"),
            ("سماعات AirPods", "Apple", "Pro 2", 1200.0, 1000.0, 8, 3, "إكسسوارات", "سماعات أيربودز برو 2", "APR2001"),
            ("كفر حماية", "OtterBox", "Defender", 200.0, 120.0, 30, 10, "إكسسوارات", "كفر حماية قوي", "OTB001"),
            ("شاشة حماية", "Belkin", "Screen Guard", 80.0, 50.0, 100, 20, "إكسسوارات", "شاشة حماية زجاجية", "BLK001")
        ]
        
        for product in products:
            try:
                cursor.execute("""
                INSERT INTO products (name, brand, model, price, cost, stock_quantity, min_stock, category, description, barcode)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, product)
            except sqlite3.IntegrityError:
                pass  # Product already exists
        
        # Sample customers
        customers = [
            ("أحمد محمد العلي", "0501234567", "ahmed@email.com", "الرياض، حي النخيل", "عميل مميز"),
            ("فاطمة سالم", "0509876543", "fatima@email.com", "جدة، حي الصفا", ""),
            ("محمد عبدالله", "0551234567", "mohammed@email.com", "الدمام، حي الشاطئ", "يفضل التوصيل"),
            ("نورا أحمد", "0558765432", "nora@email.com", "الطائف، حي السلامة", ""),
            ("خالد السعيد", "0561234567", "khalid@email.com", "المدينة المنورة", "عميل منذ سنتين")
        ]
        
        for customer in customers:
            try:
                cursor.execute("""
                INSERT INTO customers (name, phone, email, address, notes)
                VALUES (?, ?, ?, ?, ?)
                """, customer)
            except:
                pass
        
        # Sample sales (recent)
        cursor.execute("SELECT id, name, price FROM products LIMIT 5")
        products_data = cursor.fetchall()
        
        cursor.execute("SELECT id, name FROM customers LIMIT 3")
        customers_data = cursor.fetchall()
        
        # Create some sales for today and yesterday
        for day_offset in range(2):
            sale_date = datetime.now() - timedelta(days=day_offset)
            for _ in range(random.randint(2, 5)):
                if products_data and customers_data:
                    customer = random.choice(customers_data)
                    product = random.choice(products_data)
                    
                    quantity = random.randint(1, 3)
                    unit_price = product[2]
                    total_amount = unit_price * quantity
                    discount = random.randint(0, 100)
                    tax = total_amount * 0.15
                    final_amount = total_amount - discount + tax
                    
                    cursor.execute("""
                    INSERT INTO sales (customer_id, customer_name, total_amount, discount, tax, final_amount, payment_method, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (customer[0], customer[1], total_amount, discount, tax, final_amount, 'cash', sale_date.strftime('%Y-%m-%d %H:%M:%S')))
                    
                    sale_id = cursor.lastrowid
                    
                    cursor.execute("""
                    INSERT INTO sale_items (sale_id, product_id, product_name, quantity, unit_price, total_price)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """, (sale_id, product[0], product[1], quantity, unit_price, unit_price * quantity))
        
        conn.commit()
        print("✅ Sample data added successfully!")
        print(f"Added {len(products)} products, {len(customers)} customers, and sample sales")

if __name__ == "__main__":
    add_sample_data()
