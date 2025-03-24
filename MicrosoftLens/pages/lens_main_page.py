from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LensPages:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def allow_permissions(self):
        try:
            self.wait.until(EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Allow Lens to access photos and videos on this device?")')))
            self.driver.find_element(AppiumBy.ID, 'com.android.permissioncontroller:id/permission_allow_button').click()
        except:
            print("No permissions dialog appeared.")
    
    def start_scanning(self):
        try:
            self.wait.until(EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("START SCANNING")')))
            self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'New Capture').click()
        except Exception as e:
            print(f"'Start Scanning' page didn't apper, , continuing...")
    
    def microsoft_privacy(self):
        try:
            self.wait.until(EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Microsoft respects your privacy")')))
            self.driver.find_element(AppiumBy.ID, 'com.microsoft.office.officelens:id/next_button').click()
        except Exception as e:
            print(f"'Microsoft respects your privacy' page didn't apper, , continuing...")

    def sending_optional_data_to_microsoft(self):
        try:
            self.wait.until(EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Getting better together")')))
            self.driver.find_element(AppiumBy.ID, 'com.microsoft.office.officelens:id/accept_basic').click()
        except Exception as e:
            print(f"'Sending optional data to Microsoft' page didn't apper, , continuing...")

    def powering_your_experiences_page(self):
        try:
            self.wait.until(EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Powering your experiences")')))
            self.driver.find_element(AppiumBy.ID, 'com.microsoft.office.officelens:id/close_button').click()
        except Exception as e:
            print(f"'Powering your experiences' page didn't apper, continuing...")

    def allow_lens_to_take_pictures_and_record_video_page(self):
        try:
            self.wait.until(EC.presence_of_element_located((AppiumBy.ID, 'com.android.permissioncontroller:id/permission_message')))
            self.driver.find_element(AppiumBy.ID, 'com.android.permissioncontroller:id/permission_allow_foreground_only_button').click()
            print("Allow Lens to take pictures and record video page - Clicked")
        except Exception as e:
            print(f"'Upload receipt - click upload from device button' Failed: {e}")

    def upload_receipt(self, file_name):
        self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Import'))).click()
        self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Native Gallery'))).click()
        self.wait.until(EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("More options")'))).click()
        self.wait.until(EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Browse…")'))).click()
        self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'receipt.jpg, 121 kB, Mar 19'))).click()

        self.wait.until(EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.microsoft.office.officelens:id/bottomNavigationItemButton").instance(2)'))).click()
        self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Reset crop borders'))).click()
        self.wait.until(EC.element_to_be_clickable((AppiumBy.ID, 'com.microsoft.office.officelens:id/crop_commit_button'))).click()
        self.wait.until(EC.element_to_be_clickable((AppiumBy.ID, 'com.microsoft.office.officelens:id/lenshvc_pill_button_label'))).click()

        title = self.wait.until(EC.presence_of_element_located((AppiumBy.ID, 'com.microsoft.office.officelens:id/title')))
        title.send_keys(file_name)
        self.wait.until(EC.element_to_be_clickable((AppiumBy.ID, 'com.microsoft.office.officelens:id/button_save_share'))).click()

    def assert_receipt_saved(self, file_name):
        self.wait.until(EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("My Scans")'))).click()
        files = self.driver.find_elements(AppiumBy.ID, "com.microsoft.office.officelens:id/title")
        file_names = [f.text for f in files]
        assert file_name in file_names, f"{file_name} not found!"
