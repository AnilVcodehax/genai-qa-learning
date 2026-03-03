import os
import pytest
from selenium import webdriver
from core.keyword_engine import KeywordEngine
from core.driver_factory import get_driver
from utils.logger import get_logger

logger = get_logger("TestRunner")

"""
# code for local run only
@pytest.fixture
def driver():
    #driver = webdriver.Chrome()
    driver = get_driver()
    driver.maximize_window()
    yield driver
    driver.quit()
    """
# Make Selenium headless (CI-friendly)
@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


def test_execute_keyword_framework(driver):
    engine = KeywordEngine(driver)
    engine.execute_test_file("login_test.json")


