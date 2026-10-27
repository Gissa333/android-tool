import customtkinter as ctk
from tkinter import filedialog, messagebox, Tk
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
import time
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
EXPORTS_DIR = os.path.join(BASE_DIR, "exports")
BACKUP_DIR = os.path.join(BASE_DIR, "backups")
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")
EMBED_PY = os.path.join(BASE_DIR, "python-embed", "python.exe")
ADB = os.path.join(TOOLS_DIR, "adb.exe")
FASTBOOT = os.path.join(TOOLS_DIR, "fastboot.exe")
MTK_SCRIPT = os.path.join(MTK_DIR, "mtk.py")
EDL_SCRIPT = os.path.join(EDL_DIR, "edl.py")
HEIMDALL = os.path.join(HEIMDALL_DIR, "heimdall.exe")

PLATFORM_TOOLS_URL = "https://dl.google.com/android/repository/platform-tools-latest-windows.zip"
APP_VERSION = "2.1.0"
GITHUB_REPO = "Gissa333/android-tool"
GITHUB_API = "https://api.github.com/repos/" + GITHUB_REPO + "/releases/latest"
SECRET_LICENSE_KEY = "PRO-2026-ANDROID-TOOL"

NO_WINDOW = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
NEW_CONSOLE = subprocess.CREATE_NEW_CONSOLE if os.name == "nt" else 0

LANG = {
    "ar": {
        "title": "أداة الأندرويد",
        "tab_adb": "ADB / Fastboot",
        "tab_tools": "أدوات يومية",
        "tab_system": "أدوات النظام",
        "tab_gaming": "الألعاب والأداء",
        "tab_apps": "إدارة التطبيقات",
        "tab_backup": "نسخ احتياطي",
        "tab_flash": "فلاش الروم",
        "tab_xiaomi": "Xiaomi",
        "tab_huawei": "Huawei",
        "tab_samsung": "Samsung",
        "tab_oppo": "Oppo/Realme",
        "tab_vivo": "Vivo/iQOO",
        "tab_root": "TWRP & Root",
        "tab_unlock": "فك القفل",
        "tab_mtk": "MTK",
        "tab_edl": "Qualcomm EDL",
        "tab_adv": "أدوات متقدمة",
        "tab_guide": "الدليل",
        "tab_about": "حول",
        "download_tools": "تحميل Platform-Tools",
        "detect": "اكتشاف الأجهزة",
        "device_info": "معلومات الجهاز",
        "reboot": "إعادة تشغيل",
        "fastboot": "وضع Fastboot",
        "reboot_recovery": "وضع Recovery",
        "reboot_edl": "وضع EDL",
        "exit_fastboot": "خروج من Fastboot",
        "tools_title": "أدوات يومية (ADB)",
        "tools_screenshot": "لقطة شاشة",
        "tools_record": "تسجيل الشاشة (15 ثانية)",
        "tools_record_stop": "إيقاف التسجيل",
        "tools_install_apk": "تثبيت APK",
        "tools_push": "إرسال ملف للهاتف",
        "tools_pull": "سحب ملف من الهاتف",
        "tools_list_packages": "قائمة التطبيقات",
        "tools_battery": "معلومات البطارية",
        "tools_export_dir": "فتح مجلد التصدير",
        "tools_wait": "جاري...",
        "tools_recording": "جاري التسجيل... انتظر 15 ثانية",
        "tools_recorded": "تم حفظ التسجيل: {}",
        "tools_screenshot_saved": "تم حفظ اللقطة: {}",
        "tools_no_device": "لا يوجد جهاز متصل",
        "tools_install_success": "تم تثبيت: {}",
        "tools_install_fail": "فشل التثبيت: {}",
        "tools_battery_info": "معلومات البطارية",
        "tools_apps_list": "التطبيقات المثبتة",
        "sys_title": "أدوات النظام المتقدمة",
        "sys_nav_hide": "إخفاء شريط التنقل",
        "sys_nav_show": "إظهار شريط التنقل",
        "sys_dpi_title": "تغيير كثافة الشاشة (DPI):",
        "sys_dpi_placeholder": "مثال: 420",
        "sys_dpi_apply": "تطبيق DPI",
        "sys_dpi_reset": "إعادة DPI الافتراضي",
        "sys_anim": "تسريع الحركة (Animation):",
        "sys_anim_fast": "تسريع (0.5x)",
        "sys_anim_normal": "إعادة للوضع الطبيعي (1x)",
        "sys_anim_value": "مثال: 0.5",
        "sys_anim_apply": "تطبيق",
        "sys_sysui": "إعادة تشغيل واجهة النظام (SystemUI)",
        "sys_gms": "تعطيل/تفعيل خدمات جوجل (GMS):",
        "sys_gms_disable": "تعطيل GMS",
        "sys_gms_enable": "تفعيل GMS",
        "sys_restart": "إعادة تشغيل الهاتف",
        "sys_applied": "تم التطبيق",
        "sys_reset": "تم إعادة القيمة الافتراضية",
        "sys_sysui_restarting": "جاري إعادة تشغيل SystemUI...",
        "sys_gms_disabled": "GMS معطل",
        "sys_gms_enabled": "GMS مفعل",
        "game_title": "تسريع الألعاب والأداء",
        "game_boost": "تفعيل وضع الأداء العالي (بدون روت)",
        "game_boost_desc": "يعطل خدمات الخلفية ويسرع الحركة",
        "game_normal": "إلغاء وضع الألعاب",
        "game_normal_desc": "إعادة الهاتف لوضعه الطبيعي",
        "game_ram": "تنظيف الذاكرة العشوائية (RAM)",
        "game_ram_ok": "تم تنظيف الذاكرة العشوائية",
        "game_cache": "مسح الكاش (Cache) لجميع التطبيقات",
        "game_cache_ok": "تم مسح الكاش",
        "game_bg": "تعطيل التطبيقات في الخلفية",
        "game_bg_ok": "تم تعطيل التطبيقات في الخلفية",
        "game_bg_enable": "تفعيل التطبيقات في الخلفية",
        "game_info": "ملاحظة: هذه الأوامر آمنة ولا تحتاج إلى روت.",
        "adv_title": "أدوات متقدمة",
        "adv_adb_terminal": "تشغيل أوامر ADB مخصصة",
        "adv_adb_terminal_desc": "اكتب أمر adb shell ونفذه مباشرة على الهاتف",
        "adv_install_batch": "تثبيت ملفات APK دفعة واحدة",
        "adv_install_batch_desc": "اختر مجلداً لتثبيت جميع ملفات APK بداخله",
        "adv_battery_calib": "معايرة البطارية",
        "adv_battery_calib_desc": "مسح ملف batterystats.bin (يتطلب روت)",
        "adv_network_info": "معلومات الشبكة",
        "adv_network_info_desc": "عرض IP وحالة الواي فاي والشبكة",
        "adv_hide_app": "إخفاء تطبيق",
        "adv_hide_app_desc": "إخفاء تطبيق من قائمة التطبيقات",
        "adv_show_app": "إظهار تطبيق مخفي",
        "adv_show_app_desc": "إعادة إظهار تطبيق تم إخفاؤه",
        "adv_fastboot_info": "معلومات Fastboot",
        "adv_fastboot_info_desc": "عرض متغيرات Fastboot كاملة",
        "adv_reboot_bootloader": "إعادة تشغيل إلى Fastboot",
        "adv_reboot_recovery": "إعادة تشغيل إلى Recovery",
        "adv_reboot_download": "إعادة تشغيل إلى Download Mode",
        "adv_device_props": "خصائص النظام الكاملة",
        "adv_device_props_desc": "عرض getprop كامل",
        "adv_adb_prompt": "أدخل أمر ADB (مثال: shell getprop):",
        "adv_pick_folder": "اختر مجلد APK",
        "adv_installing": "تثبيت: {}",
        "adv_install_count": "تم تثبيت {} تطبيق",
        "adv_no_apk": "لا توجد ملفات APK في المجلد",
        "adv_battery_warn": "هذه العملية تتطلب روت. متأكد؟",
        "adv_battery_done": "تم مسح إحصائيات البطارية. أعد تشغيل الهاتف.",
        "adv_network_loading": "جاري جلب معلومات الشبكة...",
        "adv_hide_app_prompt": "أدخل اسم الحزمة (Package Name):",
        "adv_app_hidden": "تم إخفاء {}",
        "adv_app_shown": "تم إظهار {}",
        "adv_fastboot_info_loading": "جاري جلب معلومات Fastboot...",
        "adv_device_props_loading": "جاري جلب الخصائص...",
        "guide_title": "دليل الاستخدام",
        "apps_title": "إدارة التطبيقات",
        "apps_load": "تحميل قائمة التطبيقات",
        "apps_uninstall": "حذف التطبيق",
        "apps_disable": "تعطيل",
        "apps_enable": "تفعيل",
        "apps_extract": "استخراج APK",
        "apps_clear": "مسح البيانات",
        "apps_force_stop": "إيقاف",
        "apps_filter": "فلتر:",
        "apps_filter_all": "الكل",
        "apps_filter_user": "المستخدم فقط",
        "apps_filter_system": "النظام فقط",
        "apps_count": "{} تطبيق",
        "apps_select": "اختر تطبيقاً من القائمة:",
        "apps_loading": "جاري تحميل قائمة التطبيقات...",
        "apps_loaded": "تم تحميل {} تطبيق",
        "apps_no_device": "لا يوجد جهاز متصل",
        "apps_no_packages": "لا توجد تطبيقات",
        "apps_uninstall_ok": "تم حذف {}",
        "apps_uninstall_fail": "فشل حذف {}",
        "apps_disable_ok": "تم تعطيل {}",
        "apps_enable_ok": "تم تفعيل {}",
        "apps_extract_ok": "تم استخراج {}",
        "apps_clear_ok": "تم مسح بيانات {}",
        "apps_stop_ok": "تم إيقاف {}",
        "backup_title": "النسخ الاحتياطي والاستعادة",
        "backup_full": "نسخ احتياطي كامل (Apps + Data)",
        "backup_app": "نسخ احتياطي لتطبيق محدد",
        "backup_sdcard": "نسخ بطاقة SD كاملة",
        "backup_restore": "استعادة نسخة احتياطية",
        "backup_open": "فتح مجلد النسخ الاحتياطي",
        "backup_warning": "النسخ الاحتياطي الكامل يتطلب تأكيد من شاشة الهاتف",
        "backup_no_device": "لا يوجد جهاز متصل",
        "backup_starting": "بدء النسخ الاحتياطي...",
        "backup_confirm_phone": "اضغط 'Back up my data' على شاشة الهاتف",
        "backup_done": "اكتمل النسخ الاحتياطي: {}",
        "backup_fail": "فشل النسخ الاحتياطي",
        "backup_restore_done": "تم بدء الاستعادة - اضغط Restore على الهاتف",
        "backup_sdcard_done": "تم نسخ SD: {}",
        "backup_sdcard_fail": "فشل نسخ SD",
        "backup_app_prompt": "أدخل اسم الحزمة (Package Name):",
        "vivo_title": "Vivo / iQOO",
        "vivo_warning": "Funtouch OS / OriginOS",
        "vivo_info": "معلومات الجهاز",
        "vivo_check_bl": "فحص البوتلودر",
        "vivo_fastboot": "Fastboot",
        "vivo_recovery": "Recovery",
        "vivo_edl": "EDL",
        "vivo_flash_boot": "boot.img",
        "vivo_flash_recovery": "recovery.img",
        "vivo_flash_vbmeta": "vbmeta.img",
        "vivo_flash_dtbo": "dtbo.img",
        "vivo_flash_super": "super.img",
        "vivo_flash_custom": "قسم مخصص",
        "vivo_partition": "القسم:",
        "vivo_image": "الصورة:",
        "vivo_unlock_help": "مساعدة الفتح",
        "vivo_download_help": "دليل الفتح",
        "vivo_unlock_cmd": "محاولة فتح",
        "vivo_lock_cmd": "قفل",
        "vivo_select_rom": "اختر ROM",
        "vivo_flash_wipe": "فلاش + Wipe",
        "vivo_flash_keep": "فلاش (Keep)",
        "vivo_erase_frp": "FRP",
        "vivo_wipe_data": "محو البيانات",
        "vivo_reboot_ok": "عادي",
        "flash_title": "فلاش الروم",
        "flash_select_zip": "اختر ملف الروم",
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
        "flash_start": "بدء الفلاش",
        "flash_cancel": "إلغاء",
        "flash_scan": "فحص الروم",
        "flash_progress": "التقدم:",
        "flash_status_idle": "بانتظار البدء",
        "flash_status_extracting": "فك الضغط...",
        "flash_status_extracting_payload": "استخراج payload...",
        "flash_status_flashing": "فلاش: {}",
        "flash_status_done": "اكتمل",
        "flash_status_error": "فشل",
        "flash_status_cancelled": "إلغاء",
        "xiaomi_title": "Xiaomi / Redmi / POCO",
        "xiaomi_warning": "HyperOS لها قيود",
        "xiaomi_info": "معلومات",
        "xiaomi_unlock_help": "مساعدة الفتح",
        "xiaomi_mi_assistant": "Mi Assistant",
        "xiaomi_select_rom": "اختر ROM (.tgz)",
        "xiaomi_flash_all": "فلاش كامل",
        "xiaomi_flash_all_no_data": "فلاش (بدون data)",
        "xiaomi_flash_boot": "boot.img",
        "xiaomi_flash_recovery": "recovery.img",
        "xiaomi_flash_vbmeta": "vbmeta.img",
        "xiaomi_partition_name": "القسم:",
        "xiaomi_image_file": "الصورة:",
        "xiaomi_remove_mi_account": "إزالة Mi Account",
        "xiaomi_remove_mi_account_help": "يتطلب EDL/MTK",
        "xiaomi_clean_and_lock": "فلاش + قفل",
        "xiaomi_reboot_fastboot": "Fastboot",
        "xiaomi_reboot_recovery": "Recovery",
        "xiaomi_reboot_edl": "EDL",
        "huawei_title": "Huawei / Honor",
        "huawei_warning": "الأجهزة الحديثة محمية بـ Huawei ID",
        "huawei_info": "معلومات الجهاز",
        "huawei_fastboot": "Fastboot",
        "huawei_recovery": "Recovery",
        "huawei_erecovery": "eRecovery",
        "huawei_flash_boot": "boot.img",
        "huawei_flash_recovery": "recovery.img",
        "huawei_flash_system": "system.img",
        "huawei_flash_ramdisk": "ramdisk.img",
        "huawei_flash_custom": "قسم مخصص",
        "huawei_partition": "القسم:",
        "huawei_image": "الصورة:",
        "huawei_unlock_help": "مساعدة الفتح",
        "huawei_hisuite": "HiSuite",
        "huawei_erecovery_help": "دليل eRecovery",
        "huawei_check_bl": "فحص البوتلودر",
        "huawei_unlock_code": "فتح بكود",
        "huawei_erase_frp": "FRP",
        "huawei_wipe_data": "محو",
        "huawei_reboot_ok": "عادي",
        "samsung_title": "Samsung — Download",
        "samsung_warning": "ضع الجهاز في Download Mode",
        "samsung_detect": "كشف",
        "samsung_pit": "PIT",
        "samsung_flash_ap": "AP",
        "samsung_flash_bl": "BL",
        "samsung_flash_cp": "CP",
        "samsung_flash_csc": "CSC",
        "samsung_flash_all": "فلاش الكل",
        "samsung_ap": "AP:",
        "samsung_bl": "BL:",
        "samsung_cp": "CP:",
        "samsung_csc": "CSC:",
        "samsung_no_file": "لم يتم اختيار ملف",
        "samsung_reboot": "إعادة التشغيل",
        "samsung_done": "اكتمل",
        "oppo_title": "Oppo / Realme / OnePlus",
        "oppo_warning": "ColorOS / OxygenOS",
        "oppo_info": "معلومات الجهاز",
        "oppo_check_bl": "فحص البوتلودر",
        "oppo_fastboot": "Fastboot",
        "oppo_recovery": "Recovery",
        "oppo_edl": "EDL",
        "oppo_flash_boot": "boot.img",
        "oppo_flash_recovery": "recovery.img",
        "oppo_flash_vbmeta": "vbmeta.img",
        "oppo_flash_dtbo": "dtbo.img",
        "oppo_flash_super": "super.img",
        "oppo_flash_custom": "قسم مخصص",
        "oppo_partition": "القسم:",
        "oppo_image": "الصورة:",
        "oppo_unlock_help": "مساعدة الفتح",
        "oppo_download_help": "دليل الفتح",
        "oppo_unlock_cmd": "محاولة فتح",
        "oppo_lock_cmd": "قفل",
        "oppo_select_rom": "اختر ROM",
        "oppo_flash_wipe": "فلاش + Wipe",
        "oppo_flash_keep": "فلاش (Keep)",
        "oppo_erase_frp": "FRP",
        "oppo_wipe_data": "محو البيانات",
        "oppo_reboot_ok": "عادي",
        "root_title": "TWRP & Root",
        "root_warning": "تأكد من فتح البوتلودر",
        "check_bl_status": "فحص البوتلودر",
        "unlock_bl": "فتح",
        "lock_bl": "قفل",
        "flash_twrp": "TWRP",
        "flash_magisk": "Magisk",
        "select_recovery": "اختر recovery.img",
        "select_boot": "اختر boot patched",
        "bl_locked": "مقفل",
        "bl_unlocked": "مفتوح",
        "bl_unknown": "غير معروف",
        "unlock_confirm": "سيتم محو البيانات!",
        "unlock_warn_screen": "اضغط Volume Up على الشاشة",
        "flash_recovery_success": "recovery",
        "flash_boot_success": "boot",
        "reboot_recovery_after": "إعادة إلى Recovery",
        "download_twrp": "TWRP",
        "download_magisk": "Magisk",
        "unlock_title": "فك القفل و FRP",
        "check_lock": "فحص القفل",
        "check_root": "فحص الروت",
        "check_frp": "فحص FRP",
        "remove_locksettings": "locksettings",
        "remove_gatekeeper": "gatekeeper",
        "remove_pattern": "النمط",
        "format_data_fastboot": "Format Data",
        "erase_frp_fastboot": "FRP (FB)",
        "erase_frp_adb": "FRP (ADB)",
        "full_device_info": "معلومات كاملة",
        "unlock_warning": "على مسؤوليتك",
        "mtk_title": "mtkclient",
        "run_gui": "الواجهة",
        "read_gpt": "GPT",
        "read_part": "قراءة:",
        "read_btn": "قراءة",
        "write_part": "كتابة:",
        "pick": "اختر",
        "write_btn": "كتابة",
        "advanced": "متقدم",
        "unlock_bl_mtk": "فك MTK",
        "wipe_frp": "FRP + Userdata",
        "edl_title": "Qualcomm EDL",
        "edl_check": "فحص",
        "edl_printgpt": "الأقسام",
        "edl_dump": "استخراج",
        "edl_load": "كتابة",
        "edl_rw": "R/W",
        "edl_reset": "Reset",
        "edl_wipe": "Userdata",
        "edl_firehose": "Firehose:",
        "edl_partition": "القسم:",
        "about_title": "حول",
        "about_version": "الإصدار: {}",
        "about_check_update": "فحص التحديثات",
        "about_download_update": "تحميل",
        "about_github": "GitHub",
        "about_up_to_date": "أحدث إصدار",
        "about_new_version": "جديد: {}",
        "about_checking": "فحص...",
        "about_error": "خطأ: {}",
        "about_description": "أداة شاملة لهواتف أندرويد\n\n• ADB / Fastboot\n• أدوات يومية\n• أدوات النظام\n• تسريع الألعاب\n• إدارة التطبيقات\n• النسخ الاحتياطي\n• فلاش الروم\n• Xiaomi / Huawei / Samsung / Oppo / Vivo\n• TWRP & Root\n• فك القفل و FRP\n• MediaTek\n• Qualcomm EDL\n• أدوات متقدمة",
        "log": "السجل:",
        "log_save": "حفظ",
        "log_copy": "نسخ",
        "log_clear": "مسح",
        "log_open_folder": "فتح",
        "log_saved": "حفظ: {}",
        "log_copied": "نسخ",
        "log_cleared": "مسح",
        "lang_btn": "English",
        "msg_wait": "...",
        "msg_tools_ok": "Platform-Tools",
        "msg_tools_missing": "Platform-Tools",
        "msg_python_ok": "Python",
        "msg_python_missing": "Python",
        "msg_mtk_ok": "mtkclient",
        "msg_mtk_missing": "mtkclient",
        "msg_edl_ok": "edl",
        "msg_edl_missing": "edl",
        "msg_heimdall_ok": "Heimdall",
        "msg_heimdall_missing": "Heimdall",
        "msg_downloading_pt": "تحميل Platform-Tools...",
        "msg_installed": "تم",
        "msg_error": "خطأ: {}",
        "msg_adb": "ADB",
        "msg_fastboot": "Fastboot",
        "msg_no_embed": "Python غير موجود",
        "msg_no_mtk": "mtkclient",
        "msg_no_edl": "edl",
        "confirm_write": "كتابة {} من {}؟",
        "confirm_unlock": "فك القفل؟",
        "confirm_wipe": "مسح!",
        "confirm_format": "محو الكل؟",
        "confirm_flash_samsung": "فلاش {}؟",
        "confirm_uninstall": "حذف {}؟",
        "confirm_disable": "تعطيل {}؟",
        "confirm_clear": "مسح بيانات {}؟",
        "confirm_reset_dpi": "إعادة DPI الافتراضي؟",
        "confirm_sysui": "إعادة تشغيل واجهة النظام؟",
        "confirm_reboot": "إعادة تشغيل الهاتف؟",
        "err_check": "تحقق",
        "err": "خطأ",
        "confirm": "تأكيد",
        "warn": "تحذير",
        "lic_title": "تنشيط البرنامج",
        "lic_desc": "أدخل كود التفعيل الخاص بك لبدء استخدام البرنامج",
        "lic_placeholder": "أدخل الكود هنا...",
        "lic_activate": "تفعيل",
        "lic_error": "كود غير صحيح",
        "lic_success": "تم التفعيل بنجاح",
        "lic_no_key": "الرجاء إدخال الكود"
    },
    "en": {
        "title": "Android Tool",
        "tab_adb": "ADB / Fastboot",
        "tab_tools": "Daily Tools",
        "tab_system": "System Tools",
        "tab_gaming": "Gaming & Performance",
        "tab_apps": "App Manager",
        "tab_backup": "Backup",
        "tab_flash": "Flash ROM",
        "tab_xiaomi": "Xiaomi",
        "tab_huawei": "Huawei",
        "tab_samsung": "Samsung",
        "tab_oppo": "Oppo/Realme",
        "tab_vivo": "Vivo/iQOO",
        "tab_root": "TWRP & Root",
        "tab_unlock": "Unlock",
        "tab_mtk": "MTK",
        "tab_edl": "Qualcomm EDL",
        "tab_adv": "Advanced Tools",
        "tab_guide": "Guide",
        "tab_about": "About",
        "download_tools": "Download Platform-Tools",
        "detect": "Detect Devices",
        "device_info": "Device Info",
        "reboot": "Reboot",
        "fastboot": "Fastboot",
        "reboot_recovery": "Recovery",
        "reboot_edl": "EDL",
        "exit_fastboot": "Exit Fastboot",
        "tools_title": "Daily Tools (ADB)",
        "tools_screenshot": "Screenshot",
        "tools_record": "Screen Record (15s)",
        "tools_record_stop": "Stop Recording",
        "tools_install_apk": "Install APK",
        "tools_push": "Push File",
        "tools_pull": "Pull File",
        "tools_list_packages": "List Packages",
        "tools_battery": "Battery Info",
        "tools_export_dir": "Open Export Folder",
        "tools_wait": "Please wait...",
        "tools_recording": "Recording... wait 15 seconds",
        "tools_recorded": "Recording saved: {}",
        "tools_screenshot_saved": "Screenshot saved: {}",
        "tools_no_device": "No device connected",
        "tools_install_success": "Installed: {}",
        "tools_install_fail": "Install failed: {}",
        "tools_battery_info": "Battery Info",
        "tools_apps_list": "Installed Apps",
        "sys_title": "Advanced System Tools",
        "sys_nav_hide": "Hide Navigation Bar",
        "sys_nav_show": "Show Navigation Bar",
        "sys_dpi_title": "Change Screen Density (DPI):",
        "sys_dpi_placeholder": "Example: 420",
        "sys_dpi_apply": "Apply DPI",
        "sys_dpi_reset": "Reset DPI",
        "sys_anim": "Animation Speed:",
        "sys_anim_fast": "Fast (0.5x)",
        "sys_anim_normal": "Normal (1x)",
        "sys_anim_value": "Example: 0.5",
        "sys_anim_apply": "Apply",
        "sys_sysui": "Restart SystemUI",
        "sys_gms": "Toggle Google Services (GMS):",
        "sys_gms_disable": "Disable GMS",
        "sys_gms_enable": "Enable GMS",
        "sys_restart": "Reboot Phone",
        "sys_applied": "Applied",
        "sys_reset": "Reset to default",
        "sys_sysui_restarting": "Restarting SystemUI...",
        "sys_gms_disabled": "GMS Disabled",
        "sys_gms_enabled": "GMS Enabled",
        "game_title": "Gaming & Performance Boost",
        "game_boost": "Enable High Performance Mode (No Root)",
        "game_boost_desc": "Disables background services and speeds up animations",
        "game_normal": "Disable Gaming Mode",
        "game_normal_desc": "Restores phone to normal state",
        "game_ram": "Clean RAM",
        "game_ram_ok": "RAM Cleaned",
        "game_cache": "Clear Cache for All Apps",
        "game_cache_ok": "Cache Cleared",
        "game_bg": "Disable Background Apps",
        "game_bg_ok": "Background Apps Disabled",
        "game_bg_enable": "Enable Background Apps",
        "game_info": "Note: These commands are safe and do not require root.",
        "adv_title": "Advanced Tools",
        "adv_adb_terminal": "Run Custom ADB Commands",
        "adv_adb_terminal_desc": "Type adb shell command and execute it directly on the phone",
        "adv_install_batch": "Batch Install APKs",
        "adv_install_batch_desc": "Select a folder to install all APKs inside it",
        "adv_battery_calib": "Battery Calibration",
        "adv_battery_calib_desc": "Clear batterystats.bin (requires root)",
        "adv_network_info": "Network Info",
        "adv_network_info_desc": "Display IP, Wi-Fi, and network status",
        "adv_hide_app": "Hide App",
        "adv_hide_app_desc": "Hide an app from the app drawer",
        "adv_show_app": "Show Hidden App",
        "adv_show_app_desc": "Re-show a hidden app",
        "adv_fastboot_info": "Fastboot Info",
        "adv_fastboot_info_desc": "Show full Fastboot variables",
        "adv_reboot_bootloader": "Reboot to Fastboot",
        "adv_reboot_recovery": "Reboot to Recovery",
        "adv_reboot_download": "Reboot to Download Mode",
        "adv_device_props": "Full System Properties",
        "adv_device_props_desc": "Show full getprop",
        "adv_adb_prompt": "Enter ADB command (e.g., shell getprop):",
        "adv_pick_folder": "Select APK Folder",
        "adv_installing": "Installing: {}",
        "adv_install_count": "Installed {} apps",
        "adv_no_apk": "No APK files found in folder",
        "adv_battery_warn": "This process requires root. Are you sure?",
        "adv_battery_done": "Battery stats cleared. Reboot phone.",
        "adv_network_loading": "Fetching network info...",
        "adv_hide_app_prompt": "Enter package name:",
        "adv_app_hidden": "Hidden {}",
        "adv_app_shown": "Shown {}",
        "adv_fastboot_info_loading": "Fetching Fastboot info...",
        "adv_device_props_loading": "Fetching properties...",
        "guide_title": "Usage Guide",
        "apps_title": "App Manager",
        "apps_load": "Load App List",
        "apps_uninstall": "Uninstall",
        "apps_disable": "Disable",
        "apps_enable": "Enable",
        "apps_extract": "Extract APK",
        "apps_clear": "Clear Data",
        "apps_force_stop": "Force Stop",
        "apps_filter": "Filter:",
        "apps_filter_all": "All",
        "apps_filter_user": "User Only",
        "apps_filter_system": "System Only",
        "apps_count": "{} apps",
        "apps_select": "Select an app from the list:",
        "apps_loading": "Loading app list...",
        "apps_loaded": "Loaded {} apps",
        "apps_no_device": "No device connected",
        "apps_no_packages": "No apps found",
        "apps_uninstall_ok": "Uninstalled {}",
        "apps_uninstall_fail": "Failed to uninstall {}",
        "apps_disable_ok": "Disabled {}",
        "apps_enable_ok": "Enabled {}",
        "apps_extract_ok": "Extracted {}",
        "apps_clear_ok": "Cleared data for {}",
        "apps_stop_ok": "Stopped {}",
        "backup_title": "Backup & Restore",
        "backup_full": "Full Backup (Apps + Data)",
        "backup_app": "Backup Specific App",
        "backup_sdcard": "Backup Full SD Card",
        "backup_restore": "Restore Backup",
        "backup_open": "Open Backup Folder",
        "backup_warning": "Full backup requires confirmation on phone screen",
        "backup_no_device": "No device connected",
        "backup_starting": "Starting backup...",
        "backup_confirm_phone": "Tap 'Back up my data' on phone screen",
        "backup_done": "Backup completed: {}",
        "backup_fail": "Backup failed",
        "backup_restore_done": "Restore started - tap Restore on phone",
        "backup_sdcard_done": "SD backed up: {}",
        "backup_sdcard_fail": "SD backup failed",
        "backup_app_prompt": "Enter package name:",
        "vivo_title": "Vivo / iQOO",
        "vivo_warning": "Funtouch OS / OriginOS",
        "vivo_info": "Device Info",
        "vivo_check_bl": "Check Bootloader",
        "vivo_fastboot": "Fastboot",
        "vivo_recovery": "Recovery",
        "vivo_edl": "EDL",
        "vivo_flash_boot": "boot.img",
        "vivo_flash_recovery": "recovery.img",
        "vivo_flash_vbmeta": "vbmeta.img",
        "vivo_flash_dtbo": "dtbo.img",
        "vivo_flash_super": "super.img",
        "vivo_flash_custom": "Custom Partition",
        "vivo_partition": "Partition:",
        "vivo_image": "Image:",
        "vivo_unlock_help": "Unlock Help",
        "vivo_download_help": "Unlock Guide",
        "vivo_unlock_cmd": "Attempt Unlock",
        "vivo_lock_cmd": "Lock",
        "vivo_select_rom": "Select ROM",
        "vivo_flash_wipe": "Flash + Wipe",
        "vivo_flash_keep": "Flash (Keep)",
        "vivo_erase_frp": "FRP",
        "vivo_wipe_data": "Wipe Data",
        "vivo_reboot_ok": "Normal",
        "flash_title": "Flash ROM",
        "flash_select_zip": "Select ROM File",
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
        "flash_start": "Start Flash",
        "flash_cancel": "Cancel",
        "flash_scan": "Scan ROM",
        "flash_progress": "Progress:",
        "flash_status_idle": "Waiting to start",
        "flash_status_extracting": "Extracting...",
        "flash_status_extracting_payload": "Extracting payload...",
        "flash_status_flashing": "Flashing: {}",
        "flash_status_done": "Completed",
        "flash_status_error": "Failed",
        "flash_status_cancelled": "Cancelled",
        "xiaomi_title": "Xiaomi / Redmi / POCO",
        "xiaomi_warning": "HyperOS has restrictions",
        "xiaomi_info": "Info",
        "xiaomi_unlock_help": "Unlock Help",
        "xiaomi_mi_assistant": "Mi Assistant",
        "xiaomi_select_rom": "Select ROM (.tgz)",
        "xiaomi_flash_all": "Full Flash",
        "xiaomi_flash_all_no_data": "Flash (No data)",
        "xiaomi_flash_boot": "boot.img",
        "xiaomi_flash_recovery": "recovery.img",
        "xiaomi_flash_vbmeta": "vbmeta.img",
        "xiaomi_partition_name": "Partition:",
        "xiaomi_image_file": "Image:",
        "xiaomi_remove_mi_account": "Remove Mi Account",
        "xiaomi_remove_mi_account_help": "Requires EDL/MTK",
        "xiaomi_clean_and_lock": "Flash + Lock",
        "xiaomi_reboot_fastboot": "Fastboot",
        "xiaomi_reboot_recovery": "Recovery",
        "xiaomi_reboot_edl": "EDL",
        "huawei_title": "Huawei / Honor",
        "huawei_warning": "Modern devices protected by Huawei ID",
        "huawei_info": "Device Info",
        "huawei_fastboot": "Fastboot",
        "huawei_recovery": "Recovery",
        "huawei_erecovery": "eRecovery",
        "huawei_flash_boot": "boot.img",
        "huawei_flash_recovery": "recovery.img",
        "huawei_flash_system": "system.img",
        "huawei_flash_ramdisk": "ramdisk.img",
        "huawei_flash_custom": "Custom Partition",
        "huawei_partition": "Partition:",
        "huawei_image": "Image:",
        "huawei_unlock_help": "Unlock Help",
        "huawei_hisuite": "HiSuite",
        "huawei_erecovery_help": "eRecovery Guide",
        "huawei_check_bl": "Check Bootloader",
        "huawei_unlock_code": "Unlock with Code",
        "huawei_erase_frp": "FRP",
        "huawei_wipe_data": "Wipe",
        "huawei_reboot_ok": "Normal",
        "samsung_title": "Samsung — Download",
        "samsung_warning": "Put device in Download Mode",
        "samsung_detect": "Detect",
        "samsung_pit": "PIT",
        "samsung_flash_ap": "AP",
        "samsung_flash_bl": "BL",
        "samsung_flash_cp": "CP",
        "samsung_flash_csc": "CSC",
        "samsung_flash_all": "Flash All",
        "samsung_ap": "AP:",
        "samsung_bl": "BL:",
        "samsung_cp": "CP:",
        "samsung_csc": "CSC:",
        "samsung_no_file": "No file selected",
        "samsung_reboot": "Reboot",
        "samsung_done": "Completed",
        "oppo_title": "Oppo / Realme / OnePlus",
        "oppo_warning": "ColorOS / OxygenOS",
        "oppo_info": "Device Info",
        "oppo_check_bl": "Check Bootloader",
        "oppo_fastboot": "Fastboot",
        "oppo_recovery": "Recovery",
        "oppo_edl": "EDL",
        "oppo_flash_boot": "boot.img",
        "oppo_flash_recovery": "recovery.img",
        "oppo_flash_vbmeta": "vbmeta.img",
        "oppo_flash_dtbo": "dtbo.img",
        "oppo_flash_super": "super.img",
        "oppo_flash_custom": "Custom Partition",
        "oppo_partition": "Partition:",
        "oppo_image": "Image:",
        "oppo_unlock_help": "Unlock Help",
        "oppo_download_help": "Unlock Guide",
        "oppo_unlock_cmd": "Attempt Unlock",
        "oppo_lock_cmd": "Lock",
        "oppo_select_rom": "Select ROM",
        "oppo_flash_wipe": "Flash + Wipe",
        "oppo_flash_keep": "Flash (Keep)",
        "oppo_erase_frp": "FRP",
        "oppo_wipe_data": "Wipe Data",
        "oppo_reboot_ok": "Normal",
        "root_title": "TWRP & Root",
        "root_warning": "Make sure bootloader is unlocked",
        "check_bl_status": "Check Bootloader",
        "unlock_bl": "Unlock",
        "lock_bl": "Lock",
        "flash_twrp": "TWRP",
        "flash_magisk": "Magisk",
        "select_recovery": "Select recovery.img",
        "select_boot": "Select boot patched",
        "bl_locked": "Locked",
        "bl_unlocked": "Unlocked",
        "bl_unknown": "Unknown",
        "unlock_confirm": "Data will be wiped!",
        "unlock_warn_screen": "Press Volume Up on screen",
        "flash_recovery_success": "recovery",
        "flash_boot_success": "boot",
        "reboot_recovery_after": "Reboot to Recovery",
        "download_twrp": "TWRP",
        "download_magisk": "Magisk",
        "unlock_title": "Unlock & FRP",
        "check_lock": "Check Lock",
        "check_root": "Check Root",
        "check_frp": "Check FRP",
        "remove_locksettings": "locksettings",
        "remove_gatekeeper": "gatekeeper",
        "remove_pattern": "Pattern",
        "format_data_fastboot": "Format Data",
        "erase_frp_fastboot": "FRP (FB)",
        "erase_frp_adb": "FRP (ADB)",
        "full_device_info": "Full Info",
        "unlock_warning": "At your own risk",
        "mtk_title": "mtkclient",
        "run_gui": "GUI",
        "read_gpt": "GPT",
        "read_part": "Read:",
        "read_btn": "Read",
        "write_part": "Write:",
        "pick": "Pick",
        "write_btn": "Write",
        "advanced": "Advanced",
        "unlock_bl_mtk": "MTK Unlock",
        "wipe_frp": "FRP + Userdata",
        "edl_title": "Qualcomm EDL",
        "edl_check": "Check",
        "edl_printgpt": "Partitions",
        "edl_dump": "Dump",
        "edl_load": "Load",
        "edl_rw": "R/W",
        "edl_reset": "Reset",
        "edl_wipe": "Userdata",
        "edl_firehose": "Firehose:",
        "edl_partition": "Partition:",
        "about_title": "About",
        "about_version": "Version: {}",
        "about_check_update": "Check for Updates",
        "about_download_update": "Download",
        "about_github": "GitHub",
        "about_up_to_date": "Up to date",
        "about_new_version": "New: {}",
        "about_checking": "Checking...",
        "about_error": "Error: {}",
        "about_description": "Comprehensive Android tool\n\n• ADB / Fastboot\n• Daily Tools\n• System Tools\n• Gaming Boost\n• App Manager\n• Backup\n• Flash ROM\n• Xiaomi / Huawei / Samsung / Oppo / Vivo\n• TWRP & Root\n• Unlock & FRP\n• MediaTek\n• Qualcomm EDL\n• Advanced Tools",
        "log": "Log:",
        "log_save": "Save",
        "log_copy": "Copy",
        "log_clear": "Clear",
        "log_open_folder": "Open",
        "log_saved": "Saved: {}",
        "log_copied": "Copied",
        "log_cleared": "Cleared",
        "lang_btn": "العربية",
        "msg_wait": "...",
        "msg_tools_ok": "Platform-Tools",
        "msg_tools_missing": "Platform-Tools",
        "msg_python_ok": "Python",
        "msg_python_missing": "Python",
        "msg_mtk_ok": "mtkclient",
        "msg_mtk_missing": "mtkclient",
        "msg_edl_ok": "edl",
        "msg_edl_missing": "edl",
        "msg_heimdall_ok": "Heimdall",
        "msg_heimdall_missing": "Heimdall",
        "msg_downloading_pt": "Downloading Platform-Tools...",
        "msg_installed": "Installed",
        "msg_error": "Error: {}",
        "msg_adb": "ADB",
        "msg_fastboot": "Fastboot",
        "msg_no_embed": "Python not found",
        "msg_no_mtk": "mtkclient",
        "msg_no_edl": "edl",
        "confirm_write": "Write {} to {}?",
        "confirm_unlock": "Unlock?",
        "confirm_wipe": "Wipe!",
        "confirm_format": "Format All?",
        "confirm_flash_samsung": "Flash {}?",
        "confirm_uninstall": "Uninstall {}?",
        "confirm_disable": "Disable {}?",
        "confirm_clear": "Clear data for {}?",
        "confirm_reset_dpi": "Reset DPI to default?",
        "confirm_sysui": "Restart SystemUI?",
        "confirm_reboot": "Reboot phone?",
        "err_check": "Check",
        "err": "Error",
        "confirm": "Confirm",
        "warn": "Warning",
        "lic_title": "Activate Software",
        "lic_desc": "Enter your activation code to start using the software",
        "lic_placeholder": "Enter code here...",
        "lic_activate": "Activate",
        "lic_error": "Invalid code",
        "lic_success": "Activated successfully",
        "lic_no_key": "Please enter the code"
    }
}

def run(cmd, timeout=60, cwd=None, env=None):
    try:
        r = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout,
            encoding="utf-8", errors="ignore", cwd=cwd, env=env,
            creationflags=NO_WINDOW
        )
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
    if name.endswith(".tar.md5") or ext in [".tar", ".md5"]:
        return "samsung_tar"
    if ext in [".tgz", ".gz"] or name.endswith(".tar.gz"):
        return "tgz"
    return "unknown"

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
        ctk.CTkButton(self, text="English / العربية", width=150, height=30,
                      fg_color="gray", command=self.toggle_lang).pack(pady=5)

    def toggle_lang(self):
        self.lang = "en" if self.lang == "ar" else "ar"
        self.t = LANG[self.lang]
        self.build_ui()

    def do_activate(self):
        key = self.entry.get().strip()
        if not key:
            self.status.configure(text=self.tr("lic_no_key"), text_color="orange")
            return
        if activate_license(key):
            self.status.configure(text=self.tr("lic_success"), text_color="lightgreen")
            self.success = True
            self.after(700, self._close)

    def _close(self):
        try:
            self.quit()
        except Exception:
            pass
        try:
            self.destroy()
        except Exception:
            pass

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
        self.oppo_rom = ""
        self.vivo_rom = ""
        self.recording = False
        self.apps_list = []
        self.apps_filtered = []
        self.selected_pkg = None
        self.selected_app_info = None
        self.about_status = None
        self.download_btn = None
        self._update_url = "https://github.com/" + GITHUB_REPO + "/releases/latest"

        self.geometry("1020x950")
        self.resizable(True, True)
        os.makedirs(LOGS_DIR, exist_ok=True)
        os.makedirs(EXPORTS_DIR, exist_ok=True)
        os.makedirs(BACKUP_DIR, exist_ok=True)
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        self.build_ui()
        self.check_tools()
        threading.Thread(target=self._bg_check_update, daemon=True).start()

    def _on_close(self):
        try:
            self.destroy()
        except Exception:
            pass

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
        if self.apps_list:
            self.apps_apply_filter()

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
            content = self.log_box.get("1.0", "end")
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            path = os.path.join(LOGS_DIR, "log_" + ts + ".txt")
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            self.log(self.tr("log_saved", path))
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
                    self.ui(self._set_status, self.tr("about_up_to_date"), "lightgreen")
            except Exception as e:
                self.ui(self._set_status, self.tr("about_error", str(e)), "red")

        threading.Thread(target=t, daemon=True).start()

    def _set_status(self, text, color):
        if self.about_status is not None:
            try:
                self.about_status.configure(text=text, text_color=color)
            except Exception:
                pass

    def open_update_page(self):
        webbrowser.open(self._update_url)

    def open_github(self):
        webbrowser.open("https://github.com/" + GITHUB_REPO)

    def build_about_tab(self):
        f = self.tab_about
        ctk.CTkLabel(f, text=self.tr("about_title"), font=("Arial", 18, "bold")).pack(pady=15)
        ctk.CTkLabel(f, text=self.tr("about_version", APP_VERSION), font=("Arial", 14)).pack(pady=6)
        ctk.CTkLabel(f, text=self.tr("about_description"), font=("Arial", 12),
                     justify="center").pack(pady=15)
        self.about_status = ctk.CTkLabel(f, text="", font=("Arial", 12))
        self.about_status.pack(pady=5)
        bf = ctk.CTkFrame(f)
        bf.pack(pady=15)
        ctk.CTkButton(bf, text=self.tr("about_check_update"), width=200, height=40,
                      command=self.check_update).pack(side="left", padx=5)
        self.download_btn = ctk.CTkButton(bf, text=self.tr("about_download_update"),
                                          width=200, height=40, fg_color="green",
                                          hover_color="darkgreen", state="disabled",
                                          command=self.open_update_page)
        self.download_btn.pack(side="left", padx=5)
        ctk.CTkButton(f, text=self.tr("about_github"), width=300, height=40,
                      command=self.open_github).pack(pady=10)

    def build_guide_tab(self):
        f = self.tab_guide
        ctk.CTkLabel(f, text=self.tr("guide_title"), font=("Arial", 18, "bold")).pack(pady=15)
        guide_frame = ctk.CTkScrollableFrame(f, width=900, height=600)
        guide_frame.pack(fill="both", expand=True, padx=10, pady=5)
        ctk.CTkLabel(guide_frame,
                     text="Welcome!\nThis is the built-in guide. Use the tabs to explore features.",
                     font=("Arial", 13), justify="right", wraplength=850).pack(padx=20, pady=10, anchor="e")

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
            ctk.CTkButton(f, text=t, width=210, height=36, command=fn).grid(
                row=i // 3, column=i % 3, padx=8, pady=8)

    def build_tools_tab(self):
        f = self.tab_tools
        ctk.CTkLabel(f, text=self.tr("tools_title"), font=("Arial", 16, "bold")).pack(pady=10)
        ctk.CTkButton(f, text=self.tr("tools_screenshot"), width=350, height=50,
                      fg_color="green", hover_color="darkgreen",
                      font=("Arial", 14, "bold"),
                      command=self.tool_screenshot).pack(pady=5)
        rec_frame = ctk.CTkFrame(f)
        rec_frame.pack(pady=5)
        ctk.CTkButton(rec_frame, text=self.tr("tools_record"), width=250, height=45,
                      fg_color="orange", hover_color="darkorange",
                      command=self.tool_record).pack(side="left", padx=5)
        ctk.CTkButton(rec_frame, text=self.tr("tools_record_stop"), width=200, height=45,
                      fg_color="red", hover_color="darkred",
                      command=self.tool_record_stop).pack(side="left", padx=5)
        ctk.CTkButton(f, text=self.tr("tools_install_apk"), width=350, height=50,
                      fg_color="green", hover_color="darkgreen",
                      font=("Arial", 14, "bold"),
                      command=self.tool_install_apk).pack(pady=5)
        pf = ctk.CTkFrame(f)
        pf.pack(pady=5)
        ctk.CTkButton(pf, text=self.tr("tools_push"), width=170, height=45,
                      command=self.tool_push).pack(side="left", padx=5)
        ctk.CTkButton(pf, text=self.tr("tools_pull"), width=170, height=45,
                      command=self.tool_pull).pack(side="left", padx=5)
        info_frame = ctk.CTkFrame(f)
        info_frame.pack(pady=5)
        ctk.CTkButton(info_frame, text=self.tr("tools_battery"), width=170, height=45,
                      command=self.tool_battery).pack(side="left", padx=5)
        ctk.CTkButton(info_frame, text=self.tr("tools_export_dir"), width=170, height=45,
                      command=self.open_exports).pack(side="left", padx=5)

    def tool_screenshot(self):
        self.log("جاري أخذ لقطة شاشة...")
        def t():
            res = run([ADB, "shell", "screencap", "-p", "/sdcard/screen.png"])
            if "Error" in res or "no devices" in res.lower():
                self.log(self.tr("tools_no_device"))
                return
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            path = os.path.join(EXPORTS_DIR, f"screenshot_{ts}.png")
            run([ADB, "pull", "/sdcard/screen.png", path])
            run([ADB, "shell", "rm", "/sdcard/screen.png"])
            self.log(self.tr("tools_screenshot_saved", path))
        threading.Thread(target=t, daemon=True).start()

    def tool_record(self):
        if self.recording:
            self.log("التسجيل قيد التشغيل بالفعل.")
            return
        self.recording = True
        self.log(self.tr("tools_recording"))
        def t():
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            remote_path = "/sdcard/rec.mp4"
            run([ADB, "shell", "screenrecord", "--time-limit", "15", remote_path], timeout=20)
            path = os.path.join(EXPORTS_DIR, f"record_{ts}.mp4")
            run([ADB, "pull", remote_path, path])
            run([ADB, "shell", "rm", remote_path])
            self.recording = False
            self.log(self.tr("tools_recorded", path))
        threading.Thread(target=t, daemon=True).start()

    def tool_record_stop(self):
        if not self.recording:
            return
        run([ADB, "shell", "pkill", "-l", "SIGINT", "screenrecord"])
        self.log("تم إيقاف التسجيل.")

    def tool_install_apk(self):
        path = filedialog.askopenfilename(filetypes=[("APK", "*.apk")])
        if not path:
            return
        self.log(f"جاري تثبيت: {path}")
        def t():
            res = run([ADB, "install", "-r", path], timeout=120)
            if "Success" in res:
                self.log(self.tr("tools_install_success", os.path.basename(path)))
            else:
                self.log(self.tr("tools_install_fail", res))
        threading.Thread(target=t, daemon=True).start()

    def tool_push(self):
        path = filedialog.askopenfilename()
        if not path:
            return
        self.log(f"جاري إرسال: {path}")
        def t():
            res = run([ADB, "push", path, "/sdcard/"], timeout=120)
            self.log(res)
        threading.Thread(target=t, daemon=True).start()

    def tool_pull(self):
        remote = ctk.CTkInputDialog(text="أدخل مسار الملف في الهاتف:", title="Pull").get_input()
        if not remote:
            return
        self.log(f"جاري سحب: {remote}")
        def t():
            res = run([ADB, "pull", remote, EXPORTS_DIR], timeout=120)
            self.log(res)
        threading.Thread(target=t, daemon=True).start()

    def tool_battery(self):
        self.log(self.tr("tools_battery_info"))
        def t():
            res = run([ADB, "shell", "dumpsys", "battery"])
            self.log(res)
        threading.Thread(target=t, daemon=True).start()

    def build_system_tab(self):
        f = self.tab_system
        ctk.CTkLabel(f, text=self.tr("sys_title"), font=("Arial", 16, "bold")).pack(pady=10)
        ctk.CTkButton(f, text=self.tr("sys_nav_hide"), width=300, height=40, command=lambda: self.async_run(lambda: run([ADB, "shell", "settings", "put", "global", "policy_control", "immersive.full=*"]))).pack(pady=5)
        ctk.CTkButton(f, text=self.tr("sys_nav_show"), width=300, height=40, command=lambda: self.async_run(lambda: run([ADB, "shell", "settings", "put", "global", "policy_control", "null"]))).pack(pady=5)
        ctk.CTkButton(f, text=self.tr("sys_dpi_apply"), width=300, height=40, command=self.sys_dpi_apply).pack(pady=5)
        ctk.CTkButton(f, text=self.tr("sys_dpi_reset"), width=300, height=40, command=lambda: self.async_run(lambda: run([ADB, "shell", "wm", "density", "reset"]))).pack(pady=5)
        ctk.CTkButton(f, text=self.tr("sys_sysui"), width=300, height=40, command=lambda: self.async_run(lambda: run([ADB, "shell", "pkill", "com.android.systemui"]))).pack(pady=5)
        ctk.CTkButton(f, text=self.tr("sys_gms_disable"), width=300, height=40, command=lambda: self.async_run(lambda: run([ADB, "shell", "pm", "disable-user", "--user", "0", "com.google.android.gms"]))).pack(pady=5)
        ctk.CTkButton(f, text=self.tr("sys_gms_enable"), width=300, height=40, command=lambda: self.async_run(lambda: run([ADB, "shell", "pm", "enable", "com.google.android.gms"]))).pack(pady=5)
        ctk.CTkButton(f, text=self.tr("sys_restart"), width=300, height=40, fg_color="red", command=lambda: self.async_run(lambda: run([ADB, "reboot"]))).pack(pady=5)

    def sys_dpi_apply(self):
        val = ctk.CTkInputDialog(text="أدخل قيمة DPI (مثلاً 420):", title="DPI").get_input()
        if val and val.isdigit():
            self.async_run(lambda: run([ADB, "shell", "wm", "density", val]))

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
            self.log("تم تفعيل وضع الألعاب.")
        threading.Thread(target=t, daemon=True).start()

    def build_apps_tab(self):
        f = self.tab_apps
        ctk.CTkLabel(f, text=self.tr("apps_title"), font=("Arial", 16, "bold")).pack(pady=5)
        
        top_frame = ctk.CTkFrame(f)
        top_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkButton(top_frame, text=self.tr("apps_load"), width=150, command=self.apps_load).pack(side="left", padx=5)
        
        self.apps_filter_var = ctk.StringVar(value="all")
        ctk.CTkOptionMenu(top_frame, values=["all", "user", "system"], variable=self.apps_filter_var, command=lambda _: self.apps_apply_filter()).pack(side="left", padx=5)
        
        self.apps_count_label = ctk.CTkLabel(top_frame, text="")
        self.apps_count_label.pack(side="right", padx=5)
        
        self.apps_listbox = ctk.CTkScrollableFrame(f, width=800, height=300)
        self.apps_listbox.pack(fill="both", expand=True, padx=10, pady=5)
        
        btn_frame = ctk.CTkFrame(f)
        btn_frame.pack(pady=5)
        ctk.CTkButton(btn_frame, text=self.tr("apps_uninstall"), fg_color="red", command=lambda: self.apps_action("uninstall")).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text=self.tr("apps_extract"), fg_color="green", command=lambda: self.apps_action("extract")).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text=self.tr("apps_clear"), command=lambda: self.apps_action("clear")).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text=self.tr("apps_force_stop"), fg_color="orange", command=lambda: self.apps_action("stop")).pack(side="left", padx=5)

    def apps_load(self):
        self.log(self.tr("apps_loading"))
        def t():
            res = run([ADB, "shell", "pm", "list", "packages", "-f"])
            if "Error" in res or "no devices" in res.lower():
                self.log(self.tr("apps_no_device"))
                return
            self.apps_list = []
            for line in res.splitlines():
                if line.startswith("package:"):
                    parts = line.split("=")
                    if len(parts) == 2:
                        path = parts[0].replace("package:", "")
                        pkg = parts[1]
                        self.apps_list.append({"pkg": pkg, "path": path})
            self.ui(self.apps_apply_filter)
        threading.Thread(target=t, daemon=True).start()

    def apps_apply_filter(self):
        for w in self.apps_listbox.winfo_children():
            w.destroy()
        self.apps_filtered = self.apps_list
        self.apps_count_label.configure(text=self.tr("apps_count", len(self.apps_filtered)))
        for i, app in enumerate(self.apps_filtered[:200]):
            btn = ctk.CTkButton(self.apps_listbox, text=app["pkg"], anchor="w", fg_color="transparent", text_color="white", command=lambda p=app["pkg"]: self.apps_select(p))
            btn.pack(fill="x", pady=1)

    def apps_select(self, pkg):
        self.selected_pkg = pkg
        self.log(f"تم اختيار: {pkg}")

    def apps_action(self, action):
        if not self.selected_pkg:
            self.log("الرجاء اختيار تطبيق أولاً")
            return
        pkg = self.selected_pkg
        def t():
            if action == "uninstall":
                run([ADB, "shell", "pm", "uninstall", "--user", "0", pkg])
                self.log(self.tr("apps_uninstall_ok", pkg))
            elif action == "clear":
                run([ADB, "shell", "pm", "clear", pkg])
                self.log(self.tr("apps_clear_ok", pkg))
            elif action == "stop":
                run([ADB, "shell", "am", "force-stop", pkg])
                self.log(self.tr("apps_stop_ok", pkg))
            elif action == "extract":
                path = None
                for a in self.apps_list:
                    if a["pkg"] == pkg:
                        path = a["path"]
                        break
                if path:
                    run([ADB, "pull", path, EXPORTS_DIR])
                    self.log(self.tr("apps_extract_ok", pkg))
        threading.Thread(target=t, daemon=True).start()

    def build_backup_tab(self):
        f = self.tab_backup
        ctk.CTkLabel(f, text=self.tr("backup_title"), font=("Arial", 16, "bold")).pack(pady=10)
        ctk.CTkButton(f, text=self.tr("backup_full"), width=300, height=40, command=self.backup_full).pack(pady=5)
        ctk.CTkButton(f, text=self.tr("backup_sdcard"), width=300, height=40, command=self.backup_sdcard).pack(pady=5)
        ctk.CTkButton(f, text=self.tr("backup_open"), width=300, height=40, command=self.open_backups).pack(pady=5)

    def backup_full(self):
        self.log(self.tr("backup_starting"))
        def t():
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            path = os.path.join(BACKUP_DIR, f"backup_{ts}.ab")
            res = run([ADB, "backup", "-apk", "-all", "-f", path], timeout=600)
            self.log(self.tr("backup_done", path))
        threading.Thread(target=t, daemon=True).start()

    def backup_sdcard(self):
        def t():
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            dest = os.path.join(BACKUP_DIR, f"sdcard_{ts}")
            os.makedirs(dest, exist_ok=True)
            res = run([ADB, "pull", "/sdcard/", dest], timeout=1800)
            self.log(self.tr("backup_sdcard_done", dest))
        threading.Thread(target=t, daemon=True).start()

    def build_flash_tab(self):
        f = self.tab_flash
        ctk.CTkLabel(f, text=self.tr("flash_title"), font=("Arial", 16, "bold")).pack(pady=10)
        ctk.CTkButton(f, text=self.tr("flash_select_zip"), width=300, height=40, command=self.flash_select_file).pack(pady=5)
        self.flash_label = ctk.CTkLabel(f, text="لم يتم اختيار ملف")
        self.flash_label.pack(pady=5)
        ctk.CTkButton(f, text=self.tr("flash_start"), width=300, height=40, fg_color="green", command=self.flash_start).pack(pady=10)
        self.flash_progress = ctk.CTkProgressBar(f, width=400)
        self.flash_progress.pack(pady=10)
        self.flash_progress.set(0)

    def flash_select_file(self):
        path = filedialog.askopenfilename(filetypes=[("ROM", "*.zip *.tgz *.tar *.tar.md5")])
        if path:
            self.flash_file = path
            self.flash_rom_type = detect_rom_type(path)
            self.flash_label.configure(text=os.path.basename(path) + f" ({self.flash_rom_type})")

    def flash_start(self):
        if not self.flash_file:
            self.log("الرجاء اختيار ملف الروم أولاً")
            return
        self.log(f"بدء فلاش: {self.flash_file}")
        self.flash_progress.set(0.1)
        def t():
            time.sleep(2)
            self.ui(self.flash_progress.set, 0.5)
            time.sleep(2)
            self.ui(self.flash_progress.set, 1.0)
            self.log("اكتمل الفلاش (وهمي للتجربة)")
        threading.Thread(target=t, daemon=True).start()

    def build_xiaomi_tab(self):
        f = self.tab_xiaomi
        ctk.CTkLabel(f, text=self.tr("xiaomi_title"), font=("Arial", 16, "bold")).pack(pady=10)
        ctk.CTkButton(f, text=self.tr("xiaomi_info"), width=250, height=40, command=lambda: self.async_run(lambda: run([FASTBOOT, "getvar", "all"]))).pack(pady=5)
        ctk.CTkButton(f, text=self.tr("xiaomi_reboot_fastboot"), width=250, height=40, command=lambda: self.async_run(lambda: run([ADB, "reboot", "bootloader"]))).pack(pady=5)
        ctk.CTkButton(f, text=self.tr("xiaomi_reboot_recovery"), width=250, height=40, command=lambda: self.async_run(lambda: run([ADB, "reboot", "recovery"]))).pack(pady=5)

    def build_huawei_tab(self):
        f = self.tab_huawei
        ctk.CTkLabel(f, text=self.tr("huawei_title"), font=("Arial", 16, "bold")).pack(pady=10)
        ctk.CTkButton(f, text=self.tr("huawei_info"), width=250, height=40, command=lambda: self.async_run(lambda: run([FASTBOOT, "getvar", "all"]))).pack(pady=5)
        ctk.CTkButton(f, text=self.tr("huawei_fastboot"), width=250, height=40, command=lambda: self.async_run(lambda: run([ADB, "reboot", "bootloader"]))).pack(pady=5)
        ctk.CTkButton(f, text=self.tr("huawei_recovery"), width=250, height=40, command=lambda: self.async_run(lambda: run([ADB, "reboot", "recovery"]))).pack(pady=5)

    def build_samsung_tab(self):
        f = self.tab_samsung
        ctk.CTkLabel(f, text=self.tr("samsung_title"), font=("Arial", 16, "bold")).pack(pady=10)
        ctk.CTkButton(f, text=self.tr("samsung_detect"), width=250, height=40, command=lambda: self.async_run(lambda: run([HEIMDALL, "detect"]))).pack(pady=5)
        ctk.CTkButton(f, text=self.tr("samsung_reboot"), width=250, height=40, command=lambda: self.async_run(lambda: run([ADB, "reboot"]))).pack(pady=5)
        ctk.CTkLabel(f, text=self.tr("samsung_warning"), text_color="orange").pack(pady=5)

    def build_oppo_tab(self):
        f = self.tab_oppo
        ctk.CTkLabel(f, text=self.tr("oppo_title"), font=("Arial", 16, "bold")).pack(pady=10)
        ctk.CTkButton(f, text=self.tr("oppo_info"), width=250, height=40, command=lambda: self.async_run(lambda: run([FASTBOOT, "getvar", "all"]))).pack(pady=5)
        ctk.CTkButton(f, text=self.tr("oppo_fastboot"), width=250, height=40, command=lambda: self.async_run(lambda: run([ADB, "reboot", "bootloader"]))).pack(pady=5)
        ctk.CTkButton(f, text=self.tr("oppo_recovery"), width=250, height=40, command=lambda: self.async_run(lambda: run([ADB, "reboot", "recovery"]))).pack(pady=5)

    def build_vivo_tab(self):
        f = self.tab_vivo
        ctk.CTkLabel(f, text=self.tr("vivo_title"), font=("Arial", 16, "bold")).pack(pady=10)
        ctk.CTkButton(f, text=self.tr("vivo_info"), width=250, height=40, command=lambda: self.async_run(lambda: run([FASTBOOT, "getvar", "all"]))).pack(pady=5)
        ctk.CTkButton(f, text=self.tr("vivo_fastboot"), width=250, height=40, command=lambda: self.async_run(lambda: run([ADB, "reboot", "bootloader"]))).pack(pady=5)
        ctk.CTkButton(f, text=self.tr("vivo_recovery"), width=250, height=40, command=lambda: self.async_run(lambda: run([ADB, "reboot", "recovery"]))).pack(pady=5)

    def build_root_tab(self):
        f = self.tab_root
        ctk.CTkLabel(f, text=self.tr("root_title"), font=("Arial", 16, "bold")).pack(pady=10)
        ctk.CTkButton(f, text=self.tr("check_bl_status"), width=250, height=40, command=self.check_bl).pack(pady=5)
        ctk.CTkButton(f, text=self.tr("unlock_bl"), width=250, height=40, fg_color="red", command=lambda: self.async_run(lambda: run([FASTBOOT, "flashing", "unlock"]))).pack(pady=5)
        ctk.CTkButton(f, text=self.tr("flash_twrp"), width=250, height=40, command=self.flash_twrp).pack(pady=5)
        ctk.CTkButton(f, text=self.tr("flash_magisk"), width=250, height=40, command=self.flash_magisk).pack(pady=5)

    def check_bl(self):
        def t():
            res = run([FASTBOOT, "getvar", "unlocked"])
            self.log(res)
        threading.Thread(target=t, daemon=True).start()

    def flash_twrp(self):
        path = filedialog.askopenfilename(filetypes=[("IMG", "*.img")])
        if path:
            self.async_run(lambda: run([FASTBOOT, "flash", "recovery", path]))

    def flash_magisk(self):
        path = filedialog.askopenfilename(filetypes=[("IMG", "*.img")])
        if path:
            self.async_run(lambda: run([FASTBOOT, "flash", "boot", path]))

    def build_unlock_tab(self):
        f = self.tab_unlock
        ctk.CTkLabel(f, text=self.tr("unlock_title"), font=("Arial", 16, "bold")).pack(pady=10)
        ctk.CTkButton(f, text=self.tr("erase_frp_fastboot"), width=250, height=40, command=lambda: self.async_run(lambda: run([FASTBOOT, "erase", "frp"]))).pack(pady=5)
        ctk.CTkButton(f, text=self.tr("format_data_fastboot"), width=250, height=40, fg_color="red", command=lambda: self.async_run(lambda: run([FASTBOOT, "erase", "userdata"]))).pack(pady=5)
        ctk.CTkButton(f, text=self.tr("full_device_info"), width=250, height=40, command=lambda: self.async_run(lambda: run([ADB, "shell", "getprop"]))).pack(pady=5)

    def build_mtk_tab(self):
        f = self.tab_mtk
        ctk.CTkLabel(f, text=self.tr("mtk_title"), font=("Arial", 16, "bold")).pack(pady=10)
        ctk.CTkButton(f, text=self.tr("run_gui"), width=250, height=40, command=lambda: self.run_mtk_script()).pack(pady=5)
        ctk.CTkButton(f, text=self.tr("read_gpt"), width=250, height=40, command=lambda: self.run_mtk_script("r", "gpt")).pack(pady=5)
        ctk.CTkButton(f, text=self.tr("unlock_bl_mtk"), width=250, height=40, fg_color="red", command=lambda: self.run_mtk_script("e", "metadata")).pack(pady=5)

    def run_mtk_script(self, *args):
        if not os.path.exists(MTK_SCRIPT):
            self.log("mtkclient غير موجود")
            return
        cmd = [sys.executable, MTK_SCRIPT] + list(args)
        def t():
            res = run(cmd, timeout=300)
            self.log(res)
        threading.Thread(target=t, daemon=True).start()

    def build_edl_tab(self):
        f = self.tab_edl
        ctk.CTkLabel(f, text=self.tr("edl_title"), font=("Arial", 16, "bold")).pack(pady=10)
        ctk.CTkButton(f, text=self.tr("edl_printgpt"), width=250, height=40, command=self.edl_printgpt).pack(pady=5)
        ctk.CTkButton(f, text=self.tr("edl_reset"), width=250, height=40, command=self.edl_reset).pack(pady=5)

    def edl_printgpt(self):
        if not os.path.exists(EDL_SCRIPT):
            self.log("edl غير موجود")
            return
        def t():
            res = run([sys.executable, EDL_SCRIPT, "printgpt"], timeout=120)
            self.log(res)
        threading.Thread(target=t, daemon=True).start()

    def edl_reset(self):
        if not os.path.exists(EDL_SCRIPT):
            self.log("edl غير موجود")
            return
        def t():
            res = run([sys.executable, EDL_SCRIPT, "reset"], timeout=120)
            self.log(res)
        threading.Thread(target=t, daemon=True).start()

    def build_adv_tab(self):
        f = self.tab_adv
        ctk.CTkLabel(f, text=self.tr("adv_title"), font=("Arial", 16, "bold")).pack(pady=10)
        ctk.CTkButton(f, text=self.tr("adv_adb_terminal"), width=350, height=40, command=self.adv_adb_terminal).pack(pady=5)
        ctk.CTkButton(f, text=self.tr("adv_install_batch"), width=350, height=40, command=self.adv_install_batch).pack(pady=5)
        ctk.CTkButton(f, text=self.tr("adv_network_info"), width=350, height=40, command=lambda: self.async_run(lambda: run([ADB, "shell", "ifconfig"]))).pack(pady=5)
        ctk.CTkButton(f, text=self.tr("adv_device_props"), width=350, height=40, command=lambda: self.async_run(lambda: run([ADB, "shell", "getprop"]))).pack(pady=5)

    def adv_adb_terminal(self):
        cmd = ctk.CTkInputDialog(text="أدخل أمر ADB:", title="ADB Terminal").get_input()
        if cmd:
            self.log(f"> adb {cmd}")
            def t():
                res = run([ADB] + cmd.split())
                self.log(res)
            threading.Thread(target=t, daemon=True).start()

    def adv_install_batch(self):
        folder = filedialog.askdirectory()
        if folder:
            apks = [f for f in os.listdir(folder) if f.endswith(".apk")]
            def t():
                for apk in apks:
                    path = os.path.join(folder, apk)
                    self.log(f"تثبيت: {apk}")
                    run([ADB, "install", "-r", path], timeout=120)
            threading.Thread(target=t, daemon=True).start()

    def async_run(self, fn, *args):
        def wrapper():
            try:
                res = fn(*args)
                if res:
                    self.log(res)
            except Exception as e:
                self.log(f"Error: {e}")
        threading.Thread(target=wrapper, daemon=True).start()

    def download_tools(self):
        self.log(self.tr("msg_downloading_pt"))
        def t():
            try:
                zip_path = os.path.join(BASE_DIR, "platform-tools.zip")
                urllib.request.urlretrieve(PLATFORM_TOOLS_URL, zip_path)
                with zipfile.ZipFile(zip_path) as z:
                    z.extractall(BASE_DIR)
                os.remove(zip_path)
                self.log(self.tr("msg_installed"))
            except Exception as e:
                self.log(self.tr("msg_error", e))
        threading.Thread(target=t, daemon=True).start()

    def detect(self):
        self.async_run(lambda: run([ADB, "devices"]))

    def info(self):
        self.async_run(lambda: run([ADB, "shell", "getprop"]))

    def check_tools(self):
        self.log("--- فحص الأدوات ---")
        self.log(f"ADB: {'موجود' if os.path.exists(ADB) else 'غير موجود'}")
        self.log(f"Fastboot: {'موجود' if os.path.exists(FASTBOOT) else 'غير موجود'}")
        self.log(f"MTK: {'موجود' if os.path.exists(MTK_SCRIPT) else 'غير موجود'}")
        self.log(f"EDL: {'موجود' if os.path.exists(EDL_SCRIPT) else 'غير موجود'}")
        self.log(f"Heimdall: {'موجود' if os.path.exists(HEIMDALL) else 'غير موجود'}")


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
    ctk.CTkLabel(splash, text="Version " + APP_VERSION, font=("Arial", 12), text_color="gray").pack(pady=5)
    
    bar = ctk.CTkProgressBar(splash, width=300)
    bar.pack(pady=20)
    bar.set(0)
    splash.update()
    
    for i in range(101):
        bar.set(i / 100)
        splash.update()
        time.sleep(0.02)
        
    splash.destroy()


def main():
    show_splash()
    if not is_activated():
        holder = {"app": None}

        def launch():
            holder["app"] = App()

        lic = LicenseWindow(on_success=launch)
        lic.mainloop()
        if holder["app"] is not None:
            holder["app"].mainloop()
    else:
        app = App()
        app.mainloop()


if __name__ == "__main__":
    main()