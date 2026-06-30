from __future__ import annotations

import uuid
from typing import List

from fastapi import APIRouter, HTTPException

from api.models import (
    SessionResponse, ChartInfo, BilingualText,
    CreateSessionRequest, StepRequest, ResetRequest,
)
from api.session_runner import (
    SESSIONS, CHARTS_META, CHART_ENTRY, CHART_URGENCY, DANGER_PANEL, SessionRunner,
)

router = APIRouter()

_VALID_INPUTS = {"1", "2", "3", "4", "b", "n", "p", "u"}


def _wrap(runner: SessionRunner, override=None) -> SessionResponse:
    return SessionResponse(
        session_id=runner.session_id,
        alive=runner.alive,
        screen=runner.current_screen,
        override_event=override,
        danger_panel=DANGER_PANEL,
    )


@router.get("/charts", response_model=List[ChartInfo])
def list_charts():
    return sorted(
        [
            ChartInfo(
                chart_id=cid,
                title=BilingualText(
                    en=meta.get("title_en", cid),
                    ar=meta.get("title_ar", ""),
                ),
                urgency=CHART_URGENCY.get(cid, "standard"),
            )
            for cid, meta in CHARTS_META.items()
        ],
        key=lambda c: c.chart_id,
    )


@router.post("/sessions", response_model=SessionResponse, status_code=201)
def create_session(req: CreateSessionRequest):
    if req.chart_id not in CHARTS_META:
        raise HTTPException(404, detail={"code": "chart_not_found",
                                         "message": f"chart_id '{req.chart_id}' not found"})
    sid = str(uuid.uuid4())
    try:
        runner = SessionRunner(session_id=sid, chart_id=req.chart_id)
    except RuntimeError as exc:
        raise HTTPException(503, detail={"code": "engine_unavailable", "message": str(exc)})
    SESSIONS[sid] = runner
    return _wrap(runner)


@router.get("/sessions/{session_id}", response_model=SessionResponse)
def get_session(session_id: str):
    runner = SESSIONS.get(session_id)
    if not runner:
        raise HTTPException(404, detail={"code": "session_not_found", "message": "Session not found"})
    return _wrap(runner)


@router.post("/sessions/{session_id}/step", response_model=SessionResponse)
def step_session(session_id: str, req: StepRequest):
    runner = SESSIONS.get(session_id)
    if not runner:
        raise HTTPException(404, detail={"code": "session_not_found", "message": "Session not found"})
    if not runner.alive:
        raise HTTPException(410, detail={"code": "session_ended",
                                         "message": "Session has ended — use POST /reset to restart"})
    if req.input not in _VALID_INPUTS:
        raise HTTPException(422, detail={"code": "invalid_input",
                                         "message": f"Invalid input '{req.input}'. Must be one of: {sorted(_VALID_INPUTS)}"})
    try:
        screen, override = runner.submit(req.input)
    except RuntimeError as exc:
        raise HTTPException(503, detail={"code": "engine_timeout", "message": str(exc)})
    return _wrap(runner, override)


@router.post("/sessions/{session_id}/reset", response_model=SessionResponse)
def reset_session(session_id: str, req: ResetRequest):
    runner = SESSIONS.get(session_id)
    if not runner:
        raise HTTPException(404, detail={"code": "session_not_found", "message": "Session not found"})
    if req.chart_id and req.chart_id not in CHARTS_META:
        raise HTTPException(404, detail={"code": "chart_not_found",
                                         "message": f"chart_id '{req.chart_id}' not found"})
    try:
        runner.reset(req.chart_id)
    except (ValueError, RuntimeError) as exc:
        raise HTTPException(400, detail={"code": "engine_unavailable", "message": str(exc)})
    return _wrap(runner)


@router.delete("/sessions/{session_id}")
def delete_session(session_id: str):
    runner = SESSIONS.pop(session_id, None)
    if not runner:
        raise HTTPException(404, detail={"code": "session_not_found", "message": "Session not found"})
    runner.stop()
    return {"ok": True}
