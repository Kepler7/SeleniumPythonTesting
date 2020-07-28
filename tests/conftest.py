import pytest
from selenium import webdriver
import time

from API.QA_Botrunner_API_Client import QA_Botrunner_API_Client
from config.ConfigReader import ReadConfig
from pageObjects.faPageObjects.Login_page import LoginPage
from pageObjects.waPageObjects.ConversationPage_wa import ConversationPage

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
    if settings.bot_type == "wa":
        driver.get(settings.bot)
        driver.implicitly_wait(10)
        driver.find_element_by_xpath("//div[@id='side']/header//img").click()
        conversation_page = ConversationPage(driver)
        conversation_page.send_keys_to_bar_message("INIT MESSAGE..")
        time.sleep(10)
    elif settings.bot_type == "fb":
        driver.get("https://m.me/{}".format(settings.bot))
        login = LoginPage(driver)
        login.login(settings.fb_user, settings.fb_password)
    botrunner = QA_Botrunner_API_Client()
    botrunner.change_state(settings.user_number, settings.state)
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



