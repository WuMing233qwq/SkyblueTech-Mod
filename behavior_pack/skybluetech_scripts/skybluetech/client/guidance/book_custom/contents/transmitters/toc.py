# coding=utf-8
from skybluetech_scripts.skybluetech.common.define import id_enum
from ...define import (
    TextPage,
    TOCPage,
    TOCPageSection,
    PageGroup,
)

from . import cable, general_settings, pipe

transmitters_toc = PageGroup(
    "transmitters",
    [
        TextPage(
            "物流系统",
            '《蔚蓝科技》有着独一套的<text color="§9" t="物流系统">助您在机器或容器间运送物品和流体。',
        ),
        TOCPage(
            [
                TOCPageSection(
                    id_enum.TRANSMITTER_WRENCH,
                    0,
                    "通用设置",
                    general_settings.general_settings,
                ),
                TOCPageSection(
                    id_enum.Cable.STEEL,
                    0,
                    "物品管道",
                    cable.cable_entry,
                ),
                TOCPageSection(
                    id_enum.Pipe.BRONZE,
                    0,
                    "流体管道",
                    pipe.pipe_entry,
                ),
            ],
        ),
    ],
)
