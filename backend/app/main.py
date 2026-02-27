from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

app = FastAPI(title="TicketLens API")
@app.get("/")
def root():
    return {"message": "TicketLens API is running. Visit /docs"}

# ---------- Models ----------
class TicketCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=120)
    description: str = Field(..., min_length=5, max_length=5000)

class Ticket(TicketCreate):
    id: int
    created_at: str

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5

# ---------- In-memory "DB" ----------
TICKETS: List[Ticket] = []
NEXT_ID = 1

# Load embedding model once
model = SentenceTransformer("all-MiniLM-L6-v2")
EMBED_DIM = model.get_sentence_embedding_dimension()

# FAISS index (cosine similarity via normalized inner product)
INDEX = faiss.IndexFlatIP(EMBED_DIM)

# Map FAISS vector positions -> ticket IDs
FAISS_TO_TICKET_ID = []

@app.get("/api/health")
def health():
    return {"status": "ok"}

# ---------- CRUD ----------
@app.post("/api/tickets", response_model=Ticket)
def create_ticket(payload: TicketCreate):
    global NEXT_ID
    ticket = Ticket(
        id=NEXT_ID,
        title=payload.title,
        description=payload.description,
        created_at=datetime.utcnow().isoformat() + "Z",
    )
    TICKETS.append(ticket)

    # --- FAISS add ---
    embedding = model.encode(ticket.description).astype("float32")
    faiss.normalize_L2(embedding.reshape(1, -1))

    INDEX.add(embedding.reshape(1, -1))
    FAISS_TO_TICKET_ID.append(ticket.id)

    NEXT_ID += 1
    return ticket

@app.get("/api/tickets", response_model=List[Ticket])
def list_tickets():
    return TICKETS

@app.get("/api/tickets/{ticket_id}", response_model=Ticket)
def get_ticket(ticket_id: int):
    for t in TICKETS:
        if t.id == ticket_id:
            return t
    raise HTTPException(status_code=404, detail="Ticket not found")

@app.post("/api/search")
def search_tickets(payload: SearchRequest):
    if INDEX.ntotal == 0:
        return []

    query_vec = model.encode(payload.query).astype("float32")
    faiss.normalize_L2(query_vec.reshape(1, -1))

    top_k = min(payload.top_k, INDEX.ntotal)
    scores, idxs = INDEX.search(query_vec.reshape(1, -1), top_k)

    results = []
    for score, faiss_idx in zip(scores[0], idxs[0]):
        if faiss_idx == -1:
            continue

        ticket_id = FAISS_TO_TICKET_ID[faiss_idx]
        ticket = next((t for t in TICKETS if t.id == ticket_id), None)
        if ticket:
            results.append({"ticket": ticket, "score": float(score)})

    return results