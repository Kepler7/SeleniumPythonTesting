import requests
import json
import jsonpath

from utilities.BaseClass import BaseClass


class QA_Botrunner_API_Client(BaseClass):

    def change_state(self, user_id, state_name):
        """ Given a `user_id` and a `state_name`,
        sets the chatbot state to the value contained in `state_name`
        for the given user `user_id`.
        """
        baseurl = "https://api-global.yalochat.com/botrunner/"
        setter = self.get_settings_object()

        return requests.post(
            baseurl + f"{setter.bot_slug}/send-to",
            params={"token": setter.botrunner_auth_token},
            json={
                "userId": user_id,
                "state": state_name
            }
        )

    def get_client_id(self, bot_slug, phone, auth, content_type):
        """
        :return: Client id of a registered client, This method has
        been tested with panda with some other it could vary
        """
        baseurl = "http://api-staging2.yalochat.com/big-storage-ng/api/store/"

        response = requests.get(
            baseurl + f"{bot_slug}/clients/code/identifier/" + f"{phone}",
            headers={
                'authorization': auth,
                'content-type': content_type
            }
        )
        json_response = json.loads(response.text)
        client = jsonpath.jsonpath(json_response, '_id')
        client_id = client[0]
        return client_id

    def delete_registered_client(self, bot_slug, phone, auth, content_type):
        baseurl = "https://api-global.yalochat.com/big-storage-ng/api/store/"

        client_id = self.get_client_id(bot_slug, phone, auth, content_type)
        response = requests.delete(baseurl + f"{bot_slug}/clients/{client_id}",
                        headers={
                            'authorization': auth,
                            'content-type': content_type
                        })
        json_response = json.loads(response.text)
