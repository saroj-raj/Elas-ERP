from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ✅ FIX: import from backend.app...  (package-absolute)
from backend.app.core.config import settings
from backend.app.api.endpoints import upload, chat, business, documents, ai, dashboard

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"]
)

@app.get("/health")
def health():
    return {"status": "ok", "service": "Elas ERP Backend", "version": "2.0"}

# Include all routers
app.include_router(upload.router, prefix="/api", tags=["upload"])
app.include_router(chat.router, prefix="/api", tags=["chat"])
app.include_router(business.router, prefix="/api", tags=["business"])
app.include_router(documents.router, prefix="/api", tags=["documents"])
app.include_router(ai.router, prefix="/api", tags=["ai"])
app.include_router(dashboard.router, prefix="/api", tags=["dashboard"])

