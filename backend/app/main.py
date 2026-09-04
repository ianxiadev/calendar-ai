from fastapi import FastAPI # Pull out FastAPI class inside fastapi package
from pydantic import BaseModel
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.database import SessionLocal, EventModel, get_db
from fastapi import HTTPException
from typing import Optional

class Event(BaseModel): # New class event that inherits from BaseModel, receiving all Pydantic's validation abilities 
    title: str
    start: str
    end: str

class EventUpdate(BaseModel):
    title: Optional[str] = None
    start: Optional[str] = None
    end: Optional[str] = None


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

@app.put("/events/{event_id}")
def update_event(event_id: int, event: Event, db: Session = Depends(get_db)):
    db_event = db.query(EventModel).filter(EventModel.id == event_id).first()
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    
    db_event.title = event.title
    db_event.start = event.start
    db_event.end = event.end

    db.commit()
    db.refresh(db_event)
    return db_event

@app.delete("/events/{event_id}")
def delete_event(event_id: int, db: Session = Depends(get_db)):
    db_event = db.query(EventModel).filter(EventModel.id == event_id).first()
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    
    event_title = db_event.title
    db.delete(db_event)
    db.commit()
    return {"detail": f"Event '{event_title}' deleted"}

@app.patch("/events/{event_id}")
def patch_event(event_id: int, event: EventUpdate, db: Session = Depends(get_db)):
    
    db_event = db.query(EventModel).filter(EventModel.id == event_id).first()
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    
    update_data = event.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_event, field, value)
    
    db.commit()
    db.refresh(db_event)
    return db_event