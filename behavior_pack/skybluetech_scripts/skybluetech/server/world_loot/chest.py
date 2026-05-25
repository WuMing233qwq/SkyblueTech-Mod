# coding=utf-8
import random
from skybluetech_scripts.tooldelta.define import Item
from skybluetech_scripts.tooldelta.events.server import (
    OnContainerFillLoottableServerEvent,
)
from skybluetech_scripts.skybluetech.common.define import id_enum
from ..misc.inscribing_template import GenerateInscribingTemplateByItemId

PREFIX_LENGTH = len("loot_tables/chests/")
SUFFIX_LENGTH = len(".json")

# loot_tables/chests/nether_bridge.json


class ChestLootTableHandler(object):
    def __init__(self):
        self.mapping = {
            "village_blacksmith": self.handle_village_blacksmith,
            "monster_room": self.handle_monster_room,
            "nether_bridge": self.handle_nether_bridge,
        }

    def handle_village_blacksmith(self, event):
        # type: (OnContainerFillLoottableServerEvent) -> None
        if random.random() < 0.8:
            event.itemList.append(
                Item(
                    id_enum.Ingots.TIN,
                    random.randint(1, 6),
                    0,
                ).marshal()
            )
        if random.random() < 0.75:
            event.itemList.append(
                Item(
                    id_enum.METAL_HAMMER,
                    durability=random.randint(0, 90),
                ).marshal()
            )
        if random.random() < 0.5:
            event.itemList.append(
                Item(
                    id_enum.Wrench.IRON,
                    random.randint(1, 6),
                    0,
                ).marshal()
            )
        if random.random() < 0.5:
            event.itemList.append(
                Item(
                    id_enum.Pincer.IRON,
                    random.randint(1, 6),
                    0,
                ).marshal()
            )
        if random.random() < 0.3:
            event.itemList.append(
                Item(
                    id_enum.Ingots.SILVER,
                    random.randint(1, 6),
                    0,
                ).marshal()
            )
        if random.random() < 0.1:
            event.itemList.append(
                Item(
                    id_enum.Ingots.LEAD,
                    random.randint(1, 6),
                    0,
                ).marshal()
            )

    def handle_monster_room(self, event):
        # type: (OnContainerFillLoottableServerEvent) -> None
        if random.random() < 0.5:
            items = [
                id_enum.FamicomCartidges.YELLOW,
                id_enum.FamicomCartidges.PURPLE,
                id_enum.FamicomCartidges.BLUE,
            ]
            random.shuffle(items)
            event.itemList.append(Item(items[0]).marshal())

    def handle_nether_bridge(self, event):
        # type: (OnContainerFillLoottableServerEvent) -> None
        if random.random() < 0.4:
            event.itemList.append(
                GenerateInscribingTemplateByItemId(
                    random.choice([
                        id_enum.Upgraders.BASIC_SPEED_UPGRADER,
                        id_enum.Upgraders.BASIC_ENERGY_UPGRADER,
                    ]),
                ).marshal()
            )


instance = ChestLootTableHandler()


@OnContainerFillLoottableServerEvent.Listen()
def onContainerLoot(event):
    # type: (OnContainerFillLoottableServerEvent) -> None
    hdl = instance.mapping.get(event.loottable[PREFIX_LENGTH:-SUFFIX_LENGTH])
    if hdl:
        hdl(event)
        event.SetDirty()
