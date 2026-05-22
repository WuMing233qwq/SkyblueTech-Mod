# HeatCtrl 热机控制基类

热机机器类, 表示产热或吸热的机器。

派生自 `BaseMachine` 基类。

- 你需要额外创建以下空方法并加上 `@SuperExecutorMeta.execute_super` 装饰器：
    - `OnTicking`

## 类属性
| 属性名 | 类型 | 说明 |
| --- | --- | --- |
| heat_power | float | 产热功率, 正值代表高于环境温度, 负值代表低于环境温度 |
| spread_heat | bool | 是否扩散热量, 默认为 False |
| max_heat_value | float | 本机最大热值, 默认为 600.0 |

## 实例属性
| 属性名 | 类型 | 说明 |
| --- | --- | --- |
| heat_value | (property) float | 本机当前的热量值 |
| kelvin | (property) float | 本机当前的开尔文温度值 |

## 基类方法
```python
def SetOutputHeatPower(self, power: float) -> None
```
设置热机输出功率。

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| power | float | 新的热功率值 |
