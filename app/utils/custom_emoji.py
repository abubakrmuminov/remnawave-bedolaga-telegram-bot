"""Custom Telegram Emoji helpers and ID mappings."""

from __future__ import annotations

import re

# Custom emoji IDs mapping (Telegram Premium / custom emoji pack)
CUSTOM_EMOJI_IDS: dict[str, str] = {
    '👤': '5879770735999717115',
    '🛡': '5931409969613116639',
    '💰': '5992430854909989581',
    '💎': '6028530359975548369',
    '🎁': '5963213811597970978',
    '❌': '5985346521103604145',
    '🔴': '5872829476143894491',
    '⚠️': '5881702736843511327',
    '⚫️': '5994324703559290598',
    '⚫': '5994324703559290598',
    '⏸️': '6017174676898321263',
    '⏸': '6017174676898321263',
    '⏳': '5778605968208170641',
    '📦': '5936130851635990622',
}

_PATTERN = re.compile(
    r'(<tg-emoji\b[^>]*>.*?</tg-emoji>)|('
    + '|'.join(re.escape(k) for k in sorted(CUSTOM_EMOJI_IDS.keys(), key=len, reverse=True))
    + r')'
)


def _replace_match(m: re.Match) -> str:
    if m.group(1):
        return m.group(1)
    emoji = m.group(2)
    emoji_id = CUSTOM_EMOJI_IDS.get(emoji)
    if emoji_id:
        return f'<tg-emoji emoji-id="{emoji_id}">{emoji}</tg-emoji>'
    return emoji


def tg_emoji(char: str) -> str:
    """Wrap a single emoji character into a <tg-emoji> tag if a custom ID is configured."""
    emoji_id = CUSTOM_EMOJI_IDS.get(char)
    if emoji_id:
        return f'<tg-emoji emoji-id="{emoji_id}">{char}</tg-emoji>'
    return char


def format_custom_emojis(text: str) -> str:
    """Replace configured emoji characters in an HTML string with <tg-emoji> tags.

    Idempotent: skips emojis that are already wrapped in <tg-emoji>...</tg-emoji>.
    """
    if not text:
        return text
    return _PATTERN.sub(_replace_match, text)
