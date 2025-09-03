import random
import threading
import time
from datetime import datetime
from sqlalchemy.orm import Session
from .db import SessionLocal
from .models import Spike

class SpikeGenerator:
    def __init__(self, neurons=8, spikes_per_sec=80):
        self.neurons = neurons
        self.spikes_per_sec = spikes_per_sec
        self._stop_event = threading.Event()
        self._thread = None

    def start(self):
        if self._thread and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self):
        if self._thread is None:
            return
        self._stop_event.set()
        self._thread.join(timeout=2)

    def _run(self):
        sleep_interval = 1.0 / max(self.spikes_per_sec, 1)
        while not self._stop_event.is_set():
            try:
                with SessionLocal() as db:
                    neuron_id = random.randint(1, self.neurons)
                    amplitude = abs(random.gauss(1.0, 0.3))
                    spike = Spike(neuron_id=neuron_id, ts=datetime.utcnow(), amplitude=amplitude)
                    db.add(spike)
                    db.commit()
            except Exception:
                pass
            time.sleep(sleep_interval)
