from configparser import ConfigParser

from config.Settings import Settings


class ReadConfig:

    def readConfigFile(self):
        file = '/Users/kepler.velasco/Documents/WorkspaceSelenium/SeleniumPythonTesting/config/config.ini'
        config = ConfigParser()
        config.read(file)
        name = config.get('BOT', 'bot')
        return Settings(config.get(name, 'bot_' + name),
                        config.get('CHROME-PROFILE-PATH', 'ProfilePath'),
                        config.get(name, 'bot_slug_' + name),
                        config.get('botrunner_auth_token', 'botrunner_auth_token'),
                        config.get(name, 'restart_state_name_' + name),
                        config.get('CURRENT_NUMBER', 'current_number'),
                        config.get('STAGING', 'authorization'),
                        config.get('STAGING', 'content-type'),
                        config.get(name, 'bot_type_' + name),
                        config.get(name, 'faqs_type_' + name),
                        config.get(name, 'faqs_' + name),
                        config.get(name, 'cms_bot_slug_' + name),
                        config.get('FB_USER', 'fb_user'),
                        config.get('FB_PASSWORD', 'fb_password'),
                        config.get(name, 'fb_bot_number_' + name))
