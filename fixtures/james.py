from telnetlib import Telnet


class JamesHelper:

    def __init__(self, app):
        self.app = app

    def ensure_user_exists(self, username, password):
        james_config = self.app.config['james']
        session = JamesHelper.Session(james_config['host'], james_config['port'], james_config['username'], james_config['password'])
        if session.is_user_registred(username):
            session.reset_password(username, password)
        else:
            session.create_user(username, password)
        session.quit()

    class Session:

        def __init__(self, host, port, username, password):
            self.telnet = Telnet(host, port, 5)
            self.reed_until('Login id')
            self.write_until(username + '\n')
            self.reed_until('Password')
            self.write_until(password + '\n')
            self.reed_until('Welcome root. HELP for a list of commands')

        def reed_until(self, text):
            self.telnet.read_until(text.encode('ascii'), 5)

        def write_until(self, text):
            self.telnet.write(text.encode('ascii'))

        def is_user_registred(self, username):
            self.write_until('verify %s\n' % username)
            result = self.telnet.expect([b'exists', b'does not exist'])
            return result[0] == 0

        def create_user(self, username, password):
            self.write_until('adduser %s %s\n' % (username, password))
            self.reed_until('User %s added' % username)

        def reset_password(self, username, password):
            self.write_until('setpassword %s %s\n' % (username, password))
            self.reed_until('Password for %s reset' % username)

        def quit(self):
            self.write_until('quit\n')