#!/usr/bin/env python3
"""
VS Code Canvases 記事用の解説イメージを Gemini API（Nano Banana Pro / gemini-3-pro-image）で生成する。
Usage:
  python VSCode-canvas-article/generate_images.py          # 全部生成
  python VSCode-canvas-article/generate_images.py tldr     # 指定キーだけ生成
"""
import os
import sys
from pathlib import Path

MODEL = "gemini-3-pro-image"
OUT_DIR = Path(__file__).parent / "images"


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

STYLE = """
【共通スタイル】
- 16:9 の横長、フラットでモダンなインフォグラフィック。背景は白かごく薄いグレー
- 文字は太めで読みやすい日本語フォント。誤字・文字化けがないよう、指定した日本語をそのまま正確に描画する
- 配色は VS Code ブルー（#007ACC 系）と GitHub Copilot パープル（#8957E5 系）、アクセントにエメラルドグリーン（#2EA44F 系）
- 親しみやすく、でもプロフェッショナルな技術ブログ向けの雰囲気。指定していない余計な文字は入れない
"""

PROMPTS = {
    "img-00-tldr-overview": """日本語の技術ブログ（Qiita）用の TL;DR 解説バナー画像を作成してください。

【テーマ】
「VS Code 1.142 の Canvases（プレビュー）で、チャットの横にエージェントと一緒に触れる画面が開く」

【画像内に描画する日本語テキスト（このとおり正確に）】
- 一番上の大きな見出し: 「VS Code に Canvas が来た！」
- 小さめの副題: 「チャットの横で、エージェントと同じ画面を一緒に触る」
- 左ボックス見出し: 「1. 設定を ON」  内の文字: 「chat.canvases.enabled」
- 中央ボックス見出し: 「2. /create-canvas」  内の文字: 「作りたい画面を日本語で説明」
- 右ボックス見出し: 「3. 一緒に操作」  内の文字: 「人はクリックやドラッグ」「エージェントは操作を呼び出す」
- 一番下の小さな帯: 「Preview / デスクトップ版 / Copilot ハーネスのローカルセッション」

【レイアウト】
左 → 中央 → 右の3ボックスを太い矢印で繋ぐ。右ボックスにはカンバンボード風の小さなイラストと、人とロボットが同じボードを触っているアイコンを入れる。
""" + STYLE,

    "img-04-chat-vs-canvas": """日本語の技術ブログ用の比較図を作成してください。

【テーマ】
「チャットだけの協業」と「Canvas ありの協業」の違い

【画像内に描画する日本語テキスト（このとおり正確に）】
- 一番上の大きな見出し: 「チャットだけ vs Canvas あり」
- 左パネル見出し: 「チャットだけ」
  左パネル内の吹き出し風テキスト: 「タスクを3つ追加して」「さっきの2番目を完了にして」「今の状況まとめて」
  左パネル下の注釈: 「状態がログに埋もれて、全部プロンプト経由」
- 右パネル見出し: 「Canvas あり」
  右パネル内: チャット欄の右隣にカンバンボード（「ToDo」「Doing」「Done」の3列にカード数枚）
  右パネル下の注釈: 「同じ画面を、人もエージェントも直接触れる」

【レイアウト】
左右2分割。左は吹き出しが縦にたくさん積み重なって読みづらい様子、右は整理されたボードと小さなチャット欄が並ぶ様子。真ん中に「VS」の丸いバッジ。
""" + STYLE,

    "img-05-requirements": """日本語の技術ブログ用の「使える条件」早見表の画像を作成してください。

【テーマ】
VS Code の Canvases が使える環境と、まだ使えない環境

【画像内に描画する日本語テキスト（このとおり正確に）】
- 一番上の大きな見出し: 「Canvases が使える環境は？」
- 左カラム見出し（緑のチェックアイコン付き）: 「使える」
  項目: 「VS Code 1.142 以降」「デスクトップ版」「Copilot ハーネス」「ローカルセッション」
- 右カラム見出し（赤の×アイコン付き）: 「まだ使えない」
  項目: 「Claude / Codex ハーネス」「Local（拡張機能ホスト）セッション」「リモートセッション」「ブラウザ / Web クライアント」
- 一番下の帯: 「まず chat.canvases.enabled を ON にして、新しいセッションを開始」

【レイアウト】
2カラムのカード。左は緑系、右は赤系の淡い背景。各項目は大きめの文字で一行ずつ。
""" + STYLE,

    "img-06-architecture": """日本語の技術ブログ用の仕組み図を作成してください。

【テーマ】
Canvas 拡張機能を介して、人とエージェントが同じ状態を操作する仕組み

【画像内に描画する日本語テキスト（このとおり正確に）】
- 一番上の大きな見出し: 「Canvas の仕組み」
- 左のアイコン（人物）のラベル: 「あなた」  矢印のラベル: 「クリック・ドラッグ」
- 右のアイコン（ロボット）のラベル: 「Copilot エージェント」  矢印のラベル: 「アクションを呼び出す」
- 中央の大きな箱の見出し: 「Canvas 拡張機能」
  箱の中の3つの小さなブロック: 「画面（UI）」「共有ステート」「エージェント向けアクション」
  アクションの例を小さな文字で: 「get_board」「add_card」「move_card」
- 箱の下の注釈2行: 「プロジェクト用: .github/extensions」「個人用: ~/.copilot/extensions」

【レイアウト】
中央に Canvas 拡張機能の大きな箱。左から人、右からロボットが双方向の矢印で箱の中の「共有ステート」を指す。左右対称で整理された構図。
""" + STYLE,
}


def generate(name: str, prompt: str) -> bool:
    client = genai.Client(api_key=API_KEY)
    print(f"🎨 生成中: {name} ({MODEL})")
    resp = client.models.generate_content(
        model=MODEL,
        contents=[prompt],
        config=types.GenerateContentConfig(response_modalities=["IMAGE"]),
    )
    for part in resp.candidates[0].content.parts:
        if part.inline_data is not None:
            OUT_DIR.mkdir(parents=True, exist_ok=True)
            out = OUT_DIR / f"{name}.png"
            out.write_bytes(part.inline_data.data)
            print(f"✅ 保存完了: {out}")
            return True
    print(f"⚠️ 画像が返ってきませんでした: {name}")
    return False


def main():
    keys = sys.argv[1:]
    targets = {k: v for k, v in PROMPTS.items() if not keys or any(a in k for a in keys)}
    if not targets:
        print("該当する画像がありません:", list(PROMPTS))
        sys.exit(1)
    ok = all([generate(n, p) for n, p in targets.items()])
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
