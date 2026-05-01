# coding=utf-8
import time
from mod.server.extraServerApi import GetLevelId
from skybluetech_scripts.tooldelta.define import Item
from skybluetech_scripts.tooldelta.api.server import (
    GetExtraData,
    SetExtraData,
    SpawnItemToPlayerInv,
)
from skybluetech_scripts.tooldelta.extensions.player_loader_utils import (
    AddPlayerCompletelyLoadedServerCallback,
)
from skybluetech_scripts.skybluetech.common.define.id_enum import GUIDANCE

EX_DATA_KEY = "st:player_inited"


def onPlayerLoaded(player_id):
    # type: (str) -> None
    players_loaded = GetExtraData(GetLevelId(), EX_DATA_KEY, {})
    if player_id not in players_loaded:
        players_loaded[player_id] = time.time()
        SetExtraData(GetLevelId(), EX_DATA_KEY, players_loaded)
        SpawnItemToPlayerInv(player_id, Item(GUIDANCE))


AddPlayerCompletelyLoadedServerCallback(onPlayerLoaded)
