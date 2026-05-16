from skybluetech_scripts.tooldelta.api.client import GetBlockEntityData
from skybluetech_scripts.tooldelta.ui import RegistToolDeltaScreen
from skybluetech_scripts.tooldelta.utils.nbt import GetValueWithDefault as GetValue
from skybluetech_scripts.skybluetech.common.machinery_def.basic import (
    K_STORE_RF,
    K_PROGRESS,
)
from ....common.machinery_def.redstone_generator import recipes, STORE_RF_MAX
from ..recipe_checker import AsRecipeCheckerBtn
from .define import MachinePanelUIProxy, MAIN_PATH
from .utils import UpdatePowerBar, UpdateFlame, UpdateGenericProgressL2R


POWER_PATH = MAIN_PATH / "power_bar"
FLAME_PATH = MAIN_PATH / "flame"
PROGRESS_PATH = MAIN_PATH / "progress"


@RegistToolDeltaScreen("RedstoneGeneratorUI.main", is_proxy=True)
class RedstoneGeneratorUI(MachinePanelUIProxy):
    def OnCreate(self):
        self.power_bar = self.GetElement(POWER_PATH)
        self.flame = self.GetElement(FLAME_PATH)
        self.progress = self.GetElement(PROGRESS_PATH)
        AsRecipeCheckerBtn(
            self.GetElement(MAIN_PATH / "recipe_check_btn").asButton(), recipes
        )

    def OnTicking(self):
        data = GetBlockEntityData(*self.pos[1:])
        if data is None:
            return
        data = data["exData"]
        store_rf = GetValue(data, K_STORE_RF, 0)
        progress = GetValue(data, K_PROGRESS, 0)
        UpdatePowerBar(self.power_bar, store_rf, STORE_RF_MAX)
        UpdateFlame(self.flame, (1 - progress) if progress > 0 else 0)
        UpdateGenericProgressL2R(self.progress, progress)
