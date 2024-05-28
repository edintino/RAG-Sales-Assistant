from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from embedding_system import EmbeddingSystem

# Initialize FastAPI app
app = FastAPI()

# Load the embedding system
system = EmbeddingSystem('gamestop_data_2021_12.csv')
chat_engine = system.get_chat_engine()

class Query(BaseModel):
    question: str

@app.post("/chat")
def chat(query: Query):
    """
    Query the chat engine with a given question.
    
    Args:
        query (Query): A JSON object with a question string.
    
    Returns:
        dict: A JSON object with the response from the chat engine.
    """
    try:
        response = chat_engine.chat(query.question)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/reset")
def reset_chat():
    """
    Reset the chat history.
    
    Returns:
        dict: A JSON object confirming the reset action.
    """
    try:
        chat_engine.reset()  # Reinitialize the chat engine
        return {"message": "Chat history has been reset."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Example endpoint to test the server
@app.get("/")
def read_root():
    return {"message": "Welcome to the RAG Sales Assistant API"}