# UpgradeControl 升级卡控制基类

代表可接受升级卡的机器基类。

派生自 `ItemContainer` 和 `SPControl`。

## 类属性
| 属性名 | 类型 | 说明 |
| --- | --- | --- |
| upgrade_slot_start | int | 升级槽起始槽位 |
| upgrade_slots | int | 升级槽数量 |
| allow_upgrader_tags | set[str] | 可接受的机器升级卡标签 |

## 基类方法
```python
def InUpgradeSlot(self, slot: int) -> bool
```
检查某槽位是否为升级槽。

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| slot | int | 槽位 ID |

| 返回类型 | 说明 |
| --- | --- |
| bool | 如题 |

---

```python
def GetAllUpgraders(self) -> dict[str, int]
```
获取所有升级卡。

| 返回类型 | 说明 |
| --- | --- |
| dict[str, int] | 升级卡字典, 键为升级卡 ID, 值为升级卡数量 |

---

```python
def UpdateUpgraders(self, upgraders: dict[str, int]) -> None
```
根据升级卡更新基本的速度和能量升级处理。

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| upgraders | dict[str, int] | 升级卡字典, 键为升级卡 ID, 值为升级卡数量 |

---

```python
def HasUpgrader(self, item_id: str) -> bool
```
检查机器是否拥有某一升级卡。

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| item_id | str | 升级卡 ID |

| 返回类型 | 说明 |
| --- | --- |
| bool | 如题 |
