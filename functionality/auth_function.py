from fastapi import Depends, HTTPException, Request
from firebase_admin import auth, exceptions
from firebase_admin.auth import EmailAlreadyExistsError
from src.backend.schemas.auth_schema import UserRegistration, UserLogin, AdminRegistration
import pyrebase
from src.backend.config.firebase_config import config
from src.backend.classes.professional import Professional
from src.backend.classes.company import Company
from src.backend.database.database import *
from firebase_admin import firestore
import re
import random

db = firestore.client()
pb = pyrebase.initialize_app(config)

def auth_register_user(data: UserRegistration):
    # Email valid
    if not re.match(r"[^@]+@[^@]+\.[^@]+", data.email):
        raise HTTPException(status_code=400, detail="Invalid email format")

    # Password check
    if len(data.password) < 6:
        raise HTTPException(status_code=400, detail="Password should be at least 6 characters long")
    try:
        user = auth.create_user(
            email=data.email,
            password=data.password
        )
    except EmailAlreadyExistsError:
        raise HTTPException(status_code=400, detail="Email already in use")
            
    user_id = user.uid
    claims = {}
    if data.role == "Professional":
        professional = Professional(
            professional_id = user_id,
            website_url = data.website_url,
            job = data.job,
            email = data.email,
            firstname = data.firstname,
            lastname = data.lastname,
            biography = data.biography,
            phone_number = data.phone_number,
            logo = data.logo
        )
        addProfessional(professional)
        claims["professional_id"] = user_id

    elif data.role == "Company":
        display_name = data.company_name
        company = Company(
            email = data.email,
            company_id = user_id, 
            company_name = data.company_name, 
            website_url = data.website_url,
            industry = data.industry, 
            project_url = data.project_url,
            organization = data.organization,
            phone_number= data.phone_number,
            logo = data.logo,
            biography = data.biography
        )
        createCompany(company)
        claims["company_id"] = user_id
    else:
        raise HTTPException(status_code=400, detail="Invalid role specified")
    
    auth.set_custom_user_claims(user_id, claims)
    user = pb.auth().sign_in_with_email_and_password(data.email, data.password)
    jwt_token = user['idToken']
    # print(jwt_token)
    return {"token": jwt_token}

def auth_login_user(data: UserLogin):
    # Check for admin
    
    try:
        user = pb.auth().sign_in_with_email_and_password(data.email, data.password)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid login credentials")
    jwt_token = user['idToken']
    user_id = user['localId']
    admin = getAdmin(user_id)
    user_role = get_user_role_by_id(user_id)
    
    if admin:
        pass
        return {"token": jwt_token, "role": "Admin"}
    else:
        
        if not user_role:
            raise HTTPException(status_code=400, detail="Role not found for the user")
        return {"token": jwt_token, "role": user_role}
    
def get_user_role_by_id(user_id: str) -> str:
    if getProfessional(user_id):
        return "Professional"
    elif getCompany(user_id):
        return "Company"
    return None

def get_user_role_by_token(token: str) -> str:
    decoded_token = auth.verify_id_token(token)
    user_id = decoded_token.get('user_id')
    if getProfessional(user_id):
            return "Professional"
    elif getCompany(user_id):
        return "Company"
    return None

def auth_delete_user(user_id: str, admin_email: str = Depends(is_admin)):
    print(f"Admin Email: {admin_email}")
    all_users = getAllUsers()
    
    for user in all_users:
        # Determine the appropriate ID based on the type of user
        if isinstance(user, Professional) and user.professional_id == user_id:
            try:
                deleteProfessional(user)
                return {"message": f"Professional with ID {user_id} has been deleted successfully"}
            except auth.UserNotFoundError:
                # If user isn't found in Firebase
                raise HTTPException(status_code=404, detail=f"Firebase User not found for {user_id}")

        elif isinstance(user, Company) and user.company_id == user_id:
            try:
                deleteCompany(user)
                return {"message": f"Company with ID {user_id} has been deleted successfully"}
            except auth.UserNotFoundError:
                # If user isn't found in Firebase
                raise HTTPException(status_code=404, detail=f"Firebase User not found for {user_id}")

        elif isinstance(user, Admin) and user.admin_id == user_id:
            try:
                deleteAdmin(user)
                return {"message": f"Admin with ID {user_id} has been deleted successfully"}
            except auth.UserNotFoundError:
                # If user isn't found in Firebase
                raise HTTPException(status_code=404, detail=f"Firebase User not found for {user_id}")

    # In case no user was found with the given ID
    raise HTTPException(status_code=404, detail="User not found")


def auth_register_admin(data: AdminRegistration, admin_email: str = Depends(is_admin)):
    print(f"Admin Email (from dependency): {admin_email}")
    temp_password = str(random.randint(100000, 999999))
    try:
        user = auth.create_user(
            email=data.email,
            password=temp_password
        )
    except EmailAlreadyExistsError:
        raise HTTPException(status_code=400, detail="Email already in use")
    user_id = user.uid
    claims = {}
    admin = Admin(user_id=user_id, email=data.email)
    createAdmin(admin)
    claims["admin_id"] = user_id
    auth.set_custom_user_claims(user_id, claims)
    user = pb.auth().sign_in_with_email_and_password(data.email, temp_password)
    jwt_token = user['idToken']
    print(jwt_token)
    # send reset password email to new admin
    pb.auth().send_password_reset_email(data.email)

    return {"token": jwt_token, "role": "Admin", "temp_password": temp_password, "message": "Invitation sent to new admin."}

def get_company_id(token: str) -> str:
    decoded_token = auth.verify_id_token(token)
    company_id = decoded_token.get('company_id')
    if not company_id:
        raise HTTPException(status_code = 400, details = "company_id not found in token")
    return company_id

def get_professional_id(token: str) -> str:
    decoded_token = auth.verify_id_token(token)
    professional_id = decoded_token.get('professional_id')
    if not professional_id:
        raise HTTPException(status_code = 400, details = "professional_id not found in token")
    return professional_id

def get_user_role_by_email(email: str) -> str:
    professional = getProfessional(email)
    if professional:
        return "Professional"
    elif getCompany(email):   
        return "Company"

def funct_get_user_role(token: str):
    decoded_token = auth.verify_id_token(token)
    email = decoded_token['email']
    user_role = get_user_role_by_email(email)
    
    if not user_role:
        raise HTTPException(status_code=404, detail="Role not found for the user")

    return {"role": user_role}

def get_user_role_by_token(token: str) -> str:
    decoded_token = auth.verify_id_token(token)
    user_id = decoded_token.get('user_id')
    if getProfessional(user_id):
            return "Professional"
    elif getCompany(user_id):
        return "Company"
    return None


def get_token(request: Request):
    headers = dict(request.headers)
    token = headers['authorization'].split()[1]
    return token

def get_user_id_from_token(token: str):
    decoded_token = auth.verify_id_token(token)
    user_id = decoded_token.get('user_id')
    return user_id