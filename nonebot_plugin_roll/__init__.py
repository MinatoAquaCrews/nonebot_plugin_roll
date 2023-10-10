import re
import random
from typing import List
from nonebot import on_command
from nonebot.matcher import Matcher
from nonebot.params import CommandArg, Depends, ArgStr
from nonebot.adapters.onebot.v11 import Message
from nonebot.plugin import PluginMetadata

__plugin_version__ = "v0.2.3a1"
__plugin_usages__ = f"""
掷骰子 {__plugin_version__}
rd/roll/掷骰 [x]d[y] 掷出x个y面的骰子""".strip()

__plugin_meta__ = PluginMetadata(
    name="塔罗牌",
    description="塔罗牌！魔法占卜🔮",
    usage=__plugin_usages__,
    type="application",
    homepage="https://github.com/MinatoAquaCrews/nonebot_plugin_roll",
    extra={
        "author": "KafCoppelia <k740677208@gmail.com>",
        "version": __plugin_version__,
    },
    supported_adapters={"~onebot.v11"},
)

roll = on_command("rd", aliases={"roll", "掷骰"}, priority=10, block=False)


async def get_rd(matcher: Matcher, args: str = ArgStr("rd")) -> None:
    arg: List[str] = args.strip().split()

    if arg and len(arg) > 0:
        if len(arg) > 1:
            await matcher.send("参数过多，仅第一个参数有效")

        matcher.set_arg("rd", Message(arg[0]))
    else:
        await matcher.reject_arg("rd", "你还没掷骰子呢：rd [x]d[y]")


@roll.handle()
async def _(matcher: Matcher, args: Message = CommandArg()) -> None:
    arg: List[str] = args.extract_plain_text().strip().split()

    if arg and len(arg) > 0:
        if len(arg) > 1:
            await matcher.send("参数过多，仅第一个参数有效")

        matcher.set_arg("rd", Message(arg[0]))


@roll.got("rd", prompt="请掷骰子: [x]d[y]", parameterless=[Depends(get_rd)])
async def _(matcher: Matcher):
    dice_num, dice_side = 0, 0

    _roll = matcher.get_arg("rd", None)

    if not _roll:
        await matcher.finish("缺少参数！")

    roll_str = _roll.extract_plain_text()

    if re.match(r"^\d+[d]\d+$", roll_str):
        # <x>d<y>
        dice_info = roll_str.split("d")
        dice_num, dice_side = int(dice_info[0]), int(dice_info[1])
    elif re.match(r"^[d]\d+$", roll_str):
        # d<x>
        dice_num, dice_side = 1, int(roll_str[1:])
    elif re.match(r"^\d+$", roll_str):
        # Any number
        dice_num, dice_side = 1, int(roll_str)
    else:
        await matcher.finish("格式不对呢, 请重新输入: rd [x]d[y]")

    # Bonus
    if dice_num > 999 or dice_side > 999:
        await matcher.finish(f"错误！谁没事干扔那么多骰子啊😅")

    if dice_num <= 0 or dice_side <= 0:
        await matcher.finish(f"错误！你掷出了不存在的骰子, 只有上帝知道结果是多少🤔")

    if dice_num == 114 and dice_side == 514 or dice_num == 514 and dice_side == 114:
        await matcher.finish(f"恶臭！奇迹和魔法可不是免费的！🤗")

    if random.randint(1, 100) == 99:
        await matcher.finish(f"彩蛋！骰子之神似乎不看好你, 你掷出的骰子全部消失了😥")

    _bonus = random.randint(1, 1000)
    bonus = 0
    if _bonus % 111 == 0:
        bonus = _bonus
        await matcher.send(f"彩蛋！你掷出的点数将增加【{bonus}】")

    dice_result = 0
    for i in range(dice_num):
        dice_result += random.choice(range(dice_side)) + 1

    dice_result += bonus

    if dice_result == 6324:
        await matcher.send(f"彩蛋！6324工作室祝大家新年快乐！")

    await matcher.finish(f"你掷出了{dice_num}个{dice_side}面骰子, 点数为【{dice_result}】")
