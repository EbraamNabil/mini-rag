
from controllers.BaseController import BaseController
from fastapi import UploadFile
from models import  ResponseSignal

class DataController(BaseController):
    def __init__(self):
        super().__init__()
        self.size_scale=1024*1024  # 1 MB
    
    def validate_file(self,file:UploadFile):
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False,ResponseSignal.File_TYPE_NOT_SUPPORTED.value
        if file.size > self.app_settings.FILE_MAX_SIZE * self.size_scale:
            return False,ResponseSignal.File_SIZE_EXCEEDS.value
        
        return True,ResponseSignal.FILE_VALIDATION_SUCSESS.value