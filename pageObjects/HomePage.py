from selenium.webdriver.common.by import By

from pageObjects.CheckoutPage import CheckoutPage
from utilities.BaseClass import BaseClass


class HomePage(BaseClass):

    def __init__(self, driver):
        self.driver = driver

    shop = (By.CSS_SELECTOR, "a[href*='shop']")
    name = (By.CSS_SELECTOR, "label + [name='name']")
    email = (By.NAME, "email")
    check = (By.ID, "exampleCheck1")
    gender = (By.ID, "exampleFormControlSelect1")
    submit = (By.XPATH, "//input[@value='Submit']")
    successMessage = (By.CSS_SELECTOR, "[class*='alert-success']")

    def getShopItem(self):
        return self.driver.find_element(*HomePage.shop)

    def clickShop(self):
        self.getShopItem().click()
        return CheckoutPage(self.driver)

    def getNameField(self):
        return self.driver.find_element(*HomePage.name)
        # return self.driver.find_element(*HomePage.name)

    def sendKeysToEmail(self, keys):
        self.sendKeysTo(*HomePage.email, keys)

    def getCheckBox(self):
        return self.driver.find_element(*HomePage.check)

    def getGender(self):
        return self.driver.find_element(*HomePage.gender)

    def submitForm(self):
        return self.driver.find_element(*HomePage.submit)

    def getSuccessMessage(self):
        return self.driver.find_element(*HomePage.successMessage)

    def getEmail(self):
        return self.driver.find_element(*HomePage.email)
