from models.project import Project


def test_delete_project_by_id(app):
    if app.project.count() == 0:
        app.project.create(Project(name='Project_name_1', status = 'development', view_status = 'public', description = 'Description - 1'))
    old_list = app.project.get_project_list()
    app.project.delete_by_id('47')
    new_list = app.project.get_project_list()
    assert len(old_list) - 1 == len(new_list)

def test_delete_project_by_name(app):
    if app.project.count() == 0:
        app.project.create(Project(name='Project_name_1', status = 'development', view_status = 'public', description = 'Description - 1'))
    old_list = app.project.get_project_list()
    app.project.delete_by_name('Project_name_1')
    new_list = app.project.get_project_list()
    assert len(old_list) - 1 == len(new_list)

def test_delete_project_by_index(app):
    if app.project.count() == 0:
        app.project.create(Project(name='Project_name_1', status = 'development', view_status = 'public', description = 'Description - 1'))
    old_list = app.project.get_project_list()
    app.project.delete_by_index('1')
    new_list = app.project.get_project_list()
    assert len(old_list) - 1 == len(new_list)