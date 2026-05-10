# coding=utf-8
from ..mini_jei.machinery.hydroponic_bed_sand import (
    HydroponicBedSandRecipe,
    HydroponicBedSandRecipesCollection,
    Output,
)

K_GROW_PROGRESS = "st:grow_progress"
K_WATER_STORE = "st:water_store"
K_CROP_BLOCK_ID = "st:crop_block_id"
POWER_COST = 4
ONCE_WATER_COST = 5
MAX_WATER_STORE = 1000
WORK_TICK_DELAY = 20


recipes = HydroponicBedSandRecipesCollection({
    "minecraft:cactus": HydroponicBedSandRecipe(
        "minecraft:cactus",
        "minecraft:cactus",
        0.1,
        [Output("minecraft:cactus")],
    ),
    "minecraft:sugar_cane": HydroponicBedSandRecipe(
        "minecraft:reeds",
        "minecraft:sugar_cane",
        0.1,
        [Output("minecraft:sugar_cane")],
    ),
})
