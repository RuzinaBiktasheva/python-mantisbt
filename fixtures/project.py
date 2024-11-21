from selenium.webdriver.support.ui import Select
from models.project import Project


class ProjectHelper:

    def __init__(self, app):
        self.app = app

    # заполнение полей
    def filling_fields(self, project):
        wd = self.app.wd
        wd.find_element_by_name('name').click()
        wd.find_element_by_name('name').clear()
        wd.find_element_by_name('name').send_keys(project.name)
        wd.find_element_by_name('status').click()
        Select(wd.find_element_by_name('status')).select_by_visible_text(project.status)
        wd.find_element_by_name('view_state').click()
        Select(wd.find_element_by_name('view_state')).select_by_visible_text(project.view_status)
        wd.find_element_by_name('description').click()
        wd.find_element_by_name('description').clear()
        wd.find_element_by_name('description').send_keys(project.description)

    def open_project_page(self):
        wd = self.app.wd
        wd.find_element_by_link_text('Manage').click()
        wd.find_element_by_link_text('Manage Projects').click()

    # добавление проекта
    def create(self, project):
        wd = self.app.wd
        self.open_project_page()
        wd.find_element_by_css_selector('input[value="Create New Project"]').click()
        self.filling_fields(project)
        wd.find_element_by_css_selector('input[value="Add Project"]').click()

    # получение списка проектов
    def get_project_list(self):
        wd = self.app.wd
        self.open_project_page()
        list = []
        for element in wd.find_elements_by_css_selector('tr:has(a[href^="manage_proj_edit_page.php?project_id="])'):
            name = element.find_element_by_xpath('td[1]').text
            status = element.find_element_by_xpath('td[2]').text
            view_status = element.find_element_by_xpath('td[4]').text
            description = element.find_element_by_xpath('td[5]').text
            id = element.find_element_by_css_selector('td a').get_attribute('href')[70:]
            list.append(Project(name=name, status=status, view_status=view_status, description=description, id=id))
        return list

    # получение количества проектов
    def count(self):
        wd = self.app.wd
        self.open_project_page()
        return len(wd.find_elements_by_css_selector('a[href^="manage_proj_edit_page.php?project_id="]'))

    # удаление проекта по id
    def delete_by_id(self, id):
        wd = self.app.wd
        self.open_project_page()
        wd.find_element_by_css_selector('a[href$="%s"]' % id).click()
        wd.find_element_by_css_selector('input[value="Delete Project"]').click()
        wd.find_element_by_css_selector('input[value="Delete Project"]').click()

    # удаление проекта по имени
    def delete_by_name(self, name):
        wd = self.app.wd
        self.open_project_page()
        wd.find_element_by_link_text(name).click()
        wd.find_element_by_css_selector('input[value="Delete Project"]').click()
        wd.find_element_by_css_selector('input[value="Delete Project"]').click()

    # удаление проекта по индексу
    def delete_by_index(self, index):
        wd = self.app.wd
        self.open_project_page()
        wd.find_element_by_css_selector('tr[class$="%s"] a' % index).click()
        wd.find_element_by_css_selector('input[value="Delete Project"]').click()
        wd.find_element_by_css_selector('input[value="Delete Project"]').click()