from dataclasses import dataclass
from datetime import datetime


@dataclass
class Task:
    id: int
    ds_id: int
    func_name: str
    func_args: str
    start_time: datetime
    note: str
    source: int
