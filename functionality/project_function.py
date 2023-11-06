from src.backend.schemas.project_schema import ProjectCreation, ProjectDetails, ProjectEdit
from src.backend.database.database import *
from src.backend.classes.project import Project
from src.backend.classes.applications import Application
from google.cloud.firestore_v1.document import DocumentReference

def funct_create_project(data: ProjectCreation, company_id: str):
    project = Project(
        project_name = data.project_name, 
        start_date = data.start_date, 
        end_date = data.end_date,
        location = data.location,
        number_prof = data.number_prof,
        project_description = data.project_description,
        required_skills = data.required_skills,
        owner = company_id,
        hired_professionals = [],
        private_details = data.private_details
    )
    new_project = addProject(project)
    return new_project

def funct_delete_project(project_id):
    project = getProject(project_id)
    deleteProject(project)
    return project

def funct_listall_projects():
    all_projects = getProjects()
    return all_projects

def funct_get_project_details(user_id: str, project_id: str):
    project = getProject(project_id)
    company = getCompany(project.owner)
    
    new_project_details = ProjectDetails(
        project_name=project.project_name,
        start_date=project.start_date,
        end_date=project.end_date,
        location=project.location,
        number_prof=project.number_prof,
        project_description=project.project_description,
        required_skills=project.required_skills,
        company_name=company.company_name,
        company_industry=company.industry,
        company_type=company.organization,
        company_link=company.website_url,
        company_biography=company.biography,
        company_email=company.email
    )

    if user_id == project.owner or user_id in project.hired_professionals:
        new_project_details.private_details = project.private_details

    print(new_project_details)
    return new_project_details

def funct_view_company_projects(company_id):
    all_projects = getProjects()
    company_projects = []
    for project in all_projects:
        if project.owner == company_id:
            company_projects.append(project)

    return company_projects

def funct_view_professional_projects(professional_id):
    all_projects = getProjects()
    professional_ref = getProfessionalRef(professional_id)
    professional_projects = []
    for project in all_projects:
        if professional_ref in project['hired_professionals']:
            professional_projects.append(project)
    return professional_projects

def funct_edit_project(project_data: ProjectEdit):
    editProject(project_data)

def funct_end_project(project_id, company_id):
    project = getProject(project_id)
    if project.owner is not company_id:
        raise HTTPException(status_code=401, detail="User is not authorised to end the project")
    project.status = "Completed"
    editProject(project)
    return project

def funct_filter_projects():
    return 0
