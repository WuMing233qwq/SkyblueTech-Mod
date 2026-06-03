# coding=utf-8
import random
from skybluetech_scripts.tooldelta.define import Item
from skybluetech_scripts.skybluetech.common.define import id_enum
from .register import LootHandler, DoRand


@LootHandler("loot_tables/chests/village_blacksmith.json")
def handle_village_blacksmith(
    playerId,  # type: str
):
    # 额外产出:
    # - id_enum.Ingots.TIN(1-6)
    # - id_enum.METAL_HAMMER(随机耐久)
    # - id_enum.Wrench.IRON(1-6)
    # - id_enum.Pincer.IRON(1-6)
    # - id_enum.Ingots.SILVER(1-6)
    # - id_enum.Ingots.LEAD(1-6)
    itemList = []
    if DoRand(0.8):
        itemList.append(
            Item(
                id_enum.Ingots.TIN,
                random.randint(1, 6),
                0,
            )
        )
    if DoRand(0.75):
        itemList.append(
            Item(
                id_enum.METAL_HAMMER,
                durability=random.randint(0, 90),
            )
        )
    if DoRand(0.5):
        itemList.append(
            Item(
                id_enum.Wrench.IRON,
                random.randint(1, 6),
                0,
            )
        )
    if DoRand(0.5):
        itemList.append(
            Item(
                id_enum.Pincer.IRON,
                random.randint(1, 6),
                0,
            )
        )
    if DoRand(0.3):
        itemList.append(
            Item(
                id_enum.Ingots.LEAD,
                random.randint(1, 6),
                0,
            )
        )
    if DoRand(0.1):
        itemList.append(
            Item(
                id_enum.Ingots.SILVER,
                random.randint(1, 6),
                0,
            )
        )
    return itemList
