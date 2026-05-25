from fastapi import APIRouter , FastAPI, Depends,UploadFile,status
from fastapi.responses import JSONResponse 
from helpers.config import get_settings,Settings
import os
from controllers import DataController,ProjectController
import aiofiles
from models import  ResponseSignal
import logging

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
async def upload_data(project_id: str,file:UploadFile,
                      
                     app_settings : Settings = Depends(get_settings) 
                      
                      ):
    
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
            "file_id":file_id
        }
            )    