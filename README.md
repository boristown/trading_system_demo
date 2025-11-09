# Trading System Demo

使用 [ccxt](https://github.com/ccxt/ccxt) 构建的加密货币自动交易系统示例，包含基础的均线策略、交易撮合以及运行说明，便于快速了解如何搭建自动化交易流程。

> ⚠️ **风险提示**：该项目仅用于学习和演示目的。真实交易存在高风险，请务必谨慎评估并自行承担风险。

## 功能概览

- 基于 `ccxt` 的交易所封装，支持切换交易所、沙盒模式与 Dry-Run 模式
- 简单的快慢均线交叉策略（SMA Crossover）
- 可配置的轮询间隔、交易对、下单数量等参数
- 支持 `.env` 环境变量配置，并提供命令行入口

## 项目结构

```
.
├── requirements.txt        # 运行依赖
├── src/trading_system/
│   ├── __init__.py
│   ├── config.py           # 配置读取
│   ├── exchange.py         # ccxt 封装
│   ├── strategy.py         # 策略实现
│   ├── trader.py           # 交易执行逻辑
│   └── main.py             # CLI 入口
└── README.md
```

## 环境准备

1. 安装依赖：

   ```bash
   pip install -r requirements.txt
   ```

2. 申请交易所 API Key，并确认是否支持沙盒环境。

## 配置说明

通过环境变量或 `.env` 文件配置系统参数。常用变量如下：

| 变量名 | 说明 | 默认值 |
| --- | --- | --- |
| `TS_EXCHANGE_ID` | 交易所名称（例如 `binance`、`okx`）| `binance` |
| `TS_SYMBOL` | 交易对 | `BTC/USDT` |
| `TS_TIMEFRAME` | K线周期 | `1m` |
| `TS_FAST_WINDOW` | 快速均线周期 | `5` |
| `TS_SLOW_WINDOW` | 慢速均线周期 | `20` |
| `TS_BASE_ORDER_SIZE` | 每次下单数量（基础币种） | `0.001` |
| `TS_QUOTE_CURRENCY` | 计价币种 | `USDT` |
| `TS_API_KEY` | 交易所 API Key | 无 |
| `TS_API_SECRET` | 交易所 API Secret | 无 |
| `TS_API_PASSPHRASE` | 某些交易所需要的 passphrase | 无 |
| `TS_DRY_RUN` | Dry-Run 模式（`true` 表示不真实下单） | `true` |
| `TS_SANDBOX` | 是否启用沙盒环境 | `false` |
| `TS_POLL_INTERVAL` | 轮询间隔（秒） | `60` |

示例 `.env`：

```
TS_EXCHANGE_ID=binance
TS_SYMBOL=BTC/USDT
TS_API_KEY=your_api_key
TS_API_SECRET=your_api_secret
TS_DRY_RUN=false
TS_SANDBOX=true
```

## 运行方式

一次性执行策略：

```bash
python -m trading_system.main --once --env-file .env
```

持续运行（默认 60 秒轮询一次）：

```bash
python -m trading_system.main --env-file .env
```

添加 `-v` 可查看调试日志：

```bash
python -m trading_system.main --once -v
```

## 策略说明

当前示例策略为简单的快慢均线交叉：

- 当快速均线 > 慢速均线时触发买入信号
- 当快速均线 < 慢速均线时触发卖出信号
- Dry-Run 模式下不会实际下单，只会在日志中记录模拟结果

可在 `src/trading_system/strategy.py` 中扩展或替换策略逻辑。

## 后续扩展建议

- 添加风险控制（止损、止盈、持仓管理）
- 引入多种策略并实现策略调度
- 对接数据库或消息队列，记录实时交易数据
- 构建可视化监控面板

祝交易顺利，注意风险！
