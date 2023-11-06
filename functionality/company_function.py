from src.backend.schemas.profile_schema import *
from fastapi import Depends, HTTPException
from time import sleep
from firebase_admin import auth
from src.backend.database.database import *

def funct_view_company_profile(token: str):
    # Decode token to get company_ID
    decoded_token = auth.verify_id_token(token)
    company_id = decoded_token.get('company_id')
    if not company_id:
        raise HTTPException(status_code=400, detail="company_id not found in token.")

    # Get company details using the company_ID
    company = getCompany(company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    return company
    
def funct_edit_company_profile(company_data: CompanyEdit, company_id: str):
    return editCompany(company_data, company_id)
