from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="Saas Rotina Backend", description="Hybrid AI Fitness API (MVP)")

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "Saas Rotina Backend"}

# Importaremos os routers nas próximas etapas...
