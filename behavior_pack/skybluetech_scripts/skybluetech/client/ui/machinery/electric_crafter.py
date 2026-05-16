# coding=utf-8
from skybluetech_scripts.tooldelta.define import Item
from skybluetech_scripts.tooldelta.api.client import GetBlockEntityData
from skybluetech_scripts.tooldelta.ui import RegistToolDeltaScreen, UBaseCtrl
from skybluetech_scripts.skybluetech.common.events.machinery.electric_crafter import (
    ElectricCrafterUpdateRecipe,
)
from skybluetech_scripts.tooldelta.utils.nbt import GetValueWithDefault as GetValue
from skybluetech_scripts.skybluetech.common.machinery_def.basic import (
    K_PROGRESS,
    K_STORE_RF,
)
from skybluetech_scripts.skybluetech.common.machinery_def.electric_crafter import (
    STORE_RF_MAX,
)
from .define import MachinePanelUIProxy, MAIN_PATH
from .utils import UpdateGenericProgressL2R, UpdatePowerBar

PROGRESS_PATH = MAIN_PATH / "progress"
POWER_PATH = MAIN_PATH / "power_bar"
GRID_PATH = MAIN_PATH / "crafting_grid"

MASK_REL_PATH = "item_cell_overlay_ref/mask"
ITEM_RENDERED_REL_PATH = "item_cell_overlay_ref/item_renderer"


@RegistToolDeltaScreen("ElectricCrafterUI.main", is_proxy=True)
class ElectricCrafterUI(MachinePanelUIProxy):
    def OnCreate(self):
        self.power = self.GetElement(POWER_PATH)
        self.progress = self.GetElement(PROGRESS_PATH)
        self.grid = self.GetElement(GRID_PATH).asGrid()

    def OnTicking(self):
        data = GetBlockEntityData(*self.pos[1:])
        if data is None:
            return
        data = data["exData"]
        store_rf = GetValue(data, K_STORE_RF, 0)
        progress = GetValue(data, K_PROGRESS, 0)
        UpdatePowerBar(self.power, store_rf, STORE_RF_MAX)
        UpdateGenericProgressL2R(self.progress, progress)

    @MachinePanelUIProxy.Listen(ElectricCrafterUpdateRecipe)
    def onUpdateRecipe(self, event):
        # type: (ElectricCrafterUpdateRecipe) -> None
        for i, item_and_aux in enumerate(event.slotitems):
            slot = self.grid.GetGridItem(i % 3, i // 3)
            mask = slot[MASK_REL_PATH].asImage()
            ir = slot[ITEM_RENDERED_REL_PATH].asItemRenderer()
            if item_and_aux is None:
                mask.SetSpriteColor((0.5, 0.5, 0.5))
                ir.SetVisible(False)
            else:
                mask.SetSpriteColor((1, 1, 1))
                ir.SetVisible(True)
                ir.SetUiItem(Item(*item_and_aux))
