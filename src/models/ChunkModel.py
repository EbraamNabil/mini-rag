from .BaseDataModel import BaseDataModel
from .db_schemas import DataChunk
from  .enums.DataBaseEnum import DataBaseEnum
from  bson import ObjectId
from  pymongo import InsertOne
from typing import Dict

class ChunkModel(BaseDataModel):
    def __init__(self,db_client:object):
        super().__init__(db_client= db_client)
        self.collection=self.db_client[DataBaseEnum.COLLECTION_CHUNK_NAME.value]
        
    @classmethod
    #we make this method a class method because we need to call "init_collection" (which is async method) with "__init__" which is not async method and will make error because you can't call an async method from a non-async method so we will make "create_instances" a class method and call "init_collection" from it to avoid this problem and we will call "create_instances" from the data.py when the application starts to initialize the collection and create the indexes.
    async def create_instances(cls,db_client:object):
        instance=cls(db_client=db_client)
        await instance.init_collection()
        return instance 
    
    
       
    async def init_collection(self):
         all_collections=await self.db_client.list_collection_names()   
         if DataBaseEnum.COLLECTION_CHUNK_NAME.value not in all_collections:
              self.collection=self.db_client[DataBaseEnum.COLLECTION_CHUNK_NAME.value]
              indexes=DataChunk.get_indexes()
              for index in indexes:
                  await self.collection.create_index(index["key"]
                                                     ,name=index["name"],
                                                     unique=index["unique"])    
        
        
        
        
        
        
    async def create_chunk(self,chunk:DataChunk):     
        result= await self.collection.insert_one(chunk.dict(by_alias=True,exclude_defaults=True))
        
        chunk.id=result.inserted_id
        return chunk
    
    async def get_chunks(self,chunk_id:str):
       #when you enter motor turn the string id to ObjectId because the id in the database is stored as ObjectId and we need to convert it to ObjectId before querying the database
       #  when you exit from motor you need to convert the ObjectId to string because the ObjectId is not JSON serializable and we need to convert it to string before returning it to the caller 
       
       result=await self.collection.find_one({
           
            "_id": ObjectId(chunk_id)
       })
       
       if result is None:
           return None
       
       return DataChunk(**result)
   
   # it is difficult to insert chunck one by one because it will cause performance issues
   #so we will use bulk write or batch write to insert some  chunks at once to improve the performance and reduce the number of database calls
   #so we do that by "from  pymongo import InsertOne" 
   #and there is difference between insert_one and InsertOne .the insert_one is a method of the motor collection that inserts one document to the database and returns the result of the insertion  and the InsertOne is a class that represents an insert operation that can be used in the bulk write operation to insert multiple documents at once to the database (يعنى بتوصفلك شكل الداتا الللى هتدخل) 
   
    async def insert_many_chunks(self,chunks:list,batch_size:int=100):
        
        for i in range(0,len(chunks),batch_size):
            batch=chunks[i:i+batch_size]
            
            operations=[
                InsertOne(chunk.dict(by_alias=True,exclude_defaults=True))
                # we used InsertOne to represent the form of data which will be inserted
                for chunk in batch
                
            ]
            
            
            await self.collection.bulk_write(operations)
            
            # the worst seanrio is  we dont use "bulk_write" and use "insert_many" which insert all data at once
            
            
        return len(chunks)  
    
    async def delete_chuncks_by_id(self,project_id:ObjectId):
        result=await self.collection.delete_many(
            {"chunk_project_id":project_id}
        )
        
        return result.deleted_count
   
   
         