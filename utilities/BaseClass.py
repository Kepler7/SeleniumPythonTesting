import inspect
import logging

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select


@pytest.mark.usefixtures("setup")
class BaseClass:

    def verifyLinkPresence(self, text):
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, text)))

    def verifyPresence(self, by):
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(by))

    def getElement(self, by):
        return self.driver.find_element(by)

    def clickElement(self, by):
        try:
            if self.driver.find_elements(by).size == 1:
                self.getElement(by).click()
        except Exception as e:
            print(e)

    def sendKeysTo(self, by, keys):
        self.getElement(by).send_keys(keys)

    def selectOptionByText(self, locator, text):
        sel = Select(locator)
        sel.select_by_visible_text(text)

    def getLogger(self):
        loggerName = inspect.stack()[1][3]
        logger = logging.getLogger(loggerName)
        #logger = logging.getLogger(__name__)

        fileHandler = logging.FileHandler('C:\\Users\\deneb\\PycharmProjects\\PythonSeleniumFramework\\utilities\\logfile.log')
        formatter = logging.Formatter("%(asctime)s :%(levelname)s : %(name)s : %(message)s")

        fileHandler.setFormatter(formatter)
        logger.addHandler(fileHandler)  # this will accept filehandler object in which you will put the path of logs file

        # so these below are the levels now we have to set the level and you will see from that level example:
        # if you set to error you will see error and critical logs

        logger.setLevel(logging.DEBUG)
        return logger
