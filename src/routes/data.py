from fastapi import APIRouter , FastAPI, Depends,UploadFile
from helpers.config import get_settings,Settings
import os
from controllers import DataController

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1", "data"]
)

@data_router.post("/upload/{project_id}")
async def upload_data(project_id: str,file:UploadFile,
                      
                     app_settings : Settings = Depends(get_settings) 
                      
                      ):
    
  # 1. Validate file type and size  
    
    is_vaid = DataController().validate_file(file=file)
    
    return is_vaid