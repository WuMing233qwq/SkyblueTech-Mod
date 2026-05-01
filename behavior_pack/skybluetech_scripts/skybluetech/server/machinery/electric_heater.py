# coding=utf-8
from skybluetech_scripts.tooldelta.api.common import Delay
from skybluetech_scripts.tooldelta.extensions.super_executor import SuperExecutorMeta
from ...common.define.id_enum.machinery import ELECTRIC_HEATER as MACHINE_ID
from ...common.events.machinery.electric_heater import ElectricHeaterSetPowerEvent
from ...common.ui_sync.machinery.electric_heater import ElectricHeaterUISync
from .utils.action_commit import SafeGetMachine
from .basic import HeatCtrl, GUIControl, PowerControl, RegisterMachine
from .pool import GetMachineStrict

K_SET_POWER = "set_power"
MAX_POWER = 1 << 32


@RegisterMachine
class ElectricHeater(HeatCtrl, GUIControl, PowerControl):
    block_name = MACHINE_ID
    store_rf_max = 64000
    max_heat_value = 500

    @SuperExecutorMeta.execute_super
    def __init__(self, dim, x, y, z, block_entity_data):
        self.sync = ElectricHeaterUISync.NewServer(self).Activate()
        self._cached_running_power = self.bdata[K_SET_POWER] or 0

    def OnTicking(self):
        HeatCtrl.OnTicking(self)
        if self.IsActive():
            if self.PowerEnough():
                self.ReducePower()
            self.CallSync()

    def OnSync(self):
        self.sync.rf_max = self.store_rf_max
        self.sync.storage_rf = self.store_rf
        self.sync.power = self.running_power
        self.sync.current_temperature = self.heat_value
        self.sync.MarkedAsChanged()

    @SuperExecutorMeta.execute_super
    def OnUnload(self):
        pass

    def set_power(self, power):
        # type: (int) -> None
        self.running_power = min(MAX_POWER, power)
        self.SetOutputHeatPower(power * 1.0)

    @property
    def running_power(self):
        # type: () -> int
        return self._cached_running_power

    @running_power.setter
    def running_power(self, value):
        # type: (int) -> None
        self._cached_running_power = self.bdata[K_SET_POWER] = value


@ElectricHeaterSetPowerEvent.Listen()
def onSetPower(event):
    # type: (ElectricHeaterSetPowerEvent) -> None
    m = SafeGetMachine(event.x, event.y, event.z, event.player_id)
    if not isinstance(m, ElectricHeater):
        return
    if not isinstance(event.power, int):
        return
    m.set_power(event.power)
