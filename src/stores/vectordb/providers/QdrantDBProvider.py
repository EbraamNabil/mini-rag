from math import e

from qdrant_client import QdrantClient,models
from typing import List

from ..VectorDBInterface import VectorDBInterface
from ..VectorDBEnums import DistanceMethodEnums
import logging

class QdrantDBProvider(VectorDBInterface):
    def __init__(self,db_path:str,distance_method:str):
        
        
        
        self.client=None
        self.db_path=db_path
        self.distance_method=distance_method
        
        if distance_method==DistanceMethodEnums.COSINE.value:
            self.distance_method=models.Distance.COSINE
        
        elif distance_method==DistanceMethodEnums.DOT.value:
             self.distance_method=models.Distance.DOT
        
        
        self.logger=logging.getLogger(__name__) 
        
        
    def connect(self):
        self.client = QdrantClient(path=self.db_path) 
     
     
     #there isn't self.clientin disconnect
    def disconnect(self):
        self.client=None
        self.client = QdrantClient(path=self.db_path)    
             
    def is_collection_existed(self,collection_name:str)->bool:
        return  self.client.collection_exists(collection_name=collection_name)
    
    def list_all_collection(self)->List:
        return  self.client.get_collections()
    
    def get_collection_info(self,collection_name:str)->dict:
        return   self.client.get_collection(collection_name=collection_name)
    
    def delete_collection(self,collection_name:str):
        if self.is_collection_existed(collection_name=collection_name):
          return  self.client.delete_collection(collection_name=collection_name)

    def create_collection(self,collection_name:str,
                               embedding_size:int,
                               do_reset:bool=False):
        
        if do_reset:
            _=self.delete_collection(collection_name=collection_name)
        
        if not self.is_collection_existed (collection_name):
            _=self.client.create_collection(
                collection_name=collection_name
                vectors_config=models.VectorParams(size=embedding_size, 
                                        distance=self.distance_method,)
                
            )
            
            return True
     
        return False     
        
     
    def insert_one(self,collection_name:str,
                               text:str,
                               vector:list,
                               metadata:dict=None,
                               recoed_id:str=None):
       
        if not self.is_collection_existed:
            self.logger=logging.getLogger("can't isert new record to non existed collection")
            return False
        
        try:
            _=self.client.upload_records(
                collection_name=collection_name,
                records=[
                    models.Record(
                    vector=vector ,
                    payload={
                        "text":text,"metadata":metadata
                    }
                    )
                ]
                
                
            )
        except Exception as e :
                
             self.logger=logging.getLogger(f"ERROR whike inserting one record:{e}")
             return False
       
        return True
    
    def insert_many(self,collection_name:str,
                               texts:List,
                               vectors:list,
                               metadata:List=None,
                               recoed_ids:str=None,
                               batch_size:int=50):
    
    #we need to make metadata list of values and if it none we will convert it to list of nonvalues because we need bastc size compatible with them
        if metadata is None:
            metadata=[None]*len(texts)
            
        if recoed_ids is None:
            recoed_ids=[None]*len(texts)    
            
        for i in range (0,len(texts),batch_size):  
              batch_end=i+batch_size
              batch_texts=texts[i:batch_end]
              batch_vectors=vectors[i:batch_end]
              batch_metadata=metadata[i:batch_end]
              
              batch_records=[
                  
                  models.Record(
                   vector=batch_vectors ,
                   payload={
                       "text":batch_texts,"metadata":batch_metadata
                   }
                )
                  
                  for x in range(len(batch_texts))
                  
                ]
              
              try:
                    _=self.client.upload_records(
                    collection_name=collection_name,
                    records=batch_records)

              except Exception as e:
                    self.logger=logging.getLogger(f"ERROR whike inserting batch:{e}")

              
              
        return True  
    
    
    
    def search_by_vector(self,collection_name:str,
                               vector:list,
                               limit:int=5
                               ):
        
        return self.client.search(
            collection_name=collection_name,
            query_vector=vector,
            limit=limit
        )
    
    
         