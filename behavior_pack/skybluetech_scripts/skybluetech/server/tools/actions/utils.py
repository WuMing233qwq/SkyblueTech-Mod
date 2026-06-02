# coding=utf-8
from skybluetech_scripts.tooldelta.define.item import Item
from skybluetech_scripts.tooldelta.api.server import (
    SetItemTierSpeed,
    SetAttackDamage,
)
from skybluetech_scripts.tooldelta.utils import nbt

USELESS_SUFFIX = "_useless"
K_USELESS = "st:useless"
K_ORIGIN_ITEM_ID = "st:origin_item_id"
K_ORIGIN_TIER_SPEED = "st:origin_tier_speed"
K_ORIGIN_DAMAGE = "st:origin_damage"


def GetUselessToolId(item_id):
    # type: (str) -> str
    if item_id.endswith(USELESS_SUFFIX):
        return item_id
    return item_id + USELESS_SUFFIX


def GetOriginToolId(item_id):
    # type: (str) -> str
    if item_id.endswith(USELESS_SUFFIX):
        return item_id[:-len(USELESS_SUFFIX)]
    return item_id


def MakeToolUseless(tool_item):
    # type: (Item) -> None
    """
    使得道具物品无法使用。

    Args:
        tool_item (Item): 所给道具
    """
    ud = tool_item.userData
    if ud is not None and ud.get(K_USELESS):
        tool_item.newItemName = GetUselessToolId(tool_item.id)
        return
    if ud is None:
        origin_tier_speed = -1
        origin_damage = -1
        ud = {}
    else:
        origin_tier_speed = nbt.GetValueWithDefault(ud, "ModTierSpeed", -1)
        origin_damage = nbt.GetValueWithDefault(ud, "ModAttackDamage", -1)
    origin_item_id = GetOriginToolId(tool_item.id)
    ud[K_ORIGIN_ITEM_ID] = nbt.String(origin_item_id)
    ud[K_ORIGIN_TIER_SPEED] = nbt.Float(origin_tier_speed)
    ud[K_ORIGIN_DAMAGE] = nbt.Int(origin_damage)
    ud[K_USELESS] = True
    tool_item.userData = ud
    if not SetItemTierSpeed(tool_item, 0.0):
        print("[Error] failed to set item tier speed")
    if not SetAttackDamage(tool_item, 0):
        print("[Error] failed to set attack damage")
    tool_item.newItemName = GetUselessToolId(origin_item_id)


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
    origin_item_id = nbt.GetValueWithDefault(ud, K_ORIGIN_ITEM_ID, None)
    if origin_item_id is None:
        origin_item_id = GetOriginToolId(tool_item.id)
    tool_item.newItemName = origin_item_id
    origin_tier_speed = nbt.GetValueWithDefault(ud, K_ORIGIN_TIER_SPEED, None)
    origin_damage = nbt.GetValueWithDefault(ud, K_ORIGIN_DAMAGE, None)
    if origin_tier_speed == 0:
        origin_tier_speed = -1
    if origin_damage == 0:
        origin_damage = -1
    if origin_tier_speed == -1:
        ud.pop("ModTierSpeed", None)
    elif origin_tier_speed is not None:
        SetItemTierSpeed(tool_item, origin_tier_speed)
    if origin_damage == -1:
        ud.pop("ModAttackDamage", None)
    elif origin_damage is not None:
        SetAttackDamage(tool_item, origin_damage)
    ud = tool_item.userData or ud
    ud.pop(K_ORIGIN_ITEM_ID, None)
    ud.pop(K_ORIGIN_TIER_SPEED, None)
    ud.pop(K_ORIGIN_DAMAGE, None)
    ud.pop(K_USELESS, None)
    tool_item.userData = ud
