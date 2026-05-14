# coding=utf-8
from .basic_machine_ui_sync import MachineUISync

K_OUTPUT_RATE = "r"
K_CUR_TEMPERATURE = "t"
K_FLUID_ID = "f"
K_FLUID_VOLUME = "v"
K_MAX_VOLUME = "M"
K_PROGRESS = "st:working_ticks"


class CyroHeatMeltingChamberUISync(MachineUISync):
    produce_speed = 0.0
    current_temperature = 0.0
    fluid_id = None  # type: str | None
    fluid_volume = 0
    max_fluid_volume = 0
    progress = 0.0

    def Unmarshal(self, data):
        self.produce_speed = data[K_OUTPUT_RATE]
        self.current_temperature = data[K_CUR_TEMPERATURE]
        self.fluid_id = data[K_FLUID_ID]
        self.fluid_volume = data[K_FLUID_VOLUME]
        self.max_fluid_volume = data[K_MAX_VOLUME]
        self.progress = data[K_PROGRESS]

    def Marshal(self):
        return {
            K_OUTPUT_RATE: self.produce_speed,
            K_CUR_TEMPERATURE: self.current_temperature,
            K_FLUID_ID: self.fluid_id,
            K_FLUID_VOLUME: self.fluid_volume,
            K_MAX_VOLUME: self.max_fluid_volume,
            K_PROGRESS: self.progress,
        }
