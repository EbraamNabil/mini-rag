from abc import ABC, abstractmethod
#abc is the Abstract Base Class module in Python, which provides a way to define abstract classes(interfaces) and methods.

class LLMInterface(ABC):
    
    @abstractmethod
    # The @abstractmethod decorator indicates that this method must be implemented by any subclass of LLMInterface.
    def set_generate_model(self,model_id:str):
        pass
    
    @abstractmethod
    def set_embedding_model(self,model_id:str,embedding_size:int):
        pass
    
    @abstractmethod
    def generate_text(self,prompt:str,max_output_tokens:int=None,chat_history:list=[],
                      temperature:float=None):
        pass
    
    @abstractmethod
    def embed_text(self,text:str,document_type:str=None):
        # The embed_text method is an abstract method that takes a text string and a document type as input and returns an embedding vector. The document_type parameter can be used to specify the type of document being embedded (which can be   query or Answer(piece of text)  ), which may affect how the embedding is generated.
        pass 
        
        
    @abstractmethod
    def construct_prompt(self,prompt:str,role:str):
        # The construct_prompt method is an abstract method that takes a prompt string and a role string as input and returns a constructed prompt. The role parameter can be used to specify the role of the prompt (which can be either "user" or "assistant"), which may affect how the prompt is constructed.
        pass    
    
    