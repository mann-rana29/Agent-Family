from typing import Literal

from pydantic import BaseModel, Field

class SupportResponse(BaseModel):
    resolution : str = Field(
        min_length=1,
        max_length=4000
    )

    status : Literal["resolved", "needs_human", "needs_more_info"]

    cited_order_ids : list[str] = Field(default_factory=list)