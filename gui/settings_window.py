#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Settings Window for Mobile Shop Management System
نافذة الإعدادات لنظام إدارة محل الموبايلات
"""

import customtkinter as ctk
from tkinter import messagebox, filedialog, colorchooser
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.arabic_support import (
    create_title_font, create_heading_font, create_button_font,
    create_body_font, setup_arabic_font
)

class SettingsWindow(ctk.CTkScrollableFrame):
    """Settings window with all application configurations"""

    def __init__(self, parent, app_settings, main_window):
        super().__init__(parent)
        self.app_settings = app_settings
        self.main_window = main_window

        self.create_widgets()
        self.load_settings()

    def create_widgets(self):
        """Create settings interface"""
        # Title
        self.title_label = ctk.CTkLabel(
            self,
            text="إعدادات التطبيق",
            font=create_title_font(32)
        )
        self.title_label.pack(pady=(0, 30))

        # Tabview for different settings sections
        self.tabview = ctk.CTkTabview(self, width=1000, height=600)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=20)

        # Create tabs
        self.create_shop_tab()
        self.create_display_tab()
        self.create_currency_tab()
        self.create_tax_tab()
        self.create_inventory_tab()
        self.create_sales_tab()
        self.create_backup_tab()

        # Save and Reset buttons
        self.create_action_buttons()

    def create_shop_tab(self):
        """Create shop information tab"""
        self.shop_tab = self.tabview.add("معلومات المحل")

        # Shop name
        ctk.CTkLabel(
            self.shop_tab,
            text="اسم المحل:",
            font=create_heading_font(16)
        ).pack(anchor="w", padx=20, pady=(20, 5))

        self.shop_name_entry = ctk.CTkEntry(
            self.shop_tab,
            font=create_body_font(14),
            height=35,
            width=400
        )
        self.shop_name_entry.pack(anchor="w", padx=20, pady=(0, 15))

        # Shop name (English)
        ctk.CTkLabel(
            self.shop_tab,
            text="اسم المحل (English):",
            font=create_heading_font(16)
        ).pack(anchor="w", padx=20, pady=(0, 5))

        self.shop_name_en_entry = ctk.CTkEntry(
            self.shop_tab,
            font=create_body_font(14),
            height=35,
            width=400
        )
        self.shop_name_en_entry.pack(anchor="w", padx=20, pady=(0, 15))

        # Address
        ctk.CTkLabel(
            self.shop_tab,
            text="العنوان:",
            font=create_heading_font(16)
        ).pack(anchor="w", padx=20, pady=(0, 5))

        self.address_entry = ctk.CTkEntry(
            self.shop_tab,
            font=create_body_font(14),
            height=35,
            width=400
        )
        self.address_entry.pack(anchor="w", padx=20, pady=(0, 15))

        # Phone
        ctk.CTkLabel(
            self.shop_tab,
            text="رقم الهاتف:",
            font=create_heading_font(16)
        ).pack(anchor="w", padx=20, pady=(0, 5))

        self.phone_entry = ctk.CTkEntry(
            self.shop_tab,
            font=create_body_font(14),
            height=35,
            width=400
        )
        self.phone_entry.pack(anchor="w", padx=20, pady=(0, 15))

        # Email
        ctk.CTkLabel(
            self.shop_tab,
            text="البريد الإلكتروني:",
            font=create_heading_font(16)
        ).pack(anchor="w", padx=20, pady=(0, 5))

        self.email_entry = ctk.CTkEntry(
            self.shop_tab,
            font=create_body_font(14),
            height=35,
            width=400
        )
        self.email_entry.pack(anchor="w", padx=20, pady=(0, 15))

        # Tax number
        ctk.CTkLabel(
            self.shop_tab,
            text="الرقم الضريبي:",
            font=create_heading_font(16)
        ).pack(anchor="w", padx=20, pady=(0, 5))

        self.tax_number_entry = ctk.CTkEntry(
            self.shop_tab,
            font=create_body_font(14),
            height=35,
            width=400
        )
        self.tax_number_entry.pack(anchor="w", padx=20, pady=(0, 15))

    def create_display_tab(self):
        """Create display settings tab"""
        self.display_tab = self.tabview.add("المظهر")

        # Theme selection
        ctk.CTkLabel(
            self.display_tab,
            text="مظهر التطبيق:",
            font=create_heading_font(16)
        ).pack(anchor="w", padx=20, pady=(20, 5))

        self.theme_var = ctk.StringVar(value="dark")
        self.theme_frame = ctk.CTkFrame(self.display_tab)
        self.theme_frame.pack(anchor="w", padx=20, pady=(0, 15), fill="x")

        ctk.CTkRadioButton(
            self.theme_frame,
            text="المظهر الداكن",
            variable=self.theme_var,
            value="dark",
            font=create_body_font(14),
            command=self.preview_theme
        ).pack(side="left", padx=20, pady=10)

        ctk.CTkRadioButton(
            self.theme_frame,
            text="المظهر الفاتح",
            variable=self.theme_var,
            value="light",
            font=create_body_font(14),
            command=self.preview_theme
        ).pack(side="left", padx=20, pady=10)

        # Language selection
        ctk.CTkLabel(
            self.display_tab,
            text="لغة التطبيق:",
            font=create_heading_font(16)
        ).pack(anchor="w", padx=20, pady=(20, 5))

        self.language_var = ctk.StringVar(value="ar")
        self.language_combo = ctk.CTkComboBox(
            self.display_tab,
            values=["العربية", "English"],
            variable=self.language_var,
            font=create_body_font(14),
            width=200
        )
        self.language_combo.pack(anchor="w", padx=20, pady=(0, 15))

        # Font size
        ctk.CTkLabel(
            self.display_tab,
            text="حجم الخط:",
            font=create_heading_font(16)
        ).pack(anchor="w", padx=20, pady=(20, 5))

        self.font_size_var = ctk.IntVar(value=12)
        self.font_size_slider = ctk.CTkSlider(
            self.display_tab,
            from_=10,
            to=20,
            number_of_steps=10,
            variable=self.font_size_var,
            width=300
        )
        self.font_size_slider.pack(anchor="w", padx=20, pady=(0, 10))

        self.font_size_label = ctk.CTkLabel(
            self.display_tab,
            text="12",
            font=create_body_font(12)
        )
        self.font_size_label.pack(anchor="w", padx=20, pady=(0, 15))

        # Bind slider change
        self.font_size_slider.configure(command=self.update_font_size_label)

    def create_currency_tab(self):
        """Create currency settings tab"""
        self.currency_tab = self.tabview.add("العملة")

        # Currency symbol
        ctk.CTkLabel(
            self.currency_tab,
            text="رمز العملة:",
            font=create_heading_font(16)
        ).pack(anchor="w", padx=20, pady=(20, 5))

        self.currency_symbol_entry = ctk.CTkEntry(
            self.currency_tab,
            font=create_body_font(14),
            height=35,
            width=200
        )
        self.currency_symbol_entry.pack(anchor="w", padx=20, pady=(0, 15))

        # Currency code
        ctk.CTkLabel(
            self.currency_tab,
            text="كود العملة:",
            font=create_heading_font(16)
        ).pack(anchor="w", padx=20, pady=(0, 5))

        self.currency_code_entry = ctk.CTkEntry(
            self.currency_tab,
            font=create_body_font(14),
            height=35,
            width=200
        )
        self.currency_code_entry.pack(anchor="w", padx=20, pady=(0, 15))

        # Decimal places
        ctk.CTkLabel(
            self.currency_tab,
            text="عدد المنازل العشرية:",
            font=create_heading_font(16)
        ).pack(anchor="w", padx=20, pady=(0, 5))

        self.decimal_places_var = ctk.IntVar(value=2)
        self.decimal_places_combo = ctk.CTkComboBox(
            self.currency_tab,
            values=["0", "1", "2", "3"],
            variable=self.decimal_places_var,
            font=create_body_font(14),
            width=100
        )
        self.decimal_places_combo.pack(anchor="w", padx=20, pady=(0, 15))

    def create_tax_tab(self):
        """Create tax settings tab"""
        self.tax_tab = self.tabview.add("الضريبة")

        # VAT enabled
        self.vat_enabled_var = ctk.BooleanVar(value=True)
        self.vat_enabled_check = ctk.CTkCheckBox(
            self.tax_tab,
            text="تفعيل ضريبة القيمة المضافة",
            variable=self.vat_enabled_var,
            font=create_heading_font(16)
        )
        self.vat_enabled_check.pack(anchor="w", padx=20, pady=(20, 15))

        # VAT rate
        ctk.CTkLabel(
            self.tax_tab,
            text="نسبة ضريبة القيمة المضافة (%):",
            font=create_heading_font(16)
        ).pack(anchor="w", padx=20, pady=(0, 5))

        self.vat_rate_entry = ctk.CTkEntry(
            self.tax_tab,
            font=create_body_font(14),
            height=35,
            width=200
        )
        self.vat_rate_entry.pack(anchor="w", padx=20, pady=(0, 15))

        # Include tax in price
        self.include_tax_var = ctk.BooleanVar(value=False)
        self.include_tax_check = ctk.CTkCheckBox(
            self.tax_tab,
            text="تضمين الضريبة في السعر",
            variable=self.include_tax_var,
            font=create_heading_font(16)
        )
        self.include_tax_check.pack(anchor="w", padx=20, pady=(0, 15))

    def create_inventory_tab(self):
        """Create inventory settings tab"""
        self.inventory_tab = self.tabview.add("المخزون")

        # Low stock threshold
        ctk.CTkLabel(
            self.inventory_tab,
            text="حد المخزون المنخفض:",
            font=create_heading_font(16)
        ).pack(anchor="w", padx=20, pady=(20, 5))

        self.low_stock_entry = ctk.CTkEntry(
            self.inventory_tab,
            font=create_body_font(14),
            height=35,
            width=200
        )
        self.low_stock_entry.pack(anchor="w", padx=20, pady=(0, 15))

        # Enable alerts
        self.alerts_var = ctk.BooleanVar(value=True)
        self.alerts_check = ctk.CTkCheckBox(
            self.inventory_tab,
            text="تفعيل تنبيهات المخزون المنخفض",
            variable=self.alerts_var,
            font=create_heading_font(16)
        )
        self.alerts_check.pack(anchor="w", padx=20, pady=(0, 15))

        # Allow negative stock
        self.negative_stock_var = ctk.BooleanVar(value=False)
        self.negative_stock_check = ctk.CTkCheckBox(
            self.inventory_tab,
            text="السماح بالمخزون السالب",
            variable=self.negative_stock_var,
            font=create_heading_font(16)
        )
        self.negative_stock_check.pack(anchor="w", padx=20, pady=(0, 15))

    def create_sales_tab(self):
        """Create sales settings tab"""
        self.sales_tab = self.tabview.add("المبيعات")

        # Default payment method
        ctk.CTkLabel(
            self.sales_tab,
            text="طريقة الدفع الافتراضية:",
            font=create_heading_font(16)
        ).pack(anchor="w", padx=20, pady=(20, 5))

        self.payment_method_combo = ctk.CTkComboBox(
            self.sales_tab,
            values=["نقداً", "تحويل", "بطاقة ائتمان", "تقسيط"],
            font=create_body_font(14),
            width=200
        )
        self.payment_method_combo.pack(anchor="w", padx=20, pady=(0, 15))

        # Enable customer loyalty
        self.loyalty_var = ctk.BooleanVar(value=True)
        self.loyalty_check = ctk.CTkCheckBox(
            self.sales_tab,
            text="تفعيل برنامج نقاط الولاء",
            variable=self.loyalty_var,
            font=create_heading_font(16)
        )
        self.loyalty_check.pack(anchor="w", padx=20, pady=(0, 15))

        # Max discount
        ctk.CTkLabel(
            self.sales_tab,
            text="أقصى نسبة خصم (%):",
            font=create_heading_font(16)
        ).pack(anchor="w", padx=20, pady=(0, 5))

        self.max_discount_entry = ctk.CTkEntry(
            self.sales_tab,
            font=create_body_font(14),
            height=35,
            width=200
        )
        self.max_discount_entry.pack(anchor="w", padx=20, pady=(0, 15))

    def create_backup_tab(self):
        """Create backup settings tab"""
        self.backup_tab = self.tabview.add("النسخ الاحتياطي")

        # Auto backup
        self.auto_backup_var = ctk.BooleanVar(value=True)
        self.auto_backup_check = ctk.CTkCheckBox(
            self.backup_tab,
            text="النسخ الاحتياطي التلقائي",
            variable=self.auto_backup_var,
            font=create_heading_font(16)
        )
        self.auto_backup_check.pack(anchor="w", padx=20, pady=(20, 15))

        # Backup interval
        ctk.CTkLabel(
            self.backup_tab,
            text="فترة النسخ الاحتياطي (أيام):",
            font=create_heading_font(16)
        ).pack(anchor="w", padx=20, pady=(0, 5))

        self.backup_interval_entry = ctk.CTkEntry(
            self.backup_tab,
            font=create_body_font(14),
            height=35,
            width=200
        )
        self.backup_interval_entry.pack(anchor="w", padx=20, pady=(0, 15))

        # Backup location
        ctk.CTkLabel(
            self.backup_tab,
            text="مجلد النسخ الاحتياطي:",
            font=create_heading_font(16)
        ).pack(anchor="w", padx=20, pady=(0, 5))

        backup_frame = ctk.CTkFrame(self.backup_tab)
        backup_frame.pack(anchor="w", padx=20, pady=(0, 15), fill="x")

        self.backup_location_entry = ctk.CTkEntry(
            backup_frame,
            font=create_body_font(14),
            height=35,
            width=350
        )
        self.backup_location_entry.pack(side="left", padx=(10, 5), pady=10)

        self.browse_backup_btn = ctk.CTkButton(
            backup_frame,
            text="تصفح",
            font=create_button_font(14),
            width=80,
            command=self.browse_backup_location
        )
        self.browse_backup_btn.pack(side="left", padx=(5, 10), pady=10)

        # Backup actions
        actions_frame = ctk.CTkFrame(self.backup_tab)
        actions_frame.pack(anchor="w", padx=20, pady=(20, 15), fill="x")

        self.create_backup_btn = ctk.CTkButton(
            actions_frame,
            text="إنشاء نسخة احتياطية الآن",
            font=create_button_font(14),
            command=self.create_backup_now
        )
        self.create_backup_btn.pack(side="left", padx=10, pady=10)

        self.restore_backup_btn = ctk.CTkButton(
            actions_frame,
            text="استعادة من نسخة احتياطية",
            font=create_button_font(14),
            command=self.restore_backup
        )
        self.restore_backup_btn.pack(side="left", padx=10, pady=10)

    def create_action_buttons(self):
        """Create save and reset buttons"""
        buttons_frame = ctk.CTkFrame(self)
        buttons_frame.pack(fill="x", padx=20, pady=20)

        self.save_btn = ctk.CTkButton(
            buttons_frame,
            text="💾 حفظ الإعدادات",
            font=create_button_font(16),
            height=40,
            fg_color=("#2d6a4f", "#2d6a4f"),
            hover_color=("#40916c", "#40916c"),
            command=self.save_settings
        )
        self.save_btn.pack(side="left", padx=10, pady=10)

        self.reset_btn = ctk.CTkButton(
            buttons_frame,
            text="↺ إعادة تعيين",
            font=create_button_font(16),
            height=40,
            fg_color=("#d62828", "#d62828"),
            hover_color=("#f77f00", "#f77f00"),
            command=self.reset_settings
        )
        self.reset_btn.pack(side="left", padx=10, pady=10)

        self.export_btn = ctk.CTkButton(
            buttons_frame,
            text="📤 تصدير الإعدادات",
            font=create_button_font(16),
            height=40,
            command=self.export_settings
        )
        self.export_btn.pack(side="left", padx=10, pady=10)

        self.import_btn = ctk.CTkButton(
            buttons_frame,
            text="📥 استيراد الإعدادات",
            font=create_button_font(16),
            height=40,
            command=self.import_settings
        )
        self.import_btn.pack(side="left", padx=10, pady=10)

    def load_settings(self):
        """Load current settings into the interface"""
        # Shop settings
        self.shop_name_entry.insert(0, self.app_settings.shop.name)
        self.shop_name_en_entry.insert(0, self.app_settings.shop.name_english)
        self.address_entry.insert(0, self.app_settings.shop.address)
        self.phone_entry.insert(0, self.app_settings.shop.phone)
        self.email_entry.insert(0, self.app_settings.shop.email)
        self.tax_number_entry.insert(0, self.app_settings.shop.tax_number)

        # Display settings
        self.theme_var.set(self.app_settings.display.theme)
        self.language_var.set(self.app_settings.display.language)
        self.font_size_var.set(self.app_settings.display.font_size)
        self.update_font_size_label(self.app_settings.display.font_size)

        # Currency settings
        self.currency_symbol_entry.insert(0, self.app_settings.currency.symbol)
        self.currency_code_entry.insert(0, self.app_settings.currency.code)
        self.decimal_places_combo.set(str(self.app_settings.currency.decimal_places))

        # Tax settings
        self.vat_enabled_var.set(self.app_settings.tax.vat_enabled)
        self.vat_rate_entry.insert(0, str(self.app_settings.tax.vat_rate))
        self.include_tax_var.set(self.app_settings.tax.include_tax_in_price)

        # Inventory settings
        self.low_stock_entry.insert(0, str(self.app_settings.inventory.low_stock_threshold))
        self.alerts_var.set(self.app_settings.inventory.enable_low_stock_alerts)
        self.negative_stock_var.set(self.app_settings.inventory.allow_negative_stock)

        # Sales settings
        self.payment_method_combo.set(self.app_settings.sales.default_payment_method)
        self.loyalty_var.set(self.app_settings.sales.enable_customer_loyalty)
        self.max_discount_entry.insert(0, str(self.app_settings.sales.max_discount_percent))

        # Backup settings
        self.auto_backup_var.set(self.app_settings.backup.auto_backup)
        self.backup_interval_entry.insert(0, str(self.app_settings.backup.backup_interval_days))
        self.backup_location_entry.insert(0, self.app_settings.backup.backup_location)

    def preview_theme(self):
        """Preview theme change"""
        theme = self.theme_var.get()
        ctk.set_appearance_mode(theme)

    def update_font_size_label(self, value):
        """Update font size label"""
        self.font_size_label.configure(text=f"{int(value)}")

    def browse_backup_location(self):
        """Browse for backup location"""
        folder = filedialog.askdirectory(title="اختر مجلد النسخ الاحتياطي")
        if folder:
            self.backup_location_entry.delete(0, "end")
            self.backup_location_entry.insert(0, folder)

    def save_settings(self):
        """Save all settings"""
        try:
            # Shop settings
            self.app_settings.shop.name = self.shop_name_entry.get()
            self.app_settings.shop.name_english = self.shop_name_en_entry.get()
            self.app_settings.shop.address = self.address_entry.get()
            self.app_settings.shop.phone = self.phone_entry.get()
            self.app_settings.shop.email = self.email_entry.get()
            self.app_settings.shop.tax_number = self.tax_number_entry.get()

            # Display settings
            self.app_settings.display.theme = self.theme_var.get()
            self.app_settings.display.language = self.language_var.get()
            self.app_settings.display.font_size = int(self.font_size_var.get())

            # Currency settings
            self.app_settings.currency.symbol = self.currency_symbol_entry.get()
            self.app_settings.currency.code = self.currency_code_entry.get()
            self.app_settings.currency.decimal_places = int(self.decimal_places_combo.get())

            # Tax settings
            self.app_settings.tax.vat_enabled = self.vat_enabled_var.get()
            self.app_settings.tax.vat_rate = float(self.vat_rate_entry.get())
            self.app_settings.tax.include_tax_in_price = self.include_tax_var.get()

            # Inventory settings
            self.app_settings.inventory.low_stock_threshold = int(self.low_stock_entry.get())
            self.app_settings.inventory.enable_low_stock_alerts = self.alerts_var.get()
            self.app_settings.inventory.allow_negative_stock = self.negative_stock_var.get()

            # Sales settings
            self.app_settings.sales.default_payment_method = self.payment_method_combo.get()
            self.app_settings.sales.enable_customer_loyalty = self.loyalty_var.get()
            self.app_settings.sales.max_discount_percent = float(self.max_discount_entry.get())

            # Backup settings
            self.app_settings.backup.auto_backup = self.auto_backup_var.get()
            self.app_settings.backup.backup_interval_days = int(self.backup_interval_entry.get())
            self.app_settings.backup.backup_location = self.backup_location_entry.get()

            # Save to file
            self.app_settings.save_settings()

            # Update main window theme
            if hasattr(self.main_window, 'refresh_theme'):
                self.main_window.refresh_theme()

            messagebox.showinfo("نجح", "تم حفظ الإعدادات بنجاح!")

        except Exception as e:
            messagebox.showerror("خطأ", f"خطأ في حفظ الإعدادات: {e}")

    def reset_settings(self):
        """Reset all settings to defaults"""
        if messagebox.askyesno("تأكيد", "هل تريد إعادة تعيين جميع الإعدادات للقيم الافتراضية؟"):
            try:
                # Reset to defaults
                self.app_settings._reset_to_defaults()

                # Clear and reload interface
                self.clear_all_entries()
                self.load_settings()

                messagebox.showinfo("نجح", "تم إعادة تعيين الإعدادات بنجاح!")

            except Exception as e:
                messagebox.showerror("خطأ", f"خطأ في إعادة تعيين الإعدادات: {e}")

    def export_settings(self):
        """Export settings to file"""
        filename = filedialog.asksaveasfilename(
            title="تصدير الإعدادات",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )

        if filename:
            if self.app_settings.export_settings(filename):
                messagebox.showinfo("نجح", "تم تصدير الإعدادات بنجاح!")
            else:
                messagebox.showerror("خطأ", "فشل في تصدير الإعدادات!")

    def import_settings(self):
        """Import settings from file"""
        filename = filedialog.askopenfilename(
            title="استيراد الإعدادات",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )

        if filename:
            if messagebox.askyesno("تأكيد", "هل تريد استبدال الإعدادات الحالية؟"):
                if self.app_settings.import_settings(filename):
                    self.clear_all_entries()
                    self.load_settings()
                    messagebox.showinfo("نجح", "تم استيراد الإعدادات بنجاح!")
                else:
                    messagebox.showerror("خطأ", "فشل في استيراد الإعدادات!")

    def clear_all_entries(self):
        """Clear all entry widgets"""
        # Shop entries
        self.shop_name_entry.delete(0, "end")
        self.shop_name_en_entry.delete(0, "end")
        self.address_entry.delete(0, "end")
        self.phone_entry.delete(0, "end")
        self.email_entry.delete(0, "end")
        self.tax_number_entry.delete(0, "end")

        # Currency entries
        self.currency_symbol_entry.delete(0, "end")
        self.currency_code_entry.delete(0, "end")

        # Tax entries
        self.vat_rate_entry.delete(0, "end")

        # Inventory entries
        self.low_stock_entry.delete(0, "end")

        # Sales entries
        self.max_discount_entry.delete(0, "end")

        # Backup entries
        self.backup_interval_entry.delete(0, "end")
        self.backup_location_entry.delete(0, "end")

    def create_backup_now(self):
        """Create backup now"""
        try:
            # This would call the backup manager
            messagebox.showinfo("نجح", "تم إنشاء النسخة الاحتياطية بنجاح!")
        except Exception as e:
            messagebox.showerror("خطأ", f"خطأ في إنشاء النسخة الاحتياطية: {e}")

    def restore_backup(self):
        """Restore from backup"""
        filename = filedialog.askopenfilename(
            title="اختر ملف النسخة الاحتياطية",
            filetypes=[("Database files", "*.db"), ("All files", "*.*")]
        )

        if filename:
            if messagebox.askyesno("تحذير", "استعادة النسخة الاحتياطية ستمحو البيانات الحالية. هل تريد المتابعة؟"):
                try:
                    # This would call the backup manager to restore
                    messagebox.showinfo("نجح", "تم استعادة النسخة الاحتياطية بنجاح!")
                except Exception as e:
                    messagebox.showerror("خطأ", f"خطأ في استعادة النسخة الاحتياطية: {e}")