#!/usr/bin/env python3
"""
VS Code 1.144（Cloud セッション / Cloud Automations）記事用の解説イメージを Gemini API で生成する。
既定モデルは Nano Banana 2.1（gemini-nano-banana-2.1 / Interactions API）。失敗したら Nano Banana Pro（gemini-3-pro-image）で再試行する。
Usage:
  python vscode-1-144-cloud-sessions/generate_images.py          # 全部生成
  python vscode-1-144-cloud-sessions/generate_images.py tldr     # 指定キーを含むものだけ生成
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
「VS Code 1.144 で、PC を閉じてもエージェントが働くようになった」

【画像内に描画する日本語テキスト（このとおり正確に）】
- 一番上の大きな見出し: 「PC を閉じても、エージェントは働く」
- 左ボックス見出し: 「Cloud セッション」  内の文字: 「GitHub のクラウドで実行」「別のクライアントから続きを操作」
- 右ボックス見出し: 「Cloud Automations」  内の文字: 「スケジュールや Issue / PR で自動起動」「Preview」
- 左右のボックスの下に横長の帯: 「前提: 有料 Copilot プラン ／ GitHub.com のリポジトリ ／ VS Code 1.144」
- 一番下の小さな帯: 「2026-10-28 リリース」

【レイアウト】
左右2つの大きなボックス。左はクラウドとノート PC（フタが閉じている）のアイコン、右は時計とカレンダーとイベント（Issue アイコン）のアイコン。ボックスの間に小さく「＋」。
""" + STYLE,

    "img-01-where-it-runs": """日本語の技術ブログ用に、エージェントが「どこで動くか」で「閉じても動く」の意味が変わることを示す3列の比較図を作成してください。

【画像内に描画する日本語テキスト（このとおり正確に）】
- 一番上の大きな見出し: 「『閉じても動く』は3種類ある」
- 左の列の見出し: 「ローカルの Agent Host」
  左の列の項目: 「ウィンドウを閉じても継続」「VS Code アプリは起動したまま」「PC は電源 ON のまま」
- 中央の列の見出し: 「自分のリモートマシン」
  中央の列の項目: 「SSH / Dev Tunnel / WSL / GitHub Environments」「手元の PC は閉じてOK」「リモート側のマシンは稼働が必要」
- 右の列の見出し: 「Cloud セッション」
  右の列の項目: 「GitHub のクラウドで実行」「どの PC も落としてOK」「手元の未コミット変更は渡らない」
- 一番下の帯: 「実行する場所が、止めてよいものを決める」

【レイアウト】
3列のカード。左はノート PC、中央はサーバーとノート PC を線でつないだ絵、右は雲（クラウド）のアイコン。アイコンの中に文字やロゴ（アルファベットなど）は入れない。右の列だけ強調色（エメラルドグリーン）の枠にする。
""" + STYLE,

    "img-02-session-continuity": """日本語の技術ブログ用に、1つの Cloud セッションを複数のクライアントから続けられることを示すハブ図を作成してください。

【画像内に描画する日本語テキスト（このとおり正確に）】
- 一番上の大きな見出し: 「同じセッションを、あちこちから続ける」
- 中央の大きな角丸ボックス: 「1つの Cloud セッション」  内側の小さな文字: 「GitHub のクラウドで実行中」
- 中央を囲む6つの小さなボックス（双方向の矢印で中央とつなぐ）:
  「VS Code」「Copilot CLI」「github.com」「GitHub Mobile」「Slack / Teams」「Copilot アプリ」
- Copilot CLI ボックスの横に小さく: 「/sessions → Remote」
- 一番下の帯: 「アカウントを揃えれば、会話を引き継げる」

【レイアウト】
中央にハブ、周りに6つのクライアントを円形に配置。VS Code と Copilot CLI と GitHub Mobile のボックスは少し大きくする。ボックス内の文字は指定したものだけにし、ロゴは入れない。
""" + STYLE,

    "img-03-session-vs-automation": """日本語の技術ブログ用に、Cloud セッションと Cloud Automation の違いを示す左右比較図を作成してください。

【画像内に描画する日本語テキスト（このとおり正確に）】
- 一番上の大きな見出し: 「Cloud セッション vs Cloud Automation」
- 左パネル見出し: 「Cloud セッション」
  左パネルの項目: 「あなたが始める」「対話しながら進める」「同じ会話を再開できる」
  左パネルの例: 「例: 調査を任せて、続きは CLI で」
- 右パネル見出し: 「Cloud Automation」
  右パネルの項目: 「トリガーで自動起動」「保存したプロンプトで毎回新しく実行」「Manual / 毎日 / 毎週 / Issue・PR」
  右パネルの例: 「例: 毎週のリポジトリ要約」
- 一番下の帯: 「セッションを作っても、スケジュールは作られない」

【レイアウト】
左右2分割。左は人とロボットが吹き出しで会話しているイラスト（吹き出しの中には文字を入れず、アイコンや点々だけにする）、右は時計とカレンダーとベルのアイコンが並ぶイラスト。真ん中に「VS」の丸いバッジ。
""" + STYLE,

    "img-04-automation-anatomy": """日本語の技術ブログ用に、Cloud Automation を構成する4つの要素を左から右へ流れる図で作成してください。

【画像内に描画する日本語テキスト（このとおり正確に）】
- 一番上の大きな見出し: 「Cloud Automation の中身」
- 4つのボックスを矢印でつなぐ:
  「1. トリガー」  小さな文字: 「Manual / Daily / Weekly / Issue / Pull Request」
  「2. プロンプト」  小さな文字: 「やることと出力を具体的に書く」
  「3. 許可ツール」  小さな文字: 「必要なものだけ選ぶ」
  「4. クラウドで実行」  小さな文字: 「PC が OFF でも動く」
- 4つのボックスの下に、実行履歴を表す帯: 「実行履歴: queued → running → completed / failed」
- 一番下の帯: 「結果は Agents ウィンドウの History から確認」

【レイアウト】
左から右へ4ステップの横フロー。3番目のボックス（許可ツール）は強調色（オレンジ）の枠にして鍵のアイコンを添える。
""" + STYLE,

    "img-05-guardrails": """日本語の技術ブログ用に、Cloud Automation を安全に使うための4つのガードレールをカードで示す図を作成してください。

【画像内に描画する日本語テキスト（このとおり正確に）】
- 一番上の大きな見出し: 「放っておく前に確認する4つのこと」
- 左上のカード見出し: 「対象リポジトリ」  本文: 「private / internal のみ」「public は対象外」
- 右上のカード見出し: 「許可ツール」  本文: 「タスクに必要なものだけ許可」
- 左下のカード見出し: 「イベントの送り主」  本文: 「既定では write 権限のない人のイベントを無視」
- 右下のカード見出し: 「コスト」  本文: 「AI クレジットの上限を設定」「1 回あたり / 日 / 週 / 月」
- 一番下の帯: 「実行ログはリポジトリを読める人に見える。秘密情報はプロンプトに書かない」

【レイアウト】
2×2 のカードグリッド。各カードに小さなアイコン（リポジトリ、鍵、人のシルエット、コイン）を添える。下に注意を促すオレンジ系の帯。
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
