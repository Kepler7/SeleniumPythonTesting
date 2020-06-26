from selenium.webdriver.common.by import By

from pageObjects.ConfirmationPage import ConfirmationPage
from utilities.BaseClass import BaseClass


class CheckoutPage(BaseClass):

    def __init__(self, driver):
        self.driver = driver
        self.verifyPresence(CheckoutPage.shopPage)

    iphonexLink = (By.CSS_SELECTOR, ".row .card-title")
    addToCartButton = (By.CSS_SELECTOR, "button[class='btn btn-info']")
    checkOutButton = (By.CSS_SELECTOR, "a[class*='btn-primary']")
    shopPage = (By.XPATH, "//h1[text()='Shop Name']")
    cardFooter = (By.CSS_SELECTOR, ".card-footer button")

    # button[class='btn btn-info']

    def getIphonexLink(self):
        return self.driver.find_element(*CheckoutPage.iphonexLink)

    def selectIphoneX(self):
        self.getIphonexLink().click()

    def getCardTitles(self):
        return self.driver.find_elements(*CheckoutPage.iphonexLink)

    def getAddToCartButtons(self):
        return self.driver.find_elements(*CheckoutPage.addToCartButton)

    def clickCheckoutButton(self):
        self.driver.find_element(*CheckoutPage.checkOutButton).click()
        return ConfirmationPage(self.driver)

    def getCardFooter(self):
        return self.driver.find_elements(*CheckoutPage.cardFooter)
