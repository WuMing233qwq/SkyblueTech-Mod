# coding=utf-8
from skybluetech_scripts.tooldelta.events.server import CustomCommandTriggerServerEvent
from .register import RegisterCommand
from .utils import generate_simple_arg_mapping


@RegisterCommand("skybluetech:industrial_research_cancel")
def onCommand(event):
    # type: (CustomCommandTriggerServerEvent) -> None
    from ..misc.industrial_researching import (
        IndustrialResearchingPlayerMgr,
        VALID_RESEARCHING_ITEM_IDS,
    )
    from ...common.events.misc.industrial_researching import (
        IndustrialResearchingQueryResponse,
    )

    player_id = event.origin.get("entityId")
    if player_id is None:
        event.SetReturnMsg("%commands.generic.noTargetMatch")
        event.SetReturnFailed()
        return

    args = generate_simple_arg_mapping(event.args)
    item_arg = args.get("itemId", {})
    if isinstance(item_arg, dict):
        item_id = item_arg.get("itemName", "")
    else:
        item_id = item_arg

    if item_id not in VALID_RESEARCHING_ITEM_IDS:
        event.SetReturnMsg("%commands.skybluetech.industrial_research_cancel.invalid_item")
        event.SetReturnParams(str(item_id))
        event.SetReturnFailed()
        return

    mgr = IndustrialResearchingPlayerMgr.instance()
    if not mgr.cancel_researching(player_id, item_id):
        event.SetReturnMsg("%commands.skybluetech.industrial_research_cancel.not_researched")
        event.SetReturnParams(item_id)
        event.SetReturnFailed()
        return

    IndustrialResearchingQueryResponse(
        mgr.get_player_researchings(player_id)
    ).send(player_id)
    event.SetReturnMsg("%commands.skybluetech.industrial_research_cancel.success")
    event.SetReturnParams(item_id)
