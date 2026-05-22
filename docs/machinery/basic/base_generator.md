# BaseGenerator 发电机基类

发电机基类, 适合产出稳定的发电机器使用。
提供了 SetOutputPower() 方法。
如果需要对溢出发电量进行管理或者控制单次的发电量, 请使用 BasePowerProvider。

派生自 `BasePowerProvider` 基类。

- 你需要额外创建以下空方法并加上 `@SuperExecutorMeta.execute_super` 装饰器：
    - `OnTicking`

## 实例属性
| 属性名 | 类型 | 说明 |
| --- | --- | --- |
| output_power | int | 发电机当前的输出功率 |

## 基类方法
```python
def SetOutputPower(self, power: int) -> None
```
设置发电机输出功率。

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| power | int | 新的输出功率值 |
