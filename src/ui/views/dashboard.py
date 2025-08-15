#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dashboard View
عرض لوحة التحكم
"""

import customtkinter as ctk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from datetime import datetime, timedelta
import threading

from src.utils.logger import get_logger

logger = get_logger(__name__)

class DashboardView(ctk.CTkFrame):
    """Modern dashboard with statistics and charts"""

    def __init__(self, parent, db_manager, theme_manager):
        super().__init__(parent, fg_color="transparent")

        self.db_manager = db_manager
        self.theme_manager = theme_manager

        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.stats_data = {}

        self._setup_ui()
        self._load_data()

    def _setup_ui(self):
        """Setup dashboard UI"""
        colors = self.theme_manager.get_colors()

        # Title section
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        title_frame.grid_columnconfigure(0, weight=1)

        title_label = ctk.CTkLabel(
            title_frame,
            text="📊 لوحة التحكم",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=colors["accent"]
        )
        title_label.grid(row=0, column=0)

        # Stats cards section
        self._create_stats_cards()

        # Charts section  
        self._create_charts_section()

        # Recent activities section
        self._create_activities_section()

    def _create_stats_cards(self):
        """Create statistics cards"""
        cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        cards_frame.grid(row=1, column=0, sticky="ew", pady=(0, 20))

        # Configure grid for 4 cards
        for i in range(4):
            cards_frame.grid_columnconfigure(i, weight=1)

        # Sales today card
        self.sales_today_card = self._create_stat_card(
            cards_frame, "💰 مبيعات اليوم", "0 ر.س", "0 عملية", 0
        )

        # Sales this month card  
        self.sales_month_card = self._create_stat_card(
            cards_frame, "📈 مبيعات الشهر", "0 ر.س", "0 عملية", 1
        )

        # Products count card
        self.products_card = self._create_stat_card(
            cards_frame, "📱 المنتجات", "0 منتج", "0 في المخزون", 2
        )

        # Low stock alert card
        self.low_stock_card = self._create_stat_card(
            cards_frame, "⚠️ تنبيه المخزون", "0 منتج", "مخزون منخفض", 3
        )

    def _create_stat_card(self, parent, title, main_value, sub_value, column):
        """Create individual statistics card"""
        colors = self.theme_manager.get_colors()

        card = ctk.CTkFrame(parent, height=120, corner_radius=10)
        card.grid(row=0, column=column, padx=10, pady=10, sticky="ew")
        card.grid_propagate(False)
        card.grid_columnconfigure(0, weight=1)

        # Title
        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=colors["text_secondary"]
        )
        title_label.grid(row=0, column=0, pady=(15, 5))

        # Main value
        main_label = ctk.CTkLabel(
            card,
            text=main_value,
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=colors["accent"]
        )
        main_label.grid(row=1, column=0, pady=5)

        # Sub value
        sub_label = ctk.CTkLabel(
            card,
            text=sub_value,
            font=ctk.CTkFont(size=12),
            text_color=colors["text_secondary"]
        )
        sub_label.grid(row=2, column=0, pady=(5, 15))

        return {
            'frame': card,
            'main_label': main_label,
            'sub_label': sub_label
        }

    def _create_charts_section(self):
        """Create charts section"""
        charts_frame = ctk.CTkFrame(self, fg_color="transparent")
        charts_frame.grid(row=2, column=0, sticky="nsew", pady=(0, 20))
        charts_frame.grid_columnconfigure(0, weight=1)
        charts_frame.grid_columnconfigure(1, weight=1)
        charts_frame.grid_rowconfigure(0, weight=1)

        # Sales chart
        self._create_sales_chart(charts_frame, 0)

        # Products chart
        self._create_products_chart(charts_frame, 1)

    def _create_sales_chart(self, frame, column):
        """Create sales chart with proper Arabic font support"""
        try:
            # Configure matplotlib for Arabic fonts
            import matplotlib.pyplot as plt
            import matplotlib.font_manager as fm
            from matplotlib import rcParams

            # Set Arabic font
            rcParams['font.family'] = [self.theme_manager.arabic_font_name, 'DejaVu Sans', 'Arial Unicode MS']
            rcParams['axes.unicode_minus'] = False
            rcParams['font.size'] = 11

            # Get actual sales data from database
            sales_data = self._get_monthly_sales_data()
            months = sales_data.get('months', ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو'])
            sales = sales_data.get('sales', [12000, 15000, 18000, 22000, 25000, 28000])

            # Create figure with dark/light theme support
            colors = self.theme_manager.get_colors()
            fig_color = colors['bg_secondary'] if colors['bg_secondary'] != '#ffffff' else 'white'
            text_color = colors['text_primary']

            fig, ax = plt.subplots(figsize=(6, 4))
            fig.patch.set_facecolor(fig_color)
            ax.set_facecolor(fig_color)

            # Create the plot
            line = ax.plot(months, sales, marker='o', linewidth=3, markersize=8, 
                          color='#3B8ED0', markerfacecolor='#2980b9')

            # Styling
            ax.set_title('📈 مبيعات آخر 6 أشهر', fontsize=16, pad=20, color=text_color, weight='bold')
            ax.set_xlabel('الشهر', fontsize=13, color=text_color)
            ax.set_ylabel('المبيعات (جنيه)', fontsize=13, color=text_color)

            # Grid and styling
            ax.grid(True, alpha=0.3, color=text_color)
            ax.tick_params(colors=text_color, labelsize=10)

            # Set spine colors
            for spine in ax.spines.values():
                spine.set_color(text_color)
                spine.set_alpha(0.3)

            # Rotate x-axis labels and adjust layout
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()

            # Add canvas to frame
            canvas = FigureCanvasTkAgg(fig, frame)
            canvas.draw()
            canvas.get_tk_widget().grid(row=0, column=column, padx=(0, 10), pady=0, sticky="nsew")

        except Exception as e:
            logger.error(f"Error creating sales chart: {e}")
            error_label = ctk.CTkLabel(
                frame, 
                text=f"خطأ في عرض الرسم البياني للمبيعات\n{str(e)[:50]}...",
                font=self.theme_manager.get_font_config(12),
                text_color="red"
            )
            error_label.grid(row=0, column=column, padx=(0, 10), pady=0, sticky="nsew")

    def _create_products_chart(self, frame, column):
        """Create products chart with proper Arabic font support"""
        try:
            import matplotlib.pyplot as plt
            from matplotlib import rcParams

            # Configure Arabic fonts
            rcParams['font.family'] = [self.theme_manager.arabic_font_name, 'DejaVu Sans', 'Arial Unicode MS']
            rcParams['axes.unicode_minus'] = False
            rcParams['font.size'] = 11

            # Get actual product data
            products_data = self._get_top_products_data()
            categories = products_data.get('categories', ['سامسونج', 'آيفون', 'هواوي', 'شاومي', 'أوبو'])
            quantities = products_data.get('quantities', [45, 30, 25, 35, 20])

            # Theme colors
            colors = self.theme_manager.get_colors()
            fig_color = colors['bg_secondary'] if colors['bg_secondary'] != '#ffffff' else 'white'
            text_color = colors['text_primary']

            fig, ax = plt.subplots(figsize=(6, 4))
            fig.patch.set_facecolor(fig_color)
            ax.set_facecolor(fig_color)

            # Create colorful bars
            bar_colors = ['#3B8ED0', '#27ae60', '#f39c12', '#e74c3c', '#9b59b6']
            bars = ax.bar(categories, quantities, color=bar_colors[:len(categories)])

            # Styling
            ax.set_title('📱 أكثر المنتجات مبيعاً', fontsize=16, pad=20, color=text_color, weight='bold')
            ax.set_xlabel('الماركة', fontsize=13, color=text_color)
            ax.set_ylabel('الكمية المباعة', fontsize=13, color=text_color)

            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                       f'{int(height)}', ha='center', va='bottom', 
                       color=text_color, fontsize=10, weight='bold')

            # Grid and styling
            ax.grid(True, alpha=0.3, axis='y', color=text_color)
            ax.tick_params(colors=text_color, labelsize=10)

            # Set spine colors
            for spine in ax.spines.values():
                spine.set_color(text_color)
                spine.set_alpha(0.3)

            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()

            canvas = FigureCanvasTkAgg(fig, frame)
            canvas.draw()
            canvas.get_tk_widget().grid(row=0, column=column, padx=(10, 0), pady=0, sticky="nsew")

        except Exception as e:
            logger.error(f"Error creating products chart: {e}")
            error_label = ctk.CTkLabel(
                frame, 
                text=f"خطأ في عرض رسم المنتجات\n{str(e)[:50]}...",
                font=self.theme_manager.get_font_config(12),
                text_color="red"
            )
            error_label.grid(row=0, column=column, padx=(10, 0), pady=0, sticky="nsew")

    def _create_activities_section(self):
        """Create recent activities section"""
        activities_frame = ctk.CTkFrame(self, corner_radius=10)
        activities_frame.grid(row=3, column=0, sticky="ew", pady=(0, 0))
        activities_frame.grid_columnconfigure(1, weight=1)

        # Title
        title_label = ctk.CTkLabel(
            activities_frame,
            text="🕒 النشاطات الأخيرة",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=15)

        # Activities list (sample)
        activities = [
            "تم إنشاء فاتورة جديدة #001",
            "تم إضافة منتج جديد: iPhone 15 Pro",
            "تنبيه: مخزون منخفض لمنتج Galaxy S24",
            "تم تحديث معلومات العميل أحمد محمد"
        ]

        for i, activity in enumerate(activities):
            activity_label = ctk.CTkLabel(
                activities_frame,
                text=f"• {activity}",
                font=ctk.CTkFont(size=12),
                anchor="w"
            )
            activity_label.grid(row=i+1, column=0, columnspan=2, padx=20, pady=5, sticky="w")

        # Add some padding at the bottom
        ctk.CTkLabel(activities_frame, text="").grid(row=len(activities)+1, column=0, pady=10)

    def _load_data(self):
        """Load dashboard data in background"""
        def load_stats():
            try:
                self.stats_data = self.db_manager.get_dashboard_stats()
                self.after(0, self._update_stats_display)
            except Exception as e:
                logger.error(f"Error loading dashboard stats: {e}")

        # Load data in background thread
        threading.Thread(target=load_stats, daemon=True).start()

    def _update_stats_display(self):
        """Update statistics display with loaded data"""
        try:
            if not self.stats_data:
                return

            colors = self.theme_manager.get_colors()

            # Update sales today card
            today_sales = self.stats_data.get('today_sales', {})
            self.sales_today_card['main_label'].configure(
                text=f"{today_sales.get('total', 0):.0f} ر.س"
            )
            self.sales_today_card['sub_label'].configure(
                text=f"{today_sales.get('count', 0)} عملية"
            )

            # Update sales month card
            month_sales = self.stats_data.get('month_sales', {})
            self.sales_month_card['main_label'].configure(
                text=f"{month_sales.get('total', 0):.0f} ر.س"
            )
            self.sales_month_card['sub_label'].configure(
                text=f"{month_sales.get('count', 0)} عملية"
            )

            # Update products card
            inventory = self.stats_data.get('inventory', {})
            self.products_card['main_label'].configure(
                text=f"{inventory.get('total_products', 0)} منتج"
            )
            self.products_card['sub_label'].configure(
                text=f"{inventory.get('total_stock', 0)} في المخزون"
            )

            # Update low stock card
            low_stock_count = self.stats_data.get('low_stock_count', 0)
            self.low_stock_card['main_label'].configure(
                text=f"{low_stock_count} منتج"
            )

            # Change color if there are low stock items
            if low_stock_count > 0:
                self.low_stock_card['main_label'].configure(
                    text_color=colors["warning"]
                )

        except Exception as e:
            logger.error(f"Error updating stats display: {e}")

    def refresh_data(self):
        """Refresh dashboard data"""
        self._load_data()

    def _get_monthly_sales_data(self):
        """Get monthly sales data from database"""
        try:
            cursor = self.db_manager.connection.cursor()
            cursor.execute('''
                SELECT 
                    strftime('%m', created_at) as month,
                    SUM(final_amount) as total_sales
                FROM sales 
                WHERE created_at >= date('now', '-6 months')
                GROUP BY strftime('%Y-%m', created_at)
                ORDER BY created_at
            ''')

            results = cursor.fetchall()

            # Month names in Arabic
            month_names = {
                '01': 'يناير', '02': 'فبراير', '03': 'مارس',
                '04': 'أبريل', '05': 'مايو', '06': 'يونيو',
                '07': 'يوليو', '08': 'أغسطس', '09': 'سبتمبر',
                '10': 'أكتوبر', '11': 'نوفمبر', '12': 'ديسمبر'
            }

            months = []
            sales = []

            for month_num, total in results:
                months.append(month_names.get(month_num, f'شهر {month_num}'))
                sales.append(total or 0)

            # If no data, return sample data
            if not months:
                return {
                    'months': ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو'],
                    'sales': [12000, 15000, 18000, 22000, 25000, 28000]
                }

            return {'months': months, 'sales': sales}

        except Exception as e:
            logger.error(f"Error getting monthly sales data: {e}")
            return {
                'months': ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو'],
                'sales': [0, 0, 0, 0, 0, 0]
            }

    def _get_top_products_data(self):
        """Get top selling products data"""
        try:
            cursor = self.db_manager.connection.cursor()
            cursor.execute('''
                SELECT 
                    p.brand,
                    SUM(si.quantity) as total_quantity
                FROM sale_items si
                JOIN products p ON si.product_id = p.id
                GROUP BY p.brand
                ORDER BY total_quantity DESC
                LIMIT 5
            ''')

            results = cursor.fetchall()

            categories = []
            quantities = []

            for brand, quantity in results:
                categories.append(brand or 'غير محدد')
                quantities.append(quantity or 0)

            # If no data, return sample data
            if not categories:
                return {
                    'categories': ['سامسونج', 'آيفون', 'هواوي', 'شاومي', 'أوبو'],
                    'quantities': [45, 30, 25, 35, 20]
                }

            return {'categories': categories, 'quantities': quantities}

        except Exception as e:
            logger.error(f"Error getting top products data: {e}")
            return {
                'categories': ['سامسونج', 'آيفون', 'هواوي', 'شاومي', 'أوبو'],
                'quantities': [0, 0, 0, 0, 0]
            }