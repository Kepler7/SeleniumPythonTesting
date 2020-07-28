class Settings:
    def __init__(
            self,
            bot,
            chrome_profile_path,
            bot_slug,
            botrunner_auth_token,
            state,
            user_number,
            auth,
            content_type,
            bot_type,
            faqs,
            faqs_state_name,
            cms_bot_slug,
            fb_user,
            fb_password,
            fb_bot_number
            #test_dir
    ):
        self.bot = bot
        self.chrome_profile_path = chrome_profile_path
        self.bot_slug = bot_slug
        self.botrunner_auth_token = botrunner_auth_token
        self.state = state
        self.user_number = user_number
        self.auth = auth
        self.content_type = content_type
        self.bot_type = bot_type
        self.faqs = faqs
        self.faqs_state_name = faqs_state_name
        self.cms_bot_slug = cms_bot_slug
        self.fb_user = fb_user
        self.fb_password = fb_password
        self.fb_bot_number = fb_bot_number
        #self.test_dir = test_dir