# coding=utf-8
from ..define.id_enum import GAS_BURNING_GENERATOR, METHANE
from ..mini_jei.core import RecipesCollection
from ..mini_jei.machinery.gas_burning_generator import (
    GeneratorRecipe,
    GasBurningGeneratorRecipe,
)

MAX_INPUT_GAS_VOLUME = 2000
MAX_OUTPUT_GAS_VOLUME = 2000
STORE_RF_MAX = 28800


recipes = RecipesCollection(
    GAS_BURNING_GENERATOR,
    GasBurningGeneratorRecipe(METHANE, 4, 160),
)  # type: RecipesCollection[GeneratorRecipe]
