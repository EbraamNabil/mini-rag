from dataclasses import field

from pydantic import BaseModel, Field,validator
from typing import  Optional
from bason import ObjectId


class Project(BaseModel):
    # the datatype of _id is not str but ObjectId because that's what MongoDB uses,the objectid  is a unique identifier for each document in a MongoDB collection, and it is generated automatically by MongoDB when a new document is inserted.  
    _id: Optional[ObjectId] 
    
    project_id: str=field(...,min_length=1)
    
    
    # you can design cutom validation schema you can need it when the properties in the field can't help you
     
    @validator('project_id')
    def validate_project_id(cls,value):
        #cls >> it is a reference to the class itself(Project class),value >> it is the value of the project_id field that user is trying to set
        if not value.isalnum():
            #isalnum() is a built-in method in Python that checks if all characters in a string are alphanumeric (i.e., letters and numbers only, no special characters or spaces). If the project_id contains any non-alphanumeric characters, we raise a ValueError with a message indicating that the project_id must be alphanumeric.
            raise ValueError("project_id must be alphanumeric")
        
        return value 
    
    
    #sometime appear error because pydantic cant understand objectid type so we need to add this configuration to allow arbitrary types in pydantic model
    #that is mean we say to program when you face stanger type (like objectid) don't show errer just allow it and move on
    class Config :
        arbitary_types_allowed=True   
        

    