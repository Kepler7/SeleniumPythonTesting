import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from API.QA_Botrunner_API_Client import QA_Botrunner_API_Client
from utilities.BaseClass import BaseClass


class ConversationPage(BaseClass):

    def __init__(self, driver):
        self.driver = driver
        self.verifyPresence(ConversationPage.messageBarInput)

    messageBarInput = (By.XPATH, "//footer//div[@contenteditable]")
    send_button = (By.CSS_SELECTOR, "footer span[data-icon='send']")
    link_to_webview = (By.CSS_SELECTOR, "a[href*='https://ecommerce-qsr.yalochat.com']")

    def send_keys_to_bar_message(self, text_send):
        self.driver.find_element(*ConversationPage.messageBarInput).send_keys(text_send)

    def send_keys_and_wait_n_number_messages(self, text_send, n, expected_message):
        messages_after = []
        messages = self.get_messages_texts()
        current_quantity = len(messages) + 1
        self.send_keys_to_bar_message(text_send)
        self.click_send_button()
        for quantity in range(10):
            messages_after = self.get_messages_texts()
            if len(messages_after) < current_quantity + n:
                time.sleep(2)
        assert len(messages_after) == current_quantity + n
        assert expected_message in messages_after[-1]

    def click_send_button(self):
        self.driver.find_element(*ConversationPage.send_button).click()

    def get_messages_texts(self):
        """
        :returns a list of string with messages
        """
        currentMessage = []
        for message in self.get_messages_elements():
            currentMessage.append(message.find_element_by_xpath(".//div[@class='copyable-text']").text)
        return currentMessage

    def get_messages_elements(self):
        """
        :returns a list of webElements where the message are
        """
        return self.driver.find_elements_by_xpath("//div[@id='main']//div[@data-id]")

    def delete_client(self, bot_slug, phone, auth, content_type):
        """

        :return:
        """
        botrunner = QA_Botrunner_API_Client()
        botrunner.delete_registered_client(bot_slug, phone, auth, content_type)

    def send_to(self, user_id, state_name, bot_slug, botrunner_auth_token):
        """

        :return:
        """
        botrunner = QA_Botrunner_API_Client()
        breakpoint()
        botrunner.change_state(user_id, state_name, bot_slug, botrunner_auth_token)

    def get_webviews_links(self):
        return self.driver.find_elements(*ConversationPage.link_to_webview)

    def access_to_webview(self):
        links_to_webview = self.get_webviews_links()
        current_link = links_to_webview[-1]
        current_link.click()
