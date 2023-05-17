from pydantic import BaseModel


class ErrorResponse(BaseModel):
    status_code: str
    message: str


class ValueSetItem(BaseModel):
    accession_id: str
    label: str
    value: str
    is_current: bool
    definition: str
    description: str
