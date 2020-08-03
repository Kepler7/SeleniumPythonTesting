import os
from datetime import datetime
import pytest

from API.QA_Botrunner_API_Client import QA_Botrunner_API_Client
from API.qa_cms_client_api import QACmsClientAPI
from pageObjects.faPageObjects.FB_Conversation_page import ConversationPage_FB
from pageObjects.waPageObjects.ConversationPage_wa import ConversationPage
from utilities.BaseClass import BaseClass
from utilities.faqs_utilities import wa_faqs_semantic_search, fb_faqs_semantic_search, write_results


class TestFaqs(BaseClass):

    @pytest.mark.usefixtures("getData")
    def test_faqs(self, getData):
        cms_api = QACmsClientAPI(getData['domain'],
                                 getData['client_id'],
                                 getData['client_secret'])
        cms_api.set_token()
        botrunner_api = QA_Botrunner_API_Client()
        setter = self.get_settings_object()
        time_now = str(datetime.now())
        faqs_dir = os.path.join("test_" + time_now, "_FAQS")
        if setter.bot_type == "wa" and setter.faqs == "semantic_search":
            page = ConversationPage(self.driver)
            results = wa_faqs_semantic_search(
                cms_api,
                setter.cms_bot_slug,
                botrunner_api,
                setter.user_number,
                setter.faqs_state_name,
                page,
                faqs_dir
            )
        elif setter.bot_type == "fb" and setter.faqs == "semantic_search":
            page = ConversationPage_FB(self.driver)
            results = fb_faqs_semantic_search(
                cms_api,
                setter.cms_bot_slug,
                botrunner_api,
                setter.user_number,
                setter.faqs_state_name,
                page,
                faqs_dir
            )
        else:
            raise Exception("FAQ type configuration not supported")
        write_results(os.path.join(faqs_dir, "results.csv"), results.values())
        assert all([(result["result_code"] == 1 or result["result_code"] == 2) for result in results.values()])

    @pytest.fixture(
    params=[{"domain": "https://cms-ci-global.yalochat.com/",
             "client_id": "ci-semantic-search:ci-semantic-search-qa",
             "client_secret": "NFzA0W2VniGzJl8PEQXmn8rgzBN/5xUX8UkOIVH5jFc=",
             "staging_domain": "https://cms-staging2.yalochat.com/",
             "staging_client_id": "ci-semantic-search:ci-semantic-search-qa",
             "staging_clint_secret": "wko9jqy2hr0i9udqr0yo9g6hlokrifzgauephijespcx"}
            ])
    def getData(self, request):
        """
        getting data for cms_api
        :param request: domain, client_id, client_secret
        :return: data used to initialize QACmsClientAPI object
        """
        return request.param

