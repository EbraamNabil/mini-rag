from .BaseController import BaseController
from .projectConroller import ProjectController
import os
from langchain.document_loaders import TextLoader, PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from models import ProcessingEnum


class ProcessController(BaseController):
    def __init__(self, project_id:str):
        super().__init__()
        
        self.project_id=project_id
        self.project_path=ProjectController().get_project_path(project_id=project_id)

    def get_file_extension(self,file_id:str):
        return os.path.splitext(file_id)[-1].lower()
    
    def get_file_loader(self,file_id:str):
        
        file_ext= self.get_file_extension(file_id=file_id) 
        file_path=os.path.join(
            self.project_path,
            file_id
        )
        
        print("FILE PATH =", file_path)
        print("EXISTS =", os.path.exists(file_path))
        
        print("EXTENSION =", file_ext)
        print("TXT =", ProcessingEnum.TXT.value)
        print("PDF =", ProcessingEnum.PDF.value)

        if file_ext==ProcessingEnum.TXT.value:
            return TextLoader(file_path,encoding='utf-8')
        
        if file_ext==ProcessingEnum.PDF.value:
            return PyMuPDFLoader(file_path)
        
        
        
        return None
    
    def get_file_content(self,file_id:str):
        loader=self.get_file_loader(file_id=file_id)
        return loader.load()
    
    def process_file_content(self,file_id:str,file_content:list,
                             chunk_size:int=100,overlap_size:int=20):
        text_splitter=RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap_size,
            length_function=len
            )
        file_content_texts=[
            rec.page_content # i will take only the page content for now, but we can also take metadata and other info if needed
            for rec in file_content
        ]
        
        file_content_metadata=[
            rec.metadata
            for rec in file_content 
        ]
        
        chunks=text_splitter.create_documents(
          file_content_texts,
          metadatas=file_content_metadata
            
        )
        
        return chunks
        
         
         
        
        
    
