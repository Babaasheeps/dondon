from pydantic import BaseModel

# Registration Base Models
class UserRegistration(BaseModel):
    email: str
    password: str
    role: str
    website_url: str = None
    phone_number: str = None
    
class ProfessionalRegistration(UserRegistration):
    firstname: str = None
    lastname: str = None
    job : str = None
    biography: str = None
    logo: str = None

class CompanyRegistration(UserRegistration):
    company_name: str = None
    industry: str = None
    project_url: str = None
    organization: str = None
    logo: str = None
    biography: str = None

class AdminRegistration(BaseModel):
    email: str

# Login Base Models
class UserLogin(BaseModel):
    email: str
    password: str

# Token
class Token(BaseModel):
    token: str