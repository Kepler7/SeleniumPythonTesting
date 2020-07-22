from pageObjects.waPageObjects.ConversationPage_wa import ConversationPage
from utilities.BaseClass import BaseClass
import time


class TestWebviewBodega(BaseClass):

    def test_go_to_webview_aurrera(self):
        #setter = self.get_settings_object()
        conversation_page = ConversationPage(self.driver)
        conversation_page.send_and_wait_for_n("¡Hola!, Quiero hacer un pedido de \"Despensa A Tu Casa\"!", 3)
        conversation_page.send_and_wait_for_n("kepler", 2)
        conversation_page.send_and_wait_for_n("keph76@gmail.com", 2)
        conversation_page.click_to_webview_link()
        child_window = conversation_page.get_child_window()
        # this method will switch to webview
        web_view = conversation_page.access_to_webview(child_window)
        web_view.verify_correct_prices_in_products('ArticulosTop_Webview_new.csv')
        time.sleep(10)