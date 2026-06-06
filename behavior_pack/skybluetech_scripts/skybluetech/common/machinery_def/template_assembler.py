# coding=utf-8
from ..define import id_enum, tag_enum
from ..mini_jei.machinery.template_assembler import (
    TemplateAssemblerRecipe,
    TemplateAssemblerRecipesCollection,
    Input,
)


STORE_RF_MAX = 16000
TEMPLATE_SLOT_INDEX = 9
K_TEMPLATE_ITEMS = "st:template_items"
K_TEMPLATE_ITEM_ID = "id"
K_TEMPLATE_ITEM_IS_TAG = "is_tag"
K_TEMPLATE_ITEM_COUNT = "count"

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
    TemplateAssemblerRecipe(
        {
            0: Input(id_enum.Upgraders.EMPTY, 1),
            1: Input("minecraft:sticky_piston", 5),
            2: Input("minecraft:observer", 2),
            3: Input(id_enum.ControlCircuit.ADVANCED, 1),
            4: Input(tag_enum.PlateTag.STEEL, 5, is_tag=True),
        },
        id_enum.Upgraders.GENERIC_EXPANSION_UPGRADER,
        power_cost=60,
        tick_duration=160,
    ),
    TemplateAssemblerRecipe(
        {
            0: Input(id_enum.Upgraders.EMPTY, 1),
            1: Input("minecraft:string", 8),
            2: Input(tag_enum.StickTag.INVAR, 8, is_tag=True),
            3: Input("minecraft:paper", 1),
            4: Input(tag_enum.PlateTag.STEEL, 4, is_tag=True),
        },
        id_enum.Upgraders.GENERIC_FILTER_DEFAULT,
        power_cost=60,
        tick_duration=120,
    ),
    TemplateAssemblerRecipe(
        {
            0: Input(id_enum.Upgraders.EMPTY, 1),
            1: Input("minecraft:string", 8),
            2: Input(tag_enum.StickTag.INVAR, 8, is_tag=True),
            3: Input("minecraft:paper", 1),
            4: Input(tag_enum.PlateTag.STEEL, 4, is_tag=True),
        },
        id_enum.Upgraders.GENERIC_FILTER_DEFAULT,
        power_cost=60,
        tick_duration=120,
    ),
    TemplateAssemblerRecipe(
        {
            0: Input(id_enum.Upgraders.EMPTY, 1),
            1: Input(id_enum.HEAT_PLATE, 4),
            2: Input(tag_enum.StickTag.COPPER, 4, is_tag=True),
            3: Input("minecraft:paper", 1),
            4: Input(tag_enum.PlateTag.STEEL, 4, is_tag=True),
        },
        id_enum.Upgraders.SPEC_MAGMA_FACTORY,
        power_cost=60,
        tick_duration=120,
    ),
)

_cached_graphs = {}  # type: dict[tuple[int, ...], str]


def _init_cached_graphs(world_seed):
    # type: (int) -> None
    if _cached_graphs:
        return
    from ..misc.inscribing_template import GetTemplateGraph

    for template_item_id in recipes.recipes_mapping:
        _cached_graphs[tuple(GetTemplateGraph(template_item_id, world_seed))] = (
            template_item_id
        )


def GetResultByTemplateGraph(graph, world_seed):
    # type: (list[int], int) -> str | None
    _init_cached_graphs(world_seed)
    return _cached_graphs.get(tuple(graph))
