"""File > Settings > Project: YourProjectName > Python Interpreter.
Make sure it matches the Python environment you are using in the command prompt."""
import time
import pytest
import softest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.yatra_launuch_page import LaunchPage
from pages.search_flights_results_page import SearchFlightResults
from utilities.utils import Utils
from ddt import data, ddt, file_data, unpack


@pytest.mark.usefixtures("setup")
@ddt
class TestSearchAndVerifyFilter(softest.TestCase):
    log = Utils.custom_logger()
    @pytest.fixture(scope="class", autouse=True)
    def class_setup(self, setup):
        self.lp = LaunchPage(self.driver)
        self.ut = Utils()
    # @data(("New Delhi", "New York", "20/10/2023", "1 Stop"), ("Bom", "New York", "20/10/2023", "2 Stop"))
    # @unpack
    # @file_data("C:\\pythonselenium\\TestFrameworkDemo\\testdata\\testdata.json")
    #@file_data("C:\\pythonselenium\\TestFrameworkDemo\\testdata\\testyml.yaml")
    # @data(*Utils.read_data_from_excel("C:\\pythonselenium\\TestFrameworkDemo\\testdata\\tdataexcel.xlsx", "Sheet1"))
    @data(*Utils.read_data_from_csv("C:\\pythonselenium\\TestFrameworkDemo\\testdata\\tdatacsv1.csv"))
    @unpack
    def test_search_flights_1_stop(self, goingfrom, goingto, date, stops):
        search_flight_results = self.lp.searchFlights(goingfrom, goingto, date)
        self.lp.page_scroll()
        search_flight_results.filter_flights_by_stop(stops)
        allstops1 = search_flight_results.get_search_flights_results()
        self.log.info(len(allstops1))
        self.ut.assertListItemText(allstops1,stops)





