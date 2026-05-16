# coding=utf-8
from skybluetech_scripts.tooldelta.api.client import GetBlockEntityData
from skybluetech_scripts.tooldelta.ui import RegistToolDeltaScreen
from skybluetech_scripts.tooldelta.utils.nbt import GetValueWithDefault as GetValue
from skybluetech_scripts.skybluetech.common.machinery_def.basic import (
    K_STORE_RF,
    K_PROGRESS,
    FluidSlotClient,
)
from skybluetech_scripts.skybluetech.common.machinery_def.fluid_condenser import (
    STORE_RF_MAX,
    MAX_FLUID_VOLUME,
)
from ....common.machinery_def.fluid_condenser import recipes
from .define import MachinePanelUIProxy, MAIN_PATH
from .utils import UpdatePowerBar, UpdateGenericProgressL2R, FluidDisplayer

from ..recipe_checker import AsRecipeCheckerBtn

POWER_PATH = MAIN_PATH / "power_bar"
PRGS_PATH = MAIN_PATH / "progress"
FLUID_PATH = MAIN_PATH / "fluid_display"


@RegistToolDeltaScreen("FluidCondenserUI.main", is_proxy=True)
class FluidCondenserUI(MachinePanelUIProxy):
    def OnCreate(self):
        self.power_bar = self.GetElement(POWER_PATH)
        self.progress = self.GetElement(PRGS_PATH)
        self.fluid_display = self.GetElement(FLUID_PATH)
        self.fluid_displayer = FluidDisplayer(self.fluid_display)
        AsRecipeCheckerBtn(
            self.GetElement(MAIN_PATH / "recipe_check_btn").asButton(),
            recipes,
        )

    def OnTicking(self):
        data = GetBlockEntityData(*self.pos[1:])
        if data is None:
            return
        data = data["exData"]
        store_rf = GetValue(data, K_STORE_RF, 0)
        progress = GetValue(data, K_PROGRESS, 0.0)
        fluid = FluidSlotClient(data)
        self.fluid_displayer.update(fluid.fluid_id, fluid.volume, MAX_FLUID_VOLUME)
        UpdatePowerBar(self.power_bar, store_rf, STORE_RF_MAX)
        UpdateGenericProgressL2R(self.progress, progress)
