from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List
from sentence_transformers import SentenceTransformer
import numpy as np

app = FastAPI(title="TicketLens API")

# ---------- Models ----------
class TicketCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=120)
    description: str = Field(..., min_length=5, max_length=5000)

class Ticket(TicketCreate):
    id: int
    created_at: str

class SearchRequest(BaseModel):
    query: str

# ---------- In-memory "DB" ----------
TICKETS: List[Ticket] = []
NEXT_ID = 1

# Load embedding model once
model = SentenceTransformer("all-MiniLM-L6-v2")

# Store embeddings separately
EMBEDDINGS = []

@app.get("/health")
def health():
    return {"status": "ok"}


# ---------- CRUD ----------
@app.post("/tickets", response_model=Ticket)
def create_ticket(payload: TicketCreate):
    global NEXT_ID
    ticket = Ticket(
        id=NEXT_ID,
        title=payload.title,
        description=payload.description,
        created_at=datetime.utcnow().isoformat() + "Z",
    )
    TICKETS.append(ticket)

    embedding = model.encode(ticket.description)
    EMBEDDINGS.append(embedding)

    NEXT_ID += 1
    return ticket

@app.get("/tickets", response_model=List[Ticket])
def list_tickets():
    return TICKETS

@app.get("/tickets/{ticket_id}", response_model=Ticket)
def get_ticket(ticket_id: int):
    for t in TICKETS:
        if t.id == ticket_id:
            return t
    raise HTTPException(status_code=404, detail="Ticket not found")

@app.post("/search")
def search_tickets(payload: SearchRequest):
    query = payload.query
    if not TICKETS:
        return []

    query_embedding = model.encode(query)

    similarities = [
        float(np.dot(query_embedding, emb) / (np.linalg.norm(query_embedding) * np.linalg.norm(emb)))
        for emb in EMBEDDINGS
    ]

    ranked = sorted(
        zip(TICKETS, similarities),
        key=lambda x: x[1],
        reverse=True
    )

    return [
        {
            "ticket": ticket,
            "score": score
        }
        for ticket, score in ranked
    ]