from typing import Optional

from pydantic import BaseModel


class ValueSetItem(BaseModel):
    accession_id: str
    label: Optional[str]
    value: Optional[str]
    is_current: Optional[bool]
    definition: Optional[str]
    description: Optional[str]
