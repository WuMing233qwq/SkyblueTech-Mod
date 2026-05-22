# coding=utf-8
from ..define.id_enum import CYRO_HEAT_MELTING_CHAMBER
from ..define.id_enum import fluids, items
from ..mini_jei.machinery.cyro_heat_melting_chamber import (
    CyroHeatMeltingChamberRecipe,
    CyroHeatMeltingChamberRecipeCollection,
    c2k,
)


recipes = CyroHeatMeltingChamberRecipeCollection(
    CYRO_HEAT_MELTING_CHAMBER,
    CyroHeatMeltingChamberRecipe(
        items.ROSIN,
        fluids.Molten.ROSIN,
        144,
        c2k(60),
        c2k(70),
        c2k(80),
        tick_duration=200,
        max_tick_speed=4,
        waste=items.Dusts.CARBON,
    ),
)
