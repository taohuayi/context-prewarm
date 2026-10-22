#!/usr/bin/env python3
"""Small dependency-free check for required Agent Skills frontmatter."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "gpt-quota-prewarm" / "SKILL.md"


def validate(path: Path = SKILL) -> None:
    text = path.read_text(encoding="utf-8")
    parts = text.split("---", 2)
    if len(parts) != 3 or parts[0] != "":
        raise ValueError("SKILL.md must start with YAML frontmatter")
    front = parts[1]
    fields = {}
    for line in front.splitlines():
        if line.strip() and not line.lstrip().startswith("#"):
            if ":" not in line:
                raise ValueError("Invalid scalar frontmatter line: " + line)
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip()
    name = fields.get("name", "")
    description = fields.get("description", "")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        raise ValueError("Invalid skill name")
    if name != path.parent.name or len(name) > 64:
        raise ValueError("Skill name must match parent directory and be <= 64 chars")
    if not 1 <= len(description) <= 1024:
        raise ValueError("description must be 1..1024 characters")
    if not parts[2].strip():
        raise ValueError("Skill body is empty")


if __name__ == "__main__":
    try:
        validate()
    except (OSError, ValueError) as exc:
        print(f"SKILL INVALID: {exc}", file=sys.stderr)
        raise SystemExit(1)
    print("SKILL OK: gpt-quota-prewarm")
