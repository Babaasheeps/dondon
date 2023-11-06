from src.backend.database.database import *
from src.backend.classes.applications import Application

def funct_apply_to_project(project_id, professional_id):
    project = getProject(project_id)
    application = Application(
        project_ref = getProjectRef(project_id),
        company_ref = getCompanyRef(project.owner),
        professional_ref = getProfessionalRef(professional_id)
    )
    new_application = createApplication(application)
    return new_application.application_id

def funct_view_projects_applied(professional_id):
    all_applications = getAllApplications()
    professional_ref = getProfessionalRef(professional_id)
    projects_applied = []
    for application in all_applications:
        if application.professional_ref == professional_ref:
            projects_applied.append(application)

    return projects_applied

def funct_view_all_applicants(project_id, company_id):
    project = getProject(project_id)
    if project.owner is not company_id:
        raise HTTPException(status_code=401, detail="User does not have access to the project")
    all_applications = getAllApplications()
    project_ref = getProjectRef(project_id)
    applicants = []
    for application in all_applications:
        if application.project_ref == project_ref:
            applicants.append(application)
    
    return applicants

def funct_accept_professional(application_id: str, company_id: str, project_id: str):
    application = getApplication(application_id)
    company_ref = getCompanyRef(company_id)
    project_ref = getProjectRef(project_id)
    project = getProjectFromRef(project_ref)
    if application.company_ref is not company_ref:
        raise HTTPException(status_code=401, detail="User does not have access to the project")
    application.status = "Accepted"
    editApplication(application)

    project = getProjectFromRef(application.project_ref)
    project.hired_professionals.append(application.professional_ref)

    return application

def funct_reject_professional(application_id: str, company_id: str, project_id: str):
    company_ref = getCompanyRef(company_id)
    application = getApplication(application_id)
    if application.company_ref is not company_ref:
        raise HTTPException(status_code=401, detail="User does not have access to the project")
    application.status = "Rejected"
    editApplication(application)
    return application

def funct_list_accepted_professionals(company_id, project_id):
    project_ref = getProjectRef(project_id)
    project = getProjectFromRef(project_ref)
    if project.owner is not company_id:
        raise HTTPException(status_code=401, detail="User does not have access to the project")
    all_applications = getAllApplications()
    accepted_professionals = []
    for application in all_applications:
        if application.project_ref == project_ref and application.status == "Accepted":
            professional = getProfessionalFromRef(application.professional_ref)
            accepted_professionals.append(professional)

    return accepted_professionals

def funct_list_rejected_professionals(company_id, project_id):
    project_ref = getProjectRef(project_id)
    project = getProjectFromRef(project_ref)
    if project.owner is not company_id:
        raise HTTPException(status_code=401, detail="User does not have access to the project")
    all_applications = getAllApplications()
    rejected_professionals = []
    for application in all_applications:
        if application.project_ref == project_ref and application.status == "Rejected":
            professional = getProfessionalFromRef(application.professional_ref)
            rejected_professionals.append(professional)

    return rejected_professionals

def funct_list_pending_professionals(company_id, project_id):
    project_ref = getProjectRef(project_id)
    project = getProjectFromRef(project_ref)
    if project.owner is not company_id:
        raise HTTPException(status_code=401, detail="User does not have access to the project")
    all_applications = getAllApplications()
    pending_professionals = []
    for application in all_applications:
        if application.project_ref == project_ref and application.status == "Pending":
            professional = getProfessionalFromRef(application.professional_ref)
            pending_professionals.append(professional)

    return pending_professionals