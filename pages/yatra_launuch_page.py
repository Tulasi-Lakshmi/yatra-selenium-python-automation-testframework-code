import logging
import time
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from base.base_driver import BaseDriver
from pages.search_flights_results_page import SearchFlightResults
from utilities.utils import Utils


class LaunchPage(BaseDriver):
    log = Utils.custom_logger()
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # Locator externalizing
    DEPART_FROM_FIELD= "//input[@id='BE_flight_origin_city']"
    GOING_TO_FIELD = "//input[@id='BE_flight_arrival_city']"
    GOING_TO_RESULTS_LIST = "//div[@class='viewport']//div//div/li"
    SELECT_DATE_FIELD = "//input[@id='BE_flight_origin_date']"
    ALL_DATES = "//div[@id='monthWrapper']//div[@class='day-container']//tbody//td[@class!='inActiveTD weekend']"
    SEARCH_BUTTON = "//input[@value = 'Search Flights']"

    # FINDING THE ELEMENT AT DEPART_FROM_FIELD
    def getDepartFromField(self):
        return self.wait_element_to_be_clickable(By.XPATH, self.DEPART_FROM_FIELD)
        time.sleep(2)
    # FINDING THE ELEMENT AT GOING_TO_FIELD
    def getGoingToField(self):
        return self.wait_element_to_be_clickable(By.XPATH, self.GOING_TO_FIELD)

    def getGoingToResults(self):
        return self.wait_for_pressence_of_all_elements(By.XPATH, self.GOING_TO_RESULTS_LIST)

    def getDepartDateField(self):
        return self.wait_element_to_be_clickable(By.XPATH,self.SELECT_DATE_FIELD)

    def getAllDatesField(self):
        return self.wait_element_to_be_clickable(By.XPATH,self.ALL_DATES)

    def getSearchButton(self):
        return self.driver.find_element(By.XPATH,self.SEARCH_BUTTON)

        # Actions on Depart from location
    def enterDepartFromLocation(self, departlocation):
        self.getDepartFromField().click()
        self.getDepartFromField().send_keys(departlocation)
        time.sleep(2)
        self.getDepartFromField().send_keys(Keys.ENTER)

    def enterGoingToLocation(self, goinglocation):
        self.getGoingToField().click()
        self.log.info("click on going to location")
        self.log.error("this is error")
        time.sleep(2)
        self.getGoingToField().send_keys(goinglocation)
        time.sleep(3)
        self.log.info("Typed text into going to field successfully")
        search_results = self.getGoingToResults()
        time.sleep(4)
    # Selecting going to location from list of going names
        for results in search_results:
            if goinglocation in results.text:
                results.click()
                break

    def enterDepartFromDate(self, depadate):
        self.getDepartDateField().click()
        all_dates = self.getAllDatesField().find_elements(By.XPATH, self.ALL_DATES)
    # Selecting Departure date
        for dates in all_dates:
            if dates.get_attribute("data-date") == depadate:
                dates.click()
                break

    def clickSearchFlightButton(self):
        self.getSearchButton().click()
        time.sleep(2)

    def searchFlights(self, departlocation, goinglocation, depadate):
        self.enterDepartFromLocation(departlocation)
        self.enterGoingToLocation(goinglocation)
        self.enterDepartFromDate(depadate)
        self.clickSearchFlightButton()
        search_flights_result = SearchFlightResults(self.driver)
        return search_flights_result