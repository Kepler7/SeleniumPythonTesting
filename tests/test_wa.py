import time

import pytest

from TestData import HomePageData
from pageObjects.waPageObjects.WhatsAppHome import WhatsAppHome
from utilities.BaseClass import BaseClass


class TestWa(BaseClass):

    def test_wabot(self):
        home = WhatsAppHome(self.driver)
        home.clickContinueToChat()
        home.clickUseWeb()
        time.sleep(20)
