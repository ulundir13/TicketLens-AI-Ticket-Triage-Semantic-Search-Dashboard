# TicketLens — AI Ticket Triage & Semantic Search API

AI-powered support ticket system built with FastAPI and Sentence Transformers.  
Includes CRUD operations and semantic similarity search using vector embeddings.
Designed as a minimal demonstration of AI-powered backend architecture for support ticket triage.
---

## Features

- Create support tickets
- Retrieve tickets by ID
- List all tickets
- Semantic search using sentence-transformers
- Cosine similarity ranking
- Interactive Swagger documentation

---

## 🛠 Tech Stack

- FastAPI
- Sentence Transformers (all-MiniLM-L6-v2)
- PyTorch
- NumPy
- Uvicorn

---

## Run Locally

### 1) Clone

```bash
git clone https://github.com/ulundir13/TicketLens-AI-Ticket-Triage-Semantic-Search-Dashboard.git
cd TicketLens-AI-Ticket-Triage-Semantic-Search-Dashboard

### 2) Create Virtual Environment & Install Dependencies

```bash
py -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

### 3) Start the API
uvicorn backend.app.main:app --reload --port 8000

Open in Browser

Swagger Docs: http://127.0.0.1:8000/docs

Health Check: http://127.0.0.1:8000/health