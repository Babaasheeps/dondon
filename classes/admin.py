# Defines the structure of administrator type
from src.backend.classes.user import User

class Admin(User):
    admin_id: str = None
    
    def __init__ (self, **data):
        if 'user_id' in data:
            data['admin_id'] = data.pop('user_id')
        super().__init__(**data)
    
    # Converts dictionary to admin
    @classmethod
    def from_dict(cls, admin_dict):
        return cls(**admin_dict)
    
    # Converts admin into dictionary representation
    def to_dict(self):
        return self.dict()
        
    # Converts admin to string representation
    def __repr__(self):
        user_repr = super().__repr__()
        return f"Admin(\
            admin_id: {self.admin_id}, \
            {user_repr} \
        )"
