from datetime import datetime, timedelta
from typing import Optional
from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import func, select, desc
import os

from .db import Base, engine, SessionLocal
from .models import Spike
from .generator import SpikeGenerator

app = FastAPI(title="Neural Signal Simulator", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend")
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

generator = SpikeGenerator(neurons=8, spikes_per_sec=80)

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    generator.start()

@app.on_event("shutdown")
def on_shutdown():
    generator.stop()

@app.get("/")
def root():
    index_path = os.path.join(frontend_dir, "index.html")
    return FileResponse(index_path)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/signals")
def get_signals(
    limit: int = Query(200, ge=1, le=5000),
    neuron_id: Optional[int] = None,
    since_seconds: int = Query(60, ge=1, le=3600),
    db: Session = Depends(get_db),
):
    cutoff = datetime.utcnow() - timedelta(seconds=since_seconds)
    query = db.query(Spike).filter(Spike.ts >= cutoff)
    if neuron_id:
        query = query.filter(Spike.neuron_id == neuron_id)
    rows = query.order_by(desc(Spike.ts)).limit(limit).all()
    return [
        {"id": r.id, "neuron_id": r.neuron_id, "ts": r.ts.isoformat(), "amplitude": r.amplitude}
        for r in rows
    ]

@app.get("/stats")
def get_stats(
    window_seconds: int = Query(60, ge=5, le=3600),
    db: Session = Depends(get_db),
):
    cutoff = datetime.utcnow() - timedelta(seconds=window_seconds)
    stmt = (
        select(
            Spike.neuron_id,
            func.count(Spike.id).label("count"),
            func.avg(Spike.amplitude).label("avg_amp"),
        )
        .where(Spike.ts >= cutoff)
        .group_by(Spike.neuron_id)
        .order_by(Spike.neuron_id)
    )
    results = db.execute(stmt).all()
    total = sum(r.count for r in results) if results else 0
    return {
        "window_seconds": window_seconds,
        "total_spikes": int(total),
        "per_neuron": [
            {"neuron_id": int(r.neuron_id), "count": int(r.count), "avg_amp": float(r.avg_amp or 0.0)}
            for r in results
        ],
    }
