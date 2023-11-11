import os
import time
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager


@pytest.fixture(scope='class', autouse=True)
def setup(request, browser, url):
    global driver
    chr_options = Options()
    chr_options.add_experimental_option("detach", True)
    if browser == "chrome":
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chr_options)
    elif browser == "firefox":
        driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()),options=chr_options)
    elif browser == "edge":
        driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()),options=chr_options)
    
    driver.get(url)
    driver.maximize_window()
    request.cls.driver = driver
    yield
    driver.quit()


def pytest_addoption(parser):
    parser.addoption("--browser", default="chrome")
    parser.addoption("--url", default="http:/www.yatra.com")


# 'browser' fixture to specify the browser type
@pytest.fixture(scope="session", autouse=True)
def browser(request):
    return request.config.getoption("--browser")


# 'url' fixture to specify the URL
@pytest.fixture(scope="session", autouse=True)
def url(request):
    return request.config.getoption("--url")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extras = getattr(report, "extra", [])
    if report.when == "call" or report.when == "setup":
        xfail = hasattr(report, "wasxfail")
        # always add url to report
        if (report.skipped and xfail) or (report.failed and not xfail):
            # report_dir = os.path.dirname(item.config.option.htmlpath)
            file_name1 = report.nodeid.replace("::", "_") + ".png"
            # destinationFile = os.path.join(report_dir, file_name1)
            # **********
            report_dir = "C:\\pythonselenium\\TestFrameworkDemo\\screenshots\\"
            # file_name1 = str(int(round(time.time() * 1000))) + ".png"
            _capture_screenshot(file_name1)
            if file_name1:
                # only add additional html on failure
                # html = '<div><img src="%s" alt="screenshot" style="width:100px;height:128px;" ' \
                #        'onclick="window.open(this.src)" align="centre"/></div>' %file_name1
                extras.append(pytest_html.extras.png(file_name1))
        report.extras = extras


def _capture_screenshot(name):
   driver.get_screenshot_as_file(name)


def pytest_html_report_title(report):
    report.title = "Automation Test Report"





