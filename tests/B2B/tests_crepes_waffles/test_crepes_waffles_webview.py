from pageObjects.waPageObjects.ConversationPage_wa import ConversationPage
from utilities.BaseClass import BaseClass
import random
import time


class TestWebviewCrepes(BaseClass):

    def test_go_to_webview_crepes_address_known(self):
        conversation_page = ConversationPage(self.driver)
        conversation_page.send_and_wait_for_n("Kepler", 1)
        conversation_page.send_and_wait_for_n("keph76@gmail.com", 2)
        conversation_page.send_and_wait_for_n("si", 2)
        conversation_page.send_and_wait_for_n("1", 1)
        option = random.randint(1, 2)
        conversation_page.send_and_wait_for_n(str(option), 2)
        conversation_page.send_and_wait_for_n("si", 1)
        conversation_page.click_to_webview_link()
        child_window = conversation_page.get_child_window()
        # this method will switch to webview
        web_view = conversation_page.access_to_webview(child_window)
        web_view.verify_correct_prices_in_products('crepes_waffles_webview.csv')