# coding=utf-8
from skybluetech_scripts.skybluetech.common.misc.transmitter import TransmitterType
from skybluetech_scripts.skybluetech.common.define.id_enum import Cable
from .transmitter_settings_base import TransmitterSettingsPageBase


class CableSettingsPage(TransmitterSettingsPageBase):
    transmitter_type = TransmitterType.CABLE
    transmitter_block_ids_set = Cable.all()

    @staticmethod
    def GetIconPath():
        # type: () -> str
        return "textures/icon/item_transport_cable_steel_icon"

    @staticmethod
    def GetControlDef():
        # type: () -> str
        return "MachinePanelExPages.cable_settings"
