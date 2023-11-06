from pydantic import BaseModel
from abc import ABC, abstractmethod
from typing import Optional

class User(ABC, BaseModel):
    email: str
    phone_number: Optional[str] = None
    
    @classmethod
    def from_dict(cls, user_dict):
        return cls(**user_dict)
        
    @abstractmethod    
    def to_dict(self):
        pass
        
    def __repr__(self):
        return f"(\
            email: {self.email}, \
            phone_number: {self.phone_number} \
        )"

        
    
        
    