from .BaseDataModel import BaseDataModel
from .db_schemas import Project
from  .enums.DataBaseEnum import DataBaseEnum

class ProjectModel(BaseDataModel):
    def __init__(self,db_client:object):
        super().__init__(db_client= db_client)
        self.collection=self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value]
        
    async def create_project(self,project:Project):
        #now we will insert the project into the database and return the result of the insertion which is the id of the inserted document.
        result= await self.collection.insert_one(project.dict(by_alias=True,exclude_defaults=True))
        # as you see we are using the dict() method to convert the project object to a dictionary because the insert_one method expects a dictionary and the project its type is Project which is a pydantic model and it is not a dictionary so we need to convert it to a dictionary before inserting it to the database. 
        #by_alias=True means enable alias
        #now one important thing to notice here is  the cause of using motor which is an asynchronous driver for mongodb so we wrote  "await" before the insert_one method because it is an asynchronous method and we need to wait for it to complete before moving on to the next line of code.
        
        project.id=result.inserted_id
        return project
    
    async def get_project_or_create_one(self,project_id:str):
        
        record=await self.collection.find_one(
            {"project_id": project_id}
        )
        
        if record is None:
            # create new project
            project=Project(project_id=project_id)
            project= await self.create_project(project)
            
            return project
        
        
        # we know that the record use motor which returns a dictionary so we need to convert it to a Project object before returning it to the caller because the caller expects a Project object not a dictionary so we need to convert it
        # so we will write "**record" to unpack the dictionary and pass it as keyword arguments to the Project constructor to create a Project object from the dictionary and then return it to the caller.
        
        return Project(**record)
    
    async def get_all_projects(self,page:int=1,page_size:int=10):
        #we know that get all is good in the beginng but as the number of projects increases it will become a problem because it will return all the projects in the database which can be a lot and it can cause performance issues so we need to implement pagination 
        # pagination concept is to return a subset of the data instead of returning all the data at once so we will return a subset of the projects based on the "page" and "page_size" parameters which will be passed to the method by the caller and we will use the skip and limit methods of the motor to implement pagination.
        
        #count the total number of documents in the collection 
        total_documents= await self.collection.count_documents({})
        #count_douments is a method of the motor which returns the total number of documents in the collection and "({})" means that we want to count all the documents in the collection without any filter.
        
        #calculate total no of pages
        total_pages= total_documents // page_size 
        if total_documents % page_size > 0:
            total_pages += 1    
            
        # we will use the skip and limit methods of the motor to implement pagination and we will return a dictionary that contains the total number of pages and the list of projects for the current page.
        # cursor is an object that allows us to iterate over the results of the query and we will use the to_list method of the cursor to convert the cursor to a list of dictionaries and then we will convert each dictionary to a Project object and return the list of Project objects to the caller.   
        cursor=self.collection.find().skip((page-1)*page_size).limit(page_size)
        projects=[]
        async for document in cursor:
            projects.append(Project(**document))
            
        # we will return  total_pages to know the caller how many pages are there in total and the list of projects for the current page to display to the user.
                
        return projects , total_pages
        
                   
                
                