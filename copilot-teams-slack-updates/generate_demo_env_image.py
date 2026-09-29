#!/usr/bin/env python3
"""
デモ環境（リポジトリ構成＋バグ仕込み状況）の解説画像を
Gemini API（Nano Banana Pro / gemini-3-pro-image）で生成する。
Usage: python copilot-teams-slack-updates/generate_demo_env_image.py
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

OUTPUT_PATH = Path(__file__).parent / "Images" / "img-demo-env-overview.png"

PROMPT = """日本語の技術プレゼン用の解説画像を作成してください。16:9 の横長、テキストが主役のインフォグラフィックです。

【テーマ】
「Gh-CUG #06 登壇デモ環境：GitHub 通知ボット（バグ4つ＋要件2つ仕込み済み）」

【画像内に描画する日本語テキスト（このとおり正確に）】
- 一番上の大きな見出し: 「デモ環境：GitHub 通知ボット」
- 大見出しの下のサブ見出し: 「GitHub のイベントを Slack/Teams に通知するボット（バグ4つ＋要件2つを仕込み済み）」

- 左側のパネル見出し: 「リポジトリ構成」
- 左側のパネル内のテキスト（ファイルツリー）:
  「src/notifier.py」「tests/」「docs/」「.github/workflows/」

- 右側のパネル見出し: 「仕込んであるバグ・要件」
- 右側のパネル内の箇条書き（6つ）:
  「① 404 で例外を投げる」
  「② created_at=None で落ちる」
  「③ 未対応イベントで KeyError」
  「④ Webhook レート制限なし」
  「⑤ ReleaseEvent 非対応（要件）」
  「⑥ レビュアーメンション機能なし（要件）」

- 右下に小さく: 「CI: pytest → 2 failed, 1 passed」

【レイアウト】
左右2パネル構成。左はリポジトリのファイルツリーをイメージしたアイコン付きリスト、右はバグ・要件の箇条書きリスト。パネル同士は中央で繋がっている。

【スタイル】
- フラットでモダンなインフォグラフィック、背景は白またはごく薄いグレー
- 左パネルは薄青、右パネルは薄オレンジ系で色分け
- 文字は読みやすい太めの日本語フォントで、誤字・文字化けのないように正確に描画する
- 親しみやすく、でもプロフェッショナルな技術プレゼン向け
"""

def main():
    client = genai.Client(api_key=API_KEY)
    print("🎨 デモ環境解説イメージを生成中（gemini-3-pro-image / Nano Banana Pro）...")

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
