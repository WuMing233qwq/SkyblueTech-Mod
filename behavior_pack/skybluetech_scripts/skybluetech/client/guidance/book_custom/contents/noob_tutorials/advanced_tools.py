# coding=utf-8
from skybluetech_scripts.skybluetech.common.define import id_enum
from skybluetech_scripts.skybluetech.client.ui.recipe_checker import (
    CheckRecipe,
    CheckRecipes,
)
from ...define import (
    TextPage,
    MachineryWorkstationRecipePage,
    PageGroup,
)


advanced_tools = PageGroup(
    "advanced_tools",
    [
        TextPage(
            "合金和工具",
            '接下来就是制作各种<text color="§9" t="合金">， 这意味着你需要制作一个<item id="{alloy_furnace}"><link id="alloy_furnace" text="合金炉">。 你可以在合金炉里查看合金炉可进行的所有配方， 也可以随意点击配方内的合金锭产物来看看<text color="§6" t="它们都能做成什么东西">。'.format(
                alloy_furnace=id_enum.ALLOY_FURNACE,
            ),
            hyperlink_cbs={
                "alloy_furnace": lambda _: CheckRecipe(id_enum.ALLOY_FURNACE),
            },
        ),
        TextPage(
            "",
            '你可以用<item id="{bronze_ingot}">青铜锭和<item id="{invar_ingot}">殷钢锭来合成比铁工具更趁手的<item id="{bronze_pickaxe}"><link id="bronze_tools" text="青铜工具">和<item id="{invar_pickaxe}"><link id="invar_tools" text="殷钢工具">， 它们相比铁质工具具更耐用、 更灵活， 杀伤力也更高。'.format(
                bronze_ingot=id_enum.Ingots.BRONZE,
                invar_ingot=id_enum.Ingots.INVAR,
                bronze_pickaxe=id_enum.MetalTools.BRONZE_PICKAXE,
                invar_pickaxe=id_enum.MetalTools.INVAR_PICKAXE,
            ),
            hyperlink_cbs={
                "bronze_tools": lambda _: CheckRecipes([
                    id_enum.MetalTools.BRONZE_AXE,
                    id_enum.MetalTools.BRONZE_PICKAXE,
                    id_enum.MetalTools.BRONZE_SHOVEL,
                    id_enum.MetalTools.BRONZE_SWORD,
                    id_enum.MetalTools.BRONZE_HOE,
                ]),
                "invar_tools": lambda _: CheckRecipes([
                    id_enum.MetalTools.INVAR_AXE,
                    id_enum.MetalTools.INVAR_PICKAXE,
                    id_enum.MetalTools.INVAR_SHOVEL,
                    id_enum.MetalTools.INVAR_SWORD,
                    id_enum.MetalTools.INVAR_HOE,
                ]),
            },
        ),
    ],
)
