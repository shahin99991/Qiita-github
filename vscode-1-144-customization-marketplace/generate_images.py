#!/usr/bin/env python3
"""
VS Code 1.144（Browse マーケットプレイス / Copilot connectors）記事用の解説イメージを Gemini API で生成する。
既定モデルは Nano Banana 2.1（gemini-nano-banana-2.1 / Interactions API）。失敗したら Nano Banana Pro（gemini-3-pro-image）で再試行する。
Usage:
  python vscode-1-144-customization-marketplace/generate_images.py          # 全部生成
  python vscode-1-144-customization-marketplace/generate_images.py tldr     # 指定キーを含むものだけ生成
環境変数 IMAGE_MODEL でモデルを上書きできる。
"""
import base64
import io
import os
import sys
import time
from pathlib import Path

MODEL = os.environ.get("IMAGE_MODEL", "gemini-nano-banana-2.1")
FALLBACK_MODEL = "gemini-3-pro-image"
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
- 文字は太めで読みやすい日本語フォント。誤字・文字化けがないよう、指定した日本語と英数字をそのまま正確に描画する
- 配色は VS Code ブルー（#007ACC 系）と GitHub Copilot パープル（#8957E5 系）、アクセントにエメラルドグリーン（#2EA44F 系）とオレンジ（#F7630C 系）
- 親しみやすく、でもプロフェッショナルな技術ブログ向けの雰囲気。指定していない余計な文字やロゴは入れない
"""

PROMPTS = {
    "img-00-tldr-overview": """日本語の技術ブログ（Qiita）用の TL;DR 解説バナー画像を作成してください。

【テーマ】
「VS Code 1.144 のカスタマイズ：Browse で探して、Connect で つなぐ」

【画像内に描画する日本語テキスト（このとおり正確に）】
- 一番上の大きな見出し: 「探す → つなぐ → 整える → 配る」
- 4つのボックスを左から右へ矢印でつなぐ:
  1つ目の見出し: 「Browse」  内の文字: 「GitHub Feed とマーケットプレイスを横断検索」
  2つ目の見出し: 「Copilot connectors」  内の文字: 「Slack / Notion / Sentry などを MCP 設定なしで接続」  小さなバッジ: 「Preview」
  3つ目の見出し: 「エージェント編集」  内の文字: 「model / tools / skills を補完と検証でサポート」
  4つ目の見出し: 「共有リンク」  内の文字: 「vscode:// リンクと /plugin /mcp /skills」
- 一番下の帯: 「前提: VS Code 1.144 ／ Copilot ハーネス ／ Business・Enterprise は管理者の許可が必要」

【レイアウト】
左から右へ4ステップの横フロー。2つ目のボックスだけ強調色（Copilot パープル）の枠にする。各ボックスの上に小さなアイコン（虫眼鏡、プラグ、鉛筆、リンク）を添える。ロゴや余計な文字は入れない。
""" + STYLE,

    "img-01-browse-map": """日本語の技術ブログ用に、VS Code の Customizations の新しいホーム「Browse」の全体像を示す図を作成してください。

【画像内に描画する日本語テキスト（このとおり正確に）】
- 一番上の大きな見出し: 「Browse は“探す入口”をひとつにまとめたもの」
- 左側に縦に並ぶ3つの「ソース」ボックス:
  「GitHub Feed」  小さな文字: 「公開フィード（Local セッションでは使えない）」
  「プラグインマーケットプレイス」  小さな文字: 「自分や組織が登録したもの」
  「Copilot Connectors」  小さな文字: 「Connect で接続」
- 中央の大きなボックス: 「Browse」  内側の小さな文字: 「検索 ＋ 種類フィルター」
- 右側に並ぶ小さなタグ: 「@type:skill」「@type:mcp」「@type:canvas」
- 右端の矢印の先のボックス: 「Install ／ Connect」
- 一番下の帯: 「入れる前に、公開元・同梱物・必要な設定を確認する」

【レイアウト】
左の3ソースから中央の Browse へ矢印、Browse から右のフィルタータグ、最後に Install / Connect へ。Copilot Connectors のボックスだけ強調色（Copilot パープル）の枠にし、「Preview」の小さなバッジを付ける。ロゴは入れない。
""" + STYLE,

    "img-02-connector-vs-mcp": """日本語の技術ブログ用に、従来の MCP サーバー設定と Copilot connectors の手間の違いを示す左右比較図を作成してください。

【画像内に描画する日本語テキスト（このとおり正確に）】
- 一番上の大きな見出し: 「MCP を自分で設定する vs Connect を押す」
- 左パネル見出し: 「これまで」
  左パネルの手順（縦に番号付き）: 「1. MCP サーバーを探す」「2. mcp.json に書く」「3. 認証を設定する」「4. クライアントごとに繰り返す」
- 右パネル見出し: 「Copilot connectors」
  右パネル見出しの直下に、番号を付けない小さな補足を1行だけ: 「GitHub が管理・同じアカウントで使い回せる」
  右パネルの手順（縦に番号付き。行は 1・2・3 のちょうど3行だけ。各番号は1回ずつしか使わない。4行目以降や補足行を追加しない）: 「1. Browse で Connect」「2. ブラウザで許可」「3. 接続済みになる」
- 真ん中に「VS」の丸いバッジ
- 一番下の帯: 「ただし Preview ／ Copilot ハーネスのみ ／ 組織ポリシーの対象」

【レイアウト】
左右2分割。左は手順が長く、ごちゃごちゃした設定ファイルのイメージ（ファイルのアイコン、歯車）。右は手順が短く、ボタンを押すだけのすっきりしたイメージ。右パネルだけ強調色（エメラルドグリーン）の枠にする。ロゴや余計な文字は入れない。
""" + STYLE,

    "img-03-connect-once": """日本語の技術ブログ用に、Copilot connectors を一度つなぐと複数のクライアントで使えることを示すハブ図を作成してください。

【画像内に描画する日本語テキスト（このとおり正確に）】
- 一番上の大きな見出し: 「一度つなげば、あちこちで使える」
- 中央の大きな角丸ボックス: 「Copilot connector」  内側の小さな文字: 「GitHub が接続を管理」
- 中央を囲む5つのボックス（双方向の矢印で中央とつなぐ）:
  「VS Code」「Copilot CLI」「Copilot アプリ」「Copilot cloud」「GitHub Mobile」
- 中央の上に小さなラベル: 「Slack / Notion / Sentry / Postman / Work IQ ほか 26 サービス」
- 右下の注意書きボックス（オレンジの枠）: 「GitHub Actions 上のセッション（Issue を Copilot に割り当てる場合など）は未対応」
- 一番下の帯: 「同じ GitHub アカウントでサインインしていることが条件」

【レイアウト】
中央にハブ、周りに5つのクライアントを円形に配置。ボックス内の文字は指定したものだけにし、ロゴは入れない。
""" + STYLE,

    "img-04-share-links": """日本語の技術ブログ用に、vscode:// の共有リンクで何ができるかを示す3列の図を作成してください。

【画像内に描画する日本語テキスト（このとおり正確に）】
- 一番上の大きな見出し: 「README に貼れる3種類のリンク」
- 左の列の見出し: 「マーケットプレイスを追加」
  左の列のコード風の文字: 「vscode://chat-plugin/add-marketplace?ref=owner/repo」
- 中央の列の見出し: 「プラグインをインストール」
  中央の列のコード風の文字: 「vscode://chat-plugin/install?source=owner/repo&plugin=plugin-name」
- 右の列の見出し: 「Customizations のページを開く」
  右の列のコード風の文字: 「vscode://chat-customizations/open?page=plugins&search=github」
- 3つの列の下に共通の帯: 「実行前に VS Code が確認ダイアログを出す」
- 一番下の小さな帯: 「Insiders は vscode-insiders:// に置き換える」

【レイアウト】
3列のカード。各カードの上に小さなアイコン（追加、ダウンロード、ウィンドウ）。コード風の文字は等幅フォントで、長い場合は折り返してよい。ロゴは入れない。
""" + STYLE,

    "img-05-trust-checklist": """日本語の技術ブログ用に、マーケットプレイスのプラグインやコネクターを入れる前の確認事項をチェックリストで示す図を作成してください。

【画像内に描画する日本語テキスト（このとおり正確に）】
- 一番上の大きな見出し: 「入れる前の4つのチェック」
- 2×2 のカード:
  左上のカード見出し: 「公開元」  本文: 「Publisher と Source を確認」
  右上のカード見出し: 「同梱物」  本文: 「hooks や MCP サーバーはあなたの PC でコードを実行しうる」
  左下のカード見出し: 「権限」  本文: 「コネクターは許可画面の内容を読んでから承認」
  右下のカード見出し: 「ポリシー」  本文: 「Business / Enterprise は管理者の設定が優先」
- 一番下の帯: 「入れたら、新しいセッションで小さなタスクを試して確認」

【レイアウト】
2×2 のカードグリッド。各カードに小さなアイコン（人物バッジ、箱、鍵、盾）とチェックマークを添える。下に注意を促すオレンジ系の帯。ロゴは入れない。
""" + STYLE,
}


def _generate_interactions(model: str, prompt: str) -> bytes | None:
    client = genai.Client(api_key=API_KEY)
    interaction = client.interactions.create(
        model=model,
        input=prompt,
        response_format={"type": "image", "mime_type": "image/jpeg", "aspect_ratio": "16:9", "image_size": "2K"},
    )
    image = interaction.output_image
    if image is None:
        return None
    # 2.1 は JPEG しか返せないので、記事の参照パスに合わせて PNG へ変換する
    from PIL import Image

    buf = io.BytesIO()
    Image.open(io.BytesIO(base64.b64decode(image.data))).save(buf, format="PNG")
    return buf.getvalue()


def _generate_legacy(model: str, prompt: str) -> bytes | None:
    client = genai.Client(api_key=API_KEY)
    resp = client.models.generate_content(
        model=model,
        contents=[prompt],
        config=types.GenerateContentConfig(response_modalities=["IMAGE"]),
    )
    for part in resp.candidates[0].content.parts:
        if part.inline_data is not None:
            return part.inline_data.data
    return None


def generate(name: str, prompt: str, retries: int = 2) -> bool:
    attempts = [(MODEL, _generate_interactions)] * retries + [(FALLBACK_MODEL, _generate_legacy)]
    for i, (model, fn) in enumerate(attempts, 1):
        print(f"🎨 生成中: {name} ({model}) try {i}")
        try:
            data = fn(model, prompt)
            if data:
                OUT_DIR.mkdir(parents=True, exist_ok=True)
                out = OUT_DIR / f"{name}.png"
                out.write_bytes(data)
                print(f"✅ 保存完了: {out}")
                return True
            print("⚠️ 画像が返ってきませんでした")
        except Exception as e:  # noqa: BLE001
            print(f"⚠️ エラー: {e}")
        time.sleep(3)
    print(f"❌ 失敗: {name}")
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
