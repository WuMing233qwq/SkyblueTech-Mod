# coding=utf-8
from skybluetech_scripts.tooldelta.define import Item
from skybluetech_scripts.tooldelta.api.server import (
    GetPlayersInDim,
    GetPos,
    GetBlockEntityData,
    SpawnDroppedItem,
    UpdateBlockStates,
    SpawnItemToPlayerCarried,
)
from skybluetech_scripts.tooldelta.events.server import (
    ServerItemUseOnEvent,
    ServerBlockUseEvent,
    BlockRemoveServerEvent,
)
from skybluetech_scripts.tooldelta.events.notify import NotifyToClients
from ...common.define.id_enum.blocks import FAMICOM
from ...common.events.misc.famicom import FamicomPlaySoundEvent

MUSIC_MAPPING = {
    "skybluetech:famicom_cartidge_1": "music.skybluetech.famicom_1",
    "skybluetech:famicom_cartidge_2": "music.skybluetech.famicom_2",
    "skybluetech:famicom_cartidge_3": "music.skybluetech.famicom_3",
}
STATE_MAPPING = {
    "skybluetech:famicom_cartidge_1": 1,
    "skybluetech:famicom_cartidge_2": 2,
    "skybluetech:famicom_cartidge_3": 3,
}
K_CARTIDGE_TYPE_STATE = "skybluetech:fc_rom_type"


@ServerBlockUseEvent.Listen()
def onBlockUse(event):
    # type: (ServerBlockUseEvent) -> None
    if event.blockName != FAMICOM:
        return
    bdata = GetBlockEntityData(event.dimensionId, (event.x, event.y, event.z))
    if bdata is None:
        return
    x = event.x
    y = event.y
    z = event.z
    cartidge = bdata["st:cartidge"]
    if cartidge is not None:
        removeCartidge(event.dimensionId, x, y, z, cartidge)
        bdata["st:cartidge"] = None


@ServerItemUseOnEvent.Listen()
def onUseItemOn(event):
    # type: (ServerItemUseOnEvent) -> None
    if event.blockName != FAMICOM:
        return
    bdata = GetBlockEntityData(event.dimensionId, (event.x, event.y, event.z))
    if bdata is None:
        return
    x = event.x
    y = event.y
    z = event.z
    cartidge = bdata["st:cartidge"]
    if cartidge is not None:
        removeCartidge(event.dimensionId, x, y, z, cartidge)
        bdata["st:cartidge"] = None
        return
    item = event.item
    music_mapping = MUSIC_MAPPING.get(item.id)
    if music_mapping is None:
        return
    inrange_players = [
        i
        for i in GetPlayersInDim(event.dimensionId)
        if all(abs(b - a) <= 32 for a, b in zip(GetPos(i), (x, y, z)))
    ]
    bdata["st:cartidge"] = item.id
    UpdateBlockStates(
        event.dimensionId,
        (x, y, z),
        {K_CARTIDGE_TYPE_STATE: STATE_MAPPING[item.id]},
    )
    NotifyToClients(
        inrange_players,
        FamicomPlaySoundEvent(event.dimensionId, x, y, z, music_mapping),
    )
    SpawnItemToPlayerCarried(event.entityId, Item("minecraft:air"))


def removeCartidge(dim, x, y, z, cartidge):
    # type: (int, int, int, int, str) -> None
    SpawnDroppedItem(dim, (x + 0.5, y, z + 0.5), Item(cartidge))
    music_mapping = MUSIC_MAPPING.get(cartidge)
    if music_mapping is None:
        return
    UpdateBlockStates(dim, (x, y, z), {K_CARTIDGE_TYPE_STATE: 0})
    inrange_players = [
        i
        for i in GetPlayersInDim(dim)
        if all(abs(b - a) <= 32 for a, b in zip(GetPos(i), (x, y, z)))
    ]
    NotifyToClients(
        inrange_players, FamicomPlaySoundEvent(dim, x, y, z, music_mapping, True)
    )


@BlockRemoveServerEvent.Listen()
def onBlockRemoved(event):
    # type: (BlockRemoveServerEvent) -> None
    if event.fullName != FAMICOM:
        return
    bdata = GetBlockEntityData(event.dimension, (event.x, event.y, event.z))
    if bdata is None:
        return
    x = event.x
    y = event.y
    z = event.z
    cartidge = bdata["st:cartidge"]
    if cartidge is not None:
        removeCartidge(event.dimension, x, y, z, cartidge)
