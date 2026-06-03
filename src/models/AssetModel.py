from .BaseDataModel import BaseDataModel
from .db_schemas import Asset
from  .enums.DataBaseEnum import DataBaseEnum
from bson import ObjectId


class AssetModel(BaseDataModel):
    def __init__(self,db_client:object):
        super().__init__(db_client= db_client)
        self.collection=self.db_client[DataBaseEnum.COLLECTION_ASSET_NAME.value]

    @classmethod
    #we make this method a class method because we need to call "init_collection" ( which is async method) with "__init__" which is not async method and will make error because you can't call an async method from a non-async method so we will make "create_instances" a class method and call "init_collection" from it to avoid this problem and we will call "create_instances" from the data.py when the application starts to initialize the collection and create the indexes.
    async def create_instances(cls,db_client:object):
        instance=csl(db_client=db_client)
        await instance.init_collection() 
        return instance
    
    async def init_collection(self):
         all_collections=await self.db_client.list_collection_names()   
         if DataBaseEnum.COLLECTION_ASSET_NAME.value not in all_collections:
              self.collection=self.db_client[DataBaseEnum.COLLECTION_ASSET_NAME.value]
              indexes=Asset.get_indexes()
              for index in indexes:
                  await self.collection.create_index(index["key"]
                                                     ,name=index["name"],
                                                     unique=index["unique"])



    async def create_asset(self,asset:Asset):
            #now we will insert the asset into the database and return the result of the insertion which is the id of the inserted document.
            result= await self.collection.insert_one(asset.dict(by_alias=True,exclude_defaults=True))
            # as you see we are using the dict() method to convert the asset object to a dictionary because the insert_one method expects a dictionary and the asset its type is Asset which is a pydantic model and it is not a dictionary so we need to convert it to a dictionary before inserting it to the database. 
            #by_alias=True means enable alias
            #now one important thing to notice here is  the cause of using motor which is an asynchronous driver for mongodb so we wrote  "await" before the insert_one method because it is an asynchronous method and we need to wait for it to complete before moving on to the next line of code.
            
            asset.id=result.inserted_id
            return asset
        
        
    async def get_all_project_assets(self,asset_project_id:str):
        
        return await self.collection.find(
            {
                
                "asset_project_id": ObjectId(asset_project_id) if isinstance(asset_project_id, str) else asset_project_id
              # because the asset_project_id is of type ObjectId in the database but it can be passed as a string from the caller so we need to convert it to ObjectId before querying the database 
              # and we also need to check if the asset_project_id is already an ObjectId or not because if it is already an ObjectId we don't need to convert it again and if it is a string we need to convert it to ObjectId before querying the database
              #so we used "isinstance"which is a built-in function in Python that checks if an object is an instance of a specified class or a subclass thereof. In this case, we are checking if the asset_project_id is an instance of the str class, which means it is a string. If it is a string, we convert it to an ObjectId using the ObjectId constructor. If it is not a string (i.e., it is already an ObjectId), we use it as is in the query.
            }.to_list(length=None)
               
        ) 
        
        
    
    
    


            
        