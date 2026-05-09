import random
import re

from nonebot import on_regex
from nonebot.adapters import Event
from nonebot.matcher import Matcher
from nonebot.plugin import PluginMetadata

__plugin_version__ = "v0.2.3"
__plugin_usages__ = f"""
掷骰子 {__plugin_version__}
支持格式：
  rd2                 - 掷1个2面骰（无空格）
  r1d2                - 掷1个2面骰（无空格）
  .rd2                - 支持点号开头
  .r1d2               - 支持点号开头
  rd 1d2              - 原格式（有空格）
  roll 2d6            - roll命令（有空格）
  掷骰 2d6            - 中文命令（有空格）

附加参数功能（用空格分隔）：
  rd2 大米 白面        - 根据点数选择对应项
  r3d6 攻击 防御 闪避  - 多骰子带参数

计算过程显示（不超过20个骰子时）：
  显示 1+2+3=6 格式""".strip()

__plugin_meta__ = PluginMetadata(
    name="掷骰子",
    description="掷骰！扔出指定个数的多面骰子🎲，支持附加参数选择",
    usage=__plugin_usages__,
    type="application",
    homepage="https://github.com/MinatoAquaCrews/nonebot_plugin_roll",
    extra={
        "author": "KafCoppelia <k740677208@gmail.com>",
        "version": __plugin_version__,
    },
    supported_adapters=None,
)

# 正则匹配：支持 .rd2, rd2, r1d2, .r1d2 等无空格格式
# 同时也支持原格式（rd/roll/掷骰 后有空格）
roll = on_regex(r"^(?:\.?r(?:d?)(?:\d*d\d+|\d+))|(?:rd|roll|掷骰)\s+\S+", priority=8)


def parse_dice_expression(expr: str):
    """
    解析骰子表达式，返回 (dice_num, dice_side)
    支持格式：2d6, d6, 6
    """
    expr = expr.strip().lower()

    # 标准 xdy 格式
    match = re.match(r"^(\d*)d(\d+)$", expr)
    if match:
        num_str, side_str = match.groups()
        dice_num = int(num_str) if num_str else 1
        dice_side = int(side_str)
        return dice_num, dice_side

    # 纯数字格式（如 2 表示 1d2）
    match = re.match(r"^(\d+)$", expr)
    if match:
        dice_side = int(match.group(1))
        return 1, dice_side

    return None, None


def extract_options(text: str):
    """从文本中提取选项列表（空格分割）"""
    if not text:
        return []
    return [opt.strip() for opt in text.split() if opt.strip()]


def roll_dice(dice_num: int, dice_side: int):
    """掷骰子，返回 (results_list, total_sum)"""
    results = [random.randint(1, dice_side) for _ in range(dice_num)]
    return results, sum(results)


def format_roll_process(results: list, total: int, bonus: int = 0):
    """格式化掷骰过程（当骰子数 ≤20 时使用）"""
    if not results:
        return ""
    process = "+".join(str(r) for r in results)
    if bonus > 0:
        process += f"+{bonus}"
    process += f"={total}"
    return process


async def send_roll_result(
    matcher: Matcher,
    dice_num: int,
    dice_side: int,
    results: list,
    total: int,
    bonus: int,
    options: list,
):
    """发送掷骰结果"""
    output_lines = []

    # 显示计算过程（不超过20个骰子）
    if dice_num <= 20 and dice_num > 0:
        process_str = format_roll_process(results, total + bonus, bonus)
        if process_str:
            output_lines.append(process_str)

    # 标准输出
    output_lines.append(f"你掷出了{dice_num}个{dice_side}面骰子, 点数为【{total + bonus}】")

    # 参数选择
    if options:
        idx = (total - 1) % len(options)
        selected = options[idx]
        output_lines.append(selected)

    await matcher.finish("\n".join(output_lines))


@roll.handle()
async def handle_roll(matcher: Matcher, event: Event):
    """统一处理所有掷骰请求"""
    raw_msg = event.get_plaintext().strip()

    # 提取骰子表达式和选项
    dice_expr = None
    options_text = ""

    # 情况1：无空格格式（rd2, r1d2, .rd2, .r1d2）
    match_compact = re.match(
        r"^\.?r(?:d?)(\d*d\d+|\d+)(?:\s+(.*))?$", raw_msg, re.IGNORECASE
    )

    if match_compact:
        dice_expr = match_compact.group(1)
        options_text = match_compact.group(2) or ""

    # 情况2：原格式（rd/roll/掷骰 后面有空格）
    else:
        match_spaced = re.match(
            r"^(?:rd|roll|掷骰)\s+(\S+)(?:\s+(.*))?$", raw_msg, re.IGNORECASE
        )

        if match_spaced:
            dice_expr = match_spaced.group(1)
            options_text = match_spaced.group(2) or ""

    # 未匹配到任何格式
    if not dice_expr:
        await matcher.finish(
            "格式不对呢，请使用：\n"
            "  rd2           - 掷1个2面骰\n"
            "  r1d2          - 掷1个2面骰\n"
            "  .rd2          - 点号开头\n"
            "  .r1d2         - 点号开头\n"
            "  rd 1d2        - 原格式\n"
            "  roll 2d6      - roll命令\n"
            "  掷骰 2d6      - 中文命令"
        )
        return

    # 解析选项
    options = extract_options(options_text)

    # 解析骰子参数
    dice_num, dice_side = parse_dice_expression(dice_expr)

    if dice_num is None or dice_side is None:
        await matcher.finish("骰子格式错误，请使用：rd2 或 r2d6 或 d6")
        return

    # 限制检查
    if dice_num > 999 or dice_side > 999:
        await matcher.finish("错误！谁没事干扔那么多骰子啊😅")

    if dice_num <= 0 or dice_side <= 0:
        await matcher.finish("错误！你掷出了不存在的骰子，只有上帝知道结果是多少🤔")

    # 彩蛋：114514
    if (dice_num == 114 and dice_side == 514) or (dice_num == 514 and dice_side == 114):
        await matcher.finish("恶臭！奇迹和魔法可不是免费的！🤗")

    # 彩蛋：1%概率骰子消失
    if random.randint(1, 100) == 99:
        await matcher.finish("彩蛋！骰子之神似乎不看好你，你掷出的骰子全部消失了😥")

    # 彩蛋：随机加成
    _bonus_rand = random.randint(1, 1000)
    bonus = 0
    if _bonus_rand % 111 == 0:
        bonus = _bonus_rand
        await matcher.send(f"彩蛋！你掷出的点数将增加【{bonus}】")

    # 掷骰
    results, total = roll_dice(dice_num, dice_side)
    final_total = total + bonus

    # 彩蛋：6324
    if final_total == 6324:
        await matcher.send("彩蛋！6324工作室祝大家新年快乐！")

    # 发送结果
    await send_roll_result(matcher, dice_num, dice_side, results, total, bonus, options)
