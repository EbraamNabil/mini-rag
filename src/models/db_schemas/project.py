

from pydantic import BaseModel, Field,validator
from typing import  Optional
from bson import ObjectId


class Project(BaseModel):
    # the datatype of _id is not str but ObjectId because that's what MongoDB uses,the objectid  is a unique identifier for each document in a MongoDB collection, and it is generated automatically by MongoDB when a new document is inserted.  
    id: Optional[ObjectId]=Field(None,alias="_id")
 
    
    project_id: str=Field(...,min_length=1)
    
    
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
        arbitrary_types_allowed=True   
        
    @classmethod
    #this is a decerator which is used to define a method that belongs to the class rather than an instance of the class. It allows you to call the method on the class itself, without needing to create an instance of the class first.
    def get_indexes(cls):
     # this is static method because it doesn't depend on the instance of the class, it is a method that belongs to the class itself and can be called without creating an instance of the class. It is used to define a method that can be called on the class itself, rather than on an  
     
     return [
         {
             "key":[
                 ("project_id",1)# which 1 indicate accending order and -1 indicate decending order
                 
             ],
             "name":"project_id_index_1",
             "unique":True
         }
         
     ]