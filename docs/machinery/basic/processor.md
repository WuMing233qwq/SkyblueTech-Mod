# Processor 耗能配方处理器基类

如果你只是单纯地想让机器接受输入，消耗能量，经过一段时间输出产物~~(变成一个熔炉pro)~~， 那么可以直接继承Processor类。

派生自 `ProcessBase` 基类。
`ProcessBase` 派生自 `GUIControl`, `UpgradeControl`, `WorkRenderer` 基类。

目前 Processor 支持与 `MultiFluidContainer` 基类组合。（由于 Processor 本身继承自 `ItemContainer` 基类，所以默认支持）

## 类属性

为了一步到位，直接列出所有可用的类属性，包括父类的类属性。

- 基本类属性：

| 属性名 | 类型 | 说明 | 默认值 |
| --- | --- | --- | --- |
| block_name | str | 机器方块 ID |
| store_rf_max | int | 机器最大存储能量 | 10000 |
| process_item | bool | 是否需要处理物品，有物品输入或输出都要设为 True。下同 | False |
| process_fluid | bool | 是否需要处理流体 | False |
| recipes | RecipesCollection\[MachineRecipe] | 机器可用配方集 |
| upgrade_slot_start | int | 升级槽集合的首个槽位索引 | 2 |
| upgrade_slots | int | 升级槽集合的槽位数量 | 4 |

- 物品容器基类属性：

| 属性名 | 类型 | 说明 | 默认值 |
| --- | --- | --- | --- |
| input_slots | tuple\[int] | 物品输入槽位 | () |
| output_slots | tuple\[int] | 物品输出槽位 | () |

- 多流体容器基类属性：

| 属性名 | 类型 | 说明 | 默认值 |
| --- | --- | --- | --- |
| fluid_input_slots | set\[int] | 可用的流体输入槽位 | set() |
| fluid_output_slots | set\[int] | 可用的流体输出槽位 | set() |
| fluid_slot_max_volumes | tuple\[float] | 每个流体槽位最大容量 | () |

## 提示

当与任意机器基类组合时，你需要额外添加 `__init__` 空方法， 防止两个父类同名方法冲突：
```python
@RegisterMachine
class FluidCondenser(MultiFluidContainer, Processor):
    ...

    @SuperExecutorMeta.execute_super
    # 会使得在执行 __init__ 时先行执行两个父类的 __init__ 方法
    def __init__(self, dim, x, y, z, block_entity_data):
        pass
```

当与 `MultiFluidContainer` 组合时，你需要额外添加两个空方法：
```python
@RegisterMachine
class FluidCondenser(MultiFluidContainer, Processor):
    ...

    @SuperExecutorMeta.execute_super
    def OnAddedFluid(self, slot, fluid_id, fluid_volume, is_final):
        pass

    @SuperExecutorMeta.execute_super
    def OnReducedFluid(self, slot, fluid_id, reduced_fluid_volume, is_final):
        pass
```