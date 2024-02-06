from datetime import datetime

import pytest
from nonebot.adapters.console import Message, MessageEvent
from nonebug import App
from nonechat.info import User


def make_event(message: str = "") -> MessageEvent:
    return MessageEvent(
        time=datetime.now(),
        self_id="test",
        message=Message(message),
        user=User(id="123456789"),
    )


@pytest.mark.asyncio
async def test_roll_legal(app: App):
    from nonebot_plugin_roll import roll

    async with app.test_matcher(roll) as ctx:
        bot = ctx.create_bot()

        event = make_event("/roll 114d514 ")
        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "恶臭！奇迹和魔法可不是免费的！🤗", result=None)
        ctx.should_finished(roll)

        event = make_event("/掷骰 0d999")
        ctx.receive_event(bot, event)
        ctx.should_call_send(
            event, "错误！你掷出了不存在的骰子, 只有上帝知道结果是多少🤔", result=None
        )
        ctx.should_finished(roll)

        event = make_event("/掷骰 d0")
        ctx.receive_event(bot, event)
        ctx.should_call_send(
            event, "错误！你掷出了不存在的骰子, 只有上帝知道结果是多少🤔", result=None
        )
        ctx.should_finished(roll)

        event = make_event("/rd -1d1")
        ctx.receive_event(bot, event)
        ctx.should_call_send(
            event, "错误！你掷出了不存在的骰子, 只有上帝知道结果是多少🤔", result=None
        )
        ctx.should_finished(roll)

        event = make_event("/rd d1000")
        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "错误！谁没事干扔那么多骰子啊😅", result=None)
        ctx.should_finished(roll)


@pytest.mark.asyncio
async def test_roll_illegal(app: App):
    from nonebot_plugin_roll import roll

    async with app.test_matcher(roll) as ctx:
        bot = ctx.create_bot()

        event = make_event("/roll ddd")
        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "格式不对呢, 请重新输入: rd [x]d[y]", result=None)
        ctx.should_finished(roll)

        event = make_event("/roll 12345")
        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "格式不对呢, 请重新输入: rd [x]d[y]", result=None)
        ctx.should_finished(roll)

        event = make_event("/roll 1d-1")
        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "格式不对呢, 请重新输入: rd [x]d[y]", result=None)
        ctx.should_finished(roll)


@pytest.mark.asyncio
async def test_roll_got1(app: App):
    from nonebot_plugin_roll import roll

    async with app.test_matcher(roll) as ctx:
        bot = ctx.create_bot()

        event = make_event("/roll")
        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "你还没掷骰子呢：rd [x]d[y]", result=None)
        ctx.should_rejected(roll)

        event = make_event(" 1000d1 1d1 2d2")
        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "参数过多，仅第一个参数有效", result=None)
        ctx.should_call_send(event, "错误！谁没事干扔那么多骰子啊😅", result=None)
        ctx.should_finished(roll)


@pytest.mark.asyncio
async def test_roll_got2(app: App):
    from nonebot_plugin_roll import roll

    async with app.test_matcher(roll) as ctx:
        bot = ctx.create_bot()

        event = make_event("/rd")
        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "你还没掷骰子呢：rd [x]d[y]", result=None)
        ctx.should_rejected(roll)

        event = make_event(" ")
        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "你还没掷骰子呢：[x]d[y]", result=None)
        ctx.should_rejected(roll)

        event = make_event("-1d-1")
        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "格式不对呢, 请重新输入: rd [x]d[y]", result=None)
        ctx.should_finished(roll)
