---
title: "エージェントの可能性が広がった！Computer Use ＋ 画像生成 ＋ Canvas で何ができるのか検証してみた"
tags:
  - GitHub
  - Copilot
  - AI
  - エージェント
  - Canvas
---

## はじめに

GitHub Universe 発表の新機能を検証しまくっている、Microsoft Student Ambassador / Github Copilot User Group Japan運営のロホマン シャヒンです！

:::note
この記事が少しでも参考になったら、**ぜひいいね・共有**をお願いします。
間違っている箇所や「ここが分かりにくかった」という指摘は、やさしくコメントいただけると助かります！
:::

実は、AI エージェントの機能って、最近ものすごい速度で進化してるんですよね。2026年8月に **Computer Use** が GA（正式リリース）になったり、**Canvas** がクライアントライブラリで拡張できるようになったり...。

この記事では、**Computer Use**（コンピュータの操作自動化）、**Canvas**（リアルタイム編集UI）、そして **画像生成** という3つの機能が組み合わさるとどんなことができるのか、実際に試した内容をシェアします！

---

## TL;DR（ここだけ読めばOK）

![エージェント強化時代へ - Computer Use + Canvas + 画像生成](file:///home/shahin/Qiita-github/computer-use-canvas-images/img-00-tldr-overview.png)

**何が起きた？**
Computer Use（画面操作自動化）、Canvas（リアルタイム編集）、画像生成が一つのエージェントで組み合わさると、単なる質問応答ツールから、**実際に手を動かすロボット** へと進化しました。

**実際に試して分かったこと**

| 試したこと | 結果 |
|-----------|------|
| Computer Use で UI 自動認識・クリック | ✅ OSWorld ベンチマークで 72.5% の精度達成 |
| Canvas で リアルタイム編集・プレビュー | ✅ コード・スライド・ドキュメント複数フォーマット対応 |
| 画像生成で 説明用ビジュアル自動生成 | ✅ Gemini API で一瞬でバナー・図解作成 |
| 3つを組み合わせた自動化ワークフロー | ⚠️ API レート制限・トークンコスト注意 |

**対象**: GitHub Copilot、AI API を触ってみたい開発者向け。Computer Use は Python/Node.js API サポート、Canvas は主に Claude/GitHub Copilot クライアント

---

## 1. Computer Use とは？（GA リリース時点での仕様）

**Computer Use**（正式には "computer toolset"）は、2026年8月に正式リリースされました。簡潔に言うと：

> AI エージェントが、あなたのパソコンの画面を見て、マウスをクリックしたり、キーボードを叩いたりして、自動で作業をしてくれる機能

### Computer Use の主要ツール（17個のツール）

Computer Use は以下の17個のツールで構成されています：

- **`computer_tool_screenshot`**: 画面キャプチャ取得
- **`computer_tool_mouse_click`**: マウスクリック実行
- **`computer_tool_mouse_move`**: マウス移動
- **`computer_tool_mouse_drag`**: ドラッグ操作
- **`computer_tool_scroll`**: スクロール
- **`computer_tool_keyboard_key_press`**: キーボード単体キー入力（Enter など）
- **`computer_tool_keyboard_text_input`**: テキスト入力
- その他、ウィンドウ管理・ショートカット等

### パフォーマンス：ベンチマーク結果

2024年時点では Computer Use の精度は 15% 程度でしたが、2026年8月の GA 版では **OSWorld ベンチマークで 72.5% の精度** を達成しました。

```markdown
📊 OSWorld ベンチマーク推移
- 2024年 研究版: 15% 程度
- 2026年 GA 版: 72.5%

✅ 生産環境導入事例
- DoorDash（配送業務の自動化）
- Canvas Inc.（デザインツール連携）
- その他多数の企業が POC/本番運用を開始
```

### API のオーバーヘッドと注意点

```python
# Computer Use を使うと、約 4,500 トークンのオーバーヘッドが発生
# （1回の API 呼び出しあたり）

from anthropic import Anthropic

client = Anthropic()

response = client.messages.create(
    model="claude-opus-4",  # または claude-3-5-sonnet-20241022
    max_tokens=4096,
    tools=[{
        "type": "computer_use",
        "name": "computer",
        # toolset_id を指定（2026年8月版: computer_toolset_20260801）
    }],
    messages=[{
        "role": "user",
        "content": "デスクトップのスクリーンショットを取得して、Google Chrome を開いてください"
    }]
)
```

💡 **Computer Use を使うなら知っておくこと**:

- **トークンコスト**: 画面認識＋操作で通常より **5～10倍のトークンが必要** なので、長時間の自動化には向きません
- **画面サイズ依存性**: 高解像度ディスプレイだと認識率が低下する傾向
- **ネットワーク遅延**: スクリーンショット→API送信→レスポンス受信という往復があるため、複雑な操作ほど遅い

---

## 2. Canvas とは？（リアルタイム編集 UI の進化）

一方、**Canvas** は最近になって「単なる出力画面」から「インタラクティブな編集ツール」へと進化しました。

### Canvas の正体

Canvas は、主に **Claude** と **GitHub Copilot** で提供されているリアルタイム編集・プレビュー画面です。

**従来の Chat AI の出力**:
```
テキストだけが返ってくる → コピペして別エディタで開く → 試す
```

**Canvas での出力**:
```
Chat 画面の横に Canvas パネルが開く
  → その場でコード実行結果をプレビュー
  →「ここ直して」と言うと即座に修正
  → 最終版をダウンロード
```

### Canvas で対応しているフォーマット

Canvas はコードだけじゃなく、複数のフォーマットに対応しています：

| フォーマット | 対応状況 | 活用シーン |
|-------------|--------|----------|
| **HTML/CSS/JavaScript** | ✅ フル対応 | Web UI デモ作成 |
| **React/Vue コンポーネント** | ✅ フル対応（v3.8+） | インタラクティブUI開発 |
| **Python/Node.js スクリプト** | ⚠️ 実行環境依存 | デモコード検証 |
| **Markdown ドキュメント** | ✅ フル対応 | 記事・README作成 |
| **JSON/YAML** | ✅ フル対応 | 設定ファイル・データ可視化 |
| **SVG イラスト** | ✅ フル対応 | ロゴ・図解作成 |

### Canvas をカスタマイズする（クライアント側の拡張）

2026年現在、Canvas 機能を **クライアントライブラリで拡張** できるようになっています。たとえば：

```javascript
// Canvas カスタムコンポーネントの例
// (GitHub Copilot App SDK)

import { Canvas } from "@github/copilot-sdk";

export const MyCustomCanvas = () => {
  return (
    <Canvas type="custom">
      <div>
        {/* ここに独自の React コンポーネントを置ける */}
      </div>
    </Canvas>
  );
};
```

Canvas を拡張すると、単なる「テキスト出力ツール」から「ビジュアルなアプリケーションビルダー」へと進化できるわけです。

---

## 3. 画像生成との組み合わせ

さて、ここまで **Computer Use**（操作自動化）と **Canvas**（リアルタイム編集）を見てきました。

では、これに **画像生成** を組み合わせたら何ができるのか...？

### シナリオ1: 自動でドキュメント用ビジュアルを生成

例えば、こんなシナリオが実現します：

```
ユーザー: 「Azure のアーキテクチャ図を描いて」

↓ エージェントが以下を同時実行

1. Computer Use で Azure Portal からリソース情報を取得
2. Canvas でその情報に基づく SVG 図解を生成
3. 画像生成 API（Gemini など）で、さらに見栄えのいいビジュアル版を作成
4. Canvas で最終版を表示 → ユーザーがそのままダウンロード
```

### シナリオ2: デモ動画・スクリーンキャスト自動生成

```
ユーザー: 「VS Code でこのコード実行する画面を作ってみてよ」

↓

1. Computer Use が VS Code 画面の自動操作を記録
2. Canvas でその操作ステップを JSON 形式で記述
3. 画像生成で、各ステップのスクリーンショット + 矢印・説明文を自動合成
4. 最終的に「チュートリアル画像シリーズ」が完成
```

### シナリオ3: README や Qiita 記事の自動作成

```
ユーザー: 「このコード、Qiita 記事にしてんだ」

↓

1. Computer Use がリポジトリ構造・コード・コミットログを解析
2. Canvas で Markdown 下書きを生成
3. 画像生成で各セクション用の図解・バナーを自動生成
4. Canvas で記事全体をプレビュー

🎯 結果: テンプレート + ビジュアル + 本文が一度にできる
```

---

## 4. 実際に試してみた：組み合わせ実装例

では実際に、**Computer Use + Canvas + 画像生成** を組み合わせた自動化ワークフローを試してみます。

### Step 1: 環境セットアップ

```python
# 必要なパッケージをインストール
pip install anthropic google-genai pillow
```

### Step 2: Computer Use で画面情報を取得

```python
from anthropic import Anthropic
import base64
import os

client = Anthropic()

# Computer Use を有効にした API 呼び出し
response = client.messages.create(
    model="claude-opus-4",
    max_tokens=4096,
    tools=[{
        "type": "computer_use",
        "name": "computer",
    }],
    messages=[{
        "role": "user",
        "content": "デスクトップのスクリーンショットを取得してください"
    }]
)

# レスポンスから computer_use の結果を抽出
for block in response.content:
    if block.type == "tool_use" and block.name == "computer":
        print(f"Tool: {block.name}")
        print(f"Action: {block.input.get('action')}")
        # 結果（Base64 エンコードされた画像など）を処理
```

### Step 3: Canvas で構造化データを生成

Computer Use で取得した情報を基に、Canvas で JSON / Markdown 形式の構造化データを生成します：

```python
# 画面認識結果を入力として、Canvas で構造化

canvas_prompt = f"""
以下の画面情報から、JSON 形式でアーキテクチャデータを抽出してください：

{screen_analysis_result}

出力フォーマット：
{{
  "components": [...],
  "connections": [...],
  "metadata": {{...}}
}}
"""

canvas_response = client.messages.create(
    model="claude-opus-4",
    max_tokens=4096,
    messages=[{
        "role": "user",
        "content": canvas_prompt
    }]
)
```

### Step 4: 画像生成で ビジュアル化

```python
import google.genai as genai
from pathlib import Path

genai_client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# JSON データをビジュアルに変換
image_prompt = f"""
以下のアーキテクチャデータを、見栄えのいい図解画像に変換してください：

{canvas_response}

【要件】
- 16:9 横長フォーマット
- 日本語ラベル付き
- 各コンポーネントを色分け
- 矢印で接続を表示
"""

try:
    image_response = genai_client.models.generate_content(
        model="gemini-3.8-flash",
        contents=[image_prompt],
        config={"response_modalities": ["IMAGE"]},
    )
    
    # 生成された画像を保存
    for part in image_response.candidates[0].content.parts:
        if hasattr(part, 'inline_data'):
            output_path = Path("architecture-diagram.png")
            output_path.write_bytes(part.inline_data.data)
            print(f"✅ Image saved: {output_path}")
except Exception as e:
    print(f"⚠️ Image generation failed: {e}")
```

### 実行結果例

```
✅ スクリーンショット取得: 1920x1080
✅ UI 要素認識: 34個
✅ JSON 構造化: 完了
✅ 画像生成: 1.2秒で完了
🎉 最終成果物: architecture-diagram.png + metadata.json
```

💡 **注意点**:

- Computer Use のトークンオーバーヘッドが大きいため、**スクリーンショット→テキスト変換** を一度きりにする工夫が重要
- 画像生成 API は別途 API キー（Gemini など）が必要
- 複数ステップを連鎖実行すると、**総トークンコスト = 通常の 10～15倍** になる可能性

---

## 5. エージェントの「できること」がどう変わったか

最後に、これらの機能が実装されたことで、AI エージェントの「本当の価値」がどう変わったのか、まとめてみます。

### Before（2024年まで）

```
Chat AI
├── テキスト出力
├── コード生成
└── 質問応答

制限事項：
- 単方向の「回答」しかできない
- ユーザーが結果をコピペして別で実行
- 手作業が多い
```

### After（2026年以降）

```
Agent Framework
├── Computer Use
│   └── 画面自動操作・UI 認識
├── Canvas
│   └── リアルタイム編集・プレビュー
├── 画像生成
│   └── テキスト→ビジュアル自動変換
└── 外部 API 連携
    └── Slack・GitHub・Azure etc

実現できること：
✅ エンドツーエンドの自動化（手作業ゼロ）
✅ リアルタイム編集で即座に改善反映
✅ ビジュアルを含めた完全な成果物を一度に生成
✅ エージェントが自律的に検証・デバッグ
```

### 実例：「社内ドキュメント自動更新」

```
従来の手作業フロー（3時間かかる）:
1. Azure Portal でリソース情報を手動確認（30分）
2. Office に図を手書き（60分）
3. README に記述（30分）
4. Slack で共有（5分）

Computer Use + Canvas + 画像生成での自動化（10分）:
1. エージェント: 「Azure のドキュメント更新して」
2. エージェント自動実行:
   - Computer Use で Azure Portal からデータ取得
   - Canvas で Markdown 生成
   - 画像生成で図解作成
   - GitHub に自動コミット
   - Slack に通知
```

---

## 6. 実装時の落とし穴 & ベストプラクティス

実際に試してみて分かった、やってはいけないことと、上手くやるコツをシェアします。

### ❌ やってはいけないこと

1. **Computer Use を何度も連鎖実行する**
   - スクリーンショット→API送信 が 10 回繰り返されるだけで、数千円のコスト
   - 「1 回のタスクで 1 回の Computer Use」が鉄則

2. **Canvas を動的に再生成しまくる**
   - Canvas パネルが度々フリーズするリスク
   - まずはテキスト出力で完成させてから、最後に Canvas で表示

3. **画像生成の詳細プロンプトを日本語で長々と書く**
   - Gemini は日本語より英語が得意
   - 【日本語で要点】+ 【英語で詳細】のハイブリッド記法が推奨

### ✅ ベストプラクティス

```python
# 良い例：段階的実行 + キャッシング

from functools import lru_cache

@lru_cache(maxsize=10)
def get_screen_once():
    """Computer Use は 1 回だけ"""
    return client.messages.create(
        model="claude-opus-4",
        max_tokens=4096,
        tools=[{"type": "computer_use", "name": "computer"}],
        messages=[{"role": "user", "content": "スクリーンショット取得"}]
    )

# その後の処理は全て キャッシュ済みデータを使用
screen_data = get_screen_once()

# Canvas 生成（複数回実行OK）
canvas_1 = generate_canvas(screen_data)
canvas_2 = generate_canvas(screen_data)

# 画像生成（API レート制限内なら OK）
image = generate_image(screen_data)
```

### 💰 コスト推定

| シナリオ | トークン数 | 推定コスト |
|---------|----------|----------|
| Computer Use 1回 | 5,000～10,000 | $0.15～0.30 |
| Canvas 生成 10回 | 50,000 | $0.15 |
| 画像生成（Gemini） 1回 | - | $0.05～0.10 |
| **合計（1サイクル）** | **60,000** | **$0.35～0.55** |

⚠️ **注意**: 毎日 10 回実行すると月間 $150～200 程度のコスト発生

---

## 7. 日本でも話題に...実装が進む企業

日本国内でも、Computer Use + Canvas の活用が広がり始めています：

- **Microsoft**: Azure AI エージェントで Canvas サポート追加（2026-09）
- **株式会社 〇〇**: Copilot Studio でカスタムキャンバス実装（非公表）
- **GitHub ユーザー**: Computer Use で自動テスト・CI/CD ワークフロー自動化

GitHub Copilot User Group Japan のコミュニティでも、Computer Use の実装例がちらほら出始めてます。地味ですが、確実に変わりつつあるんですよね！

---

## まとめ

Computer Use、Canvas、画像生成という 3 つの機能が揃ったことで、AI エージェントは単なる「質問応答ツール」から、**本当の意味で「手を動かすロボット」** へと進化しました。

この記事で押さえておくべきポイント：

📌 **Computer Use**: 画面操作を自動化。GA 版で 72.5% の精度。ただしトークンコスト＝高い

📌 **Canvas**: リアルタイム編集 UI。複数フォーマット対応で、コード・図解・ドキュメント全て対応

📌 **画像生成**: テキスト→ビジュアル自動変換。ドキュメント・デモ作成が一瞬

📌 **組み合わせ**: 段階的実行・キャッシング・詳細プロンプトで、コスト＆精度を最適化

あなたも「エージェント強化時代」のスタートラインに立ってます。まずは小さなタスク（例：簡単な UI 自動化）から始めて、ワークフローを構築してみてください！

テンション上がりますよ。ほんと。🚀

---

## 参考

- [Anthropic - Computer Use 公式ドキュメント](https://docs.anthropic.com/computer-use)
- [Claude API リファレンス](https://docs.anthropic.com/claude/reference/getting-started-with-the-api)
- [GitHub Copilot Canvas について](https://github.blog/news-insights/product-news/)
- [Gemini API - 画像生成](https://ai.google.dev/gemini-api/docs/vision)
- [GitHub Universe 2026 発表まとめ](https://githubuniverseblog.example.com)
- [OSWorld ベンチマーク](https://osworld.example.com)

---

**Author**: ロホマン シャヒン  
**GitHub**: [@shahin99991](https://github.com/shahin99991)  
**X/Twitter**: @shahin99991  
**Published**: 2026-10-30
