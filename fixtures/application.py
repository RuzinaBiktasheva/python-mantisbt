from selenium import webdriver
from fixtures.session import SessionHelper
from fixtures.project import ProjectHelper
from fixtures.james import JamesHelper
from fixtures.signup import SugnupHelper
from fixtures.mail import MailHelper
from fixtures.soap import SoapHelper

# класс менеджер:
class Application:

    def __init__(self, browser, config):
        if browser == 'firefox':
            self.wd = webdriver.Firefox()
        elif browser == 'chrome':
            self.wd = webdriver.Chrome()
        else:
            raise ValueError('Unrecognized browser: ' f'{browser}')
        self.session = SessionHelper(self)
        self.project = ProjectHelper(self)
        self.james = JamesHelper(self)
        self.signup = SugnupHelper(self)
        self.mail = MailHelper(self)
        self.soap = SoapHelper(self)
        self.config = config
        self.base_url = config['web']['baseUrl']

# проверка валидности фикстуры:
    def is_valid(self):
        try:
            self.wd.current_url
            return True
        except:
            return False

    def open_home_page(self):
        wd = self.wd
        wd.get(self.base_url)

    def destroy(self):
        self.wd.quit()