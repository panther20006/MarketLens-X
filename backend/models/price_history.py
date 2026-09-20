from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class PriceHistory:

    product_id: Optional[str]

    product_title: str

    price: float

    store: Optional[str] = None

    created_at: datetime = None

    def __post_init__(self):

        if self.created_at is None:
            self.created_at = datetime.now()