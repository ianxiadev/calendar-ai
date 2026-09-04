from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, DateTime

DATABASE_URL = "sqlite:///./calender.db" #Tells SQLAlchemy what kind of database to connect to and where calender.db exists in the repo

engine = create_engine(DATABASE_URL) # This engine is SQLAlchemy's core connection object managing communication wih the database file

SessionLocal = sessionmaker(bind=engine) # A session is a emporary workspace for doing database operations. We need sessions so operations from different users/requests do not interfere with one another

Base = declarative_base() # Base class that all table definitions inherit from, represents the shape of a database tableoka

class EventModel(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key = True)
    title = Column(String)
    start = Column(DateTime)
    end = Column(DateTime)


Base.metadata.create_all(bind=engine)

# Opens a session, hands session to the route to use, and once route function is done, execution comes back and closes the session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()