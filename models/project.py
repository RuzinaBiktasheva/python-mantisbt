class Project:

    def __init__(self, name = "Project's name", status = None, view_status = None, description = None, id = None):
        self.name = name
        self.status = status
        self.view_status = view_status
        self.description = description
        self.id = id

    # переопределенная стандартная функция представления
    def __repr__(self):
        return f"{self.name}, {self.status}, {self.view_status}, {self.description}, {self.id}"

    # переопределенная стандартная функция сравнения
    def __eq__(self, other):
        return self.name == other.name and self.status == other.status and self.view_status == other.view_status and self.description == other.description