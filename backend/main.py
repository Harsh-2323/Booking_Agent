from fastapi import FastAPI, HTTPException
from calendar_service import check_availability, create_event
from pydantic import BaseModel
import json
from datetime import datetime, timedelta
import re

app = FastAPI()

# Define request model for booking
class BookingRequest(BaseModel):
    title: str
    description: str
    start_time: str
    end_time: str
    timezone: str = "Asia/Kolkata"

# /check_availability endpoint
@app.get("/check_availability")
async def get_availability(start_time: str, end_time: str, timezone: str = "Asia/Kolkata"):
    try:
        conflicts = check_availability(start_time, end_time, timezone)
        return {"available": len(conflicts) == 0, "conflicts": conflicts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking availability: {str(e)}")

# /book_appointment endpoint
@app.post("/book_appointment")
async def book_appointment(booking: BookingRequest):
    try:
        event = create_event(
            title=booking.title,
            description=booking.description,
            start_time=booking.start_time,
            end_time=booking.end_time,
            timezone=booking.timezone
        )
        if event:
            return {"status": "success", "event": event}
        else:
            raise HTTPException(status_code=400, detail="Failed to create event")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating event: {str(e)}")

# /converse endpoint (placeholder for agent interaction)
@app.post("/converse")
async def converse(message: dict):
    try:
        # Placeholder: This will later integrate with LangGraph agent
        user_input = message.get("message", "").lower()
        if "book" in user_input and "meeting" in user_input:
            # Extract time from message (e.g., "at 5 PM" or "at 6 PM")
            match = re.search(r"at (\d{1,2})\s*pm", user_input)
            if match:
                hour = int(match.group(1))
                if hour > 12: hour = 12  # Cap at 12 for PM
                elif hour == 0: hour = 12  # Handle 0 as 12 PM
                # Set base date and time
                base_date = datetime.now()
                start_time = base_date.replace(hour=hour, minute=0, second=0, microsecond=0, tzinfo=None)
                end_time = start_time + timedelta(hours=1)
                # Convert to ISO 8601 with timezone
                start_time_str = start_time.isoformat() + "+05:30"  # Asia/Kolkata offset
                end_time_str = end_time.isoformat() + "+05:30"
                # Check availability
                conflicts = check_availability(start_time_str, end_time_str, "Asia/Kolkata")
                if not conflicts:
                    event = create_event("Meeting", "Scheduled via chat", start_time_str, end_time_str, "Asia/Kolkata")
                    return {
                        "response": f"Meeting booked for July 2, {hour}:00 PM to {hour+1}:00 PM IST!",
                        "event": event
                    }
                else:
                    return {"response": f"That slot at {hour}:00 PM is taken. Please try another time."}
            else:
                return {"response": "Please specify a time, e.g., 'book a meeting at 6 PM'."}
        return {"response": "Please specify a booking request, e.g., 'book a meeting'."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing conversation: {str(e)}")