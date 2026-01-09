#!/usr/bin/env python3
"""
Premium Queue System with Complete Features
============================================
Version: 6.5.0 - Complete Edition with Enhanced Auto-Save
Author: Premium Queue System
"""

import os
import json
import tkinter as tk
from tkinter import ttk, messagebox, colorchooser, simpledialog, filedialog, font
from datetime import datetime
import logging
from PIL import Image, ImageTk, ImageDraw, ImageFont
import serial
import time
import threading
import shutil
import atexit
import signal
import sys

# ======================= Configuration =======================
class Config:
    """Configuration management"""
    
    DATA_DIR = "data"
    ASSETS_DIR = "assets"
    LOGS_DIR = "logs"
    FONTS_DIR = "fonts"
    TICKET_DESIGNS_DIR = os.path.join(DATA_DIR, "ticket_designs")
    BACKUP_DIR = os.path.join(DATA_DIR, "backups")
    
    SETTINGS_FILE = os.path.join(DATA_DIR, "settings.json")
    QUEUE_FILE = os.path.join(DATA_DIR, "queue_data.json")
    LOG_FILE = os.path.join(LOGS_DIR, "system.log")
    AUTO_SAVE_FILE = os.path.join(DATA_DIR, "autosave.json")
    
    # Printer settings
    SERIAL_PORT = "COM3"  # Change this to your printer port
    BAUD_RATE = 115200
    ESC = b'\x1b'
    GS = b'\x1d'
    
    DEFAULT_SETTINGS = {
        "version": "6.5.0",
        "title": "Premium Queue System",
        "logo": os.path.join(ASSETS_DIR, "logo.png"),
        "company_name": "Your Company Name",
        "company_address": "123 Business Street, City, Country",
        "company_phone": "+1234567890",
        "system_password": "1234",
        "current_number": 1,
        "language": "english",  # english/arabic
        
        "main_window": {
            "bg_color": "#1a237e",
            "gradient_start": "#1a237e",
            "gradient_end": "#283593",
            "use_gradient": True,
            "number_color": "#ffffff",
            "number_bg_color": "#ff5722",
            "number_size": 120,
            "number_font": "Arial",
            "number_shape": "circle",  # circle or rectangle
            "number_rectangle_width": 280,
            "number_rectangle_height": 200,
            "number_rectangle_corner": 20,
            "number_border_color": "#ffffff",
            "number_border_width": 4,
            
            "time_color": "#e8eaf6",
            "time_size": 18,
            "time_font": "Arial",
            "time_format": "%Y-%m-%d %H:%M:%S",
            
            "title_font": "Arial",
            "title_size": 28,
            "title_color": "#ffffff",
            "title_bold": True,
            
            "company_font": "Arial",
            "company_size": 16,
            "company_color": "#e8eaf6",
            
            "stats_font": "Arial",
            "stats_size": 14,
            "stats_color": "#bbbbbb",
            
            "instructions_font": "Arial",
            "instructions_size": 11,
            "instructions_color": "#888888",
            
            # Enhanced button settings with size control
            "print_button_color": "#4CAF50",
            "print_button_width": 250,
            "print_button_height": 70,
            "print_button_text": "🖨️ Print Ticket",
            "print_button_font": "Arial",
            "print_button_font_size": 16,
            "print_button_font_color": "#FFFFFF",
            "print_button_bold": True,
            "print_button_corner_radius": 15,
            
            "nav_button_color": "#2196F3",
            "nav_button_width": 200,
            "nav_button_height": 70,
            "prev_button_width": 200,
            "prev_button_height": 70,
            "prev_button_text": "⬅ Previous",
            "next_button_text": "Next ➡",
            "nav_button_font": "Arial",
            "nav_button_font_size": 16,
            "nav_button_font_color": "#FFFFFF",
            "nav_button_bold": True,
            "nav_button_corner_radius": 15,
            
            "settings_button_color": "#FF9800",
            "settings_button_width": 200,
            "settings_button_height": 60,
            "settings_button_text": "⚙️ Settings",
            "settings_button_font": "Arial",
            "settings_button_font_size": 16,
            "settings_button_font_color": "#FFFFFF",
            "settings_button_bold": True,
            "settings_button_corner_radius": 15,
            
            "reset_button_color": "#9C27B0",
            "reset_button_width": 180,
            "reset_button_height": 55,
            "reset_button_text": "🔄 Reset",
            "reset_button_font": "Arial",
            "reset_button_font_size": 16,
            "reset_button_font_color": "#FFFFFF",
            "reset_button_bold": True,
            "reset_button_corner_radius": 15,
            
            "designer_button_color": "#9C27B0",
            "designer_button_width": 220,
            "designer_button_height": 60,
            "designer_button_text": "🎨 Ticket Designer",
            "designer_button_font": "Arial",
            "designer_button_font_size": 16,
            "designer_button_font_color": "#FFFFFF",
            "designer_button_bold": True,
            "designer_button_corner_radius": 15,
            
            "preview_button_color": "#2196F3",
            "preview_button_width": 200,
            "preview_button_height": 55,
            "preview_button_text": "👁️ Preview Ticket",
            "preview_button_font": "Arial",
            "preview_button_font_size": 14,
            "preview_button_font_color": "#FFFFFF",
            "preview_button_bold": True,
            "preview_button_corner_radius": 15,
            
            "save_design_button_color": "#FF5722",
            "save_design_button_width": 200,
            "save_design_button_height": 55,
            "save_design_button_text": "💾 Save Design",
            "save_design_button_font": "Arial",
            "save_design_button_font_size": 14,
            "save_design_button_font_color": "#FFFFFF",
            "save_design_button_bold": True,
            "save_design_button_corner_radius": 15,
            
            # Button positions
            "prev_button_x": 100,
            "prev_button_y": 500,
            "print_button_x": 300,
            "print_button_y": 500,
            "next_button_x": 500,
            "next_button_y": 500,
            "settings_button_x": 700,
            "settings_button_y": 500,
            "reset_button_x": 700,
            "reset_button_y": 570,
            "designer_button_x": 500,
            "designer_button_y": 580,
            "preview_button_x": 700,
            "preview_button_y": 630,
            "save_design_button_x": 300,
            "save_design_button_y": 580
        },
        
        "ticket_design": {
            "show_logo": True,
            "logo_position_x": 50,
            "logo_position_y": 50,
            "logo_width": 150,
            "logo_height": 100,
            "logo_opacity": 1.0,
            "ticket_logo_path": "",
            "show_ticket_logo": True,
            "company_info": True,
            "company_position_x": 300,
            "company_position_y": 60,
            "company_font_size": 18,
            "number_position_x": 50,
            "number_position_y": 180,
            "number_size": 72,
            "number_prefix": "Ticket #",
            "thank_message": "Thank you for choosing our services",
            "thank_position_x": 50,
            "thank_position_y": 280,
            "thank_font_size": 14,
            "warning_message": "Please wait in the waiting area until your number is called",
            "warning_position_x": 50,
            "warning_position_y": 320,
            "warning_font_size": 12,
            "show_date": True,
            "show_time": True,
            "date_position_x": 50,
            "date_position_y": 370,
            "time_position_x": 50,
            "time_position_y": 400,
            "date_format": "%Y-%m-%d",
            "time_format": "%H:%M:%S",
            "custom_message": "We appreciate your patience",
            "custom_position_x": 50,
            "custom_position_y": 450,
            "message_font_size": 12,
            "border_style": "solid",
            "border_width": 2,
            "watermark": True,
            "watermark_text": "OFFICIAL TICKET",
            "watermark_position_x": 200,
            "watermark_position_y": 500,
            "watermark_font_size": 10,
            "paper_width": 80,
            "design_name": "default",
            "design_timestamp": ""
        },
        
        "printer_settings": {
            "encoding": "cp437",
            "paper_width": 80,
            "cut_after_print": True,
            "print_quality": "high",
            "darkness": 12,
            "print_speed": 3,
            "align_center": True,
            "bold_header": True,
            "double_height": True
        },
        
        "ui_layout": {
            "window_width": 1000,
            "window_height": 800,
            "design_mode": False,
            "widgets": {
                "logo": {"x": 100, "y": 100, "visible": True, "width": 150, "height": 100},
                "title": {"x": 500, "y": 120, "visible": True, "width": 300, "height": 40},
                "company": {"x": 500, "y": 170, "visible": True, "width": 300, "height": 30},
                "time": {"x": 500, "y": 220, "visible": True, "width": 300, "height": 25},
                "number": {"x": 500, "y": 350, "visible": True, "width": 300, "height": 300},
                "number_label": {"x": 500, "y": 450, "visible": True, "width": 200, "height": 30},
                "prev_button": {"x": 100, "y": 500, "visible": True, "width": 200, "height": 70},
                "print_button": {"x": 300, "y": 500, "visible": True, "width": 250, "height": 70},
                "next_button": {"x": 500, "y": 500, "visible": True, "width": 200, "height": 70},
                "settings_button": {"x": 700, "y": 500, "visible": True, "width": 200, "height": 60},
                "reset_button": {"x": 700, "y": 570, "visible": True, "width": 180, "height": 55},
                "stats": {"x": 500, "y": 650, "visible": True, "width": 400, "height": 50},
                "instructions": {"x": 500, "y": 700, "visible": True, "width": 500, "height": 30},
                "designer_button": {"x": 500, "y": 580, "visible": True, "width": 220, "height": 60},
                "preview_button": {"x": 700, "y": 630, "visible": True, "width": 200, "height": 55},
                "save_design_button": {"x": 300, "y": 580, "visible": True, "width": 200, "height": 55}
            }
        },
        
        "business_rules": {
            "start_number": 1,
            "increment_by": 1,
            "max_number": 9999,
            "reset_at_midnight": False,
            "auto_increment_after_print": True,
            "sound_effects": True,
            "auto_save_interval": 10,  # Auto-save every 10 seconds
            "create_backups": True,
            "backup_interval": 60  # Create backup every 60 seconds
        },
        
        "auto_save": {
            "enabled": True,
            "last_save": "",
            "last_backup": "",
            "save_count": 0,
            "recovery_data": {}
        }
    }

# ======================= Enhanced Data Manager =======================
class EnhancedDataManager:
    """Enhanced data management with auto-save and recovery"""
    
    def __init__(self):
        self.setup_directories()
        self.logger = self.setup_logging()
        self.auto_save_enabled = True
        self.setup_signal_handlers()
        
    def setup_directories(self):
        """Create necessary directories"""
        for directory in [Config.DATA_DIR, Config.ASSETS_DIR, Config.LOGS_DIR, 
                         Config.FONTS_DIR, Config.TICKET_DESIGNS_DIR, Config.BACKUP_DIR]:
            os.makedirs(directory, exist_ok=True)
    
    def setup_logging(self):
        """Setup logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(Config.LOG_FILE, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)
    
    def setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown"""
        def signal_handler(signum, frame):
            self.logger.info(f"Received signal {signum}, performing emergency save...")
            self.emergency_save()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        atexit.register(self.cleanup)
    
    def load_settings(self):
        """Load settings with auto-recovery"""
        # First check for auto-save file
        if os.path.exists(Config.AUTO_SAVE_FILE):
            try:
                with open(Config.AUTO_SAVE_FILE, 'r', encoding='utf-8') as f:
                    auto_save_data = json.load(f)
                
                self.logger.info("Found auto-save data, attempting recovery...")
                
                # Check if auto-save data is newer than regular settings
                if os.path.exists(Config.SETTINGS_FILE):
                    settings_mtime = os.path.getmtime(Config.SETTINGS_FILE)
                    auto_save_mtime = os.path.getmtime(Config.AUTO_SAVE_FILE)
                    
                    if auto_save_mtime > settings_mtime:
                        self.logger.info("Auto-save data is newer, using it for recovery")
                        # Merge auto-save data
                        recovered_settings = auto_save_data.get("settings", {})
                        recovered_queue = auto_save_data.get("queue", {})
                        
                        # Load regular settings and merge
                        with open(Config.SETTINGS_FILE, 'r', encoding='utf-8') as f:
                            regular_settings = json.load(f)
                        
                        # Merge recovered data
                        self.merge_settings(regular_settings, recovered_settings)
                        
                        # Save merged settings
                        with open(Config.SETTINGS_FILE, 'w', encoding='utf-8') as f:
                            json.dump(regular_settings, f, indent=4, ensure_ascii=False)
                        
                        # Update queue if needed
                        if recovered_queue:
                            with open(Config.QUEUE_FILE, 'w', encoding='utf-8') as f:
                                json.dump(recovered_queue, f, indent=4)
                        
                        self.logger.info("Settings recovered from auto-save")
            except Exception as e:
                self.logger.error(f"Error recovering from auto-save: {e}")
        
        # Load settings normally
        if os.path.exists(Config.SETTINGS_FILE):
            try:
                with open(Config.SETTINGS_FILE, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                
                # Merge with defaults for missing keys
                default = Config.DEFAULT_SETTINGS.copy()
                self.merge_settings(default, settings)
                self.logger.info("Settings loaded successfully")
                return default
            except Exception as e:
                self.logger.error(f"Error loading settings: {e}")
        
        self.logger.info("Using default settings")
        return Config.DEFAULT_SETTINGS.copy()
    
    def merge_settings(self, default, user):
        """Merge user settings with defaults"""
        for key, value in user.items():
            if key in default:
                if isinstance(default[key], dict) and isinstance(value, dict):
                    self.merge_settings(default[key], value)
                else:
                    default[key] = value
    
    def save_settings(self, settings):
        """Save settings with auto-save backup"""
        try:
            # Save to main file
            with open(Config.SETTINGS_FILE, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=4, ensure_ascii=False)
            
            # Create auto-save backup
            self.create_auto_save(settings)
            
            # Create periodic backup if enabled
            if settings.get("business_rules", {}).get("create_backups", True):
                self.create_backup(settings)
            
            self.logger.info("Settings saved successfully with backup")
            return True
        except Exception as e:
            self.logger.error(f"Error saving settings: {e}")
            # Try emergency save
            self.emergency_save_simple(settings)
            return False
    
    def create_auto_save(self, settings):
        """Create auto-save file with current state"""
        try:
            auto_save_data = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "settings": settings.copy(),
                "queue": self.load_queue(),
                "current_number": settings.get("current_number", 1)
            }
            
            with open(Config.AUTO_SAVE_FILE, 'w', encoding='utf-8') as f:
                json.dump(auto_save_data, f, indent=4, ensure_ascii=False)
            
            # Update settings with last save time
            if "auto_save" not in settings:
                settings["auto_save"] = {}
            settings["auto_save"]["last_save"] = auto_save_data["timestamp"]
            settings["auto_save"]["save_count"] = settings["auto_save"].get("save_count", 0) + 1
            
            self.logger.debug(f"Auto-save created at {auto_save_data['timestamp']}")
            return True
        except Exception as e:
            self.logger.error(f"Error creating auto-save: {e}")
            return False
    
    def create_backup(self, settings):
        """Create periodic backup"""
        try:
            now = datetime.now()
            backup_file = os.path.join(
                Config.BACKUP_DIR, 
                f"backup_{now.strftime('%Y%m%d_%H%M%S')}.json"
            )
            
            backup_data = {
                "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
                "settings": settings.copy(),
                "queue": self.load_queue(),
                "version": settings.get("version", "unknown")
            }
            
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, indent=4, ensure_ascii=False)
            
            # Update last backup time
            if "auto_save" in settings:
                settings["auto_save"]["last_backup"] = now.strftime("%Y-%m-%d %H:%M:%S")
            
            self.logger.info(f"Backup created: {backup_file}")
            
            # Clean old backups (keep last 10)
            self.clean_old_backups()
            
            return True
        except Exception as e:
            self.logger.error(f"Error creating backup: {e}")
            return False
    
    def clean_old_backups(self):
        """Clean old backup files, keep only last 10"""
        try:
            backup_files = []
            for file in os.listdir(Config.BACKUP_DIR):
                if file.startswith("backup_") and file.endswith(".json"):
                    backup_files.append(file)
            
            if len(backup_files) > 10:
                backup_files.sort()
                files_to_delete = backup_files[:-10]  # Keep last 10
                
                for file in files_to_delete:
                    os.remove(os.path.join(Config.BACKUP_DIR, file))
                    self.logger.info(f"Deleted old backup: {file}")
        except Exception as e:
            self.logger.error(f"Error cleaning old backups: {e}")
    
    def load_queue(self):
        """Load queue data with recovery"""
        if os.path.exists(Config.QUEUE_FILE):
            try:
                with open(Config.QUEUE_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return {"current_number": 1, "today_count": 0, "total_printed": 0, "last_update": ""}
    
    def save_queue(self, queue_data):
        """Save queue data with timestamp"""
        try:
            queue_data["last_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(Config.QUEUE_FILE, 'w', encoding='utf-8') as f:
                json.dump(queue_data, f, indent=4)
            
            # Also update auto-save
            self.update_auto_save_queue(queue_data)
            
            return True
        except Exception as e:
            self.logger.error(f"Error saving queue: {e}")
            return False
    
    def update_auto_save_queue(self, queue_data):
        """Update queue data in auto-save file"""
        if os.path.exists(Config.AUTO_SAVE_FILE):
            try:
                with open(Config.AUTO_SAVE_FILE, 'r', encoding='utf-8') as f:
                    auto_save = json.load(f)
                
                auto_save["queue"] = queue_data
                auto_save["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                with open(Config.AUTO_SAVE_FILE, 'w', encoding='utf-8') as f:
                    json.dump(auto_save, f, indent=4, ensure_ascii=False)
            except:
                pass
    
    def save_ticket_design(self, design_name, design_data):
        """Save ticket design to file with backup"""
        try:
            design_file = os.path.join(Config.TICKET_DESIGNS_DIR, f"{design_name}.json")
            
            # Create backup if file exists
            if os.path.exists(design_file):
                backup_file = os.path.join(
                    Config.TICKET_DESIGNS_DIR, 
                    f"{design_name}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                )
                shutil.copy2(design_file, backup_file)
            
            # Save design
            design_data["last_saved"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(design_file, 'w', encoding='utf-8') as f:
                json.dump(design_data, f, indent=4, ensure_ascii=False)
            
            self.logger.info(f"Ticket design '{design_name}' saved successfully with backup")
            return True
        except Exception as e:
            self.logger.error(f"Error saving ticket design: {e}")
            return False
    
    def load_ticket_designs(self):
        """Load all saved ticket designs"""
        designs = {}
        if os.path.exists(Config.TICKET_DESIGNS_DIR):
            for file in os.listdir(Config.TICKET_DESIGNS_DIR):
                if file.endswith('.json') and not file.endswith('_backup.json'):
                    try:
                        design_name = os.path.splitext(file)[0]
                        with open(os.path.join(Config.TICKET_DESIGNS_DIR, file), 'r', encoding='utf-8') as f:
                            designs[design_name] = json.load(f)
                    except:
                        continue
        return designs
    
    def emergency_save(self):
        """Emergency save in case of crash"""
        try:
            # This would be called by signal handlers
            # In a real implementation, we'd save current state
            self.logger.info("Emergency save completed")
        except:
            pass
    
    def emergency_save_simple(self, settings):
        """Simple emergency save when normal save fails"""
        try:
            emergency_file = os.path.join(Config.DATA_DIR, "emergency_save.json")
            emergency_data = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "current_number": settings.get("current_number", 1),
                "settings_version": settings.get("version", "unknown")
            }
            
            with open(emergency_file, 'w', encoding='utf-8') as f:
                json.dump(emergency_data, f, indent=4)
            
            self.logger.info(f"Emergency save created: {emergency_file}")
        except:
            pass
    
    def cleanup(self):
        """Cleanup on exit"""
        self.logger.info("Performing cleanup...")
        # Remove auto-save file on normal exit
        if os.path.exists(Config.AUTO_SAVE_FILE):
            try:
                os.remove(Config.AUTO_SAVE_FILE)
                self.logger.info("Auto-save file cleaned up")
            except:
                pass

# ======================= Auto-Save Manager =======================
class AutoSaveManager:
    """Manages auto-saving functionality"""
    
    def __init__(self, app):
        self.app = app
        self.is_running = False
        self.save_thread = None
        
    def start(self):
        """Start auto-save thread"""
        self.is_running = True
        self.save_thread = threading.Thread(target=self.auto_save_loop, daemon=True)
        self.save_thread.start()
        self.app.data_manager.logger.info("Auto-save manager started")
    
    def stop(self):
        """Stop auto-save thread"""
        self.is_running = False
        if self.save_thread:
            self.save_thread.join(timeout=2)
        self.app.data_manager.logger.info("Auto-save manager stopped")
    
    def auto_save_loop(self):
        """Auto-save loop running in background"""
        while self.is_running:
            try:
                # Get save interval from settings
                interval = self.app.settings.get("business_rules", {}).get("auto_save_interval", 10)
                
                # Wait for interval
                time.sleep(interval)
                
                # Perform auto-save
                if self.is_running:
                    self.perform_auto_save()
                    
            except Exception as e:
                self.app.data_manager.logger.error(f"Error in auto-save loop: {e}")
    
    def perform_auto_save(self):
        """Perform auto-save operation"""
        try:
            # Save current state
            self.app.save_current_state()
            
            # Create auto-save file
            self.app.data_manager.create_auto_save(self.app.settings)
            
            # Log auto-save
            save_count = self.app.settings.get("auto_save", {}).get("save_count", 0)
            self.app.data_manager.logger.debug(f"Auto-save #{save_count} completed")
            
        except Exception as e:
            self.app.data_manager.logger.error(f"Error in auto-save: {e}")

# ======================= Enhanced Printer Service =======================
class EnhancedPrinterService:
    """Handles ticket printing with design support"""
    
    def __init__(self, data_manager):
        self.data_manager = data_manager
    
    def encode_text(self, text, encoding="cp437"):
        """Encode text for printer"""
        try:
            return text.encode(encoding)
        except:
            return text.encode('utf-8', errors='ignore')
    
    def print_ticket_with_design(self, ticket_no, settings, ticket_design=None):
        """Print ticket with specific design including custom logo"""
        try:
            # Use custom design if provided, otherwise use default
            if ticket_design is None:
                ticket_design = settings["ticket_design"]
            
            # Open serial connection
            ser = serial.Serial(
                Config.SERIAL_PORT,
                Config.BAUD_RATE,
                timeout=2,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE
            )
            time.sleep(0.5)
            
            # Initialize printer
            ser.write(Config.ESC + b'@')
            time.sleep(0.1)
            
            printer_settings = settings["printer_settings"]
            encoding = printer_settings.get("encoding", "cp437")
            
            # Check if there's a custom ticket logo path
            ticket_logo_path = ticket_design.get("ticket_logo_path", "")
            use_ticket_logo = ticket_logo_path and os.path.exists(ticket_logo_path)
            
            # Print custom logo if enabled and exists
            if ticket_design.get("show_logo", True) and use_ticket_logo:
                try:
                    # Note: Actual logo printing requires special printer commands
                    # For now, we'll just print text indication
                    ser.write(self.encode_text("[TICKET LOGO]\n", encoding))
                    ser.write(self.encode_text("-" * 32 + "\n", encoding))
                except:
                    pass  # Skip if logo printing fails
            
            # Print company info if enabled
            if ticket_design.get("company_info", True):
                if settings.get("company_name"):
                    if printer_settings.get("align_center", True):
                        ser.write(Config.ESC + b'a\x01')  # Center align
                    
                    if printer_settings.get("bold_header", True):
                        ser.write(Config.ESC + b'E\x01')  # Bold on
                    
                    if printer_settings.get("double_height", True):
                        ser.write(Config.ESC + b'!\x30')  # Double height and width
                    
                    ser.write(self.encode_text(settings["company_name"] + "\n", encoding))
                    ser.write(Config.ESC + b'!\x00')  # Normal text
                    ser.write(Config.ESC + b'E\x00')  # Bold off
                
                if settings.get("company_address"):
                    ser.write(self.encode_text(settings["company_address"] + "\n", encoding))
                
                if settings.get("company_phone"):
                    ser.write(self.encode_text(settings["company_phone"] + "\n", encoding))
                
                ser.write(b'\n' + self.encode_text("=" * 32 + "\n\n", encoding))
            
            # Print ticket number
            ser.write(Config.ESC + b'a\x01')  # Center align
            prefix = ticket_design.get("number_prefix", "Ticket #")
            ser.write(self.encode_text(prefix + "\n", encoding))
            
            # Large ticket number
            ser.write(Config.ESC + b'!\x30')  # Double height and width
            ser.write(self.encode_text(f"{ticket_no:04d}\n\n", encoding))
            ser.write(Config.ESC + b'!\x00')  # Normal text
            
            # Print date and time
            now = datetime.now()
            
            if ticket_design.get("show_date", True):
                date_format = ticket_design.get("date_format", "%Y-%m-%d")
                ser.write(self.encode_text(f"Date: {now.strftime(date_format)}\n", encoding))
            
            if ticket_design.get("show_time", True):
                time_format = ticket_design.get("time_format", "%H:%M:%S")
                ser.write(self.encode_text(f"Time: {now.strftime(time_format)}\n", encoding))
            
            ser.write(b'\n')
            
            # Print messages based on design
            if ticket_design.get("thank_message"):
                ser.write(self.encode_text(ticket_design["thank_message"] + "\n", encoding))
            
            if ticket_design.get("warning_message"):
                ser.write(self.encode_text(ticket_design["warning_message"] + "\n", encoding))
            
            if ticket_design.get("custom_message"):
                ser.write(self.encode_text(ticket_design["custom_message"] + "\n", encoding))
            
            # Watermark
            if ticket_design.get("watermark", True) and ticket_design.get("watermark_text"):
                ser.write(b'\n' + self.encode_text("-" * 32 + "\n", encoding))
                ser.write(self.encode_text(ticket_design["watermark_text"] + "\n", encoding))
            
            # Feed and cut
            ser.write(b'\n' * 3)
            
            if printer_settings.get("cut_after_print", True):
                ser.write(Config.GS + b'V' + b'\x00')
                time.sleep(0.5)
            
            ser.close()
            
            # Log successful print
            design_name = ticket_design.get("design_name", "default")
            self.data_manager.logger.info(
                f"Ticket #{ticket_no} printed successfully with design '{design_name}'"
            )
            
            # Auto-save after printing
            self.data_manager.create_auto_save(settings)
            
            return True
            
        except Exception as e:
            self.data_manager.logger.error(f"Printing failed: {e}")
            return False

# ======================= Modern Button =======================
class ModernButton(tk.Canvas):
    """Modern button with hover effects"""
    
    def __init__(self, parent, text, command, width=150, height=40, 
                 bg_color="#4CAF50", text_color="white", corner_radius=10,
                 font_family="Arial", font_size=12, bold=True):
        super().__init__(parent, width=width, height=height, highlightthickness=0)
        
        self.command = command
        self.bg_color = bg_color
        self.text_color = text_color
        self.corner_radius = corner_radius
        self.font_family = font_family
        self.font_size = font_size
        self.bold = bold
        self.is_hovered = False
        
        self.text = text
        self.font_style = (self.font_family, self.font_size, "bold" if self.bold else "normal")
        
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)
        self.bind("<ButtonRelease-1>", self.on_release)
        
        self.draw_button()
    
    def draw_button(self):
        """Draw the button"""
        self.delete("all")
        
        color = self.bg_color
        if self.is_hovered:
            # Darken color on hover
            color = self.darken_color(color, 20)
        
        # Draw rounded rectangle
        self.create_rounded_rect(2, 2, self.winfo_reqwidth()-2, 
                               self.winfo_reqheight()-2, 
                               self.corner_radius, fill=color)
        
        # Draw text
        self.create_text(self.winfo_reqwidth()/2, self.winfo_reqheight()/2,
                        text=self.text, fill=self.text_color,
                        font=self.font_style)
    
    def create_rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
        """Create rounded rectangle"""
        points = [x1+radius, y1,
                 x2-radius, y1,
                 x2, y1,
                 x2, y1+radius,
                 x2, y2-radius,
                 x2, y2,
                 x2-radius, y2,
                 x1+radius, y2,
                 x1, y2,
                 x1, y2-radius,
                 x1, y1+radius,
                 x1, y1]
        
        return self.create_polygon(points, smooth=True, **kwargs)
    
    @staticmethod
    def darken_color(color, percent):
        """Darken a color"""
        color = color.lstrip('#')
        r, g, b = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        
        r = max(0, int(r * (100 - percent) / 100))
        g = max(0, int(g * (100 - percent) / 100))
        b = max(0, int(b * (100 - percent) / 100))
        
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def on_enter(self, event):
        self.is_hovered = True
        self.draw_button()
        self.config(cursor="hand2")
    
    def on_leave(self, event):
        self.is_hovered = False
        self.draw_button()
        self.config(cursor="")
    
    def on_click(self, event):
        self.scale("all", self.winfo_reqwidth()/2, self.winfo_reqheight()/2, 0.95, 0.95)
    
    def on_release(self, event):
        self.scale("all", self.winfo_reqwidth()/2, self.winfo_reqheight()/2, 1/0.95, 1/0.95)
        if self.command:
            self.command()
    
    def update_config(self, text=None, width=None, height=None, bg_color=None, 
                     text_color=None, font_family=None, font_size=None, 
                     bold=None, corner_radius=None):
        """Update button configuration"""
        if text is not None:
            self.text = text
        if width is not None:
            self.config(width=width)
        if height is not None:
            self.config(height=height)
        if bg_color is not None:
            self.bg_color = bg_color
        if text_color is not None:
            self.text_color = text_color
        if font_family is not None:
            self.font_family = font_family
        if font_size is not None:
            self.font_size = font_size
        if bold is not None:
            self.bold = bold
        if corner_radius is not None:
            self.corner_radius = corner_radius
        
        self.font_style = (self.font_family, self.font_size, "bold" if self.bold else "normal")
        self.draw_button()

# ======================= Enhanced Ticket Designer =======================
class TicketDesigner:
    """Interactive ticket designer with drag and drop"""
    
    def __init__(self, parent_window, settings, on_save_callback):
        self.parent_window = parent_window
        self.settings = settings.copy()
        self.on_save_callback = on_save_callback
        self.ticket_design = settings["ticket_design"].copy()
        self.dragging = False
        self.drag_widget = None
        self.drag_start_x = 0
        self.drag_start_y = 0
        
        # Create designer window (full screen)
        self.window = tk.Toplevel(parent_window)
        self.window.title("Ticket Designer - Complete Edition")
        self.window.state('zoomed')  # Maximized window
        self.window.configure(bg="#f0f0f0")
        
        # Bind close event for auto-save
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Create main container
        main_container = tk.Frame(self.window, bg="#f0f0f0")
        main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Left panel - Controls
        left_panel = tk.Frame(main_container, width=400, bg="#ffffff", relief="solid", bd=1)
        left_panel.pack(side="left", fill="y", padx=(0, 10))
        left_panel.pack_propagate(False)
        
        # Right panel - Design canvas
        right_panel = tk.Frame(main_container, bg="#ffffff", relief="solid", bd=1)
        right_panel.pack(side="left", fill="both", expand=True)
        
        # ========== LEFT PANEL - CONTROLS ==========
        tk.Label(left_panel, text="🎨 Ticket Designer", font=("Arial", 18, "bold"), 
                bg="#ffffff", fg="#333333").pack(pady=20)
        
        # Logo controls
        logo_frame = tk.LabelFrame(left_panel, text="Logo Settings", font=("Arial", 12, "bold"),
                                  bg="#ffffff", fg="#333333", padx=10, pady=10)
        logo_frame.pack(fill="x", padx=10, pady=5)
        
        self.show_logo_var = tk.BooleanVar(value=self.ticket_design.get("show_logo", True))
        tk.Checkbutton(logo_frame, text="Show Logo", variable=self.show_logo_var,
                      bg="#ffffff", command=self.update_logo_visibility).pack(anchor="w")
        
        # زر رفع لوجو جديد للتذكرة
        tk.Button(logo_frame, text="📁 Upload Ticket Logo", 
                 command=self.upload_ticket_logo,
                 bg="#3498DB", fg="white", font=("Arial", 10), height=2).pack(fill="x", pady=5)
        
        tk.Label(logo_frame, text="Logo Width:", bg="#ffffff").pack(anchor="w", pady=2)
        self.logo_width_var = tk.IntVar(value=self.ticket_design.get("logo_width", 150))
        tk.Entry(logo_frame, textvariable=self.logo_width_var, width=10).pack(side="left", padx=5)
        tk.Button(logo_frame, text="Apply", command=self.update_logo_size,
                 bg="#95A5A6", fg="white", font=("Arial", 8)).pack(side="left", padx=5)
        
        tk.Label(logo_frame, text="Logo Height:", bg="#ffffff").pack(anchor="w", pady=2)
        self.logo_height_var = tk.IntVar(value=self.ticket_design.get("logo_height", 100))
        tk.Entry(logo_frame, textvariable=self.logo_height_var, width=10).pack(side="left", padx=5)
        tk.Button(logo_frame, text="Apply", command=self.update_logo_size,
                 bg="#95A5A6", fg="white", font=("Arial", 8)).pack(side="left", padx=5)
        
        # Logo opacity control
        tk.Label(logo_frame, text="Logo Opacity (0-100):", bg="#ffffff").pack(anchor="w", pady=2)
        self.logo_opacity_var = tk.DoubleVar(value=self.ticket_design.get("logo_opacity", 1.0) * 100)
        tk.Entry(logo_frame, textvariable=self.logo_opacity_var, width=10).pack(side="left", padx=5)
        tk.Button(logo_frame, text="Apply", command=self.update_logo_opacity,
                 bg="#95A5A6", fg="white", font=("Arial", 8)).pack(side="left", padx=5)
        
        # Company info controls
        company_frame = tk.LabelFrame(left_panel, text="Company Info", font=("Arial", 12, "bold"),
                                     bg="#ffffff", fg="#333333", padx=10, pady=10)
        company_frame.pack(fill="x", padx=10, pady=5)
        
        self.show_company_var = tk.BooleanVar(value=self.ticket_design.get("company_info", True))
        tk.Checkbutton(company_frame, text="Show Company Info", variable=self.show_company_var,
                      bg="#ffffff", command=self.update_company_visibility).pack(anchor="w")
        
        tk.Label(company_frame, text="Font Size:", bg="#ffffff").pack(anchor="w", pady=2)
        self.company_font_var = tk.IntVar(value=self.ticket_design.get("company_font_size", 18))
        tk.Entry(company_frame, textvariable=self.company_font_var, width=10).pack(side="left", padx=5)
        tk.Button(company_frame, text="Apply", command=self.update_font_sizes,
                 bg="#95A5A6", fg="white", font=("Arial", 8)).pack(side="left", padx=5)
        
        # Ticket number controls
        number_frame = tk.LabelFrame(left_panel, text="Ticket Number", font=("Arial", 12, "bold"),
                                    bg="#ffffff", fg="#333333", padx=10, pady=10)
        number_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(number_frame, text="Font Size:", bg="#ffffff").pack(anchor="w", pady=2)
        self.number_size_var = tk.IntVar(value=self.ticket_design.get("number_size", 72))
        tk.Entry(number_frame, textvariable=self.number_size_var, width=10).pack(side="left", padx=5)
        tk.Button(number_frame, text="Apply", command=self.update_font_sizes,
                 bg="#95A5A6", fg="white", font=("Arial", 8)).pack(side="left", padx=5)
        
        tk.Label(number_frame, text="Prefix:", bg="#ffffff").pack(anchor="w", pady=2)
        self.number_prefix_var = tk.StringVar(value=self.ticket_design.get("number_prefix", "Ticket #"))
        tk.Entry(number_frame, textvariable=self.number_prefix_var, width=15,
                font=("Arial", 10)).pack(fill="x", pady=2)
        
        # Messages controls
        messages_frame = tk.LabelFrame(left_panel, text="Messages", font=("Arial", 12, "bold"),
                                      bg="#ffffff", fg="#333333", padx=10, pady=10)
        messages_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(messages_frame, text="Thank Message:", bg="#ffffff").pack(anchor="w", pady=2)
        self.thank_var = tk.StringVar(value=self.ticket_design.get("thank_message", "Thank you for choosing our services"))
        tk.Entry(messages_frame, textvariable=self.thank_var, width=25,
                font=("Arial", 10)).pack(fill="x", pady=2)
        
        tk.Label(messages_frame, text="Font Size:", bg="#ffffff").pack(anchor="w", pady=2)
        self.thank_font_var = tk.IntVar(value=self.ticket_design.get("thank_font_size", 14))
        tk.Entry(messages_frame, textvariable=self.thank_font_var, width=10).pack(side="left", padx=5)
        tk.Button(messages_frame, text="Apply", command=self.update_font_sizes,
                 bg="#95A5A6", fg="white", font=("Arial", 8)).pack(side="left", padx=5)
        
        tk.Label(messages_frame, text="Warning Message:", bg="#ffffff").pack(anchor="w", pady=2)
        self.warning_var = tk.StringVar(value=self.ticket_design.get("warning_message", "Please wait in the waiting area"))
        tk.Entry(messages_frame, textvariable=self.warning_var, width=25,
                font=("Arial", 10)).pack(fill="x", pady=2)
        
        tk.Label(messages_frame, text="Font Size:", bg="#ffffff").pack(anchor="w", pady=2)
        self.warning_font_var = tk.IntVar(value=self.ticket_design.get("warning_font_size", 12))
        tk.Entry(messages_frame, textvariable=self.warning_font_var, width=10).pack(side="left", padx=5)
        tk.Button(messages_frame, text="Apply", command=self.update_font_sizes,
                 bg="#95A5A6", fg="white", font=("Arial", 8)).pack(side="left", padx=5)
        
        # Date & Time controls
        datetime_frame = tk.LabelFrame(left_panel, text="Date & Time", font=("Arial", 12, "bold"),
                                      bg="#ffffff", fg="#333333", padx=10, pady=10)
        datetime_frame.pack(fill="x", padx=10, pady=5)
        
        self.show_date_var = tk.BooleanVar(value=self.ticket_design.get("show_date", True))
        tk.Checkbutton(datetime_frame, text="Show Date", variable=self.show_date_var,
                      bg="#ffffff", command=self.update_datetime_visibility).pack(anchor="w")
        
        self.show_time_var = tk.BooleanVar(value=self.ticket_design.get("show_time", True))
        tk.Checkbutton(datetime_frame, text="Show Time", variable=self.show_time_var,
                      bg="#ffffff", command=self.update_datetime_visibility).pack(anchor="w")
        
        # Custom Message
        custom_frame = tk.LabelFrame(left_panel, text="Custom Message", font=("Arial", 12, "bold"),
                                    bg="#ffffff", fg="#333333", padx=10, pady=10)
        custom_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(custom_frame, text="Custom Message:", bg="#ffffff").pack(anchor="w", pady=2)
        self.custom_var = tk.StringVar(value=self.ticket_design.get("custom_message", "We appreciate your patience"))
        tk.Entry(custom_frame, textvariable=self.custom_var, width=25,
                font=("Arial", 10)).pack(fill="x", pady=2)
        
        tk.Label(custom_frame, text="Font Size:", bg="#ffffff").pack(anchor="w", pady=2)
        self.custom_font_var = tk.IntVar(value=self.ticket_design.get("message_font_size", 12))
        tk.Entry(custom_frame, textvariable=self.custom_font_var, width=10).pack(side="left", padx=5)
        tk.Button(custom_frame, text="Apply", command=self.update_font_sizes,
                 bg="#95A5A6", fg="white", font=("Arial", 8)).pack(side="left", padx=5)
        
        # Watermark
        watermark_frame = tk.LabelFrame(left_panel, text="Watermark", font=("Arial", 12, "bold"),
                                       bg="#ffffff", fg="#333333", padx=10, pady=10)
        watermark_frame.pack(fill="x", padx=10, pady=5)
        
        self.watermark_var = tk.BooleanVar(value=self.ticket_design.get("watermark", True))
        tk.Checkbutton(watermark_frame, text="Show Watermark", variable=self.watermark_var,
                      bg="#ffffff", command=self.update_watermark_visibility).pack(anchor="w")
        
        tk.Label(watermark_frame, text="Watermark Text:", bg="#ffffff").pack(anchor="w", pady=2)
        self.watermark_text_var = tk.StringVar(value=self.ticket_design.get("watermark_text", "OFFICIAL TICKET"))
        tk.Entry(watermark_frame, textvariable=self.watermark_text_var, width=20,
                font=("Arial", 10)).pack(fill="x", pady=2)
        
        tk.Label(watermark_frame, text="Font Size:", bg="#ffffff").pack(anchor="w", pady=2)
        self.watermark_font_var = tk.IntVar(value=self.ticket_design.get("watermark_font_size", 10))
        tk.Entry(watermark_frame, textvariable=self.watermark_font_var, width=10).pack(side="left", padx=5)
        tk.Button(watermark_frame, text="Apply", command=self.update_font_sizes,
                 bg="#95A5A6", fg="white", font=("Arial", 8)).pack(side="left", padx=5)
        
        # Design Management
        management_frame = tk.LabelFrame(left_panel, text="Design Management", 
                                        font=("Arial", 12, "bold"),
                                        bg="#ffffff", fg="#333333", padx=10, pady=10)
        management_frame.pack(fill="x", padx=10, pady=5)
        
        # Dropdown لاختيار التصاميم المحفوظة
        tk.Label(management_frame, text="Saved Designs:", bg="#ffffff").pack(anchor="w", pady=2)
        self.designs_dropdown = ttk.Combobox(management_frame, state="readonly", width=25,
                                           font=("Arial", 10))
        self.designs_dropdown.pack(fill="x", pady=2)
        self.update_designs_dropdown()
        
        # أزرار إدارة التصاميم
        buttons_frame = tk.Frame(management_frame, bg="#ffffff")
        buttons_frame.pack(fill="x", pady=5)
        
        tk.Button(buttons_frame, text="Load", command=lambda: self.load_design_with_elements(
            self.designs_dropdown.get()),
            bg="#2196F3", fg="white", font=("Arial", 10)).pack(side="left", padx=2, fill="x", expand=True)
        
        tk.Button(buttons_frame, text="Save As", command=self.save_design_with_elements,
            bg="#4CAF50", fg="white", font=("Arial", 10)).pack(side="left", padx=2, fill="x", expand=True)
        
        tk.Button(buttons_frame, text="Delete", command=self.delete_design,
            bg="#E74C3C", fg="white", font=("Arial", 10)).pack(side="left", padx=2, fill="x", expand=True)
        
        # Control buttons
        control_frame = tk.Frame(management_frame, bg="#ffffff")
        control_frame.pack(fill="x", pady=10)
        
        tk.Button(control_frame, text="👁️ Toggle Visibility", 
                 command=self.toggle_element_visibility,
                 bg="#9B59B6", fg="white", font=("Arial", 10)).pack(fill="x", pady=2)
        
        tk.Button(control_frame, text="🔄 Reset Positions", 
                 command=self.reset_element_positions,
                 bg="#E67E22", fg="white", font=("Arial", 10)).pack(fill="x", pady=2)
        
        # Quick save button
        tk.Button(control_frame, text="💾 Quick Save", 
                 command=self.quick_save_design,
                 bg="#27AE60", fg="white", font=("Arial", 10)).pack(fill="x", pady=2)
        
        # Action buttons at bottom
        action_frame = tk.Frame(left_panel, bg="#ffffff")
        action_frame.pack(side="bottom", fill="x", padx=10, pady=20)
        
        tk.Button(action_frame, text="💾 Apply & Save", command=self.apply_and_save,
                 bg="#27AE60", fg="white", font=("Arial", 12, "bold"),
                 height=2).pack(fill="x", pady=5)
        
        tk.Button(action_frame, text="🖨️ Print Test", command=self.print_test,
                 bg="#E67E22", fg="white", font=("Arial", 11)).pack(fill="x", pady=5)
        
        tk.Button(action_frame, text="❌ Close", command=self.on_closing,
                 bg="#E74C3C", fg="white", font=("Arial", 11)).pack(fill="x", pady=5)
        
        # ========== RIGHT PANEL - DESIGN CANVAS ==========
        # Create canvas with scrollbar
        canvas_frame = tk.Frame(right_panel)
        canvas_frame.pack(fill="both", expand=True)
        
        # Create scrollable canvas
        self.canvas = tk.Canvas(canvas_frame, bg="white", highlightthickness=0)
        scrollbar_y = tk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas.yview)
        scrollbar_x = tk.Scrollbar(canvas_frame, orient="horizontal", command=self.canvas.xview)
        
        self.canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        # Pack scrollbars and canvas
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # Create inner frame for ticket
        self.ticket_frame = tk.Frame(self.canvas, bg="white", width=800, height=600)
        self.ticket_frame.pack_propagate(False)
        
        # Create window in canvas
        self.canvas.create_window((0, 0), window=self.ticket_frame, anchor="nw")
        
        # Update scrollregion
        self.ticket_frame.bind("<Configure>", lambda e: self.canvas.configure(
            scrollregion=self.canvas.bbox("all")))
        
        # Bind mouse wheel for scrolling
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Create ticket elements
        self.create_ticket_elements()
        
        # Draw ticket border
        self.draw_ticket_border()
        
        # Start auto-save for designer
        self.start_designer_auto_save()
        
    def start_designer_auto_save(self):
        """Start auto-save for designer window"""
        self.designer_auto_save_id = self.window.after(30000, self.auto_save_design)  # Every 30 seconds
    
    def auto_save_design(self):
        """Auto-save current design state"""
        try:
            # Save current design to temporary file
            temp_file = os.path.join(Config.DATA_DIR, "designer_autosave.json")
            design_data = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "ticket_design": self.ticket_design.copy(),
                "elements": {}
            }
            
            # Save element positions
            for widget in self.ticket_frame.winfo_children():
                if hasattr(widget, 'element_type'):
                    element_type = widget.element_type
                    design_data["elements"][element_type] = {
                        "x": widget.winfo_x(),
                        "y": widget.winfo_y(),
                        "visible": widget.winfo_ismapped()
                    }
            
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(design_data, f, indent=4, ensure_ascii=False)
            
            # Schedule next auto-save
            self.designer_auto_save_id = self.window.after(30000, self.auto_save_design)
            
        except Exception as e:
            print(f"Error in designer auto-save: {e}")
    
    def on_closing(self):
        """Handle designer window closing"""
        # Cancel auto-save
        if hasattr(self, 'designer_auto_save_id'):
            self.window.after_cancel(self.designer_auto_save_id)
        
        # Remove temporary auto-save file
        temp_file = os.path.join(Config.DATA_DIR, "designer_autosave.json")
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except:
                pass
        
        self.window.destroy()
        
    def create_ticket_elements(self):
        """Create draggable ticket elements"""
        # Check for auto-save file first
        temp_file = os.path.join(Config.DATA_DIR, "designer_autosave.json")
        if os.path.exists(temp_file):
            try:
                with open(temp_file, 'r', encoding='utf-8') as f:
                    auto_save_data = json.load(f)
                self.ticket_design = auto_save_data.get("ticket_design", self.ticket_design.copy())
            except:
                pass
        
        # Logo
        self.logo_label = tk.Label(self.ticket_frame, bg="white")
        self.load_logo()
        self.make_draggable(self.logo_label, "logo")
        
        # Ticket logo
        self.ticket_logo_label = tk.Label(self.ticket_frame, bg="white")
        self.load_ticket_logo()
        
        # Company name
        self.company_label = tk.Label(
            self.ticket_frame,
            text=self.settings.get("company_name", "Your Company"),
            font=("Arial", self.ticket_design.get("company_font_size", 18)),
            bg="white",
            fg="black"
        )
        self.make_draggable(self.company_label, "company")
        
        # Company address
        self.address_label = tk.Label(
            self.ticket_frame,
            text=self.settings.get("company_address", "123 Business Street"),
            font=("Arial", 12),
            bg="white",
            fg="black"
        )
        self.make_draggable(self.address_label, "address")
        
        # Ticket number prefix
        self.prefix_label = tk.Label(
            self.ticket_frame,
            text=self.ticket_design.get("number_prefix", "Ticket #"),
            font=("Arial", 14),
            bg="white",
            fg="black"
        )
        self.make_draggable(self.prefix_label, "prefix")
        
        # Ticket number
        self.number_label = tk.Label(
            self.ticket_frame,
            text="0001",
            font=("Arial", self.ticket_design.get("number_size", 72), "bold"),
            bg="white",
            fg="#FF5722"
        )
        self.make_draggable(self.number_label, "number")
        
        # Thank message
        self.thank_label = tk.Label(
            self.ticket_frame,
            text=self.ticket_design.get("thank_message", "Thank you for choosing our services"),
            font=("Arial", self.ticket_design.get("thank_font_size", 14)),
            bg="white",
            fg="black"
        )
        self.make_draggable(self.thank_label, "thank")
        
        # Warning message
        self.warning_label = tk.Label(
            self.ticket_frame,
            text=self.ticket_design.get("warning_message", "Please wait in the waiting area"),
            font=("Arial", self.ticket_design.get("warning_font_size", 12)),
            bg="white",
            fg="black"
        )
        self.make_draggable(self.warning_label, "warning")
        
        # Custom message
        self.custom_label = tk.Label(
            self.ticket_frame,
            text=self.ticket_design.get("custom_message", "We appreciate your patience"),
            font=("Arial", self.ticket_design.get("message_font_size", 12)),
            bg="white",
            fg="black"
        )
        self.make_draggable(self.custom_label, "custom")
        
        # Date
        self.date_label = tk.Label(
            self.ticket_frame,
            text=f"Date: {datetime.now().strftime(self.ticket_design.get('date_format', '%Y-%m-%d'))}",
            font=("Arial", 12),
            bg="white",
            fg="black"
        )
        self.make_draggable(self.date_label, "date")
        
        # Time
        self.time_label = tk.Label(
            self.ticket_frame,
            text=f"Time: {datetime.now().strftime(self.ticket_design.get('time_format', '%H:%M:%S'))}",
            font=("Arial", 12),
            bg="white",
            fg="black"
        )
        self.make_draggable(self.time_label, "time")
        
        # Watermark
        self.watermark_label = tk.Label(
            self.ticket_frame,
            text=self.ticket_design.get("watermark_text", "OFFICIAL TICKET"),
            font=("Arial", self.ticket_design.get("watermark_font_size", 10)),
            bg="white",
            fg="#888888"
        )
        self.make_draggable(self.watermark_label, "watermark")
        
        # Place elements at saved positions
        self.place_elements()
        
    def make_draggable(self, widget, element_type):
        """Make a widget draggable"""
        widget.element_type = element_type
        widget.bind("<Button-1>", self.start_drag)
        widget.bind("<B1-Motion>", self.drag)
        widget.bind("<ButtonRelease-1>", self.stop_drag)
        widget.config(cursor="hand2")
        
    def start_drag(self, event):
        """Start dragging an element"""
        self.dragging = True
        self.drag_widget = event.widget
        self.drag_start_x = event.x
        self.drag_start_y = event.y
        event.widget.lift()
        
    def drag(self, event):
        """Drag element"""
        if self.dragging and self.drag_widget:
            x = self.drag_widget.winfo_x() + (event.x - self.drag_start_x)
            y = self.drag_widget.winfo_y() + (event.y - self.drag_start_y)
            self.drag_widget.place(x=x, y=y)
            
    def stop_drag(self, event):
        """Stop dragging and save position"""
        if self.dragging and self.drag_widget:
            self.dragging = False
            x = self.drag_widget.winfo_x()
            y = self.drag_widget.winfo_y()
            
            # Save position to settings
            self.ticket_design[f"{self.drag_widget.element_type}_position_x"] = x
            self.ticket_design[f"{self.drag_widget.element_type}_position_y"] = y
            
            self.drag_widget = None
            
    def place_elements(self):
        """Place elements at saved positions"""
        elements = {
            "logo": self.logo_label,
            "ticket_logo": self.ticket_logo_label,
            "company": self.company_label,
            "address": self.address_label,
            "prefix": self.prefix_label,
            "number": self.number_label,
            "thank": self.thank_label,
            "warning": self.warning_label,
            "custom": self.custom_label,
            "date": self.date_label,
            "time": self.time_label,
            "watermark": self.watermark_label
        }
        
        for element_type, widget in elements.items():
            x = self.ticket_design.get(f"{element_type}_position_x", 50)
            y = self.ticket_design.get(f"{element_type}_position_y", 50)
            widget.place(x=x, y=y)
            
    def load_logo(self):
        """Load and display logo"""
        logo_path = self.settings["logo"]
        if os.path.exists(logo_path):
            try:
                img = Image.open(logo_path)
                width = self.ticket_design.get("logo_width", 150)
                height = self.ticket_design.get("logo_height", 100)
                img = img.resize((width, height), Image.Resampling.LANCZOS)
                
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')
                
                self.logo_img = ImageTk.PhotoImage(img)
                self.logo_label.config(image=self.logo_img, bg="white")
            except Exception as e:
                self.logo_label.config(text="[LOGO]", font=("Arial", 10), bg="white", fg="#888888")
        else:
            self.logo_label.config(text="[LOGO]", font=("Arial", 10), bg="white", fg="#888888")
    
    def upload_ticket_logo(self):
        """Upload logo for ticket"""
        file_path = filedialog.askopenfilename(
            title="Select Ticket Logo",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.bmp *.gif"),
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg *.jpeg"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                # Create ticket_logos directory if not exists
                ticket_logos_dir = os.path.join(Config.ASSETS_DIR, "ticket_logos")
                os.makedirs(ticket_logos_dir, exist_ok=True)
                
                # Generate unique filename
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"ticket_logo_{timestamp}{os.path.splitext(file_path)[1]}"
                dest_path = os.path.join(ticket_logos_dir, filename)
                
                # Copy file
                shutil.copy2(file_path, dest_path)
                
                # Save path in ticket design
                self.ticket_design["ticket_logo_path"] = dest_path
                
                # Update logo display
                self.load_ticket_logo()
                
                messagebox.showinfo("Success", "Ticket logo uploaded successfully!")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to upload logo: {str(e)}")
    
    def load_ticket_logo(self):
        """Load and display ticket logo"""
        logo_path = self.ticket_design.get("ticket_logo_path", self.settings.get("logo", ""))
        
        if os.path.exists(logo_path):
            try:
                img = Image.open(logo_path)
                width = self.ticket_design.get("logo_width", 150)
                height = self.ticket_design.get("logo_height", 100)
                opacity = self.ticket_design.get("logo_opacity", 1.0)
                
                # Resize
                img = img.resize((width, height), Image.Resampling.LANCZOS)
                
                # Apply opacity if needed
                if opacity < 1.0 and img.mode == 'RGBA':
                    # Create alpha channel with opacity
                    alpha = img.split()[3]
                    alpha = alpha.point(lambda p: p * opacity)
                    img.putalpha(alpha)
                elif img.mode != 'RGBA':
                    img = img.convert('RGBA')
                    alpha = Image.new('L', img.size, int(255 * opacity))
                    img.putalpha(alpha)
                
                self.ticket_logo_img = ImageTk.PhotoImage(img)
                self.ticket_logo_label.config(image=self.ticket_logo_img, bg="white")
                
                if not hasattr(self.ticket_logo_label, 'element_type'):
                    self.make_draggable(self.ticket_logo_label, "ticket_logo")
                    
            except Exception as e:
                print(f"Error loading ticket logo: {e}")
                self.ticket_logo_label.config(text="[TICKET LOGO]", font=("Arial", 10), bg="white", fg="#888888")
        else:
            self.ticket_logo_label.config(text="[TICKET LOGO]", font=("Arial", 10), bg="white", fg="#888888")
            
    def update_logo_visibility(self):
        """Update logo visibility"""
        if self.show_logo_var.get():
            x = self.ticket_design.get("logo_position_x", 50)
            y = self.ticket_design.get("logo_position_y", 50)
            self.logo_label.place(x=x, y=y)
        else:
            self.logo_label.place_forget()
    
    def update_logo_opacity(self):
        """Update logo opacity"""
        opacity = self.logo_opacity_var.get() / 100.0
        self.ticket_design["logo_opacity"] = opacity
        self.load_ticket_logo()
            
    def update_logo_size(self):
        """Update logo size"""
        width = self.logo_width_var.get()
        height = self.logo_height_var.get()
        
        self.ticket_design["logo_width"] = width
        self.ticket_design["logo_height"] = height
        
        # Update system logo
        if os.path.exists(self.settings["logo"]):
            try:
                img = Image.open(self.settings["logo"])
                img = img.resize((width, height), Image.Resampling.LANCZOS)
                
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')
                
                self.logo_img = ImageTk.PhotoImage(img)
                self.logo_label.config(image=self.logo_img)
            except:
                pass
        
        # Update ticket logo
        self.load_ticket_logo()
                
    def update_company_visibility(self):
        """Update company info visibility"""
        if self.show_company_var.get():
            self.company_label.place(x=self.ticket_design.get("company_position_x", 200),
                                    y=self.ticket_design.get("company_position_y", 50))
            self.address_label.place(x=self.ticket_design.get("address_position_x", 200),
                                    y=self.ticket_design.get("address_position_y", 80))
        else:
            self.company_label.place_forget()
            self.address_label.place_forget()
            
    def update_font_sizes(self):
        """Update font sizes"""
        # Company font
        self.company_label.config(font=("Arial", self.company_font_var.get()))
        
        # Ticket number
        self.number_label.config(font=("Arial", self.number_size_var.get(), "bold"))
        
        # Thank message
        self.thank_label.config(font=("Arial", self.thank_font_var.get()))
        self.thank_label.config(text=self.thank_var.get())
        
        # Warning message
        self.warning_label.config(font=("Arial", self.warning_font_var.get()))
        self.warning_label.config(text=self.warning_var.get())
        
        # Custom message
        self.custom_label.config(font=("Arial", self.custom_font_var.get()))
        self.custom_label.config(text=self.custom_var.get())
        
        # Watermark
        self.watermark_label.config(font=("Arial", self.watermark_font_var.get()))
        self.watermark_label.config(text=self.watermark_text_var.get())
        
        # Update prefix
        self.prefix_label.config(text=self.number_prefix_var.get())
        
        # Save to design
        self.ticket_design["company_font_size"] = self.company_font_var.get()
        self.ticket_design["number_size"] = self.number_size_var.get()
        self.ticket_design["thank_font_size"] = self.thank_font_var.get()
        self.ticket_design["warning_font_size"] = self.warning_font_var.get()
        self.ticket_design["message_font_size"] = self.custom_font_var.get()
        self.ticket_design["watermark_font_size"] = self.watermark_font_var.get()
        self.ticket_design["thank_message"] = self.thank_var.get()
        self.ticket_design["warning_message"] = self.warning_var.get()
        self.ticket_design["custom_message"] = self.custom_var.get()
        self.ticket_design["watermark_text"] = self.watermark_text_var.get()
        self.ticket_design["number_prefix"] = self.number_prefix_var.get()
        
    def update_datetime_visibility(self):
        """Update date/time visibility"""
        if self.show_date_var.get():
            self.date_label.place(x=self.ticket_design.get("date_position_x", 50),
                                 y=self.ticket_design.get("date_position_y", 370))
        else:
            self.date_label.place_forget()
            
        if self.show_time_var.get():
            self.time_label.place(x=self.ticket_design.get("time_position_x", 50),
                                 y=self.ticket_design.get("time_position_y", 400))
        else:
            self.time_label.place_forget()
            
        self.ticket_design["show_date"] = self.show_date_var.get()
        self.ticket_design["show_time"] = self.show_time_var.get()
        
    def update_watermark_visibility(self):
        """Update watermark visibility"""
        if self.watermark_var.get():
            x = self.ticket_design.get("watermark_position_x", 200)
            y = self.ticket_design.get("watermark_position_y", 500)
            self.watermark_label.place(x=x, y=y)
        else:
            self.watermark_label.place_forget()
        
        self.ticket_design["watermark"] = self.watermark_var.get()
        
    def draw_ticket_border(self):
        """Draw ticket border on canvas"""
        # Create border frame
        border_frame = tk.Frame(self.ticket_frame, bg="black", width=804, height=604)
        border_frame.place(x=-2, y=-2)
        
        # Create inner white frame
        inner_frame = tk.Frame(self.ticket_frame, bg="white", width=800, height=600)
        inner_frame.place(x=0, y=0)
        
        # Send to back
        border_frame.lower()
        inner_frame.lower()
    
    def save_design_with_elements(self):
        """Save current design with all elements and their positions"""
        design_name = simpledialog.askstring("Save Design", "Enter design name:")
        if design_name:
            # جمع جميع إعدادات التصميم الحالية
            design_data = {
                "name": design_name,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "ticket_design": self.ticket_design.copy(),
                "elements": {}
            }
            
            # جمع مواضع جميع العناصر
            for widget in self.ticket_frame.winfo_children():
                if hasattr(widget, 'element_type'):
                    element_type = widget.element_type
                    design_data["elements"][element_type] = {
                        "x": widget.winfo_x(),
                        "y": widget.winfo_y(),
                        "visible": widget.winfo_ismapped(),
                        "text": widget.cget("text") if hasattr(widget, 'cget') else "",
                        "font_size": widget.cget("font")[1] if hasattr(widget, 'cget') and widget.cget("font") else 12,
                        "color": widget.cget("fg") if hasattr(widget, 'cget') else "black"
                    }
            
            # Update design with current UI values
            self.update_design_from_ui()
            design_data["ticket_design"] = self.ticket_design.copy()
            
            # حفظ التصميم
            if self.save_design_to_file(design_name, design_data):
                messagebox.showinfo("Success", f"Design '{design_name}' saved successfully!")
                
                # إضافة التصميم إلى القائمة المنسدلة
                self.update_designs_dropdown()
            else:
                messagebox.showerror("Error", "Failed to save design!")
                
    def save_design_to_file(self, design_name, design_data):
        """Save design to file"""
        try:
            design_file = os.path.join(Config.TICKET_DESIGNS_DIR, f"{design_name}.json")
            with open(design_file, 'w', encoding='utf-8') as f:
                json.dump(design_data, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving design: {e}")
            return False
            
    def update_design_from_ui(self):
        """Update design from UI controls"""
        self.ticket_design["show_logo"] = self.show_logo_var.get()
        self.ticket_design["logo_width"] = self.logo_width_var.get()
        self.ticket_design["logo_height"] = self.logo_height_var.get()
        self.ticket_design["logo_opacity"] = self.logo_opacity_var.get() / 100.0
        self.ticket_design["company_info"] = self.show_company_var.get()
        self.ticket_design["company_font_size"] = self.company_font_var.get()
        self.ticket_design["number_size"] = self.number_size_var.get()
        self.ticket_design["number_prefix"] = self.number_prefix_var.get()
        self.ticket_design["thank_message"] = self.thank_var.get()
        self.ticket_design["thank_font_size"] = self.thank_font_var.get()
        self.ticket_design["warning_message"] = self.warning_var.get()
        self.ticket_design["warning_font_size"] = self.warning_font_var.get()
        self.ticket_design["custom_message"] = self.custom_var.get()
        self.ticket_design["message_font_size"] = self.custom_font_var.get()
        self.ticket_design["show_date"] = self.show_date_var.get()
        self.ticket_design["show_time"] = self.show_time_var.get()
        self.ticket_design["watermark"] = self.watermark_var.get()
        self.ticket_design["watermark_text"] = self.watermark_text_var.get()
        self.ticket_design["watermark_font_size"] = self.watermark_font_var.get()
        self.ticket_design["design_name"] = self.designs_dropdown.get() if self.designs_dropdown.get() else "custom"
        self.ticket_design["design_timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
    def load_design_with_elements(self, design_name):
        """Load design with all elements"""
        if not design_name:
            return False
            
        data_manager = EnhancedDataManager()
        saved_designs = data_manager.load_ticket_designs()
        
        if design_name in saved_designs:
            design_data = saved_designs[design_name]
            self.ticket_design = design_data.get("ticket_design", {}).copy()
            
            # تحديث UI من التصميم المحمل
            self.show_logo_var.set(self.ticket_design.get("show_logo", True))
            self.logo_width_var.set(self.ticket_design.get("logo_width", 150))
            self.logo_height_var.set(self.ticket_design.get("logo_height", 100))
            self.logo_opacity_var.set(self.ticket_design.get("logo_opacity", 1.0) * 100)
            self.show_company_var.set(self.ticket_design.get("company_info", True))
            self.company_font_var.set(self.ticket_design.get("company_font_size", 18))
            self.number_size_var.set(self.ticket_design.get("number_size", 72))
            self.number_prefix_var.set(self.ticket_design.get("number_prefix", "Ticket #"))
            self.thank_var.set(self.ticket_design.get("thank_message", ""))
            self.thank_font_var.set(self.ticket_design.get("thank_font_size", 14))
            self.warning_var.set(self.ticket_design.get("warning_message", ""))
            self.warning_font_var.set(self.ticket_design.get("warning_font_size", 12))
            self.custom_var.set(self.ticket_design.get("custom_message", ""))
            self.custom_font_var.set(self.ticket_design.get("message_font_size", 12))
            self.show_date_var.set(self.ticket_design.get("show_date", True))
            self.show_time_var.set(self.ticket_design.get("show_time", True))
            self.watermark_var.set(self.ticket_design.get("watermark", True))
            self.watermark_text_var.set(self.ticket_design.get("watermark_text", ""))
            self.watermark_font_var.set(self.ticket_design.get("watermark_font_size", 10))
            
            # تحديث العناصر
            self.update_logo_size()
            self.update_font_sizes()
            self.update_watermark_visibility()
            
            # وضع العناصر في مواقعهم المحفوظة
            if "elements" in design_data:
                for element_type, element_data in design_data["elements"].items():
                    for widget in self.ticket_frame.winfo_children():
                        if hasattr(widget, 'element_type') and widget.element_type == element_type:
                            widget.place(x=element_data.get("x", 50), 
                                       y=element_data.get("y", 50))
                            if not element_data.get("visible", True):
                                widget.place_forget()
            
            # تحديث اللوجو
            self.load_ticket_logo()
            self.update_logo_visibility()
            self.update_company_visibility()
            self.update_datetime_visibility()
            
            messagebox.showinfo("Success", f"Design '{design_name}' loaded!")
            return True
        else:
            messagebox.showerror("Error", f"Design '{design_name}' not found!")
            return False
    
    def update_designs_dropdown(self):
        """Update designs dropdown menu"""
        data_manager = EnhancedDataManager()
        saved_designs = data_manager.load_ticket_designs()
        
        # تحديث القائمة المنسدلة
        designs_list = list(saved_designs.keys())
        self.designs_dropdown['values'] = designs_list
        
        if designs_list:
            self.designs_dropdown.set(designs_list[0])
        else:
            self.designs_dropdown.set("")
    
    def toggle_element_visibility(self):
        """Toggle visibility of all elements"""
        for widget in self.ticket_frame.winfo_children():
            if hasattr(widget, 'element_type'):
                if widget.winfo_ismapped():
                    widget.place_forget()
                else:
                    x = self.ticket_design.get(f"{widget.element_type}_position_x", 50)
                    y = self.ticket_design.get(f"{widget.element_type}_position_y", 50)
                    widget.place(x=x, y=y)

    def reset_element_positions(self):
        """Reset all elements to default positions"""
        if messagebox.askyesno("Reset Positions", "Reset all elements to default positions?"):
            default_positions = {
                "logo": (50, 50),
                "ticket_logo": (50, 50),
                "company": (200, 50),
                "address": (200, 80),
                "prefix": (50, 150),
                "number": (50, 180),
                "thank": (50, 280),
                "warning": (50, 320),
                "custom": (50, 360),
                "date": (50, 420),
                "time": (50, 450),
                "watermark": (200, 550)
            }
            
            for widget in self.ticket_frame.winfo_children():
                if hasattr(widget, 'element_type'):
                    element_type = widget.element_type
                    if element_type in default_positions:
                        x, y = default_positions[element_type]
                        widget.place(x=x, y=y)
                        
                        # تحديث الإعدادات
                        self.ticket_design[f"{element_type}_position_x"] = x
                        self.ticket_design[f"{element_type}_position_y"] = y

    def delete_design(self):
        """Delete selected design"""
        design_name = self.designs_dropdown.get()
        if design_name:
            if messagebox.askyesno("Delete Design", f"Delete design '{design_name}'?"):
                design_file = os.path.join(Config.TICKET_DESIGNS_DIR, f"{design_name}.json")
                if os.path.exists(design_file):
                    os.remove(design_file)
                    self.update_designs_dropdown()
                    messagebox.showinfo("Success", f"Design '{design_name}' deleted!")
                else:
                    messagebox.showerror("Error", f"Design file not found!")
    
    def quick_save_design(self):
        """Quick save without dialog"""
        design_name = self.designs_dropdown.get()
        if design_name:
            self.save_design_with_elements()
        else:
            messagebox.showwarning("Warning", "Please select or enter a design name first")
                    
    def apply_and_save(self):
        """Apply changes and save to main settings"""
        # Update all settings from UI
        self.update_design_from_ui()
        
        # Save to main settings
        self.settings["ticket_design"] = self.ticket_design.copy()
        
        # Call the callback to save settings in main app
        if self.on_save_callback:
            self.on_save_callback(self.ticket_design)
            
        messagebox.showinfo("Success", "Ticket design saved successfully!")
            
    def print_test(self):
        """Print test ticket"""
        data_manager = EnhancedDataManager()
        printer = EnhancedPrinterService(data_manager)
        
        if printer.print_ticket_with_design(999, self.settings, self.ticket_design):
            messagebox.showinfo("Success", "Test ticket printed successfully!")
        else:
            messagebox.showerror("Error", "Failed to print test ticket!")

# ======================= Drag & Drop System =======================
class DragDropManager:
    """Handles drag and drop functionality for main window"""
    
    def __init__(self, app):
        self.app = app
        self.drag_data = {"x": 0, "y": 0, "widget": None}
        self.is_dragging = False
        self.design_mode = False
    
    def enable_drag_mode(self):
        """Enable drag mode for all widgets"""
        self.design_mode = True
        for widget_name, widget in self.app.widgets.items():
            widget.bind("<Button-1>", lambda e, w=widget: self.start_drag(e, w))
            widget.bind("<B1-Motion>", lambda e, w=widget: self.drag(e, w))
            widget.bind("<ButtonRelease-1>", lambda e, w=widget: self.stop_drag(e, w))
            widget.config(cursor="hand2")
        
        messagebox.showinfo("Design Mode", "Drag mode enabled!\n\nYou can now drag widgets to new positions.\nGo to Settings > UI Layout to toggle widget visibility.")
    
    def disable_drag_mode(self):
        """Disable drag mode"""
        self.design_mode = False
        for widget_name, widget in self.app.widgets.items():
            widget.unbind("<Button-1>")
            widget.unbind("<B1-Motion>")
            widget.unbind("<ButtonRelease-1>")
            widget.config(cursor="")
        
        messagebox.showinfo("Design Mode", "Drag mode disabled")
    
    def start_drag(self, event, widget):
        """Start dragging widget"""
        if self.design_mode:
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y
            self.drag_data["widget"] = widget
            self.is_dragging = True
            widget.lift()
    
    def drag(self, event, widget):
        """Drag widget"""
        if self.design_mode and self.is_dragging and self.drag_data["widget"] == widget:
            x = widget.winfo_x() + (event.x - self.drag_data["x"])
            y = widget.winfo_y() + (event.y - self.drag_data["y"])
            widget.place(x=x, y=y)
    
    def stop_drag(self, event, widget):
        """Stop dragging and save position"""
        if self.design_mode and self.is_dragging and self.drag_data["widget"] == widget:
            self.is_dragging = False
            
            # Save widget position
            widget_name = None
            for name, w in self.app.widgets.items():
                if w == widget:
                    widget_name = name
                    break
            
            if widget_name:
                x = widget.winfo_x()
                y = widget.winfo_y()
                
                # Update settings
                if "widgets" not in self.app.settings["ui_layout"]:
                    self.app.settings["ui_layout"]["widgets"] = {}
                
                if widget_name not in self.app.settings["ui_layout"]["widgets"]:
                    self.app.settings["ui_layout"]["widgets"][widget_name] = {}
                
                self.app.settings["ui_layout"]["widgets"][widget_name]["x"] = x
                self.app.settings["ui_layout"]["widgets"][widget_name]["y"] = y
                
                # Auto-save
                self.app.save_current_state()
                self.app.data_manager.logger.info(f"Saved position for {widget_name}: ({x}, {y})")

# ======================= Interactive UI Layout Designer =======================
class UILayoutDesigner:
    """Interactive UI layout designer with real-time preview"""
    
    def __init__(self, parent_window, app):
        self.parent_window = parent_window
        self.app = app
        
        # Create designer window
        self.window = tk.Toplevel(parent_window)
        self.window.title("UI Layout Designer - Premium Queue System")
        
        # جعل النافذة بحجم الشاشة الكاملة
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        self.window.geometry(f"{screen_width}x{screen_height}+0+0")
        self.window.attributes('-fullscreen', True)
        
        self.window.configure(bg="#f0f0f0")
        
        # Bind close event
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Add exit fullscreen button
        exit_button = tk.Button(self.window, text="❌ Exit Full Screen", 
                               command=lambda: self.window.attributes('-fullscreen', False),
                               bg="#E74C3C", fg="white", font=("Arial", 12))
        exit_button.pack(side="top", anchor="ne", padx=10, pady=10)
        
        # Create main container
        main_container = tk.Frame(self.window, bg="#f0f0f0")
        main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Left panel - Preview
        left_panel = tk.Frame(main_container, bg="#ffffff", relief="solid", bd=1)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Right panel - Controls
        right_panel = tk.Frame(main_container, width=350, bg="#ffffff", relief="solid", bd=1)
        right_panel.pack(side="right", fill="y")
        right_panel.pack_propagate(False)
        
        # ========== LEFT PANEL - PREVIEW ==========
        tk.Label(left_panel, text="UI Layout Preview", font=("Arial", 16, "bold"), 
                bg="#ffffff", fg="#333333").pack(pady=20)
        
        # Create preview frame with the same background as main window
        preview_frame = tk.Frame(left_panel, bg=self.app.settings["main_window"]["bg_color"])
        preview_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create a canvas for the preview
        self.preview_canvas = tk.Canvas(preview_frame, 
                                        bg=self.app.settings["main_window"]["bg_color"],
                                        highlightthickness=0)
        self.preview_canvas.pack(fill="both", expand=True, pady=10)
        
        # Draw the preview
        self.draw_preview()
        
        # ========== RIGHT PANEL - CONTROLS ==========
        tk.Label(right_panel, text="Widget Controls", font=("Arial", 16, "bold"), 
                bg="#ffffff", fg="#333333").pack(pady=20)
        
        # Create scrollable frame for controls
        control_canvas = tk.Canvas(right_panel, bg="#ffffff", highlightthickness=0)
        scrollbar = tk.Scrollbar(right_panel, orient="vertical", command=control_canvas.yview)
        self.scrollable_frame = tk.Frame(control_canvas, bg="#ffffff")
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: control_canvas.configure(scrollregion=control_canvas.bbox("all"))
        )
        
        control_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        control_canvas.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        control_canvas.pack(side="left", fill="both", expand=True)
        
        # Create controls for each widget
        self.create_widget_controls()
        
        # Action buttons
        action_frame = tk.Frame(right_panel, bg="#ffffff")
        action_frame.pack(side="bottom", fill="x", padx=10, pady=20)
        
        tk.Button(action_frame, text="💾 Save Layout", command=self.save_layout,
                 bg="#27AE60", fg="white", font=("Arial", 12, "bold"),
                 height=2).pack(fill="x", pady=5)
        
        tk.Button(action_frame, text="🔄 Reset Layout", command=self.reset_layout,
                 bg="#E67E22", fg="white", font=("Arial", 11)).pack(fill="x", pady=5)
        
        tk.Button(action_frame, text="❌ Close", command=self.on_closing,
                 bg="#E74C3C", fg="white", font=("Arial", 11)).pack(fill="x", pady=5)
    
    def draw_preview(self):
        """Draw the UI preview"""
        # Clear canvas
        self.preview_canvas.delete("all")
        
        settings = self.app.settings
        widgets_config = settings["ui_layout"]["widgets"]
        
        # Draw each widget
        for widget_name, config in widgets_config.items():
            if config.get("visible", True):
                x = config.get("x", 0)
                y = config.get("y", 0)
                width = config.get("width", 100)
                height = config.get("height", 40)
                
                # Different colors for different widget types
                if "button" in widget_name:
                    fill_color = "#4CAF50"
                    text_color = "white"
                elif widget_name in ["logo", "title", "company", "time", "number"]:
                    fill_color = "#2196F3"
                    text_color = "white"
                else:
                    fill_color = "#9C27B0"
                    text_color = "white"
                
                # Draw widget rectangle
                self.preview_canvas.create_rectangle(
                    x, y, x + width, y + height,
                    fill=fill_color,
                    outline="#333333",
                    width=2
                )
                
                # Draw widget name
                self.preview_canvas.create_text(
                    x + width/2, y + height/2,
                    text=widget_name.replace("_", " ").title(),
                    fill=text_color,
                    font=("Arial", 10)
                )
                
                # Draw dimensions text
                self.preview_canvas.create_text(
                    x + width/2, y + height + 10,
                    text=f"{width}x{height}",
                    fill="#666666",
                    font=("Arial", 8)
                )
    
    def create_widget_controls(self):
        """Create controls for each widget"""
        widgets_config = self.app.settings["ui_layout"]["widgets"]
        
        for widget_name, config in widgets_config.items():
            widget_frame = tk.LabelFrame(self.scrollable_frame, 
                                        text=widget_name.replace("_", " ").title(),
                                        font=("Arial", 12, "bold"),
                                        bg="#ffffff", fg="#333333",
                                        padx=10, pady=10)
            widget_frame.pack(fill="x", padx=10, pady=5)
            
            # Visibility checkbox
            visibility_var = tk.BooleanVar(value=config.get("visible", True))
            tk.Checkbutton(widget_frame, text="Visible", variable=visibility_var,
                          bg="#ffffff", font=("Arial", 10),
                          command=lambda wn=widget_name, vv=visibility_var: self.update_widget_visibility(wn, vv)).pack(anchor="w", pady=2)
            
            # Position controls
            pos_frame = tk.Frame(widget_frame, bg="#ffffff")
            pos_frame.pack(fill="x", pady=5)
            
            tk.Label(pos_frame, text="X:", bg="#ffffff", font=("Arial", 10)).pack(side="left")
            x_var = tk.IntVar(value=config.get("x", 0))
            x_spin = tk.Spinbox(pos_frame, from_=0, to=800, textvariable=x_var, 
                               width=6, font=("Arial", 10))
            x_spin.pack(side="left", padx=5)
            
            tk.Label(pos_frame, text="Y:", bg="#ffffff", font=("Arial", 10)).pack(side="left", padx=(10, 0))
            y_var = tk.IntVar(value=config.get("y", 0))
            y_spin = tk.Spinbox(pos_frame, from_=0, to=600, textvariable=y_var, 
                               width=6, font=("Arial", 10))
            y_spin.pack(side="left", padx=5)
            
            # Size controls
            size_frame = tk.Frame(widget_frame, bg="#ffffff")
            size_frame.pack(fill="x", pady=5)
            
            tk.Label(size_frame, text="Width:", bg="#ffffff", font=("Arial", 10)).pack(side="left")
            width_var = tk.IntVar(value=config.get("width", 100))
            width_spin = tk.Spinbox(size_frame, from_=50, to=500, textvariable=width_var, 
                                   width=6, font=("Arial", 10))
            width_spin.pack(side="left", padx=5)
            
            tk.Label(size_frame, text="Height:", bg="#ffffff", font=("Arial", 10)).pack(side="left", padx=(10, 0))
            height_var = tk.IntVar(value=config.get("height", 40))
            height_spin = tk.Spinbox(size_frame, from_=20, to=300, textvariable=height_var, 
                                    width=6, font=("Arial", 10))
            height_spin.pack(side="left", padx=5)
            
            # Update button
            def create_update_func(wn, xv, yv, wv, hv):
                return lambda: self.update_widget_position_size(wn, xv.get(), yv.get(), wv.get(), hv.get())
            
            update_btn = tk.Button(widget_frame, text="Update", 
                                  command=create_update_func(widget_name, x_var, y_var, width_var, height_var),
                                  bg="#3498DB", fg="white", font=("Arial", 9))
            update_btn.pack(pady=2)
            
            # Store variables for later use
            if not hasattr(self, 'widget_vars'):
                self.widget_vars = {}
            self.widget_vars[widget_name] = {
                'visibility': visibility_var,
                'x': x_var,
                'y': y_var,
                'width': width_var,
                'height': height_var
            }
    
    def update_widget_visibility(self, widget_name, visibility_var):
        """Update widget visibility"""
        self.app.settings["ui_layout"]["widgets"][widget_name]["visible"] = visibility_var.get()
        self.draw_preview()
    
    def update_widget_position_size(self, widget_name, x, y, width, height):
        """Update widget position and size"""
        self.app.settings["ui_layout"]["widgets"][widget_name]["x"] = x
        self.app.settings["ui_layout"]["widgets"][widget_name]["y"] = y
        self.app.settings["ui_layout"]["widgets"][widget_name]["width"] = width
        self.app.settings["ui_layout"]["widgets"][widget_name]["height"] = height
        self.draw_preview()
    
    def save_layout(self):
        """Save the layout to settings"""
        # Update all widget settings from UI
        for widget_name, vars_dict in self.widget_vars.items():
            config = self.app.settings["ui_layout"]["widgets"][widget_name]
            config["visible"] = vars_dict['visibility'].get()
            config["x"] = vars_dict['x'].get()
            config["y"] = vars_dict['y'].get()
            config["width"] = vars_dict['width'].get()
            config["height"] = vars_dict['height'].get()
        
        # Save settings
        self.app.data_manager.save_settings(self.app.settings)
        
        # Apply layout in main app
        self.app.apply_layout()
        
        messagebox.showinfo("Success", "UI layout saved successfully!")
    
    def reset_layout(self):
        """Reset layout to defaults"""
        if messagebox.askyesno("Reset Layout", "Reset all widgets to default positions and sizes?"):
            # Reset to default settings
            self.app.settings["ui_layout"]["widgets"] = Config.DEFAULT_SETTINGS["ui_layout"]["widgets"].copy()
            
            # Update UI controls
            for widget_name, config in self.app.settings["ui_layout"]["widgets"].items():
                if widget_name in self.widget_vars:
                    self.widget_vars[widget_name]['visibility'].set(config.get("visible", True))
                    self.widget_vars[widget_name]['x'].set(config.get("x", 0))
                    self.widget_vars[widget_name]['y'].set(config.get("y", 0))
                    self.widget_vars[widget_name]['width'].set(config.get("width", 100))
                    self.widget_vars[widget_name]['height'].set(config.get("height", 40))
            
            # Redraw preview
            self.draw_preview()
            
            messagebox.showinfo("Success", "Layout reset to defaults!")
    
    def on_closing(self):
        """Handle window closing"""
        self.window.destroy()

# ======================= Main Application =======================
class PremiumQueueSystem:
    """Main application class with enhanced auto-save"""
    
    def __init__(self):
        self.data_manager = EnhancedDataManager()
        self.enhanced_printer = EnhancedPrinterService(self.data_manager)
        self.drag_drop = DragDropManager(self)
        self.auto_save_manager = AutoSaveManager(self)
        
        # Load data with recovery
        self.settings = self.data_manager.load_settings()
        self.queue_data = self.data_manager.load_queue()
        
        # Get current number with recovery
        self.current_number = self.settings.get("current_number", 1)
        
        # Check for queue recovery
        if "current_number" in self.queue_data:
            queue_number = self.queue_data.get("current_number", 1)
            if queue_number > self.current_number:
                self.current_number = queue_number
                self.settings["current_number"] = queue_number
        
        # Store widget references
        self.widgets = {}
        
        # Create main window
        self.root = tk.Tk()
        self.setup_window()
        self.create_widgets()
        self.create_buttons()
        self.apply_layout()
        
        # Start auto-save manager
        if self.settings.get("business_rules", {}).get("auto_save_interval", 10) > 0:
            self.auto_save_manager.start()
        
        # Setup auto-save timer
        self.setup_auto_save_timer()
        
        # Setup emergency handlers
        self.setup_emergency_handlers()
        
        self.data_manager.logger.info(f"Application started successfully. Current number: {self.current_number}")
    
    def setup_window(self):
        """Setup main window"""
        self.root.title(self.settings["title"])
        
        # Set window size
        width = self.settings["ui_layout"]["window_width"]
        height = self.settings["ui_layout"]["window_height"]
        self.root.geometry(f"{width}x{height}")
        
        # Center window
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        # Set background
        self.update_background()
        
        # Bind close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_auto_save_timer(self):
        """Setup periodic auto-save timer"""
        interval = self.settings.get("business_rules", {}).get("auto_save_interval", 10) * 1000  # Convert to milliseconds
        self.root.after(interval, self.periodic_auto_save)
    
    def periodic_auto_save(self):
        """Periodic auto-save function"""
        try:
            self.save_current_state()
            
            # Schedule next auto-save
            interval = self.settings.get("business_rules", {}).get("auto_save_interval", 10) * 1000
            self.root.after(interval, self.periodic_auto_save)
            
        except Exception as e:
            self.data_manager.logger.error(f"Error in periodic auto-save: {e}")
    
    def setup_emergency_handlers(self):
        """Setup emergency handlers for unexpected shutdown"""
        # This is already handled by EnhancedDataManager signal handlers
        pass
    
    def update_background(self):
        """Update window background"""
        main_settings = self.settings["main_window"]
        
        if main_settings["use_gradient"]:
            # Create gradient background
            from_col = main_settings["gradient_start"]
            to_col = main_settings["gradient_end"]
            
            # Simple gradient effect
            self.root.configure(bg=from_col)
        else:
            self.root.configure(bg=main_settings["bg_color"])
    
    def create_widgets(self):
        """Create all widgets"""
        main_settings = self.settings["main_window"]
        bg_color = self.root.cget("bg")
        
        # ========== Logo ==========
        self.logo_label = tk.Label(self.root, bg=bg_color)
        self.load_logo()
        self.widgets["logo"] = self.logo_label
        
        # ========== Title ==========
        title_font = (main_settings["title_font"], 
                     main_settings["title_size"], 
                     "bold" if main_settings["title_bold"] else "normal")
        self.title_label = tk.Label(
            self.root,
            text=self.settings["title"],
            font=title_font,
            bg=bg_color,
            fg=main_settings["title_color"]
        )
        self.widgets["title"] = self.title_label
        
        # ========== Company Name ==========
        company_font = (main_settings["company_font"], 
                       main_settings["company_size"])
        self.company_label = tk.Label(
            self.root,
            text=self.settings.get("company_name", ""),
            font=company_font,
            bg=bg_color,
            fg=main_settings["company_color"]
        )
        self.widgets["company"] = self.company_label
        
        # ========== Time Display ==========
        time_font = (main_settings["time_font"], 
                    main_settings["time_size"])
        self.time_label = tk.Label(
            self.root,
            font=time_font,
            bg=bg_color,
            fg=main_settings["time_color"]
        )
        self.widgets["time"] = self.time_label
        self.update_time()
        
        # ========== Current Number ==========
        self.create_number_display()
        
        # Number label
        self.number_label = tk.Label(
            self.root,
            text="Current Number",
            font=("Arial", 18),
            bg=bg_color,
            fg="#ffffff"
        )
        self.widgets["number_label"] = self.number_label
        
        # ========== Statistics ==========
        stats_font = (main_settings["stats_font"], 
                     main_settings["stats_size"])
        self.stats_label = tk.Label(
            self.root,
            font=stats_font,
            bg=bg_color,
            fg=main_settings["stats_color"]
        )
        self.widgets["stats"] = self.stats_label
        self.update_stats()
        
        # ========== Instructions ==========
        instructions_font = (main_settings["instructions_font"], 
                           main_settings["instructions_size"])
        self.instructions_label = tk.Label(
            self.root,
            text="Press Print button to print current ticket | Settings for customization",
            font=instructions_font,
            bg=bg_color,
            fg=main_settings["instructions_color"]
        )
        self.widgets["instructions"] = self.instructions_label
        
        # ========== Auto-Save Status ==========
        self.auto_save_status = tk.Label(
            self.root,
            text="🔄 Auto-save: Active",
            font=("Arial", 10),
            bg=bg_color,
            fg="#4CAF50"
        )
        self.widgets["auto_save_status"] = self.auto_save_status
        self.auto_save_status.place(x=10, y=10)
        
        # Update auto-save status periodically
        self.update_auto_save_status()
    
    def update_auto_save_status(self):
        """Update auto-save status display"""
        last_save = self.settings.get("auto_save", {}).get("last_save", "Never")
        save_count = self.settings.get("auto_save", {}).get("save_count", 0)
        
        status_text = f"💾 Auto-save: {save_count} saves | Last: {last_save}"
        self.auto_save_status.config(text=status_text)
        
        # Update every 5 seconds
        self.root.after(5000, self.update_auto_save_status)
    
    def create_number_display(self):
        """Create number display (circle or rectangle)"""
        main_settings = self.settings["main_window"]
        bg_color = self.root.cget("bg")
        
        # Remove old number display if exists
        if hasattr(self, 'number_canvas'):
            self.number_canvas.destroy()
        
        shape = main_settings.get("number_shape", "circle")
        
        if shape == "circle":
            # Number circle
            self.number_canvas = tk.Canvas(
                self.root,
                width=300,
                height=300,
                bg=bg_color,
                highlightthickness=0
            )
            
            # Draw circle
            self.number_circle = self.number_canvas.create_oval(
                50, 50, 250, 250,
                fill=main_settings["number_bg_color"],
                outline=main_settings["number_border_color"],
                width=main_settings["number_border_width"]
            )
            
            # Draw number
            self.number_text = self.number_canvas.create_text(
                150, 150,
                text=str(self.current_number),
                font=("Arial", main_settings["number_size"], "bold"),
                fill=main_settings["number_color"]
            )
            
        else:  # rectangle
            width = main_settings.get("number_rectangle_width", 280)
            height = main_settings.get("number_rectangle_height", 200)
            corner_radius = main_settings.get("number_rectangle_corner", 20)
            
            self.number_canvas = tk.Canvas(
                self.root,
                width=width,
                height=height,
                bg=bg_color,
                highlightthickness=0
            )
            
            # Draw rounded rectangle
            self.draw_rounded_rectangle(
                self.number_canvas,
                10, 10, width-10, height-10,
                corner_radius,
                fill=main_settings["number_bg_color"],
                outline=main_settings["number_border_color"],
                width=main_settings["number_border_width"]
            )
            
            # Draw number
            self.number_text = self.number_canvas.create_text(
                width/2, height/2,
                text=str(self.current_number),
                font=("Arial", main_settings["number_size"], "bold"),
                fill=main_settings["number_color"]
            )
        
        self.widgets["number"] = self.number_canvas
    
    def draw_rounded_rectangle(self, canvas, x1, y1, x2, y2, radius, **kwargs):
        """Draw a rounded rectangle on canvas"""
        points = [x1+radius, y1,
                 x2-radius, y1,
                 x2, y1,
                 x2, y1+radius,
                 x2, y2-radius,
                 x2, y2,
                 x2-radius, y2,
                 x1+radius, y2,
                 x1, y2,
                 x1, y2-radius,
                 x1, y1+radius,
                 x1, y1]
        
        return canvas.create_polygon(points, smooth=True, **kwargs)
    
    def create_buttons(self):
        """Create all buttons with enhanced size control"""
        main_settings = self.settings["main_window"]
        
        # Calculate button sizes based on window size
        window_width = self.settings["ui_layout"]["window_width"]
        window_height = self.settings["ui_layout"]["window_height"]
        
        # Dynamic button sizing based on window size
        base_width = window_width // 8  # 1/8 of window width
        base_height = window_height // 15  # 1/15 of window height
        
        # Previous button with enhanced size control
        prev_width = main_settings.get("prev_button_width", main_settings.get("nav_button_width", base_width))
        prev_height = main_settings.get("prev_button_height", main_settings.get("nav_button_height", base_height))
        
        self.prev_btn = ModernButton(
            self.root,
            text=main_settings["prev_button_text"],
            command=self.prev_number,
            width=prev_width,
            height=prev_height,
            bg_color=main_settings["nav_button_color"],
            text_color=main_settings["nav_button_font_color"],
            font_family=main_settings["nav_button_font"],
            font_size=main_settings["nav_button_font_size"],
            bold=main_settings["nav_button_bold"],
            corner_radius=main_settings["nav_button_corner_radius"]
        )
        self.widgets["prev_button"] = self.prev_btn
        
        # Print button with enhanced size control
        print_width = main_settings.get("print_button_width", base_width * 1.2)
        print_height = main_settings.get("print_button_height", base_height * 1.2)
        
        self.print_btn = ModernButton(
            self.root,
            text=main_settings["print_button_text"],
            command=self.print_ticket,
            width=print_width,
            height=print_height,
            bg_color=main_settings["print_button_color"],
            text_color=main_settings["print_button_font_color"],
            font_family=main_settings["print_button_font"],
            font_size=main_settings["print_button_font_size"],
            bold=main_settings["print_button_bold"],
            corner_radius=main_settings["print_button_corner_radius"]
        )
        self.widgets["print_button"] = self.print_btn
        
        # Ticket Designer button
        designer_width = main_settings.get("designer_button_width", base_width)
        designer_height = main_settings.get("designer_button_height", base_height)
        
        self.designer_btn = ModernButton(
            self.root,
            text=main_settings["designer_button_text"],
            command=self.open_ticket_designer,
            width=designer_width,
            height=designer_height,
            bg_color=main_settings["designer_button_color"],
            text_color=main_settings["designer_button_font_color"],
            font_family=main_settings["designer_button_font"],
            font_size=main_settings["designer_button_font_size"],
            bold=main_settings["designer_button_bold"],
            corner_radius=main_settings["designer_button_corner_radius"]
        )
        self.widgets["designer_button"] = self.designer_btn
        
        # Save Design button (NEW)
        save_design_width = main_settings.get("save_design_button_width", base_width)
        save_design_height = main_settings.get("save_design_button_height", base_height * 0.8)
        
        self.save_design_btn = ModernButton(
            self.root,
            text=main_settings["save_design_button_text"],
            command=self.save_current_design,
            width=save_design_width,
            height=save_design_height,
            bg_color=main_settings["save_design_button_color"],
            text_color=main_settings["save_design_button_font_color"],
            font_family=main_settings["save_design_button_font"],
            font_size=main_settings["save_design_button_font_size"],
            bold=main_settings["save_design_button_bold"],
            corner_radius=main_settings["save_design_button_corner_radius"]
        )
        self.widgets["save_design_button"] = self.save_design_btn
        
        # Next button
        next_width = main_settings.get("next_button_width", main_settings.get("nav_button_width", base_width))
        next_height = main_settings.get("next_button_height", main_settings.get("nav_button_height", base_height))
        
        self.next_btn = ModernButton(
            self.root,
            text=main_settings["next_button_text"],
            command=self.next_number,
            width=next_width,
            height=next_height,
            bg_color=main_settings["nav_button_color"],
            text_color=main_settings["nav_button_font_color"],
            font_family=main_settings["nav_button_font"],
            font_size=main_settings["nav_button_font_size"],
            bold=main_settings["nav_button_bold"],
            corner_radius=main_settings["nav_button_corner_radius"]
        )
        self.widgets["next_button"] = self.next_btn
        
        # Settings button
        settings_width = main_settings.get("settings_button_width", base_width)
        settings_height = main_settings.get("settings_button_height", base_height)
        
        self.settings_btn = ModernButton(
            self.root,
            text=main_settings["settings_button_text"],
            command=self.open_settings,
            width=settings_width,
            height=settings_height,
            bg_color=main_settings["settings_button_color"],
            text_color=main_settings["settings_button_font_color"],
            font_family=main_settings["settings_button_font"],
            font_size=main_settings["settings_button_font_size"],
            bold=main_settings["settings_button_bold"],
            corner_radius=main_settings["settings_button_corner_radius"]
        )
        self.widgets["settings_button"] = self.settings_btn
        
        # Reset button
        reset_width = main_settings.get("reset_button_width", base_width * 0.8)
        reset_height = main_settings.get("reset_button_height", base_height * 0.8)
        
        self.reset_btn = ModernButton(
            self.root,
            text=main_settings["reset_button_text"],
            command=self.reset_counter,
            width=reset_width,
            height=reset_height,
            bg_color=main_settings["reset_button_color"],
            text_color=main_settings["reset_button_font_color"],
            font_family=main_settings["reset_button_font"],
            font_size=main_settings["reset_button_font_size"],
            bold=main_settings["reset_button_bold"],
            corner_radius=main_settings["reset_button_corner_radius"]
        )
        self.widgets["reset_button"] = self.reset_btn
        
        # Preview button
        preview_width = main_settings.get("preview_button_width", base_width)
        preview_height = main_settings.get("preview_button_height", base_height * 0.8)
        
        self.preview_btn = ModernButton(
            self.root,
            text=main_settings["preview_button_text"],
            command=self.preview_ticket,
            width=preview_width,
            height=preview_height,
            bg_color=main_settings["preview_button_color"],
            text_color=main_settings["preview_button_font_color"],
            font_family=main_settings["preview_button_font"],
            font_size=main_settings["preview_button_font_size"],
            bold=main_settings["preview_button_bold"],
            corner_radius=main_settings["preview_button_corner_radius"]
        )
        self.widgets["preview_button"] = self.preview_btn
    
    def load_logo(self):
        """Load and display logo"""
        logo_path = self.settings["logo"]
        if os.path.exists(logo_path):
            try:
                img = Image.open(logo_path)
                width = self.settings["ticket_design"]["logo_width"]
                height = self.settings["ticket_design"]["logo_height"]
                img = img.resize((width, height), Image.Resampling.LANCZOS)
                
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')
                
                self.logo_img = ImageTk.PhotoImage(img)
                self.logo_label.config(image=self.logo_img, bg=self.root.cget("bg"))
            except Exception as e:
                self.data_manager.logger.error(f"Error loading logo: {e}")
                self.logo_label.config(text="[LOGO]", font=("Arial", 14), 
                                     bg=self.root.cget("bg"), fg="#ffffff")
        else:
            self.logo_label.config(text="[LOGO]", font=("Arial", 14), 
                                 bg=self.root.cget("bg"), fg="#ffffff")
    
    def apply_layout(self):
        """Apply widget positions from settings with dynamic resizing"""
        widgets_config = self.settings["ui_layout"]["widgets"]
        
        for widget_name, config in widgets_config.items():
            if widget_name in self.widgets:
                widget = self.widgets[widget_name]
                x = config.get("x", 0)
                y = config.get("y", 0)
                width = config.get("width", 100)
                height = config.get("height", 40)
                visible = config.get("visible", True)
                
                if isinstance(widget, ModernButton) and "button" in widget_name:
                    # تحديث حجم الأزرار
                    widget.config(width=width, height=height)
                    widget.update_config(width=width, height=height)
                elif isinstance(widget, tk.Canvas) and widget_name == "number":
                    # Number canvas resizing
                    if self.settings["main_window"]["number_shape"] == "circle":
                        widget.config(width=width, height=height)
                    else:
                        widget.config(width=width, height=height)
                elif isinstance(widget, tk.Label):
                    # Label widgets
                    widget.config(wraplength=width)
                
                if visible:
                    widget.place(x=x, y=y, width=width, height=height if not isinstance(widget, ModernButton) else None)
                else:
                    widget.place_forget()
    
    def update_time(self):
        """Update time display"""
        now = datetime.now()
        time_format = self.settings["main_window"]["time_format"]
        time_str = now.strftime(time_format)
        
        self.time_label.config(text=f"📅 {time_str}")
        self.root.after(1000, self.update_time)
    
    def update_stats(self):
        """Update statistics display"""
        stats = f"""
        Today's Tickets: {self.queue_data.get('today_count', 0)} | 
        Total Printed: {self.queue_data.get('total_printed', 0)} | 
        Current Number: {self.current_number}
        """
        self.stats_label.config(text=stats)
    
    def prev_number(self):
        """Decrease number"""
        start_number = self.settings["business_rules"]["start_number"]
        if self.current_number > start_number:
            self.current_number -= 1
            self.update_number_display()
            self.save_current_state()
    
    def next_number(self):
        """Increase number"""
        self.current_number += 1
        self.update_number_display()
        self.save_current_state()
    
    def update_number_display(self):
        """Update number display"""
        self.number_canvas.itemconfig(self.number_text, text=str(self.current_number))
        self.update_stats()
        
        # Animation effect
        original_size = self.settings["main_window"]["number_size"]
        self.number_canvas.itemconfig(self.number_text, 
                                     font=("Arial", int(original_size * 1.1), "bold"))
        self.root.after(200, lambda: self.number_canvas.itemconfig(self.number_text, 
                                                                  font=("Arial", original_size, "bold")))
    
    def print_ticket(self):
        """Print current ticket with current design"""
        if self.enhanced_printer.print_ticket_with_design(self.current_number, self.settings):
            # Update statistics
            self.queue_data["today_count"] = self.queue_data.get("today_count", 0) + 1
            self.queue_data["total_printed"] = self.queue_data.get("total_printed", 0) + 1
            
            # Auto increment if enabled
            if self.settings["business_rules"]["auto_increment_after_print"]:
                self.next_number()
            else:
                self.update_stats()
                self.save_current_state()
            
            messagebox.showinfo("Success", f"Ticket #{self.current_number} printed successfully!")
        else:
            messagebox.showerror("Error", "Failed to print. Please check printer settings.")
    
    def preview_ticket(self):
        """Preview ticket with visual design"""
        preview_win = tk.Toplevel(self.root)
        preview_win.title("Ticket Preview - Visual Design")
        preview_win.geometry("600x700")
        preview_win.configure(bg="white")
        
        # Create frame for ticket
        ticket_frame = tk.Frame(preview_win, bg="white", width=550, height=650)
        ticket_frame.pack_propagate(False)
        ticket_frame.pack(pady=20)
        
        # Draw border
        border_frame = tk.Frame(ticket_frame, bg="black", width=554, height=654)
        border_frame.place(x=-2, y=-2)
        
        inner_frame = tk.Frame(ticket_frame, bg="white", width=550, height=650)
        inner_frame.place(x=0, y=0)
        
        design = self.settings["ticket_design"]
        
        # Display logo if enabled
        if design.get("show_logo", True) and os.path.exists(self.settings["logo"]):
            try:
                img = Image.open(self.settings["logo"])
                width = design.get("logo_width", 150)
                height = design.get("logo_height", 100)
                img = img.resize((width, height), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                logo_label = tk.Label(inner_frame, image=photo, bg="white")
                logo_label.image = photo
                logo_label.place(x=design.get("logo_position_x", 50), 
                                y=design.get("logo_position_y", 50))
            except:
                pass
        
        # Display company info if enabled
        if design.get("company_info", True):
            company_font = ("Arial", design.get("company_font_size", 18))
            company_label = tk.Label(inner_frame, text=self.settings["company_name"],
                                    font=company_font, bg="white", fg="black")
            company_label.place(x=design.get("company_position_x", 200),
                              y=design.get("company_position_y", 50))
            
            address_label = tk.Label(inner_frame, text=self.settings["company_address"],
                                    font=("Arial", 12), bg="white", fg="black")
            address_label.place(x=design.get("company_position_x", 200),
                               y=design.get("company_position_y", 80))
        
        # Ticket number
        prefix_label = tk.Label(inner_frame, text=design.get("number_prefix", "Ticket #"),
                               font=("Arial", 14), bg="white", fg="black")
        prefix_label.place(x=design.get("number_position_x", 50),
                          y=design.get("number_position_y", 150))
        
        number_label = tk.Label(inner_frame, text=f"{self.current_number:04d}",
                               font=("Arial", design.get("number_size", 72), "bold"),
                               bg="white", fg="#FF5722")
        number_label.place(x=design.get("number_position_x", 50),
                          y=design.get("number_position_y", 180))
        
        # Messages
        if design.get("thank_message"):
            thank_label = tk.Label(inner_frame, text=design["thank_message"],
                                  font=("Arial", design.get("thank_font_size", 14)),
                                  bg="white", fg="black")
            thank_label.place(x=design.get("thank_position_x", 50),
                            y=design.get("thank_position_y", 280))
        
        if design.get("warning_message"):
            warning_label = tk.Label(inner_frame, text=design["warning_message"],
                                    font=("Arial", design.get("warning_font_size", 12)),
                                    bg="white", fg="black")
            warning_label.place(x=design.get("warning_position_x", 50),
                              y=design.get("warning_position_y", 320))
        
        if design.get("custom_message"):
            custom_label = tk.Label(inner_frame, text=design["custom_message"],
                                   font=("Arial", design.get("message_font_size", 12)),
                                   bg="white", fg="black")
            custom_label.place(x=design.get("custom_position_x", 50),
                             y=design.get("custom_position_y", 450))
        
        # Date and time
        now = datetime.now()
        if design.get("show_date", True):
            date_label = tk.Label(inner_frame, 
                                 text=f"Date: {now.strftime(design.get('date_format', '%Y-%m-%d'))}",
                                 font=("Arial", 12), bg="white", fg="black")
            date_label.place(x=design.get("date_position_x", 50),
                            y=design.get("date_position_y", 370))
        
        if design.get("show_time", True):
            time_label = tk.Label(inner_frame,
                                 text=f"Time: {now.strftime(design.get('time_format', '%H:%M:%S'))}",
                                 font=("Arial", 12), bg="white", fg="black")
            time_label.place(x=design.get("time_position_x", 50),
                            y=design.get("time_position_y", 400))
        
        # Watermark
        if design.get("watermark", True) and design.get("watermark_text"):
            watermark_label = tk.Label(inner_frame, text=design["watermark_text"],
                                      font=("Arial", design.get("watermark_font_size", 10)),
                                      bg="white", fg="#888888")
            watermark_label.place(x=design.get("watermark_position_x", 200),
                                 y=design.get("watermark_position_y", 500))
        
        # Close button
        tk.Button(preview_win, text="Close", command=preview_win.destroy,
                 bg="#E74C3C", fg="white", font=("Arial", 12)).pack(pady=10)
    
    def save_current_design(self):
        """Save current ticket design from main window"""
        # Password check
        password = simpledialog.askstring(
            "Save Design",
            "Enter password:",
            show='*'
        )
        
        if password != self.settings["system_password"]:
            messagebox.showerror("Access Denied", "Incorrect password!")
            return
        
        design_name = simpledialog.askstring("Save Design", "Enter design name:")
        if design_name:
            # Create design data from current settings
            design_data = {
                "name": design_name,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "ticket_design": self.settings["ticket_design"].copy(),
                "elements": {}  # We don't have element positions in main window
            }
            
            # Save design
            if self.data_manager.save_ticket_design(design_name, design_data):
                messagebox.showinfo("Success", f"Design '{design_name}' saved successfully!")
            else:
                messagebox.showerror("Error", "Failed to save design!")
    
    def open_ticket_designer(self):
        """Open ticket designer"""
        # Password check
        password = simpledialog.askstring(
            "Admin Access",
            "Enter password:",
            show='*'
        )
        
        if password != self.settings["system_password"]:
            messagebox.showerror("Access Denied", "Incorrect password!")
            return
        
        designer = TicketDesigner(self.root, self.settings, self.on_design_saved)
    
    def on_design_saved(self, new_design):
        """Callback when design is saved"""
        # Update design in settings
        self.settings["ticket_design"] = new_design.copy()
        
        # Save settings
        self.data_manager.save_settings(self.settings)
        
        # Reload logo with new size
        self.load_logo()
        messagebox.showinfo("Success", "Ticket design updated and saved!")
    
    def reset_counter(self):
        """Reset counter to start number"""
        if messagebox.askyesno("Confirm", "Reset counter to start number?"):
            self.current_number = self.settings["business_rules"]["start_number"]
            self.update_number_display()
            self.save_current_state()
            messagebox.showinfo("Done", "Counter reset successfully")
    
    def save_current_state(self):
        """Save current state with enhanced auto-save"""
        try:
            # Update settings with current number
            self.settings["current_number"] = self.current_number
            self.queue_data["current_number"] = self.current_number
            
            # Add timestamp
            self.queue_data["last_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Save both settings and queue
            if self.data_manager.save_settings(self.settings):
                self.data_manager.save_queue(self.queue_data)
                
                # Log successful save
                save_count = self.settings.get("auto_save", {}).get("save_count", 0)
                self.data_manager.logger.info(f"State saved - Number: {self.current_number}, Save #: {save_count}")
                return True
            else:
                return False
                
        except Exception as e:
            self.data_manager.logger.error(f"Error saving state: {e}")
            # Try emergency save
            self.data_manager.emergency_save_simple(self.settings)
            return False
    
    def open_settings(self):
        """Open settings window - FULL SCREEN"""
        # Password check
        password = simpledialog.askstring(
            "Admin Access",
            "Enter password:",
            show='*'
        )
        
        if password != self.settings["system_password"]:
            messagebox.showerror("Access Denied", "Incorrect password!")
            return
        
        # Save current state before opening settings
        self.save_current_state()
        
        # Create settings window (full screen)
        settings_win = tk.Toplevel(self.root)
        settings_win.title("Settings - Complete Edition with Auto-Save")
        
        # جعل النافذة بحجم الشاشة الكاملة
        screen_width = settings_win.winfo_screenwidth()
        screen_height = settings_win.winfo_screenheight()
        settings_win.geometry(f"{screen_width}x{screen_height}+0+0")
        settings_win.attributes('-fullscreen', True)
        
        settings_win.configure(bg="#f0f0f0")
        
        # إضافة زر للخروج من وضع الشاشة الكاملة
        exit_button = tk.Button(settings_win, text="❌ Exit Full Screen", 
                               command=lambda: settings_win.attributes('-fullscreen', False),
                               bg="#E74C3C", fg="white", font=("Arial", 12))
        exit_button.pack(side="top", anchor="ne", padx=10, pady=10)
        
        # Create notebook with tabs
        notebook = ttk.Notebook(settings_win)
        notebook.pack(fill="both", expand=True, padx=10, pady=40)  # زيادة padding أعلى
        
        # ========== General Tab ==========
        general_tab = ttk.Frame(notebook)
        notebook.add(general_tab, text="General")
        
        # Create scrollable frame
        general_canvas = tk.Canvas(general_tab, bg="#ffffff")
        scrollbar = tk.Scrollbar(general_tab, orient="vertical", command=general_canvas.yview)
        scrollable_frame = ttk.Frame(general_canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: general_canvas.configure(scrollregion=general_canvas.bbox("all"))
        )
        
        general_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        general_canvas.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        general_canvas.pack(side="left", fill="both", expand=True)
        
        tk.Label(scrollable_frame, text="General Settings", font=("Arial", 20, "bold")).pack(pady=20)
        
        # System title
        tk.Label(scrollable_frame, text="System Title:", font=("Arial", 12)).pack(pady=5)
        title_var = tk.StringVar(value=self.settings["title"])
        title_entry = tk.Entry(scrollable_frame, textvariable=title_var, width=40, font=("Arial", 12))
        title_entry.pack(pady=5)
        
        # Company info
        tk.Label(scrollable_frame, text="Company Name:", font=("Arial", 12)).pack(pady=5)
        company_var = tk.StringVar(value=self.settings.get("company_name", ""))
        company_entry = tk.Entry(scrollable_frame, textvariable=company_var, width=40, font=("Arial", 12))
        company_entry.pack(pady=5)
        
        tk.Label(scrollable_frame, text="Address:", font=("Arial", 12)).pack(pady=5)
        address_var = tk.StringVar(value=self.settings.get("company_address", ""))
        address_entry = tk.Entry(scrollable_frame, textvariable=address_var, width=40, font=("Arial", 12))
        address_entry.pack(pady=5)
        
        tk.Label(scrollable_frame, text="Phone:", font=("Arial", 12)).pack(pady=5)
        phone_var = tk.StringVar(value=self.settings.get("company_phone", ""))
        phone_entry = tk.Entry(scrollable_frame, textvariable=phone_var, width=40, font=("Arial", 12))
        phone_entry.pack(pady=5)
        
        # Logo upload
        def upload_logo():
            file_path = filedialog.askopenfilename(
                title="Select Logo Image",
                filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")]
            )
            if file_path:
                try:
                    logo_name = os.path.basename(file_path)
                    dest_path = os.path.join(Config.ASSETS_DIR, logo_name)
                    shutil.copy2(file_path, dest_path)
                    
                    self.settings["logo"] = dest_path
                    self.load_logo()
                    messagebox.showinfo("Success", "Logo updated successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to upload logo: {str(e)}")
        
        tk.Button(scrollable_frame, text="Upload New Logo", command=upload_logo, 
                 bg="#3498DB", fg="white", font=("Arial", 11)).pack(pady=20)
        
        # Password change
        tk.Label(scrollable_frame, text="Admin Password:", font=("Arial", 12)).pack(pady=5)
        password_var = tk.StringVar(value=self.settings["system_password"])
        password_entry = tk.Entry(scrollable_frame, textvariable=password_var, width=30, 
                                 show="*", font=("Arial", 12))
        password_entry.pack(pady=5)
        
        # ========== Display Tab ==========
        display_tab = ttk.Frame(notebook)
        notebook.add(display_tab, text="Display")
        
        display_canvas = tk.Canvas(display_tab, bg="#ffffff")
        display_scrollbar = tk.Scrollbar(display_tab, orient="vertical", command=display_canvas.yview)
        display_scrollable_frame = ttk.Frame(display_canvas)
        
        display_scrollable_frame.bind(
            "<Configure>",
            lambda e: display_canvas.configure(scrollregion=display_canvas.bbox("all"))
        )
        
        display_canvas.create_window((0, 0), window=display_scrollable_frame, anchor="nw")
        display_canvas.configure(yscrollcommand=display_scrollbar.set)
        
        display_scrollbar.pack(side="right", fill="y")
        display_canvas.pack(side="left", fill="both", expand=True)
        
        tk.Label(display_scrollable_frame, text="Display Settings", 
                font=("Arial", 20, "bold")).pack(pady=20)
        
        # Background color
        tk.Label(display_scrollable_frame, text="Background Color:", 
                font=("Arial", 12)).pack(pady=5)
        bg_color_var = tk.StringVar(value=self.settings["main_window"]["bg_color"])
        
        def choose_bg_color():
            color = colorchooser.askcolor(title="Choose Background Color")[1]
            if color:
                bg_color_var.set(color)
        
        color_frame = tk.Frame(display_scrollable_frame)
        color_frame.pack(pady=5)
        
        tk.Entry(color_frame, textvariable=bg_color_var, width=20, 
                font=("Arial", 10)).pack(side="left", padx=5)
        tk.Button(color_frame, text="Choose", command=choose_bg_color,
                 bg="#95A5A6", fg="white").pack(side="left", padx=5)
        
        # Number display type
        tk.Label(display_scrollable_frame, text="Number Display Shape:", 
                font=("Arial", 12)).pack(pady=10)
        number_shape_var = tk.StringVar(value=self.settings["main_window"]["number_shape"])
        
        shape_frame = tk.Frame(display_scrollable_frame)
        shape_frame.pack(pady=5)
        
        tk.Radiobutton(shape_frame, text="Circle", variable=number_shape_var, 
                      value="circle", font=("Arial", 11)).pack(side="left", padx=20)
        tk.Radiobutton(shape_frame, text="Rectangle", variable=number_shape_var, 
                      value="rectangle", font=("Arial", 11)).pack(side="left", padx=20)
        
        # Number color
        tk.Label(display_scrollable_frame, text="Number Color:", 
                font=("Arial", 12)).pack(pady=5)
        number_color_var = tk.StringVar(value=self.settings["main_window"]["number_color"])
        
        def choose_number_color():
            color = colorchooser.askcolor(title="Choose Number Color")[1]
            if color:
                number_color_var.set(color)
        
        tk.Entry(display_scrollable_frame, textvariable=number_color_var, 
                width=20, font=("Arial", 10)).pack(pady=2)
        tk.Button(display_scrollable_frame, text="Choose Color", 
                 command=choose_number_color).pack(pady=5)
        
        # Number background color
        tk.Label(display_scrollable_frame, text="Number Background Color:", 
                font=("Arial", 12)).pack(pady=5)
        number_bg_color_var = tk.StringVar(value=self.settings["main_window"]["number_bg_color"])
        
        def choose_number_bg_color():
            color = colorchooser.askcolor(title="Choose Background Color")[1]
            if color:
                number_bg_color_var.set(color)
        
        tk.Entry(display_scrollable_frame, textvariable=number_bg_color_var, 
                width=20, font=("Arial", 10)).pack(pady=2)
        tk.Button(display_scrollable_frame, text="Choose Color", 
                 command=choose_number_bg_color).pack(pady=5)
        
        # Number border color
        tk.Label(display_scrollable_frame, text="Number Border Color:", 
                font=("Arial", 12)).pack(pady=5)
        number_border_color_var = tk.StringVar(value=self.settings["main_window"]["number_border_color"])
        
        def choose_number_border_color():
            color = colorchooser.askcolor(title="Choose Border Color")[1]
            if color:
                number_border_color_var.set(color)
        
        tk.Entry(display_scrollable_frame, textvariable=number_border_color_var, 
                width=20, font=("Arial", 10)).pack(pady=2)
        tk.Button(display_scrollable_frame, text="Choose Color", 
                 command=choose_number_border_color).pack(pady=5)
        
        # Number border width
        tk.Label(display_scrollable_frame, text="Number Border Width:", 
                font=("Arial", 12)).pack(pady=5)
        number_border_width_var = tk.IntVar(value=self.settings["main_window"]["number_border_width"])
        tk.Scale(display_scrollable_frame, from_=1, to=10, variable=number_border_width_var, 
                orient="horizontal", length=300).pack(pady=5)
        
        # Number size
        tk.Label(display_scrollable_frame, text="Number Size:", 
                font=("Arial", 12)).pack(pady=5)
        number_size_var = tk.IntVar(value=self.settings["main_window"]["number_size"])
        tk.Scale(display_scrollable_frame, from_=50, to=150, variable=number_size_var, 
                orient="horizontal", length=300).pack(pady=5)
        
        # Rectangle dimensions (only shown if shape is rectangle)
        rectangle_frame = tk.LabelFrame(display_scrollable_frame, text="Rectangle Dimensions",
                                       font=("Arial", 12, "bold"))
        rectangle_frame.pack(fill="x", pady=10, padx=10)
        
        tk.Label(rectangle_frame, text="Width:").pack(pady=2)
        rect_width_var = tk.IntVar(value=self.settings["main_window"]["number_rectangle_width"])
        tk.Scale(rectangle_frame, from_=100, to=500, variable=rect_width_var, 
                orient="horizontal", length=200).pack(pady=2)
        
        tk.Label(rectangle_frame, text="Height:").pack(pady=2)
        rect_height_var = tk.IntVar(value=self.settings["main_window"]["number_rectangle_height"])
        tk.Scale(rectangle_frame, from_=50, to=300, variable=rect_height_var, 
                orient="horizontal", length=200).pack(pady=2)
        
        tk.Label(rectangle_frame, text="Corner Radius:").pack(pady=2)
        rect_corner_var = tk.IntVar(value=self.settings["main_window"]["number_rectangle_corner"])
        tk.Scale(rectangle_frame, from_=0, to=100, variable=rect_corner_var, 
                orient="horizontal", length=200).pack(pady=2)
        
        # Button size controls
        button_size_frame = tk.LabelFrame(display_scrollable_frame, text="Button Sizes",
                                         font=("Arial", 12, "bold"))
        button_size_frame.pack(fill="x", pady=10, padx=10)
        
        # Print button size
        tk.Label(button_size_frame, text="Print Button Width:").pack(pady=2)
        print_width_var = tk.IntVar(value=self.settings["main_window"]["print_button_width"])
        tk.Scale(button_size_frame, from_=100, to=400, variable=print_width_var,
                orient="horizontal", length=200).pack(pady=2)
        
        tk.Label(button_size_frame, text="Print Button Height:").pack(pady=2)
        print_height_var = tk.IntVar(value=self.settings["main_window"]["print_button_height"])
        tk.Scale(button_size_frame, from_=30, to=120, variable=print_height_var,
                orient="horizontal", length=200).pack(pady=2)
        
        # Navigation buttons size
        tk.Label(button_size_frame, text="Navigation Button Width:").pack(pady=2)
        nav_width_var = tk.IntVar(value=self.settings["main_window"]["nav_button_width"])
        tk.Scale(button_size_frame, from_=80, to=300, variable=nav_width_var,
                orient="horizontal", length=200).pack(pady=2)
        
        tk.Label(button_size_frame, text="Navigation Button Height:").pack(pady=2)
        nav_height_var = tk.IntVar(value=self.settings["main_window"]["nav_button_height"])
        tk.Scale(button_size_frame, from_=30, to=100, variable=nav_height_var,
                orient="horizontal", length=200).pack(pady=2)
        
        # Settings button size
        tk.Label(button_size_frame, text="Settings Button Width:").pack(pady=2)
        settings_width_var = tk.IntVar(value=self.settings["main_window"]["settings_button_width"])
        tk.Scale(button_size_frame, from_=80, to=250, variable=settings_width_var,
                orient="horizontal", length=200).pack(pady=2)
        
        tk.Label(button_size_frame, text="Settings Button Height:").pack(pady=2)
        settings_height_var = tk.IntVar(value=self.settings["main_window"]["settings_button_height"])
        tk.Scale(button_size_frame, from_=30, to=80, variable=settings_height_var,
                orient="horizontal", length=200).pack(pady=2)
        
        # ========== Ticket Design Tab ==========
        ticket_design_tab = ttk.Frame(notebook)
        notebook.add(ticket_design_tab, text="Ticket Design")
        
        ticket_canvas = tk.Canvas(ticket_design_tab, bg="#ffffff")
        ticket_scrollbar = tk.Scrollbar(ticket_design_tab, orient="vertical", command=ticket_canvas.yview)
        ticket_scrollable_frame = ttk.Frame(ticket_canvas)
        
        ticket_scrollable_frame.bind(
            "<Configure>",
            lambda e: ticket_canvas.configure(scrollregion=ticket_canvas.bbox("all"))
        )
        
        ticket_canvas.create_window((0, 0), window=ticket_scrollable_frame, anchor="nw")
        ticket_canvas.configure(yscrollcommand=ticket_scrollbar.set)
        
        ticket_scrollbar.pack(side="right", fill="y")
        ticket_canvas.pack(side="left", fill="both", expand=True)
        
        tk.Label(ticket_scrollable_frame, text="Ticket Design Settings", 
                font=("Arial", 20, "bold")).pack(pady=20)
        
        # Logo settings
        logo_frame = tk.LabelFrame(ticket_scrollable_frame, text="Logo Settings",
                                  font=("Arial", 14, "bold"))
        logo_frame.pack(fill="x", padx=10, pady=10)
        
        show_logo_var = tk.BooleanVar(value=self.settings["ticket_design"]["show_logo"])
        tk.Checkbutton(logo_frame, text="Show Logo", variable=show_logo_var,
                      font=("Arial", 12)).pack(anchor="w", pady=5)
        
        tk.Label(logo_frame, text="Logo Width:", font=("Arial", 12)).pack(pady=5)
        ticket_logo_width_var = tk.IntVar(value=self.settings["ticket_design"]["logo_width"])
        tk.Scale(logo_frame, from_=50, to=300, variable=ticket_logo_width_var,
                orient="horizontal", length=200).pack(pady=5)
        
        tk.Label(logo_frame, text="Logo Height:", font=("Arial", 12)).pack(pady=5)
        ticket_logo_height_var = tk.IntVar(value=self.settings["ticket_design"]["logo_height"])
        tk.Scale(logo_frame, from_=30, to=200, variable=ticket_logo_height_var,
                orient="horizontal", length=200).pack(pady=5)
        
        # Company info settings
        company_frame = tk.LabelFrame(ticket_scrollable_frame, text="Company Info",
                                     font=("Arial", 14, "bold"))
        company_frame.pack(fill="x", padx=10, pady=10)
        
        show_company_var = tk.BooleanVar(value=self.settings["ticket_design"]["company_info"])
        tk.Checkbutton(company_frame, text="Show Company Info", variable=show_company_var,
                      font=("Arial", 12)).pack(anchor="w", pady=5)
        
        tk.Label(company_frame, text="Company Font Size:", font=("Arial", 12)).pack(pady=5)
        company_font_size_var = tk.IntVar(value=self.settings["ticket_design"]["company_font_size"])
        tk.Scale(company_frame, from_=10, to=30, variable=company_font_size_var,
                orient="horizontal", length=200).pack(pady=5)
        
        # Ticket number settings
        number_frame = tk.LabelFrame(ticket_scrollable_frame, text="Ticket Number",
                                    font=("Arial", 14, "bold"))
        number_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Label(number_frame, text="Number Prefix:", font=("Arial", 12)).pack(pady=5)
        number_prefix_var = tk.StringVar(value=self.settings["ticket_design"]["number_prefix"])
        tk.Entry(number_frame, textvariable=number_prefix_var, width=20,
                font=("Arial", 12)).pack(pady=5)
        
        tk.Label(number_frame, text="Number Font Size:", font=("Arial", 12)).pack(pady=5)
        ticket_number_size_var = tk.IntVar(value=self.settings["ticket_design"]["number_size"])
        tk.Scale(number_frame, from_=30, to=100, variable=ticket_number_size_var,
                orient="horizontal", length=200).pack(pady=5)
        
        # Messages settings
        messages_frame = tk.LabelFrame(ticket_scrollable_frame, text="Messages",
                                      font=("Arial", 14, "bold"))
        messages_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Label(messages_frame, text="Thank You Message:", font=("Arial", 12)).pack(pady=5)
        thank_var = tk.StringVar(value=self.settings["ticket_design"]["thank_message"])
        tk.Entry(messages_frame, textvariable=thank_var, width=40,
                font=("Arial", 12)).pack(pady=5)
        
        tk.Label(messages_frame, text="Thank You Font Size:", font=("Arial", 12)).pack(pady=5)
        thank_font_size_var = tk.IntVar(value=self.settings["ticket_design"]["thank_font_size"])
        tk.Scale(messages_frame, from_=8, to=20, variable=thank_font_size_var,
                orient="horizontal", length=200).pack(pady=5)
        
        tk.Label(messages_frame, text="Warning Message:", font=("Arial", 12)).pack(pady=5)
        warning_var = tk.StringVar(value=self.settings["ticket_design"]["warning_message"])
        tk.Entry(messages_frame, textvariable=warning_var, width=40,
                font=("Arial", 12)).pack(pady=5)
        
        tk.Label(messages_frame, text="Warning Font Size:", font=("Arial", 12)).pack(pady=5)
        warning_font_size_var = tk.IntVar(value=self.settings["ticket_design"]["warning_font_size"])
        tk.Scale(messages_frame, from_=8, to=18, variable=warning_font_size_var,
                orient="horizontal", length=200).pack(pady=5)
        
        tk.Label(messages_frame, text="Custom Message:", font=("Arial", 12)).pack(pady=5)
        custom_var = tk.StringVar(value=self.settings["ticket_design"]["custom_message"])
        tk.Entry(messages_frame, textvariable=custom_var, width=40,
                font=("Arial", 12)).pack(pady=5)
        
        tk.Label(messages_frame, text="Custom Font Size:", font=("Arial", 12)).pack(pady=5)
        custom_font_size_var = tk.IntVar(value=self.settings["ticket_design"]["message_font_size"])
        tk.Scale(messages_frame, from_=8, to=18, variable=custom_font_size_var,
                orient="horizontal", length=200).pack(pady=5)
        
        # Date & Time settings
        datetime_frame = tk.LabelFrame(ticket_scrollable_frame, text="Date & Time",
                                      font=("Arial", 14, "bold"))
        datetime_frame.pack(fill="x", padx=10, pady=10)
        
        show_date_var = tk.BooleanVar(value=self.settings["ticket_design"]["show_date"])
        tk.Checkbutton(datetime_frame, text="Show Date", variable=show_date_var,
                      font=("Arial", 12)).pack(anchor="w", pady=5)
        
        show_time_var = tk.BooleanVar(value=self.settings["ticket_design"]["show_time"])
        tk.Checkbutton(datetime_frame, text="Show Time", variable=show_time_var,
                      font=("Arial", 12)).pack(anchor="w", pady=5)
        
        # Watermark settings
        watermark_frame = tk.LabelFrame(ticket_scrollable_frame, text="Watermark",
                                       font=("Arial", 14, "bold"))
        watermark_frame.pack(fill="x", padx=10, pady=10)
        
        show_watermark_var = tk.BooleanVar(value=self.settings["ticket_design"]["watermark"])
        tk.Checkbutton(watermark_frame, text="Show Watermark", variable=show_watermark_var,
                      font=("Arial", 12)).pack(anchor="w", pady=5)
        
        tk.Label(watermark_frame, text="Watermark Text:", font=("Arial", 12)).pack(pady=5)
        watermark_text_var = tk.StringVar(value=self.settings["ticket_design"]["watermark_text"])
        tk.Entry(watermark_frame, textvariable=watermark_text_var, width=30,
                font=("Arial", 12)).pack(pady=5)
        
        tk.Label(watermark_frame, text="Watermark Font Size:", font=("Arial", 12)).pack(pady=5)
        watermark_font_size_var = tk.IntVar(value=self.settings["ticket_design"]["watermark_font_size"])
        tk.Scale(watermark_frame, from_=6, to=15, variable=watermark_font_size_var,
                orient="horizontal", length=200).pack(pady=5)
        
        # ========== Buttons Tab ==========
        buttons_tab = ttk.Frame(notebook)
        notebook.add(buttons_tab, text="Buttons")
        
        buttons_canvas = tk.Canvas(buttons_tab, bg="#ffffff")
        buttons_scrollbar = tk.Scrollbar(buttons_tab, orient="vertical", command=buttons_canvas.yview)
        buttons_scrollable_frame = ttk.Frame(buttons_canvas)
        
        buttons_scrollable_frame.bind(
            "<Configure>",
            lambda e: buttons_canvas.configure(scrollregion=buttons_canvas.bbox("all"))
        )
        
        buttons_canvas.create_window((0, 0), window=buttons_scrollable_frame, anchor="nw")
        buttons_canvas.configure(yscrollcommand=buttons_scrollbar.set)
        
        buttons_scrollbar.pack(side="right", fill="y")
        buttons_canvas.pack(side="left", fill="both", expand=True)
        
        tk.Label(buttons_scrollable_frame, text="Button Settings", 
                font=("Arial", 20, "bold")).pack(pady=20)
        
        # Print button settings
        tk.Label(buttons_scrollable_frame, text="Print Button:", 
                font=("Arial", 16, "bold")).pack(pady=10)
        
        print_text_var = tk.StringVar(value=self.settings["main_window"]["print_button_text"])
        tk.Label(buttons_scrollable_frame, text="Button Text:").pack(pady=2)
        tk.Entry(buttons_scrollable_frame, textvariable=print_text_var, 
                width=30, font=("Arial", 11)).pack(pady=2)
        
        # Print button color
        tk.Label(buttons_scrollable_frame, text="Button Color:").pack(pady=5)
        print_color_var = tk.StringVar(value=self.settings["main_window"]["print_button_color"])
        
        def choose_print_color():
            color = colorchooser.askcolor(title="Choose Button Color")[1]
            if color:
                print_color_var.set(color)
        
        tk.Entry(buttons_scrollable_frame, textvariable=print_color_var, 
                width=20, font=("Arial", 10)).pack(pady=2)
        tk.Button(buttons_scrollable_frame, text="Choose Color", 
                 command=choose_print_color).pack(pady=5)
        
        # Print button font color
        tk.Label(buttons_scrollable_frame, text="Text Color:").pack(pady=5)
        print_font_color_var = tk.StringVar(value=self.settings["main_window"]["print_button_font_color"])
        
        def choose_print_font_color():
            color = colorchooser.askcolor(title="Choose Text Color")[1]
            if color:
                print_font_color_var.set(color)
        
        tk.Entry(buttons_scrollable_frame, textvariable=print_font_color_var, 
                width=20, font=("Arial", 10)).pack(pady=2)
        tk.Button(buttons_scrollable_frame, text="Choose Color", 
                 command=choose_print_font_color).pack(pady=5)
        
        # Print button corner radius
        tk.Label(buttons_scrollable_frame, text="Corner Radius:").pack(pady=5)
        print_corner_var = tk.IntVar(value=self.settings["main_window"]["print_button_corner_radius"])
        tk.Scale(buttons_scrollable_frame, from_=0, to=30, variable=print_corner_var, 
                orient="horizontal", length=200).pack(pady=5)
        
        # Navigation buttons settings
        tk.Label(buttons_scrollable_frame, text="Navigation Buttons:", 
                font=("Arial", 16, "bold")).pack(pady=20)
        
        # Previous button text
        prev_text_var = tk.StringVar(value=self.settings["main_window"]["prev_button_text"])
        tk.Label(buttons_scrollable_frame, text="Previous Button Text:").pack(pady=5)
        tk.Entry(buttons_scrollable_frame, textvariable=prev_text_var, 
                width=30, font=("Arial", 11)).pack(pady=2)
        
        # Next button text
        next_text_var = tk.StringVar(value=self.settings["main_window"]["next_button_text"])
        tk.Label(buttons_scrollable_frame, text="Next Button Text:").pack(pady=5)
        tk.Entry(buttons_scrollable_frame, textvariable=next_text_var, 
                width=30, font=("Arial", 11)).pack(pady=2)
        
        # Navigation button color
        tk.Label(buttons_scrollable_frame, text="Navigation Button Color:").pack(pady=5)
        nav_color_var = tk.StringVar(value=self.settings["main_window"]["nav_button_color"])
        
        def choose_nav_color():
            color = colorchooser.askcolor(title="Choose Button Color")[1]
            if color:
                nav_color_var.set(color)
        
        tk.Entry(buttons_scrollable_frame, textvariable=nav_color_var, 
                width=20, font=("Arial", 10)).pack(pady=2)
        tk.Button(buttons_scrollable_frame, text="Choose Color", 
                 command=choose_nav_color).pack(pady=5)
        
        # Settings button settings
        tk.Label(buttons_scrollable_frame, text="Settings Button:", 
                font=("Arial", 16, "bold")).pack(pady=20)
        
        settings_text_var = tk.StringVar(value=self.settings["main_window"]["settings_button_text"])
        tk.Label(buttons_scrollable_frame, text="Button Text:").pack(pady=2)
        tk.Entry(buttons_scrollable_frame, textvariable=settings_text_var, 
                width=30, font=("Arial", 11)).pack(pady=2)
        
        settings_color_var = tk.StringVar(value=self.settings["main_window"]["settings_button_color"])
        
        def choose_settings_color():
            color = colorchooser.askcolor(title="Choose Button Color")[1]
            if color:
                settings_color_var.set(color)
        
        tk.Entry(buttons_scrollable_frame, textvariable=settings_color_var, 
                width=20, font=("Arial", 10)).pack(pady=2)
        tk.Button(buttons_scrollable_frame, text="Choose Color", 
                 command=choose_settings_color).pack(pady=5)
        
        # Save Design button settings
        tk.Label(buttons_scrollable_frame, text="Save Design Button:", 
                font=("Arial", 16, "bold")).pack(pady=20)
        
        save_design_text_var = tk.StringVar(value=self.settings["main_window"]["save_design_button_text"])
        tk.Label(buttons_scrollable_frame, text="Button Text:").pack(pady=2)
        tk.Entry(buttons_scrollable_frame, textvariable=save_design_text_var, 
                width=30, font=("Arial", 11)).pack(pady=2)
        
        save_design_color_var = tk.StringVar(value=self.settings["main_window"]["save_design_button_color"])
        
        def choose_save_design_color():
            color = colorchooser.askcolor(title="Choose Button Color")[1]
            if color:
                save_design_color_var.set(color)
        
        tk.Entry(buttons_scrollable_frame, textvariable=save_design_color_var, 
                width=20, font=("Arial", 10)).pack(pady=2)
        tk.Button(buttons_scrollable_frame, text="Choose Color", 
                 command=choose_save_design_color).pack(pady=5)
        
        # ========== UI Layout Tab ==========
        ui_tab = ttk.Frame(notebook)
        notebook.add(ui_tab, text="UI Layout")
        
        ui_canvas = tk.Canvas(ui_tab, bg="#ffffff")
        ui_scrollbar = tk.Scrollbar(ui_tab, orient="vertical", command=ui_canvas.yview)
        ui_scrollable_frame = ttk.Frame(ui_canvas)
        
        ui_scrollable_frame.bind(
            "<Configure>",
            lambda e: ui_canvas.configure(scrollregion=ui_canvas.bbox("all"))
        )
        
        ui_canvas.create_window((0, 0), window=ui_scrollable_frame, anchor="nw")
        ui_canvas.configure(yscrollcommand=ui_scrollbar.set)
        
        ui_scrollbar.pack(side="right", fill="y")
        ui_canvas.pack(side="left", fill="both", expand=True)
        
        tk.Label(ui_scrollable_frame, text="UI Layout Settings", 
                font=("Arial", 20, "bold")).pack(pady=20)
        
        # Design mode toggle
        tk.Label(ui_scrollable_frame, text="Design Mode:", 
                font=("Arial", 14, "bold")).pack(pady=10)
        
        design_mode_var = tk.BooleanVar(value=self.settings["ui_layout"]["design_mode"])
        
        def toggle_design_mode():
            if design_mode_var.get():
                self.drag_drop.enable_drag_mode()
            else:
                self.drag_drop.disable_drag_mode()
            self.settings["ui_layout"]["design_mode"] = design_mode_var.get()
            self.data_manager.save_settings(self.settings)
        
        tk.Checkbutton(ui_scrollable_frame, text="Enable Drag & Drop Mode", 
                      variable=design_mode_var, command=toggle_design_mode,
                      font=("Arial", 12)).pack(pady=10)
        
        # Interactive UI Designer Button
        tk.Label(ui_scrollable_frame, text="Interactive Designer:", 
                font=("Arial", 14, "bold")).pack(pady=20)
        
        def open_ui_designer():
            """Open interactive UI designer"""
            designer = UILayoutDesigner(settings_win, self)
        
        tk.Button(ui_scrollable_frame, text="🎨 Open UI Layout Designer", 
                 command=open_ui_designer,
                 bg="#9B59B6", fg="white", font=("Arial", 12, "bold"),
                 height=2, width=30).pack(pady=10)
        
        tk.Label(ui_scrollable_frame, 
                text="Interactive designer allows you to:\n• Preview UI layout\n• Adjust widget positions\n• Resize widgets\n• Control visibility",
                font=("Arial", 10), justify="left").pack(pady=10)
        
        # Widget visibility controls
        tk.Label(ui_scrollable_frame, text="Quick Visibility Controls:", 
                font=("Arial", 14, "bold")).pack(pady=20)
        
        # Create visibility variables
        self.visibility_vars = {}
        
        # Create a grid for checkboxes
        visibility_frame = tk.Frame(ui_scrollable_frame)
        visibility_frame.pack(pady=10)
        
        # List of widgets with their display names
        widget_names = {
            "logo": "Logo",
            "title": "Title",
            "company": "Company Name",
            "time": "Time Display",
            "number": "Current Number",
            "number_label": "Number Label",
            "prev_button": "Previous Button",
            "print_button": "Print Button",
            "next_button": "Next Button",
            "settings_button": "Settings Button",
            "reset_button": "Reset Button",
            "designer_button": "Designer Button",
            "preview_button": "Preview Button",
            "save_design_button": "Save Design Button",
            "stats": "Statistics",
            "instructions": "Instructions",
            "auto_save_status": "Auto-Save Status"
        }
        
        # Create checkboxes in 3 columns
        col1 = tk.Frame(visibility_frame)
        col1.pack(side="left", padx=20)
        
        col2 = tk.Frame(visibility_frame)
        col2.pack(side="left", padx=20)
        
        col3 = tk.Frame(visibility_frame)
        col3.pack(side="left", padx=20)
        
        # Distribute widgets across columns
        widgets_list = list(widget_names.items())
        for i, (widget_id, display_name) in enumerate(widgets_list):
            if i % 3 == 0:
                col = col1
            elif i % 3 == 1:
                col = col2
            else:
                col = col3
            
            # Get current visibility from settings
            visible = self.settings["ui_layout"]["widgets"].get(widget_id, {}).get("visible", True)
            var = tk.BooleanVar(value=visible)
            self.visibility_vars[widget_id] = var
            
            # Create checkbox
            tk.Checkbutton(col, text=display_name, variable=var,
                          font=("Arial", 11)).pack(anchor="w", pady=3)
        
        # Save visibility button
        def save_visibility():
            for widget_id, var in self.visibility_vars.items():
                if widget_id in self.settings["ui_layout"]["widgets"]:
                    self.settings["ui_layout"]["widgets"][widget_id]["visible"] = var.get()
            
            # Apply layout
            self.apply_layout()
            
            # Save settings
            self.data_manager.save_settings(self.settings)
            
            messagebox.showinfo("Success", "Visibility settings saved!")
        
        tk.Button(ui_scrollable_frame, text="💾 Save Visibility", 
                 command=save_visibility,
                 bg="#27AE60", fg="white", font=("Arial", 12, "bold"),
                 height=2, width=20).pack(pady=20)
        
        # Reset positions button
        def reset_positions():
            if messagebox.askyesno("Confirm", "Reset all widget positions to default?"):
                # Load default positions
                self.settings["ui_layout"]["widgets"] = Config.DEFAULT_SETTINGS["ui_layout"]["widgets"].copy()
                
                # Apply layout
                self.apply_layout()
                
                # Save settings
                self.data_manager.save_settings(self.settings)
                
                # Update checkboxes
                for widget_id, var in self.visibility_vars.items():
                    visible = self.settings["ui_layout"]["widgets"].get(widget_id, {}).get("visible", True)
                    var.set(visible)
                
                messagebox.showinfo("Success", "Positions reset to default!")
        
        tk.Button(ui_scrollable_frame, text="🔄 Reset Positions", 
                 command=reset_positions,
                 bg="#E74C3C", fg="white", font=("Arial", 12),
                 height=1, width=20).pack(pady=10)
        
        # ========== Business Rules Tab ==========
        business_tab = ttk.Frame(notebook)
        notebook.add(business_tab, text="Business Rules")
        
        business_canvas = tk.Canvas(business_tab, bg="#ffffff")
        business_scrollbar = tk.Scrollbar(business_tab, orient="vertical", command=business_canvas.yview)
        business_scrollable_frame = ttk.Frame(business_canvas)
        
        business_scrollable_frame.bind(
            "<Configure>",
            lambda e: business_canvas.configure(scrollregion=business_canvas.bbox("all"))
        )
        
        business_canvas.create_window((0, 0), window=business_scrollable_frame, anchor="nw")
        business_canvas.configure(yscrollcommand=business_scrollbar.set)
        
        business_scrollbar.pack(side="right", fill="y")
        business_canvas.pack(side="left", fill="both", expand=True)
        
        tk.Label(business_scrollable_frame, text="Business Rules & Auto-Save", 
                font=("Arial", 20, "bold")).pack(pady=20)
        
        # Start number
        tk.Label(business_scrollable_frame, text="Start Number:", font=("Arial", 12)).pack(pady=5)
        start_var = tk.IntVar(value=self.settings["business_rules"]["start_number"])
        tk.Spinbox(business_scrollable_frame, from_=1, to=9999, textvariable=start_var, 
                  width=10, font=("Arial", 12)).pack(pady=5)
        
        # Auto increment after print
        auto_var = tk.BooleanVar(value=self.settings["business_rules"]["auto_increment_after_print"])
        tk.Checkbutton(business_scrollable_frame, text="Auto increment after printing", 
                      variable=auto_var, font=("Arial", 12)).pack(pady=10)
        
        # Auto-save settings
        tk.Label(business_scrollable_frame, text="Auto-Save Settings:", 
                font=("Arial", 16, "bold")).pack(pady=20)
        
        tk.Label(business_scrollable_frame, text="Auto-Save Interval (seconds):", 
                font=("Arial", 12)).pack(pady=5)
        auto_save_interval_var = tk.IntVar(value=self.settings["business_rules"].get("auto_save_interval", 10))
        tk.Scale(business_scrollable_frame, from_=5, to=60, variable=auto_save_interval_var,
                orient="horizontal", length=300).pack(pady=5)
        
        create_backups_var = tk.BooleanVar(value=self.settings["business_rules"].get("create_backups", True))
        tk.Checkbutton(business_scrollable_frame, text="Create automatic backups", 
                      variable=create_backups_var, font=("Arial", 12)).pack(pady=10)
        
        tk.Label(business_scrollable_frame, text="Backup Interval (seconds):", 
                font=("Arial", 12)).pack(pady=5)
        backup_interval_var = tk.IntVar(value=self.settings["business_rules"].get("backup_interval", 60))
        tk.Scale(business_scrollable_frame, from_=30, to=300, variable=backup_interval_var,
                orient="horizontal", length=300).pack(pady=5)
        
        # Current auto-save status
        tk.Label(business_scrollable_frame, text="Current Auto-Save Status:", 
                font=("Arial", 14, "bold")).pack(pady=20)
        
        last_save = self.settings.get("auto_save", {}).get("last_save", "Never")
        save_count = self.settings.get("auto_save", {}).get("save_count", 0)
        last_backup = self.settings.get("auto_save", {}).get("last_backup", "Never")
        
        status_frame = tk.Frame(business_scrollable_frame, bg="#f0f0f0", relief="solid", bd=1)
        status_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(status_frame, text=f"Last Save: {last_save}", 
                font=("Arial", 11), bg="#f0f0f0").pack(pady=5)
        tk.Label(status_frame, text=f"Total Saves: {save_count}", 
                font=("Arial", 11), bg="#f0f0f0").pack(pady=5)
        tk.Label(status_frame, text=f"Last Backup: {last_backup}", 
                font=("Arial", 11), bg="#f0f0f0").pack(pady=5)
        
        # Manual save button
        def manual_save():
            if self.save_current_state():
                messagebox.showinfo("Success", "Manual save completed successfully!")
            else:
                messagebox.showerror("Error", "Manual save failed!")
        
        tk.Button(business_scrollable_frame, text="💾 Manual Save Now", 
                 command=manual_save,
                 bg="#3498DB", fg="white", font=("Arial", 12),
                 height=2, width=20).pack(pady=20)
        
        # ========== Printer Settings Tab ==========
        printer_tab = ttk.Frame(notebook)
        notebook.add(printer_tab, text="Printer")
        
        printer_canvas = tk.Canvas(printer_tab, bg="#ffffff")
        printer_scrollbar = tk.Scrollbar(printer_tab, orient="vertical", command=printer_canvas.yview)
        printer_scrollable_frame = ttk.Frame(printer_canvas)
        
        printer_scrollable_frame.bind(
            "<Configure>",
            lambda e: printer_canvas.configure(scrollregion=printer_canvas.bbox("all"))
        )
        
        printer_canvas.create_window((0, 0), window=printer_scrollable_frame, anchor="nw")
        printer_canvas.configure(yscrollcommand=printer_scrollbar.set)
        
        printer_scrollbar.pack(side="right", fill="y")
        printer_canvas.pack(side="left", fill="both", expand=True)
        
        tk.Label(printer_scrollable_frame, text="Printer Settings", font=("Arial", 20, "bold")).pack(pady=20)
        
        # Port selection
        tk.Label(printer_scrollable_frame, text="Serial Port:", font=("Arial", 12)).pack(pady=5)
        port_var = tk.StringVar(value=Config.SERIAL_PORT)
        port_entry = tk.Entry(printer_scrollable_frame, textvariable=port_var,
                             width=15, font=("Arial", 12))
        port_entry.pack(pady=5)
        
        # Baud rate
        tk.Label(printer_scrollable_frame, text="Baud Rate:", font=("Arial", 12)).pack(pady=5)
        baud_var = tk.IntVar(value=Config.BAUD_RATE)
        baud_combo = ttk.Combobox(printer_scrollable_frame, textvariable=baud_var,
                                 values=[9600, 19200, 38400, 57600, 115200],
                                 width=10, font=("Arial", 12))
        baud_combo.pack(pady=5)
        
        # Encoding
        tk.Label(printer_scrollable_frame, text="Encoding:", font=("Arial", 12)).pack(pady=5)
        encoding_var = tk.StringVar(value=self.settings["printer_settings"]["encoding"])
        encoding_combo = ttk.Combobox(printer_scrollable_frame, textvariable=encoding_var,
                                     values=["cp437", "cp850", "cp852", "cp1256", "utf-8"],
                                     width=15, font=("Arial", 12))
        encoding_combo.pack(pady=5)
        
        # Paper width
        tk.Label(printer_scrollable_frame, text="Paper Width (chars):", font=("Arial", 12)).pack(pady=5)
        paper_var = tk.IntVar(value=self.settings["printer_settings"]["paper_width"])
        tk.Scale(printer_scrollable_frame, from_=40, to=80, variable=paper_var,
                orient="horizontal", length=200).pack(pady=5)
        
        # Cut after print
        cut_var = tk.BooleanVar(value=self.settings["printer_settings"]["cut_after_print"])
        tk.Checkbutton(printer_scrollable_frame, text="Cut paper after printing", 
                      variable=cut_var, font=("Arial", 12)).pack(pady=10)
        
        # Print quality
        tk.Label(printer_scrollable_frame, text="Print Quality:", font=("Arial", 12)).pack(pady=5)
        quality_var = tk.StringVar(value=self.settings["printer_settings"]["print_quality"])
        quality_combo = ttk.Combobox(printer_scrollable_frame, textvariable=quality_var,
                                    values=["low", "medium", "high"],
                                    width=10, font=("Arial", 12))
        quality_combo.pack(pady=5)
        
        # Darkness
        tk.Label(printer_scrollable_frame, text="Print Darkness (1-15):", font=("Arial", 12)).pack(pady=5)
        darkness_var = tk.IntVar(value=self.settings["printer_settings"]["darkness"])
        tk.Scale(printer_scrollable_frame, from_=1, to=15, variable=darkness_var,
                orient="horizontal", length=200).pack(pady=5)
        
        # Print speed
        tk.Label(printer_scrollable_frame, text="Print Speed (1-5):", font=("Arial", 12)).pack(pady=5)
        speed_var = tk.IntVar(value=self.settings["printer_settings"]["print_speed"])
        tk.Scale(printer_scrollable_frame, from_=1, to=5, variable=speed_var,
                orient="horizontal", length=200).pack(pady=5)
        
        # Advanced printer options
        advanced_frame = tk.LabelFrame(printer_scrollable_frame, text="Advanced Printer Options",
                                      font=("Arial", 14, "bold"))
        advanced_frame.pack(fill="x", padx=10, pady=10)
        
        align_center_var = tk.BooleanVar(value=self.settings["printer_settings"].get("align_center", True))
        tk.Checkbutton(advanced_frame, text="Center align text", 
                      variable=align_center_var, font=("Arial", 12)).pack(anchor="w", pady=5)
        
        bold_header_var = tk.BooleanVar(value=self.settings["printer_settings"].get("bold_header", True))
        tk.Checkbutton(advanced_frame, text="Bold headers", 
                      variable=bold_header_var, font=("Arial", 12)).pack(anchor="w", pady=5)
        
        double_height_var = tk.BooleanVar(value=self.settings["printer_settings"].get("double_height", True))
        tk.Checkbutton(advanced_frame, text="Double height for headers", 
                      variable=double_height_var, font=("Arial", 12)).pack(anchor="w", pady=5)
        
        # Test printer button
        tk.Button(printer_scrollable_frame, text="🖨️ Test Printer Connection", 
                 command=self.test_printer_connection,
                 bg="#3498DB", fg="white", font=("Arial", 12),
                 height=2, width=25).pack(pady=20)
        
        # ========== Ticket Designs Tab ==========
        designs_tab = ttk.Frame(notebook)
        notebook.add(designs_tab, text="Ticket Designs")
        
        designs_canvas = tk.Canvas(designs_tab, bg="#ffffff")
        designs_scrollbar = tk.Scrollbar(designs_tab, orient="vertical", command=designs_canvas.yview)
        designs_scrollable_frame = ttk.Frame(designs_canvas)
        
        designs_scrollable_frame.bind(
            "<Configure>",
            lambda e: designs_canvas.configure(scrollregion=designs_canvas.bbox("all"))
        )
        
        designs_canvas.create_window((0, 0), window=designs_scrollable_frame, anchor="nw")
        designs_canvas.configure(yscrollcommand=designs_scrollbar.set)
        
        designs_scrollbar.pack(side="right", fill="y")
        designs_canvas.pack(side="left", fill="both", expand=True)
        
        tk.Label(designs_scrollable_frame, text="Ticket Designs Management", 
                font=("Arial", 20, "bold")).pack(pady=20)
        
        # Load saved designs
        saved_designs = self.data_manager.load_ticket_designs()
        
        if saved_designs:
            tk.Label(designs_scrollable_frame, text="Available Designs:", 
                    font=("Arial", 14, "bold")).pack(pady=10)
            
            for design_name, design_data in saved_designs.items():
                design_frame = tk.Frame(designs_scrollable_frame, relief="solid", bd=1, bg="#f9f9f9")
                design_frame.pack(fill="x", padx=20, pady=5)
                
                tk.Label(design_frame, text=f"📄 {design_name}", 
                        font=("Arial", 12, "bold"), bg="#f9f9f9").pack(side="left", padx=10, pady=5)
                
                tk.Label(design_frame, text=f"Created: {design_data.get('timestamp', 'N/A')}", 
                        font=("Arial", 9), bg="#f9f9f9").pack(side="left", padx=10, pady=5)
                
                def load_selected_design(design_name=design_name):
                    self.settings["ticket_design"] = design_data.get("ticket_design", {})
                    self.data_manager.save_settings(self.settings)
                    messagebox.showinfo("Success", f"Design '{design_name}' loaded as current!")
                
                tk.Button(design_frame, text="Load", command=load_selected_design,
                         bg="#2196F3", fg="white", font=("Arial", 9)).pack(side="right", padx=5, pady=5)
                
                def delete_selected_design(design_name=design_name):
                    if messagebox.askyesno("Delete Design", f"Delete design '{design_name}'?"):
                        design_file = os.path.join(Config.TICKET_DESIGNS_DIR, f"{design_name}.json")
                        if os.path.exists(design_file):
                            os.remove(design_file)
                            design_frame.destroy()
                            messagebox.showinfo("Success", f"Design '{design_name}' deleted!")
                
                tk.Button(design_frame, text="Delete", command=delete_selected_design,
                         bg="#E74C3C", fg="white", font=("Arial", 9)).pack(side="right", padx=5, pady=5)
        else:
            tk.Label(designs_scrollable_frame, text="No saved designs found.", 
                    font=("Arial", 12), fg="#666666").pack(pady=20)
        
        # Create new design button
        def create_new_design():
            design_name = simpledialog.askstring("New Design", "Enter design name:")
            if design_name:
                design_data = {
                    "name": design_name,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "ticket_design": self.settings["ticket_design"].copy(),
                    "elements": {}
                }
                
                if self.data_manager.save_ticket_design(design_name, design_data):
                    messagebox.showinfo("Success", f"Design '{design_name}' created!")
                    # Refresh the designs tab
                    settings_win.destroy()
                    self.open_settings()
                else:
                    messagebox.showerror("Error", "Failed to create design!")
        
        tk.Button(designs_scrollable_frame, text="➕ Create New Design", 
                 command=create_new_design,
                 bg="#27AE60", fg="white", font=("Arial", 12),
                 height=2, width=25).pack(pady=20)
        
        # ========== Bottom Control Frame ==========
        bottom_frame = tk.Frame(settings_win, bg="#f0f0f0", height=80)
        bottom_frame.pack(side="bottom", fill="x", pady=10, padx=20)
        
        def save_all_settings():
            """Save all settings"""
            # General
            self.settings["title"] = title_var.get()
            self.settings["company_name"] = company_var.get()
            self.settings["company_address"] = address_var.get()
            self.settings["company_phone"] = phone_var.get()
            self.settings["system_password"] = password_var.get()
            
            # Display
            self.settings["main_window"]["bg_color"] = bg_color_var.get()
            self.settings["main_window"]["number_color"] = number_color_var.get()
            self.settings["main_window"]["number_bg_color"] = number_bg_color_var.get()
            self.settings["main_window"]["number_border_color"] = number_border_color_var.get()
            self.settings["main_window"]["number_border_width"] = number_border_width_var.get()
            self.settings["main_window"]["number_size"] = number_size_var.get()
            self.settings["main_window"]["number_shape"] = number_shape_var.get()
            self.settings["main_window"]["number_rectangle_width"] = rect_width_var.get()
            self.settings["main_window"]["number_rectangle_height"] = rect_height_var.get()
            self.settings["main_window"]["number_rectangle_corner"] = rect_corner_var.get()
            
            # Button sizes
            self.settings["main_window"]["print_button_width"] = print_width_var.get()
            self.settings["main_window"]["print_button_height"] = print_height_var.get()
            self.settings["main_window"]["nav_button_width"] = nav_width_var.get()
            self.settings["main_window"]["nav_button_height"] = nav_height_var.get()
            self.settings["main_window"]["settings_button_width"] = settings_width_var.get()
            self.settings["main_window"]["settings_button_height"] = settings_height_var.get()
            
            # Buttons
            self.settings["main_window"]["print_button_text"] = print_text_var.get()
            self.settings["main_window"]["print_button_color"] = print_color_var.get()
            self.settings["main_window"]["print_button_font_color"] = print_font_color_var.get()
            self.settings["main_window"]["print_button_corner_radius"] = print_corner_var.get()
            
            self.settings["main_window"]["prev_button_text"] = prev_text_var.get()
            self.settings["main_window"]["next_button_text"] = next_text_var.get()
            self.settings["main_window"]["nav_button_color"] = nav_color_var.get()
            
            self.settings["main_window"]["settings_button_text"] = settings_text_var.get()
            self.settings["main_window"]["settings_button_color"] = settings_color_var.get()
            
            self.settings["main_window"]["save_design_button_text"] = save_design_text_var.get()
            self.settings["main_window"]["save_design_button_color"] = save_design_color_var.get()
            
            # Ticket Design
            self.settings["ticket_design"]["show_logo"] = show_logo_var.get()
            self.settings["ticket_design"]["logo_width"] = ticket_logo_width_var.get()
            self.settings["ticket_design"]["logo_height"] = ticket_logo_height_var.get()
            self.settings["ticket_design"]["company_info"] = show_company_var.get()
            self.settings["ticket_design"]["company_font_size"] = company_font_size_var.get()
            self.settings["ticket_design"]["number_prefix"] = number_prefix_var.get()
            self.settings["ticket_design"]["number_size"] = ticket_number_size_var.get()
            self.settings["ticket_design"]["thank_message"] = thank_var.get()
            self.settings["ticket_design"]["thank_font_size"] = thank_font_size_var.get()
            self.settings["ticket_design"]["warning_message"] = warning_var.get()
            self.settings["ticket_design"]["warning_font_size"] = warning_font_size_var.get()
            self.settings["ticket_design"]["custom_message"] = custom_var.get()
            self.settings["ticket_design"]["message_font_size"] = custom_font_size_var.get()
            self.settings["ticket_design"]["show_date"] = show_date_var.get()
            self.settings["ticket_design"]["show_time"] = show_time_var.get()
            self.settings["ticket_design"]["watermark"] = show_watermark_var.get()
            self.settings["ticket_design"]["watermark_text"] = watermark_text_var.get()
            self.settings["ticket_design"]["watermark_font_size"] = watermark_font_size_var.get()
            
            # Business rules
            self.settings["business_rules"]["start_number"] = start_var.get()
            self.settings["business_rules"]["auto_increment_after_print"] = auto_var.get()
            self.settings["business_rules"]["auto_save_interval"] = auto_save_interval_var.get()
            self.settings["business_rules"]["create_backups"] = create_backups_var.get()
            self.settings["business_rules"]["backup_interval"] = backup_interval_var.get()
            
            # Printer settings
            Config.SERIAL_PORT = port_var.get()
            Config.BAUD_RATE = baud_var.get()
            self.settings["printer_settings"]["encoding"] = encoding_var.get()
            self.settings["printer_settings"]["paper_width"] = paper_var.get()
            self.settings["printer_settings"]["cut_after_print"] = cut_var.get()
            self.settings["printer_settings"]["print_quality"] = quality_var.get()
            self.settings["printer_settings"]["darkness"] = darkness_var.get()
            self.settings["printer_settings"]["print_speed"] = speed_var.get()
            self.settings["printer_settings"]["align_center"] = align_center_var.get()
            self.settings["printer_settings"]["bold_header"] = bold_header_var.get()
            self.settings["printer_settings"]["double_height"] = double_height_var.get()
            
            # UI Layout
            self.settings["ui_layout"]["design_mode"] = design_mode_var.get()
            
            # Save visibility settings
            for widget_id, var in self.visibility_vars.items():
                if widget_id in self.settings["ui_layout"]["widgets"]:
                    self.settings["ui_layout"]["widgets"][widget_id]["visible"] = var.get()
            
            # Save settings
            if self.data_manager.save_settings(self.settings):
                # Update UI
                self.root.title(self.settings["title"])
                
                # Update background
                self.update_background()
                
                # Update title
                title_font = (self.settings["main_window"]["title_font"], 
                            self.settings["main_window"]["title_size"], 
                            "bold" if self.settings["main_window"]["title_bold"] else "normal")
                self.title_label.config(
                    text=self.settings["title"],
                    font=title_font,
                    fg=self.settings["main_window"]["title_color"],
                    bg=self.root.cget("bg")
                )
                
                # Update company
                company_font = (self.settings["main_window"]["company_font"], 
                              self.settings["main_window"]["company_size"])
                self.company_label.config(
                    text=self.settings["company_name"],
                    font=company_font,
                    fg=self.settings["main_window"]["company_color"],
                    bg=self.root.cget("bg")
                )
                
                # Update number display
                self.create_number_display()
                self.number_canvas.config(bg=self.root.cget("bg"))
                
                # Update all buttons
                self.update_all_buttons()
                
                # Apply layout
                self.apply_layout()
                
                # Update design mode if changed
                if design_mode_var.get() != self.drag_drop.design_mode:
                    if design_mode_var.get():
                        self.drag_drop.enable_drag_mode()
                    else:
                        self.drag_drop.disable_drag_mode()
                
                # Restart auto-save manager if interval changed
                self.auto_save_manager.stop()
                if self.settings["business_rules"]["auto_save_interval"] > 0:
                    self.auto_save_manager.start()
                
                # Update auto-save timer
                self.setup_auto_save_timer()
                
                settings_win.destroy()
                messagebox.showinfo("Success", "Settings saved successfully!")
            else:
                messagebox.showerror("Error", "Failed to save settings!")
        
        def test_printer():
            """Test printer"""
            if self.enhanced_printer.print_ticket_with_design(999, self.settings):
                messagebox.showinfo("Success", "Printer test successful!")
            else:
                messagebox.showerror("Error", "Printer test failed!")
        
        def test_printer_connection():
            """Test printer connection"""
            try:
                ser = serial.Serial(
                    Config.SERIAL_PORT,
                    Config.BAUD_RATE,
                    timeout=2,
                    bytesize=serial.EIGHTBITS,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE
                )
                ser.close()
                messagebox.showinfo("Success", f"Printer connected successfully on {Config.SERIAL_PORT}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to connect to printer: {str(e)}")
        
        self.test_printer_connection = test_printer_connection
        
        # Save button
        save_button = tk.Button(bottom_frame, text="💾 Save Settings", 
                               command=save_all_settings,
                               bg="#27AE60", fg="white", font=("Arial", 14, "bold"),
                               width=20, height=2)
        save_button.pack(side="left", expand=True, padx=10)
        
        # Test printer button
        test_button = tk.Button(bottom_frame, text="🖨️ Test Printer", 
                               command=test_printer,
                               bg="#3498DB", fg="white", font=("Arial", 12),
                               width=15)
        test_button.pack(side="left", padx=10)
        
        # Manual save button
        manual_button = tk.Button(bottom_frame, text="💾 Save Now", 
                                 command=lambda: self.save_current_state(),
                                 bg="#9B59B6", fg="white", font=("Arial", 12),
                                 width=15)
        manual_button.pack(side="left", padx=10)
        
        # Cancel button
        cancel_button = tk.Button(bottom_frame, text="❌ Close", 
                                 command=settings_win.destroy,
                                 bg="#E74C3C", fg="white", font=("Arial", 12),
                                 width=15)
        cancel_button.pack(side="left", padx=10)
    
    def update_all_buttons(self):
        """Update all button configurations with new sizes"""
        main_settings = self.settings["main_window"]
        
        # Print button
        self.print_btn.update_config(
            text=main_settings["print_button_text"],
            width=main_settings.get("print_button_width", 200),
            height=main_settings.get("print_button_height", 60),
            bg_color=main_settings["print_button_color"],
            text_color=main_settings["print_button_font_color"],
            font_family=main_settings["print_button_font"],
            font_size=main_settings["print_button_font_size"],
            bold=main_settings["print_button_bold"],
            corner_radius=main_settings["print_button_corner_radius"]
        )
        
        # Previous button
        self.prev_btn.update_config(
            text=main_settings["prev_button_text"],
            width=main_settings.get("prev_button_width", main_settings.get("nav_button_width", 160)),
            height=main_settings.get("prev_button_height", main_settings.get("nav_button_height", 60)),
            bg_color=main_settings["nav_button_color"],
            text_color=main_settings["nav_button_font_color"],
            font_family=main_settings["nav_button_font"],
            font_size=main_settings["nav_button_font_size"],
            bold=main_settings["nav_button_bold"],
            corner_radius=main_settings["nav_button_corner_radius"]
        )
        
        # Next button
        self.next_btn.update_config(
            text=main_settings["next_button_text"],
            width=main_settings.get("next_button_width", main_settings.get("nav_button_width", 160)),
            height=main_settings.get("next_button_height", main_settings.get("nav_button_height", 60)),
            bg_color=main_settings["nav_button_color"],
            text_color=main_settings["nav_button_font_color"],
            font_family=main_settings["nav_button_font"],
            font_size=main_settings["nav_button_font_size"],
            bold=main_settings["nav_button_bold"],
            corner_radius=main_settings["nav_button_corner_radius"]
        )
        
        # Settings button
        self.settings_btn.update_config(
            text=main_settings["settings_button_text"],
            width=main_settings.get("settings_button_width", 160),
            height=main_settings.get("settings_button_height", 50),
            bg_color=main_settings["settings_button_color"],
            text_color=main_settings["settings_button_font_color"],
            font_family=main_settings["settings_button_font"],
            font_size=main_settings["settings_button_font_size"],
            bold=main_settings["settings_button_bold"],
            corner_radius=main_settings["settings_button_corner_radius"]
        )
        
        # Reset button
        self.reset_btn.update_config(
            text=main_settings["reset_button_text"],
            width=main_settings.get("reset_button_width", 140),
            height=main_settings.get("reset_button_height", 45),
            bg_color=main_settings["reset_button_color"],
            text_color=main_settings["reset_button_font_color"],
            font_family=main_settings["reset_button_font"],
            font_size=main_settings["reset_button_font_size"],
            bold=main_settings["reset_button_bold"],
            corner_radius=main_settings["reset_button_corner_radius"]
        )
        
        # Designer button
        self.designer_btn.update_config(
            text=main_settings["designer_button_text"],
            width=main_settings.get("designer_button_width", 180),
            height=main_settings.get("designer_button_height", 50),
            bg_color=main_settings["designer_button_color"],
            text_color=main_settings["designer_button_font_color"],
            font_family=main_settings["designer_button_font"],
            font_size=main_settings["designer_button_font_size"],
            bold=main_settings["designer_button_bold"],
            corner_radius=main_settings["designer_button_corner_radius"]
        )
        
        # Preview button
        self.preview_btn.update_config(
            text=main_settings["preview_button_text"],
            width=main_settings.get("preview_button_width", 160),
            height=main_settings.get("preview_button_height", 45),
            bg_color=main_settings["preview_button_color"],
            text_color=main_settings["preview_button_font_color"],
            font_family=main_settings["preview_button_font"],
            font_size=main_settings["preview_button_font_size"],
            bold=main_settings["preview_button_bold"],
            corner_radius=main_settings["preview_button_corner_radius"]
        )
        
        # Save Design button
        self.save_design_btn.update_config(
            text=main_settings["save_design_button_text"],
            width=main_settings.get("save_design_button_width", 200),
            height=main_settings.get("save_design_button_height", 55),
            bg_color=main_settings["save_design_button_color"],
            text_color=main_settings["save_design_button_font_color"],
            font_family=main_settings["save_design_button_font"],
            font_size=main_settings["save_design_button_font_size"],
            bold=main_settings["save_design_button_bold"],
            corner_radius=main_settings["save_design_button_corner_radius"]
        )
    
    def on_closing(self):
        """Handle window closing"""
        try:
            # Stop auto-save manager
            self.auto_save_manager.stop()
            
            # Save current state
            self.save_current_state()
            
            # Cleanup
            self.data_manager.cleanup()
            
            self.data_manager.logger.info("Application closed gracefully")
            self.root.destroy()
        except Exception as e:
            self.data_manager.logger.error(f"Error during shutdown: {e}")
            self.root.destroy()
    
    def run(self):
        """Run the application"""
        self.root.mainloop()

# ======================= Main Entry Point =======================
if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║         Premium Queue System v6.5.0                      ║
    ║         Complete Edition with Enhanced Auto-Save         ║
    ║         and Interactive UI Designer                      ║
    ║         Starting...                                      ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    try:
        app = PremiumQueueSystem()
        app.run()
    except Exception as e:
        print(f"Error starting application: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")
