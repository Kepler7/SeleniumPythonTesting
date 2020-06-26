import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from TestData.HomePageData import HomePageData
from pageObjects.HomePage import HomePage
from utilities.BaseClass import BaseClass


class TestHomePage(BaseClass):

    @pytest.mark.usefixtures("getData")
    def test_formSubmission(self, getData):
        log = self.getLogger()
        homePage = HomePage(self.driver)
        #homePage.getNameField().send_keys(self.getData[0])#with tuple
        homePage.getNameField().send_keys(getData["firstName"])# with dictionary
        log.info("Entering name " + getData["firstName"])
        homePage.getEmail().send_keys(getData["email"])
        log.info("Entering email " + getData["email"])
        homePage.getCheckBox().click()
        log.info("Checkbox clicked")
        self.selectOptionByText(homePage.getGender(), getData["gender"])
        log.info("Select gender " + getData["gender"])
        homePage.submitForm().click()
        log.info("Submit form")

        alertText = homePage.getSuccessMessage().text
        log.info("Getting the alert " + alertText)

        assert ("Success" in alertText)
        self.driver.refresh()
        log.info("Refreshed form")

    # @pytest.fixture(params=[("kepler", "Velasco", "Male"), ("Deneb", "Solano", "Female")])
    # you can also pass dictionary as parameter
    #@pytest.fixture(params=[{"firstName": "Kepler", "lastName": "Velasco", "email": "keph76@gmail.com", "gender": "Male"}])
    #however data above will go to a separate file
    #@pytest.fixture(params=HomePageData.test_homePage_data)# this is to use the dict directly
    #def getData(self, request):
        #return request.param

    @pytest.fixture(params=HomePageData.getTestData("Testcase2"))# this is for used dictionary created with data from excel
    def getData(self, request):
        return request.param