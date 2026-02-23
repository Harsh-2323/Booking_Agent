from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import pytz
import os
from pathlib import Path

# Configuration
SCOPES = ['https://www.googleapis.com/auth/calendar']
CREDENTIALS_FILE = os.getenv('GOOGLE_CREDENTIALS_FILE', str(Path(__file__).parent.parent / 'config' / 'credentials.json'))
CALENDAR_ID = os.getenv('GOOGLE_CALENDAR_ID', '4906d31abdbbad405d77dbd7f8ec5d26eb6aa8961b169afb43462baad4609a30@group.calendar.google.com')

def get_calendar_service():
    """Authenticate and return a Google Calendar service object."""
    try:
        credentials = service_account.Credentials.from_service_account_file(
            CREDENTIALS_FILE, scopes=SCOPES)
        service = build('calendar', 'v3', credentials=credentials)
        return service
    except Exception as e:
        print(f"Error authenticating with Google Calendar: {e}")
        raise

def check_availability(start_time: str, end_time: str, timezone: str = 'UTC'):
    """
    Check calendar availability for a given time range.
    Args:
        start_time: ISO format string (e.g., '2025-07-02T14:00:00')
        end_time: ISO format string (e.g., '2025-07-02T15:00:00')
        timezone: Timezone name (e.g., 'America/New_York')
    Returns:
        List of conflicting events or empty list if available.
    """
    try:
        service = get_calendar_service()
        start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
        end_dt = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
        tz = pytz.timezone(timezone)
        start_dt = tz.localize(start_dt)
        end_dt = tz.localize(end_dt)

        events_result = service.events().list(
            calendarId=CALENDAR_ID,
            timeMin=start_dt.isoformat(),
            timeMax=end_dt.isoformat(),
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_result.get('items', [])
        return events
    except Exception as e:
        print(f"Error checking availability: {e}")
        return []

def create_event(title: str, description: str, start_time: str, end_time: str, timezone: str = 'UTC'):
    """
    Create a calendar event.
    Args:
        title: Event title (e.g., 'Meeting with Client')
        description: Event description
        start_time: ISO format string (e.g., '2025-07-02T14:00:00')
        end_time: ISO format string (e.g., '2025-07-02T15:00:00')
        timezone: Timezone name (e.g., 'America/New_York')
    Returns:
        Dict with event details or None if creation fails.
    """
    try:
        service = get_calendar_service()
        start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
        end_dt = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
        tz = pytz.timezone(timezone)
        start_dt = tz.localize(start_dt)
        end_dt = tz.localize(end_dt)

        event = {
            'summary': title,
            'description': description,
            'start': {
                'dateTime': start_dt.isoformat(),
                'timeZone': timezone,
            },
            'end': {
                'dateTime': end_dt.isoformat(),
                'timeZone': timezone,
            },
        }

        created_event = service.events().insert(
            calendarId=CALENDAR_ID, body=event).execute()
        return {
            'id': created_event.get('id'),
            'summary': created_event.get('summary'),
            'start': created_event.get('start').get('dateTime'),
            'end': created_event.get('end').get('dateTime'),
        }
    except Exception as e:
        print(f"Error creating event: {e}")
        return None