from typing import Self

import allure
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from src.web.selenium.core.waits import BySelector, SelectorOrElement, Wait


class BasePage:
    def __init__(self, driver: WebDriver, timeout: int = 10):
        self.driver = driver
        self.wait = Wait(driver, timeout)

    @allure.step
    def open(self, url: str) -> Self:
        self.driver.get(url)
        return self

    @allure.step
    def refresh(self) -> Self:
        self.driver.refresh()
        return self

    @allure.step
    def find(self, locator: BySelector) -> WebElement:
        return self.driver.find_element(*locator)

    @allure.step
    def find_all(self, locator: BySelector) -> list[WebElement]:
        return self.driver.find_elements(*locator)

    @allure.step
    def find_visible(self, locator: BySelector) -> WebElement:
        return self.wait.for_visible(locator)

    @allure.step
    def find_clickable(self, locator: BySelector) -> WebElement:
        return self.wait.for_clickable(locator)

    @allure.step
    def click(self, target: SelectorOrElement) -> Self:
        self.wait.for_clickable(target).click()
        return self

    @allure.step
    def type_text(self, target: SelectorOrElement, text: str, clear: bool = True) -> Self:
        element = self.wait.for_visible(target)
        if clear:
            element.clear()
        element.send_keys(text)
        return self

    @allure.step
    def get_text(self, target: SelectorOrElement) -> str:
        return self.wait.for_visible(target).text

    @allure.step
    def get_attribute(self, target: SelectorOrElement, attribute: str) -> str | None:
        element = self.wait.for_visible(target)
        return element.get_attribute(attribute)

    @allure.step
    def is_displayed(self, target: SelectorOrElement) -> bool:
        try:
            if isinstance(target, tuple):
                return self.driver.find_element(*target).is_displayed()
            return target.is_displayed()
        except Exception:
            return False

    @allure.step
    def is_enabled(self, target: SelectorOrElement) -> bool:
        try:
            if isinstance(target, tuple):
                return self.driver.find_element(*target).is_enabled()
            return target.is_enabled()
        except Exception:
            return False

    @allure.step
    def take_screenshot(self, path: str) -> Self:
        self.driver.save_screenshot(path)
        return self
