# coding=utf-8
from skybluetech_scripts.tooldelta.events.basic import CustomC2SEvent


class InscribingTemplateGraphUpload(CustomC2SEvent):
    name = "st:ITGU"

    def __init__(self, graph, player_id=""):
        # type: (list[int], str) -> None
        self.graph = graph
        self.player_id = player_id

    def marshal(self):
        # type: () -> dict
        return {"g": self.graph}

    @classmethod
    def unmarshal(cls, args):
        return cls(args["g"], args["__id__"])
