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
                        config.get('botrunner_auth_token', 'auth_token'),
                        config.get('STATE', 'state'),
                        config.get('USER-NUMBER', 'Number'),
                        config.get('HEADERS', 'authorization'),
                        config.get('HEADERS', 'content-type')
                        )
