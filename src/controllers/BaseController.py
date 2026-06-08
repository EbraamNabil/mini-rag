from helpers.config import get_settings
import os
import random
import string
class BaseController:
    def __init__(self):
        self.app_settings = get_settings()
        self.base_dir=os.path.dirname(os.path.dirname(__file__))
        self.file_dir=os.path.join(
            self.base_dir,
            "assets/files"
        )
        
        self.database_dir=os.path.join(
            self.base_dir,
          "assets/database"  
        )
        
        def genrate_random_string(self,length:int =12 ):
            letters_and_digits = string.ascii_letters + string.digits
            return ''.join(random.choice(letters_and_digits) for _ in range(length))
         
        
        
        def get_database_path(sekf,db_name:str):
            database_path=os.path.join(
                self.database_dir,db_name
            )
            
            if not os.path.exsists(database_path) :   
                os.makedirs (database_path)
                return  database_path
            
            return database_path
        
            
            