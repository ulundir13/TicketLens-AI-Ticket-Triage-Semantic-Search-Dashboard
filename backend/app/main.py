from fastapi import FastAPI

app = FastAPI(title="TicketLens API")

@app.get("/health")
def health():
    return {"status": "ok"}
