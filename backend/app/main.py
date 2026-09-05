from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from app.db.database import get_db, EventModel
from app.logic import (
    create_event_logic,
    list_events_logic,
    update_event_logic,
    delete_event_logic,
)
from app.ai.agent import run_agent

app = FastAPI()


# ---------- Pydantic models ----------

class Event(BaseModel):
    title: str
    start: datetime
    end: datetime


class EventUpdate(BaseModel):
    title: Optional[str] = None
    start: Optional[datetime] = None
    end: Optional[datetime] = None


class AssistantRequest(BaseModel):
    text: str


# ---------- Routes ----------

@app.get("/")
def read_root():
    return {"message": "Calendar API is running"}


@app.get("/events")
def list_events(db: Session = Depends(get_db)):
    return list_events_logic(db)


@app.post("/events")
def create_event(event: Event, db: Session = Depends(get_db)):
    return create_event_logic(event.title, event.start, event.end, db)


@app.put("/events/{event_id}")
def update_event(event_id: int, event: Event, db: Session = Depends(get_db)):
    return update_event_logic(event_id, event.title, event.start, event.end, db)


@app.delete("/events/{event_id}")
def delete_event(event_id: int, db: Session = Depends(get_db)):
    return delete_event_logic(event_id, db)


@app.post("/assistant")
def assistant(payload: AssistantRequest, db: Session = Depends(get_db)):
    reply = run_agent(payload.text, db)
    return {"reply": reply}