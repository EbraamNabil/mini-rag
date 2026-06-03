from enum import Enum

class ResponseSignal(Enum):
    
    
    FILE_VALIDATION_SUCSESS="file_validation_success"
    File_TYPE_NOT_SUPPORTED ="file_type_not_supported"
    File_SIZE_EXCEEDS="file_size_exceeds"
    File_UPLOAD_SUCCESS="file_upload_success"
    File_UPLOAD_FAILED="file_upload_failed"
    File_PROCESSING_SUCCESS="file_processing_success"
    File_PROCESSING_FAILED="file_processing_failed"
    NO_FILES_ERROR="no_files_error"
    