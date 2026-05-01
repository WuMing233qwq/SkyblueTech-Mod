# coding=utf-8
from .base_machine import BaseMachine
from skybluetech_scripts.tooldelta.extensions.super_executor import SuperExecutorMeta
from ....common.define.facing import FACING_DXYZ, OPPOSITE_FACING

K_HEAT_VALUE = "heat_value"
ENV_TEMPERATURE = 300.0


class HeatCtrl(BaseMachine):
    """
    热机机器类, 表示产热或吸热的机器。

    需要: `__init__`

    类属性:
        heat_loss (float): 热量流失值, 默认为 1.0
        original_heat_c (float): 原始比热容, 默认为 4000.0

    覆写:
        `OnLoad`
        `OnTicking`
        `Dump`
    """

    heat_power = 0
    "产热功率, 正值代表高于环境温度, 负值代表低于环境温度"
    spread_heat = False
    "是否扩散热量"
    max_heat_value = 600
    "最大热值"

    @SuperExecutorMeta.execute_super
    def __init__(self, dim, x, y, z, block_entity_data):
        self._heat_value = block_entity_data[K_HEAT_VALUE] or 0
        self.t = 0
        self.a = 1.0 / self.max_heat_value**3
        self.neighbor_heaters = [None] * len(FACING_DXYZ)  # type: list[HeatCtrl | None]
        self.update_neighbor_heaters()

    def OnTicking(self):
        if self.t % 5 == 0 and self.IsActive():
            self.t = 0
            self.work_once()

    def SetOutputHeatPower(self, power):
        self.heat_power = power

    def work_once(self):
        self.update_heat_value()
        if self.spread_heat:
            self.share_heat()

    def update_neighbor_heaters(self):
        from ..pool import GetMachineStrict

        for face, (dx, dy, dz) in enumerate(FACING_DXYZ):
            m = GetMachineStrict(self.dim, self.x + dx, self.y + dy, self.z + dz)
            if isinstance(m, HeatCtrl):
                self.neighbor_heaters[face] = m
                m.set_neighbor_heater(OPPOSITE_FACING[face], self)

    def set_neighbor_heater(self, face, m):
        # type: (int, HeatCtrl) -> None
        self.neighbor_heaters[face] = m

    def update_heat_value(self):
        new_heat_value = self.heat_value + self.heat_power
        self.heat_value = new_heat_value - self.calcuate_heat_loss(new_heat_value)

    def calcuate_heat_loss(self, heat_value):
        # type: (float) -> float
        return self.a * heat_value**4

    def share_heat(self):
        heaters = [
            h
            for h in self.neighbor_heaters
            if h is not None and h.heat_value < self.heat_value
        ]
        if not heaters:
            return

        m = self.heat_value
        ratio = 0.2

        # 快照
        heats = [h.heat_value for h in heaters]

        # 理想需求
        demands = [ratio * (m - h) for h in heats]
        D = sum(demands)
        if D <= 0:
            return

        # 安全缩放因子 s
        s = 1.0
        for h in heats:
            denom = D + ratio * (m - h)
            s = min(s, (m - h) / denom if denom > 0 else 0.0)
        s = min(s, m / D)
        s = max(s, 0.0)

        # 同步写入
        total = 0.0
        for i, heater in enumerate(heaters):
            actual = demands[i] * s
            heater.heat_value = heater.heat_value + actual
            total += actual
        self.heat_value = self.heat_value - total

    @property
    def heat_value(self):
        # type: () -> float
        return self._heat_value

    @heat_value.setter
    def heat_value(self, value):
        self._heat_value = value
        self.bdata[K_HEAT_VALUE] = value
