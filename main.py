import customtkinter as ctk
from tkinter import filedialog, messagebox
import subprocess
import os
import threading
import urllib.request
import zipfile

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

APP_DIR = os.path.join(os.environ.get("LOCALAPPDATA", "."), "AndroidTool")
TOOLS_DIR = os.path.join(APP_DIR, "platform-tools")
ADB = os.path.join(TOOLS_DIR, "adb.exe")
FASTBOOT = os.path.join(TOOLS_DIR, "fastboot.exe")

PLATFORM_TOOLS_URL = "https://dl.google.com/android/repository/platform-tools-latest-windows.zip"


def run(cmd, timeout=60):
    try:
        r = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout,
            encoding="utf-8", errors="ignore",
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
        )
        return (r.stdout or "") + (r.stderr or "")
    except subprocess.TimeoutExpired:
        return "خطأ: انتهت المهلة"
    except FileNotFoundError:
        return f"خطأ: لم يتم العثور على {cmd[0]}"
    except Exception as e:
        return f"خطأ: {e}"


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Android Tool v0.2")
        self.geometry("950x700")

        # العنوان
        ctk.CTkLabel(self, text="🛠️ Android Tool",
                     font=("Arial", 24, "bold")).pack(pady=8)

        # شريط حالة الأدوات
        self.status = ctk.CTkLabel(self, text="", font=("Arial", 12))
        self.status.pack()

        # إطار الأزرار الرئيسية
        frame = ctk.CTkFrame(self)
        frame.pack(fill="x", padx=15, pady=8)

        btns = [
            ("📥 تحميل Platform-Tools", self.download_tools),
            ("🔍 اكتشاف الأجهزة", self.detect),
            ("📱 معلومات الجهاز", self.info),
            ("🔄 إعادة تشغيل", lambda: self.async_run(lambda: run([ADB, "reboot"]))),
            ("⚡ وضع Fastboot", lambda: self.async_run(lambda: run([ADB, "reboot", "bootloader"]))),
            ("♻️ وضع Recovery", lambda: self.async_run(lambda: run([ADB, "reboot", "recovery"]))),
            ("🔌 خروج من Fastboot", lambda: self.async_run(lambda: run([FASTBOOT, "reboot"]))),
            ("🧹 محو Cache", lambda: self.async_run(lambda: run([FASTBOOT, "erase", "cache"]))),
            ("🗑️ محو Userdata", self.wipe_userdata),
        ]
        for i, (t, f) in enumerate(btns):
            ctk.CTkButton(frame, text=t, width=200, height=38,
                          command=f).grid(row=i // 3, column=i % 3, padx=6, pady=6)

        # إطار الفلاش
        ff = ctk.CTkFrame(self)
        ff.pack(fill="x", padx=15, pady=8)
        ctk.CTkLabel(ff, text="📦 فلاش قسم (Fastboot)",
                     font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=5, pady=5)

        ctk.CTkLabel(ff, text="القسم:").grid(row=1, column=0, padx=5)
        self.part = ctk.CTkEntry(ff, width=150)
        self.part.grid(row=1, column=1, padx=5)
        self.part.insert(0, "boot")

        ctk.CTkLabel(ff, text="الصورة:").grid(row=1, column=2, padx=5)
        self.img = ctk.CTkEntry(ff, width=300)
        self.img.grid(row=1, column=3, padx=5)

        ctk.CTkButton(ff, text="اختر", width=70,
                      command=self.pick_img).grid(row=1, column=4, padx=5)
        ctk.CTkButton(ff, text="🚀 فلاش", width=120, fg_color="green",
                      hover_color="darkgreen",
                      command=self.flash).grid(row=2, column=0, columnspan=5, pady=8)

        # السجل
        ctk.CTkLabel(self, text="📋 السجل:",
                     font=("Arial", 14, "bold")).pack(anchor="w", padx=15)
        self.log_box = ctk.CTkTextbox(self, font=("Consolas", 12))
        self.log_box.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        self.check_tools()

    # ============ أدوات مساعدة ============
    def log(self, t):
        self.log_box.insert("end", str(t) + "\n")
        self.log_box.see("end")
        self.update_idletasks()

    def async_run(self, fn):
        def wrap():
            self.log("⏳ ...")
            self.log(fn())
        threading.Thread(target=wrap, daemon=True).start()

    def check_tools(self):
        if os.path.exists(ADB) and os.path.exists(FASTBOOT):
            self.status.configure(text="✅ Platform-Tools مثبتة",
                                  text_color="lightgreen")
            self.log(f"✅ الأدوات جاهزة في: {TOOLS_DIR}")
        else:
            self.status.configure(text="⚠️ Platform-Tools غير مثبتة — اضغط الزر الأول",
                                  text_color="orange")

    # ============ تحميل Platform-Tools ============
    def download_tools(self):
        def task():
            try:
                os.makedirs(APP_DIR, exist_ok=True)
                zip_path = os.path.join(APP_DIR, "pt.zip")
                self.log(f"📥 جاري التحميل من:\n{PLATFORM_TOOLS_URL}")

                def hook(b, bs, total):
                    if total > 0:
                        pct = int(b * bs * 100 / total)
                        self.status.configure(text=f"📥 التحميل {pct}%")

                urllib.request.urlretrieve(PLATFORM_TOOLS_URL, zip_path, hook)
                self.log("✅ تم التحميل، جاري فك الضغط...")

                with zipfile.ZipFile(zip_path, "r") as z:
                    z.extractall(APP_DIR)
                os.remove(zip_path)

                self.log("✅ تم التثبيت بنجاح!")
                self.check_tools()
            except Exception as e:
                self.log(f"❌ فشل: {e}")
                self.status.configure(text="❌ فشل التحميل", text_color="red")

        threading.Thread(target=task, daemon=True).start()

    # ============ اكتشاف ============
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

    # ============ الفلاش ============
    def pick_img(self):
        p = filedialog.askopenfilename(
            filetypes=[("Images", "*.img *.bin"), ("All", "*.*")])
        if p:
            self.img.delete(0, "end")
            self.img.insert(0, p)

    def flash(self):
        part = self.part.get().strip()
        img = self.img.get().strip()
        if not part or not img or not os.path.exists(img):
            messagebox.showerror("خطأ", "تحقق من اسم القسم والملف")
            return

        def t():
            self.log("=" * 50)
            self.log(f"🚀 فلاش {part} ← {img}")
            self.log(run([FASTBOOT, "flash", part, img], timeout=600))
        threading.Thread(target=t, daemon=True).start()

    def wipe_userdata(self):
        if not messagebox.askyesno("تأكيد", "سيتم محو كل بيانات الجهاز! متأكد؟"):
            return
        self.async_run(lambda: run([FASTBOOT, "erase", "userdata"], timeout=300))


if __name__ == "__main__":
    App().mainloop()