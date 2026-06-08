from fastapi import FastAPI
from routes import base,data
from  motor.motor_asyncio import AsyncIOMotorClient
# we will use motor to connect to mongodb because it is an asynchronous driver for mongodb and it is compatible with fastapi which is an asynchronous web framework.
from helpers.config import Settings
from src.stores import vectordb
from src.stores.llm.providers import CoHereProvider
from src.stores.llm.providers.OpenAIProvider import OpenAIProvider



from.stores.llm.LLMProvierFactory import LLMProvierFactory
from .stores.vectordb.VectorDBProviderFactory import VectorDBProviderFactory

app = FastAPI()

# there are many events in fastapi like:
#1- startup event: it is triggered when the application starts and is used to perform any initialization tasks, such as connecting to a database or setting up resources.
#2- shutdown event: it is triggered when the application is shutting down and is used to    perform any cleanup tasks, such as closing database connections or releasing resources.
#3- lifespan event: it is a combination of startup and shutdown events, it allows you to define a single function that will be called both when the application starts and when it shuts down. This can be useful for managing resources that need to be initialized and cleaned up in a specific order.
#4- exception event: it is triggered when an unhandled exception occurs in the application and is used to perform any error handling tasks, such as logging the error or returning a custom error response.
#5- request event: it is triggered for each incoming request and is used to perform any tasks that need to be done for each request, such as authentication or logging.
#6- response event: it is triggered for each outgoing response and is used to perform any tasks that need to be done for each response, such as adding headers or logging.
#7- websocket event: it is triggered for each incoming websocket connection and is used to perform any tasks that need to be done for each websocket connection, such as authentication or logging.
#8- background task event: it is triggered for each background task and is used to perform any tasks that need to be done for each background task, such as logging or error handling.
#9- lifecycle event: it is a combination of startup, shutdown, and exception events, it allows you to define a single function that will be called for all three events. This can be useful for managing resources that need to be initialized, cleaned up, and handled in case of errors in a specific order.
#10- custom event: you can also define your own custom events and trigger them at specific points in your application, such as after a specific action is performed or when a certain condition is met.
#11- so these events are very useful for managing the lifecycle of your application and performing tasks that need to be done at specific points in the application's execution.
#@app.on_event("startup")

async def startup_span():
    settings=Settings()
    app.mongo_conn=AsyncIOMotorClient(settings.MONGO_URI)
    app.db_client=app.mongo_conn[settings.MONGO_DB_NAME]
    
    llm_provider_factory=LLMProvierFactory(settings)
    
    vectordb_provider_factory=VectorDBProviderFactory(settings)
    
    #Generation model
    app.generation_client=llm_provider_factory.creat(provider=settings.GENERATION_BACKEND)
    app.generation_client.set_generate_model(model_id=settings.GENERATION_MODEL_ID)
    
    
    #Embedding model
    app.embedding_client=LLMProvierFactory.creat(provider=settings.EMBEDDING_BACKEND)
    app.embedding_client.set_embedding_model(model_id=settings.EMBEDDING_MODEL_ID,embedding_size=settings.EMBEDDING_MODEL_SIZE)
    
    #vector_db client
    app.vectordb_client= vectordb_provider_factory.create(provider=settings.VECTOR_DB_BACKEND)
    app.vectordb_client.connect()
    
    
#@app.on_event("shutdown")
async def shutdown_span():
    app.mongo_conn.close()    
    app.vectordb_client.disconnect()
    
app.router.lifespan.on_startup.append(startup_span)
app.router.lifespan.on_shutdown.append(shutdown_span)

app.include_router(base.base_router)
app.include_router(data.data_router)

