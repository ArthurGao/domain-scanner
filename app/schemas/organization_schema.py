from pydantic import BaseModel
from uuid import UUID

class OrgCreate(BaseModel):
    name: str

class OrgResponse(BaseModel):
    id: UUID
    name: str

    model_config = {
        "from_attributes": True
    }