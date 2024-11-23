import pytest
import json
import os.path
import ftputil
from fixtures.application import Application

fixture = None
target = None


# загрузка конфигурации
def load_config(file):
    global target
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    if target is None:
        config_file = os.path.join(path, file)
        with open(config_file) as file:
            target = json.load(file)
    return target

# фикстура для конфигурации
@pytest.fixture (scope="session")
def config(request):
    return load_config(request.config.getoption('--target'))

# инициализация фикстуры
@pytest.fixture
def app(request, config):
    global fixture
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    web_config_admin = config['webadmin']
    browser = request.config.getoption('--browser')
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=browser, config=config)
    fixture.session.ensure_login(username=web_config_admin['username'], password=web_config_admin['password'])
    return fixture

# фикстура для ftp-соедения
@pytest.fixture (scope="session", autouse=True)
def configer_server(request, config):
    install_server_configuration(config['ftp']['host'], config['ftp']['username'], config['ftp']['password'])
    def fin():
        restore_server_configuration(config['ftp']['host'], config['ftp']['username'], config['ftp']['password'])
    request.addfinalizer(fin)

def install_server_configuration(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile('config_inc.php.bak'):
            remote.remove('config_inc.php.bak')
        if remote.path.isfile('config_inc.php'):
            remote.rename('config_inc.php', 'config_inc.php.bak')
        remote.upload(os.path.join(os.path.dirname(__file__), 'resourses/config_inc.php'), 'config_inc.php')

def restore_server_configuration(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile('config_inc.php.bak'):
            if remote.path.isfile('config_inc.php'):
                remote.remove('config_inc.php')
            remote.rename('config_inc.php.bak', 'config_inc.php')

# финализация фикстуры:
@pytest.fixture (scope="session", autouse=True)
def stop(request):
    def fin():
        fixture.session.ensure_logout()
        fixture.destroy()
    request.addfinalizer(fin)
    return fixture

# инициализация параметров
def pytest_addoption(parser):
    parser.addoption('--browser', action='store', default='firefox')
    parser.addoption('--target', action='store', default='target.json')
