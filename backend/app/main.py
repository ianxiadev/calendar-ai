from fastapi import FastAPI # Pull out FastAPI class inside fastapi package

app = FastAPI() # Create an instance of FastAPI class as object app

@app.get("/") # Checks if server is running
def read_root():
    return {"message": "Calender API is running"}

@app.get("/events")
def list_events():
    return [
        {"id": 1, "title": "CS Lecture", "start": "2026-09-05T14:00:00", "end": "2026-09-05T15:20:00"},
        {"id": 2, "title": "Study for exam", "start": "2026-09-07T19:00:00", "end": "2026-09-07T21:00:00"},
    ]