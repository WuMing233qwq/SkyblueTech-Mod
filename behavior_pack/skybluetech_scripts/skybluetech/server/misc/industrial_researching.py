# coding=utf-8
import time
from mod.server.extraServerApi import GetMinecraftEnum
from mod_log import logger
from skybluetech_scripts.tooldelta.define import Item
from skybluetech_scripts.tooldelta.api.server import (
    GetAllInventoryItems,
    GetExtraData,
    GetSeed,
    SetExtraData,
    SetOnePopupNotice,
    SetPlayerAllItems,
)
from skybluetech_scripts.tooldelta.events.service import ServerListenerService
from skybluetech_scripts.tooldelta.utils import nbt
from skybluetech_scripts.skybluetech.common.define.id_enum import INSCRIBING_TEMPLATE
from skybluetech_scripts.skybluetech.common.events.misc.industrial_researching import (
    IndustrialResearchingInscribeRequest,
    IndustrialResearchingQueryRequest,
    IndustrialResearchingQueryResponse,
    IndustrialResearchingSubmitRequest,
)
from skybluetech_scripts.skybluetech.common.misc.industrial_researching import (
    all_researchings,
)
from skybluetech_scripts.skybluetech.common.misc.inscribing_template import (
    GetTemplateGraph,
    K_UD_TEMPLATE_GRAPH,
)


ItemPosType = GetMinecraftEnum().ItemPosType
VALID_RESEARCHING_ITEM_IDS = set(
    recipe.result_item_id for recipe in all_researchings
)


class IndustrialResearchingPlayerMgr(object):
    _instance = None
    _DATA_KEY = "st:researchings"

    def __init__(self):
        pass

    def record_researching(self, player_id, researching_id):
        # type: (str, str) -> None
        """
        记录玩家研究了某种可研究物。

        Args:
            player_id (str): 玩家 ID。
            researching_id (str): 可研究物 ID。为 IndustrialResearchingRecipe 的 result_item_id。
        """
        researchings = self.get_player_researchings(player_id)
        researchings[researching_id] = int(time.time())
        self._save_player_researchings(player_id, researchings)

    def has_researched(self, player_id, researching_id):
        # type: (str, str) -> bool
        """
        玩家是否研究了某种可研究物。

        Args:
            player_id (str): 玩家 ID。
            researching_id (str): 可研究物 ID。为 IndustrialResearchingRecipe 的 result_item_id。

        Returns:
            bool: 是否研究了。
        """
        return researching_id in self.get_player_researchings(player_id)

    def get_player_researchings(self, player_id):
        # type: (str) -> dict[str, int]
        """
        获取玩家所有已研究的物品。

        Args:
            player_id (str): 玩家 ID。

        Returns:
            dict[str, int]: 所有已研究的物品，键为 IndustrialResearchingRecipe 的 result_item_id，值为研究时间戳。
        """
        return GetExtraData(player_id, self._DATA_KEY) or {}

    def _save_player_researchings(self, player_id, researchings):
        # type: (str, dict[str, int]) -> None
        SetExtraData(player_id, self._DATA_KEY, researchings)

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance


class IndustrialResearchingQueryHandler(ServerListenerService):
    def __init__(self):
        ServerListenerService.__init__(self)
        self.enable_listeners()

    @ServerListenerService.Listen(IndustrialResearchingQueryRequest)
    def on_query_researchings(self, event):
        # type: (IndustrialResearchingQueryRequest) -> None
        researched_items = IndustrialResearchingPlayerMgr.instance().get_player_researchings(
            event.player_id
        )
        IndustrialResearchingQueryResponse(researched_items).send(event.player_id)

    @ServerListenerService.Listen(IndustrialResearchingSubmitRequest)
    def on_submit_researching(self, event):
        # type: (IndustrialResearchingSubmitRequest) -> None
        player_id = event.player_id
        item_id = event.item_id
        if item_id not in VALID_RESEARCHING_ITEM_IDS:
            logger.error("Industrial researching submit invalid item: %s" % item_id)
            SetOnePopupNotice(player_id, "§c研究失败")
            return
        mgr = IndustrialResearchingPlayerMgr.instance()
        if not mgr.has_researched(player_id, item_id):
            mgr.record_researching(player_id, item_id)
        IndustrialResearchingQueryResponse(
            mgr.get_player_researchings(player_id)
        ).send(player_id)

    @ServerListenerService.Listen(IndustrialResearchingInscribeRequest)
    def on_inscribe_template(self, event):
        # type: (IndustrialResearchingInscribeRequest) -> None
        player_id = event.player_id
        item_id = event.item_id
        if item_id not in VALID_RESEARCHING_ITEM_IDS:
            logger.error("Industrial researching inscribe invalid item: %s" % item_id)
            SetOnePopupNotice(player_id, "§c刻印失败")
            return
        if not IndustrialResearchingPlayerMgr.instance().has_researched(
            player_id, item_id
        ):
            SetOnePopupNotice(player_id, "§c尚未研究该物品，无法刻印")
            return
        try:
            if self.inscribe_template(player_id, item_id):
                SetOnePopupNotice(player_id, "§a刻印成功")
            else:
                SetOnePopupNotice(player_id, "§6背包中没有单个空刻印模版")
        except Exception as err:
            logger.error(
                "Industrial researching inscribe failed: %s %s %s"
                % (player_id, item_id, err)
            )
            SetOnePopupNotice(player_id, "§c刻印失败")

    def inscribe_template(self, player_id, item_id):
        # type: (str, str) -> bool
        for slot, item in GetAllInventoryItems(player_id, get_userdata=True).items():
            if not self.is_empty_inscribing_template(item):
                continue
            graph = GetTemplateGraph(item_id, GetSeed())
            user_data = item.userData or {}
            user_data[K_UD_TEMPLATE_GRAPH] = [nbt.Int(i) for i in graph]
            user_data["display"] = {
                "Lore": [
                    nbt.String(
                        "§r§d已刻录： " + Item(item_id).GetBasicInfo().itemName
                    )
                ]
            }
            item.userData = user_data
            SetPlayerAllItems(player_id, {
                (ItemPosType.INVENTORY, slot): item
            })
            return True
        return False

    def is_empty_inscribing_template(self, item):
        # type: (Item) -> bool
        if item.id != INSCRIBING_TEMPLATE or item.count != 1:
            return False
        graph_nbt = (item.userData or {}).get(K_UD_TEMPLATE_GRAPH)
        if graph_nbt is None:
            return True
        graph = nbt.NBT2Py(graph_nbt)
        return (
            isinstance(graph, list)
            and len(graph) == 25
            and all(i == 0 for i in graph)
        )


_query_handler = IndustrialResearchingQueryHandler()
