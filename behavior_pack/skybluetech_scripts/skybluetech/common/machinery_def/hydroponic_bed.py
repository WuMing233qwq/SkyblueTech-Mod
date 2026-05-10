# coding=utf-8
from ..mini_jei.machinery.hydroponic_bed import (
    HydroponicBedRecipe,
    HydroponicBedRecipesCollection,
    Output,
)

K_GROW_STAGE = "st:grow_stage"
K_STAGE_GROW_TICKS = "st:stage_grow_ticks"
K_WATER_STORE = "st:water_store"
K_CROP_BLOCK_ID = "st:crop_block_id"
WORK_TICK_DELAY = 5
POWER_COST = 4
ONCE_WATER_COST = 5
MAX_WATER_STORE = 1000

# NOTE: 添加作物时, 如果种子和收获一致, 且收获数量随机
#       则 OutputList 为空
#       且需要补充 ProbList

recipes = HydroponicBedRecipesCollection({
    "minecraft:wheat_seeds": HydroponicBedRecipe(
        "minecraft:wheat",
        "minecraft:wheat_seeds",
        100,
        8,
        [0.1016, 0.3484, 0.3982, 0.1517],
        [Output("minecraft:wheat")],
    ),
    "minecraft:carrot": HydroponicBedRecipe(
        "minecraft:carrots",
        "minecraft:carrot",
        100,
        8,
        [0.1016, 0.3484, 0.3982, 0.1517],
        [],
    ),
    "minecraft:potato": HydroponicBedRecipe(
        "minecraft:potatoes",
        "minecraft:potato",
        100,
        8,
        [0.1016, 0.3484, 0.3982, 0.1517],
        [],
    ),
    "minecraft:beetroot_seeds": HydroponicBedRecipe(
        "minecraft:beetroot",
        "minecraft:beetroot_seeds",
        100,
        8,
        [0.1016, 0.3484, 0.3982, 0.1517],
        [Output("minecraft:beetroot")],
    ),
})
