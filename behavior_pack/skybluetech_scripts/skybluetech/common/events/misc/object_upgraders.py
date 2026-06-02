# coding=utf-8
from skybluetech_scripts.tooldelta.events.basic import CustomC2SEvent
from skybluetech_scripts.tooldelta.utils.py_comp import py2_unicode

STRING_TYPES = (str, py2_unicode)


class ObjUpVeinMinerSettingsUpload(CustomC2SEvent):
    name = "st:OVMSU"

    def __init__(self, vein_blocks, player_id=""):
        # type: (list[str], str) -> None
        self.vein_blocks = vein_blocks
        self.player_id = player_id

    def marshal(self):
        return {"v": self.vein_blocks}

    @classmethod
    def unmarshal(cls, data):
        if not isinstance(data, dict):
            return cls(vein_blocks=[], player_id="")
        raw_vein_blocks = data.get("v", [])
        if not isinstance(raw_vein_blocks, list):
            raw_vein_blocks = []
        return cls(
            vein_blocks=[str(i) for i in raw_vein_blocks if isinstance(i, STRING_TYPES)],
            player_id=data.get("__id__", ""),
        )


class ObjUpVeinMinerSettingsAddBlockRequest(CustomC2SEvent):
    name = "st:OVMSABR"

    def __init__(self, player_id=""):
        # type: (str) -> None
        self.player_id = player_id

    def marshal(self):
        return {}

    @classmethod
    def unmarshal(cls, data):
        if not isinstance(data, dict):
            return cls(player_id="")
        return cls(player_id=data.get("__id__", ""))
