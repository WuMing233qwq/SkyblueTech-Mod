# coding=utf-8
from skybluetech_scripts.tooldelta.define.item import Item
from skybluetech_scripts.tooldelta.extensions.super_executor import SuperExecutorMeta
from ...common.define import flags
from ...common.define.id_enum.machinery import REPAIRING_ANVIL as MACHINE_ID
from ...common.machinery_def.redstone_generator import recipes as Recipes
from ...common.ui_sync.machinery.redstone_generator import RedstoneGeneratorUISync
from .basic import (
    GUIControl,
    MultiFluidContainer,
    UpgradeControl,
    RegisterMachine,
)

@RegisterMachine
class RepairingAnvil(GUIControl, MultiFluidContainer, UpgradeControl):
    block_name = MACHINE_ID

    @SuperExecutorMeta.execute_super
    def __init__(self, dim, x, y, z, block_entity_data):
        pass
