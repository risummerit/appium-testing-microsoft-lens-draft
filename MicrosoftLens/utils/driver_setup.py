from appium import webdriver
from appium.options.android import UiAutomator2Options
from .config import *

def create_driver():
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.device_name = DEVICE_NAME
    options.app_package = APP_PACKAGE
    options.app_activity = APP_ACTIVITY
    options.automation_name = "UiAutomator2"
    options.no_reset = True
    options.full_reset = False
    options.ignore_hidden_api_policy_error = True

    return webdriver.Remote(APPIUM_HOST, options=options)
