import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope="function")
def driver():
    options = Options()
    if os.getenv("CI", "false").lower() == "true":
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(0)
    driver.set_window_size(1920, 1080)
    yield driver
    driver.quit()
