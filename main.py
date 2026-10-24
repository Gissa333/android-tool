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


def run_bytes(cmd, timeout=60, cwd=None):
    try:
        r = subprocess.run(cmd, capture_output=True, timeout=timeout,
                           cwd=cwd, creationflags=NO_WINDOW)
        return r.stdout or b""
    except Exception:
        return b""


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


def safe_extract_tar(tar_path, dest):
    try:
        with tarfile.open(tar_path, "r:*") as tar:
            try:
                tar.extractall(dest, filter="data")
            except TypeError:
                tar.extractall(dest)
    except tarfile.TarError:
        with tarfile.open(tar_path, "r:") as tar:
            try:
                tar.extractall(dest, filter="data")
            except TypeError:
                tar.extractall(dest)


def safe_extract_zip(zip_path, dest):
    with zipfile.ZipFile(zip_path) as z:
        z.extractall(dest)


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
        """Thread-safe UI update."""
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

    # ---------- About ----------
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

    # ---------- ADB ----------
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

    # ---------- Daily Tools ----------
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
        ctk.CTkButton(info_frame, text=self.tr("tools_list_packages"), width=170, height=45,
                      command=self.tool_list_packages).pack(side="left", padx=5)
        ctk.CTkButton(f, text=self.tr("tools_export_dir"), width=350, height=45,
                      fg_color="gray", command=self.open_exports).pack(pady=15)

    def _no_device(self):
        out = run([ADB, "get-state"], timeout=10)
        return "device" not in out.lower()

    def tool_screenshot(self):
        def t():
            if self._no_device():
                self.log(self.tr("tools_no_device"))
                return
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            path = os.path.join(EXPORTS_DIR, "screenshot_" + ts + ".png")
            data = run_bytes([ADB, "exec-out", "screencap", "-p"], timeout=30)
            if data:
                with open(path, "wb") as fh:
                    fh.write(data)
                self.log(self.tr("tools_screenshot_saved", path))
            else:
                self.log(self.tr("msg_error", "screencap failed"))
        threading.Thread(target=t, daemon=True).start()

    def tool_record(self):
        if self.recording:
            return
        self.recording = True

        def t():
            try:
                if self._no_device():
                    self.log(self.tr("tools_no_device"))
                    return
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                remote = "/sdcard/rec_" + ts + ".mp4"
                local = os.path.join(EXPORTS_DIR, "record_" + ts + ".mp4")
                self.log(self.tr("tools_recording"))
                subprocess.run([ADB, "shell", "screenrecord", "--time-limit", "15", remote],
                               capture_output=True, timeout=40, creationflags=NO_WINDOW)
                run([ADB, "pull", remote, local], timeout=180)
                run([ADB, "shell", "rm", "-f", remote], timeout=15)
                if os.path.exists(local):
                    self.log(self.tr("tools_recorded", local))
                else:
                    self.log(self.tr("msg_error", "pull failed"))
            finally:
                self.recording = False

        threading.Thread(target=t, daemon=True).start()

    def tool_record_stop(self):
        run([ADB, "shell", "pkill", "-INT", "screenrecord"], timeout=10)
        self.log(self.tr("tools_record_stop"))

    def tool_install_apk(self):
        p = filedialog.askopenfilename(filetypes=[("APK", "*.apk"), ("All", "*.*")])
        if not p:
            return

        def t():
            if self._no_device():
                self.log(self.tr("tools_no_device"))
                return
            name = os.path.basename(p)
            self.log(self.tr("adv_installing", name))
            out = run([ADB, "install", "-r", p], timeout=600)
            if "Success" in out:
                self.log(self.tr("tools_install_success", name))
            else:
                self.log(self.tr("tools_install_fail", name))
                self.log(out[-500:])

        threading.Thread(target=t, daemon=True).start()

    def _ask(self, text, title):
        root = Tk()
        root.withdraw()
        try:
            from tkinter import simpledialog
            res = simpledialog.askstring(title, text, parent=root)
        finally:
            root.destroy()
        return res

    def tool_push(self):
        src = filedialog.askopenfilename()
        if not src:
            return
        dst = self._ask("Destination path (e.g. /sdcard/):", "Push")
        if not dst:
            return
        self.async_run(lambda: run([ADB, "push", src, dst], timeout=1800))

    def tool_pull(self):
        src = self._ask("Remote path:", "Pull")
        if not src:
            return
        self.async_run(lambda: run([ADB, "pull", src, EXPORTS_DIR], timeout=3600))

    def tool_battery(self):
        self.async_run(lambda: run([ADB, "shell", "dumpsys", "battery"], timeout=30))

    def tool_list_packages(self):
        self.async_run(lambda: run([ADB, "shell", "pm", "list", "packages"], timeout=60))

    # ---------- System Tools ----------
    def build_system_tab(self):
        f = self.tab_system
        ctk.CTkLabel(f, text=self.tr("sys_title"), font=("Arial", 16, "bold")).pack(pady=10)
        row1 = ctk.CTkFrame(f)
        row1.pack(pady=4)
        ctk.CTkButton(row1, text=self.tr("sys_nav_hide"), width=200, fg_color="orange",
                      hover_color="darkorange", command=self.sys_hide_nav).pack(side="left", padx=3)
        ctk.CTkButton(row1, text=self.tr("sys_nav_show"), width=200, fg_color="green",
                      hover_color="darkgreen", command=self.sys_show_nav).pack(side="left", padx=3)
        ctk.CTkLabel(f, text=self.tr("sys_dpi_title"), font=("Arial", 12, "bold")).pack(pady=(15, 3))
        row2 = ctk.CTkFrame(f)
        row2.pack(pady=4)
        self.dpi_entry = ctk.CTkEntry(row2, width=120, placeholder_text=self.tr("sys_dpi_placeholder"))
        self.dpi_entry.pack(side="left", padx=5)
        ctk.CTkButton(row2, text=self.tr("sys_dpi_apply"), width=150,
                      command=self.sys_dpi_apply).pack(side="left", padx=5)
        ctk.CTkButton(row2, text=self.tr("sys_dpi_reset"), width=150, fg_color="red",
                      hover_color="darkred", command=self.sys_dpi_reset).pack(side="left", padx=5)
        ctk.CTkLabel(f, text=self.tr("sys_anim"), font=("Arial", 12, "bold")).pack(pady=(15, 3))
        row3 = ctk.CTkFrame(f)
        row3.pack(pady=4)
        ctk.CTkButton(row3, text=self.tr("sys_anim_fast"), width=170, fg_color="green",
                      hover_color="darkgreen", command=self.sys_anim_fast).pack(side="left", padx=3)
        ctk.CTkButton(row3, text=self.tr("sys_anim_normal"), width=170, fg_color="gray",
                      command=self.sys_anim_normal).pack(side="left", padx=3)
        row4 = ctk.CTkFrame(f)
        row4.pack(pady=4)
        self.anim_entry = ctk.CTkEntry(row4, width=120, placeholder_text=self.tr("sys_anim_value"))
        self.anim_entry.pack(side="left", padx=5)
        ctk.CTkButton(row4, text=self.tr("sys_anim_apply"), width=120,
                      command=self.sys_anim_custom).pack(side="left", padx=5)
        ctk.CTkLabel(f, text="—", text_color="gray").pack(pady=10)
        row5 = ctk.CTkFrame(f)
        row5.pack(pady=4)
        ctk.CTkButton(row5, text=self.tr("sys_sysui"), width=220, fg_color="orange",
                      hover_color="darkorange", command=self.sys_restart_sysui).pack(side="left", padx=3)
        ctk.CTkButton(row5, text=self.tr("sys_restart"), width=220, fg_color="red",
                      hover_color="darkred", command=self.sys_restart_device).pack(side="left", padx=3)
        ctk.CTkLabel(f, text=self.tr("sys_gms"), font=("Arial", 12, "bold")).pack(pady=(15, 3))
        row6 = ctk.CTkFrame(f)
        row6.pack(pady=4)
        ctk.CTkButton(row6, text=self.tr("sys_gms_disable"), width=170, fg_color="orange",
                      hover_color="darkorange", command=self.sys_gms_disable).pack(side="left", padx=3)
        ctk.CTkButton(row6, text=self.tr("sys_gms_enable"), width=170, fg_color="green",
                      hover_color="darkgreen", command=self.sys_gms_enable).pack(side="left", padx=3)

    def sys_hide_nav(self):
        self.async_run(lambda: run([ADB, "shell", "settings", "put", "global",
                                    "policy_control", "immersive.full=*"]) or self.tr("sys_applied"))

    def sys_show_nav(self):
        self.async_run(lambda: run([ADB, "shell", "settings", "put", "global",
                                    "policy_control", "null"]) or self.tr("sys_applied"))

    def sys_dpi_apply(self):
        val = self.dpi_entry.get().strip()
        if not val.isdigit():
            messagebox.showerror(self.tr("err"), self.tr("err_check"))
            return
        self.async_run(lambda: run([ADB, "shell", "wm", "density", val]) or self.tr("sys_applied"))

    def sys_dpi_reset(self):
        if not messagebox.askyesno(self.tr("warn"), self.tr("confirm_reset_dpi")):
            return
        self.async_run(lambda: run([ADB, "shell", "wm", "density", "reset"]) or self.tr("sys_reset"))

    def _set_anim(self, val, msg_key):
        for key in ["window_animation_scale", "transition_animation_scale", "animator_duration_scale"]:
            run([ADB, "shell", "settings", "put", "global", key, val])
        return self.tr(msg_key)

    def sys_anim_fast(self):
        self.async_run(lambda: self._set_anim("0.5", "sys_applied"))

    def sys_anim_normal(self):
        self.async_run(lambda: self._set_anim("1.0", "sys_reset"))

    def sys_anim_custom(self):
        val = self.anim_entry.get().strip()
        try:
            float(val)
        except ValueError:
            messagebox.showerror(self.tr("err"), self.tr("err_check"))
            return
        self.async_run(lambda: self._set_anim(val, "sys_applied"))

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
            run([ADB, "shell", "pm", "disable-user", "--user", "0", "com.google.android.gms"])
            run([ADB, "shell", "pm", "disable-user", "--user", "0", "com.android.vending"])
            self.log(self.tr("sys_gms_disabled"))
        threading.Thread(target=t, daemon=True).start()

    def sys_gms_enable(self):
        def t():
            run([ADB, "shell", "pm", "enable", "com.google.android.gms"])
            run([ADB, "shell", "pm", "enable", "com.android.vending"])
            self.log(self.tr("sys_gms_enabled"))
        threading.Thread(target=t, daemon=True).start()

    # ---------- Gaming ----------
    def build_gaming_tab(self):
        f = self.tab_gaming
        ctk.CTkLabel(f, text=self.tr("game_title"), font=("Arial", 16, "bold")).pack(pady=10)
        ctk.CTkButton(f, text=self.tr("game_boost"), width=400, height=50, fg_color="green",
                      hover_color="darkgreen", font=("Arial", 14, "bold"),
                      command=self.game_boost).pack(pady=5)
        ctk.CTkLabel(f, text=self.tr("game_boost_desc"), font=("Arial", 11),
                     text_color="gray").pack()
        ctk.CTkButton(f, text=self.tr("game_normal"), width=400, height=45, fg_color="orange",
                      hover_color="darkorange", command=self.game_normal).pack(pady=10)
        ctk.CTkLabel(f, text=self.tr("game_normal_desc"), font=("Arial", 11),
                     text_color="gray").pack()
        ctk.CTkLabel(f, text="—", text_color="gray").pack(pady=10)
        row1 = ctk.CTkFrame(f)
        row1.pack(pady=5)
        ctk.CTkButton(row1, text=self.tr("game_ram"), width=200,
                      command=self.game_ram).pack(side="left", padx=5)
        ctk.CTkButton(row1, text=self.tr("game_cache"), width=200,
                      command=self.game_cache).pack(side="left", padx=5)
        row2 = ctk.CTkFrame(f)
        row2.pack(pady=5)
        ctk.CTkButton(row2, text=self.tr("game_bg"), width=200, fg_color="orange",
                      hover_color="darkorange", command=self.game_bg_disable).pack(side="left", padx=5)
        ctk.CTkButton(row2, text=self.tr("game_bg_enable"), width=200, fg_color="green",
                      hover_color="darkgreen", command=self.game_bg_enable).pack(side="left", padx=5)
        ctk.CTkLabel(f, text=self.tr("game_info"), font=("Arial", 11),
                     text_color="lightblue").pack(pady=15)

    def game_boost(self):
        def t():
            for key in ["window_animation_scale", "transition_animation_scale", "animator_duration_scale"]:
                run([ADB, "shell", "settings", "put", "global", key, "0.5"])
            run([ADB, "shell", "settings", "put", "global", "zen_mode", "1"])
            self.log("Gaming Mode Active!")
        threading.Thread(target=t, daemon=True).start()

    def game_normal(self):
        def t():
            for key in ["window_animation_scale", "transition_animation_scale", "animator_duration_scale"]:
                run([ADB, "shell", "settings", "put", "global", key, "1.0"])
            run([ADB, "shell", "settings", "put", "global", "zen_mode", "0"])
            self.log("Normal Mode Restored!")
        threading.Thread(target=t, daemon=True).start()

    def game_ram(self):
        self.async_run(lambda: run([ADB, "shell", "am", "kill-all"]) or self.tr("game_ram_ok"))

    def game_cache(self):
        self.async_run(lambda: run([ADB, "shell", "pm", "trim-caches", "999G"]) or self.tr("game_cache_ok"))

    def game_bg_disable(self):
        def t():
            run([ADB, "shell", "settings", "put", "global", "app_standby_enabled", "0"])
            run([ADB, "shell", "settings", "put", "global", "adaptive_battery_management_enabled", "0"])
            self.log(self.tr("game_bg_ok"))
        threading.Thread(target=t, daemon=True).start()

    def game_bg_enable(self):
        def t():
            run([ADB, "shell", "settings", "put", "global", "app_standby_enabled", "1"])
            run([ADB, "shell", "settings", "put", "global", "adaptive_battery_management_enabled", "1"])
            self.log(self.tr("sys_applied"))
        threading.Thread(target=t, daemon=True).start()

    # ---------- App Manager ----------
    def build_apps_tab(self):
        f = self.tab_apps
        ctk.CTkLabel(f, text=self.tr("apps_title"), font=("Arial", 16, "bold")).pack(pady=8)
        top = ctk.CTkFrame(f)
        top.pack(fill="x", padx=20, pady=5)
        ctk.CTkButton(top, text=self.tr("apps_load"), width=200, height=38, fg_color="green",
                      hover_color="darkgreen", command=self.apps_load).pack(side="left", padx=5)
        ctk.CTkLabel(top, text=self.tr("apps_filter")).pack(side="left", padx=(20, 5))
        self.apps_filter_var = ctk.StringVar(value=self.tr("apps_filter_all"))
        self.apps_filter_menu = ctk.CTkOptionMenu(
            top, width=150, variable=self.apps_filter_var,
            values=[self.tr("apps_filter_all"), self.tr("apps_filter_user"), self.tr("apps_filter_system")],
            command=lambda _: self.apps_apply_filter()
        )
        self.apps_filter_menu.pack(side="left", padx=5)
        self.apps_count_label = ctk.CTkLabel(top, text="", font=("Arial", 11), text_color="lightblue")
        self.apps_count_label.pack(side="left", padx=15)

        list_frame = ctk.CTkScrollableFrame(f, height=280)
        list_frame.pack(fill="both", expand=True, padx=20, pady=5)
        self.apps_list_frame = list_frame

        detail_frame = ctk.CTkFrame(f)
        detail_frame.pack(fill="x", padx=20, pady=5)
        self.apps_detail_label = ctk.CTkLabel(
            detail_frame, text=self.tr("apps_select"), font=("Arial", 12),
            text_color="gray", anchor="w"
        )
        self.apps_detail_label.pack(fill="x", padx=10, pady=5)

        ops = ctk.CTkFrame(f)
        ops.pack(pady=8)
        ctk.CTkButton(ops, text=self.tr("apps_uninstall"), width=170, height=42, fg_color="red",
                      hover_color="darkred", command=self.app_uninstall).pack(side="left", padx=4)
        ctk.CTkButton(ops, text=self.tr("apps_disable"), width=170, height=42, fg_color="orange",
                      hover_color="darkorange", command=self.app_disable).pack(side="left", padx=4)
        ctk.CTkButton(ops, text=self.tr("apps_enable"), width=170, height=42, fg_color="green",
                      hover_color="darkgreen", command=self.app_enable).pack(side="left", padx=4)
        ctk.CTkButton(ops, text=self.tr("apps_extract"), width=170, height=42,
                      command=self.app_extract).pack(side="left", padx=4)
        ops2 = ctk.CTkFrame(f)
        ops2.pack(pady=4)
        ctk.CTkButton(ops2, text=self.tr("apps_clear"), width=170, height=40, fg_color="orange",
                      hover_color="darkorange", command=self.app_clear).pack(side="left", padx=4)
        ctk.CTkButton(ops2, text=self.tr("apps_force_stop"), width=170, height=40, fg_color="red",
                      hover_color="darkred", command=self.app_force_stop).pack(side="left", padx=4)

    def apps_load(self):
        def t():
            self.log(self.tr("apps_loading"))
            out = run([ADB, "shell", "pm", "list", "packages", "-f"], timeout=120)
            if not out.strip() or "error" in out.lower() or "not found" in out.lower():
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
                    size_str = run([ADB, "shell", "du", "-b", apk_path], timeout=8)
                    size_bytes = 0
                    for tok in size_str.split():
                        if tok.isdigit():
                            size_bytes = int(tok)
                            break
                except Exception:
                    size_bytes = 0
                apps.append({"package": pkg.strip(), "path": apk_path,
                             "is_system": is_system, "size": size_bytes})
            self.apps_list = apps
            self.log(self.tr("apps_loaded", len(apps)))
            self.ui(self.apps_apply_filter)
        threading.Thread(target=t, daemon=True).start()

    def apps_apply_filter(self):
        if not hasattr(self, "apps_list_frame"):
            return
        for w in self.apps_list_frame.winfo_children():
            w.destroy()
        filter_val = self.apps_filter_var.get()
        if filter_val == self.tr("apps_filter_all"):
            filtered = self.apps_list
        elif filter_val == self.tr("apps_filter_user"):
            filtered = [a for a in self.apps_list if not a["is_system"]]
        else:
            filtered = [a for a in self.apps_list if a["is_system"]]
        self.apps_filtered = filtered
        self.apps_count_label.configure(text=self.tr("apps_count", len(filtered)))
        for app in filtered:
            self._add_app_row(app)

    def _add_app_row(self, app):
        pkg = app["package"]
        icon_text = "[S]" if app["is_system"] else "[U]"
        size_mb = app["size"] / (1024 * 1024) if app["size"] else 0
        label = icon_text + "  " + pkg + "   (" + str(round(size_mb, 1)) + " MB)"
        ctk.CTkButton(self.apps_list_frame, text=label, anchor="w", height=32,
                      fg_color="#2b2b3d", hover_color="#3b3b4d",
                      command=lambda p=pkg, a=app: self._select_app(p, a)).pack(fill="x", pady=2, padx=2)

    def _select_app(self, pkg, app):
        self.selected_pkg = pkg
        self.selected_app_info = app
        kind = "System" if app["is_system"] else "User"
        size_mb = app["size"] / (1024 * 1024) if app["size"] else 0
        self.apps_detail_label.configure(
            text="Selected: " + pkg + " | " + kind + " | " + str(round(size_mb, 1)) + " MB",
            text_color="lightgreen"
        )

    def _need_pkg(self):
        if not self.selected_pkg:
            messagebox.showerror(self.tr("err"), self.tr("apps_select"))
            return False
        return True

    def app_uninstall(self):
        if not self._need_pkg():
            return
        if not messagebox.askyesno(self.tr("confirm"), self.tr("confirm_uninstall", self.selected_pkg)):
            return

        def t():
            out = run([ADB, "uninstall", self.selected_pkg], timeout=120)
            if "Success" in out:
                self.log(self.tr("apps_uninstall_ok", self.selected_pkg))
                self.apps_load()
            else:
                self.log(self.tr("apps_uninstall_fail", self.selected_pkg))
                self.log(out[-300:])

        threading.Thread(target=t, daemon=True).start()

    def app_disable(self):
        if not self._need_pkg():
            return
        if not messagebox.askyesno(self.tr("warn"), self.tr("confirm_disable", self.selected_pkg)):
            return
        self.async_run(lambda: run([ADB, "shell", "pm", "disable-user", "--user", "0", self.selected_pkg])
                       or self.tr("apps_disable_ok", self.selected_pkg))

    def app_enable(self):
        if not self._need_pkg():
            return
        self.async_run(lambda: run([ADB, "shell", "pm", "enable", self.selected_pkg])
                       or self.tr("apps_enable_ok", self.selected_pkg))

    def app_extract(self):
        if not self._need_pkg():
            return
        if not self.selected_app_info or not self.selected_app_info.get("path"):
            messagebox.showerror(self.tr("err"), "APK path unknown")
            return

        def t():
            apk_path = self.selected_app_info.get("path")
            local = os.path.join(EXPORTS_DIR, self.selected_pkg + ".apk")
            run([ADB, "pull", apk_path, local], timeout=600)
            if os.path.exists(local):
                self.log(self.tr("apps_extract_ok", local))
            else:
                self.log(self.tr("apps_extract_fail", self.selected_pkg))

        threading.Thread(target=t, daemon=True).start()

    def app_clear(self):
        if not self._need_pkg():
            return
        if not messagebox.askyesno(self.tr("warn"), self.tr("confirm_clear", self.selected_pkg)):
            return
        self.async_run(lambda: run([ADB, "shell", "pm", "clear", self.selected_pkg])
                       or self.tr("apps_clear_ok", self.selected_pkg))

    def app_force_stop(self):
        if not self._need_pkg():
            return
        self.async_run(lambda: run([ADB, "shell", "am", "force-stop", self.selected_pkg])
                       or self.tr("apps_stop_ok", self.selected_pkg))

    # ---------- Backup ----------
    def build_backup_tab(self):
        f = self.tab_backup
        ctk.CTkLabel(f, text=self.tr("backup_title"), font=("Arial", 16, "bold")).pack(pady=10)
        ctk.CTkLabel(f, text=self.tr("backup_warning"), font=("Arial", 11),
                     text_color="orange").pack(pady=4)
        bf = ctk.CTkFrame(f)
        bf.pack(pady=10)
        ctk.CTkButton(bf, text=self.tr("backup_full"), width=400, height=50, fg_color="green",
                      hover_color="darkgreen", font=("Arial", 14, "bold"),
                      command=self.backup_full).pack(pady=5)
        ctk.CTkButton(bf, text=self.tr("backup_app"), width=400, height=45, fg_color="orange",
                      hover_color="darkorange", command=self.backup_app).pack(pady=5)
        ctk.CTkButton(bf, text=self.tr("backup_sdcard"), width=400, height=45, fg_color="blue",
                      hover_color="darkblue", command=self.backup_sdcard).pack(pady=5)
        ctk.CTkLabel(f, text="—", text_color="gray").pack(pady=10)
        bf2 = ctk.CTkFrame(f)
        bf2.pack(pady=10)
        ctk.CTkButton(bf2, text=self.tr("backup_restore"), width=400, height=50, fg_color="orange",
                      hover_color="darkorange", font=("Arial", 14, "bold"),
                      command=self.backup_restore).pack(pady=5)
        ctk.CTkButton(bf2, text=self.tr("backup_open"), width=400, height=45, fg_color="gray",
                      command=self.open_backups).pack(pady=5)

    def backup_full(self):
        def t():
            self.log(self.tr("backup_starting"))
            self.log(self.tr("backup_confirm_phone"))
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            path = os.path.join(BACKUP_DIR, "full_backup_" + ts + ".ab")
            try:
                subprocess.run([ADB, "backup", "-apk", "-shared", "-all", "-f", path],
                               capture_output=True, timeout=7200, creationflags=NO_WINDOW)
                if os.path.exists(path) and os.path.getsize(path) > 100:
                    self.log(self.tr("backup_done", path))
                else:
                    self.log(self.tr("backup_fail"))
            except Exception as e:
                self.log("Error: " + str(e))

        threading.Thread(target=t, daemon=True).start()

    def backup_app(self):
        pkg = self._ask(self.tr("backup_app_prompt"), "Backup App")
        if not pkg:
            return

        def t():
            self.log("Backing up " + pkg + "...")
            self.log(self.tr("backup_confirm_phone"))
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe = pkg.replace(".", "_")
            path = os.path.join(BACKUP_DIR, "app_" + safe + "_" + ts + ".ab")
            try:
                subprocess.run([ADB, "backup", "-apk", "-f", path, pkg],
                               capture_output=True, timeout=3600, creationflags=NO_WINDOW)
                if os.path.exists(path) and os.path.getsize(path) > 100:
                    self.log(self.tr("backup_done", path))
                else:
                    self.log(self.tr("backup_fail"))
            except Exception as e:
                self.log("Error: " + str(e))

        threading.Thread(target=t, daemon=True).start()

    def backup_sdcard(self):
        def t():
            self.log("Copying /sdcard/ ...")
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            dest = os.path.join(BACKUP_DIR, "sdcard_" + ts)
            try:
                os.makedirs(dest, exist_ok=True)
                out = run([ADB, "pull", "/sdcard/", dest], timeout=14400)
                self.log(out[-300:])
                if os.path.exists(dest) and os.listdir(dest):
                    self.log(self.tr("backup_sdcard_done", dest))
                else:
                    self.log(self.tr("backup_sdcard_fail"))
            except Exception as e:
                self.log("Error: " + str(e))

        threading.Thread(target=t, daemon=True).start()

    def backup_restore(self):
        p = filedialog.askopenfilename(filetypes=[("ADB Backup", "*.ab"), ("All", "*.*")],
                                       initialdir=BACKUP_DIR)
        if not p:
            return

        def t():
            self.log("Restoring " + os.path.basename(p) + "...")
            self.log(self.tr("backup_restore_done"))
            try:
                subprocess.run([ADB, "restore", p], capture_output=True,
                               timeout=7200, creationflags=NO_WINDOW)
                self.log("Restore done")
            except Exception as e:
                self.log("Error: " + str(e))

        threading.Thread(target=t, daemon=True).start()

    # ---------- Flash ----------
    def build_flash_tab(self):
        f = self.tab_flash
        ctk.CTkLabel(f, text=self.tr("flash_title"), font=("Arial", 16, "bold")).pack(pady=8)
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
        self.flash_type_label = ctk.CTkLabel(
            tf, text=self.tr("flash_type", self.tr("flash_type_unknown")),
            font=("Arial", 11), text_color="lightblue")
        self.flash_type_label.pack(side="left", padx=10)
        opts = ctk.CTkFrame(f)
        opts.pack(pady=6)
        ctk.CTkLabel(opts, text=self.tr("flash_mode")).grid(row=0, column=0, padx=5)
        self.flash_mode = ctk.CTkOptionMenu(
            opts, width=180,
            values=[self.tr("flash_mode_normal"), self.tr("flash_mode_keep"), self.tr("flash_mode_wipe")])
        self.flash_mode.grid(row=0, column=1, padx=5)
        self.chk_stop = ctk.CTkCheckBox(opts, text=self.tr("flash_stop_on_error"))
        self.chk_stop.grid(row=0, column=2, padx=10)
        self.chk_stop.select()
        self.chk_reboot = ctk.CTkCheckBox(opts, text=self.tr("flash_auto_reboot"))
        self.chk_reboot.grid(row=0, column=3, padx=10)
        self.chk_reboot.select()
        pf = ctk.CTkFrame(f)
        pf.pack(pady=8, fill="x", padx=20)
        ctk.CTkLabel(pf, text=self.tr("flash_progress"), font=("Arial", 12, "bold")).pack(anchor="w")
        self.flash_progress = ctk.CTkProgressBar(pf, height=20)
        self.flash_progress.pack(fill="x", pady=5)
        self.flash_progress.set(0)
        self.flash_status = ctk.CTkLabel(pf, text=self.tr("flash_status_idle"), font=("Arial", 11))
        self.flash_status.pack()
        bf = ctk.CTkFrame(f)
        bf.pack(pady=8)
        ctk.CTkButton(bf, text=self.tr("flash_start"), width=200, height=45, fg_color="green",
                      hover_color="darkgreen", font=("Arial", 14, "bold"),
                      command=self.start_flash).pack(side="left", padx=6)
        ctk.CTkButton(bf, text=self.tr("flash_cancel"), width=200, height=45, fg_color="red",
                      hover_color="darkred", font=("Arial", 14, "bold"),
                      command=self.cancel_flash).pack(side="left", padx=6)
        ctk.CTkLabel(f, text="Partitions:", font=("Arial", 12, "bold")).pack(anchor="w", padx=20, pady=(10, 3))
        self.part_list = ctk.CTkTextbox(f, height=110, font=("Consolas", 11))
        self.part_list.pack(fill="both", expand=True, padx=20, pady=(0, 10))

    def pick_flash_file(self):
        p = filedialog.askopenfilename(
            filetypes=[("ROM Files", "*.zip *.tar *.md5 *.tgz *.gz"), ("All files", "*.*")])
        if p:
            self.flash_file = p
            self.flash_file_label.configure(text=os.path.basename(p), text_color="lightgreen")
            self.log(p)
            self.scan_rom()

    def scan_rom(self):
        if not self.flash_file:
            return
        self.flash_rom_type = detect_rom_type(self.flash_file)
        type_key = {"fastboot_zip": "flash_type_fastboot_zip",
                    "samsung_tar": "flash_type_samsung_tar",
                    "payload": "flash_type_payload",
                    "tgz": "flash_type_tgz"}.get(self.flash_rom_type, "flash_type_unknown")
        self.flash_type_label.configure(text=self.tr("flash_type", self.tr(type_key)))

    def _extract_any(self, path, dest):
        os.makedirs(dest, exist_ok=True)
        name = os.path.basename(path).lower()
        if name.endswith(".zip"):
            safe_extract_zip(path, dest)
        else:
            safe_extract_tar(path, dest)

    def _find_images(self):
        images = {}
        for root, dirs, files in os.walk(TEMP_FLASH):
            for f in files:
                if f.endswith(".img"):
                    images[os.path.splitext(f)[0]] = os.path.join(root, f)
        return images

    def _payload_extract(self):
        payloads = []
        for root, dirs, files in os.walk(TEMP_FLASH):
            for f in files:
                if f == "payload.bin":
                    payloads.append(os.path.join(root, f))
        if not payloads:
            return
        try:
            p_url = "https://github.com/ssut/payload-dumper-go/releases/download/1.2.2/payload-dumper-go_1.2.2_windows_amd64.tar.gz"
            tgz = os.path.join(BASE_DIR, "pdg.tgz")
            if not os.path.exists(os.path.join(BASE_DIR, "payload-dumper-go.exe")):
                urllib.request.urlretrieve(p_url, tgz)
                safe_extract_tar(tgz, BASE_DIR)
                if os.path.exists(tgz):
                    os.remove(tgz)
            exe = os.path.join(BASE_DIR, "payload-dumper-go.exe")
            if os.path.exists(exe):
                out_dir = os.path.join(TEMP_FLASH, "extracted")
                os.makedirs(out_dir, exist_ok=True)
                for pl in payloads:
                    run([exe, "-o", out_dir, pl], timeout=3600)
        except Exception as e:
            self.log("Warning: " + str(e))

    def start_flash(self):
        if not self.flash_file or not os.path.exists(self.flash_file):
            messagebox.showerror(self.tr("err"), "Select a ROM")
            return
        self.flash_cancel = False

        def task():
            try:
                if os.path.exists(TEMP_FLASH):
                    shutil.rmtree(TEMP_FLASH, ignore_errors=True)
                self.ui(self.flash_status.configure, text=self.tr("flash_status_extracting"))
                self.log("Extracting...")
                self._extract_any(self.flash_file, TEMP_FLASH)
                self.ui(self.flash_status.configure, text=self.tr("flash_status_extracting_payload"))
                self._payload_extract()
                images = self._find_images()
                if not images:
                    self.log("No images")
                    self.ui(self.flash_status.configure, text=self.tr("flash_status_error"))
                    return
                self.ui(self.part_list.delete, "1.0", "end")
                for name in sorted(images.keys()):
                    self.ui(self.part_list.insert, "end", name + "\n")
                mode = self.flash_mode.get()
                total = len(images)
                done = 0
                self.ui(self.flash_progress.set, 0)
                for name in sorted(images.keys()):
                    if self.flash_cancel:
                        self.ui(self.flash_status.configure, text=self.tr("flash_status_cancelled"))
                        return
                    if mode == self.tr("flash_mode_keep") and name in ["userdata", "metadata"]:
                        done += 1
                        continue
                    self.ui(self.flash_status.configure,
                            text=self.tr("flash_status_flashing", name))
                    self.log(name)
                    out = run([FASTBOOT, "flash", name, images[name]], timeout=1800)
                    self.log(out[-300:])
                    if "FAILED" in out and self.chk_stop.get():
                        self.ui(self.flash_status.configure, text=self.tr("flash_status_error"))
                        return
                    done += 1
                    self.ui(self.flash_progress.set, done / total)
                if self.chk_reboot.get() and not self.flash_cancel:
                    run([FASTBOOT, "reboot"])
                self.ui(self.flash_status.configure, text=self.tr("flash_status_done"))
                self.ui(self.flash_progress.set, 1)
            except Exception as e:
                self.log("Error: " + str(e))
                self.ui(self.flash_status.configure, text=self.tr("flash_status_error"))

        threading.Thread(target=task, daemon=True).start()

    def cancel_flash(self):
        self.flash_cancel = True

    # ---------- Xiaomi ----------
    def build_xiaomi_tab(self):
        f = self.tab_xiaomi
        ctk.CTkLabel(f, text=self.tr("xiaomi_title"), font=("Arial", 16, "bold")).pack(pady=6)
        ctk.CTkLabel(f, text=self.tr("xiaomi_warning"), font=("Arial", 11),
                     text_color="orange").pack(pady=4)
        row = ctk.CTkFrame(f)
        row.pack(pady=6)
        ctk.CTkButton(row, text=self.tr("xiaomi_info"), width=180,
                      command=self.xiaomi_info).pack(side="left", padx=4)
        ctk.CTkButton(row, text=self.tr("xiaomi_unlock_help"), width=180, fg_color="gray",
                      command=lambda: webbrowser.open("https://en.miui.com/unlock/")).pack(side="left", padx=4)
        ctk.CTkButton(row, text=self.tr("xiaomi_mi_assistant"), width=180, fg_color="gray",
                      command=self.xiaomi_mi_assistant).pack(side="left", padx=4)
        ctk.CTkLabel(f, text="— Fastboot ROM —", font=("Arial", 12, "bold"),
                     text_color="lightblue").pack(pady=(15, 3))
        rf = ctk.CTkFrame(f)
        rf.pack(pady=4)
        ctk.CTkButton(rf, text=self.tr("xiaomi_select_rom"), width=250,
                      command=self.xiaomi_select_rom).pack(side="left", padx=5)
        self.xiaomi_rom_label = ctk.CTkLabel(rf, text=self.tr("samsung_no_file"),
                                             font=("Arial", 10), text_color="gray")
        self.xiaomi_rom_label.pack(side="left", padx=5)
        fl = ctk.CTkFrame(f)
        fl.pack(pady=6)
        ctk.CTkButton(fl, text=self.tr("xiaomi_flash_all"), width=200, height=42, fg_color="green",
                      hover_color="darkgreen",
                      command=lambda: self.xiaomi_flash_rom(wipe=False)).pack(side="left", padx=4)
        ctk.CTkButton(fl, text=self.tr("xiaomi_flash_all_no_data"), width=200, height=42,
                      fg_color="orange", hover_color="darkorange",
                      command=lambda: self.xiaomi_flash_rom(wipe=True)).pack(side="left", padx=4)
        ctk.CTkLabel(f, text="— Partitions —", font=("Arial", 12, "bold"),
                     text_color="lightblue").pack(pady=(15, 3))
        pf = ctk.CTkFrame(f)
        pf.pack(pady=4)
        ctk.CTkButton(pf, text=self.tr("xiaomi_flash_boot"), width=180,
                      command=lambda: self.flash_single("boot")).pack(side="left", padx=3)
        ctk.CTkButton(pf, text=self.tr("xiaomi_flash_recovery"), width=180,
                      command=lambda: self.flash_single("recovery")).pack(side="left", padx=3)
        ctk.CTkButton(pf, text=self.tr("xiaomi_flash_vbmeta"), width=180,
                      command=lambda: self.flash_single("vbmeta")).pack(side="left", padx=3)
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
                      command=lambda: self._pick_into(self.xiaomi_img_file)).pack(side="left", padx=4)
        ctk.CTkButton(cf, text=self.tr("write_btn"), width=90, fg_color="red",
                      hover_color="darkred",
                      command=lambda: self._flash_custom(self.xiaomi_part_name, self.xiaomi_img_file)
                      ).pack(side="left", padx=4)
        ctk.CTkLabel(f, text=self.tr("advanced"), font=("Arial", 12, "bold"),
                     text_color="orange").pack(pady=(15, 3))
        af = ctk.CTkFrame(f)
        af.pack(pady=4)
        ctk.CTkButton(af, text=self.tr("xiaomi_remove_mi_account"), width=220, fg_color="red",
                      hover_color="darkred", command=self.xiaomi_remove_account).pack(side="left", padx=3)
        ctk.CTkButton(af, text=self.tr("xiaomi_clean_and_lock"), width=220, fg_color="red",
                      hover_color="darkred", command=self.xiaomi_clean_lock).pack(side="left", padx=3)
        ctk.CTkLabel(f, text="— Reboot —", font=("Arial", 12, "bold"),
                     text_color="lightblue").pack(pady=(15, 3))
        rbf = ctk.CTkFrame(f)
        rbf.pack(pady=4)
        ctk.CTkButton(rbf, text=self.tr("xiaomi_reboot_fastboot"), width=180,
                      command=lambda: self.async_run(lambda: run([ADB, "reboot", "bootloader"]))
                      ).pack(side="left", padx=3)
        ctk.CTkButton(rbf, text=self.tr("xiaomi_reboot_recovery"), width=180,
                      command=lambda: self.async_run(lambda: run([ADB, "reboot", "recovery"]))
                      ).pack(side="left", padx=3)
        ctk.CTkButton(rbf, text=self.tr("xiaomi_reboot_edl"), width=180,
                      command=lambda: self.async_run(lambda: run([ADB, "reboot", "edl"]))
                      ).pack(side="left", padx=3)

    def xiaomi_info(self):
        def t():
            self.log("=" * 50)
            for p in ["ro.product.model", "ro.product.brand", "ro.miui.ui.version.name",
                      "ro.mi.os.version.incremental", "ro.build.version.release", "ro.boot.hwc",
                      "ro.boot.hwlevel", "ro.secureboot.lockstate", "ro.boot.verifiedbootstate",
                      "ro.serialno", "ro.product.cpu.abi"]:
                self.log(p + ": " + run([ADB, "shell", "getprop", p]).strip())
        threading.Thread(target=t, daemon=True).start()

    def xiaomi_mi_assistant(self):
        def t():
            self.log("=" * 50)
            self.log(run([ADB, "shell", "getprop", "ro.boot.mode"]))
            self.log(run([ADB, "shell", "getprop", "ro.boot.midevicemode"]))
        threading.Thread(target=t, daemon=True).start()

    def xiaomi_select_rom(self):
        p = filedialog.askopenfilename(
            filetypes=[("Xiaomi ROM", "*.tgz *.gz *.zip"), ("All", "*.*")])
        if p:
            self.xiaomi_rom = p
            self.xiaomi_rom_label.configure(text=os.path.basename(p), text_color="lightgreen")
            self.log("Xiaomi ROM: " + os.path.basename(p))

    def xiaomi_flash_rom(self, wipe=False):
        if not self.xiaomi_rom or not os.path.exists(self.xiaomi_rom):
            messagebox.showerror(self.tr("err"), self.tr("samsung_no_file"))
            return
        if not messagebox.askyesno(self.tr("confirm"),
                                   self.tr("confirm_flash_samsung", os.path.basename(self.xiaomi_rom))):
            return

        def t():
            try:
                if os.path.exists(TEMP_FLASH):
                    shutil.rmtree(TEMP_FLASH, ignore_errors=True)
                os.makedirs(TEMP_FLASH, exist_ok=True)
                self.log("Extracting Xiaomi ROM...")
                self._extract_any(self.xiaomi_rom, TEMP_FLASH)
                images = self._find_images()
                if not images:
                    self.log("No images")
                    return
                order = ["gpt", "tz", "xbl", "abl", "aop", "bluetooth", "keymaster", "devcfg",
                         "dsp", "featenabler", "hyp", "imagefv", "qupfw", "shrm", "uefisecapp",
                         "vbmeta_system", "vbmeta_vendor", "vbmeta", "modem", "boot", "dtbo",
                         "recovery", "super", "cust", "countrycode", "frp", "persist",
                         "metadata", "userdata"]
                for part in order:
                    if part not in images:
                        continue
                    if wipe and part == "userdata":
                        continue
                    self.log("flash " + part)
                    self.log(run([FASTBOOT, "flash", part, images[part]], timeout=1800)[-200:])
                for part, path in images.items():
                    if part in order:
                        continue
                    self.log("flash " + part)
                    self.log(run([FASTBOOT, "flash", part, path], timeout=1800)[-200:])
                self.log("Xiaomi ROM flashed!")
                run([FASTBOOT, "reboot"])
            except Exception as e:
                self.log("Error: " + str(e))

        threading.Thread(target=t, daemon=True).start()

    def xiaomi_remove_account(self):
        messagebox.showinfo("Info", self.tr("xiaomi_remove_mi_account_help"))

    def xiaomi_clean_lock(self):
        if not messagebox.askyesno(self.tr("warn"), "Flash + Lock?"):
            return
        def t():
            self.log("Locking...")
            run([FASTBOOT, "flashing", "lock"], timeout=120)
            run([FASTBOOT, "reboot"])
        threading.Thread(target=t, daemon=True).start()

    # ---------- Huawei ----------
    def build_huawei_tab(self):
        f = self.tab_huawei
        ctk.CTkLabel(f, text=self.tr("huawei_title"), font=("Arial", 16, "bold")).pack(pady=6)
        ctk.CTkLabel(f, text=self.tr("huawei_warning"), font=("Arial", 11),
                     text_color="orange").pack(pady=4)
        row = ctk.CTkFrame(f)
        row.pack(pady=6)
        ctk.CTkButton(row, text=self.tr("huawei_info"), width=180,
                      command=self.huawei_info).pack(side="left", padx=4)
        ctk.CTkButton(row, text=self.tr("huawei_check_bl"), width=180,
                      command=self.huawei_check_bl).pack(side="left", padx=4)
        ctk.CTkButton(row, text=self.tr("huawei_erecovery"), width=180, fg_color="orange",
                      hover_color="darkorange",
                      command=self.huawei_erecovery).pack(side="left", padx=4)
        ctk.CTkLabel(f, text="— Tools —", font=("Arial", 12, "bold"),
                     text_color="lightblue").pack(pady=(15, 3))
        tf = ctk.CTkFrame(f)
        tf.pack(pady=4)
        ctk.CTkButton(tf, text=self.tr("huawei_unlock_help"), width=200, fg_color="gray",
                      command=lambda: webbrowser.open("https://emui.huawei.com/en/unlock_index")
                      ).pack(side="left", padx=4)
        ctk.CTkButton(tf, text=self.tr("huawei_hisuite"), width=200, fg_color="gray",
                      command=lambda: webbrowser.open("https://consumer.huawei.com/en/support/hisuite/")
                      ).pack(side="left", padx=4)
        ctk.CTkButton(tf, text=self.tr("huawei_erecovery_help"), width=200, fg_color="gray",
                      command=lambda: webbrowser.open("https://consumer.huawei.com/en/support/")
                      ).pack(side="left", padx=4)
        ctk.CTkLabel(f, text="— Flash Partitions —", font=("Arial", 12, "bold"),
                     text_color="lightblue").pack(pady=(15, 3))
        pf = ctk.CTkFrame(f)
        pf.pack(pady=4)
        for p in ["boot", "recovery", "system", "ramdisk"]:
            ctk.CTkButton(pf, text=self.tr("huawei_flash_" + p), width=180,
                          command=lambda pp=p: self.flash_single(pp)).pack(side="left", padx=3)
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
                      command=lambda: self._pick_into(self.huawei_img_file)).pack(side="left", padx=4)
        ctk.CTkButton(cf, text=self.tr("write_btn"), width=90, fg_color="red",
                      hover_color="darkred",
                      command=lambda: self._flash_custom(self.huawei_part_name, self.huawei_img_file)
                      ).pack(side="left", padx=4)
        ctk.CTkLabel(f, text=self.tr("advanced"), font=("Arial", 12, "bold"),
                     text_color="orange").pack(pady=(15, 3))
        af = ctk.CTkFrame(f)
        af.pack(pady=4)
        ctk.CTkButton(af, text=self.tr("huawei_unlock_code"), width=200, fg_color="orange",
                      hover_color="darkorange",
                      command=self.huawei_unlock_code).pack(side="left", padx=3)
        ctk.CTkButton(af, text=self.tr("huawei_erase_frp"), width=200, fg_color="red",
                      hover_color="darkred",
                      command=lambda: self._erase_frp_fastboot()).pack(side="left", padx=3)
        ctk.CTkButton(af, text=self.tr("huawei_wipe_data"), width=200, fg_color="red",
                      hover_color="darkred",
                      command=lambda: self._wipe_data_fastboot()).pack(side="left", padx=3)
        ctk.CTkLabel(f, text="— Reboot —", font=("Arial", 12, "bold"),
                     text_color="lightblue").pack(pady=(15, 3))
        rbf = ctk.CTkFrame(f)
        rbf.pack(pady=4)
        ctk.CTkButton(rbf, text=self.tr("huawei_fastboot"), width=180,
                      command=lambda: self.async_run(lambda: run([ADB, "reboot", "bootloader"]))
                      ).pack(side="left", padx=3)
        ctk.CTkButton(rbf, text=self.tr("huawei_recovery"), width=180,
                      command=lambda: self.async_run(lambda: run([ADB, "reboot", "recovery"]))
                      ).pack(side="left", padx=3)
        ctk.CTkButton(rbf, text=self.tr("huawei_reboot_ok"), width=180,
                      command=lambda: self.async_run(lambda: run([ADB, "reboot"]))
                      ).pack(side="left", padx=3)

    def huawei_info(self):
        def t():
            self.log("=" * 50)
            for p in ["ro.product.model", "ro.product.brand", "ro.build.version.release",
                      "ro.build.version.emui", "ro.build.display.id", "ro.serialno",
                      "ro.product.cpu.abi", "ro.build.version.sdk", "ro.boot.hardware",
                      "ro.board.platform"]:
                self.log(p + ": " + run([ADB, "shell", "getprop", p]).strip())
        threading.Thread(target=t, daemon=True).start()

    def huawei_check_bl(self):
        def t():
            self.log("=" * 50)
            self.log("verifiedbootstate: " +
                     run([ADB, "shell", "getprop", "ro.boot.verifiedbootstate"]).strip())
            self.log("flash.locked: " +
                     run([ADB, "shell", "getprop", "ro.boot.flash.locked"]).strip())
            self.log(run([FASTBOOT, "oem", "device-info"]))
        threading.Thread(target=t, daemon=True).start()

    def huawei_erecovery(self):
        self.async_run(lambda: run([ADB, "reboot", "erecovery"], timeout=20))

    def huawei_unlock_code(self):
        code = self._ask("Enter Huawei Unlock Code:", "Unlock")
        if not code:
            return
        self.async_run(lambda: run([FASTBOOT, "oem", "unlock", code], timeout=120))

    # ---------- Samsung ----------
    def build_samsung_tab(self):
        f = self.tab_samsung
        ctk.CTkLabel(f, text=self.tr("samsung_title"), font=("Arial", 16, "bold")).pack(pady=6)
        ctk.CTkLabel(f, text=self.tr("samsung_warning"), font=("Arial", 11),
                     text_color="orange").pack(pady=4)
        row0 = ctk.CTkFrame(f)
        row0.pack(pady=6)
        ctk.CTkButton(row0, text=self.tr("samsung_detect"), width=200, height=38,
                      command=self.samsung_detect).pack(side="left", padx=5)
        ctk.CTkButton(row0, text=self.tr("samsung_pit"), width=200, height=38,
                      command=self.samsung_pit).pack(side="left", padx=5)
        for name, var in [("samsung_ap", "samsung_ap"), ("samsung_bl", "samsung_bl"),
                          ("samsung_cp", "samsung_cp"), ("samsung_csc", "samsung_csc")]:
            row = ctk.CTkFrame(f)
            row.pack(pady=4, fill="x", padx=20)
            ctk.CTkLabel(row, text=self.tr(name), width=260, anchor="w").pack(side="left")
            lbl = ctk.CTkLabel(row, text=self.tr("samsung_no_file"),
                               font=("Arial", 10), text_color="gray")
            lbl.pack(side="left", padx=5)
            setattr(self, var + "_label", lbl)
            ctk.CTkButton(row, text=self.tr("pick"), width=80,
                          command=lambda v=var: self.samsung_pick(v)).pack(side="right", padx=5)
        opt = ctk.CTkFrame(f)
        opt.pack(pady=10)
        self.samsung_reboot = ctk.CTkCheckBox(opt, text=self.tr("samsung_reboot"))
        self.samsung_reboot.grid(row=0, column=0, padx=10)
        self.samsung_reboot.select()
        ctk.CTkButton(f, text=self.tr("samsung_flash_all"), width=350, height=50, fg_color="green",
                      hover_color="darkgreen", font=("Arial", 15, "bold"),
                      command=self.samsung_flash_all).pack(pady=15)
        fl = ctk.CTkFrame(f)
        fl.pack(pady=5)
        for p in ["AP", "BL", "CP", "CSC"]:
            ctk.CTkButton(fl, text=self.tr("samsung_flash_" + p.lower()), width=140,
                          command=lambda pp=p: self.samsung_flash_one(pp)).pack(side="left", padx=3)

    def samsung_pick(self, var):
        p = filedialog.askopenfilename(filetypes=[("Samsung", "*.tar.md5 *.tar"), ("All", "*.*")])
        if p:
            setattr(self, var, p)
            getattr(self, var + "_label").configure(text=os.path.basename(p),
                                                    text_color="lightgreen")

    def samsung_detect(self):
        def t():
            if not os.path.exists(HEIMDALL):
                self.log(self.tr("msg_no_heimdall"))
                return
            self.log(run([HEIMDALL, "detect"], timeout=30, cwd=HEIMDALL_DIR))
        threading.Thread(target=t, daemon=True).start()

    def samsung_pit(self):
        def t():
            if not os.path.exists(HEIMDALL):
                self.log(self.tr("msg_no_heimdall"))
                return
            self.log(run([HEIMDALL, "print-pit"], timeout=60, cwd=HEIMDALL_DIR))
        threading.Thread(target=t, daemon=True).start()

    def samsung_flash_one(self, partition):
        key = {"AP": "samsung_ap", "BL": "samsung_bl",
               "CP": "samsung_cp", "CSC": "samsung_csc"}[partition]
        f = getattr(self, key, "")
        if not f or not os.path.exists(f):
            messagebox.showerror(self.tr("err"), self.tr("samsung_no_file"))
            return
        self._samsung_flash([(partition, f)])

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
        self._samsung_flash(files)

    def _samsung_flash(self, files):
        def t():
            if not os.path.exists(HEIMDALL):
                self.log(self.tr("msg_no_heimdall"))
                return
            det = run([HEIMDALL, "detect"], timeout=30, cwd=HEIMDALL_DIR)
            self.log(det)
            if "Detected" not in det and "Device" not in det:
                self.log("No device")
                return
            for part, f in files:
                self.log("Flashing " + part + ": " + os.path.basename(f))
                args = [HEIMDALL, "flash",
                        "--reboot" if self.samsung_reboot.get() else "--no-reboot",
                        "--verbose", "--" + part, f]
                self.log(run(args, timeout=3600, cwd=HEIMDALL_DIR)[-1500:])
            self.log(self.tr("samsung_done"))
        threading.Thread(target=t, daemon=True).start()

    # ---------- Oppo ----------
    def build_oppo_tab(self):
        f = self.tab_oppo
        ctk.CTkLabel(f, text=self.tr("oppo_title"), font=("Arial", 16, "bold")).pack(pady=6)
        ctk.CTkLabel(f, text=self.tr("oppo_warning"), font=("Arial", 11),
                     text_color="orange").pack(pady=4)
        row = ctk.CTkFrame(f)
        row.pack(pady=6)
        ctk.CTkButton(row, text=self.tr("oppo_info"), width=170,
                      command=self.oppo_info).pack(side="left", padx=4)
        ctk.CTkButton(row, text=self.tr("oppo_check_bl"), width=170,
                      command=self.oppo_check_bl).pack(side="left", padx=4)
        ctk.CTkButton(row, text=self.tr("oppo_fastboot"), width=170,
                      command=lambda: self.async_run(lambda: run([ADB, "reboot", "bootloader"]))
                      ).pack(side="left", padx=4)
        ctk.CTkLabel(f, text="— Unlock Tools —", font=("Arial", 12, "bold"),
                     text_color="lightblue").pack(pady=(15, 3))
        uf = ctk.CTkFrame(f)
        uf.pack(pady=4)
        ctk.CTkButton(uf, text=self.tr("oppo_unlock_help"), width=220, fg_color="gray",
                      command=lambda: webbrowser.open("https://www.oppo.com/en/support/")
                      ).pack(side="left", padx=3)
        ctk.CTkButton(uf, text=self.tr("oppo_download_help"), width=220, fg_color="gray",
                      command=lambda: webbrowser.open("https://www.realme.com/global/support/")
                      ).pack(side="left", padx=3)
        ctk.CTkButton(uf, text=self.tr("oppo_flash_recovery"), width=220,
                      command=lambda: self.flash_single("recovery")).pack(side="left", padx=3)
        uf2 = ctk.CTkFrame(f)
        uf2.pack(pady=4)
        ctk.CTkButton(uf2, text=self.tr("oppo_unlock_cmd"), width=250, fg_color="orange",
                      hover_color="darkorange",
                      command=lambda: self._unlock_cmd()).pack(side="left", padx=4)
        ctk.CTkButton(uf2, text=self.tr("oppo_lock_cmd"), width=250, fg_color="red",
                      hover_color="darkred",
                      command=lambda: self._lock_cmd()).pack(side="left", padx=4)
        ctk.CTkLabel(f, text="— Fastboot ROM —", font=("Arial", 12, "bold"),
                     text_color="lightblue").pack(pady=(15, 3))
        rf = ctk.CTkFrame(f)
        rf.pack(pady=4)
        ctk.CTkButton(rf, text=self.tr("oppo_select_rom"), width=250,
                      command=lambda: self._select_rom("oppo_rom", "oppo_rom_label")
                      ).pack(side="left", padx=5)
        self.oppo_rom_label = ctk.CTkLabel(rf, text=self.tr("samsung_no_file"),
                                           font=("Arial", 10), text_color="gray")
        self.oppo_rom_label.pack(side="left", padx=5)
        fl = ctk.CTkFrame(f)
        fl.pack(pady=6)
        ctk.CTkButton(fl, text=self.tr("oppo_flash_wipe"), width=200, height=42, fg_color="green",
                      hover_color="darkgreen",
                      command=lambda: self.flash_rom_generic("oppo_rom", wipe=True)
                      ).pack(side="left", padx=4)
        ctk.CTkButton(fl, text=self.tr("oppo_flash_keep"), width=200, height=42, fg_color="orange",
                      hover_color="darkorange",
                      command=lambda: self.flash_rom_generic("oppo_rom", wipe=False)
                      ).pack(side="left", padx=4)
        ctk.CTkLabel(f, text="— Partitions —", font=("Arial", 12, "bold"),
                     text_color="lightblue").pack(pady=(15, 3))
        pf = ctk.CTkFrame(f)
        pf.pack(pady=4)
        for p in ["boot", "vbmeta", "dtbo", "super"]:
            ctk.CTkButton(pf, text=self.tr("oppo_flash_" + p), width=170,
                          command=lambda pp=p: self.flash_single(pp)).pack(side="left", padx=3)
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
                      command=lambda: self._pick_into(self.oppo_img_file)).pack(side="left", padx=4)
        ctk.CTkButton(cf, text=self.tr("write_btn"), width=90, fg_color="red",
                      hover_color="darkred",
                      command=lambda: self._flash_custom(self.oppo_part_name, self.oppo_img_file)
                      ).pack(side="left", padx=4)
        ctk.CTkLabel(f, text=self.tr("advanced"), font=("Arial", 12, "bold"),
                     text_color="orange").pack(pady=(15, 3))
        af = ctk.CTkFrame(f)
        af.pack(pady=4)
        ctk.CTkButton(af, text=self.tr("oppo_erase_frp"), width=200, fg_color="red",
                      hover_color="darkred",
                      command=lambda: self._erase_frp_fastboot()).pack(side="left", padx=3)
        ctk.CTkButton(af, text=self.tr("oppo_wipe_data"), width=200, fg_color="red",
                      hover_color="darkred",
                      command=lambda: self._wipe_data_fastboot()).pack(side="left", padx=3)
        ctk.CTkButton(af, text=self.tr("oppo_edl"), width=200,
                      command=lambda: self.async_run(lambda: run([ADB, "reboot", "edl"]))
                      ).pack(side="left", padx=3)

    def oppo_info(self):
        def t():
            self.log("=" * 50)
            for p in ["ro.product.model", "ro.product.brand", "ro.build.version.oplusrom",
                      "ro.build.version.opporom", "ro.build.version.realme",
                      "ro.build.version.oxygen", "ro.build.display.id",
                      "ro.build.version.release", "ro.build.version.sdk",
                      "ro.product.cpu.abi", "ro.serialno", "ro.boot.verifiedbootstate",
                      "ro.boot.flash.locked"]:
                self.log(p + ": " + run([ADB, "shell", "getprop", p]).strip())
        threading.Thread(target=t, daemon=True).start()

    def oppo_check_bl(self):
        def t():
            self.log("=" * 50)
            self.log(run([FASTBOOT, "oem", "device-info"], timeout=30))
            self.log(run([FASTBOOT, "getvar", "unlocked"], timeout=15))
            self.log("ro.boot.flash.locked: " +
                     run([ADB, "shell", "getprop", "ro.boot.flash.locked"]).strip())
        threading.Thread(target=t, daemon=True).start()

    # ---------- Vivo ----------
    def build_vivo_tab(self):
        f = self.tab_vivo
        ctk.CTkLabel(f, text=self.tr("vivo_title"), font=("Arial", 16, "bold")).pack(pady=6)
        ctk.CTkLabel(f, text=self.tr("vivo_warning"), font=("Arial", 11),
                     text_color="orange").pack(pady=4)
        row = ctk.CTkFrame(f)
        row.pack(pady=6)
        ctk.CTkButton(row, text=self.tr("vivo_info"), width=170,
                      command=self.vivo_info).pack(side="left", padx=4)
        ctk.CTkButton(row, text=self.tr("vivo_check_bl"), width=170,
                      command=self.vivo_check_bl).pack(side="left", padx=4)
        ctk.CTkButton(row, text=self.tr("vivo_fastboot"), width=170,
                      command=lambda: self.async_run(lambda: run([ADB, "reboot", "bootloader"]))
                      ).pack(side="left", padx=4)
        ctk.CTkLabel(f, text="— Unlock Tools —", font=("Arial", 12, "bold"),
                     text_color="lightblue").pack(pady=(15, 3))
        uf = ctk.CTkFrame(f)
        uf.pack(pady=4)
        ctk.CTkButton(uf, text=self.tr("vivo_unlock_help"), width=220, fg_color="gray",
                      command=lambda: webbrowser.open("https://www.vivo.com/en/support/")
                      ).pack(side="left", padx=3)
        ctk.CTkButton(uf, text=self.tr("vivo_download_help"), width=220, fg_color="gray",
                      command=lambda: webbrowser.open("https://www.vivo.com/en/support/faq")
                      ).pack(side="left", padx=3)
        ctk.CTkButton(uf, text=self.tr("vivo_flash_recovery"), width=220,
                      command=lambda: self.flash_single("recovery")).pack(side="left", padx=3)
        uf2 = ctk.CTkFrame(f)
        uf2.pack(pady=4)
        ctk.CTkButton(uf2, text=self.tr("vivo_unlock_cmd"), width=250, fg_color="orange",
                      hover_color="darkorange",
                      command=lambda: self._unlock_cmd()).pack(side="left", padx=4)
        ctk.CTkButton(uf2, text=self.tr("vivo_lock_cmd"), width=250, fg_color="red",
                      hover_color="darkred",
                      command=lambda: self._lock_cmd()).pack(side="left", padx=4)
        ctk.CTkLabel(f, text="— Fastboot ROM —", font=("Arial", 12, "bold"),
                     text_color="lightblue").pack(pady=(15, 3))
        rf = ctk.CTkFrame(f)
        rf.pack(pady=4)
        ctk.CTkButton(rf, text=self.tr("vivo_select_rom"), width=250,
                      command=lambda: self._select_rom("vivo_rom", "vivo_rom_label")
                      ).pack(side="left", padx=5)
        self.vivo_rom_label = ctk.CTkLabel(rf, text=self.tr("samsung_no_file"),
                                           font=("Arial", 10), text_color="gray")
        self.vivo_rom_label.pack(side="left", padx=5)
        fl = ctk.CTkFrame(f)
        fl.pack(pady=6)
        ctk.CTkButton(fl, text=self.tr("vivo_flash_wipe"), width=200, height=42, fg_color="green",
                      hover_color="darkgreen",
                      command=lambda: self.flash_rom_generic("vivo_rom", wipe=True)
                      ).pack(side="left", padx=4)
        ctk.CTkButton(fl, text=self.tr("vivo_flash_keep"), width=200, height=42, fg_color="orange",
                      hover_color="darkorange",
                      command=lambda: self.flash_rom_generic("vivo_rom", wipe=False)
                      ).pack(side="left", padx=4)
        ctk.CTkLabel(f, text="— Partitions —", font=("Arial", 12, "bold"),
                     text_color="lightblue").pack(pady=(15, 3))
        pf = ctk.CTkFrame(f)
        pf.pack(pady=4)
        for p in ["boot", "vbmeta", "dtbo", "super"]:
            ctk.CTkButton(pf, text=self.tr("vivo_flash_" + p), width=170,
                          command=lambda pp=p: self.flash_single(pp)).pack(side="left", padx=3)
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
                      command=lambda: self._pick_into(self.vivo_img_file)).pack(side="left", padx=4)
        ctk.CTkButton(cf, text=self.tr("write_btn"), width=90, fg_color="red",
                      hover_color="darkred",
                      command=lambda: self._flash_custom(self.vivo_part_name, self.vivo_img_file)
                      ).pack(side="left", padx=4)
        ctk.CTkLabel(f, text=self.tr("advanced"), font=("Arial", 12, "bold"),
                     text_color="orange").pack(pady=(15, 3))
        af = ctk.CTkFrame(f)
        af.pack(pady=4)
        ctk.CTkButton(af, text=self.tr("vivo_erase_frp"), width=200, fg_color="red",
                      hover_color="darkred",
                      command=lambda: self._erase_frp_fastboot()).pack(side="left", padx=3)
        ctk.CTkButton(af, text=self.tr("vivo_wipe_data"), width=200, fg_color="red",
                      hover_color="darkred",
                      command=lambda: self._wipe_data_fastboot()).pack(side="left", padx=3)
        ctk.CTkButton(af, text=self.tr("vivo_edl"), width=200,
                      command=lambda: self.async_run(lambda: run([ADB, "reboot", "edl"]))
                      ).pack(side="left", padx=3)

    def vivo_info(self):
        def t():
            self.log("=" * 50)
            for p in ["ro.product.model", "ro.product.brand", "ro.build.version.vivo",
                      "ro.build.version.funtouch", "ro.build.version.originos",
                      "ro.build.display.id", "ro.build.version.release",
                      "ro.build.version.sdk", "ro.product.cpu.abi", "ro.serialno",
                      "ro.boot.verifiedbootstate", "ro.boot.flash.locked"]:
                self.log(p + ": " + run([ADB, "shell", "getprop", p]).strip())
        threading.Thread(target=t, daemon=True).start()

    def vivo_check_bl(self):
        def t():
            self.log("=" * 50)
            self.log(run([FASTBOOT, "oem", "device-info"], timeout=30))
            self.log(run([FASTBOOT, "getvar", "unlocked"], timeout=15))
            self.log("ro.boot.flash.locked: " +
                     run([ADB, "shell", "getprop", "ro.boot.flash.locked"]).strip())
        threading.Thread(target=t, daemon=True).start()

    # ---------- Common helpers ----------
    def flash_single(self, partition):
        p = filedialog.askopenfilename(filetypes=[("Image", "*.img"), ("All", "*.*")])
        if not p:
            return
        self.async_run(
            lambda: run([FASTBOOT, "flash", partition, p], timeout=1200)[-1000:]
        )

    def _pick_into(self, entry):
        p = filedialog.askopenfilename(filetypes=[("Image", "*.img")])
        if p:
            entry.delete(0, "end")
            entry.insert(0, p)

    def _flash_custom(self, part_entry, file_entry):
        part = part_entry.get().strip()
        f = file_entry.get().strip()
        if not part or not os.path.exists(f):
            messagebox.showerror(self.tr("err"), self.tr("err_check"))
            return
        self.async_run(lambda: run([FASTBOOT, "flash", part, f], timeout=1200)[-1000:])

    def _unlock_cmd(self):
        if not messagebox.askyesno(self.tr("warn"), self.tr("confirm_unlock")):
            return

        def t():
            self.log("Trying unlock...")
            self.log(run([FASTBOOT, "flashing", "unlock"], timeout=120))
            self.log(run([FASTBOOT, "oem", "unlock"], timeout=60))
        threading.Thread(target=t, daemon=True).start()

    def _lock_cmd(self):
        if not messagebox.askyesno(self.tr("warn"), self.tr("confirm_unlock")):
            return
        self.async_run(lambda: run([FASTBOOT, "flashing", "lock"], timeout=120))

    def _select_rom(self, attr, label_attr):
        p = filedialog.askopenfilename(
            filetypes=[("ROM", "*.zip *.tar *.tgz *.gz *.img"), ("All", "*.*")])
        if p:
            setattr(self, attr, p)
            getattr(self, label_attr).configure(text=os.path.basename(p),
                                                text_color="lightgreen")
            self.log("ROM: " + os.path.basename(p))

    def flash_rom_generic(self, attr, wipe=False):
        rom = getattr(self, attr, "")
        if not rom or not os.path.exists(rom):
            messagebox.showerror(self.tr("err"), self.tr("samsung_no_file"))
            return
        if not messagebox.askyesno(self.tr("confirm"),
                                   self.tr("confirm_flash_samsung", os.path.basename(rom))):
            return

        def t():
            try:
                if os.path.exists(TEMP_FLASH):
                    shutil.rmtree(TEMP_FLASH, ignore_errors=True)
                os.makedirs(TEMP_FLASH, exist_ok=True)
                self.log("Extracting...")
                self._extract_any(rom, TEMP_FLASH)
                self._payload_extract()
                images = self._find_images()
                if not images:
                    self.log("No images")
                    return
                order = ["gpt", "tz", "xbl", "abl", "aop", "bluetooth", "keymaster", "devcfg",
                         "dsp", "featenabler", "hyp", "imagefv", "qupfw", "shrm", "uefisecapp",
                         "vbmeta_system", "vbmeta_vendor", "vbmeta", "modem", "boot", "dtbo",
                         "recovery", "super", "system", "system_ext", "vendor", "product", "odm",
                         "my_bigball", "my_carrier", "my_company", "my_engineering", "my_heytap",
                         "my_manifest", "my_product", "my_region", "my_stock",
                         "persist", "metadata", "userdata"]
                for part in order:
                    if part not in images:
                        continue
                    if wipe and part == "userdata":
                        continue
                    self.log("flash " + part)
                    self.log(run([FASTBOOT, "flash", part, images[part]], timeout=1800)[-200:])
                for part, path in images.items():
                    if part in order:
                        continue
                    self.log("flash " + part)
                    self.log(run([FASTBOOT, "flash", part, path], timeout=1800)[-200:])
                self.log("ROM flashed!")
                run([FASTBOOT, "reboot"])
            except Exception as e:
                self.log("Error: " + str(e))

        threading.Thread(target=t, daemon=True).start()

    # ---------- Root ----------
    def build_root_tab(self):
        f = self.tab_root
        ctk.CTkLabel(f, text=self.tr("root_title"), font=("Arial", 16, "bold")).pack(pady=6)
        ctk.CTkLabel(f, text=self.tr("root_warning"), font=("Arial", 11),
                     text_color="orange").pack(pady=4)
        blf = ctk.CTkFrame(f)
        blf.pack(pady=6)
        ctk.CTkButton(blf, text=self.tr("check_bl_status"), width=200,
                      command=self.check_bl_status).pack(side="left", padx=5)
        self.bl_status_label = ctk.CTkLabel(blf, text=self.tr("bl_unknown"),
                                            font=("Arial", 12, "bold"))
        self.bl_status_label.pack(side="left", padx=10)
        blb = ctk.CTkFrame(f)
        blb.pack(pady=4)
        ctk.CTkButton(blb, text=self.tr("unlock_bl"), width=220, fg_color="orange",
                      hover_color="darkorange",
                      command=self.unlock_bootloader).pack(side="left", padx=5)
        ctk.CTkButton(blb, text=self.tr("lock_bl"), width=220, fg_color="red",
                      hover_color="darkred",
                      command=self.lock_bootloader).pack(side="left", padx=5)
        ctk.CTkLabel(f, text="— TWRP —", font=("Arial", 12, "bold"),
                     text_color="lightblue").pack(pady=(15, 3))
        tw = ctk.CTkFrame(f)
        tw.pack(pady=4)
        ctk.CTkButton(tw, text=self.tr("select_recovery"), width=280,
                      command=self.pick_recovery).pack(side="left", padx=5)
        self.recovery_label = ctk.CTkLabel(tw, text=self.tr("samsung_no_file"),
                                           font=("Arial", 10), text_color="gray")
        self.recovery_label.pack(side="left", padx=5)
        ctk.CTkButton(f, text=self.tr("flash_twrp"), width=350, height=45, fg_color="green",
                      hover_color="darkgreen", font=("Arial", 14, "bold"),
                      command=self.flash_recovery).pack(pady=6)
        ctk.CTkLabel(f, text="— Magisk —", font=("Arial", 12, "bold"),
                     text_color="lightblue").pack(pady=(15, 3))
        mg = ctk.CTkFrame(f)
        mg.pack(pady=4)
        ctk.CTkButton(mg, text=self.tr("select_boot"), width=280,
                      command=self.pick_boot).pack(side="left", padx=5)
        self.boot_label = ctk.CTkLabel(mg, text=self.tr("samsung_no_file"),
                                       font=("Arial", 10), text_color="gray")
        self.boot_label.pack(side="left", padx=5)
        ctk.CTkButton(f, text=self.tr("flash_magisk"), width=350, height=45, fg_color="green",
                      hover_color="darkgreen", font=("Arial", 14, "bold"),
                      command=self.flash_boot).pack(pady=6)
        opt = ctk.CTkFrame(f)
        opt.pack(pady=10)
        self.reboot_after_root = ctk.CTkCheckBox(opt, text=self.tr("reboot_recovery_after"))
        self.reboot_after_root.grid(row=0, column=0, padx=10)
        self.reboot_after_root.select()
        lf = ctk.CTkFrame(f)
        lf.pack(pady=10)
        ctk.CTkButton(lf, text=self.tr("download_twrp"), width=200, fg_color="gray",
                      command=lambda: webbrowser.open("https://twrp.me/Devices/")
                      ).pack(side="left", padx=5)
        ctk.CTkButton(lf, text=self.tr("download_magisk"), width=200, fg_color="gray",
                      command=lambda: webbrowser.open("https://github.com/topjohnwu/Magisk/releases")
                      ).pack(side="left", padx=5)

    def check_bl_status(self):
        def t():
            out = run([FASTBOOT, "oem", "device-info"], timeout=30)
            out2 = run([FASTBOOT, "getvar", "unlocked"], timeout=15)
            self.log(out + out2)
            c = (out + out2).lower()
            if "unlocked: yes" in c or ": true" in c:
                self.ui(self.bl_status_label.configure, text=self.tr("bl_unlocked"),
                        text_color="lightgreen")
            elif "unlocked: no" in c or ": false" in c:
                self.ui(self.bl_status_label.configure, text=self.tr("bl_locked"),
                        text_color="red")
            else:
                self.ui(self.bl_status_label.configure, text=self.tr("bl_unknown"),
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
            self.recovery_label.configure(text=os.path.basename(p), text_color="lightgreen")

    def pick_boot(self):
        p = filedialog.askopenfilename(filetypes=[("Boot", "*.img"), ("All", "*.*")])
        if p:
            self.boot_img = p
            self.boot_label.configure(text=os.path.basename(p), text_color="lightgreen")

    def flash_recovery(self):
        if not self.recovery_img or not os.path.exists(self.recovery_img):
            messagebox.showerror(self.tr("err"), self.tr("samsung_no_file"))
            return

        def t():
            out = run([FASTBOOT, "flash", "recovery", self.recovery_img], timeout=600)
            self.log(out[-500:])
            if "OKAY" in out or "Finished" in out:
                self.log(self.tr("flash_recovery_success"))
                if self.reboot_after_root.get():
                    run([FASTBOOT, "reboot", "recovery"])
        threading.Thread(target=t, daemon=True).start()

    def flash_boot(self):
        if not self.boot_img or not os.path.exists(self.boot_img):
            messagebox.showerror(self.tr("err"), self.tr("samsung_no_file"))
            return

        def t():
            out = run([FASTBOOT, "flash", "boot", self.boot_img], timeout=600)
            self.log(out[-500:])
            if "OKAY" in out or "Finished" in out:
                self.log(self.tr("flash_boot_success"))
        threading.Thread(target=t, daemon=True).start()

    # ---------- Unlock ----------
    def build_unlock_tab(self):
        f = self.tab_unlock
        ctk.CTkLabel(f, text=self.tr("unlock_title"), font=("Arial", 15, "bold")).pack(pady=5)
        ctk.CTkLabel(f, text=self.tr("unlock_warning"), font=("Arial", 11),
                     text_color="orange").pack(pady=4)
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
        ctk.CTkButton(row2, text=self.tr("remove_locksettings"), width=250, fg_color="orange",
                      hover_color="darkorange",
                      command=self.remove_locksettings).pack(side="left", padx=4)
        ctk.CTkButton(row2, text=self.tr("remove_gatekeeper"), width=250, fg_color="orange",
                      hover_color="darkorange",
                      command=self.remove_gatekeeper).pack(side="left", padx=4)
        row3 = ctk.CTkFrame(f)
        row3.pack(pady=4)
        ctk.CTkButton(row3, text=self.tr("remove_pattern"), width=250, fg_color="orange",
                      hover_color="darkorange",
                      command=self.remove_pattern).pack(side="left", padx=4)
        ctk.CTkButton(row3, text=self.tr("full_device_info"), width=250,
                      command=self.full_info).pack(side="left", padx=4)
        row4 = ctk.CTkFrame(f)
        row4.pack(pady=4)
        ctk.CTkButton(row4, text=self.tr("erase_frp_adb"), width=250, fg_color="red",
                      hover_color="darkred",
                      command=self.erase_frp_adb).pack(side="left", padx=4)
        row5 = ctk.CTkFrame(f)
        row5.pack(pady=4)
        ctk.CTkButton(row5, text=self.tr("erase_frp_fastboot"), width=250, fg_color="red",
                      hover_color="darkred",
                      command=lambda: self._erase_frp_fastboot()).pack(side="left", padx=4)
        ctk.CTkButton(row5, text=self.tr("format_data_fastboot"), width=250, fg_color="red",
                      hover_color="darkred",
                      command=lambda: self._wipe_data_fastboot()).pack(side="left", padx=4)

    def _erase_frp_fastboot(self):
        if not messagebox.askyesno(self.tr("warn"), self.tr("confirm_wipe")):
            return
        self.async_run(lambda: run([FASTBOOT, "erase", "frp"], timeout=120))

    def _wipe_data_fastboot(self):
        if not messagebox.askyesno(self.tr("warn"), self.tr("confirm_format")):
            return
        self.async_run(lambda: run([FASTBOOT, "erase", "userdata"], timeout=300))

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
            self.log("Root: " + (out if out else "No root"))
        threading.Thread(target=t, daemon=True).start()

    def check_frp(self):
        def t():
            out = run([ADB, "shell", "getprop", "ro.frp.pst"]).strip()
            self.log("FRP: " + (out if out else "N/A"))
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
        self.async_run(lambda: run([ADB, "shell", "su", "-c", "rm -f /data/system/gesture.key"]))

    def full_info(self):
        self.async_run(lambda: run([ADB, "shell", "getprop"], timeout=30)[:5000])

    def erase_frp_adb(self):
        if not messagebox.askyesno(self.tr("warn"), self.tr("confirm_wipe")):
            return
        self.async_run(lambda: run(
            [ADB, "shell", "su", "-c", "rm -rf /persistent/frp/* /data/system/users/0/frp/*"]))

    # ---------- MTK ----------
    def build_mtk_tab(self):
        f = self.tab_mtk
        ctk.CTkLabel(f, text=self.tr("mtk_title"), font=("Arial", 15, "bold")).pack(pady=5)
        ctk.CTkButton(f, text=self.tr("run_gui"), width=280, fg_color="green",
                      hover_color="darkgreen",
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
                      command=lambda: self._pick_into(self.mtk_write_file)).pack(side="left")
        ctk.CTkButton(row2, text=self.tr("write_btn"), width=70, fg_color="red",
                      hover_color="darkred",
                      command=self.mtk_write).pack(side="left", padx=5)
        ctk.CTkLabel(f, text=self.tr("advanced"), font=("Arial", 12, "bold"),
                     text_color="orange").pack(pady=(15, 3))
        ctk.CTkButton(f, text=self.tr("unlock_bl_mtk"), width=300, fg_color="orange",
                      hover_color="darkorange",
                      command=self.mtk_unlock).pack(pady=3)
        ctk.CTkButton(f, text=self.tr("wipe_frp"), width=300, fg_color="orange",
                      hover_color="darkorange",
                      command=self.mtk_wipe).pack(pady=3)

    def run_mtk_gui(self):
        if not os.path.exists(EMBED_PY):
            self.log(self.tr("msg_no_embed"))
            return
        gui = os.path.join(MTK_DIR, "mtk_gui.py")
        if not os.path.exists(gui):
            self.log("mtk_gui.py missing")
            return
        try:
            subprocess.Popen([EMBED_PY, "mtk_gui.py"], cwd=MTK_DIR,
                             creationflags=NEW_CONSOLE)
        except Exception as e:
            self.log(str(e))

    def mtk_cmd(self, args, timeout=600):
        if not os.path.exists(MTK_SCRIPT):
            self.log(self.tr("msg_no_mtk"))
            return
        if not os.path.exists(EMBED_PY):
            self.log(self.tr("msg_no_embed"))
            return

        def t():
            self.log(run([EMBED_PY, "mtk.py"] + args, timeout=timeout, cwd=MTK_DIR))
        threading.Thread(target=t, daemon=True).start()

    def mtk_read(self):
        p = self.mtk_read_part.get().strip()
        if p:
            self.mtk_cmd(["r", p, p + ".img"])

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

    # ---------- EDL ----------
    def build_edl_tab(self):
        f = self.tab_edl
        ctk.CTkLabel(f, text=self.tr("edl_title"), font=("Arial", 15, "bold")).pack(pady=5)
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
                      command=self.edl_printgpt).pack(side="left", padx=5)
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
                      command=lambda: self._pick_into(self.edl_write_file)).pack(side="left", padx=3)
        ctk.CTkButton(wp, text=self.tr("edl_load"), width=90, fg_color="red",
                      hover_color="darkred",
                      command=self.edl_write).pack(side="left", padx=5)
        ops = ctk.CTkFrame(f)
        ops.pack(pady=15)
        ctk.CTkButton(ops, text=self.tr("edl_rw"), width=200, fg_color="orange",
                      hover_color="darkorange",
                      command=self.edl_rw).pack(side="left", padx=3)
        ctk.CTkButton(ops, text=self.tr("edl_reset"), width=180,
                      command=self.edl_reset).pack(side="left", padx=3)
        ctk.CTkButton(ops, text=self.tr("edl_wipe"), width=180, fg_color="orange",
                      hover_color="darkorange",
                      command=self.edl_wipe).pack(side="left", padx=3)

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
        if not os.path.exists(EMBED_PY):
            self.log(self.tr("msg_no_embed"))
            return

        def t():
            self.log(run(self.edl_base() + args, timeout=timeout, cwd=EDL_DIR))
        threading.Thread(target=t, daemon=True).start()

    def pick_edl_loader(self):
        p = filedialog.askopenfilename(
            filetypes=[("Loader", "*.mbn *.bin *.elf"), ("All", "*.*")])
        if p:
            self.edl_loader_entry.delete(0, "end")
            self.edl_loader_entry.insert(0, p)

    def edl_printgpt(self):
        self.edl_run(["printgpt"], timeout=300)

    def edl_dump(self):
        p = self.edl_read_part.get().strip()
        if p:
            self.edl_run(["r", p, p + ".img"])

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

    # ---------- Advanced ----------
    def build_adv_tab(self):
        f = self.tab_adv
        ctk.CTkLabel(f, text=self.tr("adv_title"), font=("Arial", 16, "bold")).pack(pady=10)
        ctk.CTkButton(f, text=self.tr("adv_adb_terminal"), width=400, height=50, fg_color="green",
                      hover_color="darkgreen", font=("Arial", 14, "bold"),
                      command=self.adv_adb_terminal).pack(pady=5)
        ctk.CTkLabel(f, text=self.tr("adv_adb_terminal_desc"), font=("Arial", 11),
                     text_color="gray").pack()
        ctk.CTkButton(f, text=self.tr("adv_install_batch"), width=400, height=50, fg_color="green",
                      hover_color="darkgreen", font=("Arial", 14, "bold"),
                      command=self.adv_install_batch).pack(pady=5)
        ctk.CTkLabel(f, text=self.tr("adv_install_batch_desc"), font=("Arial", 11),
                     text_color="gray").pack()
        ctk.CTkLabel(f, text="—", text_color="gray").pack(pady=10)
        row1 = ctk.CTkFrame(f)
        row1.pack(pady=5)
        ctk.CTkButton(row1, text=self.tr("adv_battery_calib"), width=200, fg_color="orange",
                      hover_color="darkorange",
                      command=self.adv_battery_calib).pack(side="left", padx=5)
        ctk.CTkButton(row1, text=self.tr("adv_network_info"), width=200,
                      command=self.adv_network_info).pack(side="left", padx=5)
        row2 = ctk.CTkFrame(f)
        row2.pack(pady=5)
        ctk.CTkButton(row2, text=self.tr("adv_hide_app"), width=200, fg_color="orange",
                      hover_color="darkorange",
                      command=self.adv_hide_app).pack(side="left", padx=5)
        ctk.CTkButton(row2, text=self.tr("adv_show_app"), width=200, fg_color="green",
                      hover_color="darkgreen",
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
                      command=lambda: self.async_run(lambda: run([ADB, "reboot", "bootloader"]))
                      ).pack(side="left", padx=5)
        ctk.CTkButton(row4, text=self.tr("adv_reboot_recovery"), width=200,
                      command=lambda: self.async_run(lambda: run([ADB, "reboot", "recovery"]))
                      ).pack(side="left", padx=5)
        row5 = ctk.CTkFrame(f)
        row5.pack(pady=5)
        ctk.CTkButton(row5, text=self.tr("adv_reboot_download"), width=200,
                      command=lambda: self.async_run(lambda: run([ADB, "reboot", "download"]))
                      ).pack(side="left", padx=5)

    def adv_adb_terminal(self):
        cmd = self._ask(self.tr("adv_adb_prompt"), "ADB Command")
        if not cmd:
            return
        self.async_run(lambda: "adb " + cmd + "\n" + run([ADB] + cmd.split(), timeout=300))

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
                out = run([ADB, "install", "-r", full], timeout=600)
                if "Success" in out:
                    count += 1
            self.log(self.tr("adv_install_count", count))
        threading.Thread(target=t, daemon=True).start()

    def adv_battery_calib(self):
        if not messagebox.askyesno(self.tr("warn"), self.tr("adv_battery_warn")):
            return

        def t():
            run([ADB, "shell", "su", "-c", "rm -f /data/system/batterystats.bin"])
            self.log(self.tr("adv_battery_done"))
        threading.Thread(target=t, daemon=True).start()

    def adv_network_info(self):
        def t():
            self.log(self.tr("adv_network_loading"))
            self.log("IP:")
            self.log(run([ADB, "shell", "ip", "addr", "show", "wlan0"]))
            self.log("Wi-Fi:")
            self.log(run([ADB, "shell", "dumpsys", "wifi"]))
            self.log("Data:")
            self.log(run([ADB, "shell", "dumpsys", "telephony.registry"]))
        threading.Thread(target=t, daemon=True).start()

    def adv_hide_app(self):
        pkg = self._ask(self.tr("adv_hide_app_prompt"), "Hide App")
        if not pkg:
            return
        self.async_run(lambda: (run([ADB, "shell", "pm", "hide", pkg]),
                                self.tr("adv_app_hidden", pkg))[1])

    def adv_show_app(self):
        pkg = self._ask(self.tr("adv_hide_app_prompt"), "Unhide App")
        if not pkg:
            return
        self.async_run(lambda: (run([ADB, "shell", "pm", "unhide", pkg]),
                                self.tr("adv_app_shown", pkg))[1])

    def adv_fastboot_info(self):
        self.async_run(lambda: run([FASTBOOT, "getvar", "all"], timeout=60))

    def adv_device_props(self):
        self.async_run(lambda: run([ADB, "shell", "getprop"], timeout=30))

    # ---------- Base ----------
    def async_run(self, fn):
        def wrap():
            try:
                self.log(self.tr("msg_wait"))
                self.log(fn())
            except Exception as e:
                self.log("Error: " + str(e))
        threading.Thread(target=wrap, daemon=True).start()

    def check_tools(self):
        self.log(("✔ " if os.path.exists(ADB) else "✘ ") + self.tr("msg_tools_ok"))
        self.log(("✔ " if os.path.exists(EMBED_PY) else "✘ ") + self.tr("msg_python_ok"))
        self.log(("✔ " if os.path.exists(MTK_SCRIPT) else "✘ ") + self.tr("msg_mtk_ok"))
        self.log(("✔ " if os.path.exists(EDL_SCRIPT) else "✘ ") + self.tr("msg_edl_ok"))
        self.log(("✔ " if os.path.exists(HEIMDALL) else "✘ ") + self.tr("msg_heimdall_ok"))

    def download_tools(self):
        def task():
            try:
                os.makedirs(TOOLS_DIR, exist_ok=True)
                zip_path = os.path.join(BASE_DIR, "pt.zip")
                self.log(self.tr("msg_downloading_pt"))
                urllib.request.urlretrieve(PLATFORM_TOOLS_URL, zip_path)
                safe_extract_zip(zip_path, TOOLS_DIR)
                sub = os.path.join(TOOLS_DIR, "platform-tools")
                if os.path.isdir(sub):
                    for item in os.listdir(sub):
                        shutil.move(os.path.join(sub, item), TOOLS_DIR)
                    shutil.rmtree(sub, ignore_errors=True)
                if os.path.exists(zip_path):
                    os.remove(zip_path)
                self.log(self.tr("msg_installed"))
                self.check_tools()
            except Exception as e:
                self.log(self.tr("msg_error", e))
        threading.Thread(target=task, daemon=True).start()

    def detect(self):
        def t():
            self.log("ADB:\n" + run([ADB, "devices", "-l"]))
            self.log("Fastboot:\n" + run([FASTBOOT, "devices"]))
        threading.Thread(target=t, daemon=True).start()

    def info(self):
        def t():
            for p in ["ro.product.model", "ro.product.brand", "ro.build.version.release",
                      "ro.serialno", "ro.product.cpu.abi", "ro.build.version.sdk"]:
                self.log(p + ": " + run([ADB, "shell", "getprop", p]).strip())
        threading.Thread(target=t, daemon=True).start()


def show_splash():
    splash = ctk.CTk()
    splash.title("Android Tool")
    splash.geometry("500x300")
    splash.resizable(False, False)
    sw = splash.winfo_screenwidth()
    sh = splash.winfo_screenheight()
    x = (sw - 500) // 2
    y = (sh - 300) // 2
    splash.geometry("500x300+" + str(x) + "+" + str(y))
    frame = ctk.CTkFrame(splash, fg_color="#1a1a2e", corner_radius=0)
    frame.pack(fill="both", expand=True)
    ctk.CTkLabel(frame, text="ANDROID TOOL", font=("Arial", 28, "bold"),
                 text_color="#4ade80").pack(pady=(50, 5))
    ctk.CTkLabel(frame, text="Version " + APP_VERSION, font=("Arial", 12),
                 text_color="gray").pack(pady=5)
    ctk.CTkLabel(frame, text="Loading...", font=("Arial", 12),
                 text_color="lightblue").pack(pady=20)
    bar = ctk.CTkProgressBar(frame, width=350, height=15, progress_color="#4ade80")
    bar.pack(pady=5)
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
        # بعد إغلاق نافذة الترخيص
        if holder["app"] is not None:
            holder["app"].mainloop()
    else:
        app = App()
        app.mainloop()


if __name__ == "__main__":
    main()