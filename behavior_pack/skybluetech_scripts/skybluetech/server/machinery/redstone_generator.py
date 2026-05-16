# coding=utf-8
from skybluetech_scripts.tooldelta.define.item import Item
from skybluetech_scripts.tooldelta.extensions.super_executor import SuperExecutorMeta
from ...common.define import flags
from ...common.define.id_enum.machinery import REDSTONE_GENERATOR as MACHINE_ID
from ...common.machinery_def.redstone_generator import recipes as Recipes, STORE_RF_MAX
from .basic import (
    GeneratorProcessor,
    RegisterMachine,
)

K_BURN_TICKS_LEFT = "st:burn_ticks_left"
K_MAX_BURN_TICKS = "st:max_burn_ticks"
K_LAST_BURNING_ITEM = "st:last_burning_item"


@RegisterMachine
class RedstoneGenerator(GeneratorProcessor):
    block_name = MACHINE_ID
    store_rf_max = STORE_RF_MAX
    dump_progress_to_block_entity_data = True
    process_item = True
    recipes = Recipes
    input_slots = (0,)
    output_slots = (1,)
