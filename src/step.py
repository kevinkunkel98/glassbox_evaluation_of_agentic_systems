from __future__ import annotations
import json
from dataclasses import dataclass, asdict


@dataclass
class Step:
    step_id: str
    instance_id: str
    step_idx: int
    thought: str
    tool: str
    parameters: dict
    raw_action: str
    observation: str

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json_line(self) -> str:
        return json.dumps(self.to_dict()) + "\n"

    @classmethod
    def from_dict(cls, data: dict) -> Step:
        return cls(**data)
