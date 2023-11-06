from fastapi import Depends, HTTPException
from firebase_admin import auth
from src.backend.schemas.auth_schema import UserRegistration, UserLogin, AdminRegistration
from src.backend.schemas.profile_schema import *
import pyrebase
from src.backend.config.firebase_config import config
from src.backend.classes.professional import Professional
from src.backend.database.database import *
from firebase_admin import firestore

def funct_listall_professionals():
    professionals = getProfessionals()
    return professionals

def funct_view_professional_profile(token: str):
    decoded_token = auth.verify_id_token(token)
    professional_id = decoded_token.get('professional_id')
    if not professional_id:
        raise HTTPException(status_code=400, detail="professional_id not found in token.")

    # Get professional details using the professional_ID
    professional = getProfessional(professional_id)
    if not professional:
        raise HTTPException(status_code=404, detail="professional not found")
    
    return professional