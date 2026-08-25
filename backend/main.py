from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from uuid import uuid4

from database import engine, Base, SessionLocal
from models import Monitor, CheckResult


app = FastAPI(title="Uptime Monitor API")

Base.metadata.create_all(bind=engine)


class MonitorCreate(BaseModel):
    name: str
    url: str
    interval: int = 30


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {
        "message": "Uptime Monitor API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/monitors")
def create_monitor(
    monitor: MonitorCreate,
    db: Session = Depends(get_db)
):
    monitor_id = str(uuid4())

    new_monitor = Monitor(
        id=monitor_id,
        name=monitor.name,
        url=monitor.url,
        interval=monitor.interval,
        status="unknown",
    )

    db.add(new_monitor)
    db.commit()
    db.refresh(new_monitor)

    return {
        "id": new_monitor.id,
        "name": new_monitor.name,
        "url": new_monitor.url,
        "interval": new_monitor.interval,
        "status": new_monitor.status,
    }


@app.get("/monitors")
def get_monitors(
    db: Session = Depends(get_db)
):
    monitors = db.query(Monitor).all()

    return [
        {
            "id": monitor.id,
            "name": monitor.name,
            "url": monitor.url,
            "interval": monitor.interval,
            "status": monitor.status,
        }
        for monitor in monitors
    ]


@app.get("/monitors/{monitor_id}")
def get_monitor(
    monitor_id: str,
    db: Session = Depends(get_db)
):
    monitor = (
        db.query(Monitor)
        .filter(Monitor.id == monitor_id)
        .first()
    )

    if not monitor:
        raise HTTPException(
            status_code=404,
            detail="Monitor not found"
        )

    return {
        "id": monitor.id,
        "name": monitor.name,
        "url": monitor.url,
        "interval": monitor.interval,
        "status": monitor.status,
    }


@app.post("/monitors/{monitor_id}/check")
def save_check_result(
    monitor_id: str,
    check: dict,
    db: Session = Depends(get_db)
):
    monitor = (
        db.query(Monitor)
        .filter(Monitor.id == monitor_id)
        .first()
    )

    if not monitor:
        raise HTTPException(
            status_code=404,
            detail="Monitor not found"
        )

    result = CheckResult(
        monitor_id=monitor_id,
        status=check["status"],
        status_code=check.get("status_code"),
        response_time=check.get("response_time"),
    )

    monitor.status = check["status"]

    db.add(result)
    db.commit()
    db.refresh(result)

    return {
        "message": "Check result saved",
        "monitor_id": monitor_id,
        "status": result.status,
        "status_code": result.status_code,
        "response_time": result.response_time,
    }


@app.get("/monitors/{monitor_id}/history")
def get_monitor_history(
    monitor_id: str,
    db: Session = Depends(get_db)
):
    monitor = (
        db.query(Monitor)
        .filter(Monitor.id == monitor_id)
        .first()
    )

    if not monitor:
        raise HTTPException(
            status_code=404,
            detail="Monitor not found"
        )

    results = (
        db.query(CheckResult)
        .filter(CheckResult.monitor_id == monitor_id)
        .order_by(CheckResult.checked_at.desc())
        .all()
    )

    return [
        {
            "status": result.status,
            "status_code": result.status_code,
            "response_time": result.response_time,
            "checked_at": result.checked_at,
        }
        for result in results
    ]
