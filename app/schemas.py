from pydantic import BaseModel

class ResearchRequest(BaseModel):
    query: str
    session_id: str 