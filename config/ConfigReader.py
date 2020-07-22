from configparser import ConfigParser

from config.Settings import Settings


class ReadConfig:

    def readConfigFile(self):
        file = '/Users/kepler.velasco/Documents/WorkspaceSelenium/SeleniumPythonTesting/config/config.ini'
        config = ConfigParser()
        config.read(file)
        return Settings(config.get('CURRENT-BOT-WA', 'Current'),
                        config.get('CHROME-PROFILE-PATH', 'ProfilePath'),
                        config.get('CURRENT-BOT-SLUG', 'Current_bot_slug'),
                        config.get('botrunner_auth_token', 'botrunner_auth_token'),
                        config.get('STATE', 'state'),
                        config.get('USER-NUMBER', 'Number'),
                        config.get('STAGING', 'authorization'),
                        config.get('STAGING', 'content-type'),
                        config.get('CURRENT_BOT_TYPE', 'current_bot_type'),
                        config.get('CURRENT_FAQS', 'faqs'),
                        config.get('cms_api_client', 'domain'),
                        config.get('FAQS_STATE_NAME', 'faqs_state_name'),
                        config.get('CMS-BOT-SLUG', 'cms_bot_slug')
                        #config.get('TESTS_DIR', 'test_dir')
                        )
