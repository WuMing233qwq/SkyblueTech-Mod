# SPControl 速度与能量控制合并基类

速度和能量控制基类合并, 并覆写一个更方便合理的 ProcessOnce() 方法。

派生自 `BaseSpeedControl` 和 `PowerControl`。

## 基类方法
```python
def ProcessOnce(self) -> bool
```
尝试处理一次配方, 会消耗能量, 如可处理返回 True, 制作中或能量不足返回 False。

值得注意的是, 我们可能要在 1tick 之内进行多次配方产出。

| 返回类型 | 说明 |
| --- | --- |
| bool | 是否已处理完一次配方, 可以结束配方运行 |
