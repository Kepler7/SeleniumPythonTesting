import pytest
from selenium import webdriver
import time

from TestData.HomePageData import HomePageData

driver = None


def pytest_addoption(parser):
    parser.addoption(
        "--browser_name", action="store", default="chrome"
    )


@pytest.fixture(scope="class")
def setup(request):
    data = HomePageData()
    global driver
    browser_name = request.config.getoption("browser_name")
    if browser_name == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("user-data-dir=C:\\Users\\deneb\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 2")
        driver = webdriver.Chrome(
            executable_path="C:\\Users\\deneb\\Desktop\\seleniumPython\\chromedriver_win32\\chromedriver.exe",
            chrome_options=options)
    elif browser_name == "firefox":
        driver = webdriver.Firefox(
            executable_path="C:\\Users\\deneb\\Desktop\\seleniumPython\\geckodriver-v0.25.0-win64\\geckodriver.exe")
    elif browser_name == "ie":
        print("IE driver")
    driver.get(data.wa_test_url["burgerKing"])
    driver.maximize_window()
    request.cls.driver = driver
    yield
    driver.close()
    driver.quit()


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    """
            Extends the PyTest Plugin to take and embed screenshot in html report, whenever test fails.
            :param item:
            """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            file_name = report.nodeid.replace("::", "_") + ".png"
            _capture_screenshot(file_name)
            if file_name:
                html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % file_name
                extra.append(pytest_html.extras.html(html))
        report.extra = extra


def _capture_screenshot(name):
    driver.get_screenshot_as_file(name)
