from data.project import testdata
import pytest
from models.project import Project


@pytest.mark.parametrize("project", testdata, ids=[repr(x) for x in testdata])
def test_add_project(app, project):
    list_ui = app.project.get_project_list()
    app.project.create(project)
    list_ui.append(project)
    list_soap = app.soap.list_projects_from_soap(app.config["webadmin"]["username"], app.config["webadmin"]["password"])
    assert sorted(list_ui, key=Project.sort) == sorted(list_soap, key=Project.sort)