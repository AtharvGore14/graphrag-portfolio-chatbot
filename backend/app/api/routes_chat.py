from fastapi import APIRouter, HTTPException, Request

from app.config import get_settings
from app.models.schemas import ChatRequest, ChatResponse
from app.services.chat import run_chat_turn

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(body: ChatRequest, request: Request) -> ChatResponse:
    settings = get_settings()
    session_id = body.resolved_session_id()
    driver = request.app.state.neo4j_driver
    redis = request.app.state.redis
    mood_clf = getattr(request.app.state, "mood_classifier", None)
    if mood_clf is None:
        raise HTTPException(status_code=503, detail="mood classifier not ready")

    try:
        driver.verify_connectivity()
    except Exception as exc:
        raise HTTPException(status_code=503, detail="neo4j unavailable") from exc

    try:
        return await run_chat_turn(
            user_id=body.user_id,
            message=body.message,
            session_id=session_id,
            driver=driver,
            redis=redis,
            mood_classifier=mood_clf,
            settings=settings,
        )
    except RuntimeError as exc:
        msg = str(exc)
        if msg.startswith("dependency_failure") or msg.startswith("llm_failure"):
            raise HTTPException(status_code=503, detail=msg) from exc
        raise
