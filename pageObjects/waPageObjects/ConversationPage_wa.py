import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from API.QA_Botrunner_API_Client import QA_Botrunner_API_Client
from pageObjects.waPageObjects.Webview_ProductsPage import Webview_ProductsPage
from utilities.BaseClass import BaseClass


class ConversationPage(BaseClass):

    def __init__(self, driver):
        self.driver = driver
        self.verifyPresence(ConversationPage.messageBarInput)

    messageBarInput = (By.XPATH, "//footer//div[@contenteditable]")
    send_button = (By.CSS_SELECTOR, "footer span[data-icon='send']")
    link_to_webview = (By.CSS_SELECTOR, "a[href*='yalo']")
    XPATH_PANE_CONVO_ALL = (By.XPATH, "//div[@id='main']//div[@data-id]")
    XPATH_PANE_TYPE_MESSAGE_BAR = (By.XPATH, "//footer//div[@contenteditable]")
    XPATH_PANE_SEND_MESSAGE_BUTTON = (By.XPATH, "//footer//span[@data-icon='send']")

    def send_keys_to_bar_message(self, text_send):
        self.driver.find_element(*ConversationPage.messageBarInput).send_keys(text_send)
        self.click_send_button()

    def get_type_message_bar(self):
        return self.driver.find_element(
            *ConversationPage.XPATH_PANE_TYPE_MESSAGE_BAR
        )

    def get_send_message_button(self):
        return self.driver.find_element(*ConversationPage.XPATH_PANE_SEND_MESSAGE_BUTTON)

    def send_keys_and_wait_n_number_messages(self, text_send, n, expected_message):
        """
        ************IN MAINTENANCE**************
        :sends a message to whatsapp and verify n number of messages as response
        and also verifies for an expected messages or words.
        """
        messages_after = []
        messages = self.get_messages_texts()
        current_quantity = len(messages) + 1
        self.send_keys_to_bar_message(text_send)
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
            currentMessage.append(message.find_element_by_css_selector("div[class*='copyable-text']").text)
        return currentMessage

    def get_messages_texts_faqs(self, messages):
        """
        This get messages tesxt is the one that has to be used in the FAQ's testing
        :returns a list of string with messages
        """
        currentMessage = []
        for message in messages:
            currentMessage.append(message.find_element_by_css_selector("div[class*='copyable-text']").text)
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

    def click_to_webview_link(self):
        links_to_webview = self.get_webviews_links()
        current_link = links_to_webview[-1]
        current_link.click()

    def send_and_wait_for_n(
        self, message, n_messages, loops=30, loop_sleep=0.5, force_sleep=None,
        last_element=None
    ):
        if last_element is None:
            prev_messages = self.get_all_messages_elements()
            if len(self.get_all_messages_elements()) > 0:
                last_element = prev_messages[-1]
            else:
                last_element = None

        if message:
            self.send_message(message)

        if force_sleep:
            time.sleep(force_sleep)
            return

        for _ in range(loops):
            messages = self.get_all_messages_elements()
            if last_element is not None:
                index = messages.index(last_element)
                lenght = len(messages) - (
                    (index + 1) + (1 if message else 0)
                )
            else:
                lenght = len(messages)
            if lenght == n_messages:
                break
            time.sleep(loop_sleep)
        else:
            raise TimeoutError()

    def get_all_messages_elements(self):
        return self.driver.find_elements(*ConversationPage.XPATH_PANE_CONVO_ALL)

    def send_message(self, message, try_n_times=10):
        message_bar = self.get_type_message_bar()
        message_bar.click()

        # Try to place the message in the text area
        #  `try_n_times` times, raise an exception
        #  if the placed text never matches the
        #  expected message content.
        for _ in range(try_n_times):
            self.write_message(message)
            if message_bar.text == str(message):
                break
            self.clear_message()
        else:
            raise Exception(
                "Tried using message: {} as input {} times and failed.".format(
                    message, try_n_times
                )
            )
        self.get_send_message_button().click()

    def write_message(self, message):
        message_bar = self.get_type_message_bar()
        message_bar.click()
        message_bar.send_keys(message)

    def clear_message(self):
        message_bar = self.get_type_message_bar()
        message_bar.clear()

    def get_child_window(self):
        return self.driver.window_handles[1]

    def switch_to_window(self, window_id):
        self.driver.switch_to.window(window_id)

    def access_to_webview(self, window_id):
        """
        :return: this method will access to product page in webview
        """
        self.switch_to_window(window_id)
        return Webview_ProductsPage(self.driver)

