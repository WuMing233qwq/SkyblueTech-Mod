# BasePowerProvider 能量源机器基类

能量提供类机器的基类。

派生自 `BaseMachine` 基类。


## 基类方法

```python
def PowerFull(self) -> bool
```

机器能量是否已满。

| 返回类型 | 说明 |
| ---- | -- |
| bool | 如题 |

---

```python
def GeneratePower(self, rf: int) -> tuple[bool, int]
```

产出能量, 返回是否进行了供能和能量溢出值。

| 参数 | 类型  | 说明 |
| -- | --- | -- |
| rf | int | 能量 |

| 返回类型              | 说明             |
| ----------------- | -------------- |
| tuple\[bool, int] | 是否进行了供能, 能量溢出值 |

