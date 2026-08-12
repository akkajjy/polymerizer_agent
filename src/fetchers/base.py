from pydantic import BaseModel, Field
from datetime import datetime

class RawItem(BaseModel):
    """所有info source 采集到的内容，tranfer to this format.
    the subsequent deduplication, scoring, and report generation modules only recognize this format
    """
    source: str
    title: str
    url: str
    summary: str
    published_at: datetime
    fetched_at: datetime = Field(default_factory=datetime.now)