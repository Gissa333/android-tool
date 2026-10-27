import customtkinter as ctk
from tkinter import filedialog, messagebox
import subprocess
import os
import sys
import threading
import urllib.request
import zipfile
import shutil
import json
import webbrowser
import time
from datetime import datetime

# --- الترجمة (LANG) في البداية لمنع خطأ NameError ---
LANG = {
    "ar": {
        "title": "أداة الأندرويد", "tab_adb": "ADB / Fastboot", "tab_tools": "أدوات يومية",
        "tab_system": "أدوات النظام", "tab_gaming": "الألعاب والأداء", "tab_apps": "إدارة التطبيقات",
        "tab_backup": "نسخ احتياطي", "tab_flash": "فلاش الروم", "tab_xiaomi": "Xiaomi",
        "tab_huawei": "Huawei", "tab_samsung": "Samsung", "tab_oppo": "Oppo/Realme",
        "tab_vivo": "Vivo/iQOO", "tab_root": "TWRP & Root", "tab_unlock": "فك القفل",
        "tab_mtk": "MTK", "tab_edl": "Qualcomm EDL", "tab_adv": "أدوات متقدمة",
        "tab_guide": "الدليل", "tab_about": "حول", "download_tools": "تحميل Platform-Tools",
        "detect": "اكتشاف الأجهزة", "device_info": "معلومات الجهاز", "reboot": "إعادة تشغيل",
        "fastboot": "وضع Fastboot", "reboot_recovery": "وضع Recovery", "reboot_edl": "وضع EDL",
        "exit_fastboot": "خروج من Fastboot", "tools_title": "أدوات يومية (ADB)",
        "tools_screenshot": "لقطة شاشة", "tools_record": "تسجيل الشاشة (15 ثانية)",
        "tools_record_stop": "إيقاف التسجيل", "tools_install_apk": "تثبيت APK",
        "tools_push": "إرسال ملف للهاتف", "tools_pull": "سحب ملف من الهاتف",
        "tools_battery": "معلومات البطارية", "tools_export_dir": "فتح مجلد التصدير",
        "sys_title": "أدوات النظام", "sys_nav_hide": "إخفاء شريط التنقل", "sys_nav_show": "إظهار شريط التنقل",
        "sys_dpi_apply": "تطبيق DPI", "sys_dpi_reset": "إعادة DPI", "sys_sysui": "إعادة تشغيل SystemUI",
        "sys_gms_disable": "تعطيل GMS", "sys_gms_enable": "تفعيل GMS", "sys_restart": "إعادة تشغيل الهاتف",
        "game_title": "تسريع الألعاب", "game_boost": "وضع الأداء العالي", "game_ram": "تنظيف RAM",
        "game_cache": "مسح الكاش", "adv_title": "أدوات متقدمة", "adv_adb_terminal": "أوامر ADB",
        "adv_install_batch": "تثبيت APK دفعة واحدة", "adv_network_info": "معلومات الشبكة",
        "adv_device_props": "خصائص النظام", "apps_title": "إدارة التطبيقات", "apps_load": "تحميل التطبيقات",
        "apps_uninstall": "حذف", "apps_extract": "استخراج", "apps_clear": "مسح البيانات",
        "apps_force_stop": "إيقاف", "backup_title": "النسخ الاحتياطي", "backup_full": "نسخ كامل",
        "backup_sdcard": "نسخ SD", "backup_open": "فتح المجلد", "flash_title": "فلاش الروم",
        "flash_select_zip": "اختر الروم", "flash_start": "بدء الفلاش", "root_title": "TWRP & Root",
        "check_bl_status": "فحص البوتلودر", "unlock_bl": "فتح البوتلودر", "flash_twrp": "فلاش TWRP",
        "flash_magisk": "فلاش Magisk", "unlock_title": "فك القفل", "erase_frp_fastboot": "مسح FRP",
        "format_data_fastboot": "محو البيانات", "full_device_info": "معلومات كاملة", "mtk_title": "MTK",
        "run_gui": "الواجهة", "read_gpt": "قراءة GPT", "unlock_bl_mtk": "فك MTK", "edl_title": "EDL",
        "edl_printgpt": "الأقسام", "edl_reset": "Reset", "about_title": "حول", "about_version": "الإصدار: {}",
        "about_check_update": "فحص التحديثات", "about_download_update": "تحميل", "about_github": "GitHub",
        "about_up_to_date": "محدث", "about_new_version": "جديد: {}", "about_checking": "فحص...",
        "about_error": "خطأ: {}", "log": "السجل:", "log_save": "حفظ", "log_copy": "نسخ",
        "log_clear": "مسح", "log_open_folder": "فتح", "log_saved": "حفظ", "log_copied": "نسخ",
        "log_cleared": "مسح", "lang_btn": "English", "lic_title": "تنشيط البرنامج",
        "lic_desc": "أدخل كود التفعيل", "lic_placeholder": "الكود هنا...", "lic_activate": "تفعيل",
        "lic_error": "كود غير صحيح", "lic_success": "تم التفعيل", "lic_no_key": "أدخل الكود",
        "msg_downloading_pt": "تحميل Platform-Tools...", "msg_installed": "تم التثبيت",
        "msg_error": "خطأ: {}", "msg_no_device": "لا يوجد جهاز", "confirm_reboot": "إعادة تشغيل؟"
    },
    "en": {
        "title": "Android Tool", "tab_adb": "ADB / Fastboot", "tab_tools": "Daily Tools",
        "tab_system": "System Tools", "tab_gaming": "Gaming", "tab_apps": "App Manager",
        "tab_backup": "Backup", "tab_flash": "Flash ROM", "tab_xiaomi": "Xiaomi",
        "tab_huawei": "Huawei", "tab_samsung": "Samsung", "tab_oppo": "Oppo/Realme",
        "tab_vivo": "Vivo/iQOO", "tab_root": "TWRP & Root", "tab_unlock": "Unlock",
        "tab_mtk": "MTK", "tab_edl": "Qualcomm EDL", "tab_adv": "Advanced Tools",
        "tab_guide": "Guide", "tab_about": "About", "download_tools": "Download Platform-Tools",
        "detect": "Detect Devices", "device_info": "Device Info", "reboot": "Reboot",
        "fastboot": "Fastboot", "reboot_recovery": "Recovery", "reboot_edl": "EDL",
        "exit_fastboot": "Exit Fastboot", "tools_title": "Daily Tools (ADB)",
        "tools_screenshot": "Screenshot", "tools_record": "Screen Record (15s)",
        "tools_record_stop": "Stop Recording", "tools_install_apk": "Install APK",
        "tools_push": "Push File", "tools_pull": "Pull File", "tools_battery": "Battery Info",
        "tools_export_dir": "Open Export Folder", "sys_title": "System Tools",
        "sys_nav_hide": "Hide Nav Bar", "sys_nav_show": "Show Nav Bar", "sys_dpi_apply": "Apply DPI",
        "sys_dpi_reset": "Reset DPI", "sys_sysui": "Restart SystemUI", "sys_gms_disable": "Disable GMS",
        "sys_gms_enable": "Enable GMS", "sys_restart": "Reboot Phone", "game_title": "Gaming Boost",
        "game_boost": "High Performance", "game_ram": "Clean RAM", "game_cache": "Clear Cache",
        "adv_title": "Advanced Tools", "adv_adb_terminal": "ADB Terminal", "adv_install_batch": "Batch Install",
        "adv_network_info": "Network Info", "adv_device_props": "Device Props", "apps_title": "App Manager",
        "apps_load": "Load Apps", "apps_uninstall": "Uninstall", "apps_extract": "Extract",
        "apps_clear": "Clear Data", "apps_force_stop": "Force Stop", "backup_title": "Backup",
        "backup_full": "Full Backup", "backup_sdcard": "Backup SD", "backup_open": "Open Folder",
        "flash_title": "Flash ROM", "flash_select_zip": "Select ROM", "flash_start": "Start Flash",
        "root_title": "TWRP & Root", "check_bl_status": "Check Bootloader", "unlock_bl": "Unlock Bootloader",
        "flash_twrp": "Flash TWRP", "flash_magisk": "Flash Magisk", "unlock_title": "Unlock",
        "erase_frp_fastboot": "Erase FRP", "format_data_fastboot": "Format Data",
        "full_device_info": "Full Info", "mtk_title": "MTK", "run_gui": "GUI", "read_gpt": "Read GPT",
        "unlock_bl_mtk": "MTK Unlock", "edl_title": "EDL", "edl_printgpt": "Partitions",
        "edl_reset": "Reset", "about_title": "About", "about_version": "Version: {}",
        "about_check_update": "Check Updates", "about_download_update": "Download", "about_github": "GitHub",
        "about_up_to_date": "Up to date", "about_new_version": "New: {}", "about_checking": "Checking...",
        "about_error": "Error: {}", "log": "Log:", "log_save": "Save", "log_copy": "Copy",
        "log_clear": "Clear", "log_open_folder": "Open", "log_saved": "Saved", "log_copied": "Copied",
        "log_cleared": "Cleared", "lang_btn": "العربية", "lic_title": "Activation",
        "lic_desc": "Enter code", "lic_placeholder": "Code here...", "lic_activate": "Activate",
        "lic_error": "Invalid code", "lic_success": "Activated", "lic_no_key": "Enter code",
        "msg_downloading_pt": "Downloading Platform-Tools...", "msg_installed": "Installed",
        "msg_error": "Error: {}", "msg_no_device": "No device", "confirm_reboot": "Reboot?"
    }
}

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TOOLS_DIR = resource_path("platform-tools")
MTK_DIR = resource_path("mtkclient")
EDL_DIR = resource_path("edl")
HEIMDALL_DIR = resource_path("heimdall")
LOGS_DIR = os.path.join(BASE_DIR, "logs")
EXPORTS_DIR = os.path.join(BASE_DIR, "exports")
BACKUP_DIR = os.path.join(BASE_DIR, "backups")
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")

ADB = os.path.join(TOOLS_DIR, "adb.exe")
FASTBOOT = os.path.join(TOOLS_DIR, "fastboot.exe")
MTK_SCRIPT = os.path.join(MTK_DIR, "mtk.py")
EDL_SCRIPT = os.path.join(EDL_DIR, "edl.py")
HEIMDALL = os.path.join(HEIMDALL_DIR, "heimdall.exe")

PLATFORM_TOOLS_URL = "https://dl.google.com/android/repository/platform-tools-latest-windows.zip"
APP_VERSION = "2.1.0"
GITHUB_REPO = "Gissa333/android-tool"
SECRET_LICENSE_KEY = "PRO-2026-ANDROID-TOOL"

NO_WINDOW = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0

def run(cmd, timeout=60):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout,
                           encoding="utf-8", errors="ignore", creationflags=NO_WINDOW)
        return (r.stdout or "") + (r.stderr or "")
    except Exception as e:
        return f"Error: {e}"

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def save_config(cfg):
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(cfg, f)
    except Exception:
        pass

def is_activated():
    cfg = load_config()
    return cfg.get("license") == SECRET_LICENSE_KEY

def activate_license(key):
    if key.strip() == SECRET_LICENSE_KEY:
        cfg = load_config()
        cfg["license"] = SECRET_LICENSE_KEY
        save_config(cfg)
        return True
    return False

class LicenseWindow(ctk.CTk):
    def __init__(self, on_success):
        super().__init__()
        self.on_success = on_success
        self.title("License Activation")
        self.geometry("500x350")
        self.resizable(False, False)
        self.lang = "ar"
        self.t = LANG[self.lang]
        self.success = False
        self.build_ui()

    def tr(self, key):
        return self.t.get(key, key)

    def build_ui(self):
        for w in self.winfo_children():
            w.destroy()
        ctk.CTkLabel(self, text="🔑", font=("Arial", 36)).pack(pady=10)
        ctk.CTkLabel(self, text=self.tr("lic_title"), font=("Arial", 20, "bold")).pack(pady=5)
        ctk.CTkLabel(self, text=self.tr("lic_desc"), font=("Arial", 12), text_color="gray").pack(pady=5)
        self.entry = ctk.CTkEntry(self, width=350, height=45, placeholder_text=self.tr("lic_placeholder"))
        self.entry.pack(pady=15)
        ctk.CTkButton(self, text=self.tr("lic_activate"), width=350, height=45,
                      fg_color="green", hover_color="darkgreen",
                      font=("Arial", 14, "bold"), command=self.do_activate).pack(pady=10)
        self.status = ctk.CTkLabel(self, text="", font=("Arial", 12))
        self.status.pack(pady=5)

    def do_activate(self):
        key = self.entry.get().strip()
        if not key:
            self.status.configure(text=self.tr("lic_no_key"), text_color="orange")
            return
        if activate_license(key):
            self.status.configure(text=self.tr("lic_success"), text_color="lightgreen")
            self.success = True
            self.after(1000, self._close_and_launch)

    def _close_and_launch(self):
        try:
            self.destroy()
        except Exception:
            pass
        if self.success and self.on_success:
            self.on_success()

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.lang = "ar"
        self.t = LANG[self.lang]
        self.flash_file = ""
        self.recording = False
        self.apps_list = []
        self.selected_pkg = None
        self.about_status = None
        self.download_btn = None
        self._update_url = "https://github.com/" + GITHUB_REPO + "/releases/latest"

        self.geometry("1020x950")
        self.resizable(True, True)
        os.makedirs(LOGS_DIR, exist_ok=True)
        os.makedirs(EXPORTS_DIR, exist_ok=True)
        os.makedirs(BACKUP_DIR, exist_ok=True)
        
        self.build_ui()
        self.check_tools()
        threading.Thread(target=self._bg_check_update, daemon=True).start()

    def tr(self, key, *args):
        s = self.t.get(key, key)
        if args:
            try:
                return s.format(*args)
            except Exception:
                return s
        return s

    def ui(self, fn, *args, **kwargs):
        try:
            self.after(0, lambda: fn(*args, **kwargs))
        except Exception:
            pass

    def build_ui(self):
        for w in self.winfo_children():
            w.destroy()
        self.title(self.tr("title") + " v" + APP_VERSION)
        top = ctk.CTkFrame(self)
        top.pack(fill="x", padx=15, pady=(10, 0))
        ctk.CTkLabel(top, text=self.tr("title"), font=("Arial", 22, "bold")).pack(side="left", padx=5)
        ctk.CTkButton(top, text=self.tr("lang_btn"), width=110, height=32,
                      command=self.toggle_lang).pack(side="right", padx=5)
        self.tabs = ctk.CTkTabview(self, width=970, height=690)
        self.tabs.pack(padx=15, pady=5, fill="both", expand=True)

        self.tab_adb = self.tabs.add(self.tr("tab_adb"))
        self.tab_tools = self.tabs.add(self.tr("tab_tools"))
        self.tab_system = self.tabs.add(self.tr("tab_system"))
        self.tab_gaming = self.tabs.add(self.tr("tab_gaming"))
        self.tab_apps = self.tabs.add(self.tr("tab_apps"))
        self.tab_backup = self.tabs.add(self.tr("tab_backup"))
        self.tab_flash = self.tabs.add(self.tr("tab_flash"))
        self.tab_xiaomi = self.tabs.add(self.tr("tab_xiaomi"))
        self.tab_huawei = self.tabs.add(self.tr("tab_huawei"))
        self.tab_samsung = self.tabs.add(self.tr("tab_samsung"))
        self.tab_oppo = self.tabs.add(self.tr("tab_oppo"))
        self.tab_vivo = self.tabs.add(self.tr("tab_vivo"))
        self.tab_root = self.tabs.add(self.tr("tab_root"))
        self.tab_unlock = self.tabs.add(self.tr("tab_unlock"))
        self.tab_mtk = self.tabs.add(self.tr("tab_mtk"))
        self.tab_edl = self.tabs.add(self.tr("tab_edl"))
        self.tab_adv = self.tabs.add(self.tr("tab_adv"))
        self.tab_guide = self.tabs.add(self.tr("tab_guide"))
        self.tab_about = self.tabs.add(self.tr("tab_about"))

        self.build_adb_tab()
        self.build_tools_tab()
        self.build_system_tab()
        self.build_gaming_tab()
        self.build_apps_tab()
        self.build_backup_tab()
        self.build_flash_tab()
        self.build_xiaomi_tab()
        self.build_huawei_tab()
        self.build_samsung_tab()
        self.build_oppo_tab()
        self.build_vivo_tab()
        self.build_root_tab()
        self.build_unlock_tab()
        self.build_mtk_tab()
        self.build_edl_tab()
        self.build_adv_tab()
        self.build_guide_tab()
        self.build_about_tab()

        log_header = ctk.CTkFrame(self)
        log_header.pack(fill="x", padx=15)
        ctk.CTkLabel(log_header, text=self.tr("log"), font=("Arial", 13, "bold")).pack(side="left", padx=5)
        ctk.CTkButton(log_header, text=self.tr("log_open_folder"), width=130, height=28,
                      command=self.open_logs_folder).pack(side="right", padx=3)
        ctk.CTkButton(log_header, text=self.tr("log_clear"), width=90, height=28,
                      fg_color="red", hover_color="darkred",
                      command=self.clear_log).pack(side="right", padx=3)
        ctk.CTkButton(log_header, text=self.tr("log_copy"), width=90, height=28,
                      command=self.copy_log).pack(side="right", padx=3)
        ctk.CTkButton(log_header, text=self.tr("log_save"), width=90, height=28,
                      fg_color="green", hover_color="darkgreen",
                      command=self.save_log).pack(side="right", padx=3)
        self.log_box = ctk.CTkTextbox(self, height=110, font=("Consolas", 11))
        self.log_box.pack(fill="x", padx=15, pady=(3, 10))

    def toggle_lang(self):
        self.lang = "en" if self.lang == "ar" else "ar"
        self.t = LANG[self.lang]
        self.build_ui()
        self.check_tools()

    def log(self, t):
        ts = datetime.now().strftime("[%H:%M:%S] ")
        text = ts + str(t) + "\n"
        def _append():
            try:
                self.log_box.insert("end", text)
                self.log_box.see("end")
            except Exception:
                pass
        self.ui(_append)

    def save_log(self):
        try:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            path = os.path.join(LOGS_DIR, "log_" + ts + ".txt")
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.log_box.get("1.0", "end"))
            self.log(self.tr("log_saved"))
        except Exception as e:
            self.log(self.tr("msg_error", e))

    def copy_log(self):
        try:
            self.clipboard_clear()
            self.clipboard_append(self.log_box.get("1.0", "end"))
            self.log(self.tr("log_copied"))
        except Exception as e:
            self.log(self.tr("msg_error", e))

    def clear_log(self):
        try:
            self.log_box.delete("1.0", "end")
            self.log(self.tr("log_cleared"))
        except Exception:
            pass

    def open_folder(self, path):
        try:
            if os.name == "nt":
                os.startfile(path)
            else:
                subprocess.Popen(["xdg-open", path])
        except Exception as e:
            self.log(self.tr("msg_error", e))

    def open_logs_folder(self):
        self.open_folder(LOGS_DIR)

    def open_exports(self):
        self.open_folder(EXPORTS_DIR)

    def open_backups(self):
        self.open_folder(BACKUP_DIR)

    def _bg_check_update(self):
        try:
            req = urllib.request.Request(GITHUB_API, headers={"User-Agent": "AndroidTool"})
            with urllib.request.urlopen(req, timeout=10) as r:
                data = json.loads(r.read().decode("utf-8"))
            latest = data.get("tag_name", "").lstrip("v")
            if latest and latest != APP_VERSION:
                self.ui(self._update_available, latest)
        except Exception:
            pass

    def _update_available(self, latest):
        if self.about_status is None:
            return
        try:
            self.about_status.configure(text=self.tr("about_new_version", latest), text_color="lightgreen")
            self._update_url = "https://github.com/" + GITHUB_REPO + "/releases/latest"
            if self.download_btn is not None:
                self.download_btn.configure(state="normal")
        except Exception:
            pass

    def check_update(self):
        if self.about_status is not None:
            self.about_status.configure(text=self.tr("about_checking"), text_color="gray")
        def t():
            try:
                req = urllib.request.Request(GITHUB_API, headers={"User-Agent": "AndroidTool"})
                with urllib.request.urlopen(req, timeout=10) as r:
                    data = json.loads(r.read().decode("utf-8"))
                latest = data.get("tag_name", "").lstrip("v")
                if latest and latest != APP_VERSION:
                    self.ui(self._update_available, latest)
                else:
                    self.ui(self.about_status.configure, text=self.tr("about_up_to_date"), text_color="lightgreen")
            except Exception as e:
                self.ui(self.about_status.configure, text=self.tr("about_error", str(e)), text_color="red")
        threading.Thread(target=t, daemon=True).start()

    def open_update_page(self):
        webbrowser.open(self._update_url)

    def open_github(self):
        webbrowser.open("https://github.com/" + GITHUB_REPO)

    def build_about_tab(self):
        f = self.tab_about
        ctk.CTkLabel(f, text=self.tr("about_title"), font=("Arial", 18, "bold")).pack(pady=15)
        ctk.CTkLabel(f, text=self.tr("about_version", APP_VERSION), font=("Arial", 14)).pack(pady=6)
        self.about_status = ctk.CTkLabel(f, text="", font=("Arial", 12))
        self.about_status.pack(pady=5)
        bf = ctk.CTkFrame(f)
        bf.pack(pady=15)
        ctk.CTkButton(bf, text=self.tr("about_check_update"), width=200, height=40, command=self.check_update).pack(side="left", padx=5)
        self.download_btn = ctk.CTkButton(bf, text=self.tr("about_download_update"), width=200, height=40, fg_color="green", state="disabled", command=self.open_update_page)
        self.download_btn.pack(side="left", padx=5)
        ctk.CTkButton(f, text=self.tr("about_github"), width=300, height=40, command=self.open_github).pack(pady=10)

    def build_guide_tab(self):
        f = self.tab_guide
        ctk.CTkLabel(f, text=self.tr("tab_guide"), font=("Arial", 18, "bold")).pack(pady=15)
        ctk.CTkLabel(f, text="Welcome! Use the tabs to explore features.", font=("Arial", 13)).pack(pady=10)

    def build_adb_tab(self):
        f = self.tab_adb
        btns = [
            (self.tr("download_tools"), self.download_tools),
            (self.tr("detect"), lambda: self.async_run(lambda: run([ADB, "devices"]))),
            (self.tr("device_info"), lambda: self.async_run(lambda: run([ADB, "shell", "getprop"]))),
            (self.tr("reboot"), lambda: self.async_run(lambda: run([ADB, "reboot"]))),
            (self.tr("fastboot"), lambda: self.async_run(lambda: run([ADB, "reboot", "bootloader"]))),
            (self.tr("reboot_recovery"), lambda: self.async_run(lambda: run([ADB, "reboot", "recovery"]))),
            (self.tr("reboot_edl"), lambda: self.async_run(lambda: run([ADB, "reboot", "edl"]))),
            (self.tr("exit_fastboot"), lambda: self.async_run(lambda: run([FASTBOOT, "reboot"]))),
        ]
        for i, (t, fn) in enumerate(btns):
            ctk.CTkButton(f, text=t, width=210, height=36, command=fn).grid(row=i // 3, column=i % 3, padx=8, pady=8)

    def build_tools_tab(self):
        f = self.tab_tools
        ctk.CTkLabel(f, text=self.tr("tools_title"), font=("Arial", 16, "bold")).pack(pady=10)
        ctk.CTkButton(f, text=self.tr("tools_screenshot"), width=350, height=50, fg_color="green", command=self.tool_screenshot).pack(pady=5)
        ctk.CTkButton(f, text=self.tr("tools_install_apk"), width=350, height=50, fg_color="green", command=self.tool_install_apk).pack(pady=5)
        pf = ctk.CTkFrame(f)
        pf.pack(pady=5)
        ctk.CTkButton(pf, text=self.tr("tools_push"), width=170, height=45, command=self.tool_push).pack(side="left", padx=5)
        ctk.CTkButton(pf, text=self.tr("tools_pull"), width=170, height=45, command=self.tool_pull).pack(side="left", padx=5)
        info_frame = ctk.CTkFrame(f)
        info_frame.pack(pady=5)
        ctk.CTkButton(info_frame, text=self.tr("tools_battery"), width=170, height=45, command=self.tool_battery).pack(side="left", padx=5)
        ctk.CTkButton(info_frame, text=self.tr("tools_export_dir"), width=170, height=45, command=self.open_exports).pack(side="left", padx=5)

    def tool_screenshot(self):
        self.log("جاري أخذ لقطة شاشة...")
        def t():
            res = run([ADB, "shell", "screencap", "-p", "/sdcard/screen.png"])
            if "Error" in res or "no devices" in res.lower():
                self.log(self.tr("msg_no_device")); return
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            path = os.path.join(EXPORTS_DIR, f"screenshot_{ts}.png")
            run([ADB, "pull", "/sdcard/screen.png", path])
            run([ADB, "shell", "rm", "/sdcard/screen.png"])
            self.log(f"تم الحفظ: {path}")
        threading.Thread(target=t, daemon=True).start()

    def tool_install_apk(self):
        path = filedialog.askopenfilename(filetypes=[("APK", "*.apk")])
        if not path: return
        self.log(f"جاري تثبيت: {path}")
        def t():
            res = run([ADB, "install", "-r", path], timeout=120)
            self.log("تم التثبيت" if "Success" in res else f"فشل: {res}")
        threading.Thread(target=t, daemon=True).start()

    def tool_push(self):
        path = filedialog.askopenfilename()
        if path: self.async_run(lambda: run([ADB, "push", path, "/sdcard/"]))

    def tool_pull(self):
        remote = ctk.CTkInputDialog(text="مسار الملف:", title="Pull").get_input()
        if remote: self.async_run(lambda: run([ADB, "pull", remote, EXPORTS_DIR]))

    def tool_battery(self):
        self.async_run(lambda: run([ADB, "shell", "dumpsys", "battery"]))

    def build_system_tab(self):
        f = self.tab_system
        ctk.CTkLabel(f, text=self.tr("sys_title"), font=("Arial", 16, "bold")).pack(pady=10)
        ctk.CTkButton(f, text=self.tr("sys_nav_hide"), width=300, height=40, command=lambda: self.async_run(lambda: run([ADB, "shell", "settings", "put", "global", "policy_control", "immersive.full=*"]))).pack(pady=5)
        ctk.CTkButton(f, text=self.tr("sys_nav_show"), width=300, height=40, command=lambda: self.async_run(lambda: run([ADB, "shell", "settings", "put", "global", "policy_control", "null"]))).pack(pady=5)
        ctk.CTkButton(f, text=self.tr("sys_dpi_reset"), width=300, height=40, command=lambda: self.async_run(lambda: run([ADB, "shell", "wm", "density", "reset"]))).pack(pady=5)
        ctk.CTkButton(f, text=self.tr("sys_sysui"), width=300, height=40, command=lambda: self.async_run(lambda: run([ADB, "shell", "pkill", "com.android.systemui"]))).pack(pady=5)
        ctk.CTkButton(f, text=self.tr("sys_restart"), width=300, height=40, fg_color="red", command=lambda: self.async_run(lambda: run([ADB, "reboot"]))).pack(pady=5)

    def build_gaming_tab(self):
        f = self.tab_gaming
        ctk.CTkLabel(f, text=self.tr("game_title"), font=("Arial", 16, "bold")).pack(pady=10)
        ctk.CTkButton(f, text=self.tr("game_boost"), width=300, height=40, command=self.game_boost).pack(pady=5)
        ctk.CTkButton(f, text=self.tr("game_ram"), width=300, height=40, command=lambda: self.async_run(lambda: run([ADB, "shell", "am", "kill-all"]))).pack(pady=5)
        ctk.CTkButton(f, text=self.tr("game_cache"), width=300, height=40, command=lambda: self.async_run(lambda: run([ADB, "shell", "pm", "trim-caches", "999G"]))).pack(pady=5)

    def game_boost(self):
        self.log("تفعيل وضع الأداء العالي...")
        def t():
            run([ADB, "shell", "settings", "put", "global", "window_animation_scale", "0.5"])
            run([ADB, "shell", "settings", "put", "global", "transition_animation_scale", "0.5"])
            run([ADB, "shell", "settings", "put", "global", "animator_duration_scale", "0.5"])
            self.log("تم التفعيل")
        threading.Thread(target=t, daemon=True).start()

    def build_apps_tab(self):
        f = self.tab_apps
        ctk.CTkLabel(f, text=self.tr("apps_title"), font=("Arial", 16, "bold")).pack(pady=5)
        top_frame = ctk.CTkFrame(f)
        top_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkButton(top_frame, text=self.tr("apps_load"), width=150, command=self.apps_load).pack(side="left", padx=5)
        self.apps_listbox = ctk.CTkScrollableFrame(f, width=800, height=300)
        self.apps_listbox.pack(fill="both", expand=True, padx=10, pady=5)
        btn_frame = ctk.CTkFrame(f)
        btn_frame.pack(pady=5)
        ctk.CTkButton(btn_frame, text=self.tr("apps_uninstall"), fg_color="red", command=lambda: self.apps_action("uninstall")).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text=self.tr("apps_extract"), fg_color="green", command=lambda: self.apps_action("extract")).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text=self.tr("apps_clear"), command=lambda: self.apps_action("clear")).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text=self.tr("apps_force_stop"), fg_color="orange", command=lambda: self.apps_action("stop")).pack(side="left", padx=5)

    def apps_load(self):
        self.log("جاري تحميل التطبيقات...")
        def t():
            res = run([ADB, "shell", "pm", "list", "packages", "-f"])
            if "Error" in res or "no devices" in res.lower():
                self.log(self.tr("msg_no_device")); return
            self.apps_list = [{"pkg": line.split("=")[1], "path": line.split("=")[0].replace("package:", "")} for line in res.splitlines() if line.startswith("package:")]
            self.ui(self.apps_apply_filter)
        threading.Thread(target=t, daemon=True).start()

    def apps_apply_filter(self):
        for w in self.apps_listbox.winfo_children(): w.destroy()
        for app in self.apps_list[:200]:
            ctk.CTkButton(self.apps_listbox, text=app["pkg"], anchor="w", fg_color="transparent", text_color="white", command=lambda p=app["pkg"]: self.apps_select(p)).pack(fill="x", pady=1)

    def apps_select(self, pkg):
        self.selected_pkg = pkg
        self.log(f"تم اختيار: {pkg}")

    def apps_action(self, action):
        if not self.selected_pkg: return
        pkg = self.selected_pkg
        def t():
            if action == "uninstall": run([ADB, "shell", "pm", "uninstall", "--user", "0", pkg])
            elif action == "clear": run([ADB, "shell", "pm", "clear", pkg])
            elif action == "stop": run([ADB, "shell", "am", "force-stop", pkg])
            elif action == "extract":
                for a in self.apps_list:
                    if a["pkg"] == pkg: run([ADB, "pull", a["path"], EXPORTS_DIR]); break
            self.log(f"تم تنفيذ {action} على {pkg}")
        threading.Thread(target=t, daemon=True).start()

    def build_backup_tab(self):
        f = self.tab_backup
        ctk.CTkLabel(f, text=self.tr("backup_title"), font=("Arial", 16, "bold")).pack(pady=10)
        ctk.CTkButton(f, text=self.tr("backup_full"), width=300, height=40, command=self.backup_full).pack(pady=5)
        ctk.CTkButton(f, text=self.tr("backup_sdcard"), width=300, height=40, command=self.backup_sdcard).pack(pady=5)
        ctk.CTkButton(f, text=self.tr("backup_open"), width=300, height=40, command=self.open_backups).pack(pady=5)

    def backup_full(self):
        self.log("بدء النسخ...")
        def t():
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            path = os.path.join(BACKUP_DIR, f"backup_{ts}.ab")
            run([ADB, "backup", "-apk", "-all", "-f", path], timeout=600)
            self.log(f"اكتمل: {path}")
        threading.Thread(target=t, daemon=True).start()

    def backup_sdcard(self):
        def t():
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            dest = os.path.join(BACKUP_DIR, f"sdcard_{ts}")
            os.makedirs(dest, exist_ok=True)
            run([ADB, "pull", "/sdcard/", dest], timeout=1800)
            self.log(f"اكتمل: {dest}")
        threading.Thread(target=t, daemon=True).start()

    def build_flash_tab(self):
        f = self.tab_flash
        ctk.CTkLabel(f, text=self.tr("flash_title"), font=("Arial", 16, "bold")).pack(pady=10)
        ctk.CTkButton(f, text=self.tr("flash_select_zip"), width=300, height=40, command=self.flash_select_file).pack(pady=5)
        self.flash_label = ctk.CTkLabel(f, text="لم يتم اختيار ملف")
        self.flash_label.pack(pady=5)
        ctk.CTkButton(f, text=self.tr("flash_start"), width=300, height=40, fg_color="green", command=self.flash_start).pack(pady=10)

    def flash_select_file(self):
        path = filedialog.askopenfilename()
        if path:
            self.flash_file = path
            self.flash_label.configure(text=os.path.basename(path))

    def flash_start(self):
        if not self.flash_file: return
        self.log("بدء الفلاش (محاكاة)...")

    def build_xiaomi_tab(self):
        f = self.tab_xiaomi
        ctk.CTkLabel(f, text=self.tr("tab_xiaomi"), font=("Arial", 16, "bold")).pack(pady=10)
        ctk.CTkButton(f, text=self.tr("device_info"), width=250, height=40, command=lambda: self.async_run(lambda: run([FASTBOOT, "getvar", "all"]))).pack(pady=5)
        ctk.CTkButton(f, text=self.tr("reboot_fastboot"), width=250, height=40, command=lambda: self.async_run(lambda: run([ADB, "reboot", "bootloader"]))).pack(pady=5)

    def build_huawei_tab(self):
        f = self.tab_huawei
        ctk.CTkLabel(f, text=self.tr("tab_huawei"), font=("Arial", 16, "bold")).pack(pady=10)
        ctk.CTkButton(f, text=self.tr("device_info"), width=250, height=40, command=lambda: self.async_run(lambda: run([FASTBOOT, "getvar", "all"]))).pack(pady=5)
        ctk.CTkButton(f, text=self.tr("reboot_fastboot"), width=250, height=40, command=lambda: self.async_run(lambda: run([ADB, "reboot", "bootloader"]))).pack(pady=5)

    def build_samsung_tab(self):
        f = self.tab_samsung
        ctk.CTkLabel(f, text=self.tr("tab_samsung"), font=("Arial", 16, "bold")).pack(pady=10)
        ctk.CTkButton(f, text=self.tr("detect"), width=250, height=40, command=lambda: self.async_run(lambda: run([HEIMDALL, "detect"]))).pack(pady=5)

    def build_oppo_tab(self):
        f = self.tab_oppo
        ctk.CTkLabel(f, text=self.tr("tab_oppo"), font=("Arial", 16, "bold")).pack(pady=10)
        ctk.CTkButton(f, text=self.tr("device_info"), width=250, height=40, command=lambda: self.async_run(lambda: run([FASTBOOT, "getvar", "all"]))).pack(pady=5)

    def build_vivo_tab(self):
        f = self.tab_vivo
        ctk.CTkLabel(f, text=self.tr("tab_vivo"), font=("Arial", 16, "bold")).pack(pady=10)
        ctk.CTkButton(f, text=self.tr("device_info"), width=250, height=40, command=lambda: self.async_run(lambda: run([FASTBOOT, "getvar", "all"]))).pack(pady=5)

    def build_root_tab(self):
        f = self.tab_root
        ctk.CTkLabel(f, text=self.tr("root_title"), font=("Arial", 16, "bold")).pack(pady=10)
        ctk.CTkButton(f, text=self.tr("check_bl_status"), width=250, height=40, command=lambda: self.async_run(lambda: run([FASTBOOT, "getvar", "unlocked"]))).pack(pady=5)
        ctk.CTkButton(f, text=self.tr("unlock_bl"), width=250, height=40, fg_color="red", command=lambda: self.async_run(lambda: run([FASTBOOT, "flashing", "unlock"]))).pack(pady=5)

    def build_unlock_tab(self):
        f = self.tab_unlock
        ctk.CTkLabel(f, text=self.tr("unlock_title"), font=("Arial", 16, "bold")).pack(pady=10)
        ctk.CTkButton(f, text=self.tr("erase_frp_fastboot"), width=250, height=40, command=lambda: self.async_run(lambda: run([FASTBOOT, "erase", "frp"]))).pack(pady=5)
        ctk.CTkButton(f, text=self.tr("format_data_fastboot"), width=250, height=40, fg_color="red", command=lambda: self.async_run(lambda: run([FASTBOOT, "erase", "userdata"]))).pack(pady=5)

    def build_mtk_tab(self):
        f = self.tab_mtk
        ctk.CTkLabel(f, text=self.tr("mtk_title"), font=("Arial", 16, "bold")).pack(pady=10)
        ctk.CTkButton(f, text=self.tr("run_gui"), width=250, height=40, command=lambda: self.run_mtk_script()).pack(pady=5)
        ctk.CTkButton(f, text=self.tr("read_gpt"), width=250, height=40, command=lambda: self.run_mtk_script("r", "gpt")).pack(pady=5)

    def run_mtk_script(self, *args):
        if not os.path.exists(MTK_SCRIPT): return
        def t():
            res = run([sys.executable, MTK_SCRIPT] + list(args), timeout=300)
            self.log(res)
        threading.Thread(target=t, daemon=True).start()

    def build_edl_tab(self):
        f = self.tab_edl
        ctk.CTkLabel(f, text=self.tr("edl_title"), font=("Arial", 16, "bold")).pack(pady=10)
        ctk.CTkButton(f, text=self.tr("edl_printgpt"), width=250, height=40, command=self.edl_printgpt).pack(pady=5)
        ctk.CTkButton(f, text=self.tr("edl_reset"), width=250, height=40, command=self.edl_reset).pack(pady=5)

    def edl_printgpt(self):
        if not os.path.exists(EDL_SCRIPT): return
        def t():
            self.log(run([sys.executable, EDL_SCRIPT, "printgpt"], timeout=120))
        threading.Thread(target=t, daemon=True).start()

    def edl_reset(self):
        if not os.path.exists(EDL_SCRIPT): return
        def t():
            self.log(run([sys.executable, EDL_SCRIPT, "reset"], timeout=120))
        threading.Thread(target=t, daemon=True).start()

    def build_adv_tab(self):
        f = self.tab_adv
        ctk.CTkLabel(f, text=self.tr("adv_title"), font=("Arial", 16, "bold")).pack(pady=10)
        ctk.CTkButton(f, text=self.tr("adv_adb_terminal"), width=350, height=40, command=self.adv_adb_terminal).pack(pady=5)
        ctk.CTkButton(f, text=self.tr("adv_network_info"), width=350, height=40, command=lambda: self.async_run(lambda: run([ADB, "shell", "ifconfig"]))).pack(pady=5)

    def adv_adb_terminal(self):
        cmd = ctk.CTkInputDialog(text="أدخل أمر ADB:", title="ADB").get_input()
        if cmd: self.async_run(lambda: run([ADB] + cmd.split()))

    def async_run(self, fn):
        def wrapper():
            try:
                res = fn()
                if res: self.log(res)
            except Exception as e:
                self.log(f"Error: {e}")
        threading.Thread(target=wrapper, daemon=True).start()

    def download_tools(self):
        self.log(self.tr("msg_downloading_pt"))
        def t():
            try:
                zip_path = os.path.join(BASE_DIR, "platform-tools.zip")
                urllib.request.urlretrieve(PLATFORM_TOOLS_URL, zip_path)
                with zipfile.ZipFile(zip_path) as z: z.extractall(BASE_DIR)
                os.remove(zip_path)
                self.log(self.tr("msg_installed"))
                self.check_tools()
            except Exception as e:
                self.log(self.tr("msg_error", e))
        threading.Thread(target=t, daemon=True).start()

    def check_tools(self):
        self.log("--- فحص الأدوات ---")
        self.log(f"ADB: {'موجود' if os.path.exists(ADB) else 'غير موجود'}")
        self.log(f"Fastboot: {'موجود' if os.path.exists(FASTBOOT) else 'غير موجود'}")


def show_splash():
    splash = ctk.CTk()
    splash.overrideredirect(True)
    splash.geometry("450x250")
    screen_width = splash.winfo_screenwidth()
    screen_height = splash.winfo_screenheight()
    x = (screen_width // 2) - (450 // 2)
    y = (screen_height // 2) - (250 // 2)
    splash.geometry(f"450x250+{x}+{y}")
    ctk.CTkLabel(splash, text="🤖", font=("Arial", 48)).pack(pady=(30, 10))
    ctk.CTkLabel(splash, text="Android Tool", font=("Arial", 24, "bold")).pack(pady=5)
    bar = ctk.CTkProgressBar(splash, width=300)
    bar.pack(pady=20)
    for i in range(101):
        bar.set(i / 100)
        splash.update()
        time.sleep(0.02)
    splash.destroy()


def main():
    show_splash()
    if not is_activated():
        def launch_app():
            app = App()
            app.mainloop()
        lic = LicenseWindow(on_success=launch_app)
        lic.mainloop()
    else:
        app = App()
        app.mainloop()


if __name__ == "__main__":
    main()