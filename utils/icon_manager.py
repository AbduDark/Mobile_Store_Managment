
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Icon Manager for Mobile Shop Management System
إدارة الأيقونات لنظام إدارة محل الموبايلات
"""

import os
from pathlib import Path
from typing import Dict, Optional
import customtkinter as ctk
from PIL import Image, ImageTk

class IconManager:
    """Manager for loading and caching icons"""
    
    def __init__(self):
        self.icons_dir = Path(__file__).parent.parent / "icons"
        self.icon_cache: Dict[str, Dict[int, ctk.CTkImage]] = {}
        self.fallback_icons = self._create_fallback_icons()
        
    def _create_fallback_icons(self) -> Dict[str, str]:
        """Create fallback text icons when image icons are not available"""
        return {
            'dashboard': '🏠',
            'products': '📱',
            'sales': '💰',
            'customers': '👥',
            'reports': '📊',
            'settings': '⚙️',
            'add': '➕',
            'edit': '✏️',
            'delete': '🗑️',
            'search': '🔍',
            'refresh': '🔄',
            'save': '💾',
            'cancel': '❌',
            'print': '🖨️',
            'export': '📤',
            'success': '✅',
            'warning': '⚠️',
            'error': '❌',
            'info': 'ℹ️',
            'low_stock': '📉',
            'mobile_phone': '📱',
            'barcode': '📊',
            'payment': '💳',
            'invoice': '🧾',
            'customer': '👤',
            'chart': '📈',
            'arrow_down': '⬇️',
            'arrow_up': '⬆️',
            'arrow_left': '⬅️',
            'arrow_right': '➡️',
            'calendar': '📅',
            'filter': '🔽',
            'sort': '📶'
        }
    
    def get_icon(self, icon_name: str, size: int = 24) -> Optional[ctk.CTkImage]:
        """Get icon by name and size"""
        try:
            # Check cache first
            if icon_name in self.icon_cache and size in self.icon_cache[icon_name]:
                return self.icon_cache[icon_name][size]
            
            # Try to load from file
            icon_path = self.icons_dir / f"{icon_name}.png"
            if icon_path.exists():
                image = Image.open(icon_path)
                ctk_image = ctk.CTkImage(light_image=image, dark_image=image, size=(size, size))
                
                # Cache the icon
                if icon_name not in self.icon_cache:
                    self.icon_cache[icon_name] = {}
                self.icon_cache[icon_name][size] = ctk_image
                
                return ctk_image
            
            # Fallback: return None for text fallback
            return None
            
        except Exception as e:
            print(f"خطأ في تحميل الأيقونة {icon_name}: {e}")
            return None
    
    def get_icon_text(self, icon_name: str) -> str:
        """Get fallback text icon"""
        return self.fallback_icons.get(icon_name, '●')
    
    def create_icon_button(self, parent, icon_name: str, text: str = "", 
                          command=None, size: int = 24, **kwargs) -> ctk.CTkButton:
        """Create a button with icon"""
        icon = self.get_icon(icon_name, size)
        
        if icon:
            # Use image icon
            return ctk.CTkButton(
                parent,
                image=icon,
                text=text,
                command=command,
                compound="left" if text else "center",
                **kwargs
            )
        else:
            # Use text fallback
            icon_text = self.get_icon_text(icon_name)
            display_text = f"{icon_text} {text}" if text else icon_text
            return ctk.CTkButton(
                parent,
                text=display_text,
                command=command,
                **kwargs
            )
    
    def create_icon_label(self, parent, icon_name: str, text: str = "", 
                         size: int = 24, **kwargs) -> ctk.CTkLabel:
        """Create a label with icon"""
        icon = self.get_icon(icon_name, size)
        
        if icon:
            # Use image icon
            return ctk.CTkLabel(
                parent,
                image=icon,
                text=text,
                compound="left" if text else "center",
                **kwargs
            )
        else:
            # Use text fallback
            icon_text = self.get_icon_text(icon_name)
            display_text = f"{icon_text} {text}" if text else icon_text
            return ctk.CTkLabel(
                parent,
                text=display_text,
                **kwargs
            )

# Global icon manager instance
_icon_manager = None

def get_icon_manager() -> IconManager:
    """Get the global icon manager instance"""
    global _icon_manager
    if _icon_manager is None:
        _icon_manager = IconManager()
    return _icon_manager
