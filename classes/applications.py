from pydantic import BaseModel
from google.cloud.firestore_v1.document import DocumentReference

class Application(BaseModel):
    application_id: str = None
    project_ref: DocumentReference
    company_ref: DocumentReference
    professional_ref: DocumentReference
    status: str = "Pending"
    
    class Config:
        arbitrary_types_allowed = True

    # Converts from dictionary containing:
        # project_id
        # company_id
        # professional_id
    # To an application
    @staticmethod
    def from_dict(application_dict):
        from src.backend.database.database import getProjectRef, getCompanyRef, getProfessionalRef
        return Application(
            application_id = application_dict.get("application_id"),
            project_ref = application_dict.get("project_ref"),
            company_ref = application_dict.get("company_ref"),
            professional_ref = application_dict.get("professional_ref"),
            status = application_dict.get("status")
        )
        
    def to_dict(self):
        return self.dict()