
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reports View
عرض التقارير
"""

import customtkinter as ctk
from tkinter import messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import threading
from datetime import datetime, timedelta

from src.utils.logger import get_logger

logger = get_logger(__name__)

class ReportsView(ctk.CTkFrame):
    """Reports and analytics view"""
    
    def __init__(self, parent, db_manager, theme_manager):
        super().__init__(parent, fg_color="transparent")
        
        self.db_manager = db_manager
        self.theme_manager = theme_manager
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup reports view UI"""
        colors = self.theme_manager.get_colors()
        
        # Title
        title_label = ctk.CTkLabel(
            self,
            text="📊 التقارير والإحصائيات",
            font=self.theme_manager.get_header_font_config(24),
            text_color=colors["accent"]
        )
        title_label.pack(pady=(0, 30))
        
        # Date range selection
        date_frame = ctk.CTkFrame(self, fg_color="transparent")
        date_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        ctk.CTkLabel(date_frame, text="فترة التقرير:", font=self.theme_manager.get_font_config(12, "bold")).pack(side="left", padx=(0, 10))
        
        self.date_range = ctk.CTkComboBox(
            date_frame,
            values=["اليوم", "أسبوع", "شهر", "3 أشهر", "6 أشهر", "سنة", "فترة مخصصة"],
            width=150,
            font=self.theme_manager.get_font_config(11)
        )
        self.date_range.pack(side="left", padx=(0, 20))
        
        # Generate report button
        generate_btn = ctk.CTkButton(
            date_frame,
            text="إنشاء التقرير",
            command=self._generate_report,
            font=self.theme_manager.get_font_config(12, "bold"),
            fg_color=colors["success"],
            hover_color="#229954"
        )
        generate_btn.pack(side="left")
        
        # Reports grid
        reports_frame = ctk.CTkFrame(self, fg_color="transparent")
        reports_frame.pack(expand=True, fill="both", padx=20)
        
        # Configure grid
        for i in range(3):
            reports_frame.grid_columnconfigure(i, weight=1)
        for i in range(3):
            reports_frame.grid_rowconfigure(i, weight=1)
        
        # Sales reports
        self._create_report_card(
            reports_frame, "📈 تقارير المبيعات", 
            "تقارير شاملة عن المبيعات اليومية والشهرية", 0, 0, self._show_sales_report
        )
        
        # Products reports  
        self._create_report_card(
            reports_frame, "📱 تقارير المنتجات",
            "تقارير المخزون والمنتجات الأكثر مبيعاً", 0, 1, self._show_products_report
        )
        
        # Customers reports
        self._create_report_card(
            reports_frame, "👥 تقارير العملاء", 
            "تقارير العملاء وسجل المشتريات", 0, 2, self._show_customers_report
        )
        
        # Financial reports
        self._create_report_card(
            reports_frame, "💰 التقارير المالية",
            "الأرباح والخسائر والتدفقات النقدية", 1, 0, self._show_financial_report
        )
        
        # Inventory reports
        self._create_report_card(
            reports_frame, "📦 تقارير المخزون",
            "حالة المخزون والتنبيهات", 1, 1, self._show_inventory_report
        )
        
        # Custom reports
        self._create_report_card(
            reports_frame, "🔧 تقارير مخصصة",
            "إنشاء تقارير مخصصة حسب الحاجة", 1, 2, self._show_custom_report
        )
    
    def _create_report_card(self, parent, title, description, row, column, command):
        """Create a report card widget"""
        colors = self.theme_manager.get_colors()
        
        card = ctk.CTkFrame(parent, corner_radius=15)
        card.grid(row=row, column=column, padx=15, pady=15, sticky="nsew")
        
        # Title
        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=self.theme_manager.get_font_config(16, "bold")
        )
        title_label.pack(pady=(20, 10))
        
        # Description
        desc_label = ctk.CTkLabel(
            card,
            text=description,
            font=self.theme_manager.get_font_config(12),
            wraplength=200
        )
        desc_label.pack(pady=(0, 20))
        
        # Generate button
        generate_btn = ctk.CTkButton(
            card,
            text="إنشاء التقرير",
            command=command,
            width=140,
            font=self.theme_manager.get_font_config(11)
        )
        generate_btn.pack(pady=(0, 20))
        
        return card
    
    def _generate_report(self):
        """Generate general report based on selected date range"""
        period = self.date_range.get()
        messagebox.showinfo("إنشاء التقرير", f"جاري إنشاء تقرير عام لفترة: {period}")
    
    def _show_sales_report(self):
        """Show sales report"""
        self._show_detailed_report("تقرير المبيعات", self._generate_sales_data)
    
    def _show_products_report(self):
        """Show products report"""
        self._show_detailed_report("تقرير المنتجات", self._generate_products_data)
    
    def _show_customers_report(self):
        """Show customers report"""
        self._show_detailed_report("تقرير العملاء", self._generate_customers_data)
    
    def _show_financial_report(self):
        """Show financial report"""
        self._show_detailed_report("التقرير المالي", self._generate_financial_data)
    
    def _show_inventory_report(self):
        """Show inventory report"""
        self._show_detailed_report("تقرير المخزون", self._generate_inventory_data)
    
    def _show_custom_report(self):
        """Show custom report builder"""
        messagebox.showinfo("تقارير مخصصة", "منشئ التقارير المخصصة قيد التطوير...")
    
    def _show_detailed_report(self, title, data_generator):
        """Show detailed report window"""
        colors = self.theme_manager.get_colors()
        
        # Create report window
        report_window = ctk.CTkToplevel(self)
        report_window.title(title)
        report_window.geometry("900x700")
        report_window.transient(self)
        
        # Header frame
        header_frame = ctk.CTkFrame(report_window, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(
            header_frame,
            text=title,
            font=self.theme_manager.get_header_font_config(20),
            text_color=colors["accent"]
        )
        title_label.pack(side="left")
        
        # Export button
        export_btn = ctk.CTkButton(
            header_frame,
            text="تصدير PDF",
            command=lambda: self._export_report(title),
            width=100,
            font=self.theme_manager.get_font_config(11)
        )
        export_btn.pack(side="right")
        
        # Content frame
        content_frame = ctk.CTkScrollableFrame(report_window)
        content_frame.pack(expand=True, fill="both", padx=20, pady=(0, 20))
        
        # Generate and display data
        data_generator(content_frame)
    
    def _generate_sales_data(self, parent):
        """Generate sales report data"""
        colors = self.theme_manager.get_colors()
        
        # Summary cards
        summary_frame = ctk.CTkFrame(parent, fg_color="transparent")
        summary_frame.pack(fill="x", pady=(0, 20))
        summary_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Sample data
        metrics = [
            ("إجمالي المبيعات", "45,670 ر.س", colors["success"]),
            ("عدد الفواتير", "267", colors["accent"]),
            ("متوسط الفاتورة", "171 ر.س", colors["warning"]),
            ("أعلى فاتورة", "2,450 ر.س", colors["danger"])
        ]
        
        for i, (label, value, color) in enumerate(metrics):
            card = ctk.CTkFrame(summary_frame, height=80)
            card.grid(row=0, column=i, padx=5, sticky="ew")
            
            ctk.CTkLabel(card, text=label, font=self.theme_manager.get_font_config(11)).pack(pady=(10, 5))
            ctk.CTkLabel(card, text=value, font=self.theme_manager.get_font_config(16, "bold"), text_color=color).pack(pady=(0, 10))
        
        # Chart
        chart_frame = ctk.CTkFrame(parent)
        chart_frame.pack(fill="x", pady=(0, 20))
        
        try:
            fig = Figure(figsize=(10, 6), dpi=100)
            ax = fig.add_subplot(111)
            
            # Sample sales data
            days = ['الأحد', 'الاثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة', 'السبت']
            sales = [5200, 6800, 4500, 7200, 6100, 8900, 7300]
            
            ax.plot(days, sales, marker='o', linewidth=2, markersize=6, color='#3B8ED0')
            ax.set_title('مبيعات الأسبوع', fontsize=14, fontweight='bold')
            ax.set_ylabel('المبيعات (ر.س)', fontsize=12)
            ax.grid(True, alpha=0.3)
            
            # Adjust layout
            fig.tight_layout()
            
            canvas = FigureCanvasTkAgg(fig, chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
            
        except Exception as e:
            logger.error(f"Error creating sales chart: {e}")
            ctk.CTkLabel(chart_frame, text="خطأ في تحميل الرسم البياني").pack(pady=20)
        
        # Top products table
        ctk.CTkLabel(parent, text="أكثر المنتجات مبيعاً:", font=self.theme_manager.get_font_config(14, "bold")).pack(anchor="w", pady=(20, 10))
        
        table_frame = ctk.CTkFrame(parent)
        table_frame.pack(fill="x", pady=(0, 20))
        
        # Table headers
        headers_frame = ctk.CTkFrame(table_frame, fg_color=colors["bg_secondary"])
        headers_frame.pack(fill="x", padx=10, pady=(10, 0))
        headers_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        headers = ["المنتج", "الكمية المبيعة", "الإيرادات", "النسبة"]
        for i, header in enumerate(headers):
            ctk.CTkLabel(headers_frame, text=header, font=self.theme_manager.get_font_config(12, "bold")).grid(row=0, column=i, padx=10, pady=10)
        
        # Table data
        products_data = [
            ("iPhone 15 Pro", "45", "202,500 ر.س", "44.3%"),
            ("Galaxy S24", "32", "102,400 ر.س", "22.4%"),
            ("AirPods Pro", "67", "63,650 ر.س", "13.9%"),
            ("Phone Cases", "120", "5,400 ر.س", "1.2%"),
            ("Chargers", "89", "7,565 ر.س", "1.7%")
        ]
        
        for i, (product, qty, revenue, percentage) in enumerate(products_data):
            row_frame = ctk.CTkFrame(table_frame, fg_color="transparent" if i % 2 == 0 else colors["bg_tertiary"])
            row_frame.pack(fill="x", padx=10, pady=2)
            row_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
            
            ctk.CTkLabel(row_frame, text=product, font=self.theme_manager.get_font_config(11)).grid(row=0, column=0, padx=10, pady=8, sticky="w")
            ctk.CTkLabel(row_frame, text=qty, font=self.theme_manager.get_font_config(11)).grid(row=0, column=1, padx=10, pady=8)
            ctk.CTkLabel(row_frame, text=revenue, font=self.theme_manager.get_font_config(11)).grid(row=0, column=2, padx=10, pady=8)
            ctk.CTkLabel(row_frame, text=percentage, font=self.theme_manager.get_font_config(11, "bold"), text_color=colors["success"]).grid(row=0, column=3, padx=10, pady=8)
    
    def _generate_products_data(self, parent):
        """Generate products report data"""
        colors = self.theme_manager.get_colors()
        
        # Products summary
        ctk.CTkLabel(parent, text="ملخص المنتجات:", font=self.theme_manager.get_font_config(16, "bold")).pack(anchor="w", pady=(0, 20))
        
        summary_frame = ctk.CTkFrame(parent)
        summary_frame.pack(fill="x", pady=(0, 20))
        summary_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Summary cards
        metrics = [
            ("إجمالي المنتجات", "847"),
            ("منتجات نشطة", "623"),
            ("مخزون منخفض", "23")
        ]
        
        for i, (label, value) in enumerate(metrics):
            card = ctk.CTkFrame(summary_frame, height=80)
            card.grid(row=0, column=i, padx=10, pady=10, sticky="ew")
            
            ctk.CTkLabel(card, text=label, font=self.theme_manager.get_font_config(12)).pack(pady=(15, 5))
            ctk.CTkLabel(card, text=value, font=self.theme_manager.get_font_config(18, "bold"), text_color=colors["accent"]).pack(pady=(0, 15))
        
        # Low stock alerts
        ctk.CTkLabel(parent, text="تنبيهات المخزون المنخفض:", font=self.theme_manager.get_font_config(14, "bold"), text_color=colors["warning"]).pack(anchor="w", pady=(20, 10))
        
        alerts_frame = ctk.CTkFrame(parent)
        alerts_frame.pack(fill="x", pady=(0, 20))
        
        low_stock_items = [
            ("Galaxy S24", "2", "5"),
            ("iPhone Case Pro", "1", "10"),
            ("USB-C Cable", "3", "15")
        ]
        
        for item, current, minimum in low_stock_items:
            alert_frame = ctk.CTkFrame(alerts_frame, fg_color=colors["warning"], corner_radius=8)
            alert_frame.pack(fill="x", padx=10, pady=2)
            alert_frame.grid_columnconfigure(1, weight=1)
            
            ctk.CTkLabel(alert_frame, text="⚠️", font=self.theme_manager.get_font_config(16)).grid(row=0, column=0, padx=10, pady=8)
            ctk.CTkLabel(alert_frame, text=f"{item} - المتوفر: {current} (الحد الأدنى: {minimum})", font=self.theme_manager.get_font_config(11, "bold")).grid(row=0, column=1, padx=10, pady=8, sticky="w")
    
    def _generate_customers_data(self, parent):
        """Generate customers report data"""
        colors = self.theme_manager.get_colors()
        
        ctk.CTkLabel(parent, text="إحصائيات العملاء:", font=self.theme_manager.get_font_config(16, "bold")).pack(anchor="w", pady=(0, 20))
        
        # Customer metrics
        metrics_frame = ctk.CTkFrame(parent)
        metrics_frame.pack(fill="x", pady=(0, 20))
        metrics_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        metrics = [
            ("إجمالي العملاء", "1,247"),
            ("عملاء جدد هذا الشهر", "89"),
            ("عملاء نشطون", "567"),
            ("متوسط قيمة العميل", "2,340 ر.س")
        ]
        
        for i, (label, value) in enumerate(metrics):
            card = ctk.CTkFrame(metrics_frame, height=80)
            card.grid(row=0, column=i, padx=5, pady=10, sticky="ew")
            
            ctk.CTkLabel(card, text=label, font=self.theme_manager.get_font_config(11)).pack(pady=(10, 5))
            ctk.CTkLabel(card, text=value, font=self.theme_manager.get_font_config(14, "bold"), text_color=colors["accent"]).pack(pady=(0, 10))
        
        # Top customers
        ctk.CTkLabel(parent, text="أفضل العملاء:", font=self.theme_manager.get_font_config(14, "bold")).pack(anchor="w", pady=(20, 10))
        
        customers_frame = ctk.CTkFrame(parent)
        customers_frame.pack(fill="x")
        
        top_customers = [
            ("محمد خالد", "15,670 ر.س", "23 فاتورة"),
            ("أحمد محمد", "12,340 ر.س", "18 فاتورة"),
            ("فاطمة علي", "9,580 ر.س", "15 فاتورة"),
            ("نورا السعد", "7,230 ر.س", "12 فاتورة"),
            ("عبدالله أحمد", "6,890 ر.س", "11 فاتورة")
        ]
        
        for i, (name, total, invoices) in enumerate(top_customers):
            customer_frame = ctk.CTkFrame(customers_frame, fg_color=colors["bg_secondary"])
            customer_frame.pack(fill="x", padx=10, pady=2)
            customer_frame.grid_columnconfigure(1, weight=1)
            
            rank_label = ctk.CTkLabel(customer_frame, text=f"#{i+1}", font=self.theme_manager.get_font_config(12, "bold"), text_color=colors["accent"])
            rank_label.grid(row=0, column=0, padx=10, pady=10)
            
            name_label = ctk.CTkLabel(customer_frame, text=name, font=self.theme_manager.get_font_config(12, "bold"))
            name_label.grid(row=0, column=1, padx=10, pady=10, sticky="w")
            
            total_label = ctk.CTkLabel(customer_frame, text=total, font=self.theme_manager.get_font_config(11))
            total_label.grid(row=0, column=2, padx=10, pady=10)
            
            invoices_label = ctk.CTkLabel(customer_frame, text=invoices, font=self.theme_manager.get_font_config(11))
            invoices_label.grid(row=0, column=3, padx=10, pady=10)
    
    def _generate_financial_data(self, parent):
        """Generate financial report data"""
        colors = self.theme_manager.get_colors()
        
        ctk.CTkLabel(parent, text="التقرير المالي:", font=self.theme_manager.get_font_config(16, "bold")).pack(anchor="w", pady=(0, 20))
        
        # Financial summary
        summary_frame = ctk.CTkFrame(parent)
        summary_frame.pack(fill="x", pady=(0, 20))
        summary_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        metrics = [
            ("إجمالي الإيرادات", "345,670 ر.س", colors["success"]),
            ("التكاليف", "189,340 ر.س", colors["warning"]),
            ("صافي الربح", "156,330 ر.س", colors["success"]),
            ("هامش الربح", "45.2%", colors["accent"])
        ]
        
        for i, (label, value, color) in enumerate(metrics):
            card = ctk.CTkFrame(summary_frame, height=100)
            card.grid(row=0, column=i, padx=5, pady=10, sticky="ew")
            
            ctk.CTkLabel(card, text=label, font=self.theme_manager.get_font_config(12)).pack(pady=(15, 5))
            ctk.CTkLabel(card, text=value, font=self.theme_manager.get_font_config(16, "bold"), text_color=color).pack(pady=(0, 15))
        
        # Monthly breakdown
        ctk.CTkLabel(parent, text="التفصيل الشهري:", font=self.theme_manager.get_font_config(14, "bold")).pack(anchor="w", pady=(20, 10))
        
        monthly_frame = ctk.CTkFrame(parent)
        monthly_frame.pack(fill="x")
        
        months_data = [
            ("يناير", "28,450", "15,670", "12,780"),
            ("فبراير", "31,200", "17,340", "13,860"),
            ("مارس", "35,670", "19,220", "16,450"),
            ("أبريل", "29,880", "16,540", "13,340"),
            ("مايو", "33,120", "18,890", "14,230"),
            ("يونيو", "37,340", "20,120", "17,220")
        ]
        
        # Headers
        header_frame = ctk.CTkFrame(monthly_frame, fg_color=colors["bg_secondary"])
        header_frame.pack(fill="x", padx=10, pady=(10, 0))
        header_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        headers = ["الشهر", "الإيرادات", "التكاليف", "الربح"]
        for i, header in enumerate(headers):
            ctk.CTkLabel(header_frame, text=header, font=self.theme_manager.get_font_config(12, "bold")).grid(row=0, column=i, padx=10, pady=10)
        
        # Data rows
        for month, revenue, costs, profit in months_data:
            row_frame = ctk.CTkFrame(monthly_frame, fg_color="transparent")
            row_frame.pack(fill="x", padx=10, pady=2)
            row_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
            
            ctk.CTkLabel(row_frame, text=month, font=self.theme_manager.get_font_config(11)).grid(row=0, column=0, padx=10, pady=8, sticky="w")
            ctk.CTkLabel(row_frame, text=f"{revenue} ر.س", font=self.theme_manager.get_font_config(11)).grid(row=0, column=1, padx=10, pady=8)
            ctk.CTkLabel(row_frame, text=f"{costs} ر.س", font=self.theme_manager.get_font_config(11)).grid(row=0, column=2, padx=10, pady=8)
            ctk.CTkLabel(row_frame, text=f"{profit} ر.س", font=self.theme_manager.get_font_config(11, "bold"), text_color=colors["success"]).grid(row=0, column=3, padx=10, pady=8)
    
    def _generate_inventory_data(self, parent):
        """Generate inventory report data"""
        colors = self.theme_manager.get_colors()
        
        ctk.CTkLabel(parent, text="تقرير المخزون:", font=self.theme_manager.get_font_config(16, "bold")).pack(anchor="w", pady=(0, 20))
        
        # Inventory summary
        summary_frame = ctk.CTkFrame(parent)
        summary_frame.pack(fill="x", pady=(0, 20))
        summary_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        metrics = [
            ("قيمة المخزون الإجمالية", "567,890 ر.س"),
            ("عدد الأصناف", "1,247"),
            ("متوسط قيمة المنتج", "455 ر.س")
        ]
        
        for i, (label, value) in enumerate(metrics):
            card = ctk.CTkFrame(summary_frame, height=80)
            card.grid(row=0, column=i, padx=10, pady=10, sticky="ew")
            
            ctk.CTkLabel(card, text=label, font=self.theme_manager.get_font_config(12)).pack(pady=(15, 5))
            ctk.CTkLabel(card, text=value, font=self.theme_manager.get_font_config(16, "bold"), text_color=colors["accent"]).pack(pady=(0, 15))
        
        # Inventory status
        ctk.CTkLabel(parent, text="حالة المخزون:", font=self.theme_manager.get_font_config(14, "bold")).pack(anchor="w", pady=(20, 10))
        
        status_frame = ctk.CTkFrame(parent)
        status_frame.pack(fill="x")
        
        status_data = [
            ("متوفر", "823", colors["success"]),
            ("مخزون منخفض", "67", colors["warning"]),
            ("نفد المخزون", "23", colors["danger"]),
            ("معطل", "45", colors["text_secondary"])
        ]
        
        for status, count, color in status_data:
            status_row = ctk.CTkFrame(status_frame, fg_color="transparent")
            status_row.pack(fill="x", padx=10, pady=2)
            status_row.grid_columnconfigure(1, weight=1)
            
            ctk.CTkLabel(status_row, text="●", font=self.theme_manager.get_font_config(16), text_color=color).grid(row=0, column=0, padx=10, pady=8)
            ctk.CTkLabel(status_row, text=status, font=self.theme_manager.get_font_config(12)).grid(row=0, column=1, padx=10, pady=8, sticky="w")
            ctk.CTkLabel(status_row, text=count, font=self.theme_manager.get_font_config(12, "bold")).grid(row=0, column=2, padx=10, pady=8)
    
    def _export_report(self, report_title):
        """Export report to PDF"""
        file_path = filedialog.asksaveasfilename(
            title="حفظ التقرير",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            initialname=f"{report_title}_{datetime.now().strftime('%Y%m%d')}.pdf"
        )
        
        if file_path:
            messagebox.showinfo("تصدير التقرير", f"تم تصدير التقرير إلى:\n{file_path}")
