from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class PlaceContext(BaseModel):
    place_id: str
    name: Optional[str] = None
    category: Optional[str] = None            # e.g., "restaurant"
    tags: Optional[List[str]] = None
    neighborhood: Optional[str] = None
    owner_desc: Optional[str] = None
    menu_or_services: Optional[List[str]] = None

class EvaluateRequest(BaseModel):
    review_text: str = Field(..., min_length=1)
    place_context: PlaceContext

class EvaluateResponse(BaseModel):
    action: str
    reasons: List[str]
    scores: Dict[str, Any]
    place_context: str
