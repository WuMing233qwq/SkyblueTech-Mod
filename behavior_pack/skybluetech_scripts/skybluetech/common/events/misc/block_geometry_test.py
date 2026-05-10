# coding=utf-8
from skybluetech_scripts.tooldelta.events.basic import CustomS2CEvent


class BlockGeometryTest(CustomS2CEvent):
    name = "st:BGT"

    def __init__(self, start_pos, end_pos, display_pos):
        # type: (tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]) -> None
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.display_pos = display_pos

    def marshal(self):
        return {
            "start_pos": self.start_pos,
            "end_pos": self.end_pos,
            "display_pos": self.display_pos,
        }

    @classmethod
    def unmarshal(cls, data):
        # type: (dict) -> "BlockGeometryTest"
        return cls(
            start_pos=data["start_pos"],
            end_pos=data["end_pos"],
            display_pos=data["display_pos"],
        )
