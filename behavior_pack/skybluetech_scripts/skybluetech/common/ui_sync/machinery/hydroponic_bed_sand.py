# coding=utf-8

from .basic_machine_ui_sync import MachineUISync

K_RF = "r"
K_RF_MAX = "m"
K_CROP_BLOCK_ID = "i"
K_GROW_PROGRESS = "s"


class HydroponicBedSandUISync(MachineUISync):
    store_rf = 0
    rf_max = 1
    crop_block_id = ""
    grow_progress = 0.0

    def Unmarshal(self, data):
        self.store_rf = data[K_RF]
        self.rf_max = data[K_RF_MAX]
        self.crop_block_id = data[K_CROP_BLOCK_ID]
        self.grow_progress = data[K_GROW_PROGRESS]

    def Marshal(self):
        return {
            K_RF: self.store_rf,
            K_RF_MAX: self.rf_max,
            K_CROP_BLOCK_ID: self.crop_block_id,
            K_GROW_PROGRESS: self.grow_progress,
        }
