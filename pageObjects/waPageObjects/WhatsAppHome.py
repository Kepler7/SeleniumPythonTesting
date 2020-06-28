from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from utilities.BaseClass import BaseClass


class WhatsAppHome(BaseClass):

    def __init__(self, driver):
        self.driver = driver
        self.verifyPresence(WhatsAppHome.textInMiddle)

    continueToChatButton = (By.CSS_SELECTOR, "a#action-button")
    textInMiddle = (By.CSS_SELECTOR, "h1._2yzk")
    useWhatsappWeb = (By.PARTIAL_LINK_TEXT, "Web")

    def clickContinueToChat(self):
        self.driver.find_element(
            *WhatsAppHome.continueToChatButton
        ).send_keys(Keys.ENTER)

    def clickUseWeb(self):
        self.verifyPresence(WhatsAppHome.useWhatsappWeb)
        self.driver.find_element(
            *WhatsAppHome.useWhatsappWeb
        ).send_keys(Keys.ENTER)
