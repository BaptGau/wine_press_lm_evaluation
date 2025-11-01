from dataclasses import dataclass
from enum import Enum
from typing import List


class SpeakerRole(Enum):
    ASSISTANT = "Assistant"
    USER = "User"


@dataclass
class ChatTurn:
    role: SpeakerRole
    content: str

    def to_string(self) -> str:
        return f"{self.role.value}: {self.content}"


def convert_history_to_string(history: List[ChatTurn]) -> str:
    string = ""

    for turn_idx, turn in enumerate(history):
        if turn_idx == len(history) - 1:
            string += turn.to_string()
        else:
            string += turn.to_string() + "\n"

    return string
