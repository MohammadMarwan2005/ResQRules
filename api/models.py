from __future__ import annotations
from typing import Optional, List
from pydantic import BaseModel


class BilingualText(BaseModel):
    en: str
    ar: str


class OptionItem(BaseModel):
    id: int
    label: BilingualText


class CFChoice(BaseModel):
    id: int
    key: str
    label: BilingualText
    cf_value: float


class CFConfig(BaseModel):
    prompt: BilingualText
    choices: List[CFChoice]
    threshold: float


class HemTierInfo(BaseModel):
    current: int
    max_tier: int
    terminal: bool
    intervention: BilingualText


class DangerPanelItem(BaseModel):
    key: str
    label: BilingualText
    severity: str


class OverrideEvent(BaseModel):
    kind: str
    salience: int
    jumped_to_chart: Optional[str] = None
    guard_fired: bool


class ScreenState(BaseModel):
    type: str
    node_id: str
    chart_id: str
    chart_title: BilingualText
    page: int
    text: BilingualText
    options: Optional[List[OptionItem]] = None
    cf: Optional[CFConfig] = None
    hem_tier: Optional[HemTierInfo] = None
    is_terminal: bool = False
    stub_target: Optional[str] = None


class SessionResponse(BaseModel):
    session_id: str
    alive: bool
    screen: ScreenState
    override_event: Optional[OverrideEvent] = None
    danger_panel: List[DangerPanelItem]


class ChartInfo(BaseModel):
    chart_id: str
    title: BilingualText
    urgency: str


class CreateSessionRequest(BaseModel):
    chart_id: str


class StepRequest(BaseModel):
    input: str


class ResetRequest(BaseModel):
    chart_id: Optional[str] = None
