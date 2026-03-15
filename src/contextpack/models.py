from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class ContextSource:
    url: str
    title: Optional[str] = None
    domain: Optional[str] = None

@dataclass
class ContextChunk:
    text: str
    source_url: str
    score: float = 0.0
    metadata: dict = field(default_factory=dict)

@dataclass
class ContextPackResult:
    query: str
    sources: List[ContextSource]
    chunks: List[ContextChunk]
    context: str
