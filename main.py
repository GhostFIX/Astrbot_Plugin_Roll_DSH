"""Roll 随机抽选插件。

在多个空格分隔的候选项中随机抽取一个，不依赖 AI 或任何第三方服务。
"""

from __future__ import annotations

import re
import secrets
import shlex
from collections.abc import AsyncGenerator

from astrbot.api.event import AstrMessageEvent, filter
from astrbot.api.star import Context, Star

DEFAULT_MAX_ITEMS = 20
"""默认允许的最大候选项数量。"""

HARD_MAX_ITEMS = 100
"""配置可设置的最大候选项数量上限。"""

MIN_ITEMS = 2
"""一次抽取至少需要的候选项数量。"""

USAGE = (
    "用法：roll <item1> <item2> ...（至少 2 个候选项）\n"
    "例如：roll 苹果 香蕉 橘子"
)


def _coerce_max_items(value: object) -> int:
    """把插件配置中的最大候选项数量收敛到允许范围。"""
    try:
        parsed = int(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return DEFAULT_MAX_ITEMS
    return max(MIN_ITEMS, min(parsed, HARD_MAX_ITEMS))


def _split_items(raw: str) -> list[str]:
    """按空白切分候选项，支持用引号包裹带空格的候选项。

    例如 ``"红色 队伍" 蓝色`` 会得到 ``["红色 队伍", "蓝色"]``。
    反斜杠按普通字符保留，避免 Windows 路径被改写。
    """
    if not raw.strip():
        return []

    lexer = shlex.shlex(raw, posix=False)
    lexer.whitespace_split = True
    lexer.commenters = ""
    lexer.escape = ""
    # 同时把中文全角空格和不换行空格当作分隔符。
    lexer.whitespace += "\u3000\u00a0"
    try:
        tokens = list(lexer)
    except ValueError as exc:
        raise ValueError("候选项中的引号没有闭合。") from exc

    cleaned: list[str] = []
    for token in tokens:
        token = token.strip()
        if len(token) >= 2 and token[0] == token[-1] and token[0] in {"'", '"'}:
            token = token[1:-1].strip()
        if token:
            cleaned.append(token)
    return cleaned


def parse_items(message_str: str) -> list[str]:
    """从完整指令文本中解析候选项。

    AstrBot 的指令过滤器不会改写 ``event.message_str``，因此这里去掉第一段
    命令名，把剩余文本交给引号解析器。第一段不参与判断，所以用户在 WebUI
    的“管理行为”中重命名指令后，本解析逻辑仍然有效。
    """
    text = (message_str or "").strip()
    if not text:
        return []

    parts = re.split(r"\s+", text, maxsplit=1)
    if len(parts) < 2:
        return []

    return _split_items(parts[1])


class RollPlugin(Star):
    """在多个候选项中随机抽取一个。"""

    def __init__(self, context: Context, config: dict | None = None):
        super().__init__(context)
        raw_limit = (config or {}).get("max_items", DEFAULT_MAX_ITEMS)
        self.max_items = _coerce_max_items(raw_limit)

    @filter.command("roll")
    async def roll(self, event: AstrMessageEvent) -> AsyncGenerator[object, None]:
        """从多个候选项中随机抽取一个。"""
        try:
            items = parse_items(event.message_str)
        except ValueError as exc:
            yield event.plain_result(f"{exc}\n\n{USAGE}")
            return

        if len(items) < MIN_ITEMS:
            yield event.plain_result(f"至少需要 {MIN_ITEMS} 个候选项。\n\n{USAGE}")
            return

        if len(items) > self.max_items:
            yield event.plain_result(
                f"候选项太多了：本次提供了 {len(items)} 个，"
                f"上限是 {self.max_items} 个。\n"
                f"可以在插件配置中调整 max_items（最高 {HARD_MAX_ITEMS}）。"
            )
            return

        # secrets.choice 使用系统安全随机源，保证每个候选项被选中的概率相同。
        yield event.plain_result(f"🎲 抽中了：{secrets.choice(items)}")
