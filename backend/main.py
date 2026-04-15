from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router
from utils.logger import get_logger

logger = get_logger("main")

app = FastAPI(
    title="AI Data Analysis Agent API",
    description="Professional B2B Data Analysis Agent powered by LangChain.",
    version="1.0.0"
)

# CORS middleware for Streamlit Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict to Streamlit's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up AI Data Analysis Agent Backend...")

@app.get("/health")
def health_check():
    return {"status": "healthy"}
