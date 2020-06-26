from selenium.webdriver.common.by import By

from pageObjects.ProtoCommercePage import ProtoCommercePage
from utilities.BaseClass import BaseClass


class ConfirmationPage(BaseClass):

    def __init__(self, driver):
        self.driver = driver

    checkoutButtonSuccess = (By.CSS_SELECTOR, "button[class*='btn-success']")
    buttons = (By.CSS_SELECTOR, "button[type='button']")

    def clickCheckoutButtonSuccess(self):
        for button in self.getButtons():
            if button.text == "Checkout":
                button.click()

    def getButtons(self):
        return self.driver.find_elements(*ConfirmationPage.buttons)

    #need maintenance
    def clickCheckoutButton(self):
        self.clickElement(*ConfirmationPage.checkoutButtonSuccess)