import customtkinter as ctk
import requests
import threading
import time
import sys
import os



def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class DucoDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()
        # ... (đoạn code của bạn)
        icon_path = get_resource_path("duino.ico")
        if os.path.exists(icon_path):
            self.iconbitmap(icon_path)
        # ...
        self.title("Duino-Coin DashBoard")
        self.geometry("500x662")

        icon_path = get_resource_path("duino.ico")  # Đảm bảo file tên là duino.ico
        if os.path.exists(icon_path):
            self.iconbitmap(icon_path)



        self.entry = ctk.CTkEntry(self, placeholder_text="Username...")
        self.entry.pack(pady=10, padx=20, fill="x")



        self.remember_var = ctk.BooleanVar()
        self.checkbox = ctk.CTkCheckBox(self, text="Remember me", variable=self.remember_var)
        self.checkbox.pack(pady=5)

        self.balance_label = ctk.CTkLabel(self, text="Balance: ---", font=("Arial", 20, "bold"))
        self.balance_label.pack(pady=10)

        self.miner_frame = ctk.CTkScrollableFrame(self, height=150, label_text="Device List")
        self.miner_frame.pack(pady=10, padx=20, fill="x")

        self.log_box = ctk.CTkTextbox(self, height=200, font=("Consolas", 12))
        self.log_box.pack(pady=10, padx=20, fill="both", expand=True)
        self.log_box.configure(state="disabled")

        if os.path.exists("config.txt"):
            with open("config.txt", "r") as f:
                self.entry.insert(0, f.read().strip())
                self.remember_var.set(True)
        self.add_log("--------------------------------------------")

        self.add_log("Welcome to Duino-Coin DashBoard !")
        self.add_log("")
        self.add_log("Real time update Duino-Coin DashBoard")
        self.add_log("")
        self.add_log("This programme by Razester72 with Pycharm")
        self.add_log("")
        self.add_log("1. Fill your name on blank 'Username...'")
        self.add_log("")
        self.add_log("2. Please wait 15s to load data...")
        self.add_log("--------------------------------------------")
        self.add_log("")

        self.running = True
        threading.Thread(target=self.auto_update, daemon=True).start()

        self.version_label = ctk.CTkLabel(
            self,
            text="v1.6 by Razester72",
            font=("Arial", 10),
            text_color="#888888"
        )
        self.version_label.pack(side="left", padx=20, pady=8, anchor="sw")

    def add_log(self, message):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", f"[{time.strftime('%H:%M:%S')}] {message}\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def reset_ui(self):
        self.balance_label.configure(text="Balance: ---")
        for widget in self.miner_frame.winfo_children():
            widget.destroy()
        self.add_log("Not Found User!")

    def save_user(self, username):
        if self.remember_var.get():
            with open("config.txt", "w") as f:
                f.write(username)
        elif os.path.exists("config.txt"):
            os.remove("config.txt")

    def auto_update(self):
        while self.running:
            self.load_data()
            time.sleep(15)

    def load_data(self):
        username = self.entry.get()
        self.save_user(username)
        try:
            url = f"https://server.duinocoin.com/users/{username}"
            response = requests.get(url, timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
            data = response.json()

            if data.get('success'):
                bal = data['result']['balance']['balance']
                self.balance_label.configure(text=f"Balance: {float(bal):.15f} DUCO")

                miners = data['result']['miners']
                for widget in self.miner_frame.winfo_children():
                    widget.destroy()

                if not miners:
                    ctk.CTkLabel(self.miner_frame, text="No Device Connect", text_color="red").pack(anchor="w")
                else:
                    for miner in miners:
                        good = float(miner.get('accepted', 0))
                        bad = float(miner.get('rejected', 0))
                        percent = (good / (good + bad) * 100) if (good + bad) > 0 else 0
                        is_active = float(miner['hashrate']) > 0
                        status_text = "●" if is_active else "○"
                        status_color = "#2CC985" if is_active else "#FF3E3E"

                        m_text = f"{status_text} {miner['software']} | {miner['hashrate']} H/s | {percent:.1f}%"
                        ctk.CTkLabel(self.miner_frame, text=m_text, text_color=status_color).pack(anchor="w")
                        self.add_log(f"Miner {miner['software']}: Eff: {percent:.1f}%")
            else:
                self.reset_ui()
        except Exception:
            self.reset_ui()

if __name__ == "__main__":
    app = DucoDashboard()
    app.mainloop()