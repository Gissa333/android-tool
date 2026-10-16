import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Android Tool v0.1")
        self.geometry("600x400")

        ctk.CTkLabel(
            self,
            text="🛠️ Android Tool",
            font=("Arial", 24, "bold")
        ).pack(pady=40)

        ctk.CTkLabel(
            self,
            text="النسخة الأولى — قيد التطوير",
            font=("Arial", 14)
        ).pack(pady=10)


if __name__ == "__main__":
    App().mainloop()