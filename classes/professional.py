# Defines the structure of professional type
from src.backend.classes.user import User
        
class Professional(User):
    professional_id: str = None
    firstname: str = None
    lastname: str = None
    website_url: str = None
    job: str = None
    biography: str = None
    logo: str = None

    def __init__(self, **data):
        if 'user_id' in data:
            data['professional_id'] = data.pop('user_id')
        super().__init__(**data)
    
    # Converts dictionary to Professional
    @classmethod
    def from_dict(cls, professional_dict):
        # return super.from_dict(Professional, professional_dict)
        return super().from_dict(professional_dict)
    
    # Converts professional into dictionary representation
    def to_dict(self):
        return self.dict()
        
    # Converts professional into string representation
    def __repr__(self):
        user_repr = super().__repr__()
        return f"Professional(\
            professional_id: {self.email}, \
            firstname: {self.firstname}, \
            lastname: {self.lastname}, \
            website_url: {self.website_url}, \
            job: {self.job}, \
            biography: {self.biography}, \
            logo: {self.logo}, \
            {user_repr} \
        )"
    
    