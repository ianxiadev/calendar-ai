from fastapi import FastAPI # Pull out FastAPI class inside fastapi package
from pydantic import BaseModel
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.database import SessionLocal, EventModel, get_db

class Event(BaseModel): # New class event that inherits from BaseModel, receiving all Pydantic's validation abilities 
    title: str
    start: str
    end: str


app = FastAPI() # Create an instance of FastAPI class as object app

@app.get("/") # Checks if server is running
def read_root():
    return {"message": "Calender API is running"}

@app.get("/events")
def list_events(db: Session = Depends(get_db)):
    return db.query(EventModel).all() # Look at events table and get every row (generates real SQL under the hood), returning Python objects representing each row

@app.post("/events")
def create_event(event: Event, db: Session = Depends(get_db)): # Depends(get_db) tells FastAPI to first call get_db() and pass its output as db parameter
    new_event = EventModel(title=event.title, start=event.start, end=event.end)
    db.add(new_event)
    db.commit()
    db.refresh(new_event) # database fills in detailed you didn't provide such as the auto-generated id number
    return new_event
