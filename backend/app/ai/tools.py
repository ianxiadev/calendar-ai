tools = [
    {
        "name": "create_event",
        "description": "Create a new calendar event with a title, start time, and end time.",
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "The event's title"},
                "start": {"type": "string", "description": "Start time in ISO 8601 format"},
                "end": {"type": "string", "description": "End time in ISO 8601 format"}
            },
            "required": ["title", "start", "end"]
        }
    },
    {
        "name": "find_events",
        "description": "Search for existing events by title text and optionally a specific date, to find an event's ID before updating or deleting it.",
        "input_schema": {
            "type": "object",
            "properties": {
                "search_term": {"type": "string", "description": "Text to search for in event titles"},
                "event_date": {"type": "string", "description": "Optional specific date (YYYY-MM-DD) to narrow the search"}
            },
            "required": ["search_term"]
        }
    },
    {
        "name": "update_event",
        "description": "Update an existing event's title, start, and end time. You must know the event's ID first, usually from find_events.",
        "input_schema": {
            "type": "object",
            "properties": {
                "event_id": {"type": "integer", "description": "The ID of the event to update"},
                "title": {"type": "string"},
                "start": {"type": "string", "description": "ISO 8601 format"},
                "end": {"type": "string", "description": "ISO 8601 format"}
            },
            "required": ["event_id", "title", "start", "end"]
        }
    },
    {
        "name": "delete_event",
        "description": "Delete an existing event. You must know the event's ID first, usually from find_events.",
        "input_schema": {
            "type": "object",
            "properties": {
                "event_id": {"type": "integer", "description": "The ID of the event to delete"}
            },
            "required": ["event_id"]
        }
    }
]