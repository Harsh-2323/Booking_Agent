from calendar_service import check_availability, create_event

start_time = '2025-07-02T14:00:00'
end_time = '2025-07-02T15:00:00'
timezone = 'Asia/Kolkata'

print("Checking availability...")
conflicts = check_availability(start_time, end_time, timezone)
if not conflicts:
    print("Time slot is available!")
else:
    print("Conflicting events:", conflicts)

event = create_event(
    title="Test Meeting",
    description="This is a test appointment.",
    start_time=start_time,
    end_time=end_time,
    timezone=timezone
)
if event:
    print("Event created:", event)
else:
    print("Failed to create event.")