import random
import string
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

class TestSignUpSuite:
    def setup_method(self, method):
        self.driver = webdriver.Edge()
        self.driver.set_window_size(1552, 832)
        self.driver.get("http://127.0.0.1:8000/")
    
    def teardown_method(self, method):
        self.driver.quit()

    def navigate_to_register_page(self):
        self.driver.find_element(By.CSS_SELECTOR, ".nav-link:nth-child(2)").click()
        self.driver.find_element(By.LINK_TEXT, "Register").click()

    def fill_registration_form(self, name, email, password, password_confirm):
        self.driver.find_element(By.ID, "name").send_keys(name)
        self.driver.find_element(By.ID, "email").send_keys(email)
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.ID, "passwordConfirm").send_keys(password_confirm)

    def submit_registration_form(self):
        self.driver.find_element(By.CSS_SELECTOR, ".mt-3").click()

    def generate_unique_email(self):
        """ Helper function to generate a unique email using random string """
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        return f"testuser{random_string}@example.com"

    def test_register_success(self):
        self.navigate_to_register_page()
        unique_email = self.generate_unique_email()  
        self.fill_registration_form("hello", unique_email, "helloworld", "helloworld")
        self.submit_registration_form()
        time.sleep(3)
        elements = self.driver.find_elements(By.ID, "username")
        assert len(elements) > 0, "User was not logged in after successful registration."

    def test_empty_email(self):
        self.navigate_to_register_page()
        self.fill_registration_form("testuser", "", "123456", "123456")
        self.submit_registration_form()
        elements = self.driver.find_elements(By.CSS_SELECTOR, ".banner-image")
        assert len(elements) == 0, "The sign-up might have been successful when it shouldn't have been."

    def test_empty_name(self):
        self.navigate_to_register_page()
        self.fill_registration_form("", "test@example.com", "123456", "123456")
        self.submit_registration_form()
        elements = self.driver.find_elements(By.CSS_SELECTOR, ".banner-image")
        assert len(elements) == 0, "The sign-up might have been successful when it shouldn't have been."

    def test_empty_password(self):
        self.navigate_to_register_page()
        self.fill_registration_form("Hello World", "example@example.com", "", "")
        self.submit_registration_form()
        elements = self.driver.find_elements(By.CSS_SELECTOR, ".banner-image")
        assert len(elements) == 0, "The sign-up might have been successful when it shouldn't have been."

    def test_invalid_email(self):
        self.navigate_to_register_page()
        self.fill_registration_form("hello", "hello", "123456", "123456")
        self.submit_registration_form()
        elements = self.driver.find_elements(By.CSS_SELECTOR, ".banner-image")
        assert len(elements) == 0, " The sign-up might have been successful when it shouldn't have been."


    def test_short_password(self):
        self.navigate_to_register_page()
        self.fill_registration_form("hello", "hello2@example.com", "123", "123")
        self.submit_registration_form()
        elements = self.driver.find_elements(By.CSS_SELECTOR, ".banner-image")
        assert len(elements) == 0, "The sign-up might have been successful when it shouldn't have been."
