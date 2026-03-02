from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from core.logger import get_logger
import os
from datetime import datetime


logger = get_logger("KeywordEngine")
class ActionHandler:

    def __init__(self, driver, logger=None):
        self.driver = driver
        self.logger = logger
        self.wait = WebDriverWait(driver, 10)

    def open_url(self, value):
        self.driver.get(value)

    def enter_text(self, locator, value):
        element = self.wait.until(
            EC.visibility_of_element_located((By.ID, locator))
        )
        element.clear()
        element.send_keys(value)
        #print(f"Entered text into {locator}: {value}")
        logger.info(f"Entered text into {locator}: {value}")
        

    def click(self, locator):
        element = self.wait.until(
            EC.presence_of_element_located((By.ID, locator))
        )
        #print("Submitting form using submit():", locator)
        logger.info("Logger - Submitting form using submit():%s",locator)
        element.submit()


    # Capture screen shot
    def capture_screenshot(self, test_name):
        import os
        from datetime import datetime

        os.makedirs("screenshots", exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = f"screenshots/{test_name}_{timestamp}.png"

        self.driver.save_screenshot(file_path)
        return file_path


    '''
    # without try/except
    def assert_text(self, locator, value):
        #print("Current URL during assert:", self.driver.current_url)
        logger.info("Current URL during assert:%s", self.driver.current_url)
        element = self.wait.until(
        EC.visibility_of_element_located((By.ID, locator))
        )

        actual_text = element.text.strip()
        #print("Actual message:", actual_text)
        logger.info("Actual message:%s", actual_text)
        assert value in actual_text, \
            f"Expected '{value}' but got '{actual_text}'"
    '''

    # assert text with try/except

    def assert_text(self, locator, value, test_name=None):
        try:
            # Wait until the element is visible
            element = self.wait.until(
            EC.visibility_of_element_located((By.ID, locator))
            )
            actual_text = element.text.strip()
            # Log current URL and actual message
            if self.logger:
                self.logger.info("Current URL during assert: %s", self.driver.current_url)
                self.logger.info("Actual message: %s", actual_text)
            else:
                print("Current URL during assert:", self.driver.current_url)
                print("Actual message:", actual_text)

            # Perform assertion
            assert value in actual_text, f"Expected '{value}' but got '{actual_text}'"

        except AssertionError as e:
            # Capture screenshot on failure
            self.take_screenshot(test_name=test_name)
            if self.logger:
                self.logger.error(f"Assertion failed for '{test_name}': {e}")
            raise  # Re-raise the exception so pytest marks the test as failed


    def take_screenshot(self, test_name=None, step_name=None):
        """
        Captures a screenshot of the current browser window.

        Parameters:
        - test_name: Optional. Name of the test. Used for naming the file.
        - step_name: Optional. Name of the step or action. Used for naming the file.

        Behavior:
        - If test_name is provided, screenshot filename will include it.
        - If step_name is provided, filename will include step info.
        - Automatically creates the 'screenshots' folder if missing.
        """


        try:
            # 1️⃣ Define screenshots folder path
            screenshots_path = os.path.join(
                os.path.dirname(__file__), "..", "screenshots"
            )
            screenshots_path = os.path.abspath(screenshots_path)

            # 2️⃣ Create folder if it doesn't exist
            if not os.path.exists(screenshots_path):
                os.makedirs(screenshots_path)
            
            # 3️⃣ Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_test_name = test_name.replace(" ", "_") if test_name else "Test"
            safe_step_name = step_name.replace(" ", "_") if step_name else ""
            
            file_name = f"{safe_test_name}"

            full_path = os.path.join(screenshots_path, file_name)
            if safe_step_name:
                file_name += f"_{safe_step_name}"
            file_name += f"_{timestamp}.png"
            full_path = os.path.join(screenshots_path, file_name)
            
            # 4️⃣ Capture screenshot
            self.driver.save_screenshot(full_path)

            # 5️⃣ Log success
            if hasattr(self, "logger") and self.logger:
                self.logger.info(f"Screenshot saved: {full_path}")
            else:
                print(f"Screenshot saved: {full_path}")

        except Exception as e:
            # 6️⃣ Handle any errors
            if hasattr(self, "logger") and self.logger:
                self.logger.error(f"Failed to capture screenshot: {e}")
            else:
                print(f"Failed to capture screenshot: {e}")




    