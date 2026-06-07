from ast import Pass

from .providers.OpenAIProvider import OpenAIProvider
from .providers.CoHereProvider import CoHereProvider
from LLMEnums import LLMEnums


class LLMProvierFactory():
   def __init__(self,config:dict) :
       self.config=config
       
   def creat(self,provider:str):   
        if provider== LLMEnums.OPENAI.value:
            return OpenAIProvider(
              api_key= self.config.OPENAI_API_KEY,
              api_url=self.config.OPENAI_API_URL,
              default_input_max_characters=self.config.IMPUT_DEFAULT_MAX_CHARACTERS,
              default_output_max_tokens=self.config.GENERATION_DEFAULT_MAX_TOKENS,
              default_temperature=self.config.GENERATION_DEFAULT_TEMPERATURE,
                
                
            )
            
        if provider== LLMEnums.COHERE.value:    
          return CoHereProvider(
              api_key= self.config.COHERE_API_KEY,
              default_input_max_characters=self.config.IMPUT_DEFAULT_MAX_CHARACTERS,
              default_output_max_tokens=self.config.GENERATION_DEFAULT_MAX_TOKENS,
              default_temperature=self.config.GENERATION_DEFAULT_TEMPERATURE ,
              
          )
          
          
        return None  