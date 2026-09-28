#!/usr/bin/env python3
"""
copilot-teams-slack-updates/Images 内のスクリーンショットを Gemini API で解析し、
画像ごとの内容・写っているUI要素・記事のどのデモ手順に対応しそうかを JSON で出力する。
Usage: python copilot-teams-slack-updates/analyze_images.py
"""
import json
import os
import sys
import time
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

IMAGES_DIR = Path(__file__).parent / "Images"
OUTPUT_JSON = Path(__file__).parent / "image-analysis.json"

PROMPT = """このスクリーンショットは「GitHub Copilot in Microsoft Teams / Slack」の機能検証デモで撮影されたものです。
以下を JSON 形式のみで返してください（前後に説明文や ``` を付けないこと）:

{
  "summary": "画像に何が写っているかの1-2文の要約（日本語）",
  "ui_elements": ["写っている主要なUI要素のリスト（日本語）"],
  "visible_text": "画面内の重要なテキストの抜粋（メンション文・Copilotの応答の要点など。長文は要約）",
  "features_shown": ["この画像から読み取れる Copilot の機能（例: メンション開始, 画像解析, 転送メッセージ, スレッド履歴, モデル切り替え, Issue作成, リポジトリ設定, その他）"],
  "repo_visible": "画面に写っているリポジトリ名（例: YJK-Inc/Test-Repo）。見えなければ null",
  "model_visible": "画面に写っているモデル名（例: GPT-5, Claude, MAI 等）。見えなければ null",
  "demo_step_candidate": "この画像が対応しそうなデモ手順（img-01 メンション開始 / img-02 画像解析 / img-03 転送メッセージ / img-04 スレッド履歴 / img-05 モデル切り替え / img-06 Issue作成リンク / その他）",
  "notable": "記事で触れると面白い点・デモ上のハプニング・設定ミスからの復帰などがあれば記載。なければ null"
}"""

def main():
    client = genai.Client(api_key=API_KEY)
    images = sorted(IMAGES_DIR.glob("*.png"))
    print(f"🔍 {len(images)} 枚の画像を解析します...")

    results = []
    for i, img_path in enumerate(images, start=1):
        print(f"  [{i}/{len(images)}] {img_path.name}")
        try:
            resp = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    types.Part.from_bytes(
                        data=img_path.read_bytes(), mime_type="image/png"
                    ),
                    PROMPT,
                ],
            )
            text = resp.text.strip()
            if text.startswith("```"):
                text = text.split("```")[1]
                if text.startswith("json"):
                    text = text[4:]
            data = json.loads(text)
            data["file"] = img_path.name
            results.append(data)
        except Exception as e:
            print(f"    ⚠️ 解析失敗: {e}")
            results.append({"file": img_path.name, "error": str(e)})
        time.sleep(1)  # レート制限対策

    OUTPUT_JSON.write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"\n✅ 出力完了: {OUTPUT_JSON}")

if __name__ == "__main__":
    main()
