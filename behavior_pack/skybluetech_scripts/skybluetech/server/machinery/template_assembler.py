# coding=utf-8
from skybluetech_scripts.tooldelta.extensions.super_executor import SuperExecutorMeta
from ...common.define.id_enum.machinery import TEMPLATE_ASSEMBLER as MACHINE_ID
from ...common.mini_jei.core import RecipesCollection
from ...common.machinery_def.template_assembler import recipes as Recipes, STORE_RF_MAX
from .utils.action_commit import SafeGetMachine
from .basic import MultiFluidContainer, Processor, RegisterMachine


@RegisterMachine
class TemplateAssembler(MultiFluidContainer, Processor):
    block_name = MACHINE_ID
    store_rf_max = STORE_RF_MAX
    dump_progress_to_block_entity_data = True
    process_item = True
    output_slots = (11,)
    upgrade_slot_start = 12
    upgrade_slots = 4

    @SuperExecutorMeta.execute_super
    def __init__(self, dim, x, y, z, block_entity_data):
        # self.set_mode(self.recipe_mode)
        pass

    @SuperExecutorMeta.execute_super
    def OnAddedFluid(self, slot, fluid_id, fluid_volume, is_final):
        pass

    @SuperExecutorMeta.execute_super
    def OnReducedFluid(self, slot, fluid_id, reduced_fluid_volume, is_final):
        pass

    # def set_mode(self, new_mode):
    #     # type: (int) -> None
    #     if new_mode >= len(Recipes):
    #         new_mode %= len(Recipes)
    #     self.recipes = RecipesCollection(MACHINE_ID, Recipes.recipes_mapping[new_mode])
    #     self.recipe_mode = new_mode
    #     self.start_next()

    # @property
    # def recipe_mode(self):
    #     # type: () -> int
    #     return self.bdata[K_MODE] or 0

    # @recipe_mode.setter
    # def recipe_mode(self, value):
    #     # type: (int) -> None
    #     self.bdata[K_MODE] = value


# @FreezerModeChangedEvent.Listen()
# def onFreezerModeChanged(event):
#     # type: (FreezerModeChangedEvent) -> None
#     machine = SafeGetMachine(event.x, event.y, event.z, event.player_id)
#     if not isinstance(machine, Freezer):
#         return
#     machine.set_mode(event.new_mode)
