# coding=utf-8
from skybluetech_scripts.tooldelta.events.server import (
    ServerBlockUseEvent,
    PushUIRequest,
)
from skybluetech_scripts.tooldelta.api.server import (
    GetBlockName,
    GetBlockStates,
    GetPlayerDimensionId,
    UpdateBlockStates,
    SetOnePopupNotice,
)
from skybluetech_scripts.tooldelta.events.service import ServerListenerService
from skybluetech_scripts.skybluetech.common.events.misc.transmitter_settings import (
    TransmitterSwitchAccessMode,
    TransmitterSetLabel,
    TransmitterSetPriority,
)
from skybluetech_scripts.skybluetech.common.define.id_enum.items import (
    TRANSMITTER_WRENCH,
    TRANSMITTER_SETTINGS_WRENCH,
)
from skybluetech_scripts.skybluetech.common.define.facing import (
    NEIGHBOR_BLOCKS_ENUM,
    OPPOSITE_FACING,
)
from ..base.define import AP_MODE_INPUT, AP_MODE_OUTPUT
from ..constants import FACING_EN, FACING_ZHCN
from .logic import (
    LogicModule,
    Generic,
    _NT,
    _APT,
)


class ActionModule(Generic[_NT, _APT], ServerListenerService):
    def __init__(
        self,
        logic_module,  # type: LogicModule[_NT, _APT]
        wrench_pick_threshold=5.0 / 16,
        enable_io_mode_settings=True,
        enable_label_settings=True,
    ):
        ServerListenerService.__init__(self)
        self.logic_module = logic_module
        self.wrench_pick_threshold = wrench_pick_threshold
        self.enable_io_mode_settings = enable_io_mode_settings
        self.enable_label_settings = enable_label_settings
        self.enable_listeners()

    def get_testing_facing(self, clickX, clickY, clickZ):
        # type: (float, float, float) -> int | None
        THR = self.wrench_pick_threshold
        if clickY > 0 and clickY < THR:
            return 0  # down
        elif clickY > 1 - THR and clickY < 1:
            return 1
        elif clickZ > 0 and clickZ < THR:
            return 2  # north
        elif clickZ > 1 - THR and clickZ < 1:
            return 3  # south
        elif clickX > 0 and clickX < THR:
            return 4  # west
        elif clickX > 1 - THR and clickX < 1:
            return 5  # east
        else:
            return None

    def switch_access_mode(self, dim, x, y, z, face, player_id=None):
        # type: (int, int, int, int, int, str | None) -> bool
        if not self.enable_io_mode_settings:
            return False
        block_name = GetBlockName(dim, (x, y, z))
        if block_name is None:
            return False
        block_orig_status = GetBlockStates(dim, (x, y, z))
        dx, dy, dz = NEIGHBOR_BLOCKS_ENUM[face]
        nextBlock = GetBlockName(dim, (x + dx, y + dy, z + dz))
        if nextBlock is None or self.logic_module.transmitter_check_func(nextBlock):
            if player_id is not None:
                SetOnePopupNotice(
                    player_id,
                    "§6无法为已连接了另外一根管道的管道设置传输模式",
                    "§7[§cx§7] §c错误",
                )
            return False
        elif not self.logic_module.can_connect(nextBlock, block_name):
            if player_id is not None:
                SetOnePopupNotice(
                    player_id,
                    "§6无法为未连接的管道设置传输模式",
                    "§7[§cx§7] §c错误",
                )
            return False
        facing_en_key = "skybluetech:cable_io_" + FACING_EN[face]
        newState = not block_orig_status.get(facing_en_key, False)
        block_orig_status[facing_en_key] = newState
        current_network = self.logic_module.GetNetworkByTransmitter(dim, x, y, z)
        if current_network is None:
            if player_id is not None:
                SetOnePopupNotice(player_id, "§4管道数据异常", "§7[§cx§7] §c错误")
            return False
        if newState:
            ap = self.logic_module.access_point_cls(dim, x, y, z, face, AP_MODE_OUTPUT)
            ap.bound_network(current_network)
            ok = self.logic_module.SetAccessPointIOMode(ap, AP_MODE_OUTPUT)
        else:
            ap = self.logic_module.access_point_cls(dim, x, y, z, face, AP_MODE_INPUT)
            ap.bound_network(current_network)
            ok = self.logic_module.SetAccessPointIOMode(ap, AP_MODE_INPUT)
        if ok:
            if player_id is not None:
                SetOnePopupNotice(
                    player_id,
                    "§f已将管道的§6"
                    + FACING_ZHCN[face]
                    + "§f面设置为"
                    + ("§a输入", "§c抽出")[newState],
                )
        else:
            if player_id is not None:
                SetOnePopupNotice(
                    player_id,
                    "§6无法将管道的§6"
                    + FACING_ZHCN[face]
                    + "§6面设置为"
                    + ("§a输入", "§c抽出")[newState],
                )
        UpdateBlockStates(dim, (x, y, z), block_orig_status)
        return True

    @ServerListenerService.Listen(ServerBlockUseEvent)
    def onPlayerUseWrench(self, event):
        # type: (ServerBlockUseEvent) -> None
        if not self.logic_module.transmitter_check_func(event.blockName):
            return
        if event.item.newItemName == TRANSMITTER_WRENCH:
            face = self.get_testing_facing(event.clickX, event.clickY, event.clickZ)
            if face is None:
                SetOnePopupNotice(event.playerId, "无效扳手调节位置")
                return
            else:
                self.switch_access_mode(
                    event.dimensionId, event.x, event.y, event.z, face, event.playerId
                )
        elif event.item.newItemName == TRANSMITTER_SETTINGS_WRENCH:
            if not self.enable_label_settings:
                return
            facing = self.get_testing_facing(event.clickX, event.clickY, event.clickZ)
            if facing is None:
                SetOnePopupNotice(event.playerId, "无效扳手设置位置")
                return
            ap = self.logic_module.access_points_pool.get((
                event.dimensionId,
                event.x,
                event.y,
                event.z,
                facing,
            ))
            if ap is None:
                self.logic_module.GetNetworkByTransmitter(
                    event.dimensionId, event.x, event.y, event.z
                )  # 需要激活一次
                ap = self.logic_module.access_points_pool.get((
                    event.dimensionId,
                    event.x,
                    event.y,
                    event.z,
                    facing,
                ))
                if ap is None:
                    SetOnePopupNotice(
                        event.playerId, "管道此面没有邻接容器， 无法进行设置"
                    )
                    return
            PushUIRequest(
                "TransmitterSettingsUI.main",
                params={
                    "dim": event.dimensionId,
                    "x": event.x,
                    "y": event.y,
                    "z": event.z,
                    "side": ap.access_facing,
                    "label": ap.get_label(),
                    "priority": ap.get_priority(),
                },
            ).send(event.playerId)

    @ServerListenerService.Listen(TransmitterSwitchAccessMode)
    def onSwitchAccessMode(self, event):
        # type: (TransmitterSwitchAccessMode) -> None
        if event.transmitter_type != self.logic_module.network_cls.network_type:
            return
        self.switch_access_mode(
            GetPlayerDimensionId(event.pid),
            event.x,
            event.y,
            event.z,
            event.facing,
            event.pid,
        )

    @ServerListenerService.Listen(TransmitterSetLabel)
    def onSetLabel(self, event):
        # type: (TransmitterSetLabel) -> None
        if not self.enable_label_settings:
            return
        if not isinstance(event.label, int) or event.label < 0 or event.label > 100000:
            return
        ap = self.logic_module.access_points_pool.get((
            GetPlayerDimensionId(event.pid),
            event.x,
            event.y,
            event.z,
            event.facing,
        ))
        if ap is None:
            return
        ap.set_label(event.label)

    @ServerListenerService.Listen(TransmitterSetPriority)
    def onSetPriority(self, event):
        # type: (TransmitterSetPriority) -> None
        if not self.enable_label_settings:
            return
        if (
            not isinstance(event.priority, int)
            or event.priority < -100000
            or event.priority > 100000
        ):
            return
        ap = self.logic_module.access_points_pool.get((
            GetPlayerDimensionId(event.pid),
            event.x,
            event.y,
            event.z,
            event.facing,
        ))
        if ap is None:
            return
        ap.set_priority(event.priority)
