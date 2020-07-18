import pytest
from selenium import webdriver
import time

from API.QA_Botrunner_API_Client import QA_Botrunner_API_Client
from config.ConfigReader import ReadConfig

driver = None


def pytest_addoption(parser):
    parser.addoption(
        "--browser_name", action="store", default="chrome"
    )


@pytest.fixture(scope="class")
def setup(request):
    # data = HomePageData()
    reader = ReadConfig()
    settings = reader.readConfigFile()
    global driver
    browser_name = request.config.getoption("browser_name")
    if browser_name == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("user-data-dir={}".format(
            settings.chrome_profile_path))
        driver = webdriver.Chrome(options=options)  # IF YOU ARE ON WINDOWS you will have to pass executable_path="PATH"
    elif browser_name == "firefox":
        driver = webdriver.Firefox()
    elif browser_name == "ie":
        print("IE driver")
    # driver.get(data.wa_test_url["burgerKing"])
    driver.get(settings.bot_wa_url)
    driver.implicitly_wait(10)
    driver.find_element_by_xpath("//div[@id='side']/header//img").click()
    botrunner = QA_Botrunner_API_Client()
    botrunner.change_state(settings.user_id, settings.state, settings.bot_slug, settings.botrunner_auth_token)
    time.sleep(20)
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
