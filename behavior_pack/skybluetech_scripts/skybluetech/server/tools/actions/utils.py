# coding=utf-8
from skybluetech_scripts.tooldelta.define.item import Item
from skybluetech_scripts.tooldelta.api.server import (
    SetItemTierSpeed,
    SetAttackDamage,
)
from skybluetech_scripts.tooldelta.utils import nbt


def MakeToolUseless(tool_item):
    # type: (Item) -> None
    """
    使得道具物品无法使用。

    Args:
        tool_item (Item): 所给道具
    """
    ud = tool_item.userData
    if ud is None:
        origin_tier_speed = -1
        origin_damage = -1
        ud = {}
    else:
        origin_tier_speed = nbt.GetValueWithDefault(ud, "ModTierSpeed", -1)
        origin_damage = nbt.GetValueWithDefault(ud, "ModAttackDamage", -1)
    ud["st:origin_tier_speed"] = nbt.Float(origin_tier_speed)
    ud["st:origin_damage"] = nbt.Int(origin_damage)
    ud["st:useless"] = True
    tool_item.userData = ud
    if not SetItemTierSpeed(tool_item, 0.0):
        print("[Error] failed to set item tier speed")
    if not SetAttackDamage(tool_item, 0):
        print("[Error] failed to set attack damage")


def RecoverToolFromUseless(tool_item):
    # type: (Item) -> None
    """
    恢复道具物品的原始属性。

    Args:
        tool_item (Item): 所给道具
    """
    ud = tool_item.userData
    if ud is None:
        return
    origin_tier_speed = nbt.GetValueWithDefault(ud, "st:origin_tier_speed", None)
    origin_damage = nbt.GetValueWithDefault(ud, "st:origin_damage", None)
    if origin_tier_speed == -1:
        ud.pop("ModTierSpeed", None)
    elif origin_tier_speed is not None:
        SetItemTierSpeed(tool_item, origin_tier_speed)
    if origin_damage == -1:
        ud.pop("ModAttackDamage", None)
    elif origin_damage is not None:
        SetAttackDamage(tool_item, origin_damage)
    ud.pop("st:origin_tier_speed", None)
    ud.pop("st:origin_damage", None)
    ud.pop("st:useless", None)
    tool_item.userData = ud
