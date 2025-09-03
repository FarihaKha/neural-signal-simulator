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

├── app.py # FastAPI application and endpoints
├── db.py # Database configuration and session management
├── generator.py # Spike generation thread and logic
├── models.py # SQLAlchemy data models
├── index.html # Frontend dashboard HTML
├── app.js # Frontend JavaScript for chart updates
└── signals.db # SQLite database (created automatically)


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

### Installation & Setup
Create project directory
```
mkdir neural-signal-simulator
cd neural-signal-simulator
```
