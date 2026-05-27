from fastapi import APIRouter , FastAPI, Depends,UploadFile,status
from fastapi.responses import JSONResponse 
from helpers.config import get_settings,Settings
import os
from controllers import DataController,ProjectController,ProcessController
import aiofiles
from models import  ResponseSignal
import logging
from .schemas.data import ProcessRequest
from models.ProjectModel import ProjectModel
from models.ChunkModel import ChunkModel

# we will import the Request class from fastapi to be able to access the request object in our route handlers"app"and we will use the request object to access the application state and get the database client that we initialized in the startup event of our application in main.py so we can use it to interact with the database in our route handlers data.py
from fastapi import Request
from models.db_schemas import DataChunk
from models.db_schemas import Project 
from  bson import ObjectId




logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
    
)

logger = logging.getLogger('uvicorn.error')

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1", "data"]
)

@data_router.post("/upload/{project_id}")
async def upload_data(request: Request,project_id: str,file:UploadFile,
                      
                     app_settings : Settings = Depends(get_settings) 
                      
                      ):
    
    
    
    project_model=ProjectModel(db_client=request.app.db_client)
    project= await project_model.get_project_or_create_one(
        project_id=project_id
        )
    
    
  # 1. Validate file type and size  
    
    is_vaid ,result_signal = DataController().validate_file(file=file)
    
    if not is_vaid:
        return JSONResponse(
            
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
            "signal":result_signal
        }
            )
        
       
    project_dir_path=ProjectController().get_project_path(project_id=project_id)
    file_path,file_id=DataController().generate_unique_filepath(orig_file_name=file.filename,project_id=project_id)
     
    try:    
        async with aiofiles.open(file_path,'wb') as f : #we choose to write binary to write any type of file (vedio, audio, pdf, txt, etc.)
            while chunck := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                    await f.write(chunck)
    except Exception as e:
        
        logger.error(f"Error uploading file: {str(e)}")
        return JSONResponse(
            
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
            "signal":ResponseSignal.File_UPLOAD_FAILED.value,
            
        }
            )                
            
    return JSONResponse(
            
            content={
            "signal":ResponseSignal.File_UPLOAD_SUCCESS.value,
            "file_id":file_id,
        }
            )    
    
 
@data_router.post("/process/{project_id}")    
async def process_data(request: Request, project_id: str, process_request: ProcessRequest):
    
    file_id=process_request.file_id
    chunk_size=process_request.chunk_size
    overlap_size=process_request.overlap_size
    do_reset=process_request.do_reset
    
    
    project_model=ProjectModel(db_client=request.app.db_client)
    project= await project_model.get_project_or_create_one(project_id=project_id)
    

    
    process_controller=ProcessController(project_id=project_id)
    file_content=process_controller.get_file_content(file_id=file_id)
    file_chunks=process_controller.process_file_content(
        file_id=file_id,
        file_content=file_content,
        chunk_size=chunk_size,
        overlap_size=overlap_size
        )
        
    
    
    if file_chunks is None or len(file_chunks)==0:
        return JSONResponse(
            
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
            "signal":ResponseSignal.File_PROCESSING_FAILED.value,
            
        }
            )
    
    
    
    file_chuncks_records=[
        DataChunk(
            chunk_text=chunk.page_content,
            chunk_metadata=chunk.metadata,
            chunk_order= i+1,
            chunk_project_id= project.id,
            )
        
        for i,chunk in enumerate(file_chunks)
    ]    
    
    
    chunck_model=ChunkModel(db_client=request.app.db_client)

    
    if do_reset==1 :
        _ = await chunck_model.delete_chuncks_by_id(
            project_id=project.id
        )    
        
    
    no_records= await chunck_model.insert_many_chunks(chunks=file_chuncks_records)
    
    return JSONResponse(
        content={
            "signal":ResponseSignal.File_PROCESSING_SUCCESS.value,
                "inserted_chuncks":no_records
        }
        
    )
    

          