from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By


class WebDriverExtensions():
    @staticmethod
    def WaitOnElement(wait: WebDriverWait, by: By, selector) -> WebElement:
        return wait.until(ec.visibility_of_element_located((by, selector)))

    @staticmethod
    def WaitOnElements(wait: WebDriverWait, by, selector) -> list[WebElement]:
        return wait.until(ec.visibility_of_all_elements_located((by, selector)))

    @staticmethod
    def WaitOnElement2(wait: WebDriverWait, by, selector):
        return wait.until(ec.visibility_of_element_located((by, selector)))
