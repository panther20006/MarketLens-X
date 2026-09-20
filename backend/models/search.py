from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Search:

    query: str

    shopping_query: Optional[str] = None

    created_at: datetime = None

    results_count: int = 0

    duplicates_removed: int = 0

    def __post_init__(self):

        if self.created_at is None:
            self.created_at = datetime.now()