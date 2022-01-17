import re
import random
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.params import State
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
from nonebot.adapters.onebot.v11.permission import GROUP

roll = on_command(
    'roll',
    # 使用run_preprocessor拦截权限管理, 在default_state初始化所需权限
    state={
        '_matcher_name': 'roll',
        '_command_permission': True,
        '_permission_level': 10,
        '_cool_down': 5
    },
    aliases={'Roll', '掷骰子', '掷骰', 'rd'},
    permission=GROUP,
    priority=10,
    block=True)


# 修改默认参数处理
@roll.args_parser
async def parse(bot: Bot, event: GroupMessageEvent, state: T_State = State()):
    args = str(event.get_plaintext()).strip().lower().split()
    if not args:
        await roll.reject('你似乎没有发送有效的参数, 请重新发送:')
    state[state["_current_key"]] = args[0]
    if state[state["_current_key"]] == '取消':
        await roll.finish('操作已取消')


@roll.handle()
async def handle_first_receive(bot: Bot, event: GroupMessageEvent, state: T_State = State()):
    args = str(event.get_plaintext()).strip().lower().split()
    if not args:
        pass
    elif args and len(args) == 1:
        state['roll'] = args[0]
    else:
        await roll.finish('参数错误QAQ')


@roll.got('roll', prompt='请掷骰子: <x>d<y>')
async def handle_roll(bot: Bot, event: GroupMessageEvent, state: T_State):
    _roll = state['roll']
    if re.match(r'^\d+[d]\d+$', _roll):
        # <x>d<y>
        dice_info = _roll.split('d')
        dice_num = int(dice_info[0])
        dice_side = int(dice_info[1])
    elif re.match(r'^[d]\d+$', _roll):
        # d<x>
        dice_num = 1
        dice_side = int(_roll[1:])
    elif re.match(r'^\d+$', _roll):
        # Any number
        dice_num = 1
        dice_side = int(_roll)
    else:
        await roll.finish(f'格式不对呢, 请重新输入: /roll <x>d<y>:')
        return

    # 加入一个趣味的机制
    if random.randint(1, 100) == 99:
        await roll.finish(f'【彩蛋】骰子之神似乎不看好你, 你掷出的骰子全部消失了😥')
    if dice_num > 1024 or dice_side > 1024:
        await roll.finish(f'【错误】谁没事干扔那么多骰子啊😅')
    if dice_num <= 0 or dice_side <= 0:
        await roll.finish(f'【错误】你掷出了不存在的骰子, 只有上帝知道结果是多少🤔')
    dice_result = 0
    for i in range(dice_num):
        this_dice_result = random.choice(range(dice_side)) + 1
        dice_result += this_dice_result
    await roll.finish(f'你掷出了{dice_num}个{dice_side}面骰子, 点数为【{dice_result}】')
