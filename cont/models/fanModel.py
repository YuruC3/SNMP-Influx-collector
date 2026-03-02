from dataclasses import dataclass
from typing import Optional, Annotated, Dict


@dataclass
class idracFanStatus:
    fans: Dict[str, int] | None = Dict[None, None] # name/index -> rpm