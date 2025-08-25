from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict

# Import the core logic
from core_logic import get_ai_response

# Import CORS middleware
from fastapi.middleware.cors import CORSMiddleware

# Initialize the FastAPI app
app = FastAPI(
    title="AI Character API",
    description="An API to chat with AI characters.",
    version="1.0.0"
)

# Configure CORS
# This allows the frontend (which will be on a different "origin") to communicate with the API.
origins = [
    "*",  # In a real production environment, you would restrict this to your frontend's domain.
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# --- Pydantic Models for Request and Response ---

class ChatRequest(BaseModel):
    character_prompt: str
    user_message: str
    conversation_history: List[Dict[str, str]]

class ChatResponse(BaseModel):
    ai_message: str

# --- API Endpoints ---

@app.get("/", summary="Check API Status")
def read_root():
    """A simple root endpoint to check if the server is running."""
    return {"status": "AI Character API is running!"}

@app.post("/chat", response_model=ChatResponse, summary="Chat with an AI character")
async def chat_with_character(request: ChatRequest):
    """
    Receives a chat message, character prompt, and conversation history,
    then returns the AI's response.
    """
    ai_message = get_ai_response(
        request.character_prompt,
        request.user_message,
        request.conversation_history
    )
    return ChatResponse(ai_message=ai_message)
