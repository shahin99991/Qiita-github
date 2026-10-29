#!/usr/bin/env python3
"""
Agensh / Orchestrator vs 自己組織化 記事用の解説イメージを Gemini API（gemini-3-pro-image）で生成する。
Usage:
  python agensh-agentic-workflow/generate_images.py          # 全部生成
  python agensh-agentic-workflow/generate_images.py tldr     # 指定キーを含むものだけ生成
"""
import os
import sys
import time
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
- 文字は太めで読みやすい日本語フォント。誤字・文字化けがないよう、指定した日本語と数字をそのまま正確に描画する
- 配色は Microsoft ブルー（#0078D4 系）を主役に、アクセントにオレンジ（#F7630C 系）とエメラルドグリーン（#10893E 系）
- 親しみやすく、でもプロフェッショナルな技術ブログ向けの雰囲気。指定していない余計な文字やロゴは入れない
"""

PROMPTS = {
    "img-00-tldr-overview": """日本語の技術ブログ（Qiita）用の TL;DR 解説バナー画像を作成してください。

【テーマ】
「Agent をスケールさせる方向は2つある。信頼性をスケールさせるか、組織をスケールさせるか」

【画像内に描画する日本語テキスト（このとおり正確に）】
- 一番上の大きな見出し: 「Agent をスケールさせる2つの方向」
  左ボックスの見出し: 「信頼性をスケール」
  左ボックスの小さな副題: 「例: Codex の /goal」
  左ボックスの中身: 「ゴールを持たせる」「テストなどで進捗を検証」「完了するまでループ」
  左ボックスの下の一言: 「途中で止まらない・勝手に完了しない」
- 右ボックスの見出し: 「組織をスケール」
  右ボックスの中身: 「中央の司令塔なし」「共有基盤で自己組織化」「最大 1,024 エージェント」
  右ボックスの下の一言: 「Agensh（Microsoft Research）」
- 左右のボックスの間に小さく: 「×」
- 一番下の帯: 「Orchestrator型 vs 自己組織化型 ― Agentic Workflow はどこへ向かう？」

【レイアウト】
左右2つの大きなボックスを対比させる。左は盾やチェックマークのアイコン（信頼性）、右は多数の小さなエージェントが網目状につながるアイコン（組織）。
""" + STYLE,
    "img-01-orchestrator-vs-selforg": """日本語の技術ブログ用に、2つのマルチエージェント構造を並べて比較する図解を作成してください。

【画像内に描画する日本語テキスト（このとおり正確に）】
- 左パネルの見出し: 「Orchestrator型」
  図: 中央に大きな丸「司令塔」、そこから放射状に6つの小さな丸「ワーカー」へ矢印が伸びる。矢印のラベルは「割り当て」と「報告」
  下の注釈: 「司令塔の処理能力が上限になる」
- 右パネルの見出し: 「自己組織化型」
  図: 6つの小さな丸「ワーカー」が、中央の大きな角丸ボックス「共有基盤」を取り囲み、それぞれがボックスと双方向の矢印でつながる。司令塔はいない
  共有基盤の中の3行: 「共有ワークスペース」「メッセージ」「共有コンテキスト」
  下の注釈: 「各ワーカーが自分で仕事を見つけて取りに行く」
- 一番下の帯: 「誰が分解する？ 状態はどこにある？ 誰が完了を決める？」

【レイアウト】
左右対称の2パネル。左は星型（ハブ&スポーク）の構図でオレンジ系、右は網目状の構図でブルー系。
""" + STYLE,
    "img-02-agensh-loop": """日本語の技術ブログ用に、Agensh（Microsoft Research のマルチエージェント基盤）の協調ループを図解してください。

【画像内に描画する日本語テキスト（このとおり正確に）】
- 上部の見出し: 「Agensh の協調ループ（各ワーカーが非同期に回す）」
- 円環状に5つのステップを矢印でつなぎ、最後は1に戻る:
  「1. 文脈を集める」「2. サブタスクを claim」「3. 実行する」「4. 検証する」「5. マージする」
- 円環の中央に小さく: 「ユーザーのゴール達成まで繰り返す」
- 下部に3つ横並びの基盤ボックス（円環のステップとつながる）:
  「共有ワークスペース（Git）」「メッセージ（チャット）」「共有コンテキスト」
- 共有コンテキストの下に小さなタグを5つ: 「OBSERVED」「FACT」「FAIL」「CLAIM」「PATCH_SUMMARY」

【レイアウト】
上に5ステップの円環、下に3つの基盤ボックス。ステップ4「検証する」だけ強調色（エメラルドグリーン）にして、チェックマークのアイコンを添える。
""" + STYLE,
    "img-03-scaling-results": """日本語の技術ブログ用に、エージェント数を増やしたときの成績を示す棒グラフ2つを並べた図を作成してください。数値は正確に。

【画像内に描画する日本語テキスト・数値（このとおり正確に）】
- 上の大見出し: 「エージェントを増やすと、何が起きた？」
- 左のグラフのタイトル: 「最難関5タスクの平均テスト通過率」
  棒グラフ（横軸はエージェント数、縦軸は通過率）:
  「1」→ 19.31%、「8」→ 20.68%、「32」→ 26.52%、「128」→ 28.78%
  グラフの上に吹き出し: 「約 49% 向上」
- 右のグラフのタイトル: 「pandoc のテスト通過率」
  「1」→ 33.89%、「128」→ 50.94%、「1,024」→ 55.06%
  グラフの上に吹き出し: 「+21.17pt」
- 一番下の注釈: 「条件: 各6時間・インターネットなし・同じモデルと同じ基盤」

【レイアウト】
左右に棒グラフ2つ。棒はエージェント数が増えるほど濃いブルーにする。各棒の上に数値ラベルを必ず付ける。棒の高さは数値に比例させる。
""" + STYLE,
    "img-04-emergence": """日本語の技術ブログ用に、エージェント数が増えるにつれて協調の形が進化する様子を、4段の階段図で作成してください。

【画像内に描画する日本語テキスト（このとおり正確に）】
- 上の大見出し: 「規模が大きくなると、協調の形が変わっていく」
- 階段の1段目（低い）: 見出し「8 エージェント」 説明「インターフェースを合意・重複を自分たちで解消」
- 階段の2段目: 見出し「32 エージェント」 説明「複数人で統合を管理・相互レビュー」
- 階段の3段目: 見出し「128 エージェント」 説明「レビュー役の使い分け・統合手順の標準化」
- 階段の4段目（高い）: 見出し「1,024 エージェント」 説明「同じ役割を複数人が担当・失敗を引き継ぐ」
- 一番下の帯: 「全員が同じプロンプト（違うのはワーカーIDだけ）から自然に出てきた」

【レイアウト】
左下から右上へ上る階段。段が上がるごとにアイコン（小さな人型ロボット）の数が増える。色は段ごとにブルーが濃くなる。
""" + STYLE,
    "img-05-hybrid": """日本語の技術ブログ用に、これからの Agentic Workflow の構成を3層で示す図を作成してください。

【画像内に描画する日本語テキスト（このとおり正確に）】
- 上の大見出し: 「これからの Agentic Workflow（筆者の予想）」
- 上段の帯（小さめ）: 「ゴールと完了条件を最初に固定」 右に小さく「人 / 軽量な司令塔」
- 中段の大きなエリア: 「自己組織化するワーカー群」 内部に多数の小さなエージェントが共有基盤の周りに集まる絵。エリア内の一言: 「仕事は自分で見つけて取る」
- 下段の帯: 「外部シグナルで検証」 内部に小さく「テスト」「CI」「マージ条件」
- 下段から中段へ戻る矢印に: 「未達なら再ループ」
- 上段から中段へ下りる矢印に: 「ゴールを渡す」

【レイアウト】
縦に3層。上から下へ流れ、下段から中段へ戻る循環矢印がある。中段が最も大きい。
""" + STYLE,
}


def generate(name: str, prompt: str, retries: int = 3) -> bool:
    client = genai.Client(api_key=API_KEY)
    for attempt in range(1, retries + 1):
        print(f"🎨 生成中: {name} ({MODEL}) try {attempt}")
        try:
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
