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
        
        def genrate_random_string(self,length:int =12 ):
            letters_and_digits = string.ascii_letters + string.digits
            return ''.join(random.choice(letters_and_digits) for _ in range(length))
             
        