from dataclasses import dataclass
from typing import List, Optional

@dataclass
class PlaceContextDataclass:
    place_id: str
    name: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    neighborhood: Optional[str] = None
    owner_desc: Optional[str] = None
    menu_or_services: Optional[List[str]] = None

def build_place_text(ctx) -> str:
    # ctx may be Pydantic model or dataclass
    name = getattr(ctx, "name", None) or (ctx.name if hasattr(ctx, "name") else "")
    category = getattr(ctx, "category", None) or ""
    neighborhood = getattr(ctx, "neighborhood", None) or ""
    tags = getattr(ctx, "tags", None) or []
    mos = getattr(ctx, "menu_or_services", None) or []
    owner_desc = getattr(ctx, "owner_desc", None) or ""

    parts = [
        name, category, neighborhood,
        "tags: " + ", ".join(tags),
        "menu/services: " + ", ".join(mos),
        "about: " + owner_desc
    ]
    return " | ".join([p for p in parts if p])
