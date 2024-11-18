import pytest
import json
import os.path
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

# инициализация фикстуры
@pytest.fixture
def app(request):
    global fixture
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    web_config = load_config(request.config.getoption('--target'))['web']
    web_config_admin = load_config(request.config.getoption('--target'))['webadmin']
    browser = request.config.getoption('--browser')
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=browser, base_url=web_config['baseUrl'], path=path)
    fixture.session.ensure_login(username=web_config_admin['username'], password=web_config_admin['password'])
    return fixture

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
