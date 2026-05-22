# coding=utf-8
from skybluetech_scripts.skybluetech.common.misc.transmitter import TransmitterType
from skybluetech_scripts.skybluetech.common.define.id_enum import Pipe
from .transmitter_settings_indirectional_base import (
    TransmitterSettingsPageIndirectionalBase,
)


class PipeSettingsPageIndirectional(TransmitterSettingsPageIndirectionalBase):
    transmitter_type = TransmitterType.PIPE
    transmitter_block_ids_set = Pipe.all()

    @staticmethod
    def GetIconPath():
        # type: () -> str
        return "textures/icon/pipe_bronze_icon"

    @staticmethod
    def GetControlDef():
        # type: () -> str
        return "MachinePanelExPages.pipe_settings_indirectional"
