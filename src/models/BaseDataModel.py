from helpers.config import Settings, get_settings

class BaseDataModel:
    def __init__(self,db_client:object):
        #object is a data type that is the base class for all classes in python, it is used to indicate that the parameter can be of any type.
        self.db_client=db_client
        self.app_settings=get_settings()
        