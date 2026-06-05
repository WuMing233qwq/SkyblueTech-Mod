# coding=utf-8
from skybluetech_scripts.tooldelta.define import Item
from skybluetech_scripts.tooldelta.ui import UBaseCtrl
from skybluetech_scripts.tooldelta.events.client import OnKeyPressInGame
from skybluetech_scripts.tooldelta.api.client import (
    GetItemHoverName,
    GetLocalPlayerHotbarAndInvItems,
    GetLocalPlayerLevelByExp,
)
from skybluetech_scripts.tooldelta.ui import (
    Binder,
    RegistToolDeltaScreen,
    SCREEN_BASE_PATH,
    ToolDeltaScreen,
)
from skybluetech_scripts.tooldelta.utils.py_comp import py2_unicode
from skybluetech_scripts.skybluetech.client.ui.machinery.utils import (
    UpdateGenericProgressL2R,
)
from skybluetech_scripts.skybluetech.client.ui.recipe_checker import CheckRecipe
from skybluetech_scripts.skybluetech.common.events.misc.industrial_researching import (
    IndustrialResearchingInscribeRequest,
    IndustrialResearchingQueryRequest,
    IndustrialResearchingQueryResponse,
    IndustrialResearchingSubmitRequest,
)
from skybluetech_scripts.skybluetech.common.misc.industrial_researching import (
    all_researchings,
)

if 0:
    from skybluetech_scripts.skybluetech.common.mini_jei.misc.industrial_researching import (
        IndustrialResearchingRecipe,  # noqa: F401
        Input,  # noqa: F401
    )


RESEARCHINGS_SCROLL_PATH = SCREEN_BASE_PATH / "researchings_scroll_view"
CLOSE_BTN_PATH = SCREEN_BASE_PATH / "close_btn"
EXP_BOTTLE_ITEM_ID = "minecraft:experience_bottle"
RESEARCHINGS_COLLECTION = "industrial_researchings_grid"
LABEL_NORMAL_COLOR = (0.2588, 0.2588, 0.2588)
LABEL_MISSING_COLOR = (0xAF / 255.0, 0, 0)
LABEL_OK_COLOR = (0.0, 0.5, 0.0)


def _clean_item_name(item_id):
    # type: (str) -> str
    return (GetItemHoverName(item_id) or item_id).replace("§r", "").replace("§f", "")


def _short_item_name(item_id):
    # type: (str) -> str
    item_name = py2_unicode(_clean_item_name(item_id)).replace(" ", "")
    if len(item_name) > 6:
        return item_name[:6] + ".."
    return item_name


def _safe_percent(now, total):
    # type: (float, float) -> float
    if total <= 0:
        return 1.0
    return max(0.0, min(1.0, float(now) / total))


@RegistToolDeltaScreen("IndustrialResearchProgressUI.main")
class IndustrialResearchProgressUI(ToolDeltaScreen):
    def __init__(self, screen_name, screen_instance, params=None):
        ToolDeltaScreen.__init__(self, screen_name, screen_instance, params)
        self.ready = False
        self.researched_items = {}  # type: dict[str, int]
        self.requirements_window = None
        self.current_recipe = None  # type: IndustrialResearchingRecipe | None
        self.item_id_aux_cache = {}  # type: dict[str, int]
        self.can_submit_research = False

    def OnCreate(self):
        self.ready = False
        self.researched_items = {}
        self.requirements_window = None
        self.current_recipe = None
        self.can_submit_research = False
        self.recipes = list(all_researchings)
        self.researchings_grid = (
            self
            .GetElement(RESEARCHINGS_SCROLL_PATH)
            .asScrollView()
            .GetContent()
            .asGrid()
        )
        self.researchings_grid.SetPropertyBag({
            "#maximum_grid_items": len(self.recipes)
        })
        self.GetElement(CLOSE_BTN_PATH).asButton().SetCallback(
            lambda _: self.RemoveUI()
        )
        IndustrialResearchingQueryRequest().send()

    def OnDestroy(self):
        self.close_requirements_window()

    def render_researchings(self):
        # type: () -> None
        self.researchings_grid.SetPropertyBag({
            "#maximum_grid_items": len(self.recipes)
        })

    def open_requirements_window(self, recipe):
        # type: (IndustrialResearchingRecipe) -> None
        if not self.ready:
            return
        self.close_requirements_window()
        window = self.AddElement(
            "IndustrialResearchProgressUI.requirements_window",
            "requirements_window",
        )
        window.SetLayer(20)
        self.requirements_window = window
        self.current_recipe = recipe
        self.can_submit_research = False
        window["close_btn"].asButton().SetCallback(
            lambda _: self.close_requirements_window()
        )
        window["bg/title"].asLabel().SetText(
            "研究 " + _short_item_name(recipe.result_item_id) + " 需要："
        )

        requirements = list(recipe.require_items)  # type: list[Input | None]
        requirements.append(None)
        columns = 1
        grid = window["requirements_grid"].asGrid()
        # grid.SetPropertyBag({"#maximum_grid_items": len(requirements)})
        self.update_inscribe_button()
        self.update_submit_button()

        def after():
            researched = recipe.result_item_id in self.researched_items
            item_counts = self.get_local_item_counts()
            player_level = GetLocalPlayerLevelByExp()
            can_submit = True
            for index, input_item in enumerate(requirements):
                ctrl = grid.GetGridItem(0, index)
                if input_item is None:
                    if researched:
                        self.render_researched_requirement_item(
                            ctrl,
                            EXP_BOTTLE_ITEM_ID,
                            False,
                        )
                        continue
                    enough = player_level >= recipe.require_exp_level
                    can_submit = can_submit and enough
                    self.render_requirement_item(
                        ctrl,
                        EXP_BOTTLE_ITEM_ID,
                        player_level,
                        recipe.require_exp_level,
                        enough,
                        False,
                    )
                else:
                    if researched:
                        self.render_researched_requirement_item(
                            ctrl,
                            input_item.id,
                            True,
                        )
                        continue
                    own_count = self.count_matched_items(input_item, item_counts)
                    enough = own_count >= input_item.count
                    can_submit = can_submit and enough
                    self.render_requirement_item(
                        ctrl,
                        input_item.id,
                        own_count,
                        input_item.count,
                        enough,
                        True,
                    )
            self.can_submit_research = (
                can_submit and recipe.result_item_id not in self.researched_items
            )
            self.update_submit_button()

        grid.SetDimensionAndCall((columns, len(requirements)), after)

    def render_researched_requirement_item(self, ctrl, item_id, check_recipe):
        # type: (UBaseCtrl, str, bool) -> None
        ctrl["item_renderer"].asItemRenderer().SetUiItem(Item(item_id))
        label = ctrl["progress_label"].asLabel()
        label.SetText("✔ 已完成")
        label.SetColor(LABEL_OK_COLOR)
        UpdateGenericProgressL2R(ctrl["progress"], 1.0)
        self.update_requirement_check_btn(ctrl, item_id, check_recipe)

    def render_requirement_item(
        self, ctrl, item_id, own_count, need_count, enough, check_recipe
    ):
        # type: (UBaseCtrl, str, float, float, bool, bool) -> None
        ctrl["item_renderer"].asItemRenderer().SetUiItem(Item(item_id))
        label = ctrl["progress_label"].asLabel()
        label.SetText("%d/%d" % (own_count, need_count))
        label.SetColor(LABEL_NORMAL_COLOR if enough else LABEL_MISSING_COLOR)
        UpdateGenericProgressL2R(ctrl["progress"], _safe_percent(own_count, need_count))
        self.update_requirement_check_btn(ctrl, item_id, check_recipe)

    def update_requirement_check_btn(self, ctrl, item_id, check_recipe):
        # type: (UBaseCtrl, str, bool) -> None
        btn = ctrl["item_renderer/check_recipe_btn"]
        btn.SetVisible(check_recipe)
        if check_recipe:
            btn.asButton().SetCallback(lambda _, item_id=item_id: CheckRecipe(item_id))

    def close_requirements_window(self):
        if self.requirements_window is not None:
            self.requirements_window.Remove(warning=False)
            self.requirements_window = None
            self.current_recipe = None
            self.can_submit_research = False

    def is_current_recipe_researched(self):
        # type: () -> bool
        return (
            self.current_recipe is not None
            and self.current_recipe.result_item_id in self.researched_items
        )

    def update_inscribe_button(self):
        # type: () -> None
        if self.requirements_window is None:
            return
        researched = self.is_current_recipe_researched()
        self.requirements_window["take_btn/disable_mask"].SetVisible(not researched)
        self.requirements_window["take_btn"].asButton().SetCallback(
            lambda _: self.on_click_inscribe_btn()
        )

    def update_submit_button(self):
        # type: () -> None
        if self.requirements_window is None:
            return
        self.requirements_window["submit_btn/disable_mask"].SetVisible(
            not self.can_submit_research
        )

    def on_click_inscribe_btn(self):
        # type: () -> None
        if not self.is_current_recipe_researched():
            return
        IndustrialResearchingInscribeRequest(self.current_recipe.result_item_id).send()  # pyright: ignore[reportOptionalMemberAccess]

    @Binder.binding(
        Binder.BF_ButtonClickUp,
        "#IndustrialResearchProgressUI.submit_btn",
    )
    def on_submit_btn_pressed(self, params):
        # type: (dict) -> None
        self.handle_submit_btn()

    def handle_submit_btn(self):
        # type: () -> None
        if not self.can_submit_research:
            return
        if self.current_recipe is None:
            return
        IndustrialResearchingSubmitRequest(self.current_recipe.result_item_id).send()

    def get_local_item_counts(self):
        # type: () -> dict[str, int]
        counts = {}
        for item in GetLocalPlayerHotbarAndInvItems():
            if item is None:
                continue
            counts[item.id] = counts.get(item.id, 0) + item.count
        return counts

    def count_matched_items(self, input_item, item_counts):
        # type: (Input, dict[str, int]) -> int
        count = 0
        for item_id, item_count in item_counts.items():
            if input_item.match_item_id(item_id):
                count += item_count
        return count

    @ToolDeltaScreen.Listen(IndustrialResearchingQueryResponse)
    def on_recv_query_response(self, event):
        # type: (IndustrialResearchingQueryResponse) -> None
        self.researched_items = event.researched_items or {}
        self.ready = True
        self.render_researchings()
        self.update_inscribe_button()

    @Binder.binding_collection(
        Binder.BF_BindInt,
        RESEARCHINGS_COLLECTION,
        "#IndustrialResearchProgressUI.researching_count",
    )
    def get_researching_count(self, _index):
        # type: (int) -> int
        return len(self.recipes)

    @Binder.binding_collection(
        Binder.BF_BindInt,
        RESEARCHINGS_COLLECTION,
        "#IndustrialResearchProgressUI.researching_item_id_aux",
    )
    def get_researching_item_id_aux(self, index):
        # type: (int) -> int
        if index >= len(self.recipes):
            return 131072
        item_id = self.recipes[index].result_item_id
        cached = self.item_id_aux_cache.get(item_id)
        if cached is not None:
            return cached
        item_id_aux = Item(item_id).GetBasicInfo().id_aux
        self.item_id_aux_cache[item_id] = item_id_aux
        return item_id_aux

    @Binder.binding_collection(
        Binder.BF_BindString,
        RESEARCHINGS_COLLECTION,
        "#IndustrialResearchProgressUI.researching_item_name",
    )
    def get_researching_item_name(self, index):
        # type: (int) -> str
        if index >= len(self.recipes):
            return ""
        return _clean_item_name(self.recipes[index].result_item_id)

    @Binder.binding_collection(
        Binder.BF_BindBool,
        RESEARCHINGS_COLLECTION,
        "#IndustrialResearchProgressUI.researching_ok_visible",
    )
    def get_researching_ok_visible(self, index):
        # type: (int) -> bool
        if index >= len(self.recipes):
            return False
        return self.recipes[index].result_item_id in self.researched_items

    @Binder.binding(
        Binder.BF_ButtonClickUp,
        "#IndustrialResearchProgressUI.researching_selected",
    )
    def on_researching_selected(self, params):
        # type: (dict) -> None
        index = params["#collection_index"]
        if not self.ready or index >= len(self.recipes):
            return
        self.open_requirements_window(self.recipes[index])

    @ToolDeltaScreen.Listen(OnKeyPressInGame)
    def onKeyPress(self, event):
        # type: (OnKeyPressInGame) -> None
        if event.key == event.KeyBoardType.KEY_ESCAPE and event.isDown:
            if self.requirements_window is not None:
                self.close_requirements_window()
                return
            self.RemoveUI()
