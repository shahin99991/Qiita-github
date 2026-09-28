#!/usr/bin/env python3
"""
TL;DR セクション用の解説イメージを Gemini API（Nano Banana Pro / gemini-3-pro-image）で生成する。
最新モデル一覧: https://ai.google.dev/gemini-api/docs/models （2026-09-24 時点で gemini-3-pro-image がテキスト描画最强）
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

PROMPT = """日本語の技術ブログ（Qiita）用の TL;DR 解説バナー画像を作成してください。16:9 の横長、テキストが主役のインフォグラフィックです。

【テーマ】
「Microsoft Teams の会話コンテキストを GitHub Copilot が読んで、PR/Issue を自動で作る」

【画像内に描画する日本語テキスト（このとおり正確に）】
- 一番上の大きな見出し: 「Teams の会話を読んで、PR/Issue まで作る」
- 左ボックス見出し: 「Teams の会話」
- 左ボックス内の小さな箇条書き: 「画像」「転送メッセージ」「スレッド履歴」
- 中央ボックス見出し: 「GitHub Copilot」
- 中央ボックス内の小さな箇条書き: 「コンテキスト読解」「モデル切り替え」
- 右ボックス見出し: 「GitHub に自動作成」
- 右ボックス内の小さな箇条書き: 「Pull Request」「Issue」

【レイアウト】
左 → 中央 → 右の3ボックス構成。ボックス同士は太い矢印（→）で繋ぐ。
- 左ボックス: Microsoft Teams をイメージした紫（#6264A7 系）ベース、チャットの吹き出しアイコン付き
- 中央ボックス: GitHub Copilot をイメージしたダークネイビー（#0D1117 系）ベース、かわいいロボットのアイコン付き
- 右ボックス: GitHub をイメージしたダークグレー＋エメラルドグリーン（#2EA44F 系）のアクセント、PR/Issue のカードアイコン付き

【スタイル】
- フラットでモダンなインフォグラフィック、背景は白またはごく薄いグレー
- 文字は読みやすい太めの日本語フォントで、誤字・文字化けのないように正確に描画する
- 全体の雰囲気は親しみやすく、でもプロフェッショナルな技術ブログ向け
"""

def main():
    client = genai.Client(api_key=API_KEY)
    print("🎨 TL;DR 解説イメージを生成中（gemini-3-pro-image / Nano Banana Pro）...")

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
