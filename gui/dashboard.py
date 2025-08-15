#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dashboard for Mobile Shop Management System
لوحة المعلومات الرئيسية لنظام إدارة محل الموبايلات
"""

import customtkinter as ctk
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
from typing import Dict, Any

class Dashboard(ctk.CTkScrollableFrame):
    """Dashboard widget with key metrics and charts"""
    
    def __init__(self, parent, db_manager):
        super().__init__(parent)
        self.db_manager = db_manager
        
        # Configure matplotlib for Arabic support
        plt.rcParams['font.family'] = ['Arial Unicode MS', 'Tahoma', 'DejaVu Sans']
        
        self.create_widgets()
        self.refresh_data()
    
    def create_widgets(self):
        """Create dashboard widgets"""
        # Title
        self.title_label = ctk.CTkLabel(
            self,
            text="لوحة المعلومات الرئيسية",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        self.title_label.pack(pady=(0, 30))
        
        # Stats cards frame
        self.stats_frame = ctk.CTkFrame(self)
        self.stats_frame.pack(fill="x", pady=(0, 20))
        
        # Configure grid for stats cards
        for i in range(4):
            self.stats_frame.grid_columnconfigure(i, weight=1)
        
        # Create stat cards
        self.create_stat_cards()
        
        # Charts frame
        self.charts_frame = ctk.CTkFrame(self)
        self.charts_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        # Configure charts grid
        self.charts_frame.grid_columnconfigure(0, weight=1)
        self.charts_frame.grid_columnconfigure(1, weight=1)
        
        # Create charts
        self.create_charts()
        
        # Quick actions frame
        self.actions_frame = ctk.CTkFrame(self)
        self.actions_frame.pack(fill="x", pady=(20, 0))
        
        # Create quick action buttons
        self.create_quick_actions()
    
    def create_stat_cards(self):
        """Create statistics cards"""
        # Today's Sales Card
        self.today_sales_card = self.create_stat_card(
            self.stats_frame, 
            "مبيعات اليوم", 
            "0 ريال", 
            "📈", 
            0, 0
        )
        
        # Monthly Sales Card
        self.month_sales_card = self.create_stat_card(
            self.stats_frame, 
            "مبيعات الشهر", 
            "0 ريال", 
            "💰", 
            0, 1
        )
        
        # Total Products Card
        self.products_card = self.create_stat_card(
            self.stats_frame, 
            "إجمالي المنتجات", 
            "0", 
            "📱", 
            0, 2
        )
        
        # Low Stock Alert Card
        self.low_stock_card = self.create_stat_card(
            self.stats_frame, 
            "تنبيه مخزون منخفض", 
            "0", 
            "⚠️", 
            0, 3
        )
    
    def create_stat_card(self, parent, title, value, icon, row, col):
        """Create a single statistics card"""
        card_frame = ctk.CTkFrame(parent)
        card_frame.grid(row=row, column=col, padx=10, pady=10, sticky="ew")
        
        # Icon
        icon_label = ctk.CTkLabel(
            card_frame,
            text=icon,
            font=ctk.CTkFont(size=32)
        )
        icon_label.pack(pady=(15, 5))
        
        # Value
        value_label = ctk.CTkLabel(
            card_frame,
            text=value,
            font=ctk.CTkFont(size=24, weight="bold")
        )
        value_label.pack(pady=5)
        
        # Title
        title_label = ctk.CTkLabel(
            card_frame,
            text=title,
            font=ctk.CTkFont(size=14)
        )
        title_label.pack(pady=(5, 15))
        
        return {
            'frame': card_frame,
            'value_label': value_label,
            'title_label': title_label
        }
    
    def create_charts(self):
        """Create charts for visualization"""
        # Sales chart
        self.sales_chart_frame = ctk.CTkFrame(self.charts_frame)
        self.sales_chart_frame.grid(row=0, column=0, padx=(0, 10), pady=10, sticky="nsew")
        
        sales_title = ctk.CTkLabel(
            self.sales_chart_frame,
            text="مبيعات آخر 7 أيام",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        sales_title.pack(pady=(10, 5))
        
        # Top products chart
        self.products_chart_frame = ctk.CTkFrame(self.charts_frame)
        self.products_chart_frame.grid(row=0, column=1, padx=(10, 0), pady=10, sticky="nsew")
        
        products_title = ctk.CTkLabel(
            self.products_chart_frame,
            text="أفضل المنتجات مبيعاً",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        products_title.pack(pady=(10, 5))
        
        self.charts_frame.grid_rowconfigure(0, weight=1)
    
    def create_quick_actions(self):
        """Create quick action buttons"""
        actions_title = ctk.CTkLabel(
            self.actions_frame,
            text="إجراءات سريعة",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        actions_title.pack(pady=(15, 10))
        
        buttons_frame = ctk.CTkFrame(self.actions_frame)
        buttons_frame.pack(pady=(0, 15))
        
        # Quick sale button
        self.quick_sale_btn = ctk.CTkButton(
            buttons_frame,
            text="بيعة سريعة",
            font=ctk.CTkFont(size=16),
            height=40,
            width=150
        )
        self.quick_sale_btn.pack(side="left", padx=10, pady=10)
        
        # Add product button
        self.add_product_btn = ctk.CTkButton(
            buttons_frame,
            text="إضافة منتج",
            font=ctk.CTkFont(size=16),
            height=40,
            width=150
        )
        self.add_product_btn.pack(side="left", padx=10, pady=10)
        
        # Add customer button
        self.add_customer_btn = ctk.CTkButton(
            buttons_frame,
            text="إضافة عميل",
            font=ctk.CTkFont(size=16),
            height=40,
            width=150
        )
        self.add_customer_btn.pack(side="left", padx=10, pady=10)
        
        # Refresh button
        self.refresh_btn = ctk.CTkButton(
            buttons_frame,
            text="تحديث البيانات",
            font=ctk.CTkFont(size=16),
            height=40,
            width=150,
            command=self.refresh_data
        )
        self.refresh_btn.pack(side="left", padx=10, pady=10)
    
    def refresh_data(self):
        """Refresh dashboard data"""
        try:
            # Get statistics from database
            stats = self.db_manager.get_dashboard_stats()
            
            # Update stat cards
            self.today_sales_card['value_label'].configure(
                text=f"{stats.get('today_sales_total', 0):.2f} ريال"
            )
            
            self.month_sales_card['value_label'].configure(
                text=f"{stats.get('month_sales_total', 0):.2f} ريال"
            )
            
            self.products_card['value_label'].configure(
                text=f"{stats.get('total_products', 0)}"
            )
            
            # Update low stock card with color coding
            low_stock_count = stats.get('low_stock_count', 0)
            self.low_stock_card['value_label'].configure(text=f"{low_stock_count}")
            
            if low_stock_count > 0:
                self.low_stock_card['frame'].configure(fg_color=("red", "darkred"))
            else:
                self.low_stock_card['frame'].configure(fg_color=["gray86", "gray17"])
            
            # Update charts
            self.update_sales_chart()
            self.update_products_chart()
            
        except Exception as e:
            print(f"خطأ في تحديث البيانات: {e}")
    
    def update_sales_chart(self):
        """Update sales chart with last 7 days data"""
        try:
            # Clear previous chart
            for widget in self.sales_chart_frame.winfo_children():
                if isinstance(widget, FigureCanvasTkAgg):
                    widget.get_tk_widget().destroy()
            
            # Get sales data for last 7 days
            end_date = datetime.now()
            start_date = end_date - timedelta(days=6)
            
            sales_data = self.db_manager.execute_query("""
                SELECT DATE(sale_date) as sale_day, 
                       COUNT(*) as sales_count,
                       COALESCE(SUM(total_amount), 0) as total_amount
                FROM sales 
                WHERE DATE(sale_date) BETWEEN ? AND ?
                GROUP BY DATE(sale_date)
                ORDER BY sale_day
            """, (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
            
            # Create figure
            fig, ax = plt.subplots(figsize=(6, 4))
            fig.patch.set_facecolor('none')
            ax.set_facecolor('none')
            
            if sales_data:
                dates = [datetime.strptime(row['sale_day'], '%Y-%m-%d') for row in sales_data]
                amounts = [row['total_amount'] for row in sales_data]
                
                ax.plot(dates, amounts, marker='o', linewidth=2, markersize=6)
                ax.fill_between(dates, amounts, alpha=0.3)
            else:
                # Show empty chart
                ax.text(0.5, 0.5, 'لا توجد بيانات', ha='center', va='center', 
                       transform=ax.transAxes, fontsize=14)
            
            ax.set_xlabel('التاريخ')
            ax.set_ylabel('المبيعات (ريال)')
            ax.tick_params(axis='x', rotation=45)
            
            # Format dates on x-axis
            if sales_data:
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
                ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
            
            plt.tight_layout()
            
            # Add chart to frame
            canvas = FigureCanvasTkAgg(fig, self.sales_chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=(5, 10))
            
        except Exception as e:
            print(f"خطأ في تحديث رسم المبيعات: {e}")
    
    def update_products_chart(self):
        """Update top products chart"""
        try:
            # Clear previous chart
            for widget in self.products_chart_frame.winfo_children():
                if isinstance(widget, FigureCanvasTkAgg):
                    widget.get_tk_widget().destroy()
            
            # Get top selling products
            top_products = self.db_manager.execute_query("""
                SELECT p.name, SUM(si.quantity) as total_sold
                FROM sale_items si
                JOIN products p ON si.product_id = p.id
                JOIN sales s ON si.sale_id = s.id
                WHERE DATE(s.sale_date) >= date('now', '-30 days')
                GROUP BY p.id, p.name
                ORDER BY total_sold DESC
                LIMIT 5
            """)
            
            # Create figure
            fig, ax = plt.subplots(figsize=(6, 4))
            fig.patch.set_facecolor('none')
            ax.set_facecolor('none')
            
            if top_products:
                names = [row['name'][:20] + '...' if len(row['name']) > 20 else row['name'] 
                        for row in top_products]
                quantities = [row['total_sold'] for row in top_products]
                
                bars = ax.barh(names, quantities)
                
                # Add value labels on bars
                for i, bar in enumerate(bars):
                    width = bar.get_width()
                    ax.text(width, bar.get_y() + bar.get_height()/2, 
                           f'{int(width)}', ha='left', va='center')
            else:
                ax.text(0.5, 0.5, 'لا توجد بيانات', ha='center', va='center', 
                       transform=ax.transAxes, fontsize=14)
            
            ax.set_xlabel('الكمية المباعة')
            plt.tight_layout()
            
            # Add chart to frame
            canvas = FigureCanvasTkAgg(fig, self.products_chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=(5, 10))
            
        except Exception as e:
            print(f"خطأ في تحديث رسم المنتجات: {e}")
