import customtkinter as ctk
from tkinter import filedialog, messagebox
import subprocess
import os
import sys
import threading
import urllib.request
import zipfile
import shutil

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TOOLS_DIR = os.path.join(BASE_DIR, "platform-tools")
MTK_DIR = os.path.join(BASE_DIR, "mtkclient")
EDL_DIR = os.path.join(BASE_DIR, "edl")
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
        "tab_unlock": "🔓 فك القفل",
        "tab_mtk": "MTK (ميدياتك)",
        "tab_edl": "Qualcomm EDL",
        # ADB
        "download_tools": "📥 تحميل Platform-Tools",
        "detect": "🔍 اكتشاف الأجهزة",
        "device_info": "📱 معلومات الجهاز",
        "reboot": "🔄 إعادة تشغيل",
        "fastboot": "⚡ وضع Fastboot",
        "exit_fastboot": "🔌 خروج من Fastboot",
        "reboot_recovery": "♻️ وضع Recovery",
        "reboot_edl": "📡 وضع EDL",
        # Unlock
        "unlock_title": "🔓 فك القفل و FRP",
        "check_lock": "🔍 فحص حالة القفل",
        "check_root": "👑 فحص الروت",
        "check_frp": "🚫 فحص حالة FRP",
        "remove_locksettings": "🗑️ حذف locksettings.db (يحتاج روت)",
        "remove_gatekeeper": "🔑 حذف gatekeeper (يحتاج روت)",
        "remove_pattern": "📐 حذف النمط (يحتاج روت)",
        "format_data_fastboot": "🔐 فورمات Data (Fastboot)",
        "erase_frp_fastboot": "🚫 مسح FRP (Fastboot)",
        "erase_frp_adb": "🚫 مسح FRP (ADB)",
        "full_device_info": "📊 معلومات كاملة",
        "unlock_warning": "⚠️ هذه العمليات قد تمسح كل بيانات الجهاز. استخدمها على مسؤوليتك.",
        # MTK
        "mtk_title": "⚙️ mtkclient — ميدياتك (مدمج)",
        "run_gui": "🖥️ تشغيل الواجهة الرسمية",
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
        "edl_title": "⚡ Qualcomm EDL — مدمج",
        "edl_check": "🔍 فحص اتصال EDL",
        "edl_gpt": "📋 قراءة GPT",
        "edl_printgpt": "🖨️ طباعة جدول الأقسام",
        "edl_dump": "💾 استخراج قسم",
        "edl_load": "📤 كتابة قسم",
        "edl_rw": "🔐 قراءة/كتابة (Read-Write)",
        "edl_reset": "🔄 إعادة تشغيل الجهاز",
        "edl_wipe": "🧹 محو Userdata",
        "edl_firehose": "🔥 ملف Firehose (Loader)",
        "edl_partition": "اسم القسم:",
        "edl_image": "ملف الصورة:",
        "edl_loader": "ملف Firehose:",
        # عام
        "log": "📋 السجل:",
        "lang_btn": "🌐 English",
        "msg_wait": "⏳ ...",
        "msg_tools_ok": "✅ Platform-Tools: {}",
        "msg_tools_missing": "⚠️ Platform-Tools غير مثبتة",
        "msg_python_ok": "✅ Python مدمج: {}",
        "msg_python_missing": "⚠️ Python المدمج غير موجود",
        "msg_mtk_ok": "✅ mtkclient: {}",
        "msg_mtk_missing": "⚠️ mtkclient غير موجود",
        "msg_edl_ok": "✅ edl: {}",
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
        "msg_no_device": "❌ لا يوجد جهاز متصل عبر ADB",
        "msg_running_cmd": "⚙️ {}",
        "confirm_write": "كتابة {} من {}؟",
        "confirm_unlock": "فك قفل البوتلودر سيمسح كل البيانات!\nمتأكد؟",
        "confirm_wipe": "مسح FRP و Userdata نهائياً!",
        "confirm_format": "سيتم محو كل بيانات الجهاز!\nمتأكد؟",
        "err_check": "تحقق من الحقول",
        "err": "خطأ",
        "confirm": "تأكيد",
        "warn": "تحذير",
    },
    "en": {
        "title": "🛠️ Android Tool",
        "tab_adb": "ADB / Fastboot",
        "tab_unlock": "🔓 Unlock",
        "tab_mtk": "MTK (MediaTek)",
        "tab_edl": "Qualcomm EDL",
        "download_tools": "📥 Download Platform-Tools",
        "detect": "🔍 Detect Devices",
        "device_info": "📱 Device Info",
        "reboot": "🔄 Reboot",
        "fastboot": "⚡ Fastboot Mode",
        "exit_fastboot": "🔌 Exit Fastboot",
        "reboot_recovery": "♻️ Recovery Mode",
        "reboot_edl": "📡 EDL Mode",
        "unlock_title": "🔓 Unlock & FRP",
        "check_lock": "🔍 Check Lock Status",
        "check_root": "👑 Check Root",
        "check_frp": "🚫 Check FRP Status",
        "remove_locksettings": "🗑️ Remove locksettings.db (Root)",
        "remove_gatekeeper": "🔑 Remove gatekeeper (Root)",
        "remove_pattern": "📐 Remove Pattern (Root)",
        "format_data_fastboot": "🔐 Format Data (Fastboot)",
        "erase_frp_fastboot": "🚫 Erase FRP (Fastboot)",
        "erase_frp_adb": "🚫 Erase FRP (ADB)",
        "full_device_info": "📊 Full Device Info",
        "unlock_warning": "⚠️ These operations may wipe all device data. Use at your own risk.",
        "mtk_title": "⚙️ mtkclient — MediaTek (Integrated)",
        "run_gui": "🖥️ Launch Official GUI",
        "read_gpt": "📋 Read GPT",
        "read_part": "Read partition:",
        "read_btn": "Read",
        "write_part": "Write partition:",
        "pick": "Pick",
        "write_btn": "Write",
        "advanced": "⚠️ Advanced Operations",
        "unlock_bl": "🔓 Unlock Bootloader",
        "wipe_frp": "🧹 Wipe FRP + Userdata",
        "edl_title": "⚡ Qualcomm EDL — Integrated",
        "edl_check": "🔍 Check EDL Connection",
        "edl_gpt": "📋 Read GPT",
        "edl_printgpt": "🖨️ Print Partition Table",
        "edl_dump": "💾 Dump Partition",
        "edl_load": "📤 Write Partition",
        "edl_rw": "🔐 Read/Write Mode",
        "edl_reset": "🔄 Reset Device",
        "edl_wipe": "🧹 Wipe Userdata",
        "edl_firehose": "🔥 Firehose (Loader) File",
        "edl_partition": "Partition:",
        "edl_image": "Image file:",
        "edl_loader": "Firehose file:",
        "log": "📋 Log:",
        "lang_btn": "🌐 العربية",
        "msg_wait": "⏳ ...",
        "msg_tools_ok": "✅ Platform-Tools: {}",
        "msg_tools_missing": "⚠️ Platform-Tools not installed",
        "msg_python_ok": "✅ Embedded Python: {}",
        "msg_python_missing": "⚠️ Embedded Python not found",
        "msg_mtk_ok": "✅ mtkclient: {}",
        "msg_mtk_missing": "⚠️ mtkclient not found",
        "msg_edl_ok": "✅ edl: {}",
        "msg_edl_missing": "⚠️ edl not found",
        "msg_downloading_pt": "📥 Downloading Platform-Tools...",
        "msg_installed": "✅ Installed",
        "msg_error": "❌ {}",
        "msg_adb": "— ADB —",
        "msg_fastboot": "— Fastboot —",
        "msg_running_gui": "🖥️ Launching mtk_gui...",
        "msg_no_embed": "❌ Embedded Python not found",
        "msg_no_gui": "❌ mtk_gui.py not found",
        "msg_no_mtk": "❌ mtkclient not found",
        "msg_no_edl": "❌ edl not found",
        "msg_no_device": "❌ No device connected via ADB",
        "msg_running_cmd": "⚙️ {}",
        "confirm_write": "Write {} from {}?",
        "confirm_unlock": "Unlocking bootloader will erase all data!\nAre you sure?",
        "confirm_wipe": "Wipe FRP and Userdata permanently!",
        "confirm_format": "All device data will be wiped!\nAre you sure?",
        "err_check": "Check all fields",
        "err": "Error",
        "confirm": "Confirm",
        "warn": "Warning",
    },
}


def run(cmd, timeout=60, cwd=None, env=None, input_text=None):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout,
                           encoding="utf-8", errors="ignore", cwd=cwd, env=env,
                           input=input_text,
                           creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
        return (r.stdout or "") + (r.stderr or "")
    except Exception as e:
        return f"Error: {e}"


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.lang = "ar"
        self.t = LANG[self.lang]

        self.geometry("980x800")
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

        self.tabs = ctk.CTkTabview(self, width=930, height=630)
        self.tabs.pack(padx=15, pady=5, fill="both", expand=True)

        self.tab_adb = self.tabs.add(self.tr("tab_adb"))
        self.tab_unlock = self.tabs.add(self.tr("tab_unlock"))
        self.tab_mtk = self.tabs.add(self.tr("tab_mtk"))
        self.tab_edl = self.tabs.add(self.tr("tab_edl"))

        self.build_adb_tab()
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
            ctk.CTkButton(f, text=t, width=200, height=36,
                          command=fn).grid(row=i // 3, column=i % 3, padx=8, pady=8)

    # ============ Unlock Tab ============
    def build_unlock_tab(self):
        f = self.tab_unlock

        ctk.CTkLabel(f, text=self.tr("unlock_title"),
                     font=("Arial", 15, "bold")).pack(pady=5)

        ctk.CTkLabel(f, text=self.tr("unlock_warning"),
                     font=("Arial", 11), text_color="orange").pack(pady=4)

        # أزرار الفحص
        row = ctk.CTkFrame(f)
        row.pack(pady=6)
        ctk.CTkButton(row, text=self.tr("check_lock"), width=180,
                      command=self.check_lock).pack(side="left", padx=4)
        ctk.CTkButton(row, text=self.tr("check_root"), width=180,
                      command=self.check_root).pack(side="left", padx=4)
        ctk.CTkButton(row, text=self.tr("check_frp"), width=180,
                      command=self.check_frp).pack(side="left", padx=4)

        # أزرار الحذف (روت)
        ctk.CTkLabel(f, text="— " + self.tr("remove_locksettings") + " —",
                     font=("Arial", 11), text_color="gray").pack(pady=(15, 3))

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

        # FRP عبر ADB
        ctk.CTkLabel(f, text="— FRP —",
                     font=("Arial", 11), text_color="gray").pack(pady=(15, 3))
        row4 = ctk.CTkFrame(f)
        row4.pack(pady=4)
        ctk.CTkButton(row4, text=self.tr("erase_frp_adb"), width=250,
                      fg_color="red", hover_color="darkred",
                      command=self.erase_frp_adb).pack(side="left", padx=4)

        # Fastboot operations
        ctk.CTkLabel(f, text="— Fastboot —",
                     font=("Arial", 11), text_color="gray").pack(pady=(15, 3))
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
        ctk.CTkLabel(lf, text=self.tr("edl_loader")).pack(side="left", padx=5)
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

    # ============ Common ============
    def check_tools(self):
        if os.path.exists(ADB):
            self.log(self.tr("msg_tools_ok", TOOLS_DIR))
        else:
            self.log(self.tr("msg_tools_missing"))

        if os.path.exists(EMBED_PY):
            self.log(self.tr("msg_python_ok", EMBED_PY))
        else:
            self.log(self.tr("msg_python_missing"))

        if os.path.exists(MTK_SCRIPT):
            self.log(self.tr("msg_mtk_ok", MTK_DIR))
        else:
            self.log(self.tr("msg_mtk_missing"))

        if os.path.exists(EDL_SCRIPT):
            self.log(self.tr("msg_edl_ok", EDL_DIR))
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

    # ============ Unlock Operations ============
    def check_lock(self):
        def t():
            self.log("=" * 50)
            self.log("🔍 Lock status:")
            out = run([ADB, "shell", "dumpsys", "device_policy"])
            for line in out.splitlines():
                if "mPasswordOwner" in line or "PasswordQuality" in line:
                    self.log(line.strip())
        threading.Thread(target=t, daemon=True).start()

    def check_root(self):
        def t():
            self.log("=" * 50)
            out = run([ADB, "shell", "which", "su"]).strip()
            if out:
                self.log(f"👑 Root: ✅ ({out})")
            else:
                self.log("👑 Root: ❌ غير موجود")
        threading.Thread(target=t, daemon=True).start()

    def check_frp(self):
        def t():
            self.log("=" * 50)
            out = run([ADB, "shell", "getprop", "ro.frp.pst"]).strip()
            self.log(f"FRP partition: {out if out else 'غير محدد'}")
            out2 = run([ADB, "shell", "settings", "get", "global",
                        "device_provisioned"]).strip()
            self.log(f"Device Provisioned: {out2}")
        threading.Thread(target=t, daemon=True).start()

    def remove_locksettings(self):
        def t():
            self.log("=" * 50)
            cmds = [
                "rm -f /data/system/locksettings.db",
                "rm -f /data/system/locksettings.db-shm",
                "rm -f /data/system/locksettings.db-wal",
            ]
            for c in cmds:
                self.log(f"$ {c}")
                self.log(run([ADB, "shell", "su", "-c", c]))
            self.log("✅ تم")
        threading.Thread(target=t, daemon=True).start()

    def remove_gatekeeper(self):
        def t():
            self.log("=" * 50)
            cmds = [
                "rm -f /data/system/gatekeeper.password.key",
                "rm -f /data/system/gatekeeper.pattern.key",
            ]
            for c in cmds:
                self.log(f"$ {c}")
                self.log(run([ADB, "shell", "su", "-c", c]))
            self.log("✅ تم")
        threading.Thread(target=t, daemon=True).start()

    def remove_pattern(self):
        def t():
            self.log("=" * 50)
            c = "rm -f /data/system/gesture.key"
            self.log(f"$ {c}")
            self.log(run([ADB, "shell", "su", "-c", c]))
            self.log("✅ تم — أعد التشغيل")
        threading.Thread(target=t, daemon=True).start()

    def full_info(self):
        def t():
            self.log("=" * 50)
            self.log("📊 معلومات كاملة:")
            out = run([ADB, "shell", "getprop"], timeout=30)
            self.log(out[:5000])
        threading.Thread(target=t, daemon=True).start()

    def erase_frp_adb(self):
        if not messagebox.askyesno(self.tr("warn"), self.tr("confirm_wipe")):
            return
        def t():
            self.log("=" * 50)
            c = "rm -rf /persistent/frp/* /data/system/users/0/frp/*"
            self.log(f"$ {c}")
            self.log(run([ADB, "shell", "su", "-c", c]))
            self.log("✅ تم — أعد التشغيل")
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
        mtk_gui = os.path.join(MTK_DIR, "mtk_gui.py")
        if not os.path.exists(mtk_gui):
            self.log(self.tr("msg_no_gui"))
            return
        self.log(self.tr("msg_running_gui"))
        subprocess.Popen([EMBED_PY, "mtk_gui.py"], cwd=MTK_DIR,
                         creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == "nt" else 0)

    def mtk_cmd(self, args, timeout=600):
        if not os.path.exists(EMBED_PY):
            self.log(self.tr("msg_no_embed"))
            return
        if not os.path.exists(MTK_SCRIPT):
            self.log(self.tr("msg_no_mtk"))
            return
        def t():
            self.log("=" * 50)
            self.log(self.tr("msg_running_cmd", "mtk " + " ".join(args)))
            self.log(run([EMBED_PY, "mtk.py"] + args, timeout=timeout, cwd=MTK_DIR))
        threading.Thread(target=t, daemon=True).start()

    def mtk_read(self):
        part = self.mtk_read_part.get().strip()
        if part:
            self.mtk_cmd(["r", part, f"{part}.img"])

    def pick_mtk_file(self):
        p = filedialog.askopenfilename(filetypes=[("Images", "*.img *.bin")])
        if p:
            self.mtk_write_file.delete(0, "end")
            self.mtk_write_file.insert(0, p)

    def mtk_write(self):
        part = self.mtk_write_part.get().strip()
        f = self.mtk_write_file.get().strip()
        if not part or not os.path.exists(f):
            messagebox.showerror(self.tr("err"), self.tr("err_check"))
            return
        if not messagebox.askyesno(self.tr("confirm"), self.tr("confirm_write", part, f)):
            return
        self.mtk_cmd(["w", part, f])

    def mtk_unlock(self):
        if not messagebox.askyesno(self.tr("warn"), self.tr("confirm_unlock")):
            return
        self.mtk_cmd(["da", "seccfg", "unlock"])

    def mtk_wipe(self):
        if not messagebox.askyesno(self.tr("warn"), self.tr("confirm_wipe")):
            return
        self.mtk_cmd(["e", "frp,userdata,metadata,md_udc"])

    # ============ EDL ============
    def edl_base(self):
        args = [EMBED_PY, "edl.py"]
        loader = self.edl_loader_entry.get().strip()
        if loader and os.path.exists(loader):
            args += ["--loader", loader]
        return args

    def edl_run(self, args, timeout=1200):
        if not os.path.exists(EMBED_PY):
            self.log(self.tr("msg_no_embed"))
            return
        if not os.path.exists(EDL_SCRIPT):
            self.log(self.tr("msg_no_edl"))
            return
        def t():
            self.log("=" * 50)
            full = self.edl_base() + args
            self.log(self.tr("msg_running_cmd", "edl " + " ".join(args)))
            self.log(run(full, timeout=timeout, cwd=EDL_DIR))
        threading.Thread(target=t, daemon=True).start()

    def pick_edl_loader(self):
        p = filedialog.askopenfilename(
            filetypes=[("Loader", "*.mbn *.bin *.elf"), ("All", "*.*")])
        if p:
            self.edl_loader_entry.delete(0, "end")
            self.edl_loader_entry.insert(0, p)

    def pick_edl_file(self):
        p = filedialog.askopenfilename(
            filetypes=[("Images", "*.img *.bin"), ("All", "*.*")])
        if p:
            self.edl_write_file.delete(0, "end")
            self.edl_write_file.insert(0, p)

    def edl_check(self):
        self.edl_run(["printgpt"], timeout=120)

    def edl_printgpt(self):
        self.edl_run(["printgpt"])

    def edl_dump(self):
        part = self.edl_read_part.get().strip()
        if not part:
            messagebox.showerror(self.tr("err"), self.tr("err_check"))
            return
        self.edl_run(["r", part, f"{part}.img"])

    def edl_write(self):
        part = self.edl_write_part.get().strip()
        f = self.edl_write_file.get().strip()
        if not part or not os.path.exists(f):
            messagebox.showerror(self.tr("err"), self.tr("err_check"))
            return
        if not messagebox.askyesno(self.tr("confirm"),
                                    self.tr("confirm_write", part, f)):
            return
        self.edl_run(["w", part, f])

    def edl_rw(self):
        if not messagebox.askyesno(self.tr("warn"), "Enable Read/Write mode?"):
            return
        self.edl_run(["--memory", "ufs", "printgpt"])

    def edl_reset(self):
        self.edl_run(["reset"])

    def edl_wipe(self):
        if not messagebox.askyesno(self.tr("warn"), self.tr("confirm_wipe")):
            return
        self.edl_run(["e", "userdata"])


if __name__ == "__main__":
    App().mainloop()