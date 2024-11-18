from data.project import testdata
import pytest


@pytest.mark.parametrize("project", testdata, ids=[repr(x) for x in testdata])
def test_add_project(app, project):
    old_list = app.project.get_project_list()
    app.project.create(project)
    new_list = app.project.get_project_list()
    assert len(old_list) + 1 == len(new_list)