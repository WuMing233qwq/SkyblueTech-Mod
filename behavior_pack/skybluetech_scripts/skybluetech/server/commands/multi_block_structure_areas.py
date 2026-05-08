# coding=utf-8
from skybluetech_scripts.tooldelta.events.server import CustomCommandTriggerServerEvent
from ..machinery.basic.multi_block_structure import detect_areas
from .register import RegisterCommand


@RegisterCommand("skybluetech:query_areas")
def onCommand(event):
    # type: (CustomCommandTriggerServerEvent) -> None
    detect_areas_str = "\n".join(
        "[%d]: \n  %s"
        % (
            dim,
            "\n  ".join(
                "%d %d %d ~ %d %d %d"
                % (a.min_x, a.min_y, a.min_z, a.max_x, a.max_y, a.max_z)
                for a in area
            ),
        )
        for dim, area in detect_areas.items()
    )
    event.SetReturnMsg("commands.skybluetech.query_areas.success")
    event.SetReturnParams(str(len(detect_areas)), detect_areas_str)
