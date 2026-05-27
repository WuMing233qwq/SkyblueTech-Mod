# coding=utf-8
from skybluetech_scripts.tooldelta.events.basic import CustomS2CEvent


class TemplateAssemblerUpdateRecipeEvent(CustomS2CEvent):
    name = "td:TemplateAssemblerUpdateRecipeEvent"

    def __init__(self):
        pass

    def marshal(self):
        return {}

    @classmethod
    def unmarshal(cls, data):
        return cls()


class TemplateAssemblerUpdateRecipeEvent2(CustomS2CEvent):
    name = "td:TemplateAssemblerUpdateRecipeEvent2"

    def __init__(self):
        pass

    def marshal(self):
        return {}

    @classmethod
    def unmarshal(cls, data):
        return cls()
