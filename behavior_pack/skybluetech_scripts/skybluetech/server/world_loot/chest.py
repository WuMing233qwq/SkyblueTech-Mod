# coding=utf-8
import random
from skybluetech_scripts.tooldelta.define import Item
from skybluetech_scripts.tooldelta.events.server import (
    OnContainerFillLoottableServerEvent,
)
from skybluetech_scripts.skybluetech.common.define import id_enum

PREFIX_LENGTH = len("loot_tables/chests/")
SUFFIX_LENGTH = len(".json")


class ChestLootTableHandler(object):
    def __init__(self):
        self.mapping = {
            "village_black_smith": self.handle_village_black_smith,
        }

    def handle_village_black_smith(self, event):
        # type: (OnContainerFillLoottableServerEvent) -> None
        if random.random() < 0.8:
            event.itemList.append(
                Item(
                    id_enum.Ingots.TIN,
                    random.randint(1, 6),
                    0,
                )
            )
        if random.random() < 0.75:
            event.itemList.append(
                Item(
                    id_enum.METAL_HAMMER,
                    durability=random.randint(0, 90),
                )
            )
        if random.random() < 0.5:
            event.itemList.append(
                Item(
                    id_enum.Wrench.IRON,
                    random.randint(1, 6),
                    0,
                )
            )
        if random.random() < 0.5:
            event.itemList.append(
                Item(
                    id_enum.Pincer.IRON,
                    random.randint(1, 6),
                    0,
                )
            )
        if random.random() < 0.3:
            event.itemList.append(
                Item(
                    id_enum.Ingots.SILVER,
                    random.randint(1, 6),
                    0,
                )
            )
        if random.random() < 0.1:
            event.itemList.append(
                Item(
                    id_enum.Ingots.LEAD,
                    random.randint(1, 6),
                    0,
                )
            )


instance = ChestLootTableHandler()


@OnContainerFillLoottableServerEvent.Listen()
def onContainerLoot(event):
    # type: (OnContainerFillLoottableServerEvent) -> None
    hdl = instance.mapping.get(event.loottable[PREFIX_LENGTH:-SUFFIX_LENGTH])
    if hdl:
        hdl(event)
        event.SetDirty()
