#!/usr/bin/env python3
"""
TL;DR セクション用の解説イメージを Gemini API（Nano Banana / gemini-2.5-flash-image）で生成する。
Usage: python copilot-teams-slack-updates/generate_tldr_image.py
"""
import os
import sys
from pathlib import Path

def _load_env():
    for env_path in [Path(__file__).parents[1] / ".env", Path(".env")]:
        if env_path.exists():
            with open(env_path, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, _, v = line.partition("=")
                        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
            return

_load_env()

API_KEY = os.environ.get("GEMINI_API_KEY", "")
if not API_KEY:
    print("❌ GEMINI_API_KEY が見つかりません")
    sys.exit(1)

from google import genai
from google.genai import types

OUTPUT_PATH = Path(__file__).parent / "Images" / "img-00-tldr-overview.png"

PROMPT = """Create a clean, modern tech blog illustration (wide 16:9 banner) explaining this workflow concept:

"A Microsoft Teams chat conversation where a user pastes an error message and mentions @GitHub. A friendly robot AI assistant (GitHub Copilot agent) reads the chat context (error screenshot, forwarded messages, thread history), then automatically produces GitHub artifacts: a fixed Pull Request and an Issue."

Visual elements to include (left to right flow):
1. LEFT: A chat window mockup (Microsoft Teams style, purple accent) showing a conversation thread with an error traceback pasted in it, and a mention "@GitHub"
2. CENTER: A cute friendly robot character (AI agent) with "reading" / analyzing the chat — show small icons floating around it: an image icon, a forward/share arrow icon, a thread/history icon, a brain/model-switch icon
3. RIGHT: GitHub-style cards (dark theme, GitHub dark navy background) showing a "Pull Request" card with a green checkmark and an "Issue" card, connected by arrows from the robot

Style requirements:
- Flat modern illustration, clean and minimal
- Color palette: dark navy/black background with purple (Teams), emerald green (GitHub), and white accents
- Japanese tech blog aesthetic, professional but friendly
- NO text-heavy elements; minimal short labels only (e.g. "Teams", "@GitHub", "PR", "Issue")
- Arrows showing the flow: chat → AI agent reads context → GitHub artifacts
"""

def main():
    client = genai.Client(api_key=API_KEY)
    print("🎨 TL;DR 解説イメージを生成中...")

    resp = client.models.generate_content(
        model="gemini-2.5-flash-image",
        contents=[PROMPT],
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE"],
        ),
    )

    saved = False
    for part in resp.candidates[0].content.parts:
        if part.inline_data is not None:
            OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
            OUTPUT_PATH.write_bytes(part.inline_data.data)
            print(f"✅ 保存完了: {OUTPUT_PATH}")
            saved = True
            break

    if not saved:
        print("❌ 画像が生成されませんでした")
        print(resp)
        sys.exit(1)

if __name__ == "__main__":
    main()
