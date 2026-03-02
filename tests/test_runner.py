import os
import pytest
from selenium import webdriver
from core.keyword_engine import KeywordEngine
from core.driver_factory import get_driver
from core.logger import get_logger

logger = get_logger("TestRunner")

@pytest.fixture
def driver():
    #driver = webdriver.Chrome()
    driver = get_driver()
    driver.maximize_window()
    yield driver
    driver.quit()


def test_execute_keyword_framework(driver):
    engine = KeywordEngine(driver)
    
    json_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "testcases",
        "login_test.json"
    )

    engine.execute_test_file(json_path)


