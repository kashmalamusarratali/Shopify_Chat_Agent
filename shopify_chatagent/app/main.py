from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from sqlalchemy.orm import Session
from .database import engine, Base, SessionLocal
from . import schemas, crud 
from .services.agent_service import handle_message

from fastapi.middleware.cors import CORSMiddleware
import os



Base.metadata.create_all(bind=engine)
BASE_URL = os.getenv("BASE_URL")
SHOPIFY_DOMAIN = os.getenv(SHOPIFY_DOMAIN)

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[SHOPIFY_DOMAIN],  # your Shopify domain
  # later restrict to your shop domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/chat", response_model=schemas.ChatResponse)
def chat(request: schemas.ChatRequest, db: Session = Depends(get_db)):

    crud.get_or_create_session(db, request.session_id)

    crud.save_message(db, request.session_id, "user", request.message)

    reply = handle_message(request.message)

    crud.save_message(db, request.session_id, "assistant", reply)

    return {"reply": reply}

import requests

@app.get("/inject-script")
def inject_script():
    SHOPIFY_STORE_URL = os.getenv("SHOPIFY_STORE_URL")

    url = f"https://{SHOPIFY_STORE_URL}/admin/api/2026-01/script_tags.json"
    headers = {
    "X-Shopify-Access-Token": os.getenv("SHOPIFY_ACCESS_TOKEN"),
    "Content-Type": "application/json"
}
    data = {
        "script_tag": {
            "event": "onload",
            "src": f"{BASE_URL}/static/chatbot.js"
        }
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()