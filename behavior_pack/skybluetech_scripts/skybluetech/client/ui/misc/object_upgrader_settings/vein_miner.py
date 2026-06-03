# coding=utf-8
from skybluetech_scripts.tooldelta.define import Item
from skybluetech_scripts.tooldelta.events.client import OnKeyPressInGame
from skybluetech_scripts.tooldelta.utils.py_comp import py2_unicode
from skybluetech_scripts.tooldelta.ui import (
    Binder,
    RegistToolDeltaScreen,
    SCREEN_BASE_PATH,
    ToolDeltaScreen,
)
from skybluetech_scripts.skybluetech.common.events.misc.object_upgraders import (
    ObjUpVeinMinerSettingsAddBlockRequest,
    ObjUpVeinMinerSettingsUpload,
)

GRID_COLUMNS = 10
K_UI_VEIN_BLOCKS = "vein_blocks"
GRID_COLLECTION = "obj_up_vein_blocks_grid"
STRING_TYPES = (str, py2_unicode)
BARRIER_ITEM_ID_AUX = None  # type: int | None


@RegistToolDeltaScreen("ObjUpVeinMinerSettingsUI.main")
class VeinMinerSettingsUI(ToolDeltaScreen):
    def __init__(self, screen_name, screen_instance, params):
        ToolDeltaScreen.__init__(self, screen_name, screen_instance, params)
        raw_blocks = params.get(K_UI_VEIN_BLOCKS, [])
        self.vein_blocks = [str(i) for i in raw_blocks if isinstance(i, STRING_TYPES)]
        self.current_section = 0 if self.vein_blocks else -1
        self._item_id_aux_cache = {}  # type: dict[str, int]

    def OnCreate(self):
        self.grid = (
            self
            .GetElement(SCREEN_BASE_PATH / "vein_blocks")
            .asScrollView()
            .GetContent()
            .asGrid()
        )

    @ToolDeltaScreen.Listen(OnKeyPressInGame)
    def on_key_press(self, event):
        # type: (OnKeyPressInGame) -> None
        if event.key == event.KeyBoardType.KEY_ESCAPE and event.isDown:
            self.RemoveUI()

    @Binder.binding(
        Binder.BF_ButtonClickUp,
        "#ObjUpVeinMinerSettingsUI.section_btn",
    )
    def on_section_btn_click(self, params):
        # type: (dict) -> None
        index = params["#collection_index"]
        if 0 <= index < len(self.vein_blocks):
            self.current_section = index

    @Binder.binding(
        Binder.BF_ButtonClickUp,
        "#ObjUpVeinMinerSettingsUI.del_block_btn",
    )
    def on_del_block_btn_click(self, _params):
        # type: (dict) -> None
        if not (0 <= self.current_section < len(self.vein_blocks)):
            return
        self.vein_blocks.pop(self.current_section)
        if self.current_section >= len(self.vein_blocks):
            self.current_section = len(self.vein_blocks) - 1
        ObjUpVeinMinerSettingsUpload(self.vein_blocks).send()
        self.grid.SetDimensionAndCall(self.get_grid_size(), lambda: None)

    @Binder.binding(
        Binder.BF_ButtonClickUp,
        "#ObjUpVeinMinerSettingsUI.add_block_btn",
    )
    def on_add_block_btn_click(self, _params):
        # type: (dict) -> None
        ObjUpVeinMinerSettingsAddBlockRequest().send()
        self.RemoveUI()

    @Binder.binding(
        Binder.BF_BindGridSize,
        "#ObjUpVeinMinerSettingsUI.vein_blocks_grid_size",
    )
    def get_grid_size(self):
        rows = (len(self.vein_blocks) + GRID_COLUMNS - 1) // GRID_COLUMNS
        return (GRID_COLUMNS, max(1, rows))

    @Binder.binding_collection(
        Binder.BF_BindBool,
        GRID_COLLECTION,
        "#ObjUpVeinMinerSettingsUI.vein_block_visible",
    )
    def get_vein_block_visible(self, index):
        # type: (int) -> bool
        return index < len(self.vein_blocks)

    @Binder.binding_collection(
        Binder.BF_BindBool,
        GRID_COLLECTION,
        "#ObjUpVeinMinerSettingsUI.vein_block_selected",
    )
    def get_vein_block_selected(self, index):
        # type: (int) -> bool
        return index == self.current_section and index < len(self.vein_blocks)

    @Binder.binding_collection(
        Binder.BF_BindInt,
        GRID_COLLECTION,
        "#ObjUpVeinMinerSettingsUI.vein_block_item_id_aux",
    )
    def get_vein_block_item_id_aux(self, index):
        # type: (int) -> int
        global BARRIER_ITEM_ID_AUX
        if index >= len(self.vein_blocks):
            return 0
        block_id = self.vein_blocks[index]
        cached = self._item_id_aux_cache.get(block_id)
        if cached is not None:
            return cached
        try:
            item_id_aux = Item(block_id).GetBasicInfo().id_aux
        except Exception:
            if BARRIER_ITEM_ID_AUX is None:
                BARRIER_ITEM_ID_AUX = Item("minecraft:barrier").GetBasicInfo().id_aux
            item_id_aux = BARRIER_ITEM_ID_AUX
        self._item_id_aux_cache[block_id] = item_id_aux
        return item_id_aux
