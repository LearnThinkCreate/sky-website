from dash.utils import toTitleCase, toLowerCase

class Student:
    def __init__(
        self, 
        id: int = None, 
        first_name: str = None, 
        last_name: str = None,
        grade_level: int = None,
    ):
        self.id = id
        self.first_name = toLowerCase(first_name)
        self.last_name = toLowerCase(last_name)
        self.grade_level = toLowerCase(grade_level)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class AttendanceCodes:
    def __init__(
        self,
        codes: list
    ):
        self.codes = codes


