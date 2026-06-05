# coding=utf-8
from ...common.define import id_enum
from ...common.define import tag_enum
from .core import CategoryType
from .common import RegisterDescription

# RegisterDescription(
#     {CategoryType.FLUID: [RAW_OIL]},
#     "原油获取",
#     "你可以在地下、 海上或矿洞里找到天然油井或者油田。 \n油田里的油是有限的， 可以供你装桶以便临时之需。\n油井可以提取的原油储量几乎可以认为是无限的， 你可以在油井旁就地建立一个炼油产线以提取各种油料产物。"
# )

RegisterDescription(
    {CategoryType.ITEM: ["skybluetech:description_icon"]},
    "关于介绍的介绍？！",
    "这是一个介绍， 它并没有“获取途径”， 但是你却可以通过查看介绍的介绍来获取介绍的介绍。 是不是很有趣？\n\n噢不， 为什么在座各位都被冻住了？",
)

RegisterDescription(
    {CategoryType.ITEM: [id_enum.INSCRIBING_TEMPLATE]},
    "刻印模版",
    "你可以在一些遗迹的藏宝箱里找到刻录有正确电路格式的刻印模版。\n你可以将模版放入§d模版成型机§r里制造模版对应的物品。\n§c注意！§r不要修改已刻录好正确格式的刻印模版， 如果你不知道怎么将模版图改回正确的格式， 它就没办法再拿去按模版制造对应物品了。",
)
