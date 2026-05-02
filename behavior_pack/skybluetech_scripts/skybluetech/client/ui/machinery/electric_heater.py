# coding=utf-8

from skybluetech_scripts.tooldelta.api.client import GetBlockEntityData
from skybluetech_scripts.tooldelta.ui import RegistToolDeltaScreen, Binder
from skybluetech_scripts.tooldelta.utils.nbt import GetValueWithDefault
from ....common.events.machinery.electric_heater import (
    ElectricHeaterSubmitModifiesEvent,
)
from ....common.machinery_def.electric_heater import K_SET_POWER, K_KELVIN_LIMIT
from ....common.ui_sync.machinery.electric_heater import ElectricHeaterUISync
from .define import MachinePanelUIProxy, MAIN_PATH
from .utils import UpdatePowerBar

POWER_NODE = MAIN_PATH / "power_bar"
DATABAR_TEXT_NODE = MAIN_PATH / "databar/text"
POWER_INPUT_NODE = MAIN_PATH / "power_input"
KELVIN_LIMIT_INPUT_NODE = MAIN_PATH / "kelvin_limit_input"
CONFIRM_BTN_NODE = MAIN_PATH / "confirm_btn"


@RegistToolDeltaScreen("ElectricHeaterUI.main", is_proxy=True)
class ElectricHeaterUI(MachinePanelUIProxy):
    def OnCreate(self):
        dim, x, y, z = self.pos
        self.sync = ElectricHeaterUISync.NewClient(dim, x, y, z)  # type: ElectricHeaterUISync
        self.sync.SetUpdateCallback(self.WhenUpdated)
        self.power_bar = self.GetElement(POWER_NODE)
        self.databar_text = self.GetElement(DATABAR_TEXT_NODE).asLabel()
        self.power_input = self.GetElement(POWER_INPUT_NODE).asTextEditBox()
        self.kevin_limit_input = self.GetElement(
            KELVIN_LIMIT_INPUT_NODE
        ).asTextEditBox()
        self.confirm_btn = (
            self.GetElement(CONFIRM_BTN_NODE).asButton().SetCallback(self.onSubmit)
        )
        block_nbt = GetBlockEntityData(x, y, z)
        if block_nbt is not None:
            ex_data = block_nbt.get("exData")
            if ex_data is not None:
                self.power_input.SetText(str(GetValueWithDefault(ex_data, K_SET_POWER, 0)))
                self.kevin_limit_input.SetText(str(GetValueWithDefault(ex_data, K_KELVIN_LIMIT, 300)))

    def WhenUpdated(self):
        if not self.inited:
            return
        UpdatePowerBar(self.power_bar, self.sync.storage_rf, self.sync.rf_max)
        self.databar_text.SetText(
            "设定功率： %d RF/t\n当前温度： %.1f°K"
            % (self.sync.power, self.sync.current_temperature)
        )

    def onSubmit(self, _):
        power_str = self.power_input.GetText()
        if power_str == "":
            return
        kelvin_limit_str = self.kevin_limit_input.GetText()
        if kelvin_limit_str == "":
            return
        dim, x, y, z = self.pos
        ElectricHeaterSubmitModifiesEvent(
            dim, x, y, z, int(power_str), int(kelvin_limit_str)
        ).send()

    @Binder.binding(Binder.BF_EditFinished, "#electric_heater.power")
    def onPowerEdited(self, params):
        text = params["Text"]
        if text == "":
            return
        if "." in text:
            try:
                val = int(float(text))
                self.power_input.SetText(str(val))
            except ValueError:
                self.power_input.SetText("")
        else:
            try:
                int(text)
            except ValueError:
                self.power_input.SetText("")

    @Binder.binding(Binder.BF_EditFinished, "#electric_heater.kelvin_limit")
    def onKelvinLimitEdited(self, params):
        text = params["Text"]
        if text == "":
            return
        if "." in text:
            try:
                val = int(float(text))
                self.kevin_limit_input.SetText(str(val))
            except ValueError:
                self.kevin_limit_input.SetText("")
        else:
            try:
                if int(text) < 0 or int(text) > 1500:
                    raise ValueError
            except ValueError:
                self.kevin_limit_input.SetText("")
