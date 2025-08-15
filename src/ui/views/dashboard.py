
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
    
    def _create_sales_chart(self, parent, column):
        """Create sales trends chart"""
        chart_frame = ctk.CTkFrame(parent, corner_radius=10)
        chart_frame.grid(row=0, column=column, padx=(0, 10), pady=0, sticky="nsew")
        chart_frame.grid_columnconfigure(0, weight=1)
        chart_frame.grid_rowconfigure(1, weight=1)
        
        # Chart title
        title_label = ctk.CTkLabel(
            chart_frame,
            text="📈 اتجاه المبيعات (آخر 7 أيام)",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.grid(row=0, column=0, pady=15)
        
        # Chart canvas
        fig = Figure(figsize=(6, 4), dpi=100, facecolor='none')
        ax = fig.add_subplot(111)
        
        # Sample data (will be replaced with real data)
        dates = [datetime.now() - timedelta(days=i) for i in range(6, -1, -1)]
        sales = [1200, 1500, 900, 2100, 1800, 2400, 1900]
        
        ax.plot(dates, sales, marker='o', linewidth=2, markersize=6, color='#3B8ED0')
        ax.set_title('مبيعات الأسبوع الماضي', fontsize=12, pad=20)
        ax.set_ylabel('المبيعات (ر.س)', fontsize=10)
        ax.grid(True, alpha=0.3)
        
        # Format x-axis
        fig.autofmt_xdate()
        
        # Adjust layout
        fig.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, chart_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=0, padx=10, pady=(0, 15), sticky="nsew")
        
        self.sales_chart = canvas
    
    def _create_products_chart(self, parent, column):
        """Create products distribution chart"""
        chart_frame = ctk.CTkFrame(parent, corner_radius=10)
        chart_frame.grid(row=0, column=column, padx=(10, 0), pady=0, sticky="nsew")
        chart_frame.grid_columnconfigure(0, weight=1)
        chart_frame.grid_rowconfigure(1, weight=1)
        
        # Chart title
        title_label = ctk.CTkLabel(
            chart_frame,
            text="📊 توزيع المنتجات حسب الفئة",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.grid(row=0, column=0, pady=15)
        
        # Chart canvas
        fig = Figure(figsize=(6, 4), dpi=100, facecolor='none')
        ax = fig.add_subplot(111)
        
        # Sample data (will be replaced with real data)
        categories = ['هواتف ذكية', 'إكسسوارات', 'هواتف مستعملة', 'قطع غيار']
        values = [45, 25, 20, 10]
        colors_pie = ['#3B8ED0', '#27ae60', '#f39c12', '#e74c3c']
        
        wedges, texts, autotexts = ax.pie(
            values, labels=categories, colors=colors_pie,
            autopct='%1.1f%%', startangle=90
        )
        
        ax.set_title('توزيع المنتجات', fontsize=12, pad=20)
        
        # Adjust layout
        fig.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, chart_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=0, padx=10, pady=(0, 15), sticky="nsew")
        
        self.products_chart = canvas
    
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
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dashboard View
عرض لوحة التحكم
"""

import customtkinter as ctk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta

from src.utils.logger import get_logger

logger = get_logger(__name__)

class DashboardView(ctk.CTkFrame):
    """Dashboard view with statistics and charts"""
    
    def __init__(self, parent, db_manager, theme_manager):
        super().__init__(parent)
        
        self.db_manager = db_manager
        self.theme_manager = theme_manager
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self._create_widgets()
        self._load_dashboard_data()
    
    def _create_widgets(self):
        """Create dashboard widgets"""
        # Title
        title_label = ctk.CTkLabel(
            self,
            text="لوحة التحكم الرئيسية",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="ew")
        
        # Statistics cards frame
        stats_frame = ctk.CTkFrame(self)
        stats_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        stats_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Statistics cards
        self.stats_cards = {}
        stats_data = [
            ("إجمالي المنتجات", "total_products", "#3b82f6"),
            ("إجمالي العملاء", "total_customers", "#10b981"), 
            ("مبيعات اليوم", "today_sales", "#f59e0b"),
            ("مخزون منخفض", "low_stock", "#ef4444")
        ]
        
        for i, (title, key, color) in enumerate(stats_data):
            card = self._create_stat_card(stats_frame, title, "0", color)
            card.grid(row=0, column=i, padx=10, pady=10, sticky="ew")
            self.stats_cards[key] = card
        
        # Charts frame
        charts_frame = ctk.CTkFrame(self)
        charts_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        charts_frame.grid_columnconfigure(0, weight=1)
        charts_frame.grid_rowconfigure(0, weight=1)
        
        # Create placeholder chart
        self._create_chart(charts_frame)
    
    def _create_stat_card(self, parent, title, value, color):
        """Create a statistics card"""
        card = ctk.CTkFrame(parent)
        
        # Title
        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        title_label.pack(pady=(10, 5))
        
        # Value
        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=color
        )
        value_label.pack(pady=(0, 10))
        
        # Store value label for updates
        card.value_label = value_label
        
        return card
    
    def _create_chart(self, parent):
        """Create a sample chart"""
        try:
            # Create figure
            fig, ax = plt.subplots(figsize=(10, 6))
            fig.patch.set_facecolor('#2b2b2b' if self.theme_manager.current_theme == "dark" else 'white')
            ax.set_facecolor('#2b2b2b' if self.theme_manager.current_theme == "dark" else 'white')
            
            # Sample data
            days = ['الأحد', 'الاثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة', 'السبت']
            sales = [10, 15, 12, 20, 18, 25, 22]
            
            ax.bar(days, sales, color='#3b82f6')
            ax.set_title('مبيعات الأسبوع', color='white' if self.theme_manager.current_theme == "dark" else 'black')
            ax.set_ylabel('عدد المبيعات', color='white' if self.theme_manager.current_theme == "dark" else 'black')
            
            # Style axes
            ax.tick_params(colors='white' if self.theme_manager.current_theme == "dark" else 'black')
            
            # Add to tkinter
            canvas = FigureCanvasTkAgg(fig, parent)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
            
        except Exception as e:
            logger.error(f"Error creating chart: {e}")
            error_label = ctk.CTkLabel(parent, text="خطأ في تحميل الرسم البياني")
            error_label.pack(expand=True)
    
    def _load_dashboard_data(self):
        """Load dashboard statistics"""
        try:
            stats = self.db_manager.get_dashboard_stats()
            
            # Update stat cards
            if "total_products" in self.stats_cards:
                self.stats_cards["total_products"].value_label.configure(text=str(stats['total_products']))
            
            if "total_customers" in self.stats_cards:
                self.stats_cards["total_customers"].value_label.configure(text=str(stats['total_customers']))
            
            if "today_sales" in self.stats_cards:
                self.stats_cards["today_sales"].value_label.configure(text=str(stats['today_sales']))
            
            if "low_stock" in self.stats_cards:
                self.stats_cards["low_stock"].value_label.configure(text=str(stats['low_stock']))
                
        except Exception as e:
            logger.error(f"Error loading dashboard data: {e}")
            messagebox.showerror("خطأ", f"خطأ في تحميل بيانات لوحة التحكم: {e}")
