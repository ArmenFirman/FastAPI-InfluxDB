from pydantic import BaseModel
from typing import List,Dict,Optional
from datetime import datetime

class WritingData(BaseModel):
    bucket_name: str
    measurement: str
    tag: Dict[str,str]
    field: Dict[str,float]
    timestamp: Optional[datetime] = None

    

class ReadingData(BaseModel):
    bucket_name: str
    time_interval: int
    measureament_name: str
    tag: Dict[str,str]
    field: List[str]

