from enum import Enum
from winreg import EnumValue

class LLMEnums(Enum):
    OPENAI = "openai"
    COHERE = "cohere"
    
    
class OpenAiEnums(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"  
    
    
class CohereEnums(Enum):
    SYSTEM = "SYSTEM"
    USER = "USER"
    ASSISTANT = "CHATBOT"
    
    
   #the type of the input in CoHere
    DOCUMENT="search_document"
    QUERY="search_query"            

    
class DocumentTypeEnum(Enum) :
    #the type of the input in general
      DOCUMENT="document"
      QUERY="query"            
    
       