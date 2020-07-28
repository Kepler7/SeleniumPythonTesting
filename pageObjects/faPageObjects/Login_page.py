import logging

from utilities.BaseClass import BaseClass
from selenium.webdriver.common.by import By


class LoginPage(BaseClass):

    def __init__(self, driver):
        self.driver = driver
        self.verifyPresence(LoginPage.USER_BOX)

    logging.basicConfig(level=logging.INFO)

    USER_BOX = (By.ID, "email")
    PASS_BOX = (By.ID, "pass")
    LOGIN_SUBMIT = (By.ID, "loginbutton")

    def get_username_box_element(self):
        return self.driver.find_element(*LoginPage.USER_BOX)

    def get_password_box_element(self):
        return self.driver.find_element(*LoginPage.PASS_BOX)

    def get_submit_button(self):
        return self.driver.find_element(*LoginPage.LOGIN_SUBMIT)

    def login(self, fb_user, fb_pass):
        user_box = self.get_username_box_element()
        pass_box = self.get_password_box_element()

        submit = self.get_submit_button()

        user_box.send_keys(fb_user)
        pass_box.send_keys(fb_pass)
        submit.click()
