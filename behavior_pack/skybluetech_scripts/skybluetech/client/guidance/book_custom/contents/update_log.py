# coding=utf-8
from skybluetech_scripts.skybluetech.common.define import id_enum
from ..define import (
    TextPage,
    PageGroup,
)


update_log_desc = PageGroup(
    "update_log_desc",
    [
        TextPage(
            "更新日志",
            '在这里可以查看<text color="§9" t="《蔚蓝科技》">的更新日志。',
        ),
        TextPage(
            "",
            '05/10/2026\n\n<text color="§c" t="修复以下问题：">\n1. 能源中继塔接线模式有几率触发“无效终点”，且退出按钮过于靠右导致圆角手机无法按到退出键；\n2. 物品分拣器在特定情况下可以刷物品\n3. 蔚蓝系列工具无法放入充能台进行充能\n4. 线缆无法设置传输优先级\n5. 同时放置10台以上的深层熔岩勘探器导致客户端卡顿\n6. 一些多方块结构被破坏时仍能正常使用\n7. 基岩熔岩钻开基岩层过快\n8. 矿物无法在高炉进行冶炼\n9. 铜棒出现套娃合成\n\n<text color="§9" t="功能优化：">\n书本界面尺寸减小，防止书页按钮超出屏幕\n\n<text color="§a" t="新内容加入：">\n沙底水培床， 可以培育甘蔗和仙人掌。',
        ),
    ],
)
