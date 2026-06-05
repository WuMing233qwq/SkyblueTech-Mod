# coding=utf-8
from skybluetech_scripts.tooldelta.define import Item
from skybluetech_scripts.tooldelta.api.client import GetBlockEntityData
from skybluetech_scripts.tooldelta.extensions.rate_limiter import PlayerRateLimiter
from skybluetech_scripts.tooldelta.ui import RegistToolDeltaScreen
from skybluetech_scripts.tooldelta.utils.nbt import GetValueWithDefault as GetValue
from skybluetech_scripts.skybluetech.common.events.machinery.machinery_workstation import (
    MachineryWorkstationDoCraft,
)
from skybluetech_scripts.skybluetech.common.machinery_def.machinery_workstation import (
    recipes,
    K_CRAFTING_PROGRESS,
    K_OUTPUT_ITEM_ID,
)
from ..recipe_checker import AsRecipeCheckerBtn
from .define import MachinePanelUIProxy, MAIN_PATH
from .utils import UpdateGenericProgressL2R


WARNING_BAR_DISPLAY_THRESOLD = 0.8

CRAFT_BTN_PATH = MAIN_PATH / "craft_btn"
CRAFT_SPEED_BAR_PATH = MAIN_PATH / "craft_speed_bar"
WARNING_BAR_PATH = MAIN_PATH / "warning_bar"
PRGS_PATH = MAIN_PATH / "progress"
RESEARCHING_BTN_PATH = MAIN_PATH / "researching_btn"
OUTPUT_ITEM_PREVIEWER_PATH = (
    MAIN_PATH / "output_slot/slot/item_cell_overlay_ref/item_renderer"
)

craft_hi_freq_limiter = PlayerRateLimiter(0.1)


@RegistToolDeltaScreen("MachineryWorkstationUI.main", is_proxy=True)
class MachineryWorkstationUI(MachinePanelUIProxy):
    def OnCreate(self):
        self.craft_strength = 0.0
        self.warning_bar_shown = False
        self.warning_bar_display_time = 0
        self.craft_btn = (
            self.GetElement(CRAFT_BTN_PATH).asButton().SetCallback(self.onClickCraftBtn)
        )
        self.researching_btn = (
            self
            .GetElement(RESEARCHING_BTN_PATH)
            .asButton()
            .SetCallback(self.onClickResearchingBtn)
        )
        self.craft_speed_bar = self.GetElement(CRAFT_SPEED_BAR_PATH).asImage()
        self.warning_bar = self.GetElement(WARNING_BAR_PATH)
        self.output_item_previewer = self.GetElement(
            OUTPUT_ITEM_PREVIEWER_PATH
        ).asItemRenderer()
        self.progress_bar = self.GetElement(PRGS_PATH)
        self.warning_bar.SetVisible(False)
        self.output_item_previewer.SetVisible(False)
        AsRecipeCheckerBtn(
            self.GetElement(MAIN_PATH / "recipe_check_btn").asButton(),
            recipes,
        )

    def onClickCraftBtn(self, _):
        _, x, y, z = self.pos
        if not craft_hi_freq_limiter.record():
            return
        data = GetBlockEntityData(x, y, z)
        if data is None:
            return
        output_item_id = GetValue(data["exData"], K_OUTPUT_ITEM_ID, None)
        if output_item_id is None:
            return
        self.craft_strength = min(1.0, self.craft_strength + 0.3)
        MachineryWorkstationDoCraft(x, y, z, self.craft_strength).send()

    def onClickResearchingBtn(self, _):
        from skybluetech_scripts.skybluetech.client.ui.misc.industrial_researching_ui import (
            IndustrialResearchProgressUI,
        )

        IndustrialResearchProgressUI.PushUI()

    def OnTicking(self):
        data = GetBlockEntityData(*self.pos[1:])
        if data is None:
            return
        data = data["exData"]
        output_item_id = GetValue(data, K_OUTPUT_ITEM_ID, None)
        progress = GetValue(data, K_CRAFTING_PROGRESS, 0.0)
        self.craft_strength = max(0.0, self.craft_strength - 0.01)
        self.warning_bar_display_time = max(0, self.warning_bar_display_time - 1)
        self.update_craft_speed_bar()
        if output_item_id is None:
            self.output_item_previewer.SetVisible(False)
        else:
            self.output_item_previewer.SetVisible(True)
            self.output_item_previewer.SetUiItem(Item(output_item_id))
            UpdateGenericProgressL2R(self.progress_bar, progress)

    def update_craft_speed_bar(self):
        self.craft_speed_bar.SetSpriteClipRatio(
            "fromRightToLeft",
            1 - self.craft_strength,
        )
        if self.craft_strength >= WARNING_BAR_DISPLAY_THRESOLD:
            self.warning_bar_display_time = 60
        if self.warning_bar_display_time > 0:
            if not self.warning_bar_shown:
                self.warning_bar.SetVisible(True)
                self.warning_bar_shown = True
        else:
            if self.warning_bar_shown:
                self.warning_bar.SetVisible(False)
                self.warning_bar_shown = False
