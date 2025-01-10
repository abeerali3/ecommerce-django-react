import pytest 
from selenium.webdriver.edge.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
options = Options()
options.add_argument('--headless')  # Enable headless mode for CI
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Edge(options=options)

@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Edge(options=options)
    driver.set_window_size(1552, 832)
    yield driver
    driver.quit()

def login(driver, email="", password=""):
    driver.get("http://127.0.0.1:8000/")
    driver.find_element(By.CSS_SELECTOR, ".nav-link:nth-child(2)").click()
    if email:
        driver.find_element(By.ID, "email").send_keys(email)
    if password:
        driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, ".mt-3").click()

def test_login_empty_email(driver):
    login(driver, password="123456")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "email"))
    )
    elements = driver.find_elements(By.ID, "email")
    assert len(elements) > 0

def test_login_empty_password(driver):
    login(driver, email="hello@world.com")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".alert"))
    )
    elements = driver.find_elements(By.CSS_SELECTOR, ".alert")
    assert len(elements) > 0

def test_login_success(driver):
    login(driver, email="hello@world.com", password="helloworld")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".banner-image"))
    )
    elements = driver.find_elements(By.CSS_SELECTOR, ".banner-image")
    assert len(elements) > 0

def test_incorrect_login(driver):
    login(driver, email="incorrect@email.com", password="123456")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".alert"))
    )
    elements = driver.find_elements(By.CSS_SELECTOR, ".alert")
    assert len(elements) > 0

def test_wrong_password(driver):
    login(driver, email="hello@world.com", password="1234")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".alert"))
    )
    elements = driver.find_elements(By.CSS_SELECTOR, ".alert")
    assert len(elements) > 0
