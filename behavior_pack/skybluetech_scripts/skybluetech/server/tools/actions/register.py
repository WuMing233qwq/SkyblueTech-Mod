# coding=utf-8
#
from skybluetech_scripts.tooldelta.define.item import Item
from skybluetech_scripts.tooldelta.events.server import (
    ServerItemTryUseEvent,
    ServerItemUseOnEvent,
)
from ...machinery.utils.charge import SetUpdateChargeCallback
from .utils import RecoverToolFromUseless

# TYPE_CHECKING
if 0:
    import typing
# TYPE_CHECKING END

item_pre_use_cbs = {}  # type: dict[str, typing.Callable[[ServerItemTryUseEvent]]]
item_pre_use_on_block_cbs = {}  # type: dict[str, typing.Callable[[ServerItemUseOnEvent]]]
tool_items = set()  # type: set[str]
orig_tier_speed = {}  # type: dict[str, float]
orig_attack_damage = {}  # type: dict[str, int]


def RegisterTool(item_id):
    # type: (str) -> None
    "注册工具, 使得工具能在耐久变动缺乏能量后无法挖掘方块。"
    tool_items.add(item_id)

    def on_charge(item, _):
        # type: (Item, int) -> None
        ud = item.userData
        if ud is None:
            return
        if ud.get("st:useless"):
            RecoverToolFromUseless(item)

    SetUpdateChargeCallback(item_id, on_charge)


def RegisterItemPreUseCallback(item_id, callback):
    # type: (str, typing.Callable[[ServerItemTryUseEvent]]) -> None
    "注册物品的预使用回调。"
    item_pre_use_cbs[item_id] = callback


def RegisterItemPreUseOnBlockCallback(item_id, callback):
    # type: (str, typing.Callable[[ServerItemUseOnEvent]]) -> None
    "注册物品对方块的预使用回调。"
    item_pre_use_on_block_cbs[item_id] = callback
