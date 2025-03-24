from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import subprocess


options = UiAutomator2Options()
options.platform_name = "Android"
options.device_name = "emulator-5554"
options.app_package = "com.microsoft.office.officelens"
options.app_activity = "com.microsoft.office.officelens.MainActivity"
options.automation_name = "UiAutomator2"
options.ensure_webviews_have_pages = True
options.no_reset = True
options.full_reset = False
options.ignore_hidden_api_policy_error = True  # Fix API policy error


HOST = "http://localhost:4723"
APK_PATH = "MicrosoftLens/MicrosoftLens.apk"
APP_PACKAGE = "com.microsoft.office.officelens"
FILE_NAME = "WalmartGroceryReceipt"
FILE_FORMAT = ".jpg"
LOCAL_RECEIPT_PATH = "MicrosoftLens/Grocery-Payment-Receipt.jpg"  # CHANGE THIS: Path to the receipt image on your PC
DEVICE_RECEIPT_PATH = "/sdcard/Download/receipt.jpg"  # Path where the file will be stored on the phone
DEVICE_RECEIPT_PATH_SCANS = f"/sdcard/Pictures/Office Lens/"


# Function to run ADB commands
def run_adb_command(command):
    """Executes an ADB command and returns the output."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        print(f"ADB command failed: {e}")
        return None


### **📌 Step 1: Install the App Before Running Tests**
def setup():
    """Installs the app via ADB if not installed."""
    installed_apps = run_adb_command("adb shell pm list packages")
    
    if APP_PACKAGE in installed_apps:
        print("✅ App already installed, skipping installation.")
    else:
        print("📥 Installing Microsoft Lens via ADB...")
        install_output = run_adb_command(f"adb install {APK_PATH}")
        print(f"Install Output: {install_output}")
        time.sleep(3)

    # Upload receipt image to the device before the test
    print(f"📤 Uploading receipt image to {DEVICE_RECEIPT_PATH}...")
    run_adb_command(f"adb push {LOCAL_RECEIPT_PATH} {DEVICE_RECEIPT_PATH}")

setup()  # Call setup to install the app

# Start Appium Driver
driver = webdriver.Remote(HOST, options=options)
wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds for elements

try:
    # Activate the app before tests
    driver.activate_app(APP_PACKAGE)


    # These are movements for the test
    # Allowing permission to access photos
    try:
        wait.until(EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Allow Lens to access photos and videos on this device?")')))
        driver.find_element(AppiumBy.ID, 'com.android.permissioncontroller:id/permission_allow_button').click()
        time.sleep(2)

    except Exception as e:
        print(f"'Allowing permission to access photos' page didn't apper, , continuing...")
        # print(f"❌ 'Allowing permission to access photos' Failed: {e}")

    # Start Scanning
    try:
        wait.until(EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("START SCANNING")')))
        driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'New Capture').click()
        time.sleep(2)

    except Exception as e:
        print(f"'Start Scanning' page didn't apper, , continuing...")
        # print(f"❌ 'Start Scanning' Failed: {e}")

    # Microsoft respects your privacy
    try:
        wait.until(EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Microsoft respects your privacy")')))
        driver.find_element(AppiumBy.ID, 'com.microsoft.office.officelens:id/next_button').click()
        time.sleep(2)

    except Exception as e:
        print(f"'Microsoft respects your privacy' page didn't apper, , continuing...")
        # print(f"❌ 'Microsoft respects your privacy' page Failed: {e}")

    # Sending optional data to Microsoft option
    try:
        wait.until(EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Getting better together")')))
        driver.find_element(AppiumBy.ID, 'com.microsoft.office.officelens:id/accept_basic').click()
        time.sleep(2)

    except Exception as e:
        print(f"'Sending optional data to Microsoft' page didn't apper, , continuing...")
        # print(f"❌ 'Sending optional data to Microsoft' Failed: {e}")

    # Powering your experiences
    try:
        wait.until(EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Powering your experiences")')))
        driver.find_element(AppiumBy.ID, 'com.microsoft.office.officelens:id/close_button').click()
        time.sleep(2)

    except Exception as e:
        print(f"'Powering your experiences' page didn't apper, continuing...")
        # print(f"❌ 'Powering your experiences' Failed: {e}")


    # Allow Lens to take pictures and record video page
    try:
        wait.until(EC.presence_of_element_located((AppiumBy.ID, 'com.android.permissioncontroller:id/permission_message')))
        driver.find_element(AppiumBy.ID, 'com.android.permissioncontroller:id/permission_allow_foreground_only_button').click()
        print("Allow Lens to take pictures and record video page - Clicked")
        time.sleep(2)

    except Exception as e:
        print(f"❌ 'Upload receipt - click upload from device button' Failed: {e}")


    # Upload receipt - click upload from device button
    try:
        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Import'))).click()
        time.sleep(2)

    except Exception as e:
        print(f"'Allow Lens to take pictures and record video' page didn't apper, , continuing...")
        # print(f"❌ 'Allow Lens to take pictures and record video' Failed: {e}")


    # Upload receipt - Open gallery
    try:
        wait.until(EC.presence_of_element_located((AppiumBy.ID, 'com.microsoft.office.officelens:id/capture_fragment_root_view')))

        element = wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Native Gallery'))).click()
        time.sleep(2)


        # wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'More options')))
        wait.until(EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("More options")'))).click()
        time.sleep(2)

        wait.until(EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Browse…")'))).click()
        time.sleep(2)

        wait.until(EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Images in Downloads")')))
        time.sleep(2)
        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'receipt.jpg, 121 kB, Mar 19'))).click()


        # Clip on Crop button to select the whole image
        wait.until(EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.microsoft.office.officelens:id/bottomNavigationItemButton").instance(2)'))).click()
        time.sleep(2)
        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Reset crop borders'))).click()
        wait.until(EC.element_to_be_clickable((AppiumBy.ID, 'com.microsoft.office.officelens:id/crop_commit_button'))).click()
        # Click Done
        wait.until(EC.element_to_be_clickable((AppiumBy.ID, 'com.microsoft.office.officelens:id/lenshvc_pill_button_label'))).click()


        # Name the file and save it
        titleText = wait.until(EC.presence_of_element_located((AppiumBy.ID, 'com.microsoft.office.officelens:id/title'))).send_keys(FILE_NAME)
        # By default 'Gallery' is checked
        # Click Save button
        wait.until(EC.element_to_be_clickable((AppiumBy.ID, 'com.microsoft.office.officelens:id/button_save_share'))).click()

        # Now check if it's saved in gallery
        wait.until(EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("My Scans")'))).click()
        time.sleep(2)

        # Find all file elements inside the recent scans list
        files = driver.find_elements(AppiumBy.ID, "com.microsoft.office.officelens:id/title")

        # Extract the text (file names)
        file_names = [file.text for file in files]

        # Assert WalmartGroceryReceipt is in the list
        assert FILE_NAME in file_names, f"{FILE_NAME} is NOT found!"

    except Exception as e:
        print(f"❌ 'Upload receipt' Failed: {e}")


finally:

    ### **📌 Step 2: Delete the Receipt Image from the Device After Test**
    def delete_receipt_image():
        """Deletes the uploaded receipt image after the test."""
        print(f"🗑️ Deleting receipt image from {DEVICE_RECEIPT_PATH}")
        delete_output = run_adb_command(f"adb shell rm {DEVICE_RECEIPT_PATH}")
        print(f"🗑️ Deleting receipt image from {DEVICE_RECEIPT_PATH_SCANS}{FILE_NAME}{FILE_FORMAT}")
        delete_output_scan = run_adb_command(f"adb shell 'rm \"{DEVICE_RECEIPT_PATH_SCANS}{FILE_NAME}{FILE_FORMAT}\"'")
        print(f"Delete Outputs: 'str({delete_output})' and 'str({delete_output_scan})'")

    ### **📌 Step 3: Uninstall the App After Tests Using ADB**
    def teardown():
        """Uninstalls the app via ADB after the tests are complete."""
        print("📤 Uninstalling Microsoft Lens via ADB...")
        uninstall_output = run_adb_command(f"adb uninstall {APP_PACKAGE}")
        print(f"Uninstall Output: {uninstall_output}")
        driver.quit()

    delete_receipt_image()  # Delete the uploaded file
    teardown()  # Call teardown after test execution

