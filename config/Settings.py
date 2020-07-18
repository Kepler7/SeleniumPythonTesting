class Settings:
    def __init__(
            self,
            bot_wa_url,
            chrome_profile_path,
            bot_slug,
            botrunner_auth_token,
            state,
            user_id,
            auth,
            content_type
    ):
        self.bot_wa_url = bot_wa_url
        self.chrome_profile_path = chrome_profile_path
        self.bot_slug = bot_slug
        self.botrunner_auth_token = botrunner_auth_token
        self.state = state
        self.user_id = user_id
        self.auth = auth
        self.content_type = content_type
