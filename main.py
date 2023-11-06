import requests
import pprint
from src.backend.database.database import *
from fastapi import FastAPI, Depends, Request
from src.backend.functionality.project_function import *
from src.backend.functionality.auth_function import *
from src.backend.functionality.professional_function import *
from src.backend.functionality.company_function import *
from src.backend.functionality.application_function import *
from src.backend.schemas.auth_schema import *
from src.backend.schemas.project_schema import ProjectCreation, ProjectEdit
from src.backend.schemas.profile_schema import *
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from firebase_admin import auth

# Initialize FastAPI app
app = FastAPI()

# Handling CORS
origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Authentication Routes
@app.post("/register/company")
async def register_user(data: CompanyRegistration):
    return auth_register_user(data)
    
@app.post("/register/professional")
async def register_user(data: ProfessionalRegistration):
    return auth_register_user(data)
    
@app.post("/login/user/")
async def login_user(data: UserLogin):
    return auth_login_user(data)

@app.get("/get_user_role/")
async def get_user_role(token: str):
    return funct_get_user_role(token)

@app.delete("/delete/user/{user_email}")
async def delete_user(user_email: str, email: str = Depends(is_admin)):
    return auth_delete_user(user_email, email)

# Project Routes
@app.post('/project/create')
async def create_project(project: ProjectCreation, request: Request):
    token = get_token(request)
    company_id = get_company_id(token)
    return funct_create_project(project, company_id)

@app.delete('/project/delete/{project_id}')
async def delete_project(project_id: str):
    return funct_delete_project(project_id)

@app.put('/project/{project_id}/end')
async def end_project(project_id: str, request: Request):
    token = get_token(request)
    company_id = get_company_id(token)
    return funct_end_project(project_id, company_id)

@app.get('/project/listall')
async def listall_projects():
    return funct_listall_projects()

@app.get('/project/{project_id}')
async def get_project_details(project_id: str, request: Request):
    token = get_token(request)
    user_id = get_user_id_from_token(token)
    return funct_get_project_details(user_id, project_id)

@app.get('/company/project/view')
async def view_company_project(request: Request):
    token = get_token(request)
    company_id = get_company_id(token)
    return funct_view_company_projects(company_id)

@app.get('/professional/project/view/')
async def view_professional_project(request: Request):
    token = get_token(request)
    professional_id = get_professional_id(token)
    return funct_view_professional_projects(professional_id)

# Application routes
@app.post('/project/apply/{project_id}')
async def apply_to_project(project_id: str, request: Request):
    token = get_token(request)
    professional_id = get_professional_id(token)
    return funct_apply_to_project(project_id, professional_id)

@app.get('/professional/projects/applied/')
async def view_projects_applied(request: Request):
    token = get_token(request)
    professional_id = get_professional_id(token)
    return funct_view_projects_applied(professional_id)

@app.get('/company/applicants/{project_id}')
async def view_applicants(project_id: str, request: Request):
    token = get_token(request)
    company_id = get_company_id(token)
    return funct_view_all_applicants(project_id, company_id)

@app.put('/{project_id}/{application_id}/accept')
async def accept_professional(application_id: str, project_id: str, request: Request):
    token = get_token(request)
    company_id = get_company_id(token)
    return funct_accept_professional(application_id, company_id, project_id)

@app.put('/{project_id}/{application_id}/reject')
async def reject_professional(application_id: str, project_id: str, request: Request):
    token = get_token(request)
    company_id = get_company_id(token)
    return funct_reject_professional(application_id, company_id, project_id)

@app.get('/project/{project_id}/accepted')
async def list_accepted_professionals(project_id: str, request: Request):
    token = get_token(request)
    company_id = get_company_id(token)
    return funct_list_accepted_professionals(company_id, project_id)

@app.get('/project/{project_id}/rejected')
async def list_rejected_professionals(project_id: str, request: Request):
    token = get_token(request)
    company_id = get_company_id(token)
    return funct_list_rejected_professionals(company_id, project_id)

@app.get('/project/{project_id}/pending')
async def list_pending_professionals(project_id: str, request: Request):
    token = get_token(request)
    company_id = get_company_id(token)
    return funct_list_pending_professionals(company_id, project_id)
    
@app.put("/project/{project_id}/edit")
async def edit_company_profile(project_data: ProjectEdit, request: Request):
    headers = dict(request.headers)
    token = headers['authorization'].split()[1]
    login_company_id = get_company_id(token)
    
    current_project = getProject(project_data.project_id)
    
    if login_company_id != current_project.owner:
        raise HTTPException(status_code = 401, detail = "Logged in user doesn't have editor access on this profile")
    
    funct_edit_project(project_data)

# Admin Routes
@app.delete("/delete/user/{user_id}")
async def delete_user(user_id: str, authorization: str = Depends(is_admin)):
    return auth_delete_user(user_id, authorization)

@app.post("/register/admin/")
async def register_admin(request: Request, data: AdminRegistration):
    admin_email = is_admin(request.headers.get("Authorization"))
    return auth_register_admin(data, admin_email)

# Professional Routes
@app.get("/professional/profile", response_model=Professional)
async def view_professional_profile(request: Request):
    token = get_token(request)
    return funct_view_professional_profile(token)

@app.get('/professional/listall')
async def listall_professionals():
    return funct_listall_professionals()

# Company Routes
@app.get("/company/profile", response_model=Company)
async def view_company_profile(request: Request):
    token = get_token(request)
    return funct_view_company_profile(token)
    
@app.put("/company/profile/edit")
async def edit_company_profile(request: Request, company_data: CompanyEdit):
    headers = dict(request.headers)
    token = headers['authorization'].split()[1]
    login_company_id = get_company_id(token)
    
    # if login_company_id is not company_data.company_id:
    #     raise HTTPException(status_code = 401, detail = "Logged in user doesn't have editor access on this profile")
    
    return funct_edit_company_profile(company_data, login_company_id)

if __name__ == "__main__":
    print("this might be running\n")
    uvicorn.run("src.backend.main:app", reload=True)
    print("this is running\n")
    