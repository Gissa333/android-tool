import customtkinter as ctk
import subprocess
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

PLATFORM_TOOLS = r"C:\platform-tools"
ADB = os.path.join(PLATFORM_TOOLS, "adb.exe")
FASTBOOT = os.path.join(PLATFORM_TOOLS, "fastboot.exe")


def run(cmd, timeout=60):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True,
                           timeout=timeout, encoding="utf-8", errors="ignore")
        return r.stdout + r.stderr
    except Exception as e:
        return f"خطأ: {e}"


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Android Tool v0.1")
        self.geometry("900x650")

        ctk.CTkLabel(self, text="🛠️ Android Tool",
                     font=("Arial", 22, "bold")).pack(pady=10)

        frame = ctk.CTkFrame(self)
        frame.pack(fill="x", padx=15, pady=5)

        buttons = [
            ("🔍 اكتشاف الأجهزة", self.detect),
            ("📱 معلومات الجهاز", self.info),
            ("🔄 إعادة تشغيل", lambda: self.log(run([ADB, "reboot"]))),
            ("⚡ Fastboot", lambda: self.log(run([ADB, "reboot", "bootloader"]))),
            ("♻️ Recovery", lambda: self.log(run([ADB, "reboot", "recovery"]))),
            ("🔌 خروج من Fastboot", lambda: self.log(run([FASTBOOT, "reboot"]))),
        ]
        for i, (t, f) in enumerate(buttons):
            ctk.CTkButton(frame, text=t, width=170, height=40,
                          command=f).grid(row=i // 3, column=i % 3, padx=8, pady=8)

        ctk.CTkLabel(self, text="📋 السجل:",
                     font=("Arial", 14, "bold")).pack(anchor="w", padx=15)

        self.log_box = ctk.CTkTextbox(self, font=("Consolas", 12))
        self.log_box.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    def log(self, text):
        self.log_box.insert("end", text + "\n")
        self.log_box.see("end")

    def detect(self):
        self.log("=" * 50)
        self.log("— ADB —\n" + run([ADB, "devices", "-l"]))
        self.log("— Fastboot —\n" + run([FASTBOOT, "devices"]))

    def info(self):
        self.log("=" * 50)
        for p in ["ro.product.model", "ro.product.brand",
                  "ro.build.version.release", "ro.serialno",
                  "ro.product.cpu.abi"]:
            self.log(f"{p}: {run([ADB, 'shell', 'getprop', p]).strip()}")


if __name__ == "__main__":
    App().mainloop()