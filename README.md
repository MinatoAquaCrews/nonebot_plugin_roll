<div align="center">

# Roll

_🎲 掷骰子 🎲_

</div>

<p align="center">

  <a href="https://github.com/KafCoppelia/nonebot_plugin_roll/blob/master/LICENSE">
    <img src="https://img.shields.io/github/license/MinatoAquaCrews/nonebot_plugin_roll?color=blue">
  </a>

  <a href="https://github.com/nonebot/nonebot2">
    <img src="https://img.shields.io/badge/nonebot2-2.0.0+-green">
  </a>

  <a href="https://github.com/MinatoAquaCrews/nonebot_plugin_roll/releases/tag/v0.2.3">
    <img src="https://img.shields.io/github/v/release/MinatoAquaCrews/nonebot_plugin_roll?color=orange">
  </a>

  <a href="https://www.codefactor.io/repository/github/MinatoAquaCrews/nonebot_plugin_roll">
    <img src="https://img.shields.io/codefactor/grade/github/MinatoAquaCrews/nonebot_plugin_roll/master?color=red">
  </a>

  <a href="https://github.com/MinatoAquaCrews/nonebot_plugin_roll">
    <img src="https://img.shields.io/pypi/dm/nonebot_plugin_roll">
  </a>

  <a href="https://results.pre-commit.ci/latest/github/MinatoAquaCrews/nonebot_plugin_roll/master">
	<img src="https://results.pre-commit.ci/badge/github/MinatoAquaCrews/nonebot_plugin_roll/master.svg" alt="pre-commit.ci status">
  </a>

</p>

## 版本

[v0.2.3](https://github.com/MinatoAquaCrews/nonebot_plugin_roll/releases/tag/v0.2.3)

⚠ 适配nonebot2-2.0.0+

## 安装

通过 `pip` 或 `nb-cli` 安装。

## 功能

掷骰！扔出指定个数的多面骰子；支持群聊与私聊。

## 命令

掷骰子：
[rd/roll/掷骰] [x]d[y]，掷出x个y面的骰子，并返回点数。
.r[x]d[y]，开头的点和x均可省略
所有命令后可以空格为间隔添加多个参数，会根据掷骰结果自动输出选项。

### 示例：

#### 基础掷骰

| 输入        | 输出                              |
| ----------- | --------------------------------- |
| `rd2`       | 你掷出了1个2面骰子, 点数为【2】   |
| `r2d6`      | 你掷出了2个6面骰子, 点数为【5】   |
| `.rd2`      | 你掷出了1个2面骰子, 点数为【2】   |
| `.r2d6`     | 你掷出了2个6面骰子, 点数为【6】   |
| `rd 1d2`    | 你掷出了1个2面骰子, 点数为【1】   |
| `roll 2d6`  | 你掷出了2个6面骰子, 点数为【9】   |
| `掷骰 1d20` | 你掷出了1个20面骰子, 点数为【15】 |

#### 带附加参数

| 输入                         | 输出                                                 |
| ---------------------------- | ---------------------------------------------------- |
| `rd2 大米 白面`              | 2=2<br>你掷出了1个2面骰子, 点数为【2】<br>白面       |
| `r3d6 攻击 防御 闪避`        | 3+5+2=10<br>你掷出了3个6面骰子, 点数为【10】<br>防御 |
| `.rd4 东 南 西 北`           | 3=3<br>你掷出了1个4面骰子, 点数为【3】<br>西         |
| `roll 2d6 选项A 选项B 选项C` | 4+1=5<br>你掷出了2个6面骰子, 点数为【5】<br>选项B    |

🎉 掷出特定骰子或特定点数可能有彩蛋！

## 本插件改自

[Omega Miya-roll](https://github.com/Ailitonia/omega-miya)
