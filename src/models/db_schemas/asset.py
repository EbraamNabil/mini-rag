from pydantic import BaseModel, Field,validator
from typing import  Optional
from bson import ObjectId
from datetime import datetime

class Asset(BaseModel):
    id: Optional[ObjectId]=Field(None,alias="_id")
    
    asset_project_id:ObjectId 
    asset_type:str=Field(...,min_length=1)
    asset_name:str=Field(...,min_length=1)
    asset_size:int=Field(gt=0,default=None)
    asset_config:dict=Field(default=None)
    asset_pushed_at:datetime=Field(default=datetime.utcnow())
    
    class Config:
        arbitrary_types_allowed = True
        
    @classmethod
    #this is a decerator which is used to define a method that belongs to the class rather than an instance of the class. It allows you to call the method on the class itself, without needing to create an instance of the class first.
    def get_indexes(cls):  
        return [
            {
                "key":[
                    ("asset_project_id",1 )],
                "name":"asset_project_id_index_1",
                 "unique":False 
                 #Now we make index on asset_project_id because we want to make sure that the asset 
                 #because may more than one asset can have the same project id so we set unique to false
                 } ,
            {
                "key":[
                    ("asset_project_id",1 ),
                    ("asset_name",1)
                    ],
                    
                "name":"asset_project_id_name_index_1",
                 "unique":False 
                 #Now we make index on both asset_project_id and asset_name because we want to make sure that the combination of asset_project_id and asset_name is unique
                 } ,
            
        ]