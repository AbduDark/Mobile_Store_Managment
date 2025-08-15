# Mobile Shop Management System - نظام إدارة محل الموبايلات

## Overview

A comprehensive desktop application for managing mobile phone shops built with Python and CustomTkinter. The system provides a modern Arabic/English bilingual interface for inventory management, sales processing, customer management, and business analytics. The application features a dark/light theme, real-time dashboard with sales metrics, point-of-sale functionality, and comprehensive reporting capabilities.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **GUI Framework**: CustomTkinter for modern desktop UI with dark/light theme support
- **Window Management**: Multi-tabbed interface with sidebar navigation
- **Language Support**: Bilingual Arabic-English interface with right-to-left text support
- **Data Visualization**: matplotlib integration for charts and analytics in dashboard and reports
- **Image Handling**: Pillow (PIL) for product image management and display

### Backend Architecture
- **Database Layer**: SQLite with custom DatabaseManager class for all data operations
- **Data Models**: Dataclass-based models for Products, Customers, Sales, and other entities
- **Business Logic**: Separated into individual window modules (products, sales, customers, reports)
- **Configuration Management**: Centralized settings system for shop info, currency, tax, and display preferences

### Data Storage Solutions
- **Primary Database**: SQLite for all transactional data
- **File Storage**: Local file system for product images and exported reports
- **Configuration**: JSON-based settings files for application preferences
- **Export Capabilities**: Excel export functionality using openpyxl for reports

### Key Features
- **Dashboard**: Real-time metrics display with sales statistics, inventory alerts, and revenue charts
- **Inventory Management**: Product catalog with categories, pricing, stock tracking, and low-stock alerts
- **Point of Sale**: Modern POS interface with barcode support and multiple payment methods
- **Customer Management**: Customer database with purchase history and contact information
- **Reporting System**: Comprehensive analytics with chart generation and Excel export
- **Multi-language Support**: Arabic and English interface with proper font handling

## External Dependencies

### Core Libraries
- **customtkinter**: Modern tkinter alternative for enhanced UI components
- **sqlite3**: Built-in Python SQLite interface for database operations
- **Pillow (PIL)**: Image processing library for product photos
- **matplotlib**: Plotting library for dashboard charts and report visualizations
- **openpyxl**: Excel file generation for report exports

### System Integration
- **Font Management**: Platform-specific Arabic font detection and configuration
- **File System**: Local storage for images, databases, and configuration files
- **Date/Time**: Python datetime module for sales tracking and reporting periods
- **Number Formatting**: Locale-aware currency and number formatting for Arabic regions

### UI Components
- **tkinter.messagebox**: System dialog boxes for user notifications
- **tkinter.filedialog**: File selection dialogs for image uploads and report exports
- **matplotlib.backends.backend_tkagg**: Integration layer for embedding charts in tkinter

The application is designed as a standalone desktop solution with no external API dependencies, focusing on local data management and offline functionality for small to medium-sized mobile phone retail operations.