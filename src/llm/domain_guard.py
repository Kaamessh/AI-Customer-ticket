from __future__ import annotations
from pathlib import Path
from typing import Iterable
import re

# Keywords that indicate a laptop-related technical query.
LAPTOP_KEYWORDS: tuple[str, ...] = (
    "laptop", "notebook", "macbook", "thinkpad", "ultrabook",
    "windows", "win10", "win11", "macos", "bios", "uefi",
    "battery", "charging", "charger", "power", "adapter",
    "screen", "display", "lcd", "oled", "brightness", "backlight",
    "keyboard", "key", "trackpad", "touchpad", "mouse", "bluetooth",
    "wifi", "wireless", "ethernet", "network", "driver", "drivers",
    "ssd", "hdd", "nvme", "ram", "memory", "gpu", "graphics",
    "intel", "amd", "nvidia", "fan", "overheating", "thermal",
    "usb", "hdmi", "thunderbolt", "type-c", "webcam", "microphone",
    "speakers", "audio", "firmware"
)

NON_LAPTOP_HINTS: tuple[str, ...] = (
    "phone", "iphone", "android", "tv", "television", "server",
    "router", "tablet", "watch", "camera", "printer only", "console"
)

REFUSAL_MESSAGE = "Sorry, I can assist only with laptop-related technical issues."


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def is_laptop_query(text: str, *, keywords: Iterable[str] | None = None) -> bool:
    """Return True if text appears laptop-related.

    Uses simple keyword heuristics; safe and fast for request gating.
    """
    t = normalize(text)
    kw = set(k.lower() for k in (keywords or LAPTOP_KEYWORDS))
    if any(h in t for h in NON_LAPTOP_HINTS):
        # If it obviously mentions non-laptop device, gate out.
        # Still allow if it also mentions 'laptop' explicitly.
        return "laptop" in t or "notebook" in t or "macbook" in t
    return any(k in t for k in kw)


def guard_or_message(query: str) -> tuple[bool, str]:
    """Return (allowed, message).

    If not allowed, message is the exact refusal string required.
    """
    allowed = is_laptop_query(query)
    return allowed, ("" if allowed else REFUSAL_MESSAGE)
