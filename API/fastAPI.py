from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from chatbot import chatbot
from pydantic import BaseModel
from typing import Optional, List
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class Message(BaseModel):
    role: str
    content: str
class ChatRequest(BaseModel):
    message: str
    convoHistory: Optional[List[Message]] = None
class ChatResponse(BaseModel):
    response: str
    convoHistory: List[Message]


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("chatbot", response_model=ChatResponse)
def chat(request: ChatRequest):

    try:
        convoHistory = [dict(message) for message in (request.convoHistory or [])]

        responseText = chatbot(request.message, convoHistory)

        updatedHistory = (request.convoHistory or []).copy()
        updatedHistory.append(Message(role="user", content=request.message))
        updatedHistory.append(Message(role="assistant", content=responseText))

        return ChatResponse(
            response = responseText,
            convoHistory = updatedHistory 
        )
    
    except Exception as error:
        return f"Error with fastAPI: {error}"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)