# coding=utf-8
from ..define import id_enum, tag_enum
from ..mini_jei.machinery.template_assembler import (
    TemplateAssemblerRecipe,
    TemplateAssemblerRecipesCollection,
    Input,
)

STORE_RF_MAX = 16000

recipes = TemplateAssemblerRecipesCollection(
    TemplateAssemblerRecipe(
        {
            0: Input(id_enum.Upgraders.EMPTY, 1),
            1: Input(id_enum.REDSTONEFLUX_CORE, 2),
            2: Input(id_enum.Sticks.COPPER, 2),
            3: Input(id_enum.Plates.GOLD, 1),
            4: Input(tag_enum.RUBBER, 1, is_tag=True),
            5: Input(id_enum.ControlCircuit.BASIC, 1),
        },
        id_enum.Upgraders.BASIC_ENERGY_UPGRADER,
        power_cost=60,
        tick_duration=120,
    ),
    TemplateAssemblerRecipe(
        {
            0: Input(id_enum.Upgraders.EMPTY, 1),
            1: Input("minecraft:redstone", 2),
            2: Input(id_enum.DEACTIVATION_REDSTONE, 2),
            3: Input(id_enum.Coils.COPPER),
            4: Input(tag_enum.PlateTag.CUPRONICKEL, 2, is_tag=True),
            5: Input(id_enum.ControlCircuit.BASIC, 1),
        },
        id_enum.Upgraders.BASIC_SPEED_UPGRADER,
        power_cost=60,
        tick_duration=120,
    ),
)
