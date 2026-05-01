# coding=utf-8
from skybluetech_scripts.skybluetech.common.define import id_enum
from skybluetech_scripts.skybluetech.client.ui.recipe_checker import (
    CheckRecipe,
    CheckUsage,
    PushRecipeCheckerUI,
)
from ...define import (
    TextPage,
    MachineryWorkstationRecipePage,
    PageGroup,
)

page_todo = PageGroup(
    "todo", [TextPage("未完待续...", "未完待续..说不定在下周你就能看到这章更新了！")]
)
