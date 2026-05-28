# coding=utf-8
from skybluetech_scripts.tooldelta.define import Item
from skybluetech_scripts.tooldelta.api.server import GetItemBasicInfo


def Nbt2Item(item_nbt):
    # type: (dict) -> Item
    item_name = NbtItemName(item_nbt)
    item_aux = NbtItemDamage(item_nbt)
    item_count = NbtItemCount(item_nbt)
    item_tag = NbtItemTag(item_nbt)
    return Item(item_name, item_aux, item_count, userData=item_tag)


def Item2Nbt(slot, item):
    # type: (int, Item) -> dict
    return BuildNbtEntry(slot, item.id, item.newAuxValue, item.count, item.userData)


def GetChestItems(chest_nbt):
    # type: (dict) -> dict[int, dict]
    items = {}  # type: dict[int, dict]
    chest_nbt.get("Items", [])
    for slotitem_nbt in chest_nbt.get("Items", []):
        slotIndex = slotitem_nbt.get("Slot").get("__value__", 0)
        items[slotIndex] = slotitem_nbt
    return items


def NbtItemName(nbtItem):
    # type: (dict) -> str
    nameTag = nbtItem.get("Name")
    return nameTag.get("__value__", "") if nameTag else ""


def NbtItemCount(nbtItem):
    # type: (dict) -> int
    countTag = nbtItem.get("Count")
    return countTag.get("__value__", 0) if countTag else 0


def NbtItemDamage(nbtItem):
    # type: (dict) -> int
    damageTag = nbtItem.get("Damage")
    return damageTag.get("__value__", 0) if damageTag else 0


def NbtItemTag(nbtItem):
    # type: (dict) -> dict | None
    return nbtItem.get("tag")


def CanStackNbt(nbtItem, itemName, itemAux, userData):
    # type: (dict, str, int, dict | None) -> bool
    if NbtItemName(nbtItem) != itemName:
        return False
    if NbtItemDamage(nbtItem) != itemAux:
        return False
    # 比较 tag / userData
    return NbtItemTag(nbtItem) == userData


def NbtToItemDict(nbtItem, count):
    # type: (dict, int) -> dict
    result = {
        "newItemName": NbtItemName(nbtItem),
        "count": count,
        "newAuxValue": NbtItemDamage(nbtItem),
    }  # type: dict
    tag = NbtItemTag(nbtItem)
    if tag:
        result["userData"] = tag
    return result


def BuildNbtEntry(slotIndex, itemName, itemAux, count, userData=None):
    # type: (int, str, int, int, dict | None) -> dict
    entry = {
        "Count": {"__type__": 1, "__value__": count},
        "Slot": {"__type__": 1, "__value__": slotIndex},
        "Name": {"__type__": 8, "__value__": itemName},
        "Damage": {"__type__": 2, "__value__": itemAux},
        "WasPickedUp": {"__type__": 1, "__value__": 0},
    }
    if userData:
        entry["tag"] = userData
    return entry


def GetMaxStack(itemName, auxValue=0):
    # type: (str, int) -> int
    basicInfo = GetItemBasicInfo(itemName, auxValue)
    if basicInfo:
        return basicInfo.maxStackSize
    return 64
