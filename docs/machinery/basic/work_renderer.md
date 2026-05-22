# WorkRenderer 工作状态渲染基类

表示一个存在 active 状态的机器方块基类。
机器外观会随 active 状态的改变而改变。

派生自 `BaseMachine` 基类。

- 你需要额外创建以下空方法并加上 `@SuperExecutorMeta.execute_super` 装饰器：
    - `SetDeactiveFlag`
    - `UnsetDeactiveFlag`
    - `ResetDeactiveFlags`
    - `FlushDeactiveFlags`

## 基类覆写方法
```python
def OnWorkStatusUpdated(self) -> None
```
当机器工作状态改变时执行的操作。
例如, 改变机器的外观, 播放音效等。
