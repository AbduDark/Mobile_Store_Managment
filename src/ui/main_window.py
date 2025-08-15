#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main Application Window
النافذة الرئيسية للتطبيق
"""

import customtkinter as ctk
from tkinter import messagebox
import sys
from pathlib import Path

from src.ui.components.sidebar import Sidebar
from src.ui.components.header import HeaderBar
from src.ui.views.dashboard import DashboardView
from src.ui.views.products import ProductsView
from src.ui.views.sales import SalesView
from src.ui.views.customers import CustomersView
from src.ui.views.reports import ReportsView
from src.ui.views.settings import SettingsView
from src.utils.logger import get_logger

logger = get_logger(__name__)

class MainWindow(ctk.CTk):
    """Main application window with modern UI"""

    def __init__(self, db_manager, settings_manager, theme_manager):
        super().__init__()

        self.db_manager = db_manager
        self.settings_manager = settings_manager
        self.theme_manager = theme_manager

        # Window configuration
        self.title(f"{self.settings_manager.shop_info.name} - Smart Mobile Shop v2.0")
        self.geometry("1600x1000")
        self.minsize(1200, 700)

        # Set window icon if available
        icon_path = self.theme_manager.get_icon_path("app_icon.png")
        if icon_path:
            try:
                self.iconbitmap(icon_path)
            except:
                pass

        # Configure grid weights
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Current view tracking
        self.current_view = None

        # Initialize UI
        self._setup_ui()
        self._show_dashboard()

        # Setup window close handler
        self.protocol("WM_DELETE_WINDOW", self._on_closing)

        logger.info("Main window initialized")

    def _configure_fonts(self):
        """Configure fonts for better Arabic display"""
        # Set default fonts for CustomTkinter using Hayah font
        arabic_font = self.theme_manager.get_font_config(12)
        header_font = self.theme_manager.get_header_font_config(14, "bold")

        # Update CustomTkinter default fonts
        ctk.ThemeManager.theme["CTkLabel"]["text_font"] = arabic_font
        ctk.ThemeManager.theme["CTkButton"]["text_font"] = arabic_font
        ctk.ThemeManager.theme["CTkEntry"]["text_font"] = arabic_font
        ctk.ThemeManager.theme["CTkTextbox"]["text_font"] = arabic_font

        # Store fonts for components to use
        self.default_font = arabic_font
        self.header_font = header_font

    def _setup_ui(self):
        """Setup main UI components"""
        # Header bar
        self.header = HeaderBar(
            self,
            settings_manager=self.settings_manager,
            theme_manager=self.theme_manager
        )
        self.header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=0, pady=0)

        # Sidebar
        self.sidebar = Sidebar(
            self,
            on_view_change=self._switch_view,
            theme_manager=self.theme_manager
        )
        self.sidebar.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)

        # Main content frame
        self.content_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.content_frame.grid(row=1, column=1, sticky="nsew", padx=(0, 0), pady=0)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)

    def _switch_view(self, view_name: str):
        """Switch to a different view"""
        try:
            # Clear current view
            if self.current_view:
                self.current_view.destroy()

            # Create new view based on name
            if view_name == "dashboard":
                self.current_view = DashboardView(
                    self.content_frame,
                    self.db_manager,
                    self.theme_manager
                )
            elif view_name == "products":
                self.current_view = ProductsView(
                    self.content_frame,
                    self.db_manager,
                    self.theme_manager
                )
            elif view_name == "sales":
                self.current_view = SalesView(
                    self.content_frame,
                    self.db_manager,
                    self.theme_manager
                )
            elif view_name == "customers":
                self.current_view = CustomersView(
                    self.content_frame,
                    self.db_manager,
                    self.theme_manager
                )
            elif view_name == "reports":
                self.current_view = ReportsView(
                    self.content_frame,
                    self.db_manager,
                    self.theme_manager
                )
            elif view_name == "settings":
                self.current_view = SettingsView(
                    self.content_frame,
                    self.settings_manager,
                    self.theme_manager
                )

            # Show new view
            if self.current_view:
                self.current_view.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

            # Update sidebar selection
            self.sidebar.set_active_button(view_name)

            logger.info(f"Switched to view: {view_name}")

        except Exception as e:
            logger.error(f"Error switching to view {view_name}: {e}")
            messagebox.showerror("خطأ", f"حدث خطأ في عرض الصفحة: {e}")

    def _show_dashboard(self):
        """Show dashboard by default"""
        self._switch_view("dashboard")

    def _on_closing(self):
        """Handle application closing"""
        try:
            if messagebox.askokcancel("إغلاق التطبيق", "هل تريد إغلاق التطبيق؟"):
                logger.info("Application closing by user")
                self.destroy()
        except Exception as e:
            logger.error(f"Error during application closing: {e}")
            self.destroy()