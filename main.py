import customtkinter as ctk
from tkinter import filedialog, messagebox
import subprocess
import os
import sys
import threading
import urllib.request
import zipfile
import tarfile
import shutil
import json
import webbrowser
from datetime import datetime

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TOOLS_DIR = os.path.join(BASE_DIR, "platform-tools")
MTK_DIR = os.path.join(BASE_DIR, "mtkclient")
EDL_DIR = os.path.join(BASE_DIR, "edl")
HEIMDALL_DIR = os.path.join(BASE_DIR, "heimdall")
TEMP_FLASH = os.path.join(BASE_DIR, "flash_temp")
LOGS_DIR = os.path.join(BASE_DIR, "logs")
EMBED_PY = os.path.join(BASE_DIR, "python-embed", "python.exe")
ADB = os.path.join(TOOLS_DIR, "adb.exe")
FASTBOOT = os.path.join(TOOLS_DIR, "fastboot.exe")
MTK_SCRIPT = os.path.join(MTK_DIR, "mtk.py")
EDL_SCRIPT = os.path.join(EDL_DIR, "edl.py")
HEIMDALL = os.path.join(HEIMDALL_DIR, "heimdall.exe")

PLATFORM_TOOLS_URL = "https://dl.google.com/android/repository/platform-tools-latest-windows.zip"

APP_VERSION = "1.0.0"
GITHUB_REPO = "Gissa333/android-tool"
GITHUB_API = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"


LANG = {
    "ar": {
        "title": "🛠️ أداة الأندرويد",
        "tab_adb": "ADB / Fastboot",
        "tab_flash": "📦 فلاش الروم",
        "tab_xiaomi": "🟠 Xiaomi",
        "tab_huawei": "🟣 Huawei",
        "tab_samsung": "📱 Samsung",
        "tab_root": "🔓 TWRP & Root",
        "tab_unlock": "🔒 فك القفل",
        "tab_mtk": "MTK",
        "tab_edl": "Qualcomm EDL",
        "tab_about": "ℹ️ حول",
        "download_tools": "📥 تحميل Platform-Tools",
        "detect": "🔍 اكتشاف الأجهزة",
        "device_info": "📱 معلومات الجهاز",
        "reboot": "🔄 إعادة تشغيل",
        "fastboot": "⚡ وضع Fastboot",
        "reboot_recovery": "♻️ وضع Recovery",
        "reboot_edl": "📡 وضع EDL",
        "exit_fastboot": "🔌 خروج من Fastboot",
        # Huawei
        "huawei_title": "🟣 Huawei / Honor",
        "huawei_warning": "⚠️ الأجهزة الحديثة محمية بـ Huawei ID",
        "huawei_info": "📱 معلومات الجهاز",
        "huawei_fastboot": "⚡ وضع Fastboot",
        "huawei_recovery": "♻️ وضع Recovery",
        "huawei_erecovery": "🔄 وضع eRecovery",
        "huawei_flash_boot": "📦 فلاش boot.img",
        "huawei_flash_recovery": "📦 فلاش recovery.img",
        "huawei_flash_system": "📦 فلاش system.img",
        "huawei_flash_ramdisk": "📦 فلاش ramdisk.img",
        "huawei_flash_custom": "⚙️ فلاش قسم مخصص",
        "huawei_partition": "القسم:",
        "huawei_image": "الصورة:",
        "huawei_unlock_help": "🔓 مساعدة فتح البوتلودر",
        "huawei_hisuite": "🌐 HiSuite الرسمي",
        "huawei_erecovery_help": "📖 دليل eRecovery",
        "huawei_check_bl": "🔍 فحص حالة البوتلودر",
        "huawei_unlock_code": "🔑 فتح بقفل كود Huawei",
        "huawei_erase_frp": "🚫 مسح FRP",
        "huawei_wipe_data": "🧹 محو البيانات",
        "huawei_reboot_ok": "🔄 إعادة تشغيل عادي",
        # Flash
        "flash_title": "📦 فلاش الروم",
        "flash_select_zip": "📁 اختر ملف الروم",
        "flash_type": "النوع: {}",
        "flash_type_unknown": "غير معروف",
        "flash_type_fastboot_zip": "Fastboot ZIP",
        "flash_type_samsung_tar": "Samsung TAR",
        "flash_type_payload": "Payload.bin",
        "flash_type_tgz": "TGZ",
        "flash_mode": "الوضعية:",
        "flash_mode_normal": "عادي",
        "flash_mode_keep": "الاحتفاظ بالبيانات",
        "flash_mode_wipe": "محو الكل",
        "flash_stop_on_error": "التوقف عند الخطأ",
        "flash_auto_reboot": "إعادة التشغيل",
        "flash_start": "🚀 بدء الفلاش",
        "flash_cancel": "⏹️ إلغاء",
        "flash_scan": "🔍 فحص الروم",
        "flash_progress": "التقدم:",
        "flash_status_idle": "بانتظار البدء",
        "flash_status_extracting": "فك الضغط...",
        "flash_status_extracting_payload": "استخراج payload...",
        "flash_status_flashing": "فلاش: {}",
        "flash_status_done": "✅ اكتمل",
        "flash_status_error": "❌ فشل",
        "flash_status_cancelled": "⏹️ إلغاء",
        # Xiaomi
        "xiaomi_title": "🟠 Xiaomi / Redmi / POCO",
        "xiaomi_warning": "⚠️ HyperOS لها قيود",
        "xiaomi_info": "📱 معلومات",
        "xiaomi_unlock_help": "🔓 مساعدة الفتح",
        "xiaomi_mi_assistant": "🎯 Mi Assistant",
        "xiaomi_select_rom": "اختر ROM (.tgz)",
        "xiaomi_flash_all": "🚀 فلاش كامل",
        "xiaomi_flash_all_no_data": "فلاش (بدون data)",
        "xiaomi_flash_boot": "📦 boot.img",
        "xiaomi_flash_recovery": "📦 recovery.img",
        "xiaomi_flash_vbmeta": "📦 vbmeta.img",
        "xiaomi_partition_name": "القسم:",
        "xiaomi_image_file": "الصورة:",
        "xiaomi_remove_mi_account": "🚫 إزالة Mi Account",
        "xiaomi_remove_mi_account_help": "يتطلب EDL/MTK",
        "xiaomi_clean_and_lock": "🔒 فلاش + قفل",
        "xiaomi_reboot_fastboot": "⚡ Fastboot",
        "xiaomi_reboot_recovery": "♻️ Recovery",
        "xiaomi_reboot_edl": "📡 EDL",
        # Samsung
        "samsung_title": "📱 Samsung — Download",
        "samsung_warning": "⚠️ ضع الجهاز في Download Mode",
        "samsung_detect": "🔍 كشف",
        "samsung_pit": "📋 PIT",
        "samsung_flash_ap": "📦 AP",
        "samsung_flash_bl": "📦 BL",
        "samsung_flash_cp": "📦 CP",
        "samsung_flash_csc": "📦 CSC",
        "samsung_flash_all": "🚀 فلاش الكل",
        "samsung_ap": "AP:",
        "samsung_bl": "BL:",
        "samsung_cp": "CP:",
        "samsung_csc": "CSC:",
        "samsung_no_file": "لم يتم اختيار ملف",
        "samsung_reboot": "إعادة التشغيل",
        "samsung_done": "✅ اكتمل",
        # Root
        "root_title": "🔓 TWRP & Root",
        "root_warning": "⚠️ تأكد من فتح البوتلودر",
        "check_bl_status": "🔍 فحص البوتلودر",
        "unlock_bl": "🔓 فتح",
        "lock_bl": "🔒 قفل",
        "flash_twrp": "📥 TWRP",
        "flash_magisk": "🎯 Magisk",
        "select_recovery": "اختر recovery.img",
        "select_boot": "اختر boot patched",
        "bl_locked": "🔒 مقفل",
        "bl_unlocked": "🔓 مفتوح",
        "bl_unknown": "❓ غير معروف",
        "unlock_confirm": "سيتم محو البيانات!",
        "unlock_warn_screen": "اضغط Volume Up على الشاشة",
        "flash_recovery_success": "✅ recovery",
        "flash_boot_success": "✅ boot",
        "reboot_recovery_after": "إعادة إلى Recovery",
        "download_twrp": "🌐 TWRP",
        "download_magisk": "🌐 Magisk",
        # Unlock
        "unlock_title": "🔒 فك القفل و FRP",
        "check_lock": "🔍 فحص القفل",
        "check_root": "👑 فحص الروت",
        "check_frp": "🚫 فحص FRP",
        "remove_locksettings": "🗑️ locksettings",
        "remove_gatekeeper": "🔑 gatekeeper",
        "remove_pattern": "📐 النمط",
        "format_data_fastboot": "🔐 Format Data",
        "erase_frp_fastboot": "🚫 FRP (FB)",
        "erase_frp_adb": "🚫 FRP (ADB)",
        "full_device_info": "📊 معلومات كاملة",
        "unlock_warning": "⚠️ على مسؤوليتك",
        # MTK
        "mtk_title": "⚙️ mtkclient",
        "run_gui": "🖥️ الواجهة",
        "read_gpt": "📋 GPT",
        "read_part": "قراءة:",
        "read_btn": "قراءة",
        "write_part": "كتابة:",
        "pick": "اختر",
        "write_btn": "كتابة",
        "advanced": "⚠️ متقدم",
        "unlock_bl_mtk": "🔓 فك MTK",
        "wipe_frp": "🧹 FRP + Userdata",
        # EDL
        "edl_title": "⚡ Qualcomm EDL",
        "edl_check": "🔍 فحص",
        "edl_printgpt": "🖨️ الأقسام",
        "edl_dump": "💾 استخراج",
        "edl_load": "📤 كتابة",
        "edl_rw": "🔐 R/W",
        "edl_reset": "🔄 Reset",
        "edl_wipe": "🧹 Userdata",
        "edl_firehose": "🔥 Firehose:",
        "edl_partition": "القسم:",
        # About
        "about_title": "ℹ️ حول",
        "about_version": "الإصدار: {}",
        "about_check_update": "🔄 فحص التحديثات",
        "about_download_update": "📥 تحميل",
        "about_github": "🌐 GitHub",
        "about_up_to_date": "✅ أحدث إصدار",
        "about_new_version": "🎉 جديد: {}",
        "about_checking": "⏳ فحص...",
        "about_error": "❌ {}",
        "about_description": "أداة شاملة لهواتف أندرويد\n\n• ADB / Fastboot\n• فلاش الروم\n• Xiaomi / Huawei / Samsung\n• TWRP & Root\n• فك القفل و FRP\n• MediaTek\n• Qualcomm EDL",
        "log": "📋 السجل:",
        "log_save": "💾 حفظ",
        "log_copy": "📋 نسخ",
        "log_clear": "🗑️ مسح",
        "log_open_folder": "📂 فتح",
        "log_saved": "✅ حفظ: {}",
        "log_copied": "✅ نسخ",
        "log_cleared": "🗑️ مسح",
        "lang_btn": "🌐 English",
        "msg_wait": "⏳ ...",
        "msg_tools_ok": "✅ Platform-Tools",
        "msg_tools_missing": "⚠️ Platform-Tools",
        "msg_python_ok": "✅ Python",
        "msg_python_missing": "⚠️ Python",
        "msg_mtk_ok": "✅ mtkclient",
        "msg_mtk_missing": "⚠️ mtkclient",
        "msg_edl_ok": "✅ edl",
        "msg_edl_missing": "⚠️ edl",
        "msg_heimdall_ok": "✅ Heimdall",
        "msg_heimdall_missing": "⚠️ Heimdall",
        "msg_downloading_pt": "📥 تحميل Platform-Tools...",
        "msg_installed": "✅ تم",
        "msg_error": "❌ {}",
        "msg_adb": "— ADB —",
        "msg_fastboot": "— Fastboot —",
        "msg_no_embed": "❌ Python غير موجود",
        "msg_no_mtk": "❌ mtkclient",
        "msg_no_edl": "❌ edl",
        "confirm_write": "كتابة {} من {}؟",
        "confirm_unlock": "فك القفل؟",
        "confirm_wipe": "مسح!",
        "confirm_format": "محو الكل؟",
        "confirm_flash_samsung": "فلاش {}؟",
        "err_check": "تحقق",
        "err": "خطأ",
        "confirm": "تأكيد",
        "warn": "تحذير",
    },
    "en": {
        "title": "🛠️ Android Tool",
        "tab_adb": "ADB / Fastboot",
        "tab_flash": "📦 Flash ROM",
        "tab_xiaomi": "🟠 Xiaomi",
        "tab_huawei": "🟣 Huawei",
        "tab_samsung": "📱 Samsung",
        "tab_root": "🔓 TWRP & Root",
        "tab_unlock": "🔒 Unlock",
        "tab_mtk": "MTK",
        "tab_edl": "Qualcomm EDL",
        "tab_about": "ℹ️ About",
        "download_tools": "📥 Download Platform-Tools",
        "detect": "🔍 Detect Devices",
        "device_info": "📱 Device Info",
        "reboot": "🔄 Reboot",
        "fastboot": "⚡ Fastboot",
        "reboot_recovery": "♻️ Recovery",
        "reboot_edl": "📡 EDL",
        "exit_fastboot": "🔌 Exit Fastboot",
        "huawei_title": "🟣 Huawei / Honor",
        "huawei_warning": "⚠️ Modern devices protected by Huawei ID",
        "huawei_info": "📱 Device Info",
        "huawei_fastboot": "⚡ Fastboot",
        "huawei_recovery": "♻️ Recovery",
        "huawei_erecovery": "🔄 eRecovery Mode",
        "huawei_flash_boot": "📦 Flash boot.img",
        "huawei_flash_recovery": "📦 Flash recovery.img",
        "huawei_flash_system": "📦 Flash system.img",
        "huawei_flash_ramdisk": "📦 Flash ramdisk.img",
        "huawei_flash_custom": "⚙️ Custom Partition",
        "huawei_partition": "Partition:",
        "huawei_image": "Image:",
        "huawei_unlock_help": "🔓 Unlock Help",
        "huawei_hisuite": "🌐 Official HiSuite",
        "huawei_erecovery_help": "📖 eRecovery Guide",
        "huawei_check_bl": "🔍 Check Bootloader",
        "huawei_unlock_code": "🔑 Unlock with Code",
        "huawei_erase_frp": "🚫 Erase FRP",
        "huawei_wipe_data": "🧹 Wipe Data",
        "huawei_reboot_ok": "🔄 Normal Reboot",
        "flash_title": "📦 Flash ROM",
        "flash_select_zip": "📁 Select ROM",
        "flash_type": "Type: {}",
        "flash_type_unknown": "Unknown",
        "flash_type_fastboot_zip": "Fastboot ZIP",
        "flash_type_samsung_tar": "Samsung TAR",
        "flash_type_payload": "Payload.bin",
        "flash_type_tgz": "TGZ",
        "flash_mode": "Mode:",
        "flash_mode_normal": "Normal",
        "flash_mode_keep": "Keep Data",
        "flash_mode_wipe": "Wipe All",
        "flash_stop_on_error": "Stop on Error",
        "flash_auto_reboot": "Auto Reboot",
        "flash_start": "🚀 Start Flash",
        "flash_cancel": "⏹️ Cancel",
        "flash_scan": "🔍 Scan ROM",
        "flash_progress": "Progress:",
        "flash_status_idle": "Idle",
        "flash_status_extracting": "Extracting...",
        "flash_status_extracting_payload": "Extracting payload...",
        "flash_status_flashing": "Flashing: {}",
        "flash_status_done": "✅ Done",
        "flash_status_error": "❌ Failed",
        "flash_status_cancelled": "⏹️ Cancelled",
        "xiaomi_title": "🟠 Xiaomi / Redmi / POCO",
        "xiaomi_warning": "⚠️ HyperOS has restrictions",
        "xiaomi_info": "📱 Info",
        "xiaomi_unlock_help": "🔓 Unlock Help",
        "xiaomi_mi_assistant": "🎯 Mi Assistant",
        "xiaomi_select_rom": "Select ROM (.tgz)",
        "xiaomi_flash_all": "🚀 Flash All",
        "xiaomi_flash_all_no_data": "Flash (No Data)",
        "xiaomi_flash_boot": "📦 boot.img",
        "xiaomi_flash_recovery": "📦 recovery.img",
        "xiaomi_flash_vbmeta": "📦 vbmeta.img",
        "xiaomi_partition_name": "Partition:",
        "xiaomi_image_file": "Image:",
        "xiaomi_remove_mi_account": "🚫 Remove Mi Account",
        "xiaomi_remove_mi_account_help": "Requires EDL/MTK",
        "xiaomi_clean_and_lock": "🔒 Flash + Lock",
        "xiaomi_reboot_fastboot": "⚡ Fastboot",
        "xiaomi_reboot_recovery": "♻️ Recovery",
        "xiaomi_reboot_edl": "📡 EDL",
        "samsung_title": "📱 Samsung — Download",
        "samsung_warning": "⚠️ Device must be in Download Mode",
        "samsung_detect": "🔍 Detect",
        "samsung_pit": "📋 PIT",
        "samsung_flash_ap": "📦 AP",
        "samsung_flash_bl": "📦 BL",
        "samsung_flash_cp": "📦 CP",
        "samsung_flash_csc": "📦 CSC",
        "samsung_flash_all": "🚀 Flash All",
        "samsung_ap": "AP:",
        "samsung_bl": "BL:",
        "samsung_cp": "CP:",
        "samsung_csc": "CSC:",
        "samsung_no_file": "No file",
        "samsung_reboot": "Reboot",
        "samsung_done": "✅ Done",
        "root_title": "🔓 TWRP & Root",
        "root_warning": "⚠️ Make sure bootloader unlocked",
        "check_bl_status": "🔍 Check BL",
        "unlock_bl": "🔓 Unlock",
        "lock_bl": "🔒 Lock",
        "flash_twrp": "📥 TWRP",
        "flash_magisk": "🎯 Magisk",
        "select_recovery": "Select recovery.img",
        "select_boot": "Select boot",
        "bl_locked": "🔒 Locked",
        "bl_unlocked": "🔓 Unlocked",
        "bl_unknown": "❓ Unknown",
        "unlock_confirm": "Wipe data!",
        "unlock_warn_screen": "Press Volume Up on screen",
        "flash_recovery_success": "✅ recovery",
        "flash_boot_success": "✅ boot",
        "reboot_recovery_after": "Reboot to Recovery",
        "download_twrp": "🌐 TWRP",
        "download_magisk": "🌐 Magisk",
        "unlock_title": "🔒 Unlock & FRP",
        "check_lock": "🔍 Check Lock",
        "check_root": "👑 Check Root",
        "check_frp": "🚫 Check FRP",
        "remove_locksettings": "🗑️ locksettings",
        "remove_gatekeeper": "🔑 gatekeeper",
        "remove_pattern": "📐 Pattern",
        "format_data_fastboot": "🔐 Format Data",
        "erase_frp_fastboot": "🚫 FRP (FB)",
        "erase_frp_adb": "🚫 FRP (ADB)",
        "full_device_info": "📊 Full Info",
        "unlock_warning": "⚠️ At your own risk",
        "mtk_title": "⚙️ mtkclient",
        "run_gui": "🖥️ GUI",
        "read_gpt": "📋 GPT",
        "read_part": "Read:",
        "read_btn": "Read",
        "write_part": "Write:",
        "pick": "Pick",
        "write_btn": "Write",
        "advanced": "⚠️ Advanced",
        "unlock_bl_mtk": "🔓 MTK Unlock",
        "wipe_frp": "🧹 FRP + Userdata",
        "edl_title": "⚡ Qualcomm EDL",
        "edl_check": "🔍 Check",
        "edl_printgpt": "🖨️ Partitions",
        "edl_dump": "💾 Dump",
        "edl_load": "📤 Write",
        "edl_rw": "🔐 R/W",
        "edl_reset": "🔄 Reset",
        "edl_wipe": "🧹 Userdata",
        "edl_firehose": "🔥 Firehose:",
        "edl_partition": "Partition:",
        "about_title": "ℹ️ About",
        "about_version": "Version: {}",
        "about_check_update": "🔄 Check Updates",
        "about_download_update": "📥 Download",
        "about_github": "🌐 GitHub",
        "about_up_to_date": "✅ Up to date",
        "about_new_version": "🎉 New: {}",
        "about_checking": "⏳ Checking...",
        "about_error": "❌ {}",
        "about_description": "All-in-one Android tool\n\n• ADB / Fastboot\n• Full ROM Flash\n• Xiaomi / Huawei / Samsung\n• TWRP & Root\n• Unlock & FRP\n• MediaTek\n• Qualcomm EDL",
        "log": "📋 Log:",
        "log_save": "💾 Save",
        "log_copy": "📋 Copy",
        "log_clear": "🗑️ Clear",
        "log_open_folder": "📂 Open",
        "log_saved": "✅ Saved: {}",
        "log_copied": "✅ Copied",
        "log_cleared": "🗑️ Cleared",
        "lang_btn": "🌐 العربية",
        "msg_wait": "⏳ ...",
        "msg_tools_ok": "✅ Platform-Tools",
        "msg_tools_missing": "⚠️ Platform-Tools",
        "msg_python_ok": "✅ Python",
        "msg_python_missing": "⚠️ Python",
        "msg_mtk_ok": "✅ mtkclient",
        "msg_mtk_missing": "⚠️ mtkclient",
        "msg_edl_ok": "✅ edl",
        "msg_edl_missing": "⚠️ edl",
        "msg_heimdall_ok": "✅ Heimdall",
        "msg_heimdall_missing": "⚠️ Heimdall",
        "msg_downloading_pt": "📥 Downloading Platform-Tools...",
        "msg_installed": "✅ Done",
        "msg_error": "❌ {}",
        "msg_adb": "— ADB —",
        "msg_fastboot": "— Fastboot —",
        "msg_no_embed": "❌ Python missing",
        "msg_no_mtk": "❌ mtkclient",
        "msg_no_edl": "❌ edl",
        "confirm_write": "Write {} from {}?",
        "confirm_unlock": "Unlock?",
        "confirm_wipe": "Wipe!",
        "confirm_format": "Format all?",
        "confirm_flash_samsung": "Flash {}?",
        "err_check": "Check",
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


def detect_rom_type(path):
    if not path or not os.path.exists(path):
        return "unknown"
    name = os.path.basename(path).lower()
    ext = os.path.splitext(name)[1]
    if ext == ".zip":
        try:
            with zipfile.ZipFile(path) as z:
                names = z.namelist()
                if any(n.endswith("payload.bin") for n in names):
                    return "payload"
                if any(n.endswith(".img") for n in names):
                    return "fastboot_zip"
        except Exception:
            pass
        return "fastboot_zip"
    if ext in [".tar", ".md5"] or name.endswith(".tar.md5"):
        return "samsung_tar"
    if ext in [".tgz", ".tar.gz"]:
        return "tgz"
    return "unknown"


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.lang = "ar"
        self.t = LANG[self.lang]

        self.flash_file = ""
        self.flash_rom_type = "unknown"
        self.flash_cancel = False

        self.samsung_ap = ""
        self.samsung_bl = ""
        self.samsung_cp = ""
        self.samsung_csc = ""

        self.recovery_img = ""
        self.boot_img = ""
        self.xiaomi_rom = ""

        self.geometry("1020x920")
        self.resizable(True, True)

        os.makedirs(LOGS_DIR, exist_ok=True)

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

    def build_ui(self):
        for w in self.winfo_children():
            w.destroy()

        self.title(f"{self.tr('title')} v{APP_VERSION}")

        top = ctk.CTkFrame(self)
        top.pack(fill="x", padx=15, pady=(10, 0))

        ctk.CTkLabel(top, text=self.tr("title"),
                     font=("Arial", 22, "bold")).pack(side="left", padx=5)

        ctk.CTkButton(top, text=self.tr("lang_btn"), width=110, height=32,
                      command=self.toggle_lang).pack(side="right", padx=5)

        self.tabs = ctk.CTkTabview(self, width=970, height=680)
        self.tabs.pack(padx=15, pady=5, fill="both", expand=True)

        self.tab_adb = self.tabs.add(self.tr("tab_adb"))
        self.tab_flash = self.tabs.add(self.tr("tab_flash"))
        self.tab_xiaomi = self.tabs.add(self.tr("tab_xiaomi"))
        self.tab_huawei = self.tabs.add(self.tr("tab_huawei"))
        self.tab_samsung = self.tabs.add(self.tr("tab_samsung"))
        self.tab_root = self.tabs.add(self.tr("tab_root"))
        self.tab_unlock = self.tabs.add(self.tr("tab_unlock"))
        self.tab_mtk = self.tabs.add(self.tr("tab_mtk"))
        self.tab_edl = self.tabs.add(self.tr("tab_edl"))
        self.tab_about = self.tabs.add(self.tr("tab_about"))

        self.build_adb_tab()
        self.build_flash_tab()
        self.build_xiaomi_tab()
        self.build_huawei_tab()
        self.build_samsung_tab()
        self.build_root_tab()
        self.build_unlock_tab()
        self.build_mtk_tab()
        self.build_edl_tab()
        self.build_about_tab()

        log_header = ctk.CTkFrame(self)
        log_header.pack(fill="x", padx=15)

        ctk.CTkLabel(log_header, text=self.tr("log"),
                     font=("Arial", 13, "bold")).pack(side="left", padx=5)

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
        self.log_box.insert("end", ts + str(t) + "\n")
        self.log_box.see("end")
        self.update_idletasks()

    def save_log(self):
        try:
            content = self.log_box.get("1.0", "end")
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            path = os.path.join(LOGS_DIR, f"log_{ts}.txt")
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            self.log(self.tr("log_saved", path))
        except Exception as e:
            self.log(self.tr("msg_error", e))

    def copy_log(self):
        self.clipboard_clear()
        self.clipboard_append(self.log_box.get("1.0", "end"))
        self.log(self.tr("log_copied"))

    def clear_log(self):
        self.log_box.delete("1.0", "end")
        self.log(self.tr("log_cleared"))

    def open_logs_folder(self):
        try:
            if os.name == "nt":
                os.startfile(LOGS_DIR)
            else:
                subprocess.Popen(["xdg-open", LOGS_DIR])
        except Exception as e:
            self.log(self.tr("msg_error", e))

    def _bg_check_update(self):
        try:
            req = urllib.request.Request(GITHUB_API,
                                          headers={"User-Agent": "AndroidTool"})
            with urllib.request.urlopen(req, timeout=10) as r:
                data = json.loads(r.read().decode("utf-8"))
            latest = data.get("tag_name", "").lstrip("v")
            if latest and latest != APP_VERSION:
                self.after(0, lambda: self._update_available(latest))
        except Exception:
            pass

    def _update_available(self, latest):
        try:
            self.about_status.configure(
                text=self.tr("about_new_version", latest),
                text_color="lightgreen")
            self._update_url = f"https://github.com/{GITHUB_REPO}/releases/latest"
            self.download_btn.configure(state="normal")
        except Exception:
            pass

    def check_update(self):
        self.about_status.configure(text=self.tr("about_checking"), text_color="gray")
        def t():
            try:
                req = urllib.request.Request(GITHUB_API,
                                              headers={"User-Agent": "AndroidTool"})
                with urllib.request.urlopen(req, timeout=10) as r:
                    data = json.loads(r.read().decode("utf-8"))
                latest = data.get("tag_name", "").lstrip("v")
                if latest and latest != APP_VERSION:
                    self.about_status.configure(
                        text=self.tr("about_new_version", latest),
                        text_color="lightgreen")
                    self._update_url = f"https://github.com/{GITHUB_REPO}/releases/latest"
                    self.download_btn.configure(state="normal")
                else:
                    self.about_status.configure(
                        text=self.tr("about_up_to_date"),
                        text_color="lightgreen")
            except Exception as e:
                self.about_status.configure(
                    text=self.tr("about_error", str(e)),
                    text_color="red")
        threading.Thread(target=t, daemon=True).start()

    def open_update_page(self):
        url = getattr(self, "_update_url",
                      f"https://github.com/{GITHUB_REPO}/releases/latest")
        webbrowser.open(url)

    def open_github(self):
        webbrowser.open(f"https://github.com/{GITHUB_REPO}")

    def build_about_tab(self):
        f = self.tab_about
        ctk.CTkLabel(f, text=self.tr("about_title"),
                     font=("Arial", 18, "bold")).pack(pady=15)
        ctk.CTkLabel(f, text=self.tr("about_version", APP_VERSION),
                     font=("Arial", 14)).pack(pady=6)
        ctk.CTkLabel(f, text=self.tr("about_description"),
                     font=("Arial", 12), justify="center").pack(pady=15)
        self.about_status = ctk.CTkLabel(f, text="", font=("Arial", 12))
        self.about_status.pack(pady=5)
        bf = ctk.CTkFrame(f)
        bf.pack(pady=15)
        ctk.CTkButton(bf, text=self.tr("about_check_update"), width=200, height=40,
                      command=self.check_update).pack(side="left", padx=5)
        self.download_btn = ctk.CTkButton(bf, text=self.tr("about_download_update"),
                                           width=200, height=40,
                                           fg_color="green", hover_color="darkgreen",
                                           state="disabled",
                                           command=self.open_update_page)
        self.download_btn.pack(side="left", padx=5)
        ctk.CTkButton(f, text=self.tr("about_github"), width=300, height=40,
                      command=self.open_github).pack(pady=10)

    # ============ ADB ============
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

    # ============ Huawei ============
    def build_huawei_tab(self):
        f = self.tab_huawei
        ctk.CTkLabel(f, text=self.tr("huawei_title"),
                     font=("Arial", 16, "bold")).pack(pady=6)
        ctk.CTkLabel(f, text=self.tr("huawei_warning"),
                     font=("Arial", 11), text_color="orange").pack(pady=4)

        # معلومات + إعادة تشغيل
        row = ctk.CTkFrame(f)
        row.pack(pady=6)
        ctk.CTkButton(row, text=self.tr("huawei_info"), width=180,
                      command=self.huawei_info).pack(side="left", padx=4)
        ctk.CTkButton(row, text=self.tr("huawei_check_bl"), width=180,
                      command=self.huawei_check_bl).pack(side="left", padx=4)
        ctk.CTkButton(row, text=self.tr("huawei_erecovery"), width=180,
                      fg_color="orange", hover_color="darkorange",
                      command=self.huawei_erecovery).pack(side="left", padx=4)

        # أدوات
        ctk.CTkLabel(f, text="— Tools —",
                     font=("Arial", 12, "bold"), text_color="lightblue").pack(pady=(15, 3))
        tf = ctk.CTkFrame(f)
        tf.pack(pady=4)
        ctk.CTkButton(tf, text=self.tr("huawei_unlock_help"), width=200,
                      fg_color="gray",
                      command=lambda: webbrowser.open(
                          "https://emui.huawei.com/en/unlock_index")).pack(side="left", padx=4)
        ctk.CTkButton(tf, text=self.tr("huawei_hisuite"), width=200,
                      fg_color="gray",
                      command=lambda: webbrowser.open(
                          "https://consumer.huawei.com/en/support/hisuite/")).pack(side="left", padx=4)
        ctk.CTkButton(tf, text=self.tr("huawei_erecovery_help"), width=200,
                      fg_color="gray",
                      command=lambda: webbrowser.open(
                          "https://consumer.huawei.com/en/support/")).pack(side="left", padx=4)

        # فلاش أقسام
        ctk.CTkLabel(f, text="— Flash Partitions —",
                     font=("Arial", 12, "bold"), text_color="lightblue").pack(pady=(15, 3))
        pf = ctk.CTkFrame(f)
        pf.pack(pady=4)
        ctk.CTkButton(pf, text=self.tr("huawei_flash_boot"), width=180,
                      command=lambda: self.huawei_flash_single("boot")).pack(side="left", padx=3)
        ctk.CTkButton(pf, text=self.tr("huawei_flash_recovery"), width=180,
                      command=lambda: self.huawei_flash_single("recovery")).pack(side="left", padx=3)
        ctk.CTkButton(pf, text=self.tr("huawei_flash_system"), width=180,
                      command=lambda: self.huawei_flash_single("system")).pack(side="left", padx=3)
        ctk.CTkButton(pf, text=self.tr("huawei_flash_ramdisk"), width=180,
                      command=lambda: self.huawei_flash_single("ramdisk")).pack(side="left", padx=3)

        # قسم مخصص
        cf = ctk.CTkFrame(f)
        cf.pack(pady=6)
        ctk.CTkLabel(cf, text=self.tr("huawei_partition")).pack(side="left", padx=4)
        self.huawei_part_name = ctk.CTkEntry(cf, width=140)
        self.huawei_part_name.pack(side="left", padx=4)
        self.huawei_part_name.insert(0, "boot")
        ctk.CTkLabel(cf, text=self.tr("huawei_image")).pack(side="left", padx=4)
        self.huawei_img_file = ctk.CTkEntry(cf, width=220)
        self.huawei_img_file.pack(side="left", padx=4)
        ctk.CTkButton(cf, text=self.tr("pick"), width=60,
                      command=self.huawei_pick_img).pack(side="left", padx=4)
        ctk.CTkButton(cf, text=self.tr("write_btn"), width=90, fg_color="red",
                      hover_color="darkred",
                      command=self.huawei_flash_custom).pack(side="left", padx=4)

        # عمليات متقدمة
        ctk.CTkLabel(f, text=self.tr("advanced"), font=("Arial", 12, "bold"),
                     text_color="orange").pack(pady=(15, 3))
        af = ctk.CTkFrame(f)
        af.pack(pady=4)
        ctk.CTkButton(af, text=self.tr("huawei_unlock_code"), width=200,
                      fg_color="orange", hover_color="darkorange",
                      command=self.huawei_unlock_code).pack(side="left", padx=3)
        ctk.CTkButton(af, text=self.tr("huawei_erase_frp"), width=200,
                      fg_color="red", hover_color="darkred",
                      command=self.huawei_erase_frp).pack(side="left", padx=3)
        ctk.CTkButton(af, text=self.tr("huawei_wipe_data"), width=200,
                      fg_color="red", hover_color="darkred",
                      command=self.huawei_wipe_data).pack(side="left", padx=3)

        # إعادة تشغيل
        ctk.CTkLabel(f, text="— Reboot —",
                     font=("Arial", 12, "bold"), text_color="lightblue").pack(pady=(15, 3))
        rbf = ctk.CTkFrame(f)
        rbf.pack(pady=4)
        ctk.CTkButton(rbf, text=self.tr("huawei_fastboot"), width=180,
                      command=lambda: self.async_run(lambda: run([ADB, "reboot", "bootloader"]))).pack(side="left", padx=3)
        ctk.CTkButton(rbf, text=self.tr("huawei_recovery"), width=180,
                      command=lambda: self.async_run(lambda: run([ADB, "reboot", "recovery"]))).pack(side="left", padx=3)
        ctk.CTkButton(rbf, text=self.tr("huawei_reboot_ok"), width=180,
                      command=lambda: self.async_run(lambda: run([ADB, "reboot"]))).pack(side="left", padx=3)

    def huawei_info(self):
        def t():
            self.log("=" * 50)
            props = [
                "ro.product.model", "ro.product.brand",
                "ro.build.version.release", "ro.build.version.emui",
                "ro.build.display.id", "ro.serialno",
                "ro.product.cpu.abi", "ro.build.version.sdk",
                "ro.boot.hardware", "ro.board.platform",
            ]
            for p in props:
                self.log(f"{p}: {run([ADB, 'shell', 'getprop', p]).strip()}")
        threading.Thread(target=t, daemon=True).start()

    def huawei_check_bl(self):
        def t():
            self.log("=" * 50)
            out1 = run([ADB, "shell", "getprop", "ro.boot.verifiedbootstate"])
            out2 = run([ADB, "shell", "getprop", "ro.boot.flash.locked"])
            out3 = run([FASTBOOT, "oem", "device-info"])
            self.log(f"verifiedbootstate: {out1.strip()}")
            self.log(f"flash.locked: {out2.strip()}")
            self.log(f"device-info:\n{out3}")
        threading.Thread(target=t, daemon=True).start()

    def huawei_erecovery(self):
        def t():
            self.log("🔄 Rebooting to eRecovery...")
            out = run([ADB, "reboot", "erecovery"], timeout=20)
            self.log(out)
            if not out.strip():
                self.log("✅ Done (or use Volume Up + Power manually)")
        threading.Thread(target=t, daemon=True).start()

    def huawei_flash_single(self, partition):
        p = filedialog.askopenfilename(
            filetypes=[("Image", "*.img"), ("All", "*.*")])
        if not p:
            return
        if not messagebox.askyesno(self.tr("confirm"),
                                    self.tr("confirm_flash_samsung", partition)):
            return
        def t():
            self.log(f"🚀 flash {partition}: {os.path.basename(p)}")
            out = run([FASTBOOT, "flash", partition, p], timeout=900)
            self.log(out[-1000:])
        threading.Thread(target=t, daemon=True).start()

    def huawei_pick_img(self):
        p = filedialog.askopenfilename(filetypes=[("Image", "*.img")])
        if p:
            self.huawei_img_file.delete(0, "end")
            self.huawei_img_file.insert(0, p)

    def huawei_flash_custom(self):
        part = self.huawei_part_name.get().strip()
        f = self.huawei_img_file.get().strip()
        if not part or not os.path.exists(f):
            messagebox.showerror(self.tr("err"), self.tr("err_check"))
            return
        def t():
            out = run([FASTBOOT, "flash", part, f], timeout=900)
            self.log(out[-1000:])
        threading.Thread(target=t, daemon=True).start()

    def huawei_unlock_code(self):
        code = ctk.CTkInputDialog(
            text="Enter Huawei Unlock Code:",
            title="Unlock Code").get_input()
        if not code:
            return
        def t():
            self.log(f"🔑 Unlocking with code: {code[:4]}****")
            out = run([FASTBOOT, "oem", "unlock", code], timeout=120)
            self.log(out)
        threading.Thread(target=t, daemon=True).start()

    def huawei_erase_frp(self):
        if not messagebox.askyesno(self.tr("warn"), self.tr("confirm_wipe")):
            return
        self.async_run(lambda: run([FASTBOOT, "erase", "frp"], timeout=120))

    def huawei_wipe_data(self):
        if not messagebox.askyesno(self.tr("warn"), self.tr("confirm_format")):
            return
        self.async_run(lambda: run([FASTBOOT, "erase", "userdata"], timeout=300))

    # ============ Xiaomi ============
    def build_xiaomi_tab(self):
        f = self.tab_xiaomi
        ctk.CTkLabel(f, text=self.tr("xiaomi_title"),
                     font=("Arial", 16, "bold")).pack(pady=6)
        ctk.CTkLabel(f, text=self.tr("xiaomi_warning"),
                     font=("Arial", 11), text_color="orange").pack(pady=4)

        row = ctk.CTkFrame(f)
        row.pack(pady=6)
        ctk.CTkButton(row, text=self.tr("xiaomi_info"), width=180,
                      command=self.xiaomi_info).pack(side="left", padx=4)
        ctk.CTkButton(row, text=self.tr("xiaomi_unlock_help"), width=180,
                      fg_color="gray",
                      command=lambda: webbrowser.open(
                          "https://en.miui.com/unlock/")).pack(side="left", padx=4)
        ctk.CTkButton(row, text=self.tr("xiaomi_mi_assistant"), width=180,
                      fg_color="gray",
                      command=self.xiaomi_mi_assistant).pack(side="left", padx=4)

        ctk.CTkLabel(f, text="— Fastboot ROM —",
                     font=("Arial", 12, "bold"), text_color="lightblue").pack(pady=(15, 3))

        rf = ctk.CTkFrame(f)
        rf.pack(pady=4)
        ctk.CTkButton(rf, text=self.tr("xiaomi_select_rom"), width=250,
                      command=self.xiaomi_select_rom).pack(side="left", padx=5)
        self.xiaomi_rom_label = ctk.CTkLabel(rf, text=self.tr("samsung_no_file"),
                                              font=("Arial", 10), text_color="gray")
        self.xiaomi_rom_label.pack(side="left", padx=5)

        fl = ctk.CTkFrame(f)
        fl.pack(pady=6)
        ctk.CTkButton(fl, text=self.tr("xiaomi_flash_all"), width=200, height=42,
                      fg_color="green", hover_color="darkgreen",
                      command=lambda: self.xiaomi_flash_rom(wipe=False)).pack(side="left", padx=4)
        ctk.CTkButton(fl, text=self.tr("xiaomi_flash_all_no_data"), width=200, height=42,
                      fg_color="orange", hover_color="darkorange",
                      command=lambda: self.xiaomi_flash_rom(wipe=True)).pack(side="left", padx=4)

        ctk.CTkLabel(f, text="— Partitions —",
                     font=("Arial", 12, "bold"), text_color="lightblue").pack(pady=(15, 3))
        pf = ctk.CTkFrame(f)
        pf.pack(pady=4)
        ctk.CTkButton(pf, text=self.tr("xiaomi_flash_boot"), width=180,
                      command=lambda: self.xiaomi_flash_single("boot")).pack(side="left", padx=3)
        ctk.CTkButton(pf, text=self.tr("xiaomi_flash_recovery"), width=180,
                      command=lambda: self.xiaomi_flash_single("recovery")).pack(side="left", padx=3)
        ctk.CTkButton(pf, text=self.tr("xiaomi_flash_vbmeta"), width=180,
                      command=lambda: self.xiaomi_flash_single("vbmeta")).pack(side="left", padx=3)

        cf = ctk.CTkFrame(f)
        cf.pack(pady=6)
        ctk.CTkLabel(cf, text=self.tr("xiaomi_partition_name")).pack(side="left", padx=4)
        self.xiaomi_part_name = ctk.CTkEntry(cf, width=140)
        self.xiaomi_part_name.pack(side="left", padx=4)
        self.xiaomi_part_name.insert(0, "boot")
        ctk.CTkLabel(cf, text=self.tr("xiaomi_image_file")).pack(side="left", padx=4)
        self.xiaomi_img_file = ctk.CTkEntry(cf, width=220)
        self.xiaomi_img_file.pack(side="left", padx=4)
        ctk.CTkButton(cf, text=self.tr("pick"), width=60,
                      command=self.xiaomi_pick_img).pack(side="left", padx=4)
        ctk.CTkButton(cf, text=self.tr("write_btn"), width=90, fg_color="red",
                      hover_color="darkred",
                      command=self.xiaomi_flash_custom).pack(side="left", padx=4)

        ctk.CTkLabel(f, text=self.tr("advanced"), font=("Arial", 12, "bold"),
                     text_color="orange").pack(pady=(15, 3))
        af = ctk.CTkFrame(f)
        af.pack(pady=4)
        ctk.CTkButton(af, text=self.tr("xiaomi_remove_mi_account"), width=220,
                      fg_color="red", hover_color="darkred",
                      command=self.xiaomi_remove_account).pack(side="left", padx=3)
        ctk.CTkButton(af, text=self.tr("xiaomi_clean_and_lock"), width=220,
                      fg_color="red", hover_color="darkred",
                      command=self.xiaomi_clean_lock).pack(side="left", padx=3)

        ctk.CTkLabel(f, text="— Reboot —",
                     font=("Arial", 12, "bold"), text_color="lightblue").pack(pady=(15, 3))
        rbf = ctk.CTkFrame(f)
        rbf.pack(pady=4)
        ctk.CTkButton(rbf, text=self.tr("xiaomi_reboot_fastboot"), width=180,
                      command=lambda: self.async_run(lambda: run([ADB, "reboot", "bootloader"]))).pack(side="left", padx=3)
        ctk.CTkButton(rbf, text=self.tr("xiaomi_reboot_recovery"), width=180,
                      command=lambda: self.async_run(lambda: run([ADB, "reboot", "recovery"]))).pack(side="left", padx=3)
        ctk.CTkButton(rbf, text=self.tr("xiaomi_reboot_edl"), width=180,
                      command=lambda: self.async_run(lambda: run([ADB, "reboot", "edl"]))).pack(side="left", padx=3)

    def xiaomi_info(self):
        def t():
            self.log("=" * 50)
            props = [
                "ro.product.model", "ro.product.brand",
                "ro.miui.ui.version.name", "ro.mi.os.version.incremental",
                "ro.build.version.release", "ro.boot.hwc",
                "ro.boot.hwlevel", "ro.secureboot.lockstate",
                "ro.boot.verifiedbootstate", "ro.serialno",
                "ro.product.cpu.abi",
            ]
            for p in props:
                self.log(f"{p}: {run([ADB, 'shell', 'getprop', p]).strip()}")
        threading.Thread(target=t, daemon=True).start()

    def xiaomi_mi_assistant(self):
        def t():
            self.log("=" * 50)
            self.log("🎯 Mi Assistant Mode:")
            self.log(run([ADB, "shell", "getprop", "ro.boot.mode"]))
            self.log(run([ADB, "shell", "getprop", "ro.boot.midevicemode"]))
        threading.Thread(target=t, daemon=True).start()

    def xiaomi_select_rom(self):
        p = filedialog.askopenfilename(
            filetypes=[("Xiaomi ROM", "*.tgz *.tar.gz *.zip"), ("All", "*.*")])
        if p:
            self.xiaomi_rom = p
            self.xiaomi_rom_label.configure(text=os.path.basename(p),
                                             text_color="lightgreen")
            self.log(f"🟠 Xiaomi ROM: {os.path.basename(p)}")

    def xiaomi_flash_rom(self, wipe=False):
        if not self.xiaomi_rom or not os.path.exists(self.xiaomi_rom):
            messagebox.showerror(self.tr("err"), self.tr("samsung_no_file"))
            return
        if not messagebox.askyesno(self.tr("confirm"),
                                    self.tr("confirm_flash_samsung",
                                            os.path.basename(self.xiaomi_rom))):
            return

        def t():
            try:
                if os.path.exists(TEMP_FLASH):
                    shutil.rmtree(TEMP_FLASH, ignore_errors=True)
                os.makedirs(TEMP_FLASH, exist_ok=True)
                name = os.path.basename(self.xiaomi_rom).lower()
                self.log("📦 Extracting Xiaomi ROM...")
                if name.endswith(".zip"):
                    with zipfile.ZipFile(self.xiaomi_rom) as z:
                        z.extractall(TEMP_FLASH)
                elif name.endswith((".tgz", ".tar.gz")):
                    with tarfile.open(self.xiaomi_rom, "r:gz") as tar:
                        tar.extractall(TEMP_FLASH)

                images_dir = None
                for root, dirs, files in os.walk(TEMP_FLASH):
                    if "images" in os.path.basename(root).lower():
                        images_dir = root
                        break
                if not images_dir:
                    for root, dirs, files in os.walk(TEMP_FLASH):
                        for f in files:
                            if f.endswith(".img"):
                                images_dir = root
                                break
                        if images_dir:
                            break
                if not images_dir:
                    self.log("❌ No images found")
                    return

                order = ["gpt", "tz", "xbl", "abl", "aop", "bluetooth",
                          "keymaster", "devcfg", "dsp", "featenabler",
                          "hyp", "imagefv", "qupfw", "shrm", "uefisecapp",
                          "vbmeta_system", "vbmeta_vendor", "vbmeta", "modem",
                          "boot", "dtbo", "recovery", "super",
                          "cust", "countrycode", "frp", "persist",
                          "metadata", "userdata"]
                images = {}
                for f in os.listdir(images_dir):
                    if f.endswith(".img"):
                        name_only = os.path.splitext(f)[0]
                        images[name_only] = os.path.join(images_dir, f)

                for part in order:
                    if part not in images:
                        continue
                    if wipe and part == "userdata":
                        continue
                    self.log(f"🚀 flash {part}")
                    out = run([FASTBOOT, "flash", part, images[part]], timeout=1800)
                    self.log(out[-300:])
                for part, path in images.items():
                    if part in order:
                        continue
                    if wipe and part == "userdata":
                        continue
                    self.log(f"🚀 flash {part} (extra)")
                    out = run([FASTBOOT, "flash", part, path], timeout=1800)
                    self.log(out[-300:])
                self.log("🎉 Xiaomi ROM flashed!")
                run([FASTBOOT, "reboot"])
            except Exception as e:
                self.log(f"❌ {e}")
        threading.Thread(target=t, daemon=True).start()

    def xiaomi_flash_single(self, partition):
        p = filedialog.askopenfilename(
            filetypes=[("Image", "*.img"), ("All", "*.*")])
        if not p:
            return
        def t():
            self.log(f"🚀 flash {partition}: {os.path.basename(p)}")
            out = run([FASTBOOT, "flash", partition, p], timeout=600)
            self.log(out[-500:])
        threading.Thread(target=t, daemon=True).start()

    def xiaomi_pick_img(self):
        p = filedialog.askopenfilename(filetypes=[("Image", "*.img")])
        if p:
            self.xiaomi_img_file.delete(0, "end")
            self.xiaomi_img_file.insert(0, p)

    def xiaomi_flash_custom(self):
        part = self.xiaomi_part_name.get().strip()
        f = self.xiaomi_img_file.get().strip()
        if not part or not os.path.exists(f):
            messagebox.showerror(self.tr("err"), self.tr("err_check"))
            return
        def t():
            out = run([FASTBOOT, "flash", part, f], timeout=600)
            self.log(out[-500:])
        threading.Thread(target=t, daemon=True).start()

    def xiaomi_remove_account(self):
        messagebox.showinfo("Info", self.tr("xiaomi_remove_mi_account_help"))
        def t():
            self.log("=" * 50)
            self.log("⚠️ Mi Account removal requires MTK/EDL")
            self.log(run([ADB, "shell", "pm", "list", "packages"]))
        threading.Thread(target=t, daemon=True).start()

    def xiaomi_clean_lock(self):
        if not messagebox.askyesno(self.tr("warn"),
                                    "⚠️ Flash ROM + Lock bootloader?"):
            return
        def t():
            self.log("🔒 Locking bootloader...")
            run([FASTBOOT, "flashing", "lock"], timeout=120)
            self.log("Rebooting...")
            run([FASTBOOT, "reboot"])
        threading.Thread(target=t, daemon=True).start()

    # ============ Root ============
    def build_root_tab(self):
        f = self.tab_root
        ctk.CTkLabel(f, text=self.tr("root_title"),
                     font=("Arial", 16, "bold")).pack(pady=6)
        ctk.CTkLabel(f, text=self.tr("root_warning"),
                     font=("Arial", 11), text_color="orange").pack(pady=4)
        blf = ctk.CTkFrame(f)
        blf.pack(pady=6)
        ctk.CTkButton(blf, text=self.tr("check_bl_status"), width=200,
                      command=self.check_bl_status).pack(side="left", padx=5)
        self.bl_status_label = ctk.CTkLabel(blf, text=self.tr("bl_unknown"),
                                             font=("Arial", 12, "bold"))
        self.bl_status_label.pack(side="left", padx=10)
        blb = ctk.CTkFrame(f)
        blb.pack(pady=4)
        ctk.CTkButton(blb, text=self.tr("unlock_bl"), width=220,
                      fg_color="orange", hover_color="darkorange",
                      command=self.unlock_bootloader).pack(side="left", padx=5)
        ctk.CTkButton(blb, text=self.tr("lock_bl"), width=220,
                      fg_color="red", hover_color="darkred",
                      command=self.lock_bootloader).pack(side="left", padx=5)
        ctk.CTkLabel(f, text="— TWRP —",
                     font=("Arial", 12, "bold"), text_color="lightblue").pack(pady=(15, 3))
        tw = ctk.CTkFrame(f)
        tw.pack(pady=4)
        ctk.CTkButton(tw, text=self.tr("select_recovery"), width=280,
                      command=self.pick_recovery).pack(side="left", padx=5)
        self.recovery_label = ctk.CTkLabel(tw, text=self.tr("samsung_no_file"),
                                            font=("Arial", 10), text_color="gray")
        self.recovery_label.pack(side="left", padx=5)
        ctk.CTkButton(f, text=self.tr("flash_twrp"), width=350, height=45,
                      fg_color="green", hover_color="darkgreen",
                      font=("Arial", 14, "bold"),
                      command=self.flash_recovery).pack(pady=6)
        ctk.CTkLabel(f, text="— Magisk —",
                     font=("Arial", 12, "bold"), text_color="lightblue").pack(pady=(15, 3))
        mg = ctk.CTkFrame(f)
        mg.pack(pady=4)
        ctk.CTkButton(mg, text=self.tr("select_boot"), width=280,
                      command=self.pick_boot).pack(side="left", padx=5)
        self.boot_label = ctk.CTkLabel(mg, text=self.tr("samsung_no_file"),
                                        font=("Arial", 10), text_color="gray")
        self.boot_label.pack(side="left", padx=5)
        ctk.CTkButton(f, text=self.tr("flash_magisk"), width=350, height=45,
                      fg_color="green", hover_color="darkgreen",
                      font=("Arial", 14, "bold"),
                      command=self.flash_boot).pack(pady=6)
        opt = ctk.CTkFrame(f)
        opt.pack(pady=10)
        self.reboot_after_root = ctk.CTkCheckBox(opt, text=self.tr("reboot_recovery_after"))
        self.reboot_after_root.grid(row=0, column=0, padx=10)
        self.reboot_after_root.select()
        lf = ctk.CTkFrame(f)
        lf.pack(pady=10)
        ctk.CTkButton(lf, text=self.tr("download_twrp"), width=200,
                      fg_color="gray",
                      command=lambda: webbrowser.open("https://twrp.me/Devices/")).pack(side="left", padx=5)
        ctk.CTkButton(lf, text=self.tr("download_magisk"), width=200,
                      fg_color="gray",
                      command=lambda: webbrowser.open("https://github.com/topjohnwu/Magisk/releases")).pack(side="left", padx=5)

    def check_bl_status(self):
        def t():
            self.log("=" * 50)
            out = run([FASTBOOT, "oem", "device-info"], timeout=30)
            self.log(out)
            out2 = run([FASTBOOT, "getvar", "unlocked"], timeout=15)
            self.log(out2)
            combined = (out + out2).lower()
            if "unlocked: yes" in combined or "true" in combined:
                self.bl_status_label.configure(text=self.tr("bl_unlocked"),
                                                text_color="lightgreen")
            elif "unlocked: no" in combined or "false" in combined:
                self.bl_status_label.configure(text=self.tr("bl_locked"),
                                                text_color="red")
            else:
                self.bl_status_label.configure(text=self.tr("bl_unknown"),
                                                text_color="orange")
        threading.Thread(target=t, daemon=True).start()

    def unlock_bootloader(self):
        if not messagebox.askyesno(self.tr("warn"), self.tr("unlock_confirm")):
            return
        def t():
            self.log(self.tr("unlock_warn_screen"))
            out = run([FASTBOOT, "flashing", "unlock"], timeout=120)
            self.log(out)
        threading.Thread(target=t, daemon=True).start()

    def lock_bootloader(self):
        if not messagebox.askyesno(self.tr("warn"), self.tr("unlock_confirm")):
            return
        self.async_run(lambda: run([FASTBOOT, "flashing", "lock"], timeout=120))

    def pick_recovery(self):
        p = filedialog.askopenfilename(
            filetypes=[("Recovery Image", "*.img"), ("All", "*.*")])
        if p:
            self.recovery_img = p
            self.recovery_label.configure(text=os.path.basename(p),
                                           text_color="lightgreen")

    def pick_boot(self):
        p = filedialog.askopenfilename(
            filetypes=[("Boot Image", "*.img"), ("All", "*.*")])
        if p:
            self.boot_img = p
            self.boot_label.configure(text=os.path.basename(p),
                                       text_color="lightgreen")

    def flash_recovery(self):
        if not self.recovery_img or not os.path.exists(self.recovery_img):
            messagebox.showerror(self.tr("err"), self.tr("samsung_no_file"))
            return
        def t():
            out = run([FASTBOOT, "flash", "recovery", self.recovery_img], timeout=300)
            self.log(out)
            if "OKAY" in out:
                self.log(self.tr("flash_recovery_success"))
                if self.reboot_after_root.get():
                    run([FASTBOOT, "reboot", "recovery"])
        threading.Thread(target=t, daemon=True).start()

    def flash_boot(self):
        if not self.boot_img or not os.path.exists(self.boot_img):
            messagebox.showerror(self.tr("err"), self.tr("samsung_no_file"))
            return
        def t():
            out = run([FASTBOOT, "flash", "boot", self.boot_img], timeout=300)
            self.log(out)
            if "OKAY" in out:
                self.log(self.tr("flash_boot_success"))
        threading.Thread(target=t, daemon=True).start()

    # ============ Flash ============
    def build_flash_tab(self):
        f = self.tab_flash
        ctk.CTkLabel(f, text=self.tr("flash_title"),
                     font=("Arial", 16, "bold")).pack(pady=8)
        zf = ctk.CTkFrame(f)
        zf.pack(pady=6, fill="x", padx=20)
        ctk.CTkButton(zf, text=self.tr("flash_select_zip"), width=230, height=38,
                      fg_color="green", hover_color="darkgreen",
                      command=self.pick_flash_file).pack(side="left", padx=8)
        self.flash_file_label = ctk.CTkLabel(zf, text=self.tr("flash_status_idle"),
                                              font=("Arial", 11), text_color="gray")
        self.flash_file_label.pack(side="left", padx=10)
        tf = ctk.CTkFrame(f)
        tf.pack(pady=4)
        ctk.CTkButton(tf, text=self.tr("flash_scan"), width=150,
                      command=self.scan_rom).pack(side="left", padx=5)
        self.flash_type_label = ctk.CTkLabel(tf,
                                              text=self.tr("flash_type", self.tr("flash_type_unknown")),
                                              font=("Arial", 11), text_color="lightblue")
        self.flash_type_label.pack(side="left", padx=10)
        opts = ctk.CTkFrame(f)
        opts.pack(pady=6)
        ctk.CTkLabel(opts, text=self.tr("flash_mode")).grid(row=0, column=0, padx=5)
        self.flash_mode = ctk.CTkOptionMenu(
            opts, width=180,
            values=[self.tr("flash_mode_normal"),
                    self.tr("flash_mode_keep"),
                    self.tr("flash_mode_wipe")])
        self.flash_mode.grid(row=0, column=1, padx=5)
        self.chk_stop = ctk.CTkCheckBox(opts, text=self.tr("flash_stop_on_error"))
        self.chk_stop.grid(row=0, column=2, padx=10)
        self.chk_stop.select()
        self.chk_reboot = ctk.CTkCheckBox(opts, text=self.tr("flash_auto_reboot"))
        self.chk_reboot.grid(row=0, column=3, padx=10)
        self.chk_reboot.select()
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
        ctk.CTkLabel(f, text="📋 Partitions:",
                     font=("Arial", 12, "bold")).pack(anchor="w", padx=20, pady=(10, 3))
        self.part_list = ctk.CTkTextbox(f, height=110, font=("Consolas", 11))
        self.part_list.pack(fill="both", expand=True, padx=20, pady=(0, 10))

    # ============ Samsung ============
    def build_samsung_tab(self):
        f = self.tab_samsung
        ctk.CTkLabel(f, text=self.tr("samsung_title"),
                     font=("Arial", 16, "bold")).pack(pady=6)
        ctk.CTkLabel(f, text=self.tr("samsung_warning"),
                     font=("Arial", 11), text_color="orange").pack(pady=4)
        row0 = ctk.CTkFrame(f)
        row0.pack(pady=6)
        ctk.CTkButton(row0, text=self.tr("samsung_detect"), width=200, height=38,
                      command=self.samsung_detect).pack(side="left", padx=5)
        ctk.CTkButton(row0, text=self.tr("samsung_pit"), width=200, height=38,
                      command=self.samsung_pit).pack(side="left", padx=5)
        for name, var in [("samsung_ap", "samsung_ap"),
                          ("samsung_bl", "samsung_bl"),
                          ("samsung_cp", "samsung_cp"),
                          ("samsung_csc", "samsung_csc")]:
            row = ctk.CTkFrame(f)
            row.pack(pady=4, fill="x", padx=20)
            ctk.CTkLabel(row, text=self.tr(name), width=260, anchor="w").pack(side="left")
            lbl = ctk.CTkLabel(row, text=self.tr("samsung_no_file"),
                                font=("Arial", 10), text_color="gray")
            lbl.pack(side="left", padx=5)
            setattr(self, f"{var}_label", lbl)
            ctk.CTkButton(row, text=self.tr("pick"), width=80,
                          command=lambda v=var: self.samsung_pick(v)).pack(side="right", padx=5)
        opt = ctk.CTkFrame(f)
        opt.pack(pady=10)
        self.samsung_reboot = ctk.CTkCheckBox(opt, text=self.tr("samsung_reboot"))
        self.samsung_reboot.grid(row=0, column=0, padx=10)
        self.samsung_reboot.select()
        ctk.CTkButton(f, text=self.tr("samsung_flash_all"), width=350, height=50,
                      fg_color="green", hover_color="darkgreen",
                      font=("Arial", 15, "bold"),
                      command=self.samsung_flash_all).pack(pady=15)
        fl = ctk.CTkFrame(f)
        fl.pack(pady=5)
        for p in ["AP", "BL", "CP", "CSC"]:
            ctk.CTkButton(fl, text=self.tr(f"samsung_flash_{p.lower()}"), width=140,
                          command=lambda pp=p: self.samsung_flash_one(pp)).pack(side="left", padx=3)

    def samsung_pick(self, var):
        p = filedialog.askopenfilename(
            filetypes=[("Samsung", "*.tar.md5 *.tar"), ("All", "*.*")])
        if p:
            setattr(self, var, p)
            lbl = getattr(self, f"{var}_label")
            lbl.configure(text=os.path.basename(p), text_color="lightgreen")

    def samsung_detect(self):
        def t():
            self.log("=" * 50)
            if not os.path.exists(HEIMDALL):
                self.log(self.tr("msg_no_heimdall"))
                return
            self.log(run([HEIMDALL, "detect"], timeout=30))
        threading.Thread(target=t, daemon=True).start()

    def samsung_pit(self):
        def t():
            self.log("=" * 50)
            if not os.path.exists(HEIMDALL):
                self.log(self.tr("msg_no_heimdall"))
                return
            self.log(run([HEIMDALL, "print-pit"], timeout=60))
        threading.Thread(target=t, daemon=True).start()

    def samsung_flash_one(self, partition):
        key = {"AP": "samsung_ap", "BL": "samsung_bl",
               "CP": "samsung_cp", "CSC": "samsung_csc"}[partition]
        f = getattr(self, key, "")
        if not f or not os.path.exists(f):
            messagebox.showerror(self.tr("err"), self.tr("samsung_no_file"))
            return
        self.samsung_flash([(partition, f)])

    def samsung_flash_all(self):
        files = []
        for p, k in [("AP", "samsung_ap"), ("BL", "samsung_bl"),
                     ("CP", "samsung_cp"), ("CSC", "samsung_csc")]:
            v = getattr(self, k, "")
            if v and os.path.exists(v):
                files.append((p, v))
        if not files:
            messagebox.showerror(self.tr("err"), self.tr("samsung_no_file"))
            return
        self.samsung_flash(files)

    def samsung_flash(self, files):
        def t():
            self.log("=" * 50)
            if not os.path.exists(HEIMDALL):
                self.log(self.tr("msg_no_heimdall"))
                return
            det = run([HEIMDALL, "detect"], timeout=30)
            self.log(det)
            if "Detected" not in det and "Device" not in det:
                self.log("❌ No device")
                return
            for part, f in files:
                self.log(f"⏳ Flashing {part}: {os.path.basename(f)}")
                args = [HEIMDALL, "flash",
                        "--no-reboot" if not self.samsung_reboot.get() else "--reboot",
                        "--verbose", f"--{part}", f]
                out = run(args, timeout=3600, cwd=HEIMDALL_DIR)
                self.log(out[-1500:])
            self.log(self.tr("samsung_done"))
        threading.Thread(target=t, daemon=True).start()

    # ============ Unlock ============
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

    # ============ MTK ============
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
        ctk.CTkButton(f, text=self.tr("unlock_bl_mtk"), width=300,
                      fg_color="orange", hover_color="darkorange",
                      command=self.mtk_unlock).pack(pady=3)
        ctk.CTkButton(f, text=self.tr("wipe_frp"), width=300,
                      fg_color="orange", hover_color="darkorange",
                      command=self.mtk_wipe).pack(pady=3)

    # ============ EDL ============
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
        ops = ctk.CTkFrame(f)
        ops.pack(pady=15)
        ctk.CTkButton(ops, text=self.tr("edl_rw"), width=200,
                      fg_color="orange", hover_color="darkorange",
                      command=self.edl_rw).pack(side="left", padx=3)
        ctk.CTkButton(ops, text=self.tr("edl_reset"), width=180,
                      command=self.edl_reset).pack(side="left", padx=3)
        ctk.CTkButton(ops, text=self.tr("edl_wipe"), width=180,
                      fg_color="orange", hover_color="darkorange",
                      command=self.edl_wipe).pack(side="left", padx=3)

    # ============ Common ============
    def async_run(self, fn):
        def wrap():
            self.log(self.tr("msg_wait"))
            self.log(fn())
        threading.Thread(target=wrap, daemon=True).start()

    def check_tools(self):
        self.log(self.tr("msg_tools_ok") if os.path.exists(ADB) else self.tr("msg_tools_missing"))
        self.log(self.tr("msg_python_ok") if os.path.exists(EMBED_PY) else self.tr("msg_python_missing"))
        self.log(self.tr("msg_mtk_ok") if os.path.exists(MTK_SCRIPT) else self.tr("msg_mtk_missing"))
        self.log(self.tr("msg_edl_ok") if os.path.exists(EDL_SCRIPT) else self.tr("msg_edl_missing"))
        self.log(self.tr("msg_heimdall_ok") if os.path.exists(HEIMDALL) else self.tr("msg_heimdall_missing"))

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

    # ============ Flash ============
    def pick_flash_file(self):
        p = filedialog.askopenfilename(
            filetypes=[("ROM Files", "*.zip *.tar *.md5 *.tgz *.tar.gz"),
                       ("All files", "*.*")])
        if p:
            self.flash_file = p
            self.flash_file_label.configure(text=os.path.basename(p),
                                             text_color="lightgreen")
            self.log(f"📁 {p}")
            self.scan_rom()

    def scan_rom(self):
        if not self.flash_file:
            return
        self.flash_rom_type = detect_rom_type(self.flash_file)
        type_key = {
            "fastboot_zip": "flash_type_fastboot_zip",
            "samsung_tar": "flash_type_samsung_tar",
            "payload": "flash_type_payload",
            "tgz": "flash_type_tgz",
        }.get(self.flash_rom_type, "flash_type_unknown")
        label = self.tr(type_key)
        self.flash_type_label.configure(text=self.tr("flash_type", label))

    def extract_archive(self, path, dest):
        os.makedirs(dest, exist_ok=True)
        name = os.path.basename(path).lower()
        if name.endswith(".zip"):
            with zipfile.ZipFile(path) as z:
                z.extractall(dest)
        elif name.endswith((".tar", ".md5", ".tar.md5", ".tgz", ".tar.gz")):
            if name.endswith((".tgz", ".tar.gz")):
                with tarfile.open(path, "r:gz") as t:
                    t.extractall(dest)
            else:
                try:
                    with tarfile.open(path, "r:gz") as t:
                        t.extractall(dest)
                except tarfile.ReadError:
                    with tarfile.open(path, "r:") as t:
                        t.extractall(dest)

    def find_images(self):
        images = {}
        for root, dirs, files in os.walk(TEMP_FLASH):
            for f in files:
                if f.endswith(".img"):
                    name = os.path.splitext(f)[0]
                    images[name] = os.path.join(root, f)
        return images

    def start_flash(self):
        if not self.flash_file or not os.path.exists(self.flash_file):
            messagebox.showerror(self.tr("err"), "Select a ROM")
            return
        self.flash_cancel = False

        def task():
            try:
                if os.path.exists(TEMP_FLASH):
                    shutil.rmtree(TEMP_FLASH, ignore_errors=True)
                self.flash_status.configure(text=self.tr("flash_status_extracting"))
                self.log("📦 Extracting...")
                self.extract_archive(self.flash_file, TEMP_FLASH)
                payloads = []
                for root, dirs, files in os.walk(TEMP_FLASH):
                    for f in files:
                        if f == "payload.bin":
                            payloads.append(os.path.join(root, f))
                if payloads:
                    self.flash_status.configure(
                        text=self.tr("flash_status_extracting_payload"))
                    try:
                        p_url = "https://github.com/ssut/payload-dumper-go/releases/download/1.2.2/payload-dumper-go_1.2.2_windows_amd64.tar.gz"
                        tgz = os.path.join(BASE_DIR, "pdg.tgz")
                        urllib.request.urlretrieve(p_url, tgz)
                        with tarfile.open(tgz, "r:gz") as t:
                            t.extractall(BASE_DIR)
                        os.remove(tgz)
                        exe = os.path.join(BASE_DIR, "payload-dumper-go.exe")
                        if os.path.exists(exe):
                            out_dir = os.path.join(TEMP_FLASH, "extracted")
                            os.makedirs(out_dir, exist_ok=True)
                            for pl in payloads:
                                self.log(run([exe, "-o", out_dir, pl], timeout=1800))
                    except Exception as e:
                        self.log(f"⚠️ {e}")
                images = self.find_images()
                if not images:
                    self.log("❌ No images")
                    self.flash_status.configure(text=self.tr("flash_status_error"))
                    return
                self.log(f"✅ {len(images)} images")
                for name in sorted(images.keys()):
                    self.part_list.insert("end", f"{name}\n")
                mode = self.flash_mode.get()
                total = len(images)
                done = 0
                self.flash_progress.set(0)
                for name in sorted(images.keys()):
                    if self.flash_cancel:
                        self.flash_status.configure(text=self.tr("flash_status_cancelled"))
                        return
                    if mode == self.tr("flash_mode_keep") and name in ["userdata", "metadata"]:
                        done += 1
                        continue
                    self.flash_status.configure(text=self.tr("flash_status_flashing", name))
                    self.log(f"🚀 {name}")
                    out = run([FASTBOOT, "flash", name, images[name]], timeout=1200)
                    self.log(out[-500:])
                    if "FAILED" in out:
                        if self.chk_stop.get():
                            self.flash_status.configure(text=self.tr("flash_status_error"))
                            return
                    done += 1
                    self.flash_progress.set(done / total)
                if self.chk_reboot.get() and not self.flash_cancel:
                    run([FASTBOOT, "reboot"])
                self.flash_status.configure(text=self.tr("flash_status_done"))
                self.flash_progress.set(1)
            except Exception as e:
                self.log(f"❌ {e}")

        threading.Thread(target=task, daemon=True).start()

    def cancel_flash(self):
        self.flash_cancel = True

    # ============ Unlock Ops ============
    def check_lock(self):
        def t():
            out = run([ADB, "shell", "dumpsys", "device_policy"])
            for line in out.splitlines():
                if "mPasswordOwner" in line or "PasswordQuality" in line:
                    self.log(line.strip())
        threading.Thread(target=t, daemon=True).start()

    def check_root(self):
        def t():
            out = run([ADB, "shell", "which", "su"]).strip()
            self.log(f"👑 Root: {'✅ ' + out if out else '❌'}")
        threading.Thread(target=t, daemon=True).start()

    def check_frp(self):
        def t():
            out = run([ADB, "shell", "getprop", "ro.frp.pst"]).strip()
            self.log(f"FRP: {out or 'N/A'}")
        threading.Thread(target=t, daemon=True).start()

    def remove_locksettings(self):
        def t():
            for c in ["rm -f /data/system/locksettings.db",
                      "rm -f /data/system/locksettings.db-shm",
                      "rm -f /data/system/locksettings.db-wal"]:
                self.log(run([ADB, "shell", "su", "-c", c]))
        threading.Thread(target=t, daemon=True).start()

    def remove_gatekeeper(self):
        def t():
            for c in ["rm -f /data/system/gatekeeper.password.key",
                      "rm -f /data/system/gatekeeper.pattern.key"]:
                self.log(run([ADB, "shell", "su", "-c", c]))
        threading.Thread(target=t, daemon=True).start()

    def remove_pattern(self):
        def t():
            self.log(run([ADB, "shell", "su", "-c", "rm -f /data/system/gesture.key"]))
        threading.Thread(target=t, daemon=True).start()

    def full_info(self):
        def t():
            self.log(run([ADB, "shell", "getprop"], timeout=30)[:5000])
        threading.Thread(target=t, daemon=True).start()

    def erase_frp_adb(self):
        if not messagebox.askyesno(self.tr("warn"), self.tr("confirm_wipe")):
            return
        def t():
            self.log(run([ADB, "shell", "su", "-c",
                          "rm -rf /persistent/frp/* /data/system/users/0/frp/*"]))
        threading.Thread(target=t, daemon=True).start()

    def erase_frp_fastboot(self):
        if not messagebox.askyesno(self.tr("warn"), self.tr("confirm_wipe")):
            return
        self.async_run(lambda: run([FASTBOOT, "erase", "frp"], timeout=120))

    def format_data_fastboot(self):
        if not messagebox.askyesno(self.tr("warn"), self.tr("confirm_format")):
            return
        self.async_run(lambda: run([FASTBOOT, "erase", "userdata"], timeout=300))

    # ============ MTK Ops ============
    def run_mtk_gui(self):
        if not os.path.exists(EMBED_PY):
            self.log(self.tr("msg_no_embed"))
            return
        gui = os.path.join(MTK_DIR, "mtk_gui.py")
        if not os.path.exists(gui):
            self.log("❌ mtk_gui.py missing")
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

    # ============ EDL Ops ============
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