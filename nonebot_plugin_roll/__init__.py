import re
import random
from typing import List
from nonebot import on_command
from nonebot.matcher import Matcher
from nonebot.params import CommandArg, Depends, ArgStr
from nonebot.adapters.onebot.v11 import Message

__roll_version__ = "v0.2.2a1"
__roll_notes__ = f'''
掷骰子 {__roll_version__}
rd/roll/掷骰/骰子 [x]d[y] 掷出x个y面的骰子'''.strip()

roll = on_command("rd", aliases={"roll", "掷骰"}, priority=10, block=False)

def get_rd():
    async def _rd_parser(matcher: Matcher, args: str = ArgStr("rd")) -> None:
        arg: List[str] = args.strip().split()
        
        if arg and len(arg) > 0:
            if len(arg) > 1:
                await matcher.send("参数过多，仅第一个参数有效")
            
            matcher.set_arg("rd", Message(arg[0]))
        else:
            await matcher.reject_arg("rd", "你还没掷骰子呢：[x]d[y]")
    
    return  _rd_parser

@roll.handle()
async def _(matcher: Matcher, args: Message = CommandArg()):
    arg: List[str] = args.extract_plain_text().strip().split()
    
    if arg and len(arg) > 0:
        if len(arg) > 1:
            await matcher.send("参数过多，仅第一个参数有效")
        
        matcher.set_arg("rd", Message(arg[0]))

@roll.got("rd", prompt="请掷骰子: [x]d[y]", parameterless=[Depends(get_rd())])
async def _(matcher: Matcher):
    dice_num: int = 0
    dice_side: int = 0
    
    __roll = matcher.get_arg("rd", None)
    
    if not __roll:
        await matcher.finish("输入参数错误！")
    
    _roll: str = __roll.extract_plain_text() 
    
    if re.match(r"^\d+[d]\d+$", _roll):
        # <x>d<y>
        dice_info = _roll.split('d')
        dice_num = int(dice_info[0])
        dice_side = int(dice_info[1])   
    elif re.match(r"^[d]\d+$", _roll):
        # d<x>
        dice_num = 1
        dice_side = int(_roll[1:])
    elif re.match(r"^\d+$", _roll):
        # Any number
        dice_num = 1
        dice_side = int(_roll)
    else:
        await matcher.finish("格式不对呢, 请重新输入: /rd [x]d[y]")

    # Bonus
    if dice_num > 999 or dice_side > 999:
        await matcher.finish(f"错误！谁没事干扔那么多骰子啊😅")
    
    if dice_num <= 0 or dice_side <= 0:
        await matcher.finish(f"错误！你掷出了不存在的骰子, 只有上帝知道结果是多少🤔")
    
    if dice_num == 114 and dice_side == 514 or dice_num == 514 and dice_side == 114:
        await matcher.finish(f"恶臭！奇迹和魔法可不是免费的！🤗")
    
    if random.randint(1, 100) == 99:
        await matcher.finish(f"彩蛋！骰子之神似乎不看好你, 你掷出的骰子全部消失了😥")
    
    _bonus: int = random.randint(1, 1000)
    bonus: int = 0
    if _bonus % 111 == 0:
        bonus = _bonus
        await matcher.send(f"彩蛋！你掷出的点数将增加【{bonus}】")
    
    dice_result: int = 0
    for i in range(dice_num):
        dice_result += random.choice(range(dice_side)) + 1
        
    dice_result += bonus
    
    await matcher.finish(f"你掷出了{dice_num}个{dice_side}面骰子, 点数为【{dice_result}】")