# coding=utf-8
from mod.server.extraServerApi import GetMinecraftEnum
from skybluetech_scripts.tooldelta.define import Item, BlockBasicInfo
from skybluetech_scripts.tooldelta.api.server import (
    GetPlayerMainhandItem,
    PlayerDestroyBlock,
    GetBlockBasicInfo,
    GetBlockName,
    GetBlockTags,
    GetPlayerGameType,
    SpawnItemToPlayerCarried,
    SetCommand,
)
from skybluetech_scripts.tooldelta.events.server import DestroyBlockEvent
from skybluetech_scripts.tooldelta.api.common import Delay
from ...common.tools_def.mining_hammer import MINING_HAMMERS

DIGGING_LEVEL_MAPPING = {
    "minecraft:stone_tier_destructible": 1,
    "minecraft:iron_tier_destructible": 2,
    "minecraft:diamond_tier_destructible": 3,
}
GameType = GetMinecraftEnum().GameType

player_digging_poses = {}  # type: dict[str, set[tuple[int, int, int]]]


def get_digging_level(block_id, block_basic_info, default=0):
    # type: (str, BlockBasicInfo, int) -> int
    if block_basic_info.tier is not None:
        return block_basic_info.tier.get("level", 3)
    else:
        block_tags = GetBlockTags(block_id)
        for k, v in DIGGING_LEVEL_MAPPING.items():
            if k in block_tags:
                return v
        return default


def can_dig_same(block_id1, block_id2):
    # type: (str, str) -> bool
    block_basic_info1 = GetBlockBasicInfo(block_id1)
    block_basic_info2 = GetBlockBasicInfo(block_id2)
    if (
        block_basic_info1.destroyTime < block_basic_info2.destroyTime
        or block_basic_info2.destroyTime < 0
    ):
        return False
    if block_basic_info2.tier and block_basic_info2.tier.get("digger", 1) != 1:
        return False
    if block_basic_info1.tier is not None and block_basic_info2.tier is not None:
        return block_basic_info1.tier.get("level", 0) >= block_basic_info2.tier.get(
            "level", 255
        )
    res = get_digging_level(block_id1, block_basic_info1) >= get_digging_level(
        block_id2, block_basic_info2
    )
    return res

@Delay(0)
def chain_mine(player_id, dimension_id, block_full_name, poses):
    # type: (str, int, str, list[tuple[int, int, int]]) -> None
    mhitem = GetPlayerMainhandItem(player_id)
    if mhitem is None or mhitem.id not in MINING_HAMMERS or mhitem.durability is None:
        return
    last_index = len(poses) - 1
    try:
        for i, pos in enumerate(poses):
            block_id = GetBlockName(dimension_id, pos)
            if block_id is None:
                continue
            if not can_dig_same(block_full_name, block_id):
                continue
            player_digging_poses.setdefault(player_id, set()).add(pos)
            PlayerDestroyBlock(
                player_id, pos, particle=True, send_inv_update=i == last_index
            )
    finally:
        player_digging_poses.pop(player_id, None)


@DestroyBlockEvent.Listen()
def onDestroyBlock(event):
    # type: (DestroyBlockEvent) -> None
    if (
        event.playerId in player_digging_poses
        and (event.x, event.y, event.z) in player_digging_poses[event.playerId]
    ):
        return
    mhitem = GetPlayerMainhandItem(event.playerId)
    if mhitem is None or mhitem.id not in MINING_HAMMERS or mhitem.durability is None:
        return
    if (
        "minecraft:is_pickaxe_item_destructible" not in GetBlockTags(event.fullName)
        and (GetBlockBasicInfo(event.fullName).tier or {}).get("digger") != 1
    ):
        return
    x = event.x
    y = event.y
    z = event.z
    face = event.face
    if face == 0 or face == 1:
        poses = [
            (_x, y, _z)
            for _x in range(x - 1, x + 2)
            for _z in range(z - 1, z + 2)
            if _x != x or _z != z
        ]
    elif face == 2 or face == 3:
        poses = [
            (_x, _y, z)
            for _x in range(x - 1, x + 2)
            for _y in range(y - 1, y + 2)
            if _x != x or _y != y
        ]
    elif face == 4 or face == 5:
        poses = [
            (x, _y, _z)
            for _y in range(y - 1, y + 2)
            for _z in range(z - 1, z + 2)
            if _y != y or _z != z
        ]
    else:
        return
    chain_mine(event.playerId, event.dimensionId, event.fullName, poses)


