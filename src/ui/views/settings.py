
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Settings View
عرض الإعدادات
"""

import customtkinter as ctk
from tkinter import messagebox, filedialog

class SettingsView(ctk.CTkFrame):
    """Application settings view"""
    
    def __init__(self, parent, settings_manager, theme_manager):
        super().__init__(parent, fg_color="transparent")
        
        self.settings_manager = settings_manager
        self.theme_manager = theme_manager
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup settings view UI"""
        colors = self.theme_manager.get_colors()
        
        # Title
        title_label = ctk.CTkLabel(
            self,
            text="⚙️ الإعدادات",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=colors["accent"]
        )
        title_label.pack(pady=(0, 30))
        
        # Settings notebook
        settings_frame = ctk.CTkScrollableFrame(self)
        settings_frame.pack(expand=True, fill="both", padx=20)
        
        # Shop settings section
        self._create_shop_settings(settings_frame)
        
        # Display settings section
        self._create_display_settings(settings_frame)
        
        # Business settings section
        self._create_business_settings(settings_frame)
        
        # Save button
        save_btn = ctk.CTkButton(
            self,
            text="حفظ الإعدادات",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self._save_settings,
            height=40,
            fg_color=colors["success"],
            hover_color="#229954"
        )
        save_btn.pack(pady=20)
    
    def _create_shop_settings(self, parent):
        """Create shop information settings"""
        # Shop settings frame
        shop_frame = ctk.CTkFrame(parent)
        shop_frame.pack(fill="x", pady=(0, 20))
        
        # Title
        ctk.CTkLabel(
            shop_frame,
            text="🏪 معلومات المحل",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(15, 10))
        
        # Settings grid
        grid_frame = ctk.CTkFrame(shop_frame, fg_color="transparent")
        grid_frame.pack(fill="x", padx=20, pady=(0, 15))
        grid_frame.grid_columnconfigure(1, weight=1)
        
        # Shop name
        ctk.CTkLabel(grid_frame, text="اسم المحل:").grid(row=0, column=0, sticky="w", pady=5, padx=(0, 10))
        self.shop_name_entry = ctk.CTkEntry(grid_frame, width=300)
        self.shop_name_entry.grid(row=0, column=1, sticky="ew", pady=5)
        self.shop_name_entry.insert(0, self.settings_manager.shop.name)
        
        # Phone
        ctk.CTkLabel(grid_frame, text="رقم الهاتف:").grid(row=1, column=0, sticky="w", pady=5, padx=(0, 10))
        self.shop_phone_entry = ctk.CTkEntry(grid_frame, width=300)
        self.shop_phone_entry.grid(row=1, column=1, sticky="ew", pady=5)
        self.shop_phone_entry.insert(0, self.settings_manager.shop.phone)
        
        # Address
        ctk.CTkLabel(grid_frame, text="العنوان:").grid(row=2, column=0, sticky="w", pady=5, padx=(0, 10))
        self.shop_address_entry = ctk.CTkEntry(grid_frame, width=300)
        self.shop_address_entry.grid(row=2, column=1, sticky="ew", pady=5)
        self.shop_address_entry.insert(0, self.settings_manager.shop.address)
        
        # Tax number
        ctk.CTkLabel(grid_frame, text="الرقم الضريبي:").grid(row=3, column=0, sticky="w", pady=5, padx=(0, 10))
        self.tax_number_entry = ctk.CTkEntry(grid_frame, width=300)
        self.tax_number_entry.grid(row=3, column=1, sticky="ew", pady=5)
        self.tax_number_entry.insert(0, self.settings_manager.shop.tax_number)
    
    def _create_display_settings(self, parent):
        """Create display settings"""
        display_frame = ctk.CTkFrame(parent)
        display_frame.pack(fill="x", pady=(0, 20))
        
        # Title
        ctk.CTkLabel(
            display_frame,
            text="🎨 إعدادات العرض",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(15, 10))
        
        # Settings grid
        grid_frame = ctk.CTkFrame(display_frame, fg_color="transparent")
        grid_frame.pack(fill="x", padx=20, pady=(0, 15))
        grid_frame.grid_columnconfigure(1, weight=1)
        
        # Theme
        ctk.CTkLabel(grid_frame, text="المظهر:").grid(row=0, column=0, sticky="w", pady=5, padx=(0, 10))
        self.theme_combo = ctk.CTkComboBox(grid_frame, values=["dark", "light"], width=200)
        self.theme_combo.grid(row=0, column=1, sticky="w", pady=5)
        self.theme_combo.set(self.settings_manager.display.theme)
        
        # Language
        ctk.CTkLabel(grid_frame, text="اللغة:").grid(row=1, column=0, sticky="w", pady=5, padx=(0, 10))
        self.language_combo = ctk.CTkComboBox(grid_frame, values=["ar", "en"], width=200)
        self.language_combo.grid(row=1, column=1, sticky="w", pady=5)
        self.language_combo.set(self.settings_manager.display.language)
        
        # Font size
        ctk.CTkLabel(grid_frame, text="حجم الخط:").grid(row=2, column=0, sticky="w", pady=5, padx=(0, 10))
        self.font_size_slider = ctk.CTkSlider(grid_frame, from_=10, to=20, number_of_steps=10)
        self.font_size_slider.grid(row=2, column=1, sticky="w", pady=5)
        self.font_size_slider.set(self.settings_manager.display.font_size)
    
    def _create_business_settings(self, parent):
        """Create business settings"""
        business_frame = ctk.CTkFrame(parent)
        business_frame.pack(fill="x", pady=(0, 20))
        
        # Title
        ctk.CTkLabel(
            business_frame,
            text="💼 الإعدادات التجارية",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(15, 10))
        
        # Settings grid
        grid_frame = ctk.CTkFrame(business_frame, fg_color="transparent")
        grid_frame.pack(fill="x", padx=20, pady=(0, 15))
        grid_frame.grid_columnconfigure(1, weight=1)
        
        # Tax rate
        ctk.CTkLabel(grid_frame, text="معدل الضريبة (%):").grid(row=0, column=0, sticky="w", pady=5, padx=(0, 10))
        self.tax_rate_entry = ctk.CTkEntry(grid_frame, width=100)
        self.tax_rate_entry.grid(row=0, column=1, sticky="w", pady=5)
        self.tax_rate_entry.insert(0, str(self.settings_manager.business.tax_rate))
        
        # Default payment method
        ctk.CTkLabel(grid_frame, text="طريقة الدفع الافتراضية:").grid(row=1, column=0, sticky="w", pady=5, padx=(0, 10))
        self.payment_combo = ctk.CTkComboBox(
            grid_frame, 
            values=["نقد", "بطاقة ائتمان", "تحويل"], 
            width=200
        )
        self.payment_combo.grid(row=1, column=1, sticky="w", pady=5)
        self.payment_combo.set(self.settings_manager.business.default_payment_method)
        
        # Loyalty points
        self.loyalty_switch = ctk.CTkSwitch(grid_frame, text="تفعيل نقاط الولاء")
        self.loyalty_switch.grid(row=2, column=1, sticky="w", pady=5)
        if self.settings_manager.business.enable_loyalty_points:
            self.loyalty_switch.select()
        
        # Auto backup
        self.backup_switch = ctk.CTkSwitch(grid_frame, text="النسخ الاحتياطي التلقائي")
        self.backup_switch.grid(row=3, column=1, sticky="w", pady=5)
        if self.settings_manager.business.auto_backup:
            self.backup_switch.select()
    
    def _save_settings(self):
        """Save all settings"""
        try:
            # Update shop settings
            self.settings_manager.update_shop_settings(
                name=self.shop_name_entry.get(),
                phone=self.shop_phone_entry.get(),
                address=self.shop_address_entry.get(),
                tax_number=self.tax_number_entry.get()
            )
            
            # Update display settings
            self.settings_manager.update_display_settings(
                theme=self.theme_combo.get(),
                language=self.language_combo.get(),
                font_size=int(self.font_size_slider.get())
            )
            
            # Update business settings
            self.settings_manager.update_business_settings(
                tax_rate=float(self.tax_rate_entry.get()),
                default_payment_method=self.payment_combo.get(),
                enable_loyalty_points=self.loyalty_switch.get(),
                auto_backup=self.backup_switch.get()
            )
            
            # Apply theme change if needed
            self.theme_manager.apply_theme()
            
            messagebox.showinfo("نجح", "تم حفظ الإعدادات بنجاح!")
            
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ في حفظ الإعدادات: {e}")
