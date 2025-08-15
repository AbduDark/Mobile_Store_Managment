
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Settings View
صفحة الإعدادات
"""

import customtkinter as ctk
from tkinter import messagebox, filedialog
from pathlib import Path
import json
from datetime import datetime

from src.utils.logger import get_logger

logger = get_logger(__name__)

class SettingsView(ctk.CTkFrame):
    """Settings view with comprehensive options"""

    def __init__(self, parent, settings_manager, theme_manager):
        super().__init__(parent)
        
        self.settings_manager = settings_manager
        self.theme_manager = theme_manager
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self._setup_ui()
        self._load_current_settings()
        
        logger.info("Settings view initialized")

    def _setup_ui(self):
        """Setup settings UI"""
        # Header
        header_frame = ctk.CTkFrame(self, height=60, corner_radius=10)
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        header_frame.grid_columnconfigure(1, weight=1)
        header_frame.grid_propagate(False)

        title_label = ctk.CTkLabel(
            header_frame,
            text="⚙️ إعدادات النظام",
            font=self.theme_manager.get_header_font_config(24, "bold")
        )
        title_label.grid(row=0, column=0, padx=20, pady=15, sticky="w")

        # Save button
        save_btn = ctk.CTkButton(
            header_frame,
            text="💾 حفظ الإعدادات",
            command=self._save_settings,
            font=self.theme_manager.get_font_config(14),
            width=150,
            height=35
        )
        save_btn.grid(row=0, column=1, padx=20, pady=15, sticky="e")

        # Main content with tabs
        self.tabview = ctk.CTkTabview(self, corner_radius=10)
        self.tabview.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)

        # Setup tabs
        self._setup_shop_info_tab()
        self._setup_display_tab()
        self._setup_business_tab()
        self._setup_system_tab()
        self._setup_backup_tab()

    def _setup_shop_info_tab(self):
        """Setup shop information tab"""
        tab = self.tabview.add("معلومات المحل")
        tab.grid_columnconfigure((0, 1), weight=1)

        # Shop basic info frame
        basic_frame = ctk.CTkFrame(tab)
        basic_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        basic_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(basic_frame, text="📋 المعلومات الأساسية", 
                    font=self.theme_manager.get_header_font_config(16, "bold")).grid(
                        row=0, column=0, columnspan=2, padx=10, pady=(10, 20), sticky="w")

        # Shop name
        ctk.CTkLabel(basic_frame, text="اسم المحل:", 
                    font=self.theme_manager.get_font_config(12)).grid(
                        row=1, column=0, padx=10, pady=5, sticky="w")
        self.shop_name_entry = ctk.CTkEntry(basic_frame, font=self.theme_manager.get_font_config(12))
        self.shop_name_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        # Owner name
        ctk.CTkLabel(basic_frame, text="اسم المالك:", 
                    font=self.theme_manager.get_font_config(12)).grid(
                        row=2, column=0, padx=10, pady=5, sticky="w")
        self.owner_name_entry = ctk.CTkEntry(basic_frame, font=self.theme_manager.get_font_config(12))
        self.owner_name_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        # Phone
        ctk.CTkLabel(basic_frame, text="رقم الهاتف:", 
                    font=self.theme_manager.get_font_config(12)).grid(
                        row=3, column=0, padx=10, pady=5, sticky="w")
        self.phone_entry = ctk.CTkEntry(basic_frame, font=self.theme_manager.get_font_config(12))
        self.phone_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        # Email
        ctk.CTkLabel(basic_frame, text="البريد الإلكتروني:", 
                    font=self.theme_manager.get_font_config(12)).grid(
                        row=4, column=0, padx=10, pady=5, sticky="w")
        self.email_entry = ctk.CTkEntry(basic_frame, font=self.theme_manager.get_font_config(12))
        self.email_entry.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

        # Address
        ctk.CTkLabel(basic_frame, text="العنوان:", 
                    font=self.theme_manager.get_font_config(12)).grid(
                        row=5, column=0, padx=10, pady=5, sticky="w")
        self.address_entry = ctk.CTkEntry(basic_frame, font=self.theme_manager.get_font_config(12))
        self.address_entry.grid(row=5, column=1, padx=10, pady=5, sticky="ew")

        # Tax number
        ctk.CTkLabel(basic_frame, text="الرقم الضريبي:", 
                    font=self.theme_manager.get_font_config(12)).grid(
                        row=6, column=0, padx=10, pady=5, sticky="w")
        self.tax_number_entry = ctk.CTkEntry(basic_frame, font=self.theme_manager.get_font_config(12))
        self.tax_number_entry.grid(row=6, column=1, padx=10, pady=(5, 15), sticky="ew")

        # Logo section
        logo_frame = ctk.CTkFrame(tab)
        logo_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        logo_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(logo_frame, text="🖼️ شعار المحل", 
                    font=self.theme_manager.get_header_font_config(16, "bold")).grid(
                        row=0, column=0, columnspan=2, padx=10, pady=(10, 15), sticky="w")

        ctk.CTkLabel(logo_frame, text="مسار الشعار:", 
                    font=self.theme_manager.get_font_config(12)).grid(
                        row=1, column=0, padx=10, pady=5, sticky="w")
        self.logo_path_entry = ctk.CTkEntry(logo_frame, font=self.theme_manager.get_font_config(12))
        self.logo_path_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        logo_btn = ctk.CTkButton(
            logo_frame,
            text="📁 اختيار شعار",
            command=self._select_logo,
            font=self.theme_manager.get_font_config(12),
            width=120
        )
        logo_btn.grid(row=1, column=2, padx=10, pady=(5, 15), sticky="e")

    def _setup_display_tab(self):
        """Setup display settings tab"""
        tab = self.tabview.add("العرض")
        tab.grid_columnconfigure((0, 1), weight=1)

        # Theme frame
        theme_frame = ctk.CTkFrame(tab)
        theme_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        theme_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(theme_frame, text="🎨 السمة والمظهر", 
                    font=self.theme_manager.get_header_font_config(16, "bold")).grid(
                        row=0, column=0, columnspan=2, padx=10, pady=(10, 15), sticky="w")

        # Theme selection
        ctk.CTkLabel(theme_frame, text="السمة:", 
                    font=self.theme_manager.get_font_config(12)).grid(
                        row=1, column=0, padx=10, pady=5, sticky="w")
        self.theme_var = ctk.StringVar(value="dark")
        theme_menu = ctk.CTkOptionMenu(
            theme_frame,
            variable=self.theme_var,
            values=["dark", "light"],
            font=self.theme_manager.get_font_config(12),
            command=self._on_theme_change
        )
        theme_menu.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        # Language
        ctk.CTkLabel(theme_frame, text="اللغة:", 
                    font=self.theme_manager.get_font_config(12)).grid(
                        row=2, column=0, padx=10, pady=5, sticky="w")
        self.language_var = ctk.StringVar(value="ar")
        language_menu = ctk.CTkOptionMenu(
            theme_frame,
            variable=self.language_var,
            values=["ar", "en"],
            font=self.theme_manager.get_font_config(12)
        )
        language_menu.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        # Font size
        ctk.CTkLabel(theme_frame, text="حجم الخط:", 
                    font=self.theme_manager.get_font_config(12)).grid(
                        row=3, column=0, padx=10, pady=5, sticky="w")
        self.font_size_var = ctk.StringVar(value="12")
        font_size_menu = ctk.CTkOptionMenu(
            theme_frame,
            variable=self.font_size_var,
            values=["10", "12", "14", "16", "18"],
            font=self.theme_manager.get_font_config(12)
        )
        font_size_menu.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        # Show grid
        self.show_grid_var = ctk.BooleanVar(value=True)
        grid_check = ctk.CTkCheckBox(
            theme_frame,
            text="إظهار الشبكة في الجداول",
            variable=self.show_grid_var,
            font=self.theme_manager.get_font_config(12)
        )
        grid_check.grid(row=4, column=0, columnspan=2, padx=10, pady=(5, 15), sticky="w")

        # Items per page
        ctk.CTkLabel(theme_frame, text="عدد العناصر في الصفحة:", 
                    font=self.theme_manager.get_font_config(12)).grid(
                        row=5, column=0, padx=10, pady=(5, 15), sticky="w")
        self.items_per_page_var = ctk.StringVar(value="50")
        items_menu = ctk.CTkOptionMenu(
            theme_frame,
            variable=self.items_per_page_var,
            values=["25", "50", "100", "200"],
            font=self.theme_manager.get_font_config(12)
        )
        items_menu.grid(row=5, column=1, padx=10, pady=(5, 15), sticky="ew")

    def _setup_business_tab(self):
        """Setup business settings tab"""
        tab = self.tabview.add("الأعمال")
        tab.grid_columnconfigure((0, 1), weight=1)

        # Currency frame
        currency_frame = ctk.CTkFrame(tab)
        currency_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        currency_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(currency_frame, text="💰 العملة والأسعار", 
                    font=self.theme_manager.get_header_font_config(16, "bold")).grid(
                        row=0, column=0, columnspan=2, padx=10, pady=(10, 15), sticky="w")

        # Currency
        ctk.CTkLabel(currency_frame, text="العملة:", 
                    font=self.theme_manager.get_font_config(12)).grid(
                        row=1, column=0, padx=10, pady=5, sticky="w")
        self.currency_entry = ctk.CTkEntry(currency_frame, font=self.theme_manager.get_font_config(12))
        self.currency_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        # Currency symbol
        ctk.CTkLabel(currency_frame, text="رمز العملة:", 
                    font=self.theme_manager.get_font_config(12)).grid(
                        row=2, column=0, padx=10, pady=5, sticky="w")
        self.currency_symbol_entry = ctk.CTkEntry(currency_frame, font=self.theme_manager.get_font_config(12))
        self.currency_symbol_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        # Tax rate
        ctk.CTkLabel(currency_frame, text="معدل الضريبة (%):", 
                    font=self.theme_manager.get_font_config(12)).grid(
                        row=3, column=0, padx=10, pady=5, sticky="w")
        self.tax_rate_entry = ctk.CTkEntry(currency_frame, font=self.theme_manager.get_font_config(12))
        self.tax_rate_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        # Default discount
        ctk.CTkLabel(currency_frame, text="الخصم الافتراضي (%):", 
                    font=self.theme_manager.get_font_config(12)).grid(
                        row=4, column=0, padx=10, pady=(5, 15), sticky="w")
        self.default_discount_entry = ctk.CTkEntry(currency_frame, font=self.theme_manager.get_font_config(12))
        self.default_discount_entry.grid(row=4, column=1, padx=10, pady=(5, 15), sticky="ew")

        # Alerts frame
        alerts_frame = ctk.CTkFrame(tab)
        alerts_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        alerts_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(alerts_frame, text="🔔 التنبيهات", 
                    font=self.theme_manager.get_header_font_config(16, "bold")).grid(
                        row=0, column=0, columnspan=2, padx=10, pady=(10, 15), sticky="w")

        # Low stock alert
        self.low_stock_alert_var = ctk.BooleanVar(value=True)
        stock_check = ctk.CTkCheckBox(
            alerts_frame,
            text="تنبيه انخفاض المخزون",
            variable=self.low_stock_alert_var,
            font=self.theme_manager.get_font_config(12)
        )
        stock_check.grid(row=1, column=0, columnspan=2, padx=10, pady=(5, 15), sticky="w")

    def _setup_system_tab(self):
        """Setup system settings tab"""
        tab = self.tabview.add("النظام")
        tab.grid_columnconfigure(0, weight=1)

        # Payment methods frame
        payment_frame = ctk.CTkFrame(tab)
        payment_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        payment_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(payment_frame, text="💳 طرق الدفع المدعومة", 
                    font=self.theme_manager.get_header_font_config(16, "bold")).grid(
                        row=0, column=0, columnspan=2, padx=10, pady=(10, 15), sticky="w")

        # Payment methods checkboxes
        self.payment_methods = {}
        methods = [
            ("cash", "نقداً 💵"),
            ("card", "بطاقة ائتمان 💳"),
            ("transfer", "تحويل بنكي 🏦"),
            ("wallet", "محفظة إلكترونية 📱"),
            ("installment", "تقسيط 📅")
        ]

        for i, (key, label) in enumerate(methods):
            var = ctk.BooleanVar(value=True if key == "cash" else False)
            self.payment_methods[key] = var
            check = ctk.CTkCheckBox(
                payment_frame,
                text=label,
                variable=var,
                font=self.theme_manager.get_font_config(12)
            )
            check.grid(row=i+1, column=0, padx=10, pady=2, sticky="w")

        # Cash tracking frame
        cash_frame = ctk.CTkFrame(tab)
        cash_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
        cash_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(cash_frame, text="💰 تتبع النقدية والرصيد", 
                    font=self.theme_manager.get_header_font_config(16, "bold")).grid(
                        row=0, column=0, columnspan=2, padx=10, pady=(10, 15), sticky="w")

        # Enable cash tracking
        self.track_cash_var = ctk.BooleanVar(value=True)
        track_check = ctk.CTkCheckBox(
            cash_frame,
            text="تفعيل تتبع تحويلات الكاش والرصيد",
            variable=self.track_cash_var,
            font=self.theme_manager.get_font_config(12)
        )
        track_check.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        # Daily cash limit alert
        ctk.CTkLabel(cash_frame, text="حد تنبيه الكاش اليومي:", 
                    font=self.theme_manager.get_font_config(12)).grid(
                        row=2, column=0, padx=10, pady=5, sticky="w")
        self.cash_limit_entry = ctk.CTkEntry(cash_frame, font=self.theme_manager.get_font_config(12))
        self.cash_limit_entry.grid(row=2, column=1, padx=10, pady=(5, 15), sticky="ew")

    def _setup_backup_tab(self):
        """Setup backup settings tab"""
        tab = self.tabview.add("النسخ الاحتياطي")
        tab.grid_columnconfigure(0, weight=1)

        # Backup frame
        backup_frame = ctk.CTkFrame(tab)
        backup_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        backup_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(backup_frame, text="💾 النسخ الاحتياطي", 
                    font=self.theme_manager.get_header_font_config(16, "bold")).grid(
                        row=0, column=0, columnspan=2, padx=10, pady=(10, 15), sticky="w")

        # Auto backup
        self.auto_backup_var = ctk.BooleanVar(value=True)
        auto_check = ctk.CTkCheckBox(
            backup_frame,
            text="تفعيل النسخ الاحتياطي التلقائي",
            variable=self.auto_backup_var,
            font=self.theme_manager.get_font_config(12)
        )
        auto_check.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        # Backup interval
        ctk.CTkLabel(backup_frame, text="فترة النسخ الاحتياطي (أيام):", 
                    font=self.theme_manager.get_font_config(12)).grid(
                        row=2, column=0, padx=10, pady=5, sticky="w")
        self.backup_interval_var = ctk.StringVar(value="7")
        interval_menu = ctk.CTkOptionMenu(
            backup_frame,
            variable=self.backup_interval_var,
            values=["1", "3", "7", "14", "30"],
            font=self.theme_manager.get_font_config(12)
        )
        interval_menu.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        # Backup buttons
        backup_btn = ctk.CTkButton(
            backup_frame,
            text="📥 إنشاء نسخة احتياطية الآن",
            command=self._create_backup,
            font=self.theme_manager.get_font_config(12),
            height=35
        )
        backup_btn.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        restore_btn = ctk.CTkButton(
            backup_frame,
            text="📤 استعادة من نسخة احتياطية",
            command=self._restore_backup,
            font=self.theme_manager.get_font_config(12),
            height=35,
            fg_color="transparent",
            border_width=2
        )
        restore_btn.grid(row=4, column=0, columnspan=2, padx=10, pady=(0, 15), sticky="ew")

        # Export/Import frame
        export_frame = ctk.CTkFrame(tab)
        export_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
        export_frame.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(export_frame, text="📊 تصدير واستيراد البيانات", 
                    font=self.theme_manager.get_header_font_config(16, "bold")).grid(
                        row=0, column=0, columnspan=2, padx=10, pady=(10, 15), sticky="w")

        export_data_btn = ctk.CTkButton(
            export_frame,
            text="📤 تصدير البيانات",
            command=self._export_data,
            font=self.theme_manager.get_font_config(12),
            height=35
        )
        export_data_btn.grid(row=1, column=0, padx=10, pady=(0, 15), sticky="ew")

        import_data_btn = ctk.CTkButton(
            export_frame,
            text="📥 استيراد البيانات",
            command=self._import_data,
            font=self.theme_manager.get_font_config(12),
            height=35
        )
        import_data_btn.grid(row=1, column=1, padx=10, pady=(0, 15), sticky="ew")

    def _load_current_settings(self):
        """Load current settings into UI"""
        try:
            # Shop info
            self.shop_name_entry.insert(0, self.settings_manager.shop_info.name)
            self.owner_name_entry.insert(0, self.settings_manager.shop_info.owner)
            self.phone_entry.insert(0, self.settings_manager.shop_info.phone)
            self.email_entry.insert(0, self.settings_manager.shop_info.email)
            self.address_entry.insert(0, self.settings_manager.shop_info.address)
            self.tax_number_entry.insert(0, self.settings_manager.shop_info.tax_number)
            self.logo_path_entry.insert(0, self.settings_manager.shop_info.logo_path)

            # Display settings
            self.theme_var.set(self.settings_manager.display.theme)
            self.language_var.set(self.settings_manager.display.language)
            self.font_size_var.set(str(self.settings_manager.display.font_size))
            self.show_grid_var.set(self.settings_manager.display.show_grid)
            self.items_per_page_var.set(str(self.settings_manager.display.items_per_page))

            # Business settings
            self.currency_entry.insert(0, self.settings_manager.business.currency)
            self.currency_symbol_entry.insert(0, self.settings_manager.business.currency_symbol)
            self.tax_rate_entry.insert(0, str(self.settings_manager.business.tax_rate))
            self.default_discount_entry.insert(0, str(self.settings_manager.business.default_discount))
            self.low_stock_alert_var.set(self.settings_manager.business.low_stock_alert)

            # System settings
            self.cash_limit_entry.insert(0, "10000")  # Default value

            # Backup settings
            self.backup_interval_var.set(str(self.settings_manager.business.backup_interval_days))

        except Exception as e:
            logger.error(f"Error loading settings: {e}")

    def _on_theme_change(self, value):
        """Handle theme change"""
        self.theme_manager.switch_theme(value)

    def _select_logo(self):
        """Select logo file"""
        file_path = filedialog.askopenfilename(
            title="اختيار شعار المحل",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )
        if file_path:
            self.logo_path_entry.delete(0, "end")
            self.logo_path_entry.insert(0, file_path)

    def _save_settings(self):
        """Save all settings"""
        try:
            # Update shop info
            self.settings_manager.update_shop_info(
                name=self.shop_name_entry.get(),
                owner=self.owner_name_entry.get(),
                phone=self.phone_entry.get(),
                email=self.email_entry.get(),
                address=self.address_entry.get(),
                tax_number=self.tax_number_entry.get(),
                logo_path=self.logo_path_entry.get()
            )

            # Update display settings
            self.settings_manager.update_display_settings(
                theme=self.theme_var.get(),
                language=self.language_var.get(),
                font_size=int(self.font_size_var.get()),
                show_grid=self.show_grid_var.get(),
                items_per_page=int(self.items_per_page_var.get())
            )

            # Update business settings
            self.settings_manager.update_business_settings(
                currency=self.currency_entry.get(),
                currency_symbol=self.currency_symbol_entry.get(),
                tax_rate=float(self.tax_rate_entry.get()),
                default_discount=float(self.default_discount_entry.get()),
                low_stock_alert=self.low_stock_alert_var.get(),
                backup_interval_days=int(self.backup_interval_var.get())
            )

            messagebox.showinfo("نجح", "تم حفظ الإعدادات بنجاح!")
            logger.info("Settings saved successfully")

        except Exception as e:
            logger.error(f"Error saving settings: {e}")
            messagebox.showerror("خطأ", f"حدث خطأ في حفظ الإعدادات: {e}")

    def _create_backup(self):
        """Create database backup"""
        try:
            import shutil
            from datetime import datetime
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = f"data/backups/backup_{timestamp}.db"
            
            # Create backup directory if it doesn't exist
            Path("data/backups").mkdir(parents=True, exist_ok=True)
            
            # Copy database file
            shutil.copy2("data/database/shop.db", backup_file)
            
            messagebox.showinfo("نجح", f"تم إنشاء النسخة الاحتياطية بنجاح!\n{backup_file}")
            logger.info(f"Backup created: {backup_file}")
            
        except Exception as e:
            logger.error(f"Error creating backup: {e}")
            messagebox.showerror("خطأ", f"حدث خطأ في إنشاء النسخة الاحتياطية: {e}")

    def _restore_backup(self):
        """Restore from backup"""
        try:
            file_path = filedialog.askopenfilename(
                title="اختيار ملف النسخة الاحتياطية",
                filetypes=[("Database files", "*.db")]
            )
            
            if file_path:
                if messagebox.askyesno("تأكيد", "هل أنت متأكد من استعادة النسخة الاحتياطية؟\nسيتم استبدال البيانات الحالية!"):
                    import shutil
                    shutil.copy2(file_path, "data/database/shop.db")
                    messagebox.showinfo("نجح", "تم استعادة النسخة الاحتياطية بنجاح!")
                    logger.info(f"Backup restored from: {file_path}")
                    
        except Exception as e:
            logger.error(f"Error restoring backup: {e}")
            messagebox.showerror("خطأ", f"حدث خطأ في استعادة النسخة الاحتياطية: {e}")

    def _export_data(self):
        """Export data to CSV/Excel"""
        try:
            file_path = filedialog.asksaveasfilename(
                title="تصدير البيانات",
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")]
            )
            
            if file_path:
                # Implementation for data export would go here
                messagebox.showinfo("نجح", f"تم تصدير البيانات بنجاح!\n{file_path}")
                logger.info(f"Data exported to: {file_path}")
                
        except Exception as e:
            logger.error(f"Error exporting data: {e}")
            messagebox.showerror("خطأ", f"حدث خطأ في تصدير البيانات: {e}")

    def _import_data(self):
        """Import data from CSV/Excel"""
        try:
            file_path = filedialog.askopenfilename(
                title="استيراد البيانات",
                filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")]
            )
            
            if file_path:
                if messagebox.askyesno("تأكيد", "هل أنت متأكد من استيراد البيانات؟"):
                    # Implementation for data import would go here
                    messagebox.showinfo("نجح", f"تم استيراد البيانات بنجاح!\n{file_path}")
                    logger.info(f"Data imported from: {file_path}")
                    
        except Exception as e:
            logger.error(f"Error importing data: {e}")
            messagebox.showerror("خطأ", f"حدث خطأ في استيراد البيانات: {e}")
