#!/usr/bin/env python3
"""
vscode-1-144-cloud-sessions/images 内の実機スクショを Gemini API で解析し、
記事のどの demo-XX 枠に対応するかを JSON で出力する（img-* の生成画像は対象外）。
Usage: python vscode-1-144-cloud-sessions/analyze_images.py
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

IMAGES_DIR = Path(__file__).parent / "images"
OUTPUT_JSON = Path(__file__).parent / "image-analysis.json"
MODELS = [os.environ.get("ANALYSIS_MODEL", "gemini-3-pro"), "gemini-2.5-pro", "gemini-2.5-flash"]

PROMPT = """このスクリーンショットは「VS Code 1.144 の Cloud セッションと Cloud Automations」の検証中に撮影されたものです。
以下を JSON のみで返してください（前後に説明文や ``` を付けないこと）:

{
  "summary": "画像に何が写っているかの1-2文の要約（日本語）",
  "visible_text": "画面内の重要なテキスト（設定名・ボタン名・プロンプト・応答の要点・ステータス表示など。見えたまま正確に）",
  "ui_state": "画面の状態（例: 設定画面で該当設定なし / Cloud環境ドロップダウン / 作成フォーム / 履歴 completed / Issueコメント表示 など）",
  "demo_slot": "最も合う枠を1つ選ぶ: demo-01-settings / demo-02-env-picker-cloud / demo-03-cloud-session-running / demo-04-lid-closed-github-com / demo-05-cli-sessions-remote / demo-06-automations-view / demo-07-create-cloud-automation / demo-08-run-history / demo-09-event-trigger-issue / demo-10-result-github / demo-11-open-on-github / none",
  "demo_slot_reason": "その枠を選んだ理由（日本語）",
  "usable_for_article": "記事にそのまま使えるか。true/false",
  "issues": "機密情報（トークン・メール・内部URL）、画質、切れ、無関係な情報の写り込みなどの懸念。なければ null",
  "article_notes": "記事の本文（結果・所要時間・ハマりどころ）に反映できる事実。なければ null"
}"""


def analyze(client, data: bytes) -> dict:
    last = None
    for model in MODELS:
        try:
            resp = client.models.generate_content(
                model=model,
                contents=[types.Part.from_bytes(data=data, mime_type="image/png"), PROMPT],
            )
            text = resp.text.strip()
            if text.startswith("```"):
                text = text.split("```")[1].removeprefix("json").strip()
            result = json.loads(text)
            result["model"] = model
            return result
        except Exception as e:  # noqa: BLE001
            last = e
    raise RuntimeError(last)


def main():
    client = genai.Client(api_key=API_KEY)
    images = sorted(p for p in IMAGES_DIR.glob("*.png") if not p.name.startswith("img-"))
    print(f"🔍 {len(images)} 枚を解析します")
    results = []
    for i, path in enumerate(images, 1):
        print(f"  [{i}/{len(images)}] {path.name}")
        try:
            data = analyze(client, path.read_bytes())
            data["file"] = path.name
        except Exception as e:  # noqa: BLE001
            print(f"    ⚠️ 失敗: {e}")
            data = {"file": path.name, "error": str(e)}
        results.append(data)
        time.sleep(1)
    OUTPUT_JSON.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ 出力: {OUTPUT_JSON}")


if __name__ == "__main__":
    main()
