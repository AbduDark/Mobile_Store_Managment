
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reports View
عرض التقارير
"""

import customtkinter as ctk
from tkinter import messagebox

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
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=colors["accent"]
        )
        title_label.pack(pady=(0, 30))
        
        # Reports grid
        reports_frame = ctk.CTkFrame(self, fg_color="transparent")
        reports_frame.pack(expand=True, fill="both", padx=20)
        
        # Configure grid
        for i in range(3):
            reports_frame.grid_columnconfigure(i, weight=1)
        for i in range(3):
            reports_frame.grid_rowconfigure(i, weight=1)
        
        # Sales reports
        sales_frame = self._create_report_card(
            reports_frame, "📈 تقارير المبيعات", 
            "تقارير شاملة عن المبيعات اليومية والشهرية", 0, 0
        )
        
        # Products reports  
        products_frame = self._create_report_card(
            reports_frame, "📱 تقارير المنتجات",
            "تقارير المخزون والمنتجات الأكثر مبيعاً", 0, 1
        )
        
        # Customers reports
        customers_frame = self._create_report_card(
            reports_frame, "👥 تقارير العملاء", 
            "تقارير العملاء وسجل المشتريات", 0, 2
        )
        
        # Financial reports
        financial_frame = self._create_report_card(
            reports_frame, "💰 التقارير المالية",
            "الأرباح والخسائر والتدفقات النقدية", 1, 0
        )
        
        # Inventory reports
        inventory_frame = self._create_report_card(
            reports_frame, "📦 تقارير المخزون",
            "حالة المخزون والتنبيهات", 1, 1
        )
        
        # Custom reports
        custom_frame = self._create_report_card(
            reports_frame, "🔧 تقارير مخصصة",
            "إنشاء تقارير مخصصة حسب الحاجة", 1, 2
        )
    
    def _create_report_card(self, parent, title, description, row, column):
        """Create a report card widget"""
        card = ctk.CTkFrame(parent, corner_radius=15)
        card.grid(row=row, column=column, padx=15, pady=15, sticky="nsew")
        
        # Title
        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.pack(pady=(20, 10))
        
        # Description
        desc_label = ctk.CTkLabel(
            card,
            text=description,
            font=ctk.CTkFont(size=12),
            wraplength=200
        )
        desc_label.pack(pady=(0, 20))
        
        # Generate button
        generate_btn = ctk.CTkButton(
            card,
            text="إنشاء التقرير",
            command=lambda t=title: self._generate_report(t),
            width=140
        )
        generate_btn.pack(pady=(0, 20))
        
        return card
    
    def _generate_report(self, report_type):
        """Generate the selected report"""
        messagebox.showinfo("قريباً", f"تقرير {report_type} قيد التطوير")
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reports View
عرض التقارير
"""

import customtkinter as ctk

class ReportsView(ctk.CTkFrame):
    """Reports view"""
    
    def __init__(self, parent, db_manager, theme_manager):
        super().__init__(parent)
        
        self.db_manager = db_manager
        self.theme_manager = theme_manager
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create reports view widgets"""
        title_label = ctk.CTkLabel(
            self,
            text="التقارير والإحصائيات",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(0, 20))
        
        info_label = ctk.CTkLabel(
            self,
            text="صفحة التقارير قيد التطوير...",
            font=ctk.CTkFont(size=16)
        )
        info_label.pack(expand=True)
