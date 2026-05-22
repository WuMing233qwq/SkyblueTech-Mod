# coding=utf-8
from skybluetech_scripts.skybluetech.common.define import id_enum
from ...define import (
    TOCPage,
    TOCPageSection,
    PageGroup,
)

from . import famicom, resin_collector

misc_toc = PageGroup(
    "misc_toc",
    [
        TOCPage(
            [
                TOCPageSection(
                    id_enum.RESIN_COLLECTOR,
                    0,
                    "树脂采集",
                    resin_collector.resin_collect,
                ),
                TOCPageSection(id_enum.FAMICOM, 0, "红白机音乐", famicom.famicom),
            ],
        ),
    ],
)
