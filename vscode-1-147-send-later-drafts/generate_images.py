#!/usr/bin/env python3
"""
VS Code 1.147（Send Later + Drafts）記事用の解説イメージを OpenAI の GPT Image 2.5 で生成する。
既定モデルは gpt-image-2.5-sunburst（編集精度重視）。速さ優先なら IMAGE_MODEL=gpt-image-2.5-flare。
Usage:
  python vscode-1-147-send-later-drafts/generate_images.py          # 全部生成
  python vscode-1-147-send-later-drafts/generate_images.py tldr     # 指定キーを含むものだけ生成
環境変数（.env でも可）:
  OPENAI_API_KEY   必須。api.openai.com の API キー（Organization Verification が必要な場合あり）
  IMAGE_MODEL      既定 gpt-image-2.5-sunburst
  IMAGE_SIZE       既定 1536x864（16:9。幅・高さとも16の倍数）
  IMAGE_QUALITY    既定 high（low / medium / high / xhigh / max / auto）
  OPENAI_BASE_URL  既定 https://api.openai.com/v1
"""
import base64
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

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

API_KEY = os.environ.get("OPENAI_API_KEY", "")
MODEL = os.environ.get("IMAGE_MODEL", "gpt-image-2.5-sunburst")
SIZE = os.environ.get("IMAGE_SIZE", "1536x864")
QUALITY = os.environ.get("IMAGE_QUALITY", "high")
BASE_URL = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")

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
「VS Code 1.147 で、エージェントへの依頼を『いま送らない』で管理できるようになった」

【画像内に描画する日本語テキスト（このとおり正確に）】
- 一番上の大きな見出し: 「あとで送る。いまは寝かせる。」
- 左ボックス見出し: 「Drafts（下書き）」  内の文字: 「未送信の依頼を複数ためておく」「ワークスペース・モデル・添付も保持」「再起動しても残る」
- 右ボックス見出し: 「Send Later（予約送信）」  内の文字: 「日時を指定して送る」「自然言語でも予約できる」「Experimental」
- 左右のボックスの下に横長の帯: 「前提: Agents ウィンドウ ／ This Computer のセッション ／ VS Code 1.147」
- 一番下の小さな帯: 「2026-11-18 リリース」

【レイアウト】
左右2つの大きなボックス。左は付箋が何枚か重なった下書きのアイコン、右は時計と紙飛行機のアイコン。ボックスの間に小さく「＋」。
""" + STYLE,

    "img-01-where-it-waits": """日本語の技術ブログ用に、予約した依頼が「どこで待つか」を示す左右比較図を作成してください。

【画像内に描画する日本語テキスト（このとおり正確に）】
- 一番上の大きな見出し: 「予約した依頼は、どこで待つ？」
- 左パネル見出し: 「新しいセッションに予約」
  左パネルの項目: 「サイドバーの Drafts に表示」「送信時刻になるとセッションが始まる」
- 右パネル見出し: 「既存のチャットに予約」
  右パネルの項目: 「そのチャットの Scheduled エリアに表示」「送信時刻つきで並ぶ」
- 両パネルの下に横長の帯: 「エージェントが作業中でも、割り込まずに順番待ち」
- 一番下の帯: 「送信時刻のとき、そのチャットの現在の設定で送られる」

【レイアウト】
左右2分割。左はサイドバーのリストに「Drafts」の見出しとカードが並ぶ絵、右はチャット画面の下に時計つきの小さなカードが並ぶ絵。ボックス内の文字は指定したものだけにし、ロゴは入れない。
""" + STYLE,

    "img-02-conditions": """日本語の技術ブログ用に、Send Later が動く条件と落とし穴をチェックリスト形式で示す図を作成してください。

【画像内に描画する日本語テキスト（このとおり正確に）】
- 一番上の大きな見出し: 「Send Later が届く条件」
- 左側に「必要なもの」の列（緑のチェックマークつきカード3枚）:
  「Agent Host が起動している」「対象は This Computer のセッション」「chat.automations.enabled がオン」
- 右側に「注意すること」の列（オレンジの注意マークつきカード3枚）:
  「スリープ中の PC は起こさない」「リモート / Cloud セッションは対象外」「逃した依頼はホスト復帰後に1回だけ処理」
- 一番下の帯: 「PC を起こしておくのは、あなたの役目」

【レイアウト】
左右2列のチェックリスト。左は緑系、右はオレンジ系で色分けする。中央に小さなノート PC のアイコン（フタが半分閉じている）。
""" + STYLE,

    "img-03-sleep-timeline": """日本語の技術ブログ用に、PC がスリープしている間に予約時刻を過ぎた場合の動きを示す横長のタイムライン図を作成してください。

【画像内に描画する日本語テキスト（このとおり正確に）】
- 一番上の大きな見出し: 「スリープ中に時刻を過ぎたら？」
- 左から右へ4つの出来事を矢印でつなぐ（それぞれ時刻と短い説明）:
  「22:00  7:00 に送る予約をする」
  「23:00  PC がスリープ」
  「07:00  予約時刻。でも PC は眠ったまま」
  「07:30  PC が復帰 → 逃した依頼を1回だけ処理」
- 「例」と小さく書いたバッジをタイムラインの左上に置く
- 一番下の帯: 「予約は消えない。ただし、時刻ぴったりには届かない」

【レイアウト】
横一直線のタイムライン。4つの出来事のうち、3つ目は月と Zzz のアイコン、4つ目は太陽とノート PC のアイコンで描く。3つ目と4つ目の間に点線の「待ち」区間を入れる。
""" + STYLE,

    "img-04-compare-scheduling": """日本語の技術ブログ用に、VS Code の「あとで動かす」3つの仕組みを比べる3列の比較表を作成してください。

【画像内に描画する日本語テキスト（このとおり正確に）】
- 一番上の大きな見出し: 「あとで動かす3つの仕組み」
- 左の列の見出し: 「Send Later」
  左の列の項目: 「1回だけ送る」「ローカルの Agent Host で待つ」「PC は起きている必要あり」
- 中央の列の見出し: 「ローカル Automation」
  中央の列の項目: 「繰り返し実行（Hourly / Daily / Weekly / Cron）」「ローカルの Agent Host で実行」「PC は起きている必要あり」
- 右の列の見出し: 「Cloud Automation」
  右の列の項目: 「繰り返し・イベントで起動（Daily / Weekly / Issue / PR）」「GitHub のクラウドで実行」「PC を閉じても動く」
- 一番下の帯: 「1回なら Send Later、繰り返しなら Automation」

【レイアウト】
3列のカード。左はノート PC と紙飛行機、中央はノート PC とカレンダー、右は雲とカレンダーのアイコン。右の列だけ強調色（エメラルドグリーン）の枠にする。アイコンの中に文字やロゴは入れない。
""" + STYLE,

    "img-05-decision-flow": """日本語の技術ブログ用に、「どれを使う？」を決めるフローチャートを作成してください。

【画像内に描画する日本語テキスト（このとおり正確に）】
- 一番上の大きな見出し: 「どれを使う？ 早見フロー」
- スタート: 「エージェントに頼みたいことがある」
- 分岐1（ひし形）: 「いま送れる状態？」
  「いいえ（準備中）」→ 結果ボックス: 「Drafts に保存」
  「はい」→ 分岐2へ
- 分岐2（ひし形）: 「いま送る？」
  「はい」→ 結果ボックス: 「そのまま送信」
  「あとで」→ 分岐3へ
- 分岐3（ひし形）: 「1回だけ？」
  「はい」→ 結果ボックス: 「Send Later」
  「繰り返す」→ 分岐4へ
- 分岐4（ひし形）: 「PC を閉じても動かしたい？」
  「はい」→ 結果ボックス: 「Cloud Automation」
  「いいえ」→ 結果ボックス: 「ローカル Automation」

【レイアウト】
上から下へ流れるフローチャート。結果ボックスは右側に縦に並べ、色で区別する（Drafts は紫、Send Later は青、Cloud Automation は緑、ローカル Automation はオレンジ）。
""" + STYLE,
}


def generate(name: str, prompt: str) -> bool:
    body = json.dumps({
        "model": MODEL,
        "prompt": prompt,
        "size": SIZE,
        "quality": QUALITY,
        "n": 1,
    }).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE_URL}/images/generations",
        data=body,
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
    )
    for attempt in range(1, 4):
        try:
            with urllib.request.urlopen(req, timeout=300) as resp:
                data = json.load(resp)
            image = base64.b64decode(data["data"][0]["b64_json"])
            OUT_DIR.mkdir(parents=True, exist_ok=True)
            out = OUT_DIR / f"{name}.png"
            out.write_bytes(image)
            print(f"✅ 保存完了: {out}")
            return True
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", errors="replace")[:300]
            # 429 / 5xx は待って再試行。それ以外（認証・モデル名・モデレーション）は直さないと再試行しても無駄
            if e.code == 429 or e.code >= 500:
                print(f"⏳ {name}: HTTP {e.code}、{attempt * 10}秒待って再試行します")
                time.sleep(attempt * 10)
                continue
            print(f"❌ {name}: HTTP {e.code} {detail}")
            return False
        except Exception as e:  # noqa: BLE001
            print(f"❌ {name}: {e}")
            return False
    return False


def main():
    if not API_KEY:
        print("❌ OPENAI_API_KEY が見つかりません。.env に OPENAI_API_KEY=... を追加してください")
        sys.exit(1)
    keys = sys.argv[1:]
    targets = {k: v for k, v in PROMPTS.items() if not keys or any(s in k for s in keys)}
    if not targets:
        print(f"❌ 一致する画像がありません。候補: {', '.join(PROMPTS)}")
        sys.exit(1)
    print(f"モデル: {MODEL} / サイズ: {SIZE} / 品質: {QUALITY} / 対象: {len(targets)} 枚")
    failed = [name for name, prompt in targets.items() if not generate(name, prompt)]
    if failed:
        print(f"⚠️ 失敗: {', '.join(failed)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
