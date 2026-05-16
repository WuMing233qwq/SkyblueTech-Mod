# coding=utf-8
from skybluetech_scripts.tooldelta.api.client import GetBlockEntityData
from skybluetech_scripts.tooldelta.ui import RegistToolDeltaScreen
from skybluetech_scripts.tooldelta.utils.nbt import GetValueWithDefault as GetValue
from skybluetech_scripts.skybluetech.common.machinery_def.basic import K_STORE_RF
from skybluetech_scripts.skybluetech.common.machinery_def.forester import (
    STORE_RF_MAX,
)
from .define import MachinePanelUIProxy, MAIN_PATH
from .utils import UpdatePowerBar

POWER_PATH = MAIN_PATH / "power_bar"


@RegistToolDeltaScreen("ForesterUI.main", is_proxy=True)
class ForesterUI(MachinePanelUIProxy):
    def OnCreate(self):
        self.power_bar = self.GetElement(POWER_PATH)

    def OnTicking(self):
        data = GetBlockEntityData(*self.pos[1:])
        if data is None:
            return
        data = data["exData"]
        store_rf = GetValue(data, K_STORE_RF, 0)
        UpdatePowerBar(self.power_bar, store_rf, STORE_RF_MAX)
