import inspect
import logging

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select

from config.ConfigReader import ReadConfig


@pytest.mark.usefixtures("setup")
class BaseClass:

    def get_settings_object(self):
        reader = ReadConfig()
        return reader.readConfigFile()

    def verifyLinkPresence(self, text):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, text)))

    def verifyPresence(self, by):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(by))

    def verify_text_in_locator(self, by, text):
        WebDriverWait(self.driver, 10).until(
            EC.text_to_be_present_in_element(by, text))

    def verify_text_in_element(self, element, text_to_compare):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of(element))
        assert text_to_compare in element.text

    def getLogger(self):
        """
        Initializes logs, pass path where your logfile will be saved
        :return: log instance
        """
        loggerName = inspect.stack()[1][3]
        logger = logging.getLogger(loggerName)
        # logger = logging.getLogger(__name__)

        fileHandler = logging.FileHandler('\\Users\\kepler.velasco\\Documents\\WorkspaceSelenium\\SeleniumPythonTesting\\utilities\\logfile.log')
        formatter = logging.Formatter("%(asctime)s :%(levelname)s : %(name)s : %(message)s")

        fileHandler.setFormatter(formatter)
        logger.addHandler(
            fileHandler)  # this will accept filehandler object in which you will put the path of logs file

        # so these below are the levels now we have to set the level and you will see from that level example:
        # if you set to error you will see error and critical logs

        logger.setLevel(logging.DEBUG)
        return logger
