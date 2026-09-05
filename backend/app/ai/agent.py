from app.ai.tools import tools
import os
import json
from datetime import datetime, date
from dotenv import load_dotenv
from anthropic import Anthropic
from app.logic import create_event_logic, find_events_logic, update_event_logic, delete_event_logic

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def run_agent(user_text: str, db):
    now = datetime.now()
    current_date = now.strftime("%A, %B %d, %Y, %I:%M %p") # Formates the datetime into readable string
    system_prompt = f"""You are a calendar assistant. The current date and time is {current_date}.
Use this to resolve relative dates like "tomorrow" or "next Friday" into exact dates.
When creating or updating events, use ISO 8601 format (YYYY-MM-DDTHH:MM:SS) for start and end times.
To update or delete an event, first use find_events to locate it and get its ID. CRITICAL: You must NEVER guess an event's 
ID, start time, or end time. You do not have access to any event's details unless you call find_events first. For any update 
or delete request, you must call find_events before calling update_event or delete_event, even if you think you already know the details."""
    messages = [{"role": "user", "content": user_text}]

    while True:
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1000,
            system=system_prompt,
            tools=tools,
            messages=messages # messages serves as a memory accumulating conversation history
        )
        if response.stop_reason != "tool_use":
            for block in response.content:
                if block.type == "text":
                    return block.text
            return ""

        messages.append({"role": "assistant", "content": response.content})

        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                result = execute_tool(block.name, block.input, db)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": json.dumps(result, default=str)
                })
        
        messages.append({"role": "user", "content": tool_results})

    
# Runs specific tool
def execute_tool(tool_name: str, tool_input: dict, db):
    if tool_name == "create_event":
        return create_event_logic(
            title=tool_input["title"],
            start=datetime.fromisoformat(tool_input["start"]),
            end=datetime.fromisoformat(tool_input["end"]),
            db=db
        )

    elif tool_name == "find_events":
        event_date = None
        if "event_date" in tool_input:
            event_date = date.fromisoformat(tool_input["event_date"])
        results = find_events_logic(
            search_term=tool_input["search_term"],
            event_date=event_date,
            db=db
        )
        return [
        {"id": e.id, "title": e.title, "start": e.start.isoformat(), "end": e.end.isoformat()}
        for e in results
        ]

    elif tool_name == "update_event":
        return update_event_logic(
            event_id=tool_input["event_id"],
            title=tool_input["title"],
            start=datetime.fromisoformat(tool_input["start"]),
            end=datetime.fromisoformat(tool_input["end"]),
            db=db
        )

    elif tool_name == "delete_event":
        return delete_event_logic(
            event_id=tool_input["event_id"],
            db=db
        )

    else:
        return {"error": f"Unknown tool: {tool_name}"}
