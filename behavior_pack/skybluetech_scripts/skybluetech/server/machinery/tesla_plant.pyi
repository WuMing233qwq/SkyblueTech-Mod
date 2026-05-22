# coding=utf-8
from mod.server.extraServerApi import GetMinecraftEnum
from skybluetech_scripts.tooldelta.api.server import (
    GetEntitiesInSquareArea,
    GetEntityType,
    GetEntityAttr,
    Hurt,
)
from skybluetech_scripts.tooldelta.events.server.block import (
    ServerBlockUseEvent,
)
from skybluetech_scripts.tooldelta.extensions.super_executor import SuperExecutorMeta
from ...common.define import flags
from ...common.events.machinery.tesla_plant import (
    TeslaPlantSettingsUpload,
    TeslaPlantSettingsUpdate,
    TeslaPlantAttack,
)
from ...common.define.id_enum.machinery import TESLA_PLANT as MACHINE_ID
from .basic import (
    BaseSpeedControl,
    GUIControl,
    UpgradeControl,
    WorkRenderer,
    RegisterMachine,
)
from .utils.action_commit import SafeGetMachine

K_SETTING_ATTACK_MONSTER = "st:do_attack_monster"
K_SETTING_ATTACK_MOB = "st:do_attack_mob"
K_SETTING_ATTACK_PLAYER = "st:do_attack_player"
K_SETTING_ENABLE = "st:do_enable"
K_SETTING_WORK_RANGE = "st:work_range"

ActorDamageCause = GetMinecraftEnum().ActorDamageCause
EntityType = GetMinecraftEnum().EntityType
AttrType = GetMinecraftEnum().AttrType


@RegisterMachine
class TeslaPlant(GUIControl, UpgradeControl, WorkRenderer):
    block_name = MACHINE_ID

    @SuperExecutorMeta.execute_super
    def __init__(self, dim, x, y, z, block_entity_data):
        self._cached_setting_do_attack_mob = None
        self._cached_setting_do_attack_player = None
        self._cached_setting_do_attack_monster = None
        self._cached_work_range = None
        self.shock_damage = 0

    def OnTicking(self):
        while self.IsActive():
            if BaseSpeedControl.ProcessOnce(self):
                self.work_once()

    @SuperExecutorMeta.execute_super
    def OnClick(self, event, extra_datas=None):
        pass

    @SuperExecutorMeta.execute_super
    def OnUnload(self):
        pass

    @SuperExecutorMeta.execute_super
    def SetDeactiveFlag(self, flag):
        pass

    def work_once(self):
        range = self.work_range
        entities = GetEntitiesInSquareArea(
            None,
            (self.x - range, self.y - range, self.z - range),
            (self.x + range, self.y + range, self.z + range),
            dimensionId=self.dim,
        )
        self.attack_once(entities)

    def attack_once(self, entities):
        # type: (list[str]) -> None
        for entity_id in entities:
            entity_type = GetEntityType(entity_id)
            if (
                entity_type & EntityType.Player
                and not self.do_attack_player
                or entity_type & EntityType.Monster
                and not self.do_attack_monster
                or entity_type & EntityType.Mob
                and not self.do_attack_mob
            ):
                continue
            max_hp = GetEntityAttr(entity_id, AttrType.HEALTH)
            damage = min(max_hp, self.store_rf_max / 100)
            Hurt(entity_id, damage, ActorDamageCause.Lightning)
            self.ReducePower(int(damage * 100))

    def update_settings(
        self, do_attack_mob, do_attack_player, do_attack_monster, work_range
    ):
        # type: (bool, bool, bool, int) -> None
        self.do_attack_mob = do_attack_mob
        self.do_attack_player = do_attack_player
        self.do_attack_monster = do_attack_monster
        self.work_range = work_range
        TeslaPlantSettingsUpdate(
            self.dim,
            self.x,
            self.y,
            self.z,
            self.work_range,
            self.do_attack_monster,
            self.do_attack_mob,
            self.do_attack_player,
        ).sendMulti(self.ui_sync.GetPlayersInSync())

    @property
    def do_attack_mob(self):
        # type: () -> bool
        if self._cached_setting_do_attack_mob is None:
            self._cached_setting_do_attack_mob = self.bdata[K_SETTING_ATTACK_MOB]
        return self._cached_setting_do_attack_mob

    @do_attack_mob.setter
    def do_attack_mob(self, value):
        # type: (bool) -> None
        self._cached_setting_do_attack_mob = self.bdata[K_SETTING_ATTACK_MOB] = value

    @property
    def do_attack_player(self):
        # type: () -> bool
        if self._cached_setting_do_attack_player is None:
            self._cached_setting_do_attack_player = self.bdata[K_SETTING_ATTACK_PLAYER]
        return self._cached_setting_do_attack_player

    @do_attack_player.setter
    def do_attack_player(self, value):
        # type: (bool) -> None
        self._cached_setting_do_attack_player = self.bdata[K_SETTING_ATTACK_PLAYER] = (
            value
        )

    @property
    def do_attack_monster(self):
        # type: () -> bool
        if self._cached_setting_do_attack_monster is None:
            self._cached_setting_do_attack_monster = self.bdata[
                K_SETTING_ATTACK_MONSTER
            ]
        return self._cached_setting_do_attack_monster

    @do_attack_monster.setter
    def do_attack_monster(self, value):
        # type: (bool) -> None
        self._cached_setting_do_attack_monster = self.bdata[
            K_SETTING_ATTACK_MONSTER
        ] = value

    @property
    def work_range(self):
        # type: () -> int
        if self._cached_work_range is None:
            self._cached_work_range = self.bdata[K_SETTING_WORK_RANGE] or 5
        return self._cached_work_range

    @work_range.setter
    def work_range(self, value):
        # type: (int) -> None
        self._cached_work_range = self.bdata[K_SETTING_WORK_RANGE] = value


@TeslaPlantSettingsUpload.Listen()
def onUpload(event):
    # type: (TeslaPlantSettingsUpload) -> None
    m = SafeGetMachine(event.x, event.y, event.z, event.player_id)
    if not isinstance(m, TeslaPlant):
        return
    m.update_settings(
        event.do_attack_mob,
        event.do_attack_player,
        event.do_attack_monster,
        event.work_range,
    )


#
