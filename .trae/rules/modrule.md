---
alwaysApply: true
---

- **优先使用本模组使用的封装库 tooldelta**, 优先在 behavior_pack/skybluetech_scripts/tooldelta/api 下查找 modapi 接口的实现, 在 behavior_pack/skybluetech_scripts/tooldelta/events 下查找 modapi 事件的实现。 如在 tooldelta 库查找不到但是使用 MCP 调用 minecraft_mod_assistant 找得到, 需要显式说明让用户封装接口/事件。
    - 如查找获取特定坐标方块的 ID, 在 tooldelta 库找到了 (tooldelta/api/server/block.py: def GetBlockName), 则使用 `from skybluetech_scripts.tooldelta.api.server import GetBlockName` 导入接口。
- **严禁凭感觉编接口!**
- **遇到任何不确定的模组运行逻辑都应当先行询问用户, 强行中断编写**
- 非 Python Builtin 库导入的模块(也就是模组自行使用的模块)都要应当从 skybluetech_scripts 下导入, 以它为顶层模块。
- 禁止擅自编译py文件
- 这是一个minecraft-bedrock模组项目, 使用python2语言开发, 但是实际上是py2和py3兼容的写法, 实际运行环境是python2.7.13
- minecraft_mod_assistant MCP工具应该使用`中文且短的keyword`进行搜索