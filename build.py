import os
import platform
import subprocess
from pathlib import Path
import shutil

APP_NAME = "billable_tracker"
PY_FILE = f"{APP_NAME}.py"
DIST_DIR = Path("dist")
BUILD_DIR = Path("build")

def clean_previous():
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
    if Path(f"{APP_NAME}.spec").exists():
        Path(f"{APP_NAME}.spec").unlink()

def build_windows():
    print("[*] Building for Windows using PyInstaller...")
    subprocess.run([
        "pyinstaller",
        "--noconfirm",
        "--onefile",
        "--windowed",
        PY_FILE
    ], check=True)
    zip_output(DIST_DIR / f"{APP_NAME}.exe")

def build_mac():
    print("[*] Building for macOS using py2app...")
    with open("setup.py", "w") as f:
        f.write(f"""
from setuptools import setup

APP = ['{APP_NAME}.py']
OPTIONS = {{
    'argv_emulation': True,
    'packages': ['tkinter']
}}

setup(
    app=APP,
    options={{'py2app': OPTIONS}},
    setup_requires=['py2app'],
)
""")
    subprocess.run(["python3", "setup.py", "py2app"], check=True)
    zip_output(DIST_DIR / f"{APP_NAME}.app")

def zip_output(target_path):
    zip_name = f"{APP_NAME}_{platform.system().lower()}.zip"
    print(f"[*] Zipping: {target_path} → {zip_name}")
    if target_path.is_dir():
        shutil.make_archive(zip_name.replace(".zip", ""), "zip", target_path)
    else:
        with shutil.make_archive(zip_name.replace(".zip", ""), "zip", root_dir=target_path.parent, base_dir=target_path.name):
            pass

def main():
    clean_previous()
    current_os = platform.system().lower()

    if current_os == "windows":
        build_windows()
    elif current_os == "darwin":
        build_mac()
    else:
        print("❌ Unsupported OS. Only Windows and macOS are supported.")

if __name__ == "__main__":
    main()
