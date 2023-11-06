# Defines the structure of company type
from src.backend.classes.user import User

class Company(User):
    company_id: str = None
    company_name: str = None
    website_url: str = None
    industry: str = None
    project_url: str = None
    organization: str = None
    logo: str = None
    biography: str = None

    def __init__(self, **data):
        if 'user_id' in data:
            data['company_id'] = data.pop('user_id')
        super().__init__(**data)

    # Converts dictionary to Company
    @classmethod
    def from_dict(cls, company_dict):
        return super().from_dict(company_dict)

    # Converts Company into dictionary representation
    def to_dict(self):
        return self.dict()
        
    # Converts Company into string representation
    def __repr__(self):
        user_repr = super().__repr__()
        return f"Company(\
            company_id: {self.company_id}, \
            company_name: {self.company_name}, \
            industry: {self.industry}, \
            website_url: {self.website_url}, \
            project_url: {self.project_url}, \
            organization: {self.organization}, \
            phone_number: {self.phone_number}, \
            biography: {self.biography}, \
            logo: {self.logo}, \
            {user_repr} \
        )"
