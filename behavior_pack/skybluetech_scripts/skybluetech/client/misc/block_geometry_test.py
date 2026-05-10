# coding=utf-8
from mod_log import logger
from skybluetech_scripts.tooldelta.api.client import (
    CombineBlockPaletteToGeometry,
    AddActorBlockGeometry,
    GetBlockPaletteBetweenPos,
    CreateClientEntity,
    DestroyClientEntity,
)
from skybluetech_scripts.tooldelta.api.common import Delay
from ...common.events.misc.block_geometry_test import BlockGeometryTest


@BlockGeometryTest.Listen()
def onRecvTest(event):
    # type: (BlockGeometryTest) -> None
    pal = GetBlockPaletteBetweenPos(event.start_pos, event.end_pos, eliminateAir=False)
    geo_id = CombineBlockPaletteToGeometry(pal, "geometry.block_geometry.test")
    entity_id = CreateClientEntity(
        "skybluetech:model_entity", event.display_pos, (0, 0)
    )
    if entity_id is not None:
        res = AddActorBlockGeometry(entity_id, geo_id, rotation=(0, 180, 0))
        remove_later(entity_id)
        if not res:
            logger.error("AddActorBlockGeometry failed")
    else:
        logger.error("CreateClientEntity failed")


@Delay(30)
def remove_later(entity_id):
    # type: (str) -> None
    DestroyClientEntity(entity_id)
