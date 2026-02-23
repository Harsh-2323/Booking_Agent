# Booking Agent

A FastAPI-based booking agent that integrates with Google Calendar to check availability and schedule appointments through a REST API.

## Features

- **Check Availability** - Query Google Calendar for open slots in a given time range
- **Book Appointments** - Create calendar events with title, description, and timezone support
- **Conversational Booking** - Natural language endpoint to book meetings (e.g., "book a meeting at 5 PM")

## Tech Stack

- **FastAPI** - Async web framework
- **Google Calendar API** - Calendar integration via service account
- **Pydantic** - Request validation
- **pytz** - Timezone handling

## Project Structure

```
Booking_Agent/
├── backend/
│   ├── main.py                # FastAPI app with 3 endpoints
│   ├── calendar_service.py    # Google Calendar service wrapper
│   └── test.py                # Test script
├── config/
│   └── credentials.json       # Google service account key (not tracked)
├── requirements.txt
├── .env.example
└── .gitignore
```

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/Harsh-2323/Booking_Agent.git
cd Booking_Agent
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Google Calendar API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project and enable the **Google Calendar API**
3. Create a **Service Account** and download the JSON key
4. Place the key at `config/credentials.json`
5. Share your Google Calendar with the service account email

### 5. Configure environment

```bash
cp .env.example .env
# Edit .env with your Calendar ID
```

### 6. Run the server

```bash
cd backend
uvicorn main:app --reload
```

## API Endpoints

### GET `/check_availability`

Check if a time slot is available.

```bash
curl "http://localhost:8000/check_availability?start_time=2025-07-02T14:00:00&end_time=2025-07-02T15:00:00&timezone=Asia/Kolkata"
```

### POST `/book_appointment`

Book a calendar event.

```bash
curl -X POST http://localhost:8000/book_appointment \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Team Meeting",
    "description": "Weekly sync",
    "start_time": "2025-07-02T14:00:00+05:30",
    "end_time": "2025-07-02T15:00:00+05:30",
    "timezone": "Asia/Kolkata"
  }'
```

### POST `/converse`

Natural language booking.

```bash
curl -X POST http://localhost:8000/converse \
  -H "Content-Type: application/json" \
  -d '{"message": "book a meeting at 5 PM"}'
```
