class SessionHelper():

    def __init__(self, app, base_url):
        self.app = app
        self.base_url = base_url

    def login(self, username, password):
        wd = self.app.wd
        self.app.open_home_page()
        wd.find_element_by_name("username").click()
        wd.find_element_by_name("username").clear()
        wd.find_element_by_name("username").send_keys(username)
        wd.find_element_by_name("password").click()
        wd.find_element_by_name("password").clear()
        wd.find_element_by_name("password").send_keys(password)
        wd.find_element_by_css_selector("input[type='submit']").click()

    def logout(self):
        wd = self.app.wd
        wd.find_element_by_link_text("Logout").click()
        wd.get(self.base_url)

# проверка аунтификации:
    def is_logged_in(self):
        wd = self.app.wd
        return len(wd.find_elements_by_link_text("Logout")) > 0

# проверка, что аунтификация выполнена под нужным пользователем:
    def is_logged_in_as(self, username):
        wd = self.app.wd
        return self.get_logged_user() == username

# получение имени пользователя
    def get_logged_user(self):
        wd = self.app.wd
        return wd.find_element_by_css_selector('td.login-info-left span').text

# проверка при выходе из системы:
    def ensure_logout(self):
        wd = self.app.wd
        if self.is_logged_in():
            self.logout()

# проверка при аунтификации:
    def ensure_login(self, username, password):
        wd = self.app.wd
        if self.is_logged_in():
            if self.is_logged_in_as(username):
                return
            else:
                self.logout()
        self.login(username, password)