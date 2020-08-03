import time

from pageObjects.waPageObjects.ConversationPage_wa import ConversationPage
from utilities.BaseClass import BaseClass


class TestwebviewPanda(BaseClass):

    def test_register_data(self):
        setter = self.get_settings_object()
        conversation_page = ConversationPage(self.driver)
        elements = conversation_page.get_messages_elements()
        if "nombre completo" not in elements[-1].text:
            conversation_page.delete_client(setter.bot_slug, setter.user_id, setter.auth, setter.content_type)
            conversation_page.send_to(setter.user_id, setter.state, setter.bot_slug, setter.botrunner_auth_token)
        self.verify_text_in_element(elements[-1], "nombre completo")
        conversation_page.send_keys_to_bar_message("kepler")
        time.sleep(20)

    def test_flow_to_webview_registered_user(self):
        conversation_page = ConversationPage(self.driver)
        conversation_page.send_keys_and_wait_n_number_messages("1", 2, "( sí / no )")
        conversation_page.send_keys_and_wait_n_number_messages("si", 1, "Entra al siguiente enlace")
        conversation_page.access_to_webview()