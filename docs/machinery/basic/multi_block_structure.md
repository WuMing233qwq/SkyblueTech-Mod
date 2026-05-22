# MultiBlockStructure 多方块结构基类

多方块机器结构的基类。

派生自 `BaseMachine` 基类。

## 类属性
| 属性名 | 类型 | 说明 |
| --- | --- | --- |
| structure_palette | StructureBlockPalette \| None | 用于进行多方块完整性检测的多方块结构调色板 |
| functional_block_ids | set[str] | 多方块结构中功能性方块的 ID 列表。GetMachine() 获取的机器方块 ID 都需要包含在其中 |

## 实例属性
| 属性名 | 类型 | 说明 |
| --- | --- | --- |
| last_destroy_flag | (property) int | 上一次检测到的结构销毁标记 |
| lacked_blocks | (property) dict[str, int] | 结构缺失的方块列表 |

## 基类覆写方法
```python
def OnStructureChanged(self, structure_finished: bool) -> None
```
结构变更（完成或破损）时的回调。

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| structure_finished | bool | 结构是否已完成 |

## 基类方法
```python
def GetFunctionalBlockPoses(self) -> dict[str, list[tuple[int, int, int]]]
```
返回功能性方块对于多方块结构核心位置的相对坐标。

| 返回类型 | 说明 |
| --- | --- |
| dict[str, list[tuple[int, int, int]]] | 方块 ID 对应坐标列表 |

---

```python
def GetMachine(self, cls: type[BaseMachine], block_id: str | None = None, index: int = 0) -> BaseMachine
```
获取多方块结构中某一类型的机器（多用于多方块结构接口的获取）。
其 ID 需要被包含在类属性 `functional_block_ids` 中。

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| cls | type[BaseMachine] | 机器类 |
| block_id | str \| None | 机器方块 ID。默认为 cls.block_name |
| index | int | 索引值, 如果有多个匹配的机器则使用索引值 |

| 返回类型 | 说明 |
| --- | --- |
| BaseMachine | 所求机器实例 |

| 异常 | 说明 |
| --- | --- |
| ValueError | 找不到对应机器 |

---

```python
def TryGetMachine(self, cls: type[BaseMachine], block_id: str | None = None, index: int = 0) -> BaseMachine | None
```
GetMachine 的可空返回版本, 获取不到对应机器则返回 None。

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| cls | type[BaseMachine] | 机器类 |
| block_id | str \| None | 机器方块 ID。默认为 cls.block_name |
| index | int | 索引值 |

| 返回类型 | 说明 |
| --- | --- |
| BaseMachine \| None | 所求机器实例, 找不到则返回 None |
