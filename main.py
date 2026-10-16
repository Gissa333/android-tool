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

# مسار الموارد
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
    BUNDLE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    BUNDLE_DIR = BASE_DIR

# مسار Python الداخلي (المضمّن في PyInstaller)
PYTHON_EXE = sys.executable if getattr(sys, 'frozen', False) else sys.executable

TOOLS_DIR = os.path.join(BASE_DIR, "platform-tools")
MTK_DIR = os.path.join(BASE_DIR, "mtkclient")
ADB = os.path.join(TOOLS_DIR, "adb.exe")
FASTBOOT = os.path.join(TOOLS_DIR, "fastboot.exe")
MTK_SCRIPT = os.path.join(MTK_DIR, "mtk.py")

PLATFORM_TOOLS_URL = "https://dl.google.com/android/repository/platform-tools-latest-windows.zip"


def run(cmd, timeout=60, cwd=None, env=None):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout,
                           encoding="utf-8", errors="ignore", cwd=cwd, env=env,
                           creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
        return (r.stdout or "") + (r.stderr or "")
    except Exception as e:
        return f"خطأ: {e}"


def run_mtk(args, timeout=600):
    """تشغيل mtkclient كـ module داخلي بدون Python خارجي"""
    if not os.path.exists(os.path.join(MTK_DIR, "mtkclient")):
        return "❌ mtkclient غير موجود في المجلد"

    env = os.environ.copy()
    env["PYTHONPATH"] = MTK_DIR + os.pathsep + env.get("PYTHONPATH", "")

    try:
        # استخدام Python المضمّن في PyInstaller مباشرة
        r = subprocess.run(
            [PYTHON_EXE, "-c",
             f"import sys; sys.path.insert(0, r'{MTK_DIR}'); "
             f"import mtkclient.mtk as m; m.main({args!r})"],
            capture_output=True, text=True, timeout=timeout,
            encoding="utf-8", errors="ignore", env=env, cwd=MTK_DIR,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
        )
        return (r.stdout or "") + (r.stderr or "")
    except Exception as e:
        return f"خطأ: {e}"


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Android Tool v0.4")
        self.geometry("950x750")

        ctk.CTkLabel(self, text="🛠️ Android Tool",
                     font=("Arial", 22, "bold")).pack(pady=5)

        self.tabs = ctk.CTkTabview(self, width=900, height=650)
        self.tabs.pack(padx=15, pady=5, fill="both", expand=True)

        self.tab_adb = self.tabs.add("ADB/Fastboot")
        self.tab_mtk = self.tabs.add("MTK (MediaTek)")

        self.build_adb_tab()
        self.build_mtk_tab()

        ctk.CTkLabel(self, text="📋 السجل:", font=("Arial", 13, "bold")).pack(anchor="w", padx=15)
        self.log_box = ctk.CTkTextbox(self, height=130, font=("Consolas", 11))
        self.log_box.pack(fill="x", padx=15, pady=(0, 10))

        self.check_tools()

    def log(self, t):
        self.log_box.insert("end", str(t) + "\n")
        self.log_box.see("end")
        self.update_idletasks()

    def async_run(self, fn):
        def wrap():
            self.log("⏳ ...")
            self.log(fn())
        threading.Thread(target=wrap, daemon=True).start()

    def build_adb_tab(self):
        f = self.tab_adb
        btns = [
            ("📥 تحميل Platform-Tools", self.download_tools),
            ("🔍 اكتشاف الأجهزة", self.detect),
            ("📱 معلومات الجهاز", self.info),
            ("🔄 إعادة تشغيل", lambda: self.async_run(lambda: run([ADB, "reboot"]))),
            ("⚡ Fastboot", lambda: self.async_run(lambda: run([ADB, "reboot", "bootloader"]))),
            ("🔌 خروج من Fastboot", lambda: self.async_run(lambda: run([FASTBOOT, "reboot"]))),
        ]
        for i, (t, fn) in enumerate(btns):
            ctk.CTkButton(f, text=t, width=200, height=36,
                          command=fn).grid(row=i // 3, column=i % 3, padx=8, pady=8)

    def build_mtk_tab(self):
        f = self.tab_mtk

        ctk.CTkLabel(f, text="⚙️ mtkclient — MediaTek (مدمج)",
                     font=("Arial", 15, "bold")).pack(pady=5)

        ctk.CTkButton(f, text="🖥️ تشغيل الواجهة الرسمية", width=280,
                      fg_color="green", hover_color="darkgreen",
                      command=self.run_mtk_gui).pack(pady=4)

        ctk.CTkButton(f, text="📋 قراءة GPT", width=280,
                      command=lambda: self.mtk_cmd(["printgpt"])).pack(pady=4)

        row = ctk.CTkFrame(f)
        row.pack(pady=4)
        ctk.CTkLabel(row, text="قراءة قسم:").pack(side="left", padx=5)
        self.mtk_read_part = ctk.CTkEntry(row, width=120)
        self.mtk_read_part.pack(side="left", padx=5)
        self.mtk_read_part.insert(0, "boot")
        ctk.CTkButton(row, text="قراءة", width=80,
                      command=self.mtk_read).pack(side="left")

        row2 = ctk.CTkFrame(f)
        row2.pack(pady=4)
        ctk.CTkLabel(row2, text="كتابة قسم:").pack(side="left", padx=5)
        self.mtk_write_part = ctk.CTkEntry(row2, width=120)
        self.mtk_write_part.pack(side="left", padx=5)
        self.mtk_write_part.insert(0, "boot")
        self.mtk_write_file = ctk.CTkEntry(row2, width=200)
        self.mtk_write_file.pack(side="left", padx=5)
        ctk.CTkButton(row2, text="اختر", width=60,
                      command=self.pick_mtk_file).pack(side="left")
        ctk.CTkButton(row2, text="كتابة", width=70, fg_color="red",
                      hover_color="darkred",
                      command=self.mtk_write).pack(side="left", padx=5)

        ctk.CTkLabel(f, text="⚠️ عمليات متقدمة", font=("Arial", 12, "bold"),
                     text_color="orange").pack(pady=(15, 3))

        ctk.CTkButton(f, text="🔓 فك قفل البوتلودر", width=300,
                      fg_color="orange", hover_color="darkorange",
                      command=self.mtk_unlock).pack(pady=3)

        ctk.CTkButton(f, text="🧹 مسح FRP + Userdata", width=300,
                      fg_color="orange", hover_color="darkorange",
                      command=self.mtk_wipe).pack(pady=3)

    def check_tools(self):
        if os.path.exists(ADB):
            self.log(f"✅ Platform-Tools: {TOOLS_DIR}")
        else:
            self.log("⚠️ Platform-Tools غير مثبتة — اضغط الزر")

        if os.path.exists(os.path.join(MTK_DIR, "mtkclient")):
            self.log(f"✅ mtkclient مدمج: {MTK_DIR}")
        else:
            self.log("⚠️ mtkclient غير موجود في المجلد")

    def download_tools(self):
        def task():
            try:
                os.makedirs(TOOLS_DIR, exist_ok=True)
                zip_path = os.path.join(BASE_DIR, "pt.zip")
                self.log("📥 تحميل Platform-Tools...")
                urllib.request.urlretrieve(PLATFORM_TOOLS_URL, zip_path)
                with zipfile.ZipFile(zip_path, "r") as z:
                    z.extractall(TOOLS_DIR)
                # نقل المحتوى من platform-tools الفرعي
                sub = os.path.join(TOOLS_DIR, "platform-tools")
                if os.path.isdir(sub):
                    for item in os.listdir(sub):
                        shutil.move(os.path.join(sub, item), TOOLS_DIR)
                    shutil.rmtree(sub, ignore_errors=True)
                os.remove(zip_path)
                self.log("✅ تم التثبيت")
                self.check_tools()
            except Exception as e:
                self.log(f"❌ {e}")
        threading.Thread(target=task, daemon=True).start()

    def detect(self):
        def t():
            self.log("=" * 50)
            self.log("— ADB —\n" + run([ADB, "devices", "-l"]))
            self.log("— Fastboot —\n" + run([FASTBOOT, "devices"]))
        threading.Thread(target=t, daemon=True).start()

    def info(self):
        def t():
            self.log("=" * 50)
            for p in ["ro.product.model", "ro.product.brand",
                      "ro.build.version.release", "ro.serialno",
                      "ro.product.cpu.abi", "ro.build.version.sdk"]:
                self.log(f"{p}: {run([ADB, 'shell', 'getprop', p]).strip()}")
        threading.Thread(target=t, daemon=True).start()

    def run_mtk_gui(self):
        mtk_gui = os.path.join(MTK_DIR, "mtk_gui.py")
        if not os.path.exists(mtk_gui):
            self.log("❌ mtk_gui.py غير موجود في مجلد mtkclient")
            return
        env = os.environ.copy()
        env["PYTHONPATH"] = MTK_DIR + os.pathsep + env.get("PYTHONPATH", "")
        self.log("🖥️ تشغيل mtk_gui...")
        subprocess.Popen([PYTHON_EXE, mtk_gui], cwd=MTK_DIR, env=env,
                         creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == "nt" else 0)

    def mtk_cmd(self, args, timeout=600):
        def t():
            self.log("=" * 50)
            self.log(f"⚙️ mtk {' '.join(args)}")
            self.log(run_mtk(args, timeout=timeout))
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
            messagebox.showerror("خطأ", "تحقق من القسم والملف")
            return
        if not messagebox.askyesno("تأكيد", f"كتابة {part} من {f}؟"):
            return
        self.mtk_cmd(["w", part, f])

    def mtk_unlock(self):
        if not messagebox.askyesno("تحذير", "فك قفل البوتلودر سيمسح كل البيانات!\nمتأكد؟"):
            return
        self.mtk_cmd(["da", "seccfg", "unlock"])

    def mtk_wipe(self):
        if not messagebox.askyesno("تحذير", "مسح FRP و Userdata نهائياً!"):
            return
        self.mtk_cmd(["e", "frp,userdata,metadata,md_udc"])


if __name__ == "__main__":
    App().mainloop()