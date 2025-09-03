from datetime import datetime
from sqlalchemy import Column, Integer, Float, DateTime, Index
from .db import Base

class Spike(Base):
    __tablename__ = "spikes"

    id = Column(Integer, primary_key=True, index=True)
    neuron_id = Column(Integer, index=True)
    ts = Column(DateTime, index=True, default=datetime.utcnow)
    amplitude = Column(Float)

Index("ix_spikes_neuron_ts", Spike.neuron_id, Spike.ts)
