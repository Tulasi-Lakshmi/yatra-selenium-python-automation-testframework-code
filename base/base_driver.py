import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class BaseDriver:
    def __init__(self,driver):
        self.driver = driver

    # To handle dynamic scroll
    def page_scroll(self):
        pageLength = self.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var pageLength = document.body.scrollHeight;return pageLength;")
        match = False
        while (match == False):
            lastCount = pageLength
            time.sleep(2)
            lenOfPage = self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);var pageLength = document.body.scrollHeight;return pageLength;")
            if lastCount == pageLength:
                match = True
        time.sleep(3)

    def wait_for_pressence_of_all_elements(self,locater_type,locater):
        wait = WebDriverWait(self.driver, 10)
        list_of_elements = wait.until(EC.presence_of_all_elements_located((locater_type,locater)))
        return list_of_elements

    def wait_element_to_be_clickable(self,locater_type,locater):
        wait = WebDriverWait(self.driver, 15)
        depart = wait.until(EC.element_to_be_clickable((locater_type, locater)))
        return depart

    def wait_visibility_of_all_elements_located(self,locater_type,locater):
        wait = WebDriverWait(self.driver, 10)
        search_res = wait.until(EC.visibility_of_all_elements_located((locater_type,locater)))
        return search_res
