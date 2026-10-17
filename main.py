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
APP_VERSION = "1.9.0"
GITHUB_REPO = "Gissa333/android-tool"
GITHUB_API = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"

SECRET_LICENSE_KEY = "PRO-2026-ANDROID-TOOL"

LANG = {
    "ar": {
        "title": "🛠️ أداة الأندرويد",
        "tab_adb": "ADB / Fastboot",
        "tab_tools": "📸 أدوات يومية",
        "tab_system": "⚙️ أدوات النظام",
        "tab_gaming": "🎮 الألعاب والأداء",
        "tab_apps": "📱 إدارة التطبيقات",
        "tab_backup": "💾 نسخ احتياطي",
        "tab_flash": "📦 فلاش الروم",
        "tab_xiaomi": "🟠 Xiaomi",
        "tab_huawei": "🟣 Huawei",
        "tab_samsung": "📱 Samsung",
        "tab_oppo": "🟢 Oppo/Realme",
        "tab_vivo": "🔵 Vivo/iQOO",
        "tab_root": "🔓 TWRP & Root",
        "tab_unlock": "🔒 فك القفل",
        "tab_mtk": "MTK",
        "tab_edl": "Qualcomm EDL",
        "tab_adv": "🧰 أدوات متقدمة",
        "tab_about": "ℹ️ حول",
        "download_tools": "📥 تحميل Platform-Tools",
        "detect": "🔍 اكتشاف الأجهزة",
        "device_info": "📱 معلومات الجهاز",
        "reboot": "🔄 إعادة تشغيل",
        "fastboot": "⚡ وضع Fastboot",
        "reboot_recovery": "♻️ وضع Recovery",
        "reboot_edl": "📡 وضع EDL",
        "exit_fastboot": "🔌 خروج من Fastboot",
        "tools_title": "📸 أدوات يومية (ADB)",
        "tools_screenshot": "📸 لقطة شاشة",
        "tools_record": "🎬 تسجيل الشاشة (15 ثانية)",
        "tools_record_stop": "⏹️ إيقاف التسجيل",
        "tools_install_apk": "📦 تثبيت APK",
        "tools_push": "📤 إرسال ملف للهاتف",
        "tools_pull": "📥 سحب ملف من الهاتف",
        "tools_list_packages": "📋 قائمة التطبيقات",
        "tools_battery": "🔋 معلومات البطارية",
        "tools_export_dir": "📂 فتح مجلد التصدير",
        "tools_wait": "⏳ جاري...",
        "tools_recording": "🎬 جاري التسجيل... انتظر 15 ثانية",
        "tools_recorded": "✅ تم حفظ التسجيل: {}",
        "tools_screenshot_saved": "✅ تم حفظ اللقطة: {}",
        "tools_no_device": "❌ لا يوجد جهاز متصل",
        "tools_install_success": "✅ تم تثبيت: {}",
        "tools_install_fail": "❌ فشل التثبيت: {}",
        "tools_battery_info": "🔋 معلومات البطارية",
        "tools_apps_list": "📋 التطبيقات المثبتة",
        "sys_title": "⚙️ أدوات النظام المتقدمة",
        "sys_nav_hide": "🙈 إخفاء شريط التنقل",
        "sys_nav_show": "👁️ إظهار شريط التنقل",
        "sys_dpi_title": "تغيير كثافة الشاشة (DPI):",
        "sys_dpi_placeholder": "مثال: 420",
        "sys_dpi_apply": "تطبيق DPI",
        "sys_dpi_reset": "إعادة DPI الافتراضي",
        "sys_res_reset": "🔄 إعادة دقة الشاشة الافتراضية",
        "sys_anim": "🎬 تسريع الحركة (Animation):",
        "sys_anim_fast": "🚀 تسريع (0.5x)",
        "sys_anim_normal": "🔄 إعادة للوضع الطبيعي (1x)",
        "sys_anim_value": "مثال: 0.5",
        "sys_anim_apply": "تطبيق",
        "sys_sysui": "🔄 إعادة تشغيل واجهة النظام (SystemUI)",
        "sys_gms": "تعطيل/تفعيل خدمات جوجل (GMS):",
        "sys_gms_disable": "🚫 تعطيل GMS",
        "sys_gms_enable": "✅ تفعيل GMS",
        "sys_restart": "♻️ إعادة تشغيل الهاتف",
        "sys_applied": "✅ تم التطبيق",
        "sys_reset": "✅ تم إعادة القيمة الافتراضية",
        "sys_sysui_restarting": "🔄 جاري إعادة تشغيل SystemUI...",
        "sys_gms_disabled": "✅ GMS معطل",
        "sys_gms_enabled": "✅ GMS مفعل",
        "game_title": "🎮 تسريع الألعاب والأداء",
        "game_boost": "🚀 تفعيل وضع الأداء العالي (بدون روت)",
        "game_boost_desc": "يعطل خدمات الخلفية ويسرع الحركة",
        "game_normal": "🔄 إلغاء وضع الألعاب",
        "game_normal_desc": "إعادة الهاتف لوضعه الطبيعي",
        "game_fps": "عرض معدل الإطارات (FPS) الحالي:",
        "game_refresh": "🔄 إعادة تحديث المعلومات",
        "game_ram": "🧹 تنظيف الذاكرة العشوائية (RAM)",
        "game_ram_ok": "✅ تم تنظيف الذاكرة العشوائية",
        "game_cache": "🗑️ مسح الكاش (Cache) لجميع التطبيقات",
        "game_cache_ok": "✅ تم مسح الكاش",
        "game_bg": "🚫 تعطيل التطبيقات في الخلفية",
        "game_bg_ok": "✅ تم تعطيل التطبيقات في الخلفية",
        "game_bg_enable": "✅ تفعيل التطبيقات في الخلفية",
        "game_res": "تغيير دقة الشاشة للألعاب (لتسريعها):",
        "game_res_apply": "تطبيق",
        "game_res_reset": "🔄 إعادة الدقة الأصلية",
        "game_status": "⏳ جاري التنفيذ...",
        "game_info": "ملاحظة: هذه الأوامر آمنة ولا تحتاج إلى روت.",
        "adv_title": "🧰 أدوات متقدمة",
        "adv_adb_terminal": "🖥️ تشغيل أوامر ADB مخصصة",
        "adv_adb_terminal_desc": "اكتب أمر adb shell ونفذه مباشرة على الهاتف",
        "adv_install_batch": "📦 تثبيت ملفات APK دفعة واحدة",
        "adv_install_batch_desc": "اختر مجلداً لتثبيت جميع ملفات APK بداخله",
        "adv_battery_calib": "🔋 معايرة البطارية",
        "adv_battery_calib_desc": "مسح ملف batterystats.bin (يتطلب روت)",
        "adv_network_info": "📡 معلومات الشبكة",
        "adv_network_info_desc": "عرض IP وحالة الواي فاي والشبكة",
        "adv_hide_app": "🔐 إخفاء تطبيق",
        "adv_hide_app_desc": "إخفاء تطبيق من قائمة التطبيقات",
        "adv_show_app": "👁️ إظهار تطبيق مخفي",
        "adv_show_app_desc": "إعادة إظهار تطبيق تم إخفاؤه",
        "adv_fastboot_info": "📊 معلومات Fastboot",
        "adv_fastboot_info_desc": "عرض متغيرات Fastboot كاملة",
        "adv_reboot_bootloader": "⚡ إعادة تشغيل إلى Fastboot",
        "adv_reboot_bootloader_desc": "نقل الهاتف إلى وضع Fastboot",
        "adv_reboot_recovery": "♻️ إعادة تشغيل إلى Recovery",
        "adv_reboot_recovery_desc": "نقل الهاتف إلى وضع Recovery",
        "adv_reboot_download": "📥 إعادة تشغيل إلى Download Mode",
        "adv_reboot_download_desc": "أجهزة سامسونج - Download Mode",
        "adv_device_props": "📋 خصائص النظام الكاملة",
        "adv_device_props_desc": "عرض getprop كامل",
        "adv_wait": "⏳ جاري التنفيذ...",
        "adv_done": "✅ تم",
        "adv_no_input": "⚠️ الرجاء إدخال أمر",
        "adv_adb_prompt": "أدخل أمر ADB (مثال: shell getprop):",
        "adv_adb_result": "نتيجة الأمر:",
        "adv_pick_folder": "📁 اختر مجلد APK",
        "adv_installing": "⏳ تثبيت: {}",
        "adv_install_count": "✅ تم تثبيت {} تطبيق",
        "adv_no_apk": "⚠️ لا توجد ملفات APK في المجلد",
        "adv_battery_warn": "⚠️ هذه العملية تتطلب روت. متأكد؟",
        "adv_battery_done": "✅ تم مسح إحصائيات البطارية. أعد تشغيل الهاتف.",
        "adv_network_loading": "⏳ جاري جلب معلومات الشبكة...",
        "adv_hide_app_prompt": "أدخل اسم الحزمة (Package Name):",
        "adv_app_hidden": "✅ تم إخفاء {}",
        "adv_app_shown": "✅ تم إظهار {}",
        "adv_fastboot_info_loading": "⏳ جاري جلب معلومات Fastboot...",
        "adv_device_props_loading": "⏳ جاري جلب الخصائص...",
        "apps_title": "📱 إدارة التطبيقات",
        "apps_load": "📋 تحميل قائمة التطبيقات",
        "apps_uninstall": "🗑️ حذف التطبيق",
        "apps_disable": "🚫 تعطيل",
        "apps_enable": "✅ تفعيل",
        "apps_extract": "📤 استخراج APK",
        "apps_clear": "🧹 مسح البيانات",
        "apps_force_stop": "⛔ إيقاف",
        "apps_filter": "فلتر:",
        "apps_filter_all": "الكل",
        "apps_filter_user": "المستخدم فقط",
        "apps_filter_system": "النظام فقط",
        "apps_count": "📊 {} تطبيق",
        "apps_select": "اختر تطبيقاً من القائمة:",
        "apps_loading": "⏳ جاري تحميل قائمة التطبيقات...",
        "apps_loaded": "✅ تم تحميل {} تطبيق",
        "apps_no_device": "❌ لا يوجد جهاز متصل",
        "apps_no_packages": "⚠️ لا توجد تطبيقات",
        "apps_uninstall_ok": "✅ تم حذف {}",
        "apps_uninstall_fail": "❌ فشل حذف {}",
        "apps_disable_ok": "✅ تم تعطيل {}",
        "apps_enable_ok": "✅ تم تفعيل {}",
        "apps_extract_ok": "✅ تم استخراج {}",
        "apps_clear_ok": "✅ تم مسح بيانات {}",
        "apps_stop_ok": "✅ تم إيقاف {}",
        "backup_title": "💾 النسخ الاحتياطي والاستعادة",
        "backup_full": "📦 نسخ احتياطي كامل (Apps + Data)",
        "backup_app": "📱 نسخ احتياطي لتطبيق محدد",
        "backup_sdcard": "📂 نسخ بطاقة SD كاملة",
        "backup_restore": "♻️ استعادة نسخة احتياطية",
        "backup_open": "📂 فتح مجلد النسخ الاحتياطي",
        "backup_warning": "⚠️ النسخ الاحتياطي الكامل يتطلب تأكيد من شاشة الهاتف",
        "backup_no_device": "❌ لا يوجد جهاز متصل",
        "backup_starting": "⏳ بدء النسخ الاحتياطي...",
        "backup_confirm_phone": "⚠️ اضغط 'Back up my data' على شاشة الهاتف",
        "backup_done": "✅ اكتمل النسخ الاحتياطي: {}",
        "backup_fail": "❌ فشل النسخ الاحتياطي",
        "backup_select_file": "اختر ملف .ab للاستعادة",
        "backup_restore_done": "✅ تم بدء الاستعادة - اضغط Restore على الهاتف",
        "backup_sdcard_done": "✅ تم نسخ SD: {}",
        "backup_sdcard_fail": "❌ فشل نسخ SD",
        "backup_app_placeholder": "com.example.app",
        "backup_app_prompt": "أدخل اسم الحزمة (Package Name):",
        "vivo_title": "🔵 Vivo / iQOO",
        "vivo_warning": "⚠️ Funtouch OS / OriginOS",
        "vivo_info": "📱 معلومات الجهاز",
        "vivo_check_bl": "🔍 فحص البوتلودر",
        "vivo_fastboot": "⚡ Fastboot",
        "vivo_recovery": "♻️ Recovery",
        "vivo_edl": "📡 EDL",
        "vivo_flash_boot": "📦 boot.img",
        "vivo_flash_recovery": "📦 recovery.img",
        "vivo_flash_vbmeta": "📦 vbmeta.img",
        "vivo_flash_dtbo": "📦 dtbo.img",
        "vivo_flash_super": "📦 super.img",
        "vivo_flash_custom": "⚙️ قسم مخصص",
        "vivo_partition": "القسم:",
        "vivo_image": "الصورة:",
        "vivo_unlock_help": "🔓 مساعدة الفتح",
        "vivo_download_help": "🌐 دليل الفتح",
        "vivo_unlock_cmd": "🔓 محاولة فتح",
        "vivo_lock_cmd": "🔒 قفل",
        "vivo_flash_rom": "📦 فلاش ROM",
        "vivo_select_rom": "اختر ROM",
        "vivo_flash_wipe": "🚀 فلاش + Wipe",
        "vivo_flash_keep": "🚀 فلاش (Keep)",
        "vivo_erase_frp": "🚫 FRP",
        "vivo_wipe_data": "🧹 محو البيانات",
        "vivo_reboot_ok": "🔄 عادي",
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
        "huawei_title": "🟣 Huawei / Honor",
        "huawei_warning": "⚠️ الأجهزة الحديثة محمية بـ Huawei ID",
        "huawei_info": "📱 معلومات الجهاز",
        "huawei_fastboot": "⚡ Fastboot",
        "huawei_recovery": "♻️ Recovery",
        "huawei_erecovery": "🔄 eRecovery",
        "huawei_flash_boot": "📦 boot.img",
        "huawei_flash_recovery": "📦 recovery.img",
        "huawei_flash_system": "📦 system.img",
        "huawei_flash_ramdisk": "📦 ramdisk.img",
        "huawei_flash_custom": "⚙️ قسم مخصص",
        "huawei_partition": "القسم:",
        "huawei_image": "الصورة:",
        "huawei_unlock_help": "🔓 مساعدة الفتح",
        "huawei_hisuite": "🌐 HiSuite",
        "huawei_erecovery_help": "📖 دليل eRecovery",
        "huawei_check_bl": "🔍 فحص البوتلودر",
        "huawei_unlock_code": "🔑 فتح بكود",
        "huawei_erase_frp": "🚫 FRP",
        "huawei_wipe_data": "🧹 محو",
        "huawei_reboot_ok": "🔄 عادي",
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
        "oppo_title": "🟢 Oppo / Realme / OnePlus",
        "oppo_warning": "⚠️ ColorOS / OxygenOS",
        "oppo_info": "📱 معلومات الجهاز",
        "oppo_check_bl": "🔍 فحص البوتلودر",
        "oppo_fastboot": "⚡ Fastboot",
        "oppo_recovery": "♻️ Recovery",
        "oppo_edl": "📡 EDL",
        "oppo_flash_boot": "📦 boot.img",
        "oppo_flash_recovery": "📦 recovery.img",
        "oppo_flash_vbmeta": "📦 vbmeta.img",
        "oppo_flash_dtbo": "📦 dtbo.img",
        "oppo_flash_super": "📦 super.img",
        "oppo_flash_custom": "⚙️ قسم مخصص",
        "oppo_partition": "القسم:",
        "oppo_image": "الصورة:",
        "oppo_unlock_help": "🔓 مساعدة الفتح",
        "oppo_download_help": "🌐 دليل الفتح",
        "oppo_unlock_cmd": "🔓 محاولة فتح",
        "oppo_lock_cmd": "🔒 قفل",
        "oppo_flash_rom": "📦 فلاش ROM",
        "oppo_select_rom": "اختر ROM",
        "oppo_flash_wipe": "🚀 فلاش + Wipe",
        "oppo_flash_keep": "🚀 فلاش (Keep)",
        "oppo_erase_frp": "🚫 FRP",
        "oppo_wipe_data": "🧹 محو البيانات",
        "oppo_reboot_ok": "🔄 عادي",
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
        "about_title": "ℹ️ حول",
        "about_version": "الإصدار: {}",
        "about_check_update": "🔄 فحص التحديثات",
        "about_download_update": "📥 تحميل",
        "about_github": "🌐 GitHub",
        "about_up_to_date": "✅ أحدث إصدار",
        "about_new_version": "🎉 جديد: {}",
        "about_checking": "⏳ فحص...",
        "about_error": "❌ {}",
        "about_description": "أداة شاملة لهواتف أندرويد\n\n• ADB / Fastboot\n• أدوات يومية\n• أدوات النظام\n• تسريع الألعاب\n• إدارة التطبيقات\n• النسخ الاحتياطي\n• فلاش الروم\n• Xiaomi / Huawei / Samsung / Oppo / Vivo\n• TWRP & Root\n• فك القفل و FRP\n• MediaTek\n• Qualcomm EDL\n• أدوات متقدمة",
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
        "lic_title": "🔑 تنشيط البرنامج",
        "lic_desc": "أدخل كود التفعيل الخاص بك لبدء استخدام البرنامج",
        "lic_placeholder": "أدخل الكود هنا...",
        "lic_activate": "✅ تفعيل",
        "lic_error": "❌ كود غير صحيح",
        "lic_success": "✅ تم التفعيل بنجاح",
        "lic_no_key": "⚠️ الرجاء إدخال الكود",
    },
    "en": {
        "title": "🛠️ Android Tool",
        "tab_adb": "ADB / Fastboot",
        "tab_tools": "📸 Daily Tools",
        "tab_system": "⚙️ System Tools",
        "tab_gaming": "🎮 Gaming & Performance",
        "tab_apps": "📱 App Manager",
        "tab_backup": "💾 Backup",
        "tab_flash": "📦 Flash ROM",
        "tab_xiaomi": "🟠 Xiaomi",
        "tab_huawei": "🟣 Huawei",
        "tab_samsung": "📱 Samsung",
        "tab_oppo": "🟢 Oppo/Realme",
        "tab_vivo": "🔵 Vivo/iQOO",
        "tab_root": "🔓 TWRP & Root",
        "tab_unlock": "🔒 Unlock",
        "tab_mtk": "MTK",
        "tab_edl": "Qualcomm EDL",
        "tab_adv": "🧰 Advanced Tools",
        "tab_about": "ℹ️ About",
        "download_tools": "📥 Download Platform-Tools",
        "detect": "🔍 Detect Devices",
        "device_info": "📱 Device Info",
        "reboot": "🔄 Reboot",
        "fastboot": "⚡ Fastboot",
        "reboot_recovery": "♻️ Recovery",
        "reboot_edl": "📡 EDL",
        "exit_fastboot": "🔌 Exit Fastboot",
        "tools_title": "📸 Daily Tools (ADB)",
        "tools_screenshot": "📸 Screenshot",
        "tools_record": "🎬 Screen Record (15s)",
        "tools_record_stop": "⏹️ Stop Recording",
        "tools_install_apk": "📦 Install APK",
        "tools_push": "📤 Push file to device",
        "tools_pull": "📥 Pull file from device",
        "tools_list_packages": "📋 List apps",
        "tools_battery": "🔋 Battery Info",
        "tools_export_dir": "📂 Open Exports Folder",
        "tools_wait": "⏳ ...",
        "tools_recording": "🎬 Recording... wait 15 seconds",
        "tools_recorded": "✅ Recording saved: {}",
        "tools_screenshot_saved": "✅ Screenshot saved: {}",
        "tools_no_device": "❌ No device connected",
        "tools_install_success": "✅ Installed: {}",
        "tools_install_fail": "❌ Install failed: {}",
        "tools_battery_info": "🔋 Battery Info",
        "tools_apps_list": "📋 Installed apps",
        "sys_title": "⚙️ Advanced System Tools",
        "sys_nav_hide": "🙈 Hide Navigation Bar",
        "sys_nav_show": "👁️ Show Navigation Bar",
        "sys_dpi_title": "Change Screen Density (DPI):",
        "sys_dpi_placeholder": "e.g. 420",
        "sys_dpi_apply": "Apply DPI",
        "sys_dpi_reset": "Reset DPI to Default",
        "sys_res_reset": "🔄 Reset Screen Resolution",
        "sys_anim": "🎬 Speed Up Animation:",
        "sys_anim_fast": "🚀 Faster (0.5x)",
        "sys_anim_normal": "🔄 Reset (1x)",
        "sys_anim_value": "e.g. 0.5",
        "sys_anim_apply": "Apply",
        "sys_sysui": "🔄 Restart System UI",
        "sys_gms": "Disable/Enable Google Services (GMS):",
        "sys_gms_disable": "🚫 Disable GMS",
        "sys_gms_enable": "✅ Enable GMS",
        "sys_restart": "♻️ Restart Device",
        "sys_applied": "✅ Applied",
        "sys_reset": "✅ Reset to default",
        "sys_sysui_restarting": "🔄 Restarting SystemUI...",
        "sys_gms_disabled": "✅ GMS disabled",
        "sys_gms_enabled": "✅ GMS enabled",
        "game_title": "🎮 Gaming & Performance Boost",
        "game_boost": "🚀 Enable Performance Mode (No Root)",
        "game_boost_desc": "Disables background services and speeds up animations",
        "game_normal": "🔄 Disable Gaming Mode",
        "game_normal_desc": "Restore phone to normal state",
        "game_fps": "Current FPS Rate:",
        "game_refresh": "🔄 Refresh Info",
        "game_ram": "🧹 Clean RAM",
        "game_ram_ok": "✅ RAM Cleaned",
        "game_cache": "🗑️ Clear Cache for All Apps",
        "game_cache_ok": "✅ Cache Cleared",
        "game_bg": "🚫 Disable Background Apps",
        "game_bg_ok": "✅ Background Apps Disabled",
        "game_bg_enable": "✅ Enable Background Apps",
        "game_res": "Change Screen Resolution for Gaming:",
        "game_res_apply": "Apply",
        "game_res_reset": "🔄 Reset Resolution",
        "game_status": "⏳ Running...",
        "game_info": "Note: These commands are safe and don't require root.",
        "adv_title": "🧰 Advanced Tools",
        "adv_adb_terminal": "🖥️ Run Custom ADB Command",
        "adv_adb_terminal_desc": "Type adb shell command and run on device",
        "adv_install_batch": "📦 Batch Install APKs",
        "adv_install_batch_desc": "Pick a folder to install all APKs inside",
        "adv_battery_calib": "🔋 Battery Calibration",
        "adv_battery_calib_desc": "Clear batterystats.bin (Requires Root)",
        "adv_network_info": "📡 Network Info",
        "adv_network_info_desc": "Show IP, Wi-Fi and network status",
        "adv_hide_app": "🔐 Hide App",
        "adv_hide_app_desc": "Hide an app from the app list",
        "adv_show_app": "👁️ Unhide App",
        "adv_show_app_desc": "Restore a hidden app",
        "adv_fastboot_info": "📊 Fastboot Info",
        "adv_fastboot_info_desc": "Show all fastboot variables",
        "adv_reboot_bootloader": "⚡ Reboot to Fastboot",
        "adv_reboot_bootloader_desc": "Send phone to Fastboot mode",
        "adv_reboot_recovery": "♻️ Reboot to Recovery",
        "adv_reboot_recovery_desc": "Send phone to Recovery mode",
        "adv_reboot_download": "📥 Reboot to Download Mode",
        "adv_reboot_download_desc": "Samsung - Download Mode",
        "adv_device_props": "📋 Full Device Properties",
        "adv_device_props_desc": "Show full getprop",
        "adv_wait": "⏳ Running...",
        "adv_done": "✅ Done",
        "adv_no_input": "⚠️ Please enter a command",
        "adv_adb_prompt": "Enter ADB command (e.g. shell getprop):",
        "adv_adb_result": "Command result:",
        "adv_pick_folder": "📁 Select APK Folder",
        "adv_installing": "⏳ Installing: {}",
        "adv_install_count": "✅ Installed {} apps",
        "adv_no_apk": "⚠️ No APK files found in folder",
        "adv_battery_warn": "⚠️ This requires root. Are you sure?",
        "adv_battery_done": "✅ Battery stats cleared. Reboot device.",
        "adv_network_loading": "⏳ Fetching network info...",
        "adv_hide_app_prompt": "Enter package name:",
        "adv_app_hidden": "✅ Hidden {}",
        "adv_app_shown": "✅ Unhidden {}",
        "adv_fastboot_info_loading": "⏳ Fetching fastboot info...",
        "adv_device_props_loading": "⏳ Fetching properties...",
        "apps_title": "📱 App Manager",
        "apps_load": "📋 Load Apps List",
        "apps_uninstall": "🗑️ Uninstall App",
        "apps_disable": "🚫 Disable",
        "apps_enable": "✅ Enable",
        "apps_extract": "📤 Extract APK",
        "apps_clear": "🧹 Clear Data",
        "apps_force_stop": "⛔ Force Stop",
        "apps_filter": "Filter:",
        "apps_filter_all": "All",
        "apps_filter_user": "User only",
        "apps_filter_system": "System only",
        "apps_count": "📊 {} apps",
        "apps_select": "Select an app from list:",
        "apps_loading": "⏳ Loading apps list...",
        "apps_loaded": "✅ Loaded {} apps",
        "apps_no_device": "❌ No device connected",
        "apps_no_packages": "⚠️ No apps",
        "apps_uninstall_ok": "✅ Uninstalled {}",
        "apps_uninstall_fail": "❌ Failed {}",
        "apps_disable_ok": "✅ Disabled {}",
        "apps_enable_ok": "✅ Enabled {}",
        "apps_extract_ok": "✅ Extracted {}",
        "apps_clear_ok": "✅ Cleared data for {}",
        "apps_stop_ok": "✅ Stopped {}",
        "backup_title": "💾 Backup & Restore",
        "backup_full": "📦 Full Backup (Apps + Data)",
        "backup_app": "📱 Backup Specific App",
        "backup_sdcard": "📂 Backup Full SD Card",
        "backup_restore": "♻️ Restore Backup",
        "backup_open": "📂 Open Backups Folder",
        "backup_warning": "⚠️ Full backup requires confirmation on phone screen",
        "backup_no_device": "❌ No device connected",
        "backup_starting": "⏳ Starting backup...",
        "backup_confirm_phone": "⚠️ Tap 'Back up my data' on phone screen",
        "backup_done": "✅ Backup completed: {}",
        "backup_fail": "❌ Backup failed",
        "backup_select_file": "Select .ab file to restore",
        "backup_restore_done": "✅ Restore started - tap Restore on phone",
        "backup_sdcard_done": "✅ SD card copied: {}",
        "backup_sdcard_fail": "❌ SD card copy failed",
        "backup_app_placeholder": "com.example.app",
        "backup_app_prompt": "Enter package name:",
        "vivo_title": "🔵 Vivo / iQOO",
        "vivo_warning": "⚠️ Funtouch OS / OriginOS",
        "vivo_info": "📱 Device Info",
        "vivo_check_bl": "🔍 Check BL",
        "vivo_fastboot": "⚡ Fastboot",
        "vivo_recovery": "♻️ Recovery",
        "vivo_edl": "📡 EDL",
        "vivo_flash_boot": "📦 boot.img",
        "vivo_flash_recovery": "📦 recovery.img",
        "vivo_flash_vbmeta": "📦 vbmeta.img",
        "vivo_flash_dtbo": "📦 dtbo.img",
        "vivo_flash_super": "📦 super.img",
        "vivo_flash_custom": "⚙️ Custom",
        "vivo_partition": "Partition:",
        "vivo_image": "Image:",
        "vivo_unlock_help": "🔓 Unlock Help",
        "vivo_download_help": "🌐 Unlock Guide",
        "vivo_unlock_cmd": "🔓 Try Unlock",
        "vivo_lock_cmd": "🔒 Lock",
        "vivo_flash_rom": "📦 Flash ROM",
        "vivo_select_rom": "Select ROM",
        "vivo_flash_wipe": "🚀 Flash + Wipe",
        "vivo_flash_keep": "🚀 Flash (Keep)",
        "vivo_erase_frp": "🚫 FRP",
        "vivo_wipe_data": "🧹 Wipe Data",
        "vivo_reboot_ok": "🔄 Normal",
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
        "huawei_title": "🟣 Huawei / Honor",
        "huawei_warning": "⚠️ Modern devices protected by Huawei ID",
        "huawei_info": "📱 Device Info",
        "huawei_fastboot": "⚡ Fastboot",
        "huawei_recovery": "♻️ Recovery",
        "huawei_erecovery": "🔄 eRecovery",
        "huawei_flash_boot": "📦 boot.img",
        "huawei_flash_recovery": "📦 recovery.img",
        "huawei_flash_system": "📦 system.img",
        "huawei_flash_ramdisk": "📦 ramdisk.img",
        "huawei_flash_custom": "⚙️ Custom",
        "huawei_partition": "Partition:",
        "huawei_image": "Image:",
        "huawei_unlock_help": "🔓 Unlock Help",
        "huawei_hisuite": "🌐 HiSuite",
        "huawei_erecovery_help": "📖 eRecovery Guide",
        "huawei_check_bl": "🔍 Check BL",
        "huawei_unlock_code": "🔑 Unlock Code",
        "huawei_erase_frp": "🚫 FRP",
        "huawei_wipe_data": "🧹 Wipe",
        "huawei_reboot_ok": "🔄 Normal",
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
        "oppo_title": "🟢 Oppo / Realme / OnePlus",
        "oppo_warning": "⚠️ ColorOS / OxygenOS",
        "oppo_info": "📱 Device Info",
        "oppo_check_bl": "🔍 Check BL",
        "oppo_fastboot": "⚡ Fastboot",
        "oppo_recovery": "♻️ Recovery",
        "oppo_edl": "📡 EDL",
        "oppo_flash_boot": "📦 boot.img",
        "oppo_flash_recovery": "📦 recovery.img",
        "oppo_flash_vbmeta": "📦 vbmeta.img",
        "oppo_flash_dtbo": "📦 dtbo.img",
        "oppo_flash_super": "📦 super.img",
        "oppo_flash_custom": "⚙️ Custom",
        "oppo_partition": "Partition:",
        "oppo_image": "Image:",
        "oppo_unlock_help": "🔓 Unlock Help",
        "oppo_download_help": "🌐 Unlock Guide",
        "oppo_unlock_cmd": "🔓 Try Unlock",
        "oppo_lock_cmd": "🔒 Lock",
        "oppo_flash_rom": "📦 Flash ROM",
        "oppo_select_rom": "Select ROM",
        "oppo_flash_wipe": "🚀 Flash + Wipe",
        "oppo_flash_keep": "🚀 Flash (Keep)",
        "oppo_erase_frp": "🚫 FRP",
        "oppo_wipe_data": "🧹 Wipe Data",
        "oppo_reboot_ok": "🔄 Normal",
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
        "about_description": "All-in-one Android tool\n\n• ADB / Fastboot\n• Daily Tools\n• System Tools\n• Gaming Boost\n• App Manager\n• Backup\n• Full ROM Flash\n• Xiaomi / Huawei / Samsung / Oppo / Vivo\n• TWRP & Root\n• Unlock & FRP\n• MediaTek\n• Qualcomm EDL\n• Advanced Tools",
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
        "confirm_uninstall": "Uninstall {}?",
        "confirm_disable": "Disable {}?",
        "confirm_clear": "Clear {} data?",
        "confirm_reset_dpi": "Reset DPI to default?",
        "confirm_sysui": "Restart SystemUI?",
        "confirm_reboot": "Reboot device?",
        "err_check": "Check",
        "err": "Error",
        "confirm": "Confirm",
        "warn": "Warning",
        "lic_title": "🔑 Activate Software",
        "lic_desc": "Enter your license key to start using the tool",
        "lic_placeholder": "Enter your key here...",
        "lic_activate": "✅ Activate",
        "lic_error": "❌ Invalid License Key",
        "lic_success": "✅ Activation Successful",
        "lic_no_key": "⚠️ Please enter the key",
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

        self.build_ui()

    def tr(self, key):
        return self.t.get(key, key)

    def build_ui(self):
        for w in self.winfo_children():
            w.destroy()

        ctk.CTkLabel(self, text="🔑", font=("Arial", 50)).pack(pady=10)
        ctk.CTkLabel(self, text=self.tr("lic_title"),
                     font=("Arial", 20, "bold")).pack(pady=5)
        ctk.CTkLabel(self, text=self.tr("lic_desc"),
                     font=("Arial", 12), text_color="gray").pack(pady=5)

        self.entry = ctk.CTkEntry(self, width=350, height=45,
                                   placeholder_text=self.tr("lic_placeholder"))
        self.entry.pack(pady=15)

        ctk.CTkButton(self, text=self.tr("lic_activate"), width=350, height=45,
                      fg_color="green", hover_color="darkgreen",
                      font=("Arial", 14, "bold"),
                      command=self.do_activate).pack(pady=10)

        self.status = ctk.CTkLabel(self, text="", font=("Arial", 12))
        self.status.pack(pady=5)

        ctk.CTkButton(self, text="🌐 English / العربية", width=150, height=30,
                      fg_color="gray",
                      command=self.toggle_lang).pack(pady=5)

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
            self.after(800, self.destroy)
            self.after(900, self.on_success)
        else:
            self.status.configure(text=self.tr("lic_error"), text_color="red")

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
        self.selected_app_info = ""

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

    def build_tools_tab(self):
        f = self.tab_tools
        ctk.CTkLabel(f, text=self.tr("tools_title"),
                     font=("Arial", 16, "bold")).pack(pady=10)

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
        ctk.CTkButton(info_frame, text=self.tr("tools_list_packages"), width=170, height=45,
                      command=self.tool_list_packages).pack(side="left", padx=5)

        ctk.CTkButton(f, text=self.tr("tools_export_dir"), width=350, height=45,
                      fg_color="gray",
                      command=self.open_exports).pack(pady=15)

    def build_system_tab(self):
        f = self.tab_system
        ctk.CTkLabel(f, text=self.tr("sys_title"),
                     font=("Arial", 16, "bold")).pack(pady=10)

        row1 = ctk.CTkFrame(f)
        row1.pack(pady=4)
        ctk.CTkButton(row1, text=self.tr("sys_nav_hide"), width=200,
                      fg_color="orange", hover_color="darkorange",
                      command=self.sys_hide_nav).pack(side="left", padx=3)
        ctk.CTkButton(row1, text=self.tr("sys_nav_show"), width=200,
                      fg_color="green", hover_color="darkgreen",
                      command=self.sys_show_nav).pack(side="left", padx=3)

        ctk.CTkLabel(f, text=self.tr("sys_dpi_title"),
                     font=("Arial", 12, "bold")).pack(pady=(15, 3))
        row2 = ctk.CTkFrame(f)
        row2.pack(pady=4)
        self.dpi_entry = ctk.CTkEntry(row2, width=120,
                                       placeholder_text=self.tr("sys_dpi_placeholder"))
        self.dpi_entry.pack(side="left", padx=5)
        ctk.CTkButton(row2, text=self.tr("sys_dpi_apply"), width=150,
                      command=self.sys_dpi_apply).pack(side="left", padx=5)
        ctk.CTkButton(row2, text=self.tr("sys_dpi_reset"), width=150,
                      fg_color="red", hover_color="darkred",
                      command=self.sys_dpi_reset).pack(side="left", padx=5)

        ctk.CTkLabel(f, text=self.tr("sys_anim"),
                     font=("Arial", 12, "bold")).pack(pady=(15, 3))
        row3 = ctk.CTkFrame(f)
        row3.pack(pady=4)
        ctk.CTkButton(row3, text=self.tr("sys_anim_fast"), width=170,
                      fg_color="green", hover_color="darkgreen",
                      command=self.sys_anim_fast).pack(side="left", padx=3)
        ctk.CTkButton(row3, text=self.tr("sys_anim_normal"), width=170,
                      fg_color="gray",
                      command=self.sys_anim_normal).pack(side="left", padx=3)

        row4 = ctk.CTkFrame(f)
        row4.pack(pady=4)
        self.anim_entry = ctk.CTkEntry(row4, width=120,
                                        placeholder_text=self.tr("sys_anim_value"))
        self.anim_entry.pack(side="left", padx=5)
        ctk.CTkButton(row4, text=self.tr("sys_anim_apply"), width=120,
                      command=self.sys_anim_custom).pack(side="left", padx=5)

        ctk.CTkLabel(f, text="—",
                     text_color="gray").pack(pady=10)
        row5 = ctk.CTkFrame(f)
        row5.pack(pady=4)
        ctk.CTkButton(row5, text=self.tr("sys_sysui"), width=220,
                      fg_color="orange", hover_color="darkorange",
                      command=self.sys_restart_sysui).pack(side="left", padx=3)
        ctk.CTkButton(row5, text=self.tr("sys_restart"), width=220,
                      fg_color="red", hover_color="darkred",
                      command=self.sys_restart_device).pack(side="left", padx=3)

        ctk.CTkLabel(f, text=self.tr("sys_gms"),
                     font=("Arial", 12, "bold")).pack(pady=(15, 3))
        row6 = ctk.CTkFrame(f)
        row6.pack(pady=4)
        ctk.CTkButton(row6, text=self.tr("sys_gms_disable"), width=170,
                      fg_color="orange", hover_color="darkorange",
                      command=self.sys_gms_disable).pack(side="left", padx=3)
        ctk.CTkButton(row6, text=self.tr("sys_gms_enable"), width=170,
                      fg_color="green", hover_color="darkgreen",
                      command=self.sys_gms_enable).pack(side="left", padx=3)

    def sys_hide_nav(self):
        def t():
            self.log("🙈 Hiding nav bar...")
            run([ADB, "shell", "settings", "put", "global", "policy_control",
                 "immersive.full=*"])
            self.log(self.tr("sys_applied"))
        threading.Thread(target=t, daemon=True).start()

    def sys_show_nav(self):
        def t():
            self.log("👁️ Showing nav bar...")
            run([ADB, "shell", "settings", "put", "global", "policy_control", "null"])
            self.log(self.tr("sys_applied"))
        threading.Thread(target=t, daemon=True).start()

    def sys_dpi_apply(self):
        val = self.dpi_entry.get().strip()
        if not val.isdigit():
            messagebox.showerror(self.tr("err"), self.tr("err_check"))
            return
        def t():
            self.log(f"⚙️ Setting DPI to {val}...")
            run([ADB, "shell", "wm", "density", val])
            self.log(self.tr("sys_applied"))
        threading.Thread(target=t, daemon=True).start()

    def sys_dpi_reset(self):
        if not messagebox.askyesno(self.tr("warn"), self.tr("confirm_reset_dpi")):
            return
        def t():
            self.log("🔄 Resetting DPI...")
            run([ADB, "shell", "wm", "density", "reset"])
            self.log(self.tr("sys_reset"))
        threading.Thread(target=t, daemon=True).start()

    def sys_anim_fast(self):
        def t():
            self.log("🚀 Speeding up animations...")
            for key in ["window_animation_scale",
                        "transition_animation_scale",
                        "animator_duration_scale"]:
                run([ADB, "shell", "settings", "put", "global", key, "0.5"])
            self.log(self.tr("sys_applied"))
        threading.Thread(target=t, daemon=True).start()

    def sys_anim_normal(self):
        def t():
            self.log("🔄 Resetting animations...")
            for key in ["window_animation_scale",
                        "transition_animation_scale",
                        "animator_duration_scale"]:
                run([ADB, "shell", "settings", "put", "global", key, "1.0"])
            self.log(self.tr("sys_reset"))
        threading.Thread(target=t, daemon=True).start()

    def sys_anim_custom(self):
        val = self.anim_entry.get().strip()
        try:
            float(val)
        except ValueError:
            messagebox.showerror(self.tr("err"), self.tr("err_check"))
            return
        def t():
            self.log(f"⚙️ Animation scale = {val}...")
            for key in ["window_animation_scale",
                        "transition_animation_scale",
                        "animator_duration_scale"]:
                run([ADB, "shell", "settings", "put", "global", key, val])
            self.log(self.tr("sys_applied"))
        threading.Thread(target=t, daemon=True).start()

    def sys_restart_sysui(self):
        if not messagebox.askyesno(self.tr("warn"), self.tr("confirm_sysui")):
            return
        def t():
            self.log(self.tr("sys_sysui_restarting"))
            run([ADB, "shell", "pkill", "com.android.systemui"], timeout=15)
            self.log(self.tr("sys_applied"))
        threading.Thread(target=t, daemon=True).start()

    def sys_restart_device(self):
        if not messagebox.askyesno(self.tr("warn"), self.tr("confirm_reboot")):
            return
        self.async_run(lambda: run([ADB, "reboot"]))

    def sys_gms_disable(self):
        def t():
            self.log("🚫 Disabling GMS...")
            run([ADB, "shell", "pm", "disable-user", "--user", "0", "com.google.android.gms"])
            run([ADB, "shell", "pm", "disable-user", "--user", "0", "com.android.vending"])
            self.log(self.tr("sys_gms_disabled"))
        threading.Thread(target=t, daemon=True).start()

    def sys_gms_enable(self):
        def t():
            self.log("✅ Enabling GMS...")
            run([ADB, "shell", "pm", "enable", "com.google.android.gms"])
            run([ADB, "shell", "pm", "enable", "com.android.vending"])
            self.log(self.tr("sys_gms_enabled"))
        threading.Thread(target=t, daemon=True).start()

    def build_gaming_tab(self):
        f = self.tab_gaming
        ctk.CTkLabel(f, text=self.tr("game_title"),
                     font=("Arial", 16, "bold")).pack(pady=10)

        ctk.CTkButton(f, text=self.tr("game_boost"), width=400, height=50,
                      fg_color="green", hover_color="darkgreen",
                      font=("Arial", 14, "bold"),
                      command=self.game_boost).pack(pady=5)
        ctk.CTkLabel(f, text=self.tr("game_boost_desc"),
                     font=("Arial", 11), text_color="gray").pack()

        ctk.CTkButton(f, text=self.tr("game_normal"), width=400, height=45,
                      fg_color="orange", hover_color="darkorange",
                      command=self.game_normal).pack(pady=10)
        ctk.CTkLabel(f, text=self.tr("game_normal_desc"),
                     font=("Arial", 11), text_color="gray").pack()

        ctk.CTkLabel(f, text="—", text_color="gray").pack(pady=10)

        row1 = ctk.CTkFrame(f)
        row1.pack(pady=5)
        ctk.CTkButton(row1, text=self.tr("game_ram"), width=200,
                      command=self.game_ram).pack(side="left", padx=5)
        ctk.CTkButton(row1, text=self.tr("game_cache"), width=200,
                      command=self.game_cache).pack(side="left", padx=5)

        row2 = ctk.CTkFrame(f)
        row2.pack(pady=5)
        ctk.CTkButton(row2, text=self.tr("game_bg"), width=200,
                      fg_color="orange", hover_color="darkorange",
                      command=self.game_bg_disable).pack(side="left", padx=5)
        ctk.CTkButton(row2, text=self.tr("game_bg_enable"), width=200,
                      fg_color="green", hover_color="darkgreen",
                      command=self.game_bg_enable).pack(side="left", padx=5)

        ctk.CTkLabel(f, text=self.tr("game_info"),
                     font=("Arial", 11), text_color="lightblue").pack(pady=15)

    def game_boost(self):
        def t():
            self.log("🚀 Activating Gaming Mode...")
            for key in ["window_animation_scale",
                        "transition_animation_scale",
                        "animator_duration_scale"]:
                run([ADB, "shell", "settings", "put", "global", key, "0.5"])
            run([ADB, "shell", "settings", "put", "global", "zen_mode", "1"])
            self.log("✅ Gaming Mode Active!")
        threading.Thread(target=t, daemon=True).start()

    def game_normal(self):
        def t():
            self.log("🔄 Deactivating Gaming Mode...")
            for key in ["window_animation_scale",
                        "transition_animation_scale",
                        "animator_duration_scale"]:
                run([ADB, "shell", "settings", "put", "global", key, "1.0"])
            run([ADB, "shell", "settings", "put", "global", "zen_mode", "0"])
            self.log("✅ Normal Mode Restored!")
        threading.Thread(target=t, daemon=True).start()

    def game_ram(self):
        def t():
            self.log("🧹 Cleaning RAM...")
            run([ADB, "shell", "am", "kill-all"])
            self.log(self.tr("game_ram_ok"))
        threading.Thread(target=t, daemon=True).start()

    def game_cache(self):
        def t():
            self.log("🗑️ Clearing Cache...")
            run([ADB, "shell", "pm", "trim-caches", "999G"])
            self.log(self.tr("game_cache_ok"))
        threading.Thread(target=t, daemon=True).start()

    def game_bg_disable(self):
        def t():
            self.log("🚫 Disabling background apps...")
            run([ADB, "shell", "settings", "put", "global", "app_standby_enabled", "0"])
            run([ADB, "shell", "settings", "put", "global", "adaptive_battery_management_enabled", "0"])
            self.log(self.tr("game_bg_ok"))
        threading.Thread(target=t, daemon=True).start()

    def game_bg_enable(self):
        def t():
            self.log("✅ Enabling background apps...")
            run([ADB, "shell", "settings", "put", "global", "app_standby_enabled", "1"])
            run([ADB, "shell", "settings", "put", "global", "adaptive_battery_management_enabled", "1"])
            self.log(self.tr("sys_applied"))
        threading.Thread(target=t, daemon=True).start()

    def build_apps_tab(self):
        f = self.tab_apps
        ctk.CTkLabel(f, text=self.tr("apps_title"),
                     font=("Arial", 16, "bold")).pack(pady=8)

        top = ctk.CTkFrame(f)
        top.pack(fill="x", padx=20, pady=5)
        ctk.CTkButton(top, text=self.tr("apps_load"), width=200, height=38,
                      fg_color="green", hover_color="darkgreen",
                      command=self.apps_load).pack(side="left", padx=5)

        ctk.CTkLabel(top, text=self.tr("apps_filter")).pack(side="left", padx=(20, 5))
        self.apps_filter_var = ctk.StringVar(value=self.tr("apps_filter_all"))
        self.apps_filter_menu = ctk.CTkOptionMenu(
            top, width=150, variable=self.apps_filter_var,
            values=[self.tr("apps_filter_all"),
                    self.tr("apps_filter_user"),
                    self.tr("apps_filter_system")],
            command=lambda _: self.apps_apply_filter())
        self.apps_filter_menu.pack(side="left", padx=5)

        self.apps_count_label = ctk.CTkLabel(top, text="", font=("Arial", 11),
                                              text_color="lightblue")
        self.apps_count_label.pack(side="left", padx=15)

        list_frame = ctk.CTkScrollableFrame(f, height=280)
        list_frame.pack(fill="both", expand=True, padx=20, pady=5)
        self.apps_list_frame = list_frame

        detail_frame = ctk.CTkFrame(f)
        detail_frame.pack(fill="x", padx=20, pady=5)
        self.apps_detail_label = ctk.CTkLabel(
            detail_frame, text=self.tr("apps_select"),
            font=("Arial", 12), text_color="gray", anchor="w")
        self.apps_detail_label.pack(fill="x", padx=10, pady=5)

        ops = ctk.CTkFrame(f)
        ops.pack(pady=8)
        ctk.CTkButton(ops, text=self.tr("apps_uninstall"), width=170, height=42,
                      fg_color="red", hover_color="darkred",
                      command=self.app_uninstall).pack(side="left", padx=4)
        ctk.CTkButton(ops, text=self.tr("apps_disable"), width=170, height=42,
                      fg_color="orange", hover_color="darkorange",
                      command=self.app_disable).pack(side="left", padx=4)
        ctk.CTkButton(ops, text=self.tr("apps_enable"), width=170, height=42,
                      fg_color="green", hover_color="darkgreen",
                      command=self.app_enable).pack(side="left", padx=4)
        ctk.CTkButton(ops, text=self.tr("apps_extract"), width=170, height=42,
                      command=self.app_extract).pack(side="left", padx=4)

        ops2 = ctk.CTkFrame(f)
        ops2.pack(pady=4)
        ctk.CTkButton(ops2, text=self.tr("apps_clear"), width=170, height=40,
                      fg_color="orange", hover_color="darkorange",
                      command=self.app_clear).pack(side="left", padx=4)
        ctk.CTkButton(ops2, text=self.tr("apps_force_stop"), width=170, height=40,
                      fg_color="red", hover_color="darkred",
                      command=self.app_force_stop).pack(side="left", padx=4)

    def apps_load(self):
        def t():
            self.log(self.tr("apps_loading"))
            out = run([ADB, "shell", "pm", "list", "packages", "-f"], timeout=60)
            if not out.strip() or "error" in out.lower():
                self.log(self.tr("apps_no_device"))
                return
            apps = []
            for line in out.strip().splitlines():
                line = line.strip()
                if not line.startswith("package:"):
                    continue
                parts = line[len("package:"):].split("=")
                if len(parts) != 2:
                    continue
                apk_path, pkg = parts
                is_system = apk_path.startswith("/system") or apk_path.startswith("/product")
                try:
                    size_str = run([ADB, "shell", "du", "-b", apk_path], timeout=5)
                    size_bytes = 0
                    for tok in size_str.split():
                        if tok.isdigit():
                            size_bytes = int(tok)
                            break
                except Exception:
                    size_bytes = 0
                apps.append({
                    "package": pkg.strip(),
                    "path": apk_path,
                    "is_system": is_system,
                    "size": size_bytes,
                })
            self.apps_list = apps
            self.log(self.tr("apps_loaded", len(apps)))
            self.apps_apply_filter()
        threading.Thread(target=t, daemon=True).start()

    def apps_apply_filter(self):
        for w in self.apps_list_frame.winfo_children():
            w.destroy()

        filter_val = self.apps_filter_var.get()
        all_val = self.tr("apps_filter_all")
        user_val = self.tr("apps_filter_user")
        sys_val = self.tr("apps_filter_system")

        if filter_val == all_val:
            filtered = self.apps_list
        elif filter_val == user_val:
            filtered = [a for a in self.apps_list if not a["is_system"]]
        else:
            filtered = [a for a in self.apps_list if a["is_system"]]

        self.apps_filtered = filtered
        self.apps_count_label.configure(text=self.tr("apps_count", len(filtered)))

        for app in filtered:
            self._add_app_row(app)

    def _add_app_row(self, app):
        pkg = app["package"]
        icon_text = "⚙️" if app["is_system"] else "📱"
        size_mb = app["size"] / (1024 * 1024) if app["size"] else 0
        label = f"{icon_text}  {pkg}   ({size_mb:.1f} MB)"

        btn = ctk.CTkButton(
            self.apps_list_frame, text=label, anchor="w",
            height=32, fg_color="#2b2b3d", hover_color="#3b3b4d",
            command=lambda p=pkg, a=app: self._select_app(p, a))
        btn.pack(fill="x", pady=2, padx=2)

    def _select_app(self, pkg, app):
        self.selected_pkg = pkg
        self.selected_app_info = app
        kind = "System" if app["is_system"] else "User"
        size_mb = app["size"] / (1024 * 1024) if app["size"] else 0
        self.apps_detail_label.configure(
            text=f"🎯 {pkg}  |  {kind}  |  {size_mb:.1f} MB",
            text_color="lightgreen")

    def _app_cmd(self, args, timeout=60):
        if not self.selected_pkg:
            messagebox.showerror(self.tr("err"), self.tr("apps_select"))
            return None
        return run([ADB, "shell"] + args, timeout=timeout)

    def app_uninstall(self):
        if not self.selected_pkg:
            messagebox.showerror(self.tr("err"), self.tr("apps_select"))
            return
        if not messagebox.askyesno(self.tr("confirm"),
                                    self.tr("confirm_uninstall", self.selected_pkg)):
            return
        
        def t():
            out = run([ADB, "uninstall", self.selected_pkg], timeout=120)
            self.log(out)
            if "Success" in out:
                self.log(self.tr("apps_uninstall_ok", self.selected_pkg))
                self.apps_load()
            else:
                self.log(self.tr("apps_uninstall_fail", self.selected_pkg))
        threading.Thread(target=t, daemon=True).start()

    def app_disable(self):
        if not self.selected_pkg:
            messagebox.showerror(self.tr("err"), self.tr("apps_select"))
            return
        if not messagebox.askyesno(self.tr("warn"),
                                    self.tr("confirm_disable", self.selected_pkg)):
            return
        def t():
            out = run([ADB, "shell", "pm", "disable-user",
                       "--user", "0", self.selected_pkg], timeout=60)
            self.log(out)
            self.log(self.tr("apps_disable_ok", self.selected_pkg))
        threading.Thread(target=t, daemon=True).start()

    def app_enable(self):
        if not self.selected_pkg:
            messagebox.showerror(self.tr("err"), self.tr("apps_select"))
            return
        def t():
            out = run([ADB, "shell", "pm", "enable",
                       self.selected_pkg], timeout=60)
            self.log(out)
            self.log(self.tr("apps_enable_ok", self.selected_pkg))
        threading.Thread(target=t, daemon=True).start()

    def app_extract(self):
        if not self.selected_pkg:
            messagebox.showerror(self.tr("err"), self.tr("apps_select"))
            return
        if not self.selected_apk_path():
            messagebox.showerror(self.tr("err"), "APK path unknown")
            return
        def t():
            apk_path = self.selected_apk_path()
            local = os.path.join(EXPORTS_DIR, f"{self.selected_pkg}.apk")
            self.log(f"📤 Pulling {apk_path}...")
            self.log(run([ADB, "pull", apk_path, local], timeout=300))
            if os.path.exists(local):
                self.log(self.tr("apps_extract_ok", local))
            else:
                self.log("❌ Extract failed")
        threading.Thread(target=t, daemon=True).start()

    def selected_apk_path(self):
        if not self.selected_app_info:
            return None
        return self.selected_app_info.get("path")

    def app_clear(self):
        if not self.selected_pkg:
            messagebox.showerror(self.tr("err"), self.tr("apps_select"))
            return
        if not messagebox.askyesno(self.tr("warn"),
                                    self.tr("confirm_clear", self.selected_pkg)):
            return
        def t():
            out = run([ADB, "shell", "pm", "clear", self.selected_pkg], timeout=60)
            self.log(out)
            self.log(self.tr("apps_clear_ok", self.selected_pkg))
        threading.Thread(target=t, daemon=True).start()

    def app_force_stop(self):
        if not self.selected_pkg:
            messagebox.showerror(self.tr("err"), self.tr("apps_select"))
            return
        def t():
            out = run([ADB, "shell", "am", "force-stop",
                       self.selected_pkg], timeout=30)
            self.log(out)
            self.log(self.tr("apps_stop_ok", self.selected_pkg))
        threading.Thread(target=t, daemon=True).start()

    def build_backup_tab(self):
        f = self.tab_backup
        ctk.CTkLabel(f, text=self.tr("backup_title"),
                     font=("Arial", 16, "bold")).pack(pady=10)
        ctk.CTkLabel(f, text=self.tr("backup_warning"),
                     font=("Arial", 11), text_color="orange").pack(pady=4)

        bf = ctk.CTkFrame(f)
        bf.pack(pady=10)
        ctk.CTkButton(bf, text=self.tr("backup_full"), width=400, height=50,
                      fg_color="green", hover_color="darkgreen",
                      font=("Arial", 14, "bold"),
                      command=self.backup_full).pack(pady=5)
        ctk.CTkButton(bf, text=self.tr("backup_app"), width=400, height=45,
                      fg_color="orange", hover_color="darkorange",
                      command=self.backup_app).pack(pady=5)
        ctk.CTkButton(bf, text=self.tr("backup_sdcard"), width=400, height=45,
                      fg_color="blue", hover_color="darkblue",
                      command=self.backup_sdcard).pack(pady=5)

        ctk.CTkLabel(f, text="—", text_color="gray").pack(pady=10)

        bf2 = ctk.CTkFrame(f)
        bf2.pack(pady=10)
        ctk.CTkButton(bf2, text=self.tr("backup_restore"), width=400, height=50,
                      fg_color="orange", hover_color="darkorange",
                      font=("Arial", 14, "bold"),
                      command=self.backup_restore).pack(pady=5)
        ctk.CTkButton(bf2, text=self.tr("backup_open"), width=400, height=45,
                      fg_color="gray",
                      command=self.open_backups).pack(pady=5)

    def open_backups(self):
        try:
            if os.name == "nt":
                os.startfile(BACKUP_DIR)
            else:
                subprocess.Popen(["xdg-open", BACKUP_DIR])
        except Exception as e:
            self.log(self.tr("msg_error", e))

    def backup_full(self):
        def t():
            self.log(self.tr("backup_starting"))
            self.log(self.tr("backup_confirm_phone"))
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            path = os.path.join(BACKUP_DIR, f"full_backup_{ts}.ab")
            try:
                r = subprocess.run(
                    [ADB, "backup", "-apk", "-shared", "-all", "-f", path],
                    capture_output=True, timeout=3600,
                    creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
                if os.path.exists(path) and os.path.getsize(path) > 100:
                    self.log(self.tr("backup_done", path))
                else:
                    self.log(self.tr("backup_fail"))
            except Exception as e:
                self.log(f"❌ {e}")
        threading.Thread(target=t, daemon=True).start()

    def backup_app(self):
        pkg = ctk.CTkInputDialog(
            text=self.tr("backup_app_prompt"),
            title="Backup App").get_input()
        if not pkg:
            return
        def t():
            self.log(f"⏳ Backing up {pkg}...")
            self.log(self.tr("backup_confirm_phone"))
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe = pkg.replace(".", "_")
            path = os.path.join(BACKUP_DIR, f"app_{safe}_{ts}.ab")
            try:
                r = subprocess.run(
                    [ADB, "backup", "-apk", "-f", path, pkg],
                    capture_output=True, timeout=1800,
                    creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
                if os.path.exists(path) and os.path.getsize(path) > 100:
                    self.log(self.tr("backup_done", path))
                else:
                    self.log(self.tr("backup_fail"))
            except Exception as e:
                self.log(f"❌ {e}")
        threading.Thread(target=t, daemon=True).start()

    def backup_sdcard(self):
        def t():
            self.log("📂 Copying /sdcard/ ...")
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            dest = os.path.join(BACKUP_DIR, f"sdcard_{ts}")
            try:
                os.makedirs(dest, exist_ok=True)
                out = run([ADB, "pull", "/sdcard/", dest], timeout=7200)
                self.log(out[-500:])
                if os.path.exists(dest) and os.listdir(dest):
                    self.log(self.tr("backup_sdcard_done", dest))
                else:
                    self.log(self.tr("backup_sdcard_fail"))
            except Exception as e:
                self.log(f"❌ {e}")
        threading.Thread(target=t, daemon=True).start()

    def backup_restore(self):
        p = filedialog.askopenfilename(
            filetypes=[("ADB Backup", "*.ab"), ("All", "*.*")],
            initialdir=BACKUP_DIR)
        if not p:
            return
        def t():
            self.log(f"♻️ Restoring {os.path.basename(p)}...")
            self.log(self.tr("backup_restore_done"))
            try:
                r = subprocess.run(
                    [ADB, "restore", p],
                    capture_output=True, timeout=3600,
                    creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
                self.log((r.stdout or b"").decode("utf-8", "ignore")[-500:])
                self.log("✅ Restore done")
            except Exception as e:
                self.log(f"❌ {e}")
        threading.Thread(target=t, daemon=True).start()

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
                      command=lambda: webbrowser.open("https://en.miui.com/unlock/")).pack(side="left", padx=4)
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
            for p in ["ro.product.model", "ro.product.brand",
                      "ro.miui.ui.version.name", "ro.mi.os.version.incremental",
                      "ro.build.version.release", "ro.boot.hwc",
                      "ro.boot.hwlevel", "ro.secureboot.lockstate",
                      "ro.boot.verifiedbootstate", "ro.serialno",
                      "ro.product.cpu.abi"]:
                self.log(f"{p}: {run([ADB, 'shell', 'getprop', p]).strip()}")
        threading.Thread(target=t, daemon=True).start()

    def xiaomi_mi_assistant(self):
        def t():
            self.log("=" * 50)
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
                    self.log("❌ No images")
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
                        images[os.path.splitext(f)[0]] = os.path.join(images_dir, f)
                for part in order:
                    if part not in images:
                        continue
                    if wipe and part == "userdata":
                        continue
                    self.log(f"🚀 flash {part}")
                    self.log(run([FASTBOOT, "flash", part, images[part]], timeout=1800)[-300:])
                for part, path in images.items():
                    if part in order or (wipe and part == "userdata"):
                        continue
                    self.log(f"🚀 flash {part}")
                    self.log(run([FASTBOOT, "flash", part, path], timeout=1800)[-300:])
                self.log("🎉 Xiaomi ROM flashed!")
                run([FASTBOOT, "reboot"])
            except Exception as e:
                self.log(f"❌ {e}")
        threading.Thread(target=t, daemon=True).start()

    def xiaomi_flash_single(self, partition):
        p = filedialog.askopenfilename(filetypes=[("Image", "*.img")])
        if not p:
            return
        def t():
            self.log(f"🚀 flash {partition}")
            self.log(run([FASTBOOT, "flash", partition, p], timeout=600)[-500:])
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
            self.log(run([FASTBOOT, "flash", part, f], timeout=600)[-500:])
        threading.Thread(target=t, daemon=True).start()

    def xiaomi_remove_account(self):
        messagebox.showinfo("Info", self.tr("xiaomi_remove_mi_account_help"))
        def t():
            self.log("⚠️ Mi Account removal requires MTK/EDL")
        threading.Thread(target=t, daemon=True).start()

    def xiaomi_clean_lock(self):
        if not messagebox.askyesno(self.tr("warn"), "Flash + Lock?"):
            return
        def t():
            self.log("🔒 Locking...")
            run([FASTBOOT, "flashing", "lock"], timeout=120)
            run([FASTBOOT, "reboot"])
        threading.Thread(target=t, daemon=True).start()

    def build_huawei_tab(self):
        f = self.tab_huawei
        ctk.CTkLabel(f, text=self.tr("huawei_title"),
                     font=("Arial", 16, "bold")).pack(pady=6)
        ctk.CTkLabel(f, text=self.tr("huawei_warning"),
                     font=("Arial", 11), text_color="orange").pack(pady=4)
        row = ctk.CTkFrame(f)
        row.pack(pady=6)
        ctk.CTkButton(row, text=self.tr("huawei_info"), width=180,
                      command=self.huawei_info).pack(side="left", padx=4)
        ctk.CTkButton(row, text=self.tr("huawei_check_bl"), width=180,
                      command=self.huawei_check_bl).pack(side="left", padx=4)
        ctk.CTkButton(row, text=self.tr("huawei_erecovery"), width=180,
                      fg_color="orange", hover_color="darkorange",
                      command=self.huawei_erecovery).pack(side="left", padx=4)
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
            for p in ["ro.product.model", "ro.product.brand",
                      "ro.build.version.release", "ro.build.version.emui",
                      "ro.build.display.id", "ro.serialno",
                      "ro.product.cpu.abi", "ro.build.version.sdk",
                      "ro.boot.hardware", "ro.board.platform"]:
                self.log(f"{p}: {run([ADB, 'shell', 'getprop', p]).strip()}")
        threading.Thread(target=t, daemon=True).start()

    def huawei_check_bl(self):
        def t():
            self.log("=" * 50)
            self.log(f"verifiedbootstate: {run([ADB, 'shell', 'getprop', 'ro.boot.verifiedbootstate']).strip()}")
            self.log(f"flash.locked: {run([ADB, 'shell', 'getprop', 'ro.boot.flash.locked']).strip()}")
            self.log(run([FASTBOOT, "oem", "device-info"]))
        threading.Thread(target=t, daemon=True).start()

    def huawei_erecovery(self):
        def t():
            self.log("🔄 Rebooting to eRecovery...")
            self.log(run([ADB, "reboot", "erecovery"], timeout=20))
        threading.Thread(target=t, daemon=True).start()

    def huawei_flash_single(self, partition):
        p = filedialog.askopenfilename(filetypes=[("Image", "*.img"), ("All", "*.*")])
        if not p:
            return
        if not messagebox.askyesno(self.tr("confirm"), self.tr("confirm_flash_samsung", partition)):
            return
        def t():
            self.log(f"🚀 flash {partition}: {os.path.basename(p)}")
            self.log(run([FASTBOOT, "flash", partition, p], timeout=900)[-1000:])
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
            self.log(run([FASTBOOT, "flash", part, f], timeout=900)[-1000:])
        threading.Thread(target=t, daemon=True).start()

    def huawei_unlock_code(self):
        code = ctk.CTkInputDialog(text="Enter Huawei Unlock Code:", title="Unlock").get_input()
        if not code:
            return
        def t():
            self.log(f"🔑 Unlocking...")
            self.log(run([FASTBOOT, "oem", "unlock", code], timeout=120))
        threading.Thread(target=t, daemon=True).start()

    def huawei_erase_frp(self):
        if not messagebox.askyesno(self.tr("warn"), self.tr("confirm_wipe")):
            return
        self.async_run(lambda: run([FASTBOOT, "erase", "frp"], timeout=120))

    def huawei_wipe_data(self):
        if not messagebox.askyesno(self.tr("warn"), self.tr("confirm_format")):
            return
        self.async_run(lambda: run([FASTBOOT, "erase", "userdata"], timeout=300))

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
            getattr(self, f"{var}_label").configure(text=os.path.basename(p),
                                                     text_color="lightgreen")

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
                self.log(run(args, timeout=3600, cwd=HEIMDALL_DIR)[-1500:])
            self.log(self.tr("samsung_done"))
        threading.Thread(target=t, daemon=True).start()

    def build_oppo_tab(self):
        f = self.tab_oppo
        ctk.CTkLabel(f, text=self.tr("oppo_title"),
                     font=("Arial", 16, "bold")).pack(pady=6)
        ctk.CTkLabel(f, text=self.tr("oppo_warning"),
                     font=("Arial", 11), text_color="orange").pack(pady=4)
        row = ctk.CTkFrame(f)
        row.pack(pady=6)
        ctk.CTkButton(row, text=self.tr("oppo_info"), width=170,
                      command=self.oppo_info).pack(side="left", padx=4)
        ctk.CTkButton(row, text=self.tr("oppo_check_bl"), width=170,
                      command=self.oppo_check_bl).pack(side="left", padx=4)
        ctk.CTkButton(row, text=self.tr("oppo_fastboot"), width=170,
                      command=lambda: self.async_run(lambda: run([ADB, "reboot", "bootloader"]))).pack(side="left", padx=4)
        ctk.CTkLabel(f, text="— Unlock Tools —",
                     font=("Arial", 12, "bold"), text_color="lightblue").pack(pady=(15, 3))
        uf = ctk.CTkFrame(f)
        uf.pack(pady=4)
        ctk.CTkButton(uf, text=self.tr("oppo_unlock_help"), width=220,
                      fg_color="gray",
                      command=lambda: webbrowser.open("https://www.oppo.com/en/support/")).pack(side="left", padx=3)
        ctk.CTkButton(uf, text=self.tr("oppo_download_help"), width=220,
                      fg_color="gray",
                      command=lambda: webbrowser.open("https://www.realme.com/global/support/")).pack(side="left", padx=3)
        ctk.CTkButton(uf, text=self.tr("oppo_flash_recovery"), width=220,
                      command=lambda: self.oppo_flash_single("recovery")).pack(side="left", padx=3)
        uf2 = ctk.CTkFrame(f)
        uf2.pack(pady=4)
        ctk.CTkButton(uf2, text=self.tr("oppo_unlock_cmd"), width=250,
                      fg_color="orange", hover_color="darkorange",
                      command=self.oppo_unlock).pack(side="left", padx=4)
        ctk.CTkButton(uf2, text=self.tr("oppo_lock_cmd"), width=250,
                      fg_color="red", hover_color="darkred",
                      command=self.oppo_lock).pack(side="left", padx=4)
        ctk.CTkLabel(f, text="— Fastboot ROM —",
                     font=("Arial", 12, "bold"), text_color="lightblue").pack(pady=(15, 3))
        rf = ctk.CTkFrame(f)
        rf.pack(pady=4)
        ctk.CTkButton(rf, text=self.tr("oppo_select_rom"), width=250,
                      command=self.oppo_select_rom).pack(side="left", padx=5)
        self.oppo_rom_label = ctk.CTkLabel(rf, text=self.tr("samsung_no_file"),
                                            font=("Arial", 10), text_color="gray")
        self.oppo_rom_label.pack(side="left", padx=5)
        fl = ctk.CTkFrame(f)
        fl.pack(pady=6)
        ctk.CTkButton(fl, text=self.tr("oppo_flash_wipe"), width=200, height=42,
                      fg_color="green", hover_color="darkgreen",
                      command=lambda: self.oppo_flash_rom(wipe=True)).pack(side="left", padx=4)
        ctk.CTkButton(fl, text=self.tr("oppo_flash_keep"), width=200, height=42,
                      fg_color="orange", hover_color="darkorange",
                      command=lambda: self.oppo_flash_rom(wipe=False)).pack(side="left", padx=4)
        ctk.CTkLabel(f, text="— Partitions —",
                     font=("Arial", 12, "bold"), text_color="lightblue").pack(pady=(15, 3))
        pf = ctk.CTkFrame(f)
        pf.pack(pady=4)
        ctk.CTkButton(pf, text=self.tr("oppo_flash_boot"), width=170,
                      command=lambda: self.oppo_flash_single("boot")).pack(side="left", padx=3)
        ctk.CTkButton(pf, text=self.tr("oppo_flash_vbmeta"), width=170,
                      command=lambda: self.oppo_flash_single("vbmeta")).pack(side="left", padx=3)
        ctk.CTkButton(pf, text=self.tr("oppo_flash_dtbo"), width=170,
                      command=lambda: self.oppo_flash_single("dtbo")).pack(side="left", padx=3)
        ctk.CTkButton(pf, text=self.tr("oppo_flash_super"), width=170,
                      command=lambda: self.oppo_flash_single("super")).pack(side="left", padx=3)
        cf = ctk.CTkFrame(f)
        cf.pack(pady=6)
        ctk.CTkLabel(cf, text=self.tr("oppo_partition")).pack(side="left", padx=4)
        self.oppo_part_name = ctk.CTkEntry(cf, width=140)
        self.oppo_part_name.pack(side="left", padx=4)
        self.oppo_part_name.insert(0, "boot")
        ctk.CTkLabel(cf, text=self.tr("oppo_image")).pack(side="left", padx=4)
        self.oppo_img_file = ctk.CTkEntry(cf, width=220)
        self.oppo_img_file.pack(side="left", padx=4)
        ctk.CTkButton(cf, text=self.tr("pick"), width=60,
                      command=self.oppo_pick_img).pack(side="left", padx=4)
        ctk.CTkButton(cf, text=self.tr("write_btn"), width=90, fg_color="red",
                      hover_color="darkred",
                      command=self.oppo_flash_custom).pack(side="left", padx=4)
        ctk.CTkLabel(f, text=self.tr("advanced"), font=("Arial", 12, "bold"),
                     text_color="orange").pack(pady=(15, 3))
        af = ctk.CTkFrame(f)
        af.pack(pady=4)
        ctk.CTkButton(af, text=self.tr("oppo_erase_frp"), width=200,
                      fg_color="red", hover_color="darkred",
                      command=self.oppo_erase_frp).pack(side="left", padx=3)
        ctk.CTkButton(af, text=self.tr("oppo_wipe_data"), width=200,
                      fg_color="red", hover_color="darkred",
                      command=self.oppo_wipe_data).pack(side="left", padx=3)
        ctk.CTkButton(af, text=self.tr("oppo_edl"), width=200,
                      command=lambda: self.async_run(lambda: run([ADB, "reboot", "edl"]))).pack(side="left", padx=3)

    def oppo_info(self):
        def t():
            self.log("=" * 50)
            for p in ["ro.product.model", "ro.product.brand",
                      "ro.build.version.oplusrom", "ro.build.version.opporom",
                      "ro.build.version.realme", "ro.build.version.oxygen",
                      "ro.build.display.id", "ro.build.version.release",
                      "ro.build.version.sdk", "ro.product.cpu.abi",
                      "ro.serialno", "ro.boot.verifiedbootstate",
                      "ro.boot.flash.locked"]:
                self.log(f"{p}: {run([ADB, 'shell', 'getprop', p]).strip()}")
        threading.Thread(target=t, daemon=True).start()

    def oppo_check_bl(self):
        def t():
            self.log("=" * 50)
            self.log(run([FASTBOOT, "oem", "device-info"], timeout=30))
            self.log(run([FASTBOOT, "getvar", "unlocked"], timeout=15))
            self.log(f"ro.boot.flash.locked: {run([ADB, 'shell', 'getprop', 'ro.boot.flash.locked']).strip()}")
            self.log(f"secureboot.lockstate: {run([ADB, 'shell', 'getprop', 'ro.secureboot.lockstate']).strip()}")
        threading.Thread(target=t, daemon=True).start()

    def oppo_unlock(self):
        if not messagebox.askyesno(self.tr("warn"), self.tr("confirm_unlock")):
            return
        def t():
            self.log("🔓 Trying unlock...")
            self.log(run([FASTBOOT, "flashing", "unlock"], timeout=120))
            self.log(run([FASTBOOT, "oem", "unlock"], timeout=60))
        threading.Thread(target=t, daemon=True).start()

    def oppo_lock(self):
        if not messagebox.askyesno(self.tr("warn"), self.tr("confirm_unlock")):
            return
        self.async_run(lambda: run([FASTBOOT, "flashing", "lock"], timeout=120))

    def oppo_flash_single(self, partition):
        p = filedialog.askopenfilename(filetypes=[("Image", "*.img"), ("All", "*.*")])
        if not p:
            return
        def t():
            self.log(f"🚀 flash {partition}: {os.path.basename(p)}")
            self.log(run([FASTBOOT, "flash", partition, p], timeout=900)[-1000:])
        threading.Thread(target=t, daemon=True).start()

    def oppo_pick_img(self):
        p = filedialog.askopenfilename(filetypes=[("Image", "*.img")])
        if p:
            self.oppo_img_file.delete(0, "end")
            self.oppo_img_file.insert(0, p)

    def oppo_flash_custom(self):
        part = self.oppo_part_name.get().strip()
        f = self.oppo_img_file.get().strip()
        if not part or not os.path.exists(f):
            messagebox.showerror(self.tr("err"), self.tr("err_check"))
            return
        def t():
            self.log(run([FASTBOOT, "flash", part, f], timeout=900)[-1000:])
        threading.Thread(target=t, daemon=True).start()

    def oppo_erase_frp(self):
        if not messagebox.askyesno(self.tr("warn"), self.tr("confirm_wipe")):
            return
        self.async_run(lambda: run([FASTBOOT, "erase", "frp"], timeout=120))

    def oppo_wipe_data(self):
        if not messagebox.askyesno(self.tr("warn"), self.tr("confirm_format")):
            return
        self.async_run(lambda: run([FASTBOOT, "erase", "userdata"], timeout=300))

    def oppo_select_rom(self):
        p = filedialog.askopenfilename(
            filetypes=[("ROM", "*.zip *.tar *.tgz *.img"), ("All", "*.*")])
        if p:
            self.oppo_rom = p
            self.oppo_rom_label.configure(text=os.path.basename(p),
                                           text_color="lightgreen")
            self.log(f"🟢 ROM: {os.path.basename(p)}")

    def oppo_flash_rom(self, wipe=False):
        if not self.oppo_rom or not os.path.exists(self.oppo_rom):
            messagebox.showerror(self.tr("err"), self.tr("samsung_no_file"))
            return
        if not messagebox.askyesno(self.tr("confirm"),
                                    self.tr("confirm_flash_samsung",
                                            os.path.basename(self.oppo_rom))):
            return
        def t():
            try:
                if os.path.exists(TEMP_FLASH):
                    shutil.rmtree(TEMP_FLASH, ignore_errors=True)
                os.makedirs(TEMP_FLASH, exist_ok=True)
                name = os.path.basename(self.oppo_rom).lower()
                self.log("📦 Extracting Oppo/Realme ROM...")
                if name.endswith(".zip"):
                    with zipfile.ZipFile(self.oppo_rom) as z:
                        z.extractall(TEMP_FLASH)
                elif name.endswith((".tgz", ".tar.gz", ".tar")):
                    try:
                        with tarfile.open(self.oppo_rom, "r:gz") as tar:
                            tar.extractall(TEMP_FLASH)
                    except tarfile.ReadError:
                        with tarfile.open(self.oppo_rom, "r:") as tar:
                            tar.extractall(TEMP_FLASH)
                payloads = []
                for root, dirs, files in os.walk(TEMP_FLASH):
                    for f in files:
                        if f == "payload.bin":
                            payloads.append(os.path.join(root, f))
                if payloads:
                    self.log("⚠️ payload.bin detected")
                    try:
                        p_url = "https://github.com/ssut/payload-dumper-go/releases/download/1.2.2/payload-dumper-go_1.2.2_windows_amd64.tar.gz"
                        tgz = os.path.join(BASE_DIR, "pdg.tgz")
                        urllib.request.urlretrieve(p_url, tgz)
                        with tarfile.open(tgz, "r:gz") as t_:
                            t_.extractall(BASE_DIR)
                        os.remove(tgz)
                        exe = os.path.join(BASE_DIR, "payload-dumper-go.exe")
                        if os.path.exists(exe):
                            out_dir = os.path.join(TEMP_FLASH, "extracted")
                            os.makedirs(out_dir, exist_ok=True)
                            for pl in payloads:
                                self.log(f"🔧 {os.path.basename(pl)}...")
                                self.log(run([exe, "-o", out_dir, pl], timeout=1800))
                    except Exception as e:
                        self.log(f"⚠️ {e}")
                images = {}
                for root, dirs, files in os.walk(TEMP_FLASH):
                    for f in files:
                        if f.endswith(".img"):
                            n = os.path.splitext(f)[0]
                            images[n] = os.path.join(root, f)
                if not images:
                    self.log("❌ No images")
                    return
                order = ["gpt", "tz", "xbl", "abl", "aop", "bluetooth",
                          "keymaster", "devcfg", "dsp", "featenabler",
                          "hyp", "imagefv", "qupfw", "shrm", "uefisecapp",
                          "vbmeta_system", "vbmeta_vendor", "vbmeta", "modem",
                          "boot", "dtbo", "recovery", "super",
                          "my_bigball", "my_carrier", "my_company",
                          "my_engineering", "my_heytap", "my_manifest",
                          "my_product", "my_region", "my_stock",
                          "odm", "product", "system", "system_ext",
                          "vendor", "persist", "metadata", "userdata"]
                for part in order:
                    if part not in images:
                        continue
                    if wipe and part == "userdata":
                        continue
                    self.log(f"🚀 flash {part}")
                    self.log(run([FASTBOOT, "flash", part, images[part]], timeout=1800)[-300:])
                for part, path in images.items():
                    if part in order or (wipe and part == "userdata"):
                        continue
                    self.log(f"🚀 flash {part}")
                    self.log(run([FASTBOOT, "flash", part, path], timeout=1800)[-300:])
                self.log("🎉 Oppo/Realme ROM flashed!")
                run([FASTBOOT, "reboot"])
            except Exception as e:
                self.log(f"❌ {e}")
        threading.Thread(target=t, daemon=True).start()

    def build_vivo_tab(self):
        f = self.tab_vivo
        ctk.CTkLabel(f, text=self.tr("vivo_title"),
                     font=("Arial", 16, "bold")).pack(pady=6)
        ctk.CTkLabel(f, text=self.tr("vivo_warning"),
                     font=("Arial", 11), text_color="orange").pack(pady=4)
        row = ctk.CTkFrame(f)
        row.pack(pady=6)
        ctk.CTkButton(row, text=self.tr("vivo_info"), width=170,
                      command=self.vivo_info).pack(side="left", padx=4)
        ctk.CTkButton(row, text=self.tr("vivo_check_bl"), width=170,
                      command=self.vivo_check_bl).pack(side="left", padx=4)
        ctk.CTkButton(row, text=self.tr("vivo_fastboot"), width=170,
                      command=lambda: self.async_run(lambda: run([ADB, "reboot", "bootloader"]))).pack(side="left", padx=4)
        ctk.CTkLabel(f, text="— Unlock Tools —",
                     font=("Arial", 12, "bold"), text_color="lightblue").pack(pady=(15, 3))
        uf = ctk.CTkFrame(f)
        uf.pack(pady=4)
        ctk.CTkButton(uf, text=self.tr("vivo_unlock_help"), width=220,
                      fg_color="gray",
                      command=lambda: webbrowser.open("https://www.vivo.com/en/support/")).pack(side="left", padx=3)
        ctk.CTkButton(uf, text=self.tr("vivo_download_help"), width=220,
                      fg_color="gray",
                      command=lambda: webbrowser.open("https://www.vivo.com/en/support/faq")).pack(side="left", padx=3)
        ctk.CTkButton(uf, text=self.tr("vivo_flash_recovery"), width=220,
                      command=lambda: self.vivo_flash_single("recovery")).pack(side="left", padx=3)
        uf2 = ctk.CTkFrame(f)
        uf2.pack(pady=4)
        ctk.CTkButton(uf2, text=self.tr("vivo_unlock_cmd"), width=250,
                      fg_color="orange", hover_color="darkorange",
                      command=self.vivo_unlock).pack(side="left", padx=4)
        ctk.CTkButton(uf2, text=self.tr("vivo_lock_cmd"), width=250,
                      fg_color="red", hover_color="darkred",
                      command=self.vivo_lock).pack(side="left", padx=4)
        ctk.CTkLabel(f, text="— Fastboot ROM —",
                     font=("Arial", 12, "bold"), text_color="lightblue").pack(pady=(15, 3))
        rf = ctk.CTkFrame(f)
        rf.pack(pady=4)
        ctk.CTkButton(rf, text=self.tr("vivo_select_rom"), width=250,
                      command=self.vivo_select_rom).pack(side="left", padx=5)
        self.vivo_rom_label = ctk.CTkLabel(rf, text=self.tr("samsung_no_file"),
                                            font=("Arial", 10), text_color="gray")
        self.vivo_rom_label.pack(side="left", padx=5)
        fl = ctk.CTkFrame(f)
        fl.pack(pady=6)
        ctk.CTkButton(fl, text=self.tr("vivo_flash_wipe"), width=200, height=42,
                      fg_color="green", hover_color="darkgreen",
                      command=lambda: self.vivo_flash_rom(wipe=True)).pack(side="left", padx=4)
        ctk.CTkButton(fl, text=self.tr("vivo_flash_keep"), width=200, height=42,
                      fg_color="orange", hover_color="darkorange",
                      command=lambda: self.vivo_flash_rom(wipe=False)).pack(side="left", padx=4)
        ctk.CTkLabel(f, text="— Partitions —",
                     font=("Arial", 12, "bold"), text_color="lightblue").pack(pady=(15, 3))
        pf = ctk.CTkFrame(f)
        pf.pack(pady=4)
        ctk.CTkButton(pf, text=self.tr("vivo_flash_boot"), width=170,
                      command=lambda: self.vivo_flash_single("boot")).pack(side="left", padx=3)
        ctk.CTkButton(pf, text=self.tr("vivo_flash_vbmeta"), width=170,
                      command=lambda: self.vivo_flash_single("vbmeta")).pack(side="left", padx=3)
        ctk.CTkButton(pf, text=self.tr("vivo_flash_dtbo"), width=170,
                      command=lambda: self.vivo_flash_single("dtbo")).pack(side="left", padx=3)
        ctk.CTkButton(pf, text=self.tr("vivo_flash_super"), width=170,
                      command=lambda: self.vivo_flash_single("super")).pack(side="left", padx=3)
        cf = ctk.CTkFrame(f)
        cf.pack(pady=6)
        ctk.CTkLabel(cf, text=self.tr("vivo_partition")).pack(side="left", padx=4)
        self.vivo_part_name = ctk.CTkEntry(cf, width=140)
        self.vivo_part_name.pack(side="left", padx=4)
        self.vivo_part_name.insert(0, "boot")
        ctk.CTkLabel(cf, text=self.tr("vivo_image")).pack(side="left", padx=4)
        self.vivo_img_file = ctk.CTkEntry(cf, width=220)
        self.vivo_img_file.pack(side="left", padx=4)
        ctk.CTkButton(cf, text=self.tr("pick"), width=60,
                      command=self.vivo_pick_img).pack(side="left", padx=4)
        ctk.CTkButton(cf, text=self.tr("write_btn"), width=90, fg_color="red",
                      hover_color="darkred",
                      command=self.vivo_flash_custom).pack(side="left", padx=4)
        ctk.CTkLabel(f, text=self.tr("advanced"), font=("Arial", 12, "bold"),
                     text_color="orange").pack(pady=(15, 3))
        af = ctk.CTkFrame(f)
        af.pack(pady=4)
        ctk.CTkButton(af, text=self.tr("vivo_erase_frp"), width=200,
                      fg_color="red", hover_color="darkred",
                      command=self.vivo_erase_frp).pack(side="left", padx=3)
        ctk.CTkButton(af, text=self.tr("vivo_wipe_data"), width=200,
                      fg_color="red", hover_color="darkred",
                      command=self.vivo_wipe_data).pack(side="left", padx=3)
        ctk.CTkButton(af, text=self.tr("vivo_edl"), width=200,
                      command=lambda: self.async_run(lambda: run([ADB, "reboot", "edl"]))).pack(side="left", padx=3)

    def vivo_info(self):
        def t():
            self.log("=" * 50)
            for p in ["ro.product.model", "ro.product.brand",
                      "ro.build.version.vivo", "ro.build.version.funtouch",
                      "ro.build.version.originos", "ro.build.display.id",
                      "ro.build.version.release", "ro.build.version.sdk",
                      "ro.product.cpu.abi", "ro.serialno",
                      "ro.boot.verifiedbootstate", "ro.boot.flash.locked"]:
                self.log(f"{p}: {run([ADB, 'shell', 'getprop', p]).strip()}")
        threading.Thread(target=t, daemon=True).start()

    def vivo_check_bl(self):
        def t():
            self.log("=" * 50)
            self.log(run([FASTBOOT, "oem", "device-info"], timeout=30))
            self.log(run([FASTBOOT, "getvar", "unlocked"], timeout=15))
            self.log(f"ro.boot.flash.locked: {run([ADB, 'shell', 'getprop', 'ro.boot.flash.locked']).strip()}")
        threading.Thread(target=t, daemon=True).start()

    def vivo_unlock(self):
        if not messagebox.askyesno(self.tr("warn"), self.tr("confirm_unlock")):
            return
        def t():
            self.log("🔓 Trying unlock...")
            self.log(run([FASTBOOT, "flashing", "unlock"], timeout=120))
            self.log(run([FASTBOOT, "oem", "unlock"], timeout=60))
        threading.Thread(target=t, daemon=True).start()

    def vivo_lock(self):
        if not messagebox.askyesno(self.tr("warn"), self.tr("confirm_unlock")):
            return
        self.async_run(lambda: run([FASTBOOT, "flashing", "lock"], timeout=120))

    def vivo_flash_single(self, partition):
        p = filedialog.askopenfilename(filetypes=[("Image", "*.img"), ("All", "*.*")])
        if not p:
            return
        def t():
            self.log(f"🚀 flash {partition}: {os.path.basename(p)}")
            self.log(run([FASTBOOT, "flash", partition, p], timeout=900)[-1000:])
        threading.Thread(target=t, daemon=True).start()

    def vivo_pick_img(self):
        p = filedialog.askopenfilename(filetypes=[("Image", "*.img")])
        if p:
            self.vivo_img_file.delete(0, "end")
            self.vivo_img_file.insert(0, p)

    def vivo_flash_custom(self):
        part = self.vivo_part_name.get().strip()
        f = self.vivo_img_file.get().strip()
        if not part or not os.path.exists(f):
            messagebox.showerror(self.tr("err"), self.tr("err_check"))
            return
        def t():
            self.log(run([FASTBOOT, "flash", part, f], timeout=900)[-1000:])
        threading.Thread(target=t, daemon=True).start()

    def vivo_erase_frp(self):
        if not messagebox.askyesno(self.tr("warn"), self.tr("confirm_wipe")):
            return
        self.async_run(lambda: run([FASTBOOT, "erase", "frp"], timeout=120))

    def vivo_wipe_data(self):
        if not messagebox.askyesno(self.tr("warn"), self.tr("confirm_format")):
            return
        self.async_run(lambda: run([FASTBOOT, "erase", "userdata"], timeout=300))

    def vivo_select_rom(self):
        p = filedialog.askopenfilename(
            filetypes=[("ROM", "*.zip *.tar *.tgz *.img"), ("All", "*.*")])
        if p:
            self.vivo_rom = p
            self.vivo_rom_label.configure(text=os.path.basename(p),
                                           text_color="lightgreen")
            self.log(f"🔵 ROM: {os.path.basename(p)}")

    def vivo_flash_rom(self, wipe=False):
        if not self.vivo_rom or not os.path.exists(self.vivo_rom):
            messagebox.showerror(self.tr("err"), self.tr("samsung_no_file"))
            return
        if not messagebox.askyesno(self.tr("confirm"),
                                    self.tr("confirm_flash_samsung",
                                            os.path.basename(self.vivo_rom))):
            return
        def t():
            try:
                if os.path.exists(TEMP_FLASH):
                    shutil.rmtree(TEMP_FLASH, ignore_errors=True)
                os.makedirs(TEMP_FLASH, exist_ok=True)
                name = os.path.basename(self.vivo_rom).lower()
                self.log("📦 Extracting Vivo ROM...")
                if name.endswith(".zip"):
                    with zipfile.ZipFile(self.vivo_rom) as z:
                        z.extractall(TEMP_FLASH)
                elif name.endswith((".tgz", ".tar.gz", ".tar")):
                    try:
                        with tarfile.open(self.vivo_rom, "r:gz") as tar:
                            tar.extractall(TEMP_FLASH)
                    except tarfile.ReadError:
                        with tarfile.open(self.vivo_rom, "r:") as tar:
                            tar.extractall(TEMP_FLASH)
                payloads = []
                for root, dirs, files in os.walk(TEMP_FLASH):
                    for f in files:
                        if f == "payload.bin":
                            payloads.append(os.path.join(root, f))
                if payloads:
                    self.log("⚠️ payload.bin detected")
                    try:
                        p_url = "https://github.com/ssut/payload-dumper-go/releases/download/1.2.2/payload-dumper-go_1.2.2_windows_amd64.tar.gz"
                        tgz = os.path.join(BASE_DIR, "pdg.tgz")
                        urllib.request.urlretrieve(p_url, tgz)
                        with tarfile.open(tgz, "r:gz") as t_:
                            t_.extractall(BASE_DIR)
                        os.remove(tgz)
                        exe = os.path.join(BASE_DIR, "payload-dumper-go.exe")
                        if os.path.exists(exe):
                            out_dir = os.path.join(TEMP_FLASH, "extracted")
                            os.makedirs(out_dir, exist_ok=True)
                            for pl in payloads:
                                self.log(f"🔧 {os.path.basename(pl)}...")
                                self.log(run([exe, "-o", out_dir, pl], timeout=1800))
                    except Exception as e:
                        self.log(f"⚠️ {e}")
                images = {}
                for root, dirs, files in os.walk(TEMP_FLASH):
                    for f in files:
                        if f.endswith(".img"):
                            n = os.path.splitext(f)[0]
                            images[n] = os.path.join(root, f)
                if not images:
                    self.log("❌ No images")
                    return
                order = ["gpt", "tz", "xbl", "abl", "aop", "bluetooth",
                          "keymaster", "devcfg", "dsp", "featenabler",
                          "hyp", "imagefv", "qupfw", "shrm", "uefisecapp",
                          "vbmeta_system", "vbmeta_vendor", "vbmeta", "modem",
                          "boot", "dtbo", "recovery", "super",
                          "system", "system_ext", "vendor", "product", "odm",
                          "persist", "metadata", "userdata"]
                for part in order:
                    if part not in images:
                        continue
                    if wipe and part == "userdata":
                        continue
                    self.log(f"🚀 flash {part}")
                    self.log(run([FASTBOOT, "flash", part, images[part]], timeout=1800)[-300:])
                for part, path in images.items():
                    if part in order or (wipe and part == "userdata"):
                        continue
                    self.log(f"🚀 flash {part}")
                    self.log(run([FASTBOOT, "flash", part, path], timeout=1800)[-300:])
                self.log("🎉 Vivo ROM flashed!")
                run([FASTBOOT, "reboot"])
            except Exception as e:
                self.log(f"❌ {e}")
        threading.Thread(target=t, daemon=True).start()

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
            c = (out + out2).lower()
            if "unlocked: yes" in c or "true" in c:
                self.bl_status_label.configure(text=self.tr("bl_unlocked"),
                                                text_color="lightgreen")
            elif "unlocked: no" in c or "false" in c:
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
            self.log(run([FASTBOOT, "flashing", "unlock"], timeout=120))
        threading.Thread(target=t, daemon=True).start()

    def lock_bootloader(self):
        if not messagebox.askyesno(self.tr("warn"), self.tr("unlock_confirm")):
            return
        self.async_run(lambda: run([FASTBOOT, "flashing", "lock"], timeout=120))

    def pick_recovery(self):
        p = filedialog.askopenfilename(filetypes=[("Recovery", "*.img"), ("All", "*.*")])
        if p:
            self.recovery_img = p
            self.recovery_label.configure(text=os.path.basename(p),
                                           text_color="lightgreen")

    def pick_boot(self):
        p = filedialog.askopenfilename(filetypes=[("Boot", "*.img"), ("All", "*.*")])
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

    def build_adv_tab(self):
        f = self.tab_adv
        ctk.CTkLabel(f, text=self.tr("adv_title"),
                     font=("Arial", 16, "bold")).pack(pady=10)

        ctk.CTkButton(f, text=self.tr("adv_adb_terminal"), width=400, height=50,
                      fg_color="green", hover_color="darkgreen",
                      font=("Arial", 14, "bold"),
                      command=self.adv_adb_terminal).pack(pady=5)
        ctk.CTkLabel(f, text=self.tr("adv_adb_terminal_desc"),
                     font=("Arial", 11), text_color="gray").pack()

        ctk.CTkButton(f, text=self.tr("adv_install_batch"), width=400, height=50,
                      fg_color="green", hover_color="darkgreen",
                      font=("Arial", 14, "bold"),
                      command=self.adv_install_batch).pack(pady=5)
        ctk.CTkLabel(f, text=self.tr("adv_install_batch_desc"),
                     font=("Arial", 11), text_color="gray").pack()

        ctk.CTkLabel(f, text="—", text_color="gray").pack(pady=10)

        row1 = ctk.CTkFrame(f)
        row1.pack(pady=5)
        ctk.CTkButton(row1, text=self.tr("adv_battery_calib"), width=200,
                      fg_color="orange", hover_color="darkorange",
                      command=self.adv_battery_calib).pack(side="left", padx=5)
        ctk.CTkButton(row1, text=self.tr("adv_network_info"), width=200,
                      command=self.adv_network_info).pack(side="left", padx=5)

        row2 = ctk.CTkFrame(f)
        row2.pack(pady=5)
        ctk.CTkButton(row2, text=self.tr("adv_hide_app"), width=200,
                      fg_color="orange", hover_color="darkorange",
                      command=self.adv_hide_app).pack(side="left", padx=5)
        ctk.CTkButton(row2, text=self.tr("adv_show_app"), width=200,
                      fg_color="green", hover_color="darkgreen",
                      command=self.adv_show_app).pack(side="left", padx=5)

        row3 = ctk.CTkFrame(f)
        row3.pack(pady=5)
        ctk.CTkButton(row3, text=self.tr("adv_fastboot_info"), width=200,
                      command=self.adv_fastboot_info).pack(side="left", padx=5)
        ctk.CTkButton(row3, text=self.tr("adv_device_props"), width=200,
                      command=self.adv_device_props).pack(side="left", padx=5)

        ctk.CTkLabel(f, text="—", text_color="gray").pack(pady=10)

        row4 = ctk.CTkFrame(f)
        row4.pack(pady=5)
        ctk.CTkButton(row4, text=self.tr("adv_reboot_bootloader"), width=200,
                      command=lambda: self.async_run(lambda: run([ADB, "reboot", "bootloader"]))).pack(side="left", padx=5)
        ctk.CTkButton(row4, text=self.tr("adv_reboot_recovery"), width=200,
                      command=lambda: self.async_run(lambda: run([ADB, "reboot", "recovery"]))).pack(side="left", padx=5)

        row5 = ctk.CTkFrame(f)
        row5.pack(pady=5)
        ctk.CTkButton(row5, text=self.tr("adv_reboot_download"), width=200,
                      command=lambda: self.async_run(lambda: run([ADB, "reboot", "download"]))).pack(side="left", padx=5)

    def adv_adb_terminal(self):
        cmd = ctk.CTkInputDialog(
            text=self.tr("adv_adb_prompt"),
            title="ADB Command").get_input()
        if not cmd:
            return
        def t():
            self.log(f"$ adb {cmd}")
            self.log(run([ADB] + cmd.split(), timeout=120))
        threading.Thread(target=t, daemon=True).start()

    def adv_install_batch(self):
        folder = filedialog.askdirectory(title=self.tr("adv_pick_folder"))
        if not folder:
            return
        def t():
            apks = [f for f in os.listdir(folder) if f.lower().endswith(".apk")]
            if not apks:
                self.log(self.tr("adv_no_apk"))
                return
            count = 0
            for apk in apks:
                full = os.path.join(folder, apk)
                self.log(self.tr("adv_installing", apk))
                out = run([ADB, "install", "-r", full], timeout=300)
                if "Success" in out:
                    count += 1
            self.log(self.tr("adv_install_count", count))
        threading.Thread(target=t, daemon=True).start()

    def adv_battery_calib(self):
        if not messagebox.askyesno(self.tr("warn"), self.tr("adv_battery_warn")):
            return
        def t():
            self.log("🔋 Clearing battery stats...")
            run([ADB, "shell", "su", "-c", "rm -f /data/system/batterystats.bin"])
            self.log(self.tr("adv_battery_done"))
        threading.Thread(target=t, daemon=True).start()

    def adv_network_info(self):
        def t():
            self.log(self.tr("adv_network_loading"))
            self.log("=" * 50)
            self.log("IP Address:")
            self.log(run([ADB, "shell", "ip", "addr", "show", "wlan0"]))
            self.log("Wi-Fi Status:")
            self.log(run([ADB, "shell", "dumpsys", "wifi"]))
            self.log("Data Connection:")
            self.log(run([ADB, "shell", "dumpsys", "telephony.registry"]))
        threading.Thread(target=t, daemon=True).start()

    def adv_hide_app(self):
        pkg = ctk.CTkInputDialog(text=self.tr("adv_hide_app_prompt"), title="Hide App").get_input()
        if not pkg:
            return
        def t():
            run([ADB, "shell", "pm", "hide", pkg])
            self.log(self.tr("adv_app_hidden", pkg))
        threading.Thread(target=t, daemon=True).start()

    def adv_show_app(self):
        pkg = ctk.CTkInputDialog(text=self.tr("adv_hide_app_prompt"), title="Unhide App").get_input()
        if not pkg:
            return
        def t():
            run([ADB, "shell", "pm", "unhide", pkg])
            self.log(self.tr("adv_app_shown", pkg))
        threading.Thread(target=t, daemon=True).start()

    def adv_fastboot_info(self):
        def t():
            self.log(self.tr("adv_fastboot_info_loading"))
            self.log("=" * 50)
            self.log(run([FASTBOOT, "getvar", "all"], timeout=30))
        threading.Thread(target=t, daemon=True).start()

    def adv_device_props(self):
        def t():
            self.log(self.tr("adv_device_props_loading"))
            self.log("=" * 50)
            self.log(run([ADB, "shell", "getprop"], timeout=30))
        threading.Thread(target=t, daemon=True).start()

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
        self.flash_type_label.configure(text=self.tr("flash_type", self.tr(type_key)))

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
                    images[os.path.splitext(f)[0]] = os.path.join(root, f)
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
                    self.flash_status.configure(text=self.tr("flash_status_extracting_payload"))
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
                    if "FAILED" in out and self.chk_stop.get():
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

def show_splash():
    splash = ctk.CTk()
    splash.title("Android Tool")
    splash.geometry("500x300")
    splash.resizable(False, False)

    sw = splash.winfo_screenwidth()
    sh = splash.winfo_screenheight()
    x = (sw - 500) // 2
    y = (sh - 300) // 2
    splash.geometry(f"500x300+{x}+{y}")

    frame = ctk.CTkFrame(splash, fg_color="#1a1a2e", corner_radius=0)
    frame.pack(fill="both", expand=True)

    ctk.CTkLabel(frame, text="🛠️", font=("Arial", 60)).pack(pady=(30, 5))
    ctk.CTkLabel(frame, text="Android Tool",
                 font=("Arial", 28, "bold"),
                 text_color="#4ade80").pack()
    ctk.CTkLabel(frame, text=f"Version {APP_VERSION}",
                 font=("Arial", 12),
                 text_color="gray").pack(pady=5)
    ctk.CTkLabel(frame, text="Loading...",
                 font=("Arial", 12),
                 text_color="lightblue").pack(pady=20)

    bar = ctk.CTkProgressBar(frame, width=350, height=15,
                               progress_color="#4ade80")
    bar.pack(pady=5)
    bar.set(0)

    splash.update()

    def animate():
        for i in range(101):
            bar.set(i / 100)
            splash.update()
            time.sleep(0.02)
        splash.destroy()

    animate()

def main():
    if not is_activated():
        def start_main():
            app = App()
            app.mainloop()

        lic = LicenseWindow(on_success=start_main)
        lic.mainloop()
    else:
        app = App()
        app.mainloop()

if __name__ == "__main__":
    show_splash()
    main()