from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import func
from database import SessionLocal, engine, Base
from models import Session

Base.metadata.create_all(bind=engine)

app = FastAPI()

PRODUCTIVE = ["github.com", "leetcode.com", "stackoverflow.com"]

class TrackData(BaseModel):
    domain: str
    duration: int

def classify(domain):
    return "productive" if domain in PRODUCTIVE else "unproductive"

@app.post("/track")
def track(data: TrackData):
    db = SessionLocal()

    record = Session(
        domain=data.domain,
        duration=data.duration,
        category=classify(data.domain)
    )

    db.add(record)
    db.commit()
    db.close()

    return {"status": "saved"}

@app.get("/weekly")
def weekly():
    db = SessionLocal()

    result = db.query(
        Session.category,
        func.sum(Session.duration)
    ).group_by(Session.category).all()

    db.close()
    return result
