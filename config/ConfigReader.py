from configparser import ConfigParser

from config.Settings import Settings


class ReadConfig:

    def readConfigFile(self):
        file = '/Users/kepler.velasco/Documents/WorkspaceSelenium/SeleniumPythonTesting/config/config.ini'
        config = ConfigParser()
        config.read(file)
        return Settings(config.get('CURRENT-BOT', 'Current_bot'),
                        config.get('CHROME-PROFILE-PATH', 'ProfilePath'),
                        config.get('CURRENT-BOT-SLUG', 'Current_bot_slug'),
                        config.get('botrunner_auth_token', 'botrunner_auth_token'),
                        config.get('CURRENT_RESTART_NAME', 'restart_state_name'),
                        config.get('CURRENT_NUMBER', 'current_number'),
                        config.get('STAGING', 'authorization'),
                        config.get('STAGING', 'content-type'),
                        config.get('CURRENT_BOT_TYPE', 'current_bot_type'),
                        config.get('CURRENT_FAQS', 'faqs'),
                        config.get('CURRENT_FAQS_STATE_NAME', 'current_faqs_state_name'),
                        config.get('CURRENT_CMS_BOT_SLUG', 'current_cms_bot_slug'),
                        config.get('FB_USER', 'fb_user'),
                        config.get('FB_PASSWORD', 'fb_password'),
                        config.get('FB_BOT_NUMBER', 'fb_bot_number')
                        #config.get('TESTS_DIR', 'test_dir')
                        )
