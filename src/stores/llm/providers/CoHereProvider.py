from ..LLMInterface import LLMInterface
from ..LLMEnums import CohereEnums,DocumentTypeEnum
import cohere 
import logging


class CoHereProvider(LLMInterface):
    
    def __init__(self, api_key: str ,
        # Here cohere dont use apt_url
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
        
        self.client=cohere.Client(api_key=self.api_key)
        
        self.logger=logging.getLogger(__name__)
        
        
    def set_generate_model(self, model_id: str):
        self.generating_model_id=model_id
        
    def set_embedding_model(self, model_id: str, embedding_size: int):
        self.embedding_model_id=model_id
        self.embedding_size=embedding_size
        
    def process_text(self,text:str):
        # this is helper method which isnt put in interface because not all providers will use it but this provider only
        return text[:self.default_input_max_characters].strip()     
    
    def generate_text(self, prompt: str, max_output_tokens: int = None,
                        temperature: float = None, chat_history: list = []): 
        if not self.client:
            self.logger.error("The OpenAI client is not initialized")
            return None
    
        if not self.generating_model_id:
            self.logger.error("The generating model for openai is not set")
            return None
        
        response = self.client.chat(
                model=self.generating_model_id,
                chat_history=chat_history,
                message=self.process_text(prompt),
                temperature=temperature,
                max_tokens=max_output_tokens
                
                
                )
        
        if not response or not response.text:
            self.logger.error("Error while generating text witk coHere")
        
        
        
        max_output_tokens = max_output_tokens if max_output_tokens is not None else self.default_output_max_tokens
            
        temperature = temperature if temperature is not None else self.default_temperature
            
        return response.text
    
        
            
    def embed_text(self,text:str,document_type:str=None):
        # The embed_text method is an abstract method that takes a text string and a document type as input and returns an embedding vector. The document_type parameter can be used to specify the type of document being embedded (which can be   query or Answer(piece of text)  ), which may affect how the embedding is generated.
            
        if not self.client:
            self.logger.error("The OpenAI client is not initialized")
            return None
    
        if not self.embedding_model_id:
            self.logger.error("The embedding model for openai is not set")
            return None
        
        input_type=CohereEnums.DOCUMENT.value
        if document_type==DocumentTypeEnum.QUERY:
            input_type=CohereEnums.QUERY.value
            
        response=self.client.embed(
            model=self.embedding_model_id,
            texts=[self.process_text(text)],
            input_type=input_type,
            embedding_types=["float"],
        )
        
    
        if not response or not response.embeddings or not response.embeddings.float:
                self.logger.error("The response from CoHere is empty")
                return None              
        
    def construct_prompt(self, prompt: str, role: str):
        # in cohere V1 : "
        # response co.chat(
        # model-command-r-plus",
        # chat history-[
        # ("cole": "USER", "text": "Hey, my name is Michaell"),
        # ("role": "CHATBOT", "text": "Hey Michael! How can I help you today?"),
        # ],
        # message"Can you tell me about LEMS?"
        # )
        # print(response.text)# "Sure thing Michael, US are..."
        # V2 is similar to openai (There isn't chat_history but only messages)
        return {
            "role":role,
            "text": self.process_text(prompt)
        }    
    



