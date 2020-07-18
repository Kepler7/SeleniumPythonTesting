import time

import pytest

from API.QA_Botrunner_API_Client import QA_Botrunner_API_Client
from TestData import HomePageData
from pageObjects.waPageObjects.WhatsAppHome import WhatsAppHome
from utilities.BaseClass import BaseClass


class TestWa(BaseClass):

    def test_wabot(self):
        time.sleep(20)
