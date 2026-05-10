# coding=utf-8
from skybluetech_scripts.tooldelta.define import UICtrlPosData
from skybluetech_scripts.tooldelta.ui import RegistToolDeltaScreen
from skybluetech_scripts.tooldelta.api.client import (
    NewSingleBlockPalette,
    CombineBlockPaletteToGeometry,
)
from ....common.ui_sync.machinery.hydroponic_bed_sand import HydroponicBedSandUISync
from .define import MachinePanelUIProxy, MAIN_PATH
from .utils import UpdatePowerBar

from ..recipe_checker import AsRecipeCheckerBtn
from ....common.machinery_def.hydroponic_bed_sand import recipes

POWER_NODE = MAIN_PATH / "power_bar"
CROP_DISP_NODE = MAIN_PATH / "visualer/crop_disp"


@RegistToolDeltaScreen("HydroponicBedSandUI.main", is_proxy=True)
class HydroponicBedSandUI(MachinePanelUIProxy):
    def OnCreate(self):
        dim, x, y, z = self.pos
        self.sync = HydroponicBedSandUISync.NewClient(dim, x, y, z)  # type: HydroponicBedSandUISync
        self.sync.SetUpdateCallback(self.WhenUpdated)
        self.power_bar = self.GetElement(POWER_NODE)
        self.crop_disp = self.GetElement(CROP_DISP_NODE).asNeteasePaperDoll()
        AsRecipeCheckerBtn(
            self.GetElement(MAIN_PATH / "recipe_check_btn").asButton(),
            recipes,  # pyright: ignore[reportArgumentType]
        )
        self.last_render_crop_block_id = None
        self.last_progress = None

    def WhenUpdated(self):
        if not self.inited:
            return
        UpdatePowerBar(self.power_bar, self.sync.store_rf, self.sync.rf_max)
        if (
            self.last_render_crop_block_id == self.sync.crop_block_id
            and self.last_progress == self.sync.grow_progress
        ):
            return
        self.last_render_crop_block_id = self.sync.crop_block_id
        self.last_progress = self.sync.grow_progress
        pal = NewSingleBlockPalette(self.sync.crop_block_id or "minecraft:air", 0)
        geo_id = CombineBlockPaletteToGeometry(
            pal, "geometry.skybluetech_temp.crop_block_id"
        )
        self.crop_disp.RenderBlockGeometryModel(
            geo_id,
            scale=0.5 + 4 * self.sync.grow_progress,
            init_rot_x=-90,
            init_rot_y=0,
            init_rot_z=90,
            rotation_axis=(0, 1, 0),
        )
        self.crop_disp.SetFullPos(
            "y",
            UICtrlPosData(
                follow_type="parent", absolute_value=-20 * self.sync.grow_progress + 8
            ),
        )
        self.last_render_crop_block_id = self.sync.crop_block_id
