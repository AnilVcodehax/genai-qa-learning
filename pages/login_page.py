from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # Locators
    FORM_AUTH_LINK = (By.LINK_TEXT, "Form Authentication")
    USERNAME = (By.ID, "username")
    PASSWORD = (By.ID, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    FLASH_MESSAGE = (By.ID, "flash")

    # Actions
    def open(self, url):
        self.driver.get(url)

    def click_form_auth(self):
        self.wait.until(EC.element_to_be_clickable(self.FORM_AUTH_LINK)).click()

    def login(self, username, password):
        self.wait.until(EC.visibility_of_element_located(self.USERNAME)).clear()
        self.wait.until(EC.visibility_of_element_located(self.USERNAME)).send_keys(username)

        self.wait.until(EC.visibility_of_element_located(self.PASSWORD)).clear()
        self.wait.until(EC.visibility_of_element_located(self.PASSWORD)).send_keys(password)

        self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON)).click()

    def get_flash_message(self):
        return self.wait.until(EC.visibility_of_element_located(self.FLASH_MESSAGE)).text