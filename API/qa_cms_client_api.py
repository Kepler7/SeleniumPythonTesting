"""Main module."""
import requests


class QACmsClientAPI:

    def __init__(
        self, domain, client_id=None, client_secret=None, auth_token=None
    ):
        """ Initializes the instance with the given arguments.
        """
        self.domain = domain
        self.auth_token = auth_token
        self.client_id = client_id
        self.client_secret = client_secret

    def clean_domain(self):
        """ Removes the trailing forward slash from a domain if contained.
        """
        if not self.domain.endswith("/"):
            return self.domain
        return self.domain[:-1]

    def get_endpoint_url(self, endpoint):
        """ Given an endpoint returns the full endpoint for the
        set domain.
        """
        return f"{self.clean_domain()}{endpoint}"

    def get_headers(self):
        """ Return the required authorization headers
        """
        return {
            "Authorization": f"Bearer {self.auth_token}"
        }

    def get_semantic_search(self, bot_slug):
        """ Returns the object related to the semantic search configuration
        for a the given bot_slug
        """
        endpoint = f"/api/content/ci-semantic-search/{bot_slug}"
        response = requests.get(f"{self.get_endpoint_url(endpoint)}", headers=self.get_headers())
        #response = requests.get("https://cms-ci-global.yalochat.com/" + endpoint, headers=self.get_headers())
        breakpoint()
        return response.json()

    def set_token(
        self, client_id=None, client_secret=None,
        scope="squidex-api", auth_token=None
    ):
        """ Sets the instance auth_token,
        if not given, requests a new token with the given or already set,
        client_id and client_secret
        """
        if auth_token is None:
            client_id = client_id if client_id is not None else self.client_id
            if client_secret is None:
                client_secret = self.client_secret

            get_token_endpoint = "/identity-server/connect/token"
            data = {
                "grant_type": "client_credentials",
                "client_id": client_id,
                "client_secret": client_secret,
                "scope": scope
            }
            response = requests.post(
                f"{self.get_endpoint_url(get_token_endpoint)}",
                data=data
            ).json()
            auth_token = response["access_token"]
        self.auth_token = auth_token

    def get_questions_and_answers(self, cms_data):
        semantic_data = {}
        for semantic_data_item in cms_data["items"]:
            semantic_data[semantic_data_item["id"]] = {
                "question": semantic_data_item["data"]["title"]["iv"],
                "answer": semantic_data_item["data"]["content"]["iv"].replace(
                    "\\n", "\n"
                ).strip()
            }
        return semantic_data
