# coding=utf-8
from skybluetech_scripts.tooldelta.events.basic import CustomC2SEvent, CustomS2CEvent


class IndustrialResearchingQueryRequest(CustomC2SEvent):
    name = "st:IRQReq"

    def __init__(self, player_id=""):
        # type: (str) -> None
        self.player_id = player_id

    def marshal(self):
        return {}

    @classmethod
    def unmarshal(cls, data):
        return cls(data["__id__"])


class IndustrialResearchingQueryResponse(CustomS2CEvent):
    name = "st:IRQResp"

    def __init__(self, researched_items):
        # type: (dict[str, int]) -> None
        self.researched_items = researched_items

    def marshal(self):
        return {"items": self.researched_items}

    @classmethod
    def unmarshal(cls, data):
        return cls(data.get("items", {}))


class IndustrialResearchingInscribeRequest(CustomC2SEvent):
    name = "st:IRInscribeReq"

    def __init__(self, item_id="", player_id=""):
        # type: (str, str) -> None
        self.item_id = item_id
        self.player_id = player_id

    def marshal(self):
        return {"item": self.item_id}

    @classmethod
    def unmarshal(cls, data):
        return cls(data.get("item", ""), data["__id__"])


class IndustrialResearchingSubmitRequest(CustomC2SEvent):
    name = "st:IRSubmitReq"

    def __init__(self, item_id="", player_id=""):
        # type: (str, str) -> None
        self.item_id = item_id
        self.player_id = player_id

    def marshal(self):
        return {"item": self.item_id}

    @classmethod
    def unmarshal(cls, data):
        return cls(data.get("item", ""), data["__id__"])
