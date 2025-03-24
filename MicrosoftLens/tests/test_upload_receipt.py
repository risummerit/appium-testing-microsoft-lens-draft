import pytest
from MicrosoftLens.utils.adb_utils import install_app, push_receipt_image, delete_images, uninstall_app
from MicrosoftLens.utils.driver_setup import create_driver
from MicrosoftLens.pages.lens_main_page import LensPages
from MicrosoftLens.utils.config import *


@pytest.mark.microsoftLens
def test_upload_receipt():
    install_app()
    push_receipt_image()

    driver = create_driver()
    driver.activate_app(APP_PACKAGE)
    page = LensPages(driver)

    try:
        page.allow_permissions()
        page.start_scanning()
        page.microsoft_privacy()
        page.sending_optional_data_to_microsoft()
        page.powering_your_experiences_page()
        page.allow_lens_to_take_pictures_and_record_video_page()
        page.upload_receipt(FILE_NAME)
        page.assert_receipt_saved(FILE_NAME)
    finally:
        delete_images()
        uninstall_app()
        driver.quit()
