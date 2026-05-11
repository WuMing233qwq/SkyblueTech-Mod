# coding=utf-8
from skybluetech_scripts.tooldelta.events.basic import CustomS2CEvent


class FamicomPlaySoundEvent(CustomS2CEvent):
    name = "st:FCPlaysound"

    def __init__(self, dim=0, x=0, y=0, z=0, sound_name="", stop=False):
        # type: (int, float, float, float, str, bool) -> None
        self.dim = dim
        self.x = x
        self.y = y
        self.z = z
        self.sound_name = sound_name
        self.stop = stop

    def marshal(self):
        return {
            "dim": self.dim,
            "x": self.x,
            "y": self.y,
            "z": self.z,
            "sound_name": self.sound_name,
            "stop": self.stop,
        }

    @classmethod
    def unmarshal(cls, data):
        return cls(
            dim=data["dim"],
            x=data["x"],
            y=data["y"],
            z=data["z"],
            sound_name=data["sound_name"],
            stop=data["stop"],
        )
