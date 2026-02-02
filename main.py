from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from datetime import datetime
import os
import random

app = FastAPI(title="Ticket API", version="1.0")

client = MongoClient(os.environ.get("MONGO_URI"))
db = client.ticketdb
tickets = db.tickets

def generate_ticket_id():
    return f"TCK-{random.randint(10000, 99999)}"

@app.post("/api/tickets")
def create_ticket(data: dict):
    ticket_id = generate_ticket_id()

    ticket = {
        "ticket_id": ticket_id,
        "user_name": data.get("user_name"),
        "issue_type": data.get("issue_type"),
        "description": data.get("description"),
        "priority": data.get("priority", "medium"),
        "status": "open",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }

    tickets.insert_one(ticket)

    return {
        "success": True,
        "ticket_id": ticket_id,
        "status": "open",
        "message": "Ticket created successfully"
    }

@app.get("/api/tickets/{ticket_id}")
def get_ticket_status(ticket_id: str):
    ticket = tickets.find_one({"ticket_id": ticket_id})
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return {
        "ticket_id": ticket["ticket_id"],
        "status": ticket["status"],
        "issue_type": ticket["issue_type"],
        "last_updated": ticket["updated_at"]
    }
