import json
import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


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

    driver.get(test["url"])
    time.sleep(12)

    driver.find_element(By.LINK_TEXT, "Form Authentication").click()
    time.sleep(12)

    driver.find_element(By.ID, "username").clear()
    driver.find_element(By.ID, "username").send_keys(test["username"])

    driver.find_element(By.ID, "password").clear()
    driver.find_element(By.ID, "password").send_keys(test["password"])

    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(12)

    message = driver.find_element(By.ID, "flash").text

    try:
        assert test["expected_message"] in message
    except AssertionError:
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")

        screenshot_name = f"screenshots/{test['scenario'].replace(' ', '_')}.png"
        driver.save_screenshot(screenshot_name)
        pytest.fail(f"Test Failed. Screenshot saved: {screenshot_name}")