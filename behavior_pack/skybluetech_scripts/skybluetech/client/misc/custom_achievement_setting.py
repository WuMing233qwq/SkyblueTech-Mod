# coding = utf-8
import mod.client.extraClientApi as clientApi
from skybluetech_scripts.tooldelta.events.basic import ClientEvent


ACHIEVEMENT_COMMAND = "achievement"


class ClientChatEvent(ClientEvent):
    name = "ClientChatEvent"

    def __init__(self, args=None):
        self.args = args or {}
        self.message = (
            self.args.get("message")
            or self.args.get("msg")
            or self.args.get("chat")
            or self.args.get("command")
            or ""
        )

    @classmethod
    def unmarshal(cls, data):
        return cls(data)

    def cancel(self):
        self.args["cancel"] = True


def SetCustomAchievementHudButtonVisible(visible):
    # type: (bool) -> bool
    achievementSys = clientApi.GetSystem("Minecraft", "achievement")
    if not achievementSys:
        return False

    gate = getattr(achievementSys, "mAchievementGate", None)
    if not gate:
        return False

    gate.SetVisible(gate.mGoodBtn, bool(visible), True)
    gate.UpdateScreen(True)
    return True


@ClientChatEvent.Listen()
def onClientChat(event):
    # type: (ClientChatEvent) -> None
    message = event.message.strip().lower()
    args = message.split()
    if len(args) != 2 or args[0] != ACHIEVEMENT_COMMAND:
        return

    if args[1] == "true":
        SetCustomAchievementHudButtonVisible(True)
    elif args[1] == "false":
        SetCustomAchievementHudButtonVisible(False)
    else:
        return

    event.cancel()
