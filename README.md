# Neural Signal Simulator

A real-time neural spike activity simulator and visualization dashboard built with FastAPI, SQLite, and Chart.js.

## Overview

This project simulates neural spike activity from multiple neurons in real-time, stores the data in a SQLite database, and provides a web dashboard to visualize spike counts and statistics. It's designed to mimic the behavior of neural recording systems for demonstration and testing purposes.

## Features

- **Real-time Data Generation**: Simulates spike activity from multiple neurons with configurable rates
- **RESTful API**: FastAPI backend with endpoints for retrieving spike data and statistics
- **Live Dashboard**: Interactive web interface with real-time bar charts and total spike counters
- **Database Storage**: SQLite database with efficient indexing for time-series neural data
- **CORS Support**: Configured for cross-origin requests
- **Configurable Parameters**: Adjustable time windows, spike rates, and neuron counts

## Project Structure
```
├── app.py # FastAPI application and endpoints
├── db.py # Database configuration and session management
├── generator.py # Spike generation thread and logic
├── models.py # SQLAlchemy data models
├── index.html # Frontend dashboard HTML
├── app.js # Frontend JavaScript for chart updates
└── signals.db # SQLite database (created automatically)
```

## API Endpoints

### `GET /`
Serves the main dashboard interface.

### `GET /health`
Health check endpoint returning `{"status": "ok"}`.

### `GET /signals`
Retrieves individual spike events with optional filtering.

**Query Parameters:**
- `limit`: Number of records to return (1-5000, default: 200)
- `neuron_id`: Filter by specific neuron ID
- `since_seconds`: Time window in seconds (1-3600, default: 60)

### `GET /stats`
Returns aggregated spike statistics for the specified time window.

**Query Parameters:**
- `window_seconds`: Aggregation window in seconds (5-3600, default: 60)

**Response Format:**
```json
{
  "window_seconds": 60,
  "total_spikes": 450,
  "per_neuron": [
    {"neuron_id": 1, "count": 55, "avg_amp": 1.02},
    {"neuron_id": 2, "count": 62, "avg_amp": 0.98}
  ]
}
```

## Installation & Setup
1. Create project directory
```
mkdir neural-signal-simulator
cd neural-signal-simulator
```
2. Create a virtual environment
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
3. Install dependencies
```
pip install fastapi uvicorn sqlalchemy
```
4. Create project files
Add the provided Python files (app.py, db.py, generator.py, models.py) to your project directory.
5. Create frontend directory and files
```
mkdir frontend
```
Add index.html and app.js to the frontend directory.
6. Run the application
```
uvicorn app:app --reload
```
7. Access the dashboard
Open your browser and navigate to http://localhost:8000

## Configuration
The simulator can be configured by modifying the SpikeGenerator parameters in app.py:
```
generator = SpikeGenerator(neurons=8, spikes_per_sec=80)
```
- neurons: Number of simulated neurons (default: 8)
- spikes_per_sec: Total spikes per second across all neurons (default: 80)

## Database Schema
The spikes table contains:
- id: Primary key (auto-incrementing)
- neuron_id: Identifier for the neuron (1-based)
- ts: Timestamp of the spike event (UTC)
- amplitude: Simulated spike amplitude (normal distribution around 1.0)

Indexes are created on neuron_id, ts, and a composite index for efficient querying.

## Frontend Features
- Real-time bar chart showing spike counts per neuron
- Total spike counter for the last 60 seconds
- Responsive design that works on desktop and mobile devices
- Automatic updates every second

## Performance Considerations
- The database uses appropriate indexing for time-series queries
- The generator includes error handling to prevent application crashes
- Query limits prevent excessive data retrieval
- The frontend uses efficient Chart.js updates without full redraws

## Development
To modify or extend the project:
1. Add new endpoints: Edit app.py and add new route handlers
2. Modify data model: Update models.py and regenerate the database
3. Change generation logic: Adjust parameters in generator.py
4. Customize frontend: Modify index.html and app.js in the frontend directory

## License
This project is open source and available under the MIT License.
