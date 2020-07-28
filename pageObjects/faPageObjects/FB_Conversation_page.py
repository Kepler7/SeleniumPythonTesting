from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import logging
import re

from utilities.BaseClass import BaseClass

logging.basicConfig(level=logging.INFO)


class ConversationPage_FB(BaseClass):

    def __init__(self, driver):
        self.driver = driver
        self.verifyPresence(ConversationPage_FB.TEXT_BOX)

    NEW_MSG_BUTTON = (By.XPATH, "//a[@title='New Message']")

    TEXT_BOX = (By.XPATH, '//div[@role="main"]//div[@role="combobox"][@aria-label]')

    INPUT_FIELD = (By.XPATH, "//input[@data-testid='photo_input']")

    BUBBLE_MSG = (By.XPATH, "//div[contains(@class, '_aok _7i2m')]")

    LAST_BUBBLE_MSG = (By.XPATH, '(//div[@aria-label])[last()-2]/span/span')

    def get_text_box(self):
        return self.driver.find_element(*ConversationPage_FB.TEXT_BOX)

    def send_message(self, text_to_be_sent):
        text_box = self.get_text_box()
        text_box.send_keys(text_to_be_sent)
        text_box.send_keys(Keys.RETURN)

    def type_message(self, text_to_be_sent, expected_num_msg):
        '''Type a message, this emulates a user typing through the box'''

        #  total_msgs is the sum of current msg ,
        #  the sent message and the expected reply msg
        total_msgs = len(
            self.get_all_msg_bubbles(self.driver)
        ) + expected_num_msg + 1

        self.send_message(text_to_be_sent)

        self.wait_for_n_messages(self.driver, total_msgs)
        logging.info(
            "\nSENDING MESSAGE:\n {} \n---------------\n".format(
                text_to_be_sent
            )
        )

    def retrieve_response_msg(self, text):
        '''Received messages are findable through the aria-label attr
        value will be the text of the message
        '''
        time.sleep(5)

        bubble_text = self.driver.find_element(
            By.XPATH,
            f"(//div[@aria-label='" + text + "'])[last()]"
        )
        logging.info("\nRECEIVED MESSAGE:\n {} \n---------------\n".format(
            bubble_text)
        )

        return bubble_text

    def retrieve_quick_reply_msg(self, text):
        '''Received messages are findable through the xpath through the text
        that is included
        '''
        quick_reply = self.driver.find_element(
            By.XPATH,
            f"//div[contains(text(), '" + text + "')]"
        )
        return quick_reply

    def retrieve_bubble_by_position(self, position):
        '''The last bubble message that contains a specific text
        '''
        locator_string = f"(//div[contains(@class, '_aok _7i2m')])"
        locator_string += f"[last()-" + str(position) + "]"
        bubble_text = self.driver.find_element(
            By.XPATH,
            locator_string
        ).text
        logging.info(
            "RECEIVED MESSAGE:\n {} \n---------------\n".format(bubble_text)
        )
        return bubble_text

    def get_all_msg_bubbles(self):
        '''Retrieves all the message bubbles that exist in the DOM,
        they can be found by the class name.
        '''
        msg_bubbles = self.driver.find_elements(*ConversationPage_FB.BUBBLE_MSG)
        return msg_bubbles

    def wait_for_n_messages(
            self, expected_n_messages, n_iterations=10, iteration_sleep_time=3
    ):
        for _ in range(n_iterations):
            try:
                msg_bubbles_retrieved = len(
                    self.get_all_msg_bubbles(self.driver)
                )
                if expected_n_messages == msg_bubbles_retrieved:
                    break
                else:
                    time.sleep(iteration_sleep_time)
            except Exception as e:
                print(e)
                time.sleep(iteration_sleep_time)
        else:
            wait_time = n_iterations * iteration_sleep_time
            err_message = f"Failed got {msg_bubbles_retrieved}"
            err_message += f" absolute messages in {wait_time} seconds when "
            err_message += f"{expected_n_messages} absolute messages"
            err_message += f" were expected"
            logging.info(err_message)
            raise TimeoutError(err_message)

    def get_option_sugg_list(self, search_text):

        try:
            bubble_msg = self.retrieve_bubble_by_position(self.driver, 0)
            time.sleep(2)
            retrieved_faq_match = re.search(
                r'.*' + search_text, bubble_msg, re.MULTILINE
            ).group()
            option_number = retrieved_faq_match[0]
            return option_number

        except Exception:
            err_message = f"\nExpected Text: {search_text} \n"
            err_message += f"Was NOT found in the \n"
            err_message += f"Retrieved Message:  {bubble_msg}"
            logging.info(err_message)
            raise AssertionError(err_message)

    def get_all_messages_elements(self):
        return self.driver.find_elements_by_xpath(
            "//div[@role='region']/div[2]//div[contains(@class, 'clearfix')] [contains(@class, 'text_align')]"
        )

    def send_and_wait_for_n(self, send_message_string, expected_n_messages, last_element=None):

        # Get last element if no reference to a last element is provided.
        if last_element is None:
            last_element = self.get_all_messages_elements()[-1]

        # Send message if a message is provided.
        if send_message_string is not None:
            self.send_message(send_message_string)

        for _ in range(20):
            convo_elements = self.get_all_messages_elements()
            if (len(convo_elements) - convo_elements.index(last_element) - 1) == (
                    expected_n_messages + (1 if send_message_string else 0)):
                break
            time.sleep(1)
        else:
            raise TimeoutError("TIMEOUT ERROR")

    def get_messages_texts(self, message_elements):
        return [text_element.text for text_element in message_elements]

    def get_quick_reply_elements(self):
        return self.get_quick_reply_container_element().find_elements_by_xpath(
            './/div[@role="button"]'
        )

    def get_quick_reply_container_element(self):
        return self.driver.find_element_by_xpath(
            '//div[@currentselectedindex]'
        )

    def find_quick_reply(self):
        pass

    def get_shift_left_button(self):
        return self.get_quick_reply_container_element().find_element_by_xpath("./a/div[@direction='backward']")

    def get_shift_right_button(self):
        return self.get_quick_reply_container_element().find_element_by_xpath("./a/div[@direction='forward']")

    def get_first_visible_element(self):
        for i, quick_reply_element in enumerate(self.get_quick_reply_elements()):
            if quick_reply_element.is_displayed():
                return i, quick_reply_element

    def display_quick_reply_element(self, quick_reply_element):
        visible_index, first_visible_element = self.get_first_visible_element()
        desired_quick_reply_index = self.get_quick_reply_elements().index(quick_reply_element)
        if desired_quick_reply_index > visible_index:
            shift_button_element = self.get_shift_right_button
        else:
            shift_button_element = self.get_shift_left_button
        while quick_reply_element.is_displayed() is False:
            shift_button_element().click()
            time.sleep(0.2)

    def get_quick_reply_elements_texts(self):
        quick_replies = self.get_quick_reply_elements()
        quick_reply_texts = []
        for i, quick_reply_element in enumerate(quick_replies):
            try:
                self.display_quick_reply_element(quick_reply_element)
            except Exception as exception:
                print(exception)
            time.sleep(0.2)
            quick_reply_texts.append(quick_reply_element.text)
        return quick_reply_texts

    def scroll_last_element_visible(self):
        quick_replies_element = self.get_quick_reply_container_element()
        messages_scrollable_area_element = self.driver.find_elements_by_xpath('//div[contains(@class,"uiScrollableAreaWrap")]')[-1]
        while quick_replies_element.is_displayed() is False:
            self.driver.execute_script("arguments[0].scrollBy(0,500)", messages_scrollable_area_element)

    def click_nth_quick_reply(self, nth_element):
        self.scroll_last_element_visible()
        quick_replies = self.get_quick_reply_elements()
        self.display_quick_reply_element(quick_replies[nth_element])
        quick_replies[nth_element].click()