# Load .env
from dotenv import load_dotenv
from pathlib import Path
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)
# ---------

from fastapi import FastAPI

from src.endpoints.auth import router as router_auth 
from src.endpoints.qr_codes import router as router_qr_codes


app = FastAPI(
    title="QR Challenge",
    version="1.1",
)

app.include_router(router_auth)
app.include_router(router_qr_codes)
