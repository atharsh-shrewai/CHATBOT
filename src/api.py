from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from main import get_response

# Create the FastAPI app

app = FastAPI(
    title="Chatbot API",
    description="A simple API to interact with the chatbot",
)

# CORS Middleware 

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,

)

# Request body model

class QuestionRequest(BaseModel):
    question: str

# APIs

# Health check endpoint
@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}


# Chatbot endpoint
@app.post("/chat", tags=["Chatbot"])
def chat(request: QuestionRequest):
    try:
        response = get_response(request.question)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


