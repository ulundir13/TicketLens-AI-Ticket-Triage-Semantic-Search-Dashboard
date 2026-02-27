## TicketLens – AI Ticket Triage + Semantic Search

TicketLens is a full-stack AI-powered ticket management system that uses Sentence Transformers + FAISS vector search to perform semantic similarity matching on support tickets.

## It allows you to:

- Create tickets
- Store embeddings
- Perform semantic search using cosine similarity
- Run the entire stack via Docker

## Architecture

- Backend: FastAPI
- Embeddings: sentence-transformers (all-MiniLM-L6-v2)
- Vector Index: FAISS (IndexFlatIP with L2 normalization)
- Frontend: React + Vite
- Reverse Proxy: Nginx
- Containerization: Docker (multi-stage builds)
- Orchestration: Docker Compose

## System Architecture

![TicketLens Architecture](docs/architecture.png)

```mermaid
flowchart LR
    User[User Browser]
    React[React Frontend (Vite)]
    Nginx[Nginx Reverse Proxy]
    API[FastAPI Backend]
    Model[Sentence Transformer Model]
    FAISS[FAISS Vector Index]

    User --> React
    React --> Nginx
    Nginx --> API
    API --> Model
    Model --> FAISS
    FAISS --> API
    API --> React

## Run With Docker (Recommended)
Requirements:

-Docker Desktop installed
-Docker Engine running

## One Command Startup

From the project root:
docker compose up --build

This will:

- Build backend container (FastAPI + FAISS)
- Build frontend container (React + Nginx)
- Start both services
- Wire networking automatically

## Access the Application

Frontend: http://localhost:5173

Backend API Docs: http://localhost:8000/docs

Health Check: http://localhost:8000/api/health

## Stop The Application

Press: CTRL + C
Or run: docker compose down

## Running Without Docker (Dev Mode)

Backend:
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

Frontend:
cd frontend
npm install
npm run dev

Frontend will run on: http://localhost:5173

## API Endpoints
Method	Endpoint	Description
GET	/api/health	Health check
POST	/api/tickets	Create ticket
GET	/api/tickets	List tickets
GET	/api/tickets/{id}	Get ticket by ID
POST	/api/search	Semantic search

## How Semantic Search Works

1. Ticket description is embedded using: all-MiniLM-L6-v2
2. Embeddings are normalized using faiss.normalize_L2
3. Stored in a FAISS IndexFlatIP
4. Query embeddings are normalized and searched via inner product
5. Top-K results returned with similarity scores

## Frontend (Vite Template Info)

This project uses React + Vite.

The original Vite template includes:

- @vitejs/plugin-react
- Optional SWC plugin
- HMR support
- ESLint integration

React Compiler is not enabled by default.

## Project Structure:
backend/
  Dockerfile
  app/
    main.py

frontend/
  Dockerfile
  nginx.conf
  src/

docker-compose.yml
requirements.txt