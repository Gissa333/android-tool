import customtkinter as ctk
from tkinter import filedialog, messagebox
import subprocess
import os
import sys
import threading
import urllib.request
import zipfile
import shutil
import time

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TOOLS_DIR = os.path.join(BASE_DIR, "platform-tools")
MTK_DIR = os.path.join(BASE_DIR, "mtkclient")
EDL_DIR = os.path.join(BASE_DIR, "edl")
TEMP_FLASH = os.path.join(BASE_DIR, "flash_temp")
EMBED_PY = os.path.join(BASE_DIR, "python-embed", "python.exe")
ADB = os.path.join(TOOLS_DIR, "adb.exe")
FASTBOOT = os.path.join(TOOLS_DIR, "fastboot.exe")
MTK_SCRIPT = os.path.join(MTK_DIR, "mtk.py")
EDL_SCRIPT = os.path.join(EDL_DIR, "edl.py")

PLATFORM_TOOLS_URL = "https://dl.google.com/android/repository/platform-tools-latest-windows.zip"


LANG = {
    "ar": {
        "title": "🛠️ أداة الأندرويد",
        "tab_adb": "ADB / Fastboot",
        "tab_flash": "📦 فلاش الروم",
        "tab_unlock": "🔓 فك القفل",
        "tab_mtk": "MTK",
        "tab_edl": "Qualcomm EDL",
        # ADB
        "download_tools": "📥 تحميل Platform-Tools",
        "detect": "🔍 اكتشاف الأجهزة",
        "device_info": "📱 معلومات الجهاز",
        "reboot": "🔄 إعادة تشغيل",
        "fastboot": "⚡ وضع Fastboot",
        "reboot_recovery": "♻️ وضع Recovery",
        "reboot_edl": "📡 وضع EDL",
        "exit_fastboot": "🔌 خروج من Fastboot",
        # Flash
        "flash_title": "📦 فلاش الروم الكامل",
        "flash_select_zip": "📁 اختر ملف الروم (ZIP)",
        "flash_selected": "الملف المختار:",
        "flash_mode": "وضعية الفلاش:",
        "flash_mode_normal": "عادي",
        "flash_mode_keep": "الاحتفاظ بالبيانات",
        "flash_mode_wipe": "محو كل شيء",
        "flash_stop_on_error": "التوقف عند الخطأ",
        "flash_auto_reboot": "إعادة التشغيل تلقائياً",
        "flash_start": "🚀 بدء الفلاش",
        "flash_cancel": "⏹️ إلغاء",
        "flash_progress": "التقدم:",
        "flash_status_idle": "بانتظار البدء",
        "flash_status_extracting": "جاري فك الضغط...",
        "flash_status_flashing": "جاري فلاش: {}",
        "flash_status_done": "✅ اكتمل الفلاش",
        "flash_status_error": "❌ فشل",
        "flash_status_cancelled": "⏹️ تم الإلغاء",
        # Unlock
        "unlock_title": "🔓 فك القفل و FRP",
        "check_lock": "🔍 فحص حالة القفل",
        "check_root": "👑 فحص الروت",
        "check_frp": "🚫 فحص حالة FRP",
        "remove_locksettings": "🗑️ حذف locksettings.db",
        "remove_gatekeeper": "🔑 حذف gatekeeper",
        "remove_pattern": "📐 حذف النمط",
        "format_data_fastboot": "🔐 فورمات Data",
        "erase_frp_fastboot": "🚫 مسح FRP (Fastboot)",
        "erase_frp_adb": "🚫 مسح FRP (ADB)",
        "full_device_info": "📊 معلومات كاملة",
        "unlock_warning": "⚠️ استخدم على مسؤوليتك — قد تُفقد البيانات",
        # MTK
        "mtk_title": "⚙️ mtkclient — مدمج",
        "run_gui": "🖥️ الواجهة الرسمية",
        "read_gpt": "📋 قراءة GPT",
        "read_part": "قراءة قسم:",
        "read_btn": "قراءة",
        "write_part": "كتابة قسم:",
        "pick": "اختر",
        "write_btn": "كتابة",
        "advanced": "⚠️ عمليات متقدمة",
        "unlock_bl": "🔓 فك قفل البوتلودر",
        "wipe_frp": "🧹 مسح FRP + Userdata",
        # EDL
        "edl_title": "⚡ Qualcomm EDL",
        "edl_check": "🔍 فحص الاتصال",
        "edl_gpt": "📋 قراءة GPT",
        "edl_printgpt": "🖨️ طباعة الأقسام",
        "edl_dump": "💾 استخراج قسم",
        "edl_load": "📤 كتابة قسم",
        "edl_rw": "🔐 Read/Write",
        "edl_reset": "🔄 Reset",
        "edl_wipe": "🧹 محو Userdata",
        "edl_firehose": "🔥 Firehose Loader:",
        "edl_partition": "القسم:",
        "edl_image": "الصورة:",
        # عام
        "log": "📋 السجل:",
        "lang_btn": "🌐 English",
        "msg_wait": "⏳ ...",
        "msg_tools_ok": "✅ Platform-Tools: {}",
        "msg_tools_missing": "⚠️ Platform-Tools غير مثبتة",
        "msg_python_ok": "✅ Python مدمج",
        "msg_python_missing": "⚠️ Python المدمج غير موجود",
        "msg_mtk_ok": "✅ mtkclient جاهز",
        "msg_mtk_missing": "⚠️ mtkclient غير موجود",
        "msg_edl_ok": "✅ edl جاهز",
        "msg_edl_missing": "⚠️ edl غير موجود",
        "msg_downloading_pt": "📥 تحميل Platform-Tools...",
        "msg_installed": "✅ تم التثبيت",
        "msg_error": "❌ {}",
        "msg_adb": "— ADB —",
        "msg_fastboot": "— Fastboot —",
        "msg_running_gui": "🖥️ تشغيل mtk_gui...",
        "msg_no_embed": "❌ Python المدمج غير موجود",
        "msg_no_gui": "❌ mtk_gui.py غير موجود",
        "msg_no_mtk": "❌ mtkclient غير موجود",
        "msg_no_edl": "❌ edl غير موجود",
        "msg_running_cmd": "⚙️ {}",
        "confirm_write": "كتابة {} من {}؟",
        "confirm_unlock": "فك قفل البوتلودر سيمسح كل البيانات! متأكد؟",
        "confirm_wipe": "مسح FRP و Userdata نهائياً!",
        "confirm_format": "سيتم محو كل بيانات الجهاز! متأكد؟",
        "confirm_flash": "بدء فلاش {} قسم؟",
        "err_check": "تحقق من الحقول",
        "err": "خطأ",
        "confirm": "تأكيد",
        "warn": "تحذير",
    },
    "en": {
        "title": "🛠️ Android Tool",
        "tab_adb": "ADB / Fastboot",
        "tab_flash": "📦 Flash ROM",
        "tab_unlock": "🔓 Unlock",
        "tab_mtk": "MTK",
        "tab_edl": "Qualcomm EDL",
        "download_tools": "📥 Download Platform-Tools",
        "detect": "🔍 Detect Devices",
        "device_info": "📱 Device Info",
        "reboot": "🔄 Reboot",
        "fastboot": "⚡ Fastboot",
        "reboot_recovery": "♻️ Recovery",
        "reboot_edl": "📡 EDL",
        "exit_fastboot": "🔌 Exit Fastboot",
        "flash_title": "📦 Full ROM Flash",
        "flash_select_zip": "📁 Select ROM (ZIP)",
        "flash_selected": "Selected:",
        "flash_mode": "Flash Mode:",
        "flash_mode_normal": "Normal",
        "flash_mode_keep": "Keep Data",
        "flash_mode_wipe": "Wipe All",
        "flash_stop_on_error": "Stop on Error",
        "flash_auto_reboot": "Auto Reboot",
        "flash_start": "🚀 Start Flash",
        "flash_cancel": "⏹️ Cancel",
        "flash_progress": "Progress:",
        "flash_status_idle": "Idle",
        "flash_status_extracting": "Extracting...",
        "flash_status_flashing": "Flashing: {}",
        "flash_status_done": "✅ Done",
        "flash_status_error": "❌ Failed",
        "flash_status_cancelled": "⏹️ Cancelled",
        "unlock_title": "🔓 Unlock & FRP",
        "check_lock": "🔍 Check Lock",
        "check_root": "👑 Check Root",
        "check_frp": "🚫 Check FRP",
        "remove_locksettings": "🗑️ Remove locksettings",
        "remove_gatekeeper": "🔑 Remove gatekeeper",
        "remove_pattern": "📐 Remove Pattern",
        "format_data_fastboot": "🔐 Format Data",
        "erase_frp_fastboot": "🚫 Erase FRP (FB)",
        "erase_frp_adb": "🚫 Erase FRP (ADB)",
        "full_device_info": "📊 Full Info",
        "unlock_warning": "⚠️ Use at your own risk — data may be lost",
        "mtk_title": "⚙️ mtkclient — Integrated",
        "run_gui": "🖥️ Official GUI",
        "read_gpt": "📋 Read GPT",
        "read_part": "Read partition:",
        "read_btn": "Read",
        "write_part": "Write partition:",
        "pick": "Pick",
        "write_btn": "Write",
        "advanced": "⚠️ Advanced",
        "unlock_bl": "🔓 Unlock Bootloader",
        "wipe_frp": "🧹 Wipe FRP + Userdata",
        "edl_title": "⚡ Qualcomm EDL",
        "edl_check": "🔍 Check Connection",
        "edl_gpt": "📋 Read GPT",
        "edl_printgpt": "🖨️ Print Partitions",
        "edl_dump": "💾 Dump Partition",
        "edl_load": "📤 Write Partition",
        "edl_rw": "🔐 Read/Write",
        "edl_reset": "🔄 Reset",
        "edl_wipe": "🧹 Wipe Userdata",
        "edl_firehose": "🔥 Firehose Loader:",
        "edl_partition": "Partition:",
        "edl_image": "Image:",
        "log": "📋 Log:",
        "lang_btn": "🌐 العربية",
        "msg_wait": "⏳ ...",
        "msg_tools_ok": "✅ Platform-Tools ready",
        "msg_tools_missing": "⚠️ Platform-Tools missing",
        "msg_python_ok": "✅ Embedded Python ready",
        "msg_python_missing": "⚠️ Embedded Python missing",
        "msg_mtk_ok": "✅ mtkclient ready",
        "msg_mtk_missing": "⚠️ mtkclient missing",
        "msg_edl_ok": "✅ edl ready",
        "msg_edl_missing": "⚠️ edl missing",
        "msg_downloading_pt": "📥 Downloading Platform-Tools...",
        "msg_installed": "✅ Installed",
        "msg_error": "❌ {}",
        "msg_adb": "— ADB —",
        "msg_fastboot": "— Fastboot —",
        "msg_running_gui": "🖥️ Launching mtk_gui...",
        "msg_no_embed": "❌ Embedded Python missing",
        "msg_no_gui": "❌ mtk_gui.py missing",
        "msg_no_mtk": "❌ mtkclient missing",
        "msg_no_edl": "❌ edl missing",
        "msg_running_cmd": "⚙️ {}",
        "confirm_write": "Write {} from {}?",
        "confirm_unlock": "Unlocking bootloader will erase all data! Sure?",
        "confirm_wipe": "Wipe FRP and Userdata permanently!",
        "confirm_format": "All data will be wiped! Sure?",
        "confirm_flash": "Start flashing {} partitions?",
        "err_check": "Check fields",
        "err": "Error",
        "confirm": "Confirm",
        "warn": "Warning",
    },
}


def run(cmd, timeout=60, cwd=None, env=None):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout,
                           encoding="utf-8", errors="ignore", cwd=cwd, env=env,
                           creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
        return (r.stdout or "") + (r.stderr or "")
    except Exception as e:
        return f"Error: {e}"


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.lang = "ar"
        self.t = LANG[self.lang]

        self.flash_zip = ""
        self.flash_cancel = False
        self.flash_temp = TEMP_FLASH

        self.geometry("1020x820")
        self.resizable(True, True)

        self.build_ui()
        self.check_tools()

    def tr(self, key, *args):
        s = self.t.get(key, key)
        if args:
            try:
                return s.format(*args)
            except Exception:
                return s
        return s

    def build_ui(self):
        for w in self.winfo_children():
            w.destroy()

        self.title(self.tr("title"))

        top = ctk.CTkFrame(self)
        top.pack(fill="x", padx=15, pady=(10, 0))

        ctk.CTkLabel(top, text=self.tr("title"),
                     font=("Arial", 22, "bold")).pack(side="left", padx=5)

        ctk.CTkButton(top, text=self.tr("lang_btn"), width=110, height=32,
                      command=self.toggle_lang).pack(side="right", padx=5)

        self.tabs = ctk.CTkTabview(self, width=970, height=640)
        self.tabs.pack(padx=15, pady=5, fill="both", expand=True)

        self.tab_adb = self.tabs.add(self.tr("tab_adb"))
        self.tab_flash = self.tabs.add(self.tr("tab_flash"))
        self.tab_unlock = self.tabs.add(self.tr("tab_unlock"))
        self.tab_mtk = self.tabs.add(self.tr("tab_mtk"))
        self.tab_edl = self.tabs.add(self.tr("tab_edl"))

        self.build_adb_tab()
        self.build_flash_tab()
        self.build_unlock_tab()
        self.build_mtk_tab()
        self.build_edl_tab()

        ctk.CTkLabel(self, text=self.tr("log"),
                     font=("Arial", 13, "bold")).pack(anchor="w", padx=15)

        self.log_box = ctk.CTkTextbox(self, height=110, font=("Consolas", 11))
        self.log_box.pack(fill="x", padx=15, pady=(0, 10))

    def toggle_lang(self):
        self.lang = "en" if self.lang == "ar" else "ar"
        self.t = LANG[self.lang]
        self.build_ui()
        self.check_tools()

    def log(self, t):
        self.log_box.insert("end", str(t) + "\n")
        self.log_box.see("end")
        self.update_idletasks()

    def async_run(self, fn):
        def wrap():
            self.log(self.tr("msg_wait"))
            self.log(fn())
        threading.Thread(target=wrap, daemon=True).start()

    # ============ ADB Tab ============
    def build_adb_tab(self):
        f = self.tab_adb
        btns = [
            (self.tr("download_tools"), self.download_tools),
            (self.tr("detect"), self.detect),
            (self.tr("device_info"), self.info),
            (self.tr("reboot"), lambda: self.async_run(lambda: run([ADB, "reboot"]))),
            (self.tr("fastboot"), lambda: self.async_run(lambda: run([ADB, "reboot", "bootloader"]))),
            (self.tr("reboot_recovery"), lambda: self.async_run(lambda: run([ADB, "reboot", "recovery"]))),
            (self.tr("reboot_edl"), lambda: self.async_run(lambda: run([ADB, "reboot", "edl"]))),
            (self.tr("exit_fastboot"), lambda: self.async_run(lambda: run([FASTBOOT, "reboot"]))),
        ]
        for i, (t, fn) in enumerate(btns):
            ctk.CTkButton(f, text=t, width=210, height=36,
                          command=fn).grid(row=i // 3, column=i % 3, padx=8, pady=8)

    # ============ Flash Tab ============
    def build_flash_tab(self):
        f = self.tab_flash

        ctk.CTkLabel(f, text=self.tr("flash_title"),
                     font=("Arial", 16, "bold")).pack(pady=8)

        # اختيار ZIP
        zf = ctk.CTkFrame(f)
        zf.pack(pady=6)
        ctk.CTkButton(zf, text=self.tr("flash_select_zip"), width=250, height=38,
                      fg_color="green", hover_color="darkgreen",
                      command=self.pick_flash_zip).pack(side="left", padx=8)
        self.flash_zip_label = ctk.CTkLabel(zf, text=self.tr("flash_status_idle"),
                                             font=("Arial", 11), text_color="gray")
        self.flash_zip_label.pack(side="left", padx=10)

        # الإعدادات
        opts = ctk.CTkFrame(f)
        opts.pack(pady=6)

        ctk.CTkLabel(opts, text=self.tr("flash_mode")).grid(row=0, column=0, padx=5, pady=5)
        self.flash_mode = ctk.CTkOptionMenu(
            opts, width=180,
            values=[self.tr("flash_mode_normal"),
                    self.tr("flash_mode_keep"),
                    self.tr("flash_mode_wipe")]
        )
        self.flash_mode.grid(row=0, column=1, padx=5, pady=5)

        self.chk_stop = ctk.CTkCheckBox(opts, text=self.tr("flash_stop_on_error"))
        self.chk_stop.grid(row=0, column=2, padx=10, pady=5)
        self.chk_stop.select()

        self.chk_reboot = ctk.CTkCheckBox(opts, text=self.tr("flash_auto_reboot"))
        self.chk_reboot.grid(row=0, column=3, padx=10, pady=5)
        self.chk_reboot.select()

        # شريط التقدم
        pf = ctk.CTkFrame(f)
        pf.pack(pady=8, fill="x", padx=20)
        ctk.CTkLabel(pf, text=self.tr("flash_progress"),
                     font=("Arial", 12, "bold")).pack(anchor="w")
        self.flash_progress = ctk.CTkProgressBar(pf, height=20)
        self.flash_progress.pack(fill="x", pady=5)
        self.flash_progress.set(0)

        self.flash_status = ctk.CTkLabel(pf, text=self.tr("flash_status_idle"),
                                          font=("Arial", 11))
        self.flash_status.pack()

        # أزرار البدء/الإلغاء
        bf = ctk.CTkFrame(f)
        bf.pack(pady=8)
        ctk.CTkButton(bf, text=self.tr("flash_start"), width=200, height=45,
                      fg_color="green", hover_color="darkgreen",
                      font=("Arial", 14, "bold"),
                      command=self.start_flash).pack(side="left", padx=6)
        ctk.CTkButton(bf, text=self.tr("flash_cancel"), width=200, height=45,
                      fg_color="red", hover_color="darkred",
                      font=("Arial", 14, "bold"),
                      command=self.cancel_flash).pack(side="left", padx=6)

        # قائمة الأقسام
        ctk.CTkLabel(f, text="📋 Partitions:",
                     font=("Arial", 12, "bold")).pack(anchor="w", padx=20, pady=(15, 3))
        self.part_list = ctk.CTkTextbox(f, height=150, font=("Consolas", 11))
        self.part_list.pack(fill="both", expand=True, padx=20, pady=(0, 10))

    # ============ Unlock Tab ============
    def build_unlock_tab(self):
        f = self.tab_unlock

        ctk.CTkLabel(f, text=self.tr("unlock_title"),
                     font=("Arial", 15, "bold")).pack(pady=5)

        ctk.CTkLabel(f, text=self.tr("unlock_warning"),
                     font=("Arial", 11), text_color="orange").pack(pady=4)

        row = ctk.CTkFrame(f)
        row.pack(pady=6)
        ctk.CTkButton(row, text=self.tr("check_lock"), width=180,
                      command=self.check_lock).pack(side="left", padx=4)
        ctk.CTkButton(row, text=self.tr("check_root"), width=180,
                      command=self.check_root).pack(side="left", padx=4)
        ctk.CTkButton(row, text=self.tr("check_frp"), width=180,
                      command=self.check_frp).pack(side="left", padx=4)

        row2 = ctk.CTkFrame(f)
        row2.pack(pady=4)
        ctk.CTkButton(row2, text=self.tr("remove_locksettings"), width=250,
                      fg_color="orange", hover_color="darkorange",
                      command=self.remove_locksettings).pack(side="left", padx=4)
        ctk.CTkButton(row2, text=self.tr("remove_gatekeeper"), width=250,
                      fg_color="orange", hover_color="darkorange",
                      command=self.remove_gatekeeper).pack(side="left", padx=4)

        row3 = ctk.CTkFrame(f)
        row3.pack(pady=4)
        ctk.CTkButton(row3, text=self.tr("remove_pattern"), width=250,
                      fg_color="orange", hover_color="darkorange",
                      command=self.remove_pattern).pack(side="left", padx=4)
        ctk.CTkButton(row3, text=self.tr("full_device_info"), width=250,
                      command=self.full_info).pack(side="left", padx=4)

        row4 = ctk.CTkFrame(f)
        row4.pack(pady=4)
        ctk.CTkButton(row4, text=self.tr("erase_frp_adb"), width=250,
                      fg_color="red", hover_color="darkred",
                      command=self.erase_frp_adb).pack(side="left", padx=4)

        row5 = ctk.CTkFrame(f)
        row5.pack(pady=4)
        ctk.CTkButton(row5, text=self.tr("erase_frp_fastboot"), width=250,
                      fg_color="red", hover_color="darkred",
                      command=self.erase_frp_fastboot).pack(side="left", padx=4)
        ctk.CTkButton(row5, text=self.tr("format_data_fastboot"), width=250,
                      fg_color="red", hover_color="darkred",
                      command=self.format_data_fastboot).pack(side="left", padx=4)

    # ============ MTK Tab ============
    def build_mtk_tab(self):
        f = self.tab_mtk
        ctk.CTkLabel(f, text=self.tr("mtk_title"),
                     font=("Arial", 15, "bold")).pack(pady=5)
        ctk.CTkButton(f, text=self.tr("run_gui"), width=280,
                      fg_color="green", hover_color="darkgreen",
                      command=self.run_mtk_gui).pack(pady=4)
        ctk.CTkButton(f, text=self.tr("read_gpt"), width=280,
                      command=lambda: self.mtk_cmd(["printgpt"])).pack(pady=4)

        row = ctk.CTkFrame(f)
        row.pack(pady=4)
        ctk.CTkLabel(row, text=self.tr("read_part")).pack(side="left", padx=5)
        self.mtk_read_part = ctk.CTkEntry(row, width=120)
        self.mtk_read_part.pack(side="left", padx=5)
        self.mtk_read_part.insert(0, "boot")
        ctk.CTkButton(row, text=self.tr("read_btn"), width=80,
                      command=self.mtk_read).pack(side="left")

        row2 = ctk.CTkFrame(f)
        row2.pack(pady=4)
        ctk.CTkLabel(row2, text=self.tr("write_part")).pack(side="left", padx=5)
        self.mtk_write_part = ctk.CTkEntry(row2, width=120)
        self.mtk_write_part.pack(side="left", padx=5)
        self.mtk_write_part.insert(0, "boot")
        self.mtk_write_file = ctk.CTkEntry(row2, width=200)
        self.mtk_write_file.pack(side="left", padx=5)
        ctk.CTkButton(row2, text=self.tr("pick"), width=60,
                      command=self.pick_mtk_file).pack(side="left")
        ctk.CTkButton(row2, text=self.tr("write_btn"), width=70, fg_color="red",
                      hover_color="darkred",
                      command=self.mtk_write).pack(side="left", padx=5)

        ctk.CTkLabel(f, text=self.tr("advanced"), font=("Arial", 12, "bold"),
                     text_color="orange").pack(pady=(15, 3))
        ctk.CTkButton(f, text=self.tr("unlock_bl"), width=300,
                      fg_color="orange", hover_color="darkorange",
                      command=self.mtk_unlock).pack(pady=3)
        ctk.CTkButton(f, text=self.tr("wipe_frp"), width=300,
                      fg_color="orange", hover_color="darkorange",
                      command=self.mtk_wipe).pack(pady=3)

    # ============ EDL Tab ============
    def build_edl_tab(self):
        f = self.tab_edl
        ctk.CTkLabel(f, text=self.tr("edl_title"),
                     font=("Arial", 15, "bold")).pack(pady=5)

        lf = ctk.CTkFrame(f)
        lf.pack(pady=4)
        ctk.CTkLabel(lf, text=self.tr("edl_firehose")).pack(side="left", padx=5)
        self.edl_loader_entry = ctk.CTkEntry(lf, width=380)
        self.edl_loader_entry.pack(side="left", padx=5)
        ctk.CTkButton(lf, text=self.tr("pick"), width=70,
                      command=self.pick_edl_loader).pack(side="left", padx=5)

        row = ctk.CTkFrame(f)
        row.pack(pady=4)
        ctk.CTkButton(row, text=self.tr("edl_check"), width=200,
                      command=self.edl_check).pack(side="left", padx=5)
        ctk.CTkButton(row, text=self.tr("edl_printgpt"), width=200,
                      command=self.edl_printgpt).pack(side="left", padx=5)

        rp = ctk.CTkFrame(f)
        rp.pack(pady=4)
        ctk.CTkLabel(rp, text=self.tr("edl_partition")).pack(side="left", padx=5)
        self.edl_read_part = ctk.CTkEntry(rp, width=140)
        self.edl_read_part.pack(side="left", padx=5)
        self.edl_read_part.insert(0, "boot")
        ctk.CTkButton(rp, text=self.tr("edl_dump"), width=120,
                      command=self.edl_dump).pack(side="left", padx=5)

        wp = ctk.CTkFrame(f)
        wp.pack(pady=4)
        ctk.CTkLabel(wp, text=self.tr("edl_partition")).pack(side="left", padx=5)
        self.edl_write_part = ctk.CTkEntry(wp, width=100)
        self.edl_write_part.pack(side="left", padx=5)
        self.edl_write_part.insert(0, "boot")
        self.edl_write_file = ctk.CTkEntry(wp, width=220)
        self.edl_write_file.pack(side="left", padx=5)
        ctk.CTkButton(wp, text=self.tr("pick"), width=60,
                      command=self.pick_edl_file).pack(side="left", padx=3)
        ctk.CTkButton(wp, text=self.tr("edl_load"), width=90, fg_color="red",
                      hover_color="darkred",
                      command=self.edl_write).pack(side="left", padx=5)

        ctk.CTkLabel(f, text=self.tr("advanced"), font=("Arial", 12, "bold"),
                     text_color="orange").pack(pady=(15, 3))
        ops = ctk.CTkFrame(f)
        ops.pack(pady=4)
        ctk.CTkButton(ops, text=self.tr("edl_rw"), width=200,
                      fg_color="orange", hover_color="darkorange",
                      command=self.edl_rw).pack(side="left", padx=3)
        ctk.CTkButton(ops, text=self.tr("edl_reset"), width=180,
                      command=self.edl_reset).pack(side="left", padx=3)
        ctk.CTkButton(ops, text=self.tr("edl_wipe"), width=180,
                      fg_color="orange", hover_color="darkorange",
                      command=self.edl_wipe).pack(side="left", padx=3)

    # ============ Flash Logic ============
    def pick_flash_zip(self):
        p = filedialog.askopenfilename(
            filetypes=[("ROM ZIP", "*.zip"), ("All", "*.*")])
        if p:
            self.flash_zip = p
            self.flash_zip_label.configure(
                text=os.path.basename(p), text_color="lightgreen")
            self.log(f"📁 {p}")

    def extract_zip(self, zip_path):
        if os.path.exists(self.flash_temp):
            shutil.rmtree(self.flash_temp, ignore_errors=True)
        os.makedirs(self.flash_temp, exist_ok=True)
        with zipfile.ZipFile(zip_path, "r") as z:
            z.extractall(self.flash_temp)

    def find_images(self):
        """البحث عن ملفات img في مجلد الروم"""
        images = {}
        for root, dirs, files in os.walk(self.flash_temp):
            for f in files:
                if f.endswith(".img"):
                    name = os.path.splitext(f)[0]
                    images[name] = os.path.join(root, f)
        return images

    def start_flash(self):
        if not self.flash_zip or not os.path.exists(self.flash_zip):
            messagebox.showerror(self.tr("err"), "Select a ROM ZIP first")
            return

        self.flash_cancel = False

        def task():
            try:
                # فك الضغط
                self.flash_status.configure(text=self.tr("flash_status_extracting"))
                self.update_idletasks()
                self.log("📦 Extracting...")
                self.extract_zip(self.flash_zip)

                images = self.find_images()
                if not images:
                    self.log("❌ No .img files found")
                    self.flash_status.configure(text=self.tr("flash_status_error"))
                    return

                self.log(f"✅ Found {len(images)} images:")
                for name in images:
                    self.log(f"  • {name}")
                    self.part_list.insert("end", f"{name}\n")

                # بدء الفلاش
                mode = self.flash_mode.get()
                total = len(images)
                done = 0

                self.flash_progress.set(0)
                self.flash_status.configure(text="...")

                for name, path in images.items():
                    if self.flash_cancel:
                        self.flash_status.configure(text=self.tr("flash_status_cancelled"))
                        return

                    # skip userdata إذا "الاحتفاظ بالبيانات"
                    if mode == self.tr("flash_mode_keep") and name in ["userdata", "metadata"]:
                        self.log(f"⏭️ Skipping {name} (keep data)")
                        done += 1
                        continue

                    self.flash_status.configure(
                        text=self.tr("flash_status_flashing", name))
                    self.log(f"🚀 Flashing: {name}")

                    out = run([FASTBOOT, "flash", name, path], timeout=1200)
                    self.log(out[-500:])

                    if "FAILED" in out or "error" in out.lower():
                        self.log(f"❌ {name} failed")
                        if self.chk_stop.get():
                            self.flash_status.configure(text=self.tr("flash_status_error"))
                            return

                    done += 1
                    self.flash_progress.set(done / total)

                # إعادة تشغيل
                if self.chk_reboot.get() and not self.flash_cancel:
                    self.log("🔄 Rebooting...")
                    run([FASTBOOT, "reboot"])

                self.flash_status.configure(text=self.tr("flash_status_done"))
                self.flash_progress.set(1)
                self.log("🎉 Flash completed!")

            except Exception as e:
                self.log(f"❌ {e}")
                self.flash_status.configure(text=self.tr("flash_status_error"))

        threading.Thread(target=task, daemon=True).start()

    def cancel_flash(self):
        self.flash_cancel = True
        self.log("⏹️ Cancelling...")
        self.flash_status.configure(text=self.tr("flash_status_cancelled"))

    # ============ Common ============
    def check_tools(self):
        if os.path.exists(ADB):
            self.log(self.tr("msg_tools_ok", TOOLS_DIR))
        else:
            self.log(self.tr("msg_tools_missing"))
        if os.path.exists(EMBED_PY):
            self.log(self.tr("msg_python_ok"))
        else:
            self.log(self.tr("msg_python_missing"))
        if os.path.exists(MTK_SCRIPT):
            self.log(self.tr("msg_mtk_ok"))
        else:
            self.log(self.tr("msg_mtk_missing"))
        if os.path.exists(EDL_SCRIPT):
            self.log(self.tr("msg_edl_ok"))
        else:
            self.log(self.tr("msg_edl_missing"))

    def download_tools(self):
        def task():
            try:
                os.makedirs(TOOLS_DIR, exist_ok=True)
                zip_path = os.path.join(BASE_DIR, "pt.zip")
                self.log(self.tr("msg_downloading_pt"))
                urllib.request.urlretrieve(PLATFORM_TOOLS_URL, zip_path)
                with zipfile.ZipFile(zip_path, "r") as z:
                    z.extractall(TOOLS_DIR)
                sub = os.path.join(TOOLS_DIR, "platform-tools")
                if os.path.isdir(sub):
                    for item in os.listdir(sub):
                        shutil.move(os.path.join(sub, item), TOOLS_DIR)
                    shutil.rmtree(sub, ignore_errors=True)
                os.remove(zip_path)
                self.log(self.tr("msg_installed"))
                self.check_tools()
            except Exception as e:
                self.log(self.tr("msg_error", e))
        threading.Thread(target=task, daemon=True).start()

    def detect(self):
        def t():
            self.log("=" * 50)
            self.log(self.tr("msg_adb") + "\n" + run([ADB, "devices", "-l"]))
            self.log(self.tr("msg_fastboot") + "\n" + run([FASTBOOT, "devices"]))
        threading.Thread(target=t, daemon=True).start()

    def info(self):
        def t():
            self.log("=" * 50)
            for p in ["ro.product.model", "ro.product.brand",
                      "ro.build.version.release", "ro.serialno",
                      "ro.product.cpu.abi", "ro.build.version.sdk"]:
                self.log(f"{p}: {run([ADB, 'shell', 'getprop', p]).strip()}")
        threading.Thread(target=t, daemon=True).start()

    # ============ Unlock Ops ============
    def check_lock(self):
        def t():
            self.log("=" * 50)
            out = run([ADB, "shell", "dumpsys", "device_policy"])
            for line in out.splitlines():
                if "mPasswordOwner" in line or "PasswordQuality" in line:
                    self.log(line.strip())
        threading.Thread(target=t, daemon=True).start()

    def check_root(self):
        def t():
            self.log("=" * 50)
            out = run([ADB, "shell", "which", "su"]).strip()
            self.log(f"👑 Root: {'✅ ' + out if out else '❌'}")
        threading.Thread(target=t, daemon=True).start()

    def check_frp(self):
        def t():
            self.log("=" * 50)
            out = run([ADB, "shell", "getprop", "ro.frp.pst"]).strip()
            self.log(f"FRP partition: {out or 'N/A'}")
        threading.Thread(target=t, daemon=True).start()

    def remove_locksettings(self):
        def t():
            for c in ["rm -f /data/system/locksettings.db",
                      "rm -f /data/system/locksettings.db-shm",
                      "rm -f /data/system/locksettings.db-wal"]:
                self.log(f"$ {c}")
                self.log(run([ADB, "shell", "su", "-c", c]))
        threading.Thread(target=t, daemon=True).start()

    def remove_gatekeeper(self):
        def t():
            for c in ["rm -f /data/system/gatekeeper.password.key",
                      "rm -f /data/system/gatekeeper.pattern.key"]:
                self.log(f"$ {c}")
                self.log(run([ADB, "shell", "su", "-c", c]))
        threading.Thread(target=t, daemon=True).start()

    def remove_pattern(self):
        def t():
            c = "rm -f /data/system/gesture.key"
            self.log(f"$ {c}")
            self.log(run([ADB, "shell", "su", "-c", c]))
        threading.Thread(target=t, daemon=True).start()

    def full_info(self):
        def t():
            out = run([ADB, "shell", "getprop"], timeout=30)
            self.log(out[:5000])
        threading.Thread(target=t, daemon=True).start()

    def erase_frp_adb(self):
        if not messagebox.askyesno(self.tr("warn"), self.tr("confirm_wipe")):
            return
        def t():
            c = "rm -rf /persistent/frp/* /data/system/users/0/frp/*"
            self.log(run([ADB, "shell", "su", "-c", c]))
        threading.Thread(target=t, daemon=True).start()

    def erase_frp_fastboot(self):
        if not messagebox.askyesno(self.tr("warn"), self.tr("confirm_wipe")):
            return
        self.async_run(lambda: run([FASTBOOT, "erase", "frp"], timeout=120))

    def format_data_fastboot(self):
        if not messagebox.askyesno(self.tr("warn"), self.tr("confirm_format")):
            return
        self.async_run(lambda: run([FASTBOOT, "erase", "userdata"], timeout=300))

    # ============ MTK ============
    def run_mtk_gui(self):
        if not os.path.exists(EMBED_PY):
            self.log(self.tr("msg_no_embed"))
            return
        gui = os.path.join(MTK_DIR, "mtk_gui.py")
        if not os.path.exists(gui):
            self.log(self.tr("msg_no_gui"))
            return
        subprocess.Popen([EMBED_PY, "mtk_gui.py"], cwd=MTK_DIR,
                         creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == "nt" else 0)

    def mtk_cmd(self, args, timeout=600):
        if not os.path.exists(MTK_SCRIPT):
            self.log(self.tr("msg_no_mtk"))
            return
        def t():
            self.log("=" * 50)
            self.log(run([EMBED_PY, "mtk.py"] + args, timeout=timeout, cwd=MTK_DIR))
        threading.Thread(target=t, daemon=True).start()

    def mtk_read(self):
        p = self.mtk_read_part.get().strip()
        if p:
            self.mtk_cmd(["r", p, f"{p}.img"])

    def pick_mtk_file(self):
        f = filedialog.askopenfilename(filetypes=[("Images", "*.img")])
        if f:
            self.mtk_write_file.delete(0, "end")
            self.mtk_write_file.insert(0, f)

    def mtk_write(self):
        p = self.mtk_write_part.get().strip()
        f = self.mtk_write_file.get().strip()
        if not p or not os.path.exists(f):
            messagebox.showerror(self.tr("err"), self.tr("err_check"))
            return
        if messagebox.askyesno(self.tr("confirm"), self.tr("confirm_write", p, f)):
            self.mtk_cmd(["w", p, f])

    def mtk_unlock(self):
        if messagebox.askyesno(self.tr("warn"), self.tr("confirm_unlock")):
            self.mtk_cmd(["da", "seccfg", "unlock"])

    def mtk_wipe(self):
        if messagebox.askyesno(self.tr("warn"), self.tr("confirm_wipe")):
            self.mtk_cmd(["e", "frp,userdata,metadata,md_udc"])

    # ============ EDL ============
    def edl_base(self):
        args = [EMBED_PY, "edl.py"]
        loader = self.edl_loader_entry.get().strip()
        if loader and os.path.exists(loader):
            args += ["--loader", loader]
        return args

    def edl_run(self, args, timeout=1200):
        if not os.path.exists(EDL_SCRIPT):
            self.log(self.tr("msg_no_edl"))
            return
        def t():
            full = self.edl_base() + args
            self.log("=" * 50)
            self.log(run(full, timeout=timeout, cwd=EDL_DIR))
        threading.Thread(target=t, daemon=True).start()

    def pick_edl_loader(self):
        p = filedialog.askopenfilename(
            filetypes=[("Loader", "*.mbn *.bin *.elf"), ("All", "*.*")])
        if p:
            self.edl_loader_entry.delete(0, "end")
            self.edl_loader_entry.insert(0, p)

    def pick_edl_file(self):
        p = filedialog.askopenfilename(filetypes=[("Images", "*.img")])
        if p:
            self.edl_write_file.delete(0, "end")
            self.edl_write_file.insert(0, p)

    def edl_check(self):
        self.edl_run(["printgpt"], timeout=120)

    def edl_printgpt(self):
        self.edl_run(["printgpt"])

    def edl_dump(self):
        p = self.edl_read_part.get().strip()
        if p:
            self.edl_run(["r", p, f"{p}.img"])

    def edl_write(self):
        p = self.edl_write_part.get().strip()
        f = self.edl_write_file.get().strip()
        if not p or not os.path.exists(f):
            messagebox.showerror(self.tr("err"), self.tr("err_check"))
            return
        if messagebox.askyesno(self.tr("confirm"), self.tr("confirm_write", p, f)):
            self.edl_run(["w", p, f])

    def edl_rw(self):
        if messagebox.askyesno(self.tr("warn"), "Read/Write?"):
            self.edl_run(["--memory", "ufs", "printgpt"])

    def edl_reset(self):
        self.edl_run(["reset"])

    def edl_wipe(self):
        if messagebox.askyesno(self.tr("warn"), self.tr("confirm_wipe")):
            self.edl_run(["e", "userdata"])


if __name__ == "__main__":
    App().mainloop()