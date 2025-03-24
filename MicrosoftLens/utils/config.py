from dotenv import load_dotenv
import os

load_dotenv()

DEVICE_NAME = os.getenv("DEVICE_NAME")
# HOST = os.getenv("APPIUM_SERVER", "http://localhost:4723")
APK_PATH = os.getenv("APK_PATH", "/app/MicrosoftLens/MicrosoftLens.apk")
APP_PACKAGE = os.getenv("APP_PACKAGE")
APP_ACTIVITY = os.getenv("APP_ACTIVITY")
APPIUM_HOST = os.getenv("APPIUM_HOST")
RECEIPT_FILENAME = os.getenv("RECEIPT_FILENAME")
FILE_NAME = os.getenv("FILE_NAME")
FILE_FORMAT = ".jpg"
LOCAL_RECEIPT_PATH = f"MicrosoftLens/assets/{RECEIPT_FILENAME}"
DEVICE_RECEIPT_PATH = "/sdcard/Download/receipt.jpg"
DEVICE_RECEIPT_PATH_SCANS = "/sdcard/Pictures/Office Lens/"