from suds.client import Client
from suds import WebFault

class SoapHelper:
    def __init__(self, app):
         self.app = app

    def can_login(self, username, password):
        client = Client(self.app.base_url + 'api/soap/mantisconnect.php?wsdl')
        try:
            client.service.mc_login(username, password)
            return True
        except WebFault:
            return False

    def list_projects_from_soap(self,username, password):
        client = Client(self.app.base_url + 'api/soap/mantisconnect.php?wsdl')
        list = []
        try:
            projects = client.service.mc_projects_get_user_accessible(username, password)
            for project in projects:
                list.append(project.name)
            return list
        except Exception as e:
            print(f"Error: {e}")