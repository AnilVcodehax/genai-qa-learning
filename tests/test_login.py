import pytest
import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.login_page import LoginPage

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


def load_test_data():
    with open("testcases.json") as f:
        data = json.load(f)
    return data["test_cases"]


@pytest.mark.parametrize("test", load_test_data())
def test_login(driver, test):

    page = LoginPage(driver)

    page.open(test["url"])
    page.click_form_auth()
    page.login(test["username"], test["password"])

    message = page.get_flash_message()

    try:
        assert test["expected_message"] in message
    except AssertionError:
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")

        screenshot_name = f"screenshots/{test['scenario'].replace(' ', '_')}.png"
        driver.save_screenshot(screenshot_name)
        pytest.fail(f"Test Failed. Screenshot saved: {screenshot_name}")