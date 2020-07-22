class Settings:
    def __init__(
            self,
            bot_wa_url,
            chrome_profile_path,
            bot_slug,
            botrunner_auth_token,
            state,
            user_number,
            auth,
            content_type,
            bot_type,
            faqs,
            cms_api,
            faqs_state_name,
            cms_bot_slug
            #test_dir
    ):
        self.bot_wa_url = bot_wa_url
        self.chrome_profile_path = chrome_profile_path
        self.bot_slug = bot_slug
        self.botrunner_auth_token = botrunner_auth_token
        self.state = state
        self.user_number = user_number
        self.auth = auth
        self.content_type = content_type
        self.bot_type = bot_type
        self.faqs = faqs
        self.cms_api = cms_api
        self.faqs_state_name = faqs_state_name
        self.cms_bot_slug = cms_bot_slug
        #self.test_dir = test_dir