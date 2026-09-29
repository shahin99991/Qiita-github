#!/usr/bin/env python3
"""
「Shared agentic work（共同エージェント作業）」の4ポイントを解説する画像を
Gemini API（Nano Banana Pro / gemini-3-pro-image）で生成する。
対象ポイント:
  1. 会話の全員がエージェントの調査・作業を見られる
  2. 誰かが質問・コンテキスト追加・舵取りができる
  3. 書き込み権限を持つ人は実際の変更作業まで指示できる
  4. 作業はセキュアなクラウドサンドボックスで非同期に進行する
Usage: python copilot-teams-slack-updates/generate_shared_agentic_image.py
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

OUTPUT_PATH = Path(__file__).parent / "Images" / "img-shared-agentic-work.png"

PROMPT = """日本語の技術プレゼン用の解説バナー画像を作成してください。16:9 の横長、テキストが主役のインフォグラフィックです。

【テーマ】
「GitHub Copilot in Microsoft Teams は、チーム全員でエージェントと共同作業できる」

【画像内に描画する日本語テキスト（このとおり正確に）】
- 一番上の大きな見出し: 「Shared Agentic Work：みんなでエージェントと仕事する」

- 左上のカードの見出し: 「① 全員が見られる」
- 左上のカードの本文: 「会話の参加者全員がエージェントの調査・作業をリアルタイムで見られる」

- 右上のカードの見出し: 「② 誰でも舵取りできる」
- 右上のカードの本文: 「質問を足す・コンテキストを追加・作業の方向修正を誰でもできる」

- 左下のカードの見出し: 「③ 権限で変わる操作」
- 左下のカードの本文: 「書き込み権限を持つ人は、実際のコード変更まで指示できる」

- 右下のカードの見出し: 「④ 裏側は安全」
- 右下のカードの本文: 「作業はセキュアなクラウドサンドボックスで非同期に進行」

【レイアウト】
2×2 のカードグリッド（2行2列）。中央に GitHub Copilot をイメージしたかわいいロボットのキャラクターを配置し、4枚のカードがロボットを囲むように配置する。カード同士は細い線でロボットと繋がっているように見せる。

【スタイル】
- フラットでモダンなインフォグラフィック、背景は白またはごく薄いグレー
- 各カードは淡い色で色分け（① 薄紫、② 薄青、③ 薄緑、④ 薄オレンジ）
- 文字は読みやすい太めの日本語フォントで、誤字・文字化けのないように正確に描画する
- 親しみやすく、でもプロフェッショナルな技術プレゼン向け
"""

def main():
    client = genai.Client(api_key=API_KEY)
    print("🎨 Shared Agentic Work 解説イメージを生成中（gemini-3-pro-image / Nano Banana Pro）...")

    resp = client.models.generate_content(
        model="gemini-3-pro-image",
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
