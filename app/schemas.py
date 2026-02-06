from pydantic import BaseModel
from typing import List, Optional


class IncidentRequest(BaseModel):
    incident_text: str


class IncidentResponse(BaseModel):
    steps: List[str]
    root_cause: str
    resolution: str


class IncidentOut(BaseModel):
    id: int
    input_text: str
    steps: str
    root_cause: str
    resolution: str

    class Config:
        from_attributes = True
