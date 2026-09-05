from datetime import datetime, date
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.db.database import EventModel

def create_event_logic(title: str, start: datetime, end: datetime, db: Session):
    new_event = EventModel(title=title, start=start, end=end)
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event

def list_events_logic(db: Session):
    return db.query(EventModel).all()

def find_events_logic(search_term: str, event_date: date | None, db: Session):
    query = db.query(EventModel).filter(EventModel.title.ilike(f"%{search_term}%"))
    if event_date is not None:
        from datetime import timedelta
        query = query.filter(EventModel.start >= event_date, EventModel.start < event_date + timedelta(days=1))
    return query.all()

def update_event_logic(event_id: int, title: str, start: datetime, end: datetime, db: Session):
    db_event = db.query(EventModel).filter(EventModel.id == event_id).first()
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    db_event.title = title
    db_event.start = start
    db_event.end = end
    db.commit()
    db.refresh(db_event)
    return db_event

def delete_event_logic(event_id: int, db: Session):
    db_event = db.query(EventModel).filter(EventModel.id == event_id).first()
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    event_title = db_event.title
    db.delete(db_event)
    db.commit()
    return {"detail": f"Event '{event_title}' deleted"}