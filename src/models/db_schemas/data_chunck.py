from pydantic import BaseModel, Field
from  bson import ObjectId
from typing import Optional

class DataChunk(BaseModel):
    id: Optional[ObjectId]=Field(None,alias="_id")
    chunk_text: str=Field(...,min_length=1)
    chunk_metadata: dict
    chunk_order: int=Field(...,ge=0) #ge means greater than or equal to 0 because the chunk order should start from 0 and be a positive integer
    chunk_project_id:Optional[ObjectId]=None #this field is used to link the chunk to the project in the database(project.py), it is optional because we will set it after we insert the chunk to the database and get its id
    chunk_asset_id:ObjectId #this field is used to link the chunk to the asset in the database(asset.py), it is not optional because we need to set it before we insert the chunk to the database because we need to know which asset this chunk belongs to in order to link it to the project and also to be able to query the chunks by asset id later on when we want to retrieve the chunks for a specific asset or project
    class Config:
        arbitrary_types_allowed = True
        
    @classmethod
    #this is a decerator which is used to define a method that belongs to the class rather than an instance of the class. It allows you to call the method on the class itself, without needing to create an instance of the class first.
    def get_indexes(cls):  
        return [
            {
                "key":[
                    ("chunk_project_id",1 )],
                "name":"chunk_project_id_index_1",
                 "unique":False 
                 #because may more than one chunk can have the same project id so we set unique to false
                 } 
        ]