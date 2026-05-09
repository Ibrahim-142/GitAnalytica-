from fastapi import FastAPI
from app.api.routes import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="GitHub Developer Analyzer")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)
