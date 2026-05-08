# coding=utf-8
# coding=utf-8
from skybluetech_scripts.tooldelta.events.server import (
    DelServerPlayerEvent,
    OnSimTickServerEvent,
    ClientLoadAddonsFinishServerEvent,
)
from .define import PlayerKit

pool = {}  # type: dict[str, PlayerKit]
ticks = 0


def GetPlayer(player_id):
    # type: (str) -> PlayerKit | None
    return pool.get(player_id)


@OnSimTickServerEvent.Listen()
def onServerTick(event):
    # type: (OnSimTickServerEvent) -> None
    global ticks
    ticks += 1
    if ticks % 40 == 0:
        for player in pool.values():
            player.run_charge_once()


@ClientLoadAddonsFinishServerEvent.Listen()
def onAddPlayer(event):
    # type: (ClientLoadAddonsFinishServerEvent) -> None
    pool[event.playerId] = PlayerKit(event.playerId)


@DelServerPlayerEvent.Listen()
def onDelPlayer(event):
    # type: (DelServerPlayerEvent) -> None
    player = pool.pop(event.id, None)
    if player is not None:
        player.destroy()
