# coding=utf-8
#
from .actions.register import RegisterTool


ITEM_ID = "skybluetech:skyblue_hoe"
DIRTLIKE_BLOCK = {"minecraft:dirt", "minecraft:grass_block"}
HOE_POWER_COST = 200


RegisterTool(ITEM_ID)
