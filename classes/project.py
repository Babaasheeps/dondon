# Defines the structure of project type
from pydantic import BaseModel
from src.backend.database.database import *
from google.cloud.firestore_v1.document import DocumentReference

class Project(BaseModel):
    project_id: str = None
    project_name: str = None
    start_date: str = None
    end_date: str = None
    location: str = None
    number_prof: str = None
    project_description: str = None
    required_skills: str = None
    owner: str = None
    hired_professionals: list
    private_details: str = None
    status: str = "Active"

    class Config:
        arbitrary_types_allowed = True
        
    # Converts dictionary into project
    @staticmethod
    def from_dict(project_dict):
        return Project(**project_dict)
        
    # Converts project into dictionary representation
    def to_dict(self):
        return self.dict()
        
    # Converts project to string representation
    def __repr__ (self):
        return f"Project(\
            project_id: {self.project_id}, \
            project_name: {self.project_name}, \
            start_date: {self.start_date}, \
            end_date: {self.end_date}, \
            location: {self.location}, \
            number_prof: {self.number_prof}, \
            project_description: {self.project_description}, \
            required_skills: {self.required_skills}, \
            hired_professionals: {self.hired_professionals}, \
            owner: {self.owner}, \
            private_details: {self.private_details}, \
            status: {self.status} \
        )"