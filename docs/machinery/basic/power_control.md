# PowerControl 功率控制器基类

机器的额定功率控制器。
自动控制机器的 active 状态。

派生自 `BaseMachine` 基类。

## 实例属性
| 属性名 | 类型 | 说明 |
| --- | --- | --- |
| running_power | int | 机器当前的运行功率, 默认为 1000 |

## 基类方法
```python
def SetPower(self, power: int) -> None
```
设置机器当前功率。

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| power | int | 新的功率值 |

---

```python
def SetPowerPositiveRate(self, rate: float) -> None
```
设置耗能正倍率; 仅提供给升级类用。

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| rate | float | 倍率值 |

---

```python
def SetPowerNegativeRate(self, rate: float) -> None
```
设置耗能负倍率; 仅提供给升级类用。

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| rate | float | 倍率值 |

---

```python
def ReducePower(self, rf: int | None = None) -> None
```
消耗能量。如果未指定能量值, 则使用当前运行功率。

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| rf | int \| None | 能量值。默认为 None, 即使用 running_power |

---

```python
def PowerEnough(self) -> bool
```
机器当前能量是否足够运行。如果不够, 则将机器设置为停机（能量不足）。

| 返回类型 | 说明 |
| --- | --- |
| bool | 能量是否足够 |
