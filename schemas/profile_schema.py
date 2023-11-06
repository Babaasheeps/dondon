from pydantic import BaseModel

class CompanyProfile(BaseModel):
    #company_id: str
    email: str
    company_name: str
    industry: str
    location: str
    website_url: str
    biography: str = None
    project_url: str = None
    organization: str = None
    phone_number: str = None
    logo: str = None
    biography: str = None

class TokenUser(BaseModel):
    token: str

class CompanyEdit(BaseModel):
    company_name: str = None
    website_url: str = None
    industry: str = None
    biography: str = None
    project_url: str = None
    logo: str = None
    organization: str = None