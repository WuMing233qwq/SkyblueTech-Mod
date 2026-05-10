# coding=utf-8
from skybluetech_scripts.tooldelta.events.server import CustomCommandTriggerServerEvent
from ...common.events.misc.block_geometry_test import BlockGeometryTest
from .register import RegisterCommand
from .utils import generate_simple_arg_mapping


@RegisterCommand("skybluetech:block_geometry_test")
def onCommand(event):
    # type: (CustomCommandTriggerServerEvent) -> None
    args = generate_simple_arg_mapping(event.args)
    start_x, start_y, start_z = tuple(int(i) for i in args["start"])
    end_x, end_y, end_z = tuple(int(i) for i in args["end"])
    display_x, display_y, display_z = tuple(int(i) for i in args["display_pos"])
    player_id = event.origin.get("entityId")
    if player_id is not None:
        BlockGeometryTest(
            (start_x, start_y, start_z),
            (end_x, end_y, end_z),
            (display_x, display_y, display_z),
        ).send(player_id)

    event.SetReturnMsg("%commands.skybluetech.block_geometry_test.success")
