# coding=utf-8
import random
from skybluetech_scripts.skybluetech.common.define import id_enum
from ...misc.inscribing_template import GenerateInscribingTemplateByItemId
from .register import LootHandler, DoRand, PlayerLootHistoryManager


def _DropInscribingTemplate(
    playerId,  # type: str
    template_item_id,  # type: str
    chance,  # type: float
):
    item_id = id_enum.INSCRIBING_TEMPLATE
    actual_chance = chance
    loot_history = PlayerLootHistoryManager.instance()
    if loot_history.has(playerId, item_id, template_item_id):
        actual_chance = chance / 2.0
    if not DoRand(actual_chance):
        return None
    loot_history.record(playerId, item_id, template_item_id)
    return GenerateInscribingTemplateByItemId(template_item_id)


@LootHandler("loot_tables/chests/nether_bridge.json")
def handle_nether_bridge(
    playerId,  # type: str
):
    # 额外产出: 随机一个刻印模板, 目标物品为
    # - id_enum.Upgraders.BASIC_SPEED_UPGRADER
    # - id_enum.Upgraders.BASIC_ENERGY_UPGRADER
    items = []
    item = _DropInscribingTemplate(
        playerId,
        random.choice([
            id_enum.Upgraders.BASIC_SPEED_UPGRADER,
            id_enum.Upgraders.BASIC_ENERGY_UPGRADER,
        ]),
        0.4,
    )
    if item:
        items.append(item)
    item = _DropInscribingTemplate(
        playerId,
        random.choice([
            id_enum.ObjectUpgraders.AUTO_BURNING,
            id_enum.ObjectUpgraders.DIGSPEED,
        ]),
        0.4,
    )
    if item:
        items.append(item)
    return items


@LootHandler("loot_tables/chests/abandoned_mineshaft.json")
def handle_abandoned_mineshaft(
    playerId,  # type: str
):
    items = []
    item = _DropInscribingTemplate(
        playerId,
        id_enum.ObjectUpgraders.VEINMINER,
        0.8,
    )
    if item:
        items.append(item)
    return items
