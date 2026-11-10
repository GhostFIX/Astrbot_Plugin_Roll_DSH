# Roll 随机抽选

<p align="center">
  <img src="logo.png" width="128" alt="Roll 随机抽选插件 Logo">
</p>

![AstrBot](https://img.shields.io/badge/AstrBot-%3E%3D4.16%2C%20%3C5-76bad9)
![License](https://img.shields.io/badge/license-MIT-green)

一个符合 AstrBot 插件规范的轻量随机抽选插件：在多个候选项中随机选出一个。

```text
/roll 苹果 香蕉 橘子
🎲 抽中了：香蕉
```

- 默认指令名：`roll`
- 默认最多 **20** 个候选项，可在插件配置中调整，最高 **100** 个
- 不需要 AI、不需要额外依赖、不访问网络、不保存聊天数据

## 功能

- 在 2～20 个候选项中等概率随机抽取一个（可通过配置提高上限至 100）。
- 候选项使用空格分隔，支持单引号或双引号包裹带空格的内容。
- 结果以纯文本回复，不经过大模型，响应速度快。
- 指令名可以在 AstrBot WebUI 的“插件 → 管理行为 → 指令”中重命名，插件无需改代码。


## 安装

### 方式一：通过自定义插件源安装（推荐）

前提：插件仓库已推送到 GitHub，且默认分支为 `main`。本仓库已经包含符合 AstrBot 插件市场规范的 `plugins.json`。

1. 在 GitHub 打开仓库，确认以下地址可以访问并返回 JSON：

   <https://raw.githubusercontent.com/GhostFIX/Astrbot_Plugin_Roll_DSH/main/plugins.json>

2. 打开 AstrBot WebUI，进入 **插件 → 插件市场 → 插件源管理**。
3. 添加自定义插件源，地址填写上面的 `plugins.json` 链接。
4. 保存后刷新插件市场，搜索 **Roll 随机抽选** 并安装。
5. 回到“已安装”页面，确认插件已启用。
6. 在聊天中发送：

   ```text
   /roll 苹果 香蕉 橘子
   ```

### 方式二：从仓库链接安装

在 AstrBot 的 **插件 → 安装插件（+）→ 从链接安装** 中填写：

```text
https://github.com/GhostFIX/Astrbot_Plugin_Roll_DSH
```

### 方式三：手动安装

把仓库放到 AstrBot 的插件目录，目录名建议使用 `astrbot_plugin_roll`：

```bash
git clone https://github.com/GhostFIX/Astrbot_Plugin_Roll_DSH.git AstrBot/data/plugins/astrbot_plugin_roll
```

```text
AstrBot/data/plugins/astrbot_plugin_roll/
├── main.py
├── metadata.yaml
├── _conf_schema.json
└── ...
```

然后在 WebUI 中重载插件，或重启 AstrBot。

## 使用

默认唤醒前缀为 `/`；如果你修改过 AstrBot 的唤醒前缀，请使用对应前缀，例如 `!roll 苹果 香蕉`。

```text
/roll 苹果 香蕉 橘子
/roll "火锅" "烧烤" "麻辣烫"
/roll 读书 运动 早睡 打游戏
```

规则：

- 至少提供 **2** 个候选项。
- 默认最多 **20** 个；可在插件配置中把 `max_items` 调到 2～100。
- 超过上限时会拒绝抽取并提示当前上限，不会截断候选项。
- 重复的候选项按出现次数计算概率。例如 `roll 苹果 苹果 香蕉` 中苹果被抽中的概率为 2/3。
- 带空格的候选项必须用引号包裹；未闭合的引号会返回用法提示。
- 只抽取 **一个** 结果，不支持一次抽多个。

### 重命名指令

默认指令名是 `roll`。如需改名：

1. 打开 AstrBot WebUI → **插件 → 管理行为 → 指令**。
2. 找到本插件注册的 `roll` 指令，修改名称并保存。
3. 新名称立即生效，插件内部会根据消息的第一段自动识别命令，无需修改代码。

## 配置

配置文件由 `_conf_schema.json` 自动生成，路径通常为：

```text
AstrBot/data/config/astrbot_plugin_roll_config.json
```

| 配置项 | 类型 | 默认值 | 范围 | 说明 |
| --- | --- | --- | --- | --- |
| `max_items` | int | `20` | `2`～`100` | 单次抽取允许的最大候选项数量 |

即使手动把配置文件改成更大的值，插件也会把它限制在 100 以内。

## 自定义源说明

`plugins.json` 遵循 AstrBot 插件市场 JSON 规范（schema 版本 `1`）：

- `$meta.schema_version` 为 `1`。
- 插件记录键为 `GhostFIX/astrbot_plugin_roll`。
- `author`、`name`、`version`、`repo` 分别与 `metadata.yaml` 保持一致。
- 安装时 AstrBot 会读取仓库根目录的 `metadata.yaml`，并校验插件身份。

发布新版本时，请同步更新 `metadata.yaml`、`plugins.json` 与 `CHANGELOG.md` 中的版号和说明。

如果自定义源添加后市场为空或安装失败，请依次检查：

1. `plugins.json` 的 Raw 链接是否能在浏览器直接打开。
2. 仓库是否为公开仓库，默认分支名是否正确。
3. `plugins.json` 中的 `repo` 是否是实际仓库地址。
4. `metadata.yaml` 中的 `name`、`author`、`version` 是否与 `plugins.json` 完全一致。

## 兼容性

- AstrBot：`>=4.16,<5`（`metadata.yaml` 中的 `astrbot_version`）。
- Python：以 AstrBot 运行环境为准；插件代码兼容 Python 3.10+。
- 消息平台：所有支持文本消息的 AstrBot 适配器均可使用，不依赖特定平台能力。

## 开发与测试

本插件只使用 Python 标准库和 AstrBot 自带 API，没有第三方运行时依赖。

```bash
python -m unittest discover -s tests -v
python -m compileall -q main.py
```

测试使用最小 AstrBot API 桩，因此不需要安装 AstrBot 本体。

## 项目结构

```text
.
├── main.py                 # 插件实现
├── metadata.yaml           # AstrBot 插件元数据
├── _conf_schema.json       # 插件配置 schema
├── plugins.json            # 自定义插件源（AstrBot 市场 JSON）
├── logo.png                # 插件 Logo（可选）
├── tests/test_plugin.py    # 功能单元测试
├── tests/test_packaging.py # 元数据与插件源一致性测试
├── .github/workflows/ci.yml
├── README.md
├── CHANGELOG.md
└── LICENSE
```

## 隐私

插件不会主动发起网络请求，不会读取或写入聊天记录，也不会持久化抽取结果。所有候选项只存在于当前消息的处理过程中。

## License

[MIT](LICENSE)

## 参考

- [AstrBot 插件开发指南](https://docs.astrbot.app/dev/star/plugin-new.html)
- [AstrBot 插件市场 JSON 规范](https://docs.astrbot.app/dev/plugin-market/2026-06-27.html)
- [AstrBot 插件安装说明](https://docs.astrbot.app/use/plugin.html)
