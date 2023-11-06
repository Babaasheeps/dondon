# Abstraction layer for interacting with database
import sys

sys.path.append('/home/andy/COMP/COMP3900/capstone-project-3900h13bpotatoes/project-pals')
from .firestore import db
from src.backend.classes.project import Project
from src.backend.classes.professional import Professional
from src.backend.classes.company import Company
from src.backend.classes.admin import Admin
from firebase_admin import auth
from fastapi import FastAPI, Depends, HTTPException, Body, Header
from src.backend.classes.applications import Application
from typing import List
# TODO: refactor get functions

# ------------------------------------
# PROJECT SECTION
# ------------------------------------

# Get all projects
def getProjects():
    projects = db.collection("projects").stream()
    project_list = []
    
    for project_snapshot in projects:
        project_data = project_snapshot.to_dict()
        project = Project.from_dict(project_data)
        project_list.append(project)
    
    return project_list
        
# Create a project
def addProject(project: Project):
    project_ref = db.collection("projects").document()
    project_ref.set(project.to_dict())
    project_id = project_ref.id
    project_ref.update({"project_id": project_id})
    
    project_snapshot = project_ref.get()
    return Project.from_dict(project_snapshot.to_dict())
    
# Get a project from its project_ID
def getProject(project_id):
    project_ref = db.collection("projects").document(project_id)
    project_snapshot = project_ref.get()
    
    return Project.from_dict(project_snapshot.to_dict())
    
# Get a project reference from its project_id
def getProjectRef(project_id):
    project_ref = db.collection("projects").document(project_id)
    return project_ref
    
# Get a project from a project reference
def getProjectFromRef(project_ref):
    project_snapshot = project_ref.get()
    return Project.from_dict(project_snapshot.to_dict())
        
# Edit project
def editProject(project_data):
    project_ref = db.collection("projects").document(project_data.project_id)
    project_ref.update(project_data.dict())
    
# Delete project
def deleteProject(project):
    db.collection("projects").document(project.project_id).delete()
    
# ------------------------------------
# PROFESSIONAL SECTION
# ------------------------------------

# Get all professionals
def getProfessionals():
    professionals = db.collection("professionals").stream()
    professionals_list = []
    
    for professional_snapshot in professionals:
        professional_data = professional_snapshot.to_dict()
        professional = Professional.from_dict(professional_data)
        professionals_list.append(professional)
        
    return professionals_list
        
# Create a professional
def addProfessional(professional):
    professional_ref = db.collection("professionals").document(professional.professional_id).set(professional.to_dict())
    
# Get a professional from its professional_ID
def getProfessional(professional_id):
    professional_ref = db.collection("professionals").document(professional_id)
    professional_snapshot = professional_ref.get()
    if not professional_snapshot.exists:
        return None
    return Professional.from_dict(professional_snapshot.to_dict())

# Get a professional reference from a professional_id
def getProfessionalRef(professional_id):
    professional_ref = db.collection("professionals").document(professional_id)
    return professional_ref

# Get a professional from a professional reference
def getProfessionalFromRef(professional_ref):
    professional_snapshot = db.document(professional_ref).get()
    return Professional.from_dict(professional_snapshot.to_dict())
    
# Edit professional
def editProfessional(professional):
    professional_ref = db.collection("professionals").document(professional.email)
    professional.update(professional.to_dict())
    
# Delete professional
def deleteProfessional(professional):
    professional_id = professional.professional_id
    db.collection("professionals").document(professional_id).delete()
    try:
        auth.delete_user(professional_id)
    except auth.UserNotFoundError:
        raise

# ------------------------------------
# COMPANY SECTION
# ------------------------------------

# Get all companies
def getCompanies():
    companies = db.collection("companies").stream()
    companies_list = []
    
    for company_snapshot in companies:
        company_data = company_snapshot.to_dict()
        company = Company.from_dict(company_data)
        companies_list.append(company)
        
    return companies_list
    
# Create a company
def createCompany(company):
    company_ref = db.collection("companies").document(company.company_id).set(company.to_dict())

# Get a company from its company_id
def getCompany(company_id):
    company_ref = db.collection("companies").document(company_id)
    company_snapshot = company_ref.get()
    if not company_snapshot.exists:
        return None
    return Company.from_dict(company_snapshot.to_dict())
 
# Get a company reference from its company
def getCompanyRef(company_id):
    company_ref = db.collection("companies").document(company_id)
    return company_ref

# Get a company from its company reference
def getCompanyFromRef(company_ref):
    company_snapshot = db.document(company_ref).get()
    return Company.from_dict(company_snapshot.to_dict())
    
# Edit company
def editCompany(edited_data, company_id):
    company_ref = db.collection("companies").document(company_id)
    company_ref.update(edited_data.dict())
    company_snapshot = company_ref.get()
    
    return Company.from_dict(company_snapshot.to_dict())
    
# Delete company
def deleteCompany(company):
    company_id = company.company_id
    db.collection("companies").document(company_id).delete()
    try:
        auth.delete_user(company_id)
    except auth.UserNotFoundError:
        raise

# ------------------------------------
# ADMIN SECTION
# ------------------------------------

# Get all admins
def getAdmins():
    admins = db.collection("admins").stream()
    admins_list = []
    
    for admin_snapshot in admins:
        admin_data = admin_snapshot.to_dict()
        admin = Admin.from_dict(admin_data)
        admins_list.append(admin)
        
    return admins_list
    
# Create an admin
def createAdmin(admin):
    admin_id = admin.admin_id
    admin_ref = db.collection("admins").document(admin_id).set(admin.to_dict())

    
# Get an admin from its admin_id
def getAdmin(admin_id):
    admin_ref = db.collection("admins").document(admin_id)
    admin_snapshot = admin_ref.get()
    if not admin_snapshot.exists:
        return None

    return Admin.from_dict(admin_snapshot.to_dict())

 
# Check if admin
def is_admin(authorization: str = Header(...)):
    # Extract the token from the Authorization header
    token = authorization.split("Bearer ")[1] if "Bearer " in authorization else authorization.split("bearer ")[1]

    print(f"Token Extracted: {token}")

    # Verify the token using Firebase Admin SDK
    decoded_token = auth.verify_id_token(token)
    email = decoded_token.get('email')
    print(f"Decoded Token Email: {email}")
    user_id = decoded_token.get('user_id')
    # Check if this email belongs to an admin
    admin_data = getAdmin(user_id)
    print(f"Admin Data: {admin_data}")
    if not admin_data:
        raise HTTPException(status_code=403, detail="You are not authorized to perform this action.")

    return email

# Edit admin
def editAdmin(admin):
    admin_ref = db.collection("admins").document(admin.email)
    admin_ref.update(admin.to_dict())
    
# Delete admin
def deleteAdmin(admin):
    admin_id = admin.admin_id
    db.collection("admins").document(admin_id).delete()
    try:
        auth.delete_user(admin_id)
    except auth.UserNotFoundError:
        raise

# Get all users
def getAllUsers():
    professionals_list = getProfessionals()
    companies_list = getCompanies()
    admins_list = getAdmins()
    all_users_list = professionals_list + companies_list + admins_list

    return all_users_list

# ------------------------------------
# APPLICATION SECTION
# ------------------------------------
def createApplication(application: Application):
    # application_ref = db.collection("applications").add(application)
    # application_id = application_ref.id
    # application_ref.update({"application_id": application_id})

    # application_snapshot = application_ref.get()
    
    application_ref = db.collection("applications").document()
    application_ref.set(application.to_dict())
    application_id = application_ref.id
    application_ref.update({"application_id": application_id})
    
    application_snapshot = application_ref.get()
    application_dict = application_snapshot.to_dict()
    return Application.from_dict(application_dict)
    
def deleteApplication(application):
    db.collection("applications").document(application.application_id).delete()
    
def getApplication(application_id: str) -> Application:
    application = db.collection("applications").document(application_id)
    return application
    
def editApplication(application: Application):
    application_ref = db.collection("applications").document(application.application_id)
    application_ref.update(application.to_dict())
    
def getAllApplications() -> List[Application]:
    application_snapshots = db.collection("applications").stream()
    application_list = []
    
    for application_snapshot in application_snapshots:
        application_data = application_snapshot.to_dict()
        application = Application.from_dict(application_data)
        application_list.append(application)
        
    return application_list