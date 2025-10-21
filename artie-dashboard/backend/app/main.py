from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ✅ FIX: import from backend.app...  (package-absolute)
from backend.app.core.config import settings
from backend.app.api.endpoints import upload, chat

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"]
)

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(upload.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
