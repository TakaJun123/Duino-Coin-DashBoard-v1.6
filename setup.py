import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"  # Ẩn hoàn toàn màn hình đen CMD khi chạy app

build_exe_options = {
    # TUI ĐÃ THÊM: "customtkinter" và "requests" vào đây để không bị lỗi thiếu thư viện
    "packages": ["os", "tkinter", "threading", "shutil", "subprocess", "customtkinter", "requests"],
    "include_files": ["duino.ico"]  # Nhúng file icon chuẩn vào thư mục build
}

setup(
    name="Duino-Coin DashBoard",
    version="1.0",
    description="Duino-Coin DashBoard - DuCo Miner DashBoard",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            "Main.py",
            base=base,
            target_name="Duino-Coin DashBoard.exe",
            icon="duino.ico"  # Ép icon chữ D màu cam hiển thị ngoài màn hình
        )
    ]
)