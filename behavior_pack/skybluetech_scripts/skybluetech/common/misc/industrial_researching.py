# coding=utf-8
from ...common.define import id_enum
from ..mini_jei.core import RecipesCollection
from ..mini_jei.misc.industrial_researching import IndustrialResearchingRecipe, Input

all_researchings = RecipesCollection(
    "IndustrialResearching",
    IndustrialResearchingRecipe(
        [
            Input("minecraft:string", 32),
            Input(id_enum.Sticks.INVAR, 16),
            Input("minecraft:redstone", 4),
        ],
        15,
        id_enum.Upgraders.GENERIC_FILTER_DEFAULT,
    ),
    IndustrialResearchingRecipe(
        [
            Input(id_enum.Coils.COPPER, 24),
            Input(id_enum.Sticks.COPPER, 20),
            Input("minecraft:redstone", 16),
            Input("minecraft:red_nether_brick", 10),
            Input("minecraft:magma", 8),
        ],
        12,
        id_enum.Upgraders.SPEC_MAGMA_FACTORY,
    ),
    IndustrialResearchingRecipe(
        [
            Input(id_enum.Sticks.STEEL, 32),
            Input(id_enum.Sticks.BRONZE, 28),
            Input("minecraft:redstone", 24),
            Input("minecraft:sticky_piston", 16),
            Input("minecraft:scaffolding", 10),
        ],
        24,
        id_enum.Upgraders.GENERIC_EXPANSION_UPGRADER,
    ),
    IndustrialResearchingRecipe(
        [
            Input("minecraft:furnace", 18),
            Input("skybluetech:deactivation_redstone", 16),
            Input(id_enum.HEAT_PLATE, 12),
        ],
        16,
        id_enum.ObjectUpgraders.AUTO_BURNING,
    ),
    IndustrialResearchingRecipe(
        [
            Input("minecraft:lapis_block", 20),
            Input(id_enum.Plates.PLATINUM, 16),
            Input(id_enum.Plates.SILVER, 16),
            Input(id_enum.Sticks.SILVER, 16),
            Input(id_enum.ControlCircuit.ADVANCED, 4),
        ],
        30,
        id_enum.ObjectUpgraders.FORTUNE,
    ),
    IndustrialResearchingRecipe(
        [
            Input("minecraft:sticky_piston", 14),
            Input("minecraft:iron_pickaxe", 12),
            Input(id_enum.ELECTRIC_MOTOR, 8),
            Input(id_enum.DRILL_TOP_STEEL, 4),
        ],
        8,
        id_enum.ObjectUpgraders.VEINMINER,
    ),
    IndustrialResearchingRecipe(
        [
            Input("minecraft:piston", 14),
            Input("minecraft:iron_hoe", 8),
            Input("minecraft:hay_block", 6),
            Input(id_enum.ELECTRIC_MOTOR, 5),
        ],
        8,
        id_enum.ObjectUpgraders.SPEC_FARMING,
    ),
)
