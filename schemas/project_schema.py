from pydantic import BaseModel

class ProjectCreation(BaseModel):
    project_name: str = None
    start_date: str = None
    end_date: str = None
    location: str = None
    number_prof: str = None
    project_description: str = None
    required_skills: str = None
    private_details: str = None

class ProjectDetails(ProjectCreation):
    company_name: str = None
    company_industry: str = None
    company_type: str = None
    company_link: str = None
    company_biography: str = None
    company_email: str = None

class ProjectEdit(BaseModel):
    project_id: str = None
    project_name: str = None
    start_date: str = None
    end_date: str = None
    location: str = None
    number_prof: str = None
    project_description: str = None
    required_skills: str = None
    private_details: str = None
