import logging
from ..LLMInterface import LLMInterface
from ..LLMEnums import OpenAiEnums
from openai import OpenAI


class OpenAIProvider(LLMInterface):
    
    def __init__(self, api_key: str ,
         #api_url is optional because if the user want to use the default openai api url he can just provide the api key and if he want to use custom api url  (like in the case of ollama )he can provide the api url as well

                       api_url:str=None,
                       default_input_max_characters:int=1000,
                        default_output_max_tokens : int=1000,
                        default_temperature:float=0.1):
        
        self.api_key=api_key
        self.api_url=api_url
        self.default_input_max_characters=default_input_max_characters
        self.default_output_max_tokens=default_output_max_tokens
        self.default_temperature=default_temperature
        
        
        # now we define some variables to hold the current generating model and embedding model and embedding size (because we need it when we want to generate embedding for the chunks to know the size of the embedding vector)
        self.generating_model_id=None
        #we dont put it in the constructor (__init__) parameters because we want the user to be able to change it later by using the set_generate_model method  in the runtime if we put it in init we cant change it later because it will be fixed when we create the instance of the OpenAIProvider class but by using the set_generate_model method we can change it later in the runtime
        self.embedding_model_id=None
        self.embedding_size=None
        
        self.client=OpenAI(
            api_key=self.api_key,
            api_url=self.api_url
            )
        
        self.logger=logging.getLogger(__name__)
        # we will use this logger to log any error that may occur 
        #by using the __name__ variable we can know which file the error occurred in and this will help us to debug the error more easily
        
        def set_generate_model(self, model_id: str):
            self.generating_model_id=model_id
            
        def set_embedding_model(self, model_id: str, embedding_size: int):
            self.embedding_model_id=model_id
            self.embedding_size=embedding_size
            
        def process_text(self,text:str):
            # this is helper method which isnt put in interface because not all providers will use it but this provider only
            return text[:self.default_input_max_characters].strip()   
             # strip used to delete any spaces in the begining or end
        
        
        def generate_text(self, prompt: str, max_output_tokens: int = None,
                          temperature: float = None, chat_history: list = []): 
              if not self.client:
                self.logger.error("The OpenAI client is not initialized")
                return None
            
              if not self.generating_model_id:
                self.logger.error("The generating model for openai is not set")
                return None
            
            
              
              max_output_tokens = max_output_tokens if max_output_tokens is not None else self.default_output_max_tokens
              
              temperature = temperature if temperature is not None else self.default_temperature
              
              chat_history .append(
                  self.construct_prompt(prompt=prompt,role=OpenAiEnums.USER.value)
                  # even chat history is empty we will add the user prompt to the chat history because openai need to have the user prompt in the chat history to be able to generate a response  
              )
              
              response = self.client.chat.completions.create(
                  model=self.generating_model_id,
                  messages=chat_history,
                  max_tokens=max_output_tokens,
                  temperature=temperature
              )
              
              if not response or not response.choices or len(response.choices) == 0:
                    self.logger.error("The response from OpenAI is empty")
                    return None
                
              return response.choices[0].message["content"]  
                
             # "raise NotImplementedError("The generate_text method is not implemented yet")"
             #some times you will use embedding model but you dont want to use the generate text method but you have to implement it because it is an abstract method 
             #so until now we can skip the implementation of this method by raising NotImplementedError and we will implement it later when we need it in the future when we want to use the generate text method in our application
        
        
        def embed_text(self, text: str, document_type: str=None):     
            if not self.client:
              #we want to make validation to check if the client is initialized or not because if the client is not initialized it means that there is an error in the initialization of the OpenAIProvider class and we want to log this error and raise an exception to notify the user about this error 
              # we can do that by using  2 metods 1. logging the error using the logger that we defined in the constructor (this is the better solution to avoid to break the application ) and  2. raising an exception to notify the user about this error  
              self.logger.error("The OpenAI client is not initialized")
              return None
            
            if not self.embedding_model_id :
                self.logger.error("The embedding model is not set")
                return None
            
            response =self.client.embeddings.create(
            model=self.embedding_model_id,
            input=text
        
            )
            if not response or not response.data or len(response.data) == 0:
                self.logger.error("The embedding response is empty")
                return None 
            
            return response.data[0].embedding 
        
        
        def construct_prompt(self, prompt: str, role: str):
           #we used this method to hekp openai to understand the role of the prompt (whether it is a user prompt or an assistant prompt) because openai use this information to generate better response and  content for the user and assistant prompts and this is important to improve the performance of the model   
           #for example:
           #messages=[ {role:"assistant",content:"You are a helpful assistant that helps the user "} ,
           # {role:"user",content:"what is the capital of france?"} ,
           # {role:"assistant",content:"the capital of france is paris"}
           #  {"role":"user","content":"what is the population of paris?"}   
           #]
           
            return {
                "role":role,
                "content": self.process_text(prompt)
            }
        
            
            