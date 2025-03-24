import subprocess
from .config import *

def run_adb_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        print(f"ADB command failed: {e}")
        return None

def install_app():
    installed = run_adb_command("adb shell pm list packages")
    if APP_PACKAGE not in installed:
        print("📥 Installing app...")
        run_adb_command(f"adb install {APK_PATH}")

def push_receipt_image():
    print("📤 Pushing receipt image...")
    run_adb_command(f"adb push {LOCAL_RECEIPT_PATH} {DEVICE_RECEIPT_PATH}")

def delete_images():
    print("🧹 Cleaning up receipt images...")
    run_adb_command(f"adb shell rm {DEVICE_RECEIPT_PATH}")
    run_adb_command(f"adb shell 'rm \"{DEVICE_RECEIPT_PATH_SCANS}{FILE_NAME}{FILE_FORMAT}\"'")

def uninstall_app():
    print("📤 Uninstalling app...")
    run_adb_command(f"adb uninstall {APP_PACKAGE}")
