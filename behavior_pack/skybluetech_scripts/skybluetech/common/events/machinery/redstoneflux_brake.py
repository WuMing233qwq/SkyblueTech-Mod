# coding=utf-8
from skybluetech_scripts.tooldelta.events.basic import CustomC2SEvent


class RedstoneFluxBrakeModeSwitchRequest(CustomC2SEvent):
    name = "st:RFBMSR"

    def __init__(self, x, y, z, invert_redstone, player_id=""):
        # type: (int, int, int, bool, str) -> None
        self.x = x
        self.y = y
        self.z = z
        self.invert_redstone = invert_redstone
        self.player_id = player_id

    def marshal(self):
        return {
            "x": self.x,
            "y": self.y,
            "z": self.z,
            "ir": self.invert_redstone,
        }

    @classmethod
    def unmarshal(cls, data):
        return cls(data["x"], data["y"], data["z"], data["ir"], data["__id__"])
