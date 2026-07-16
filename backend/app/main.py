from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from neo4j import GraphDatabase
from redis import Redis

from app.api.routes_chat import router as chat_router
from app.config import get_settings
from app.services.mood import get_mood_classifier
from app.services.schema import ensure_schema

WEB_DIR = Path("/web")


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    app.state.neo4j_driver = GraphDatabase.driver(
        settings.neo4j_uri,
        auth=(settings.neo4j_user, settings.neo4j_password),
    )
    app.state.redis = Redis.from_url(settings.redis_url, decode_responses=True)
    ensure_schema(app.state.neo4j_driver)
    app.state.mood_classifier = get_mood_classifier(settings.mood_model)
    app.state.mood_ready = True
    yield
    app.state.neo4j_driver.close()
    app.state.redis.close()


app = FastAPI(title="Portfolio GraphRAG Chatbot", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)


@app.get("/health")
def health():
    neo4j_ok = False
    redis_ok = False

    try:
        app.state.neo4j_driver.verify_connectivity()
        neo4j_ok = True
    except Exception:
        pass

    try:
        redis_ok = app.state.redis.ping() is True
    except Exception:
        pass

    mood_ok = bool(getattr(app.state, "mood_ready", False))
    status = "ok" if neo4j_ok and redis_ok and mood_ok else "degraded"
    return {
        "status": status,
        "neo4j": neo4j_ok,
        "redis": redis_ok,
        "mood": mood_ok,
    }


# Mount last so /health and /chat win
if WEB_DIR.is_dir():
    app.mount("/", StaticFiles(directory=str(WEB_DIR), html=True), name="web")
