# デモ手順 & スクリーンショット撮影ガイド

記事「エージェントの可能性が広がった！Computer Use ＋ 画像生成 ＋ Canvas で何ができるのか検証してみた」の、実装例セクションでデモする際の手順書です。

このガイドを参考に、各セクションで対応するスクリーンショットを撮影・編集し、記事に挿入してください。

---

## 📺 動画化・デモ化の構成

### セクション別 スクリーンショット撮影チェックリスト

| # | セクション | 撮影内容 | ファイル名 | 備考 |
|----|-----------|---------|----------|------|
| 1 | Computer Use とは | Computer Use ツール一覧のテーブル | `img-01-computer-tools.png` | 17個のツール図 |
| 2 | Computer Use パフォーマンス | ベンチマークグラフ | `img-02-benchmark-osworld.png` | 2024年 → 2026年の推移 |
| 3 | Computer Use API 例 | Python コード＆実行結果 | `img-03-api-code-example.png` | VS Code で実行中の画面 |
| 4 | Canvas UI デモ | Canvas パネルの操作画面 | `img-04-canvas-demo.png` | Claude / GitHub Copilot での実例 |
| 5 | Canvas フォーマット対応表 | テーブル表示 | `img-05-canvas-formats.png` | HTML/React/Markdown 対応状況 |
| 6 | Canvas カスタマイズコード | React コードスニペット | `img-06-canvas-custom-code.png` | GitHub Copilot SDK 例 |
| 7 | 画像生成 API 例 | Python コード＆生成結果 | `img-07-image-gen-result.png` | Gemini API 呼び出し + 出力画像 |
| 8 | 統合ワークフロー実行結果 | ターミナル出力 | `img-08-workflow-output.png` | ✅ スクリーンショット取得 〜 🎉 最終成果物 |
| 9 | コスト推定テーブル | 料金表 | `img-09-cost-table.png` | トークン数 & 推定コスト |

---

## 📋 詳細なデモ手順

### Step 1: Computer Use ツール一覧 `img-01-computer-tools.png`

**撮影方法**:
1. VS Code またはテキストエディタを開く
2. 以下を表示（または作成）:
```python
# Computer Use の 17 個ツール
COMPUTER_TOOLS = [
    "computer_tool_screenshot",
    "computer_tool_mouse_click",
    "computer_tool_mouse_move",
    # ... 残り 14 個
]
```
3. VS Code のテーマを「Dark Modern」に設定
4. **スクリーン範囲**: エディタ全体（画面の左右辺まで）
5. **サイズ**: 1280x720 以上推奨
6. **ファイルに保存**: `/computer-use-canvas-images/img-01-computer-tools.png`

---

### Step 2: OSWorld ベンチマーク `img-02-benchmark-osworld.png`

**撮影方法**:
1. Google Sheets / Excel で以下グラフを作成:

```
年  精度
2024  15%
2025  45%
2026  72.5%
```

2. 折線グラフで表示
3. 横軸ラベル: "2024年 → 2026年"
4. 縦軸ラベル: "精度 (%)"
5. 大見出し: "OSWorld ベンチマーク推移"
6. **スクリーンショット**: グラフ全体
7. **ファイルに保存**: `/computer-use-canvas-images/img-02-benchmark-osworld.png`

---

### Step 3: API コード例＆実行 `img-03-api-code-example.png`

**撮影方法**:
1. VS Code で以下ファイルを開く:
```python
# computer_use_demo.py
from anthropic import Anthropic

client = Anthropic()

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

for block in response.content:
    if block.type == "tool_use":
        print(f"Tool Used: {block.name}")
```

2. **スプリットビュー**: 左にコード、右にターミナル出力
3. ターミナルで実際に `python computer_use_demo.py` を実行
4. 出力例:
```
Tool Used: computer
Action: screenshot
Image size: 1920x1080
```
5. **スクリーンショット**: VS Code 全体（コード＋ターミナル）
6. **ファイルに保存**: `/computer-use-canvas-images/img-03-api-code-example.png`

---

### Step 4: Canvas UI デモ `img-04-canvas-demo.png`

**撮影方法**:
1. **実機デモ推奨**（実際の Claude.ai / GitHub Copilot）
   - または、デモ画面のスクリーンショットをネットから取得

2. **表示内容**: Canvas パネルが左右に分かれている画面
   - 左: Chat ウィンドウ「Create a React counter component」
   - 右: Canvas パネルで React コードがリアルタイム表示
   - Canvas パネルに「Edit」ボタン、「Preview」タブが見える

3. **スクリーンショット**: ブラウザ全体（タイトルバー含む）
4. **ファイルに保存**: `/computer-use-canvas-images/img-04-canvas-demo.png`

💡 **代替案**: 公式ブログの Canvas デモ画像を参照して、自分の言葉で説明を追加するだけでも OK

---

### Step 5: Canvas フォーマット対応表 `img-05-canvas-formats.png`

**撮影方法**:
1. Google Sheets / Excel / Numbers で以下テーブルを作成:

```
フォーマット | 対応状況 | 活用シーン
HTML/CSS | ✅ | Web UI デモ作成
React | ✅ | インタラクティブ UI
Python | ⚠️ | デモコード検証
Markdown | ✅ | 記事・README 作成
JSON | ✅ | 設定ファイル
SVG | ✅ | ロゴ・図解
```

2. 行ごとに背景色を交互に変更（見やすく）
3. ✅ / ⚠️ / ❌ は大きめのフォントで
4. **スクリーンショット**: テーブル全体
5. **ファイルに保存**: `/computer-use-canvas-images/img-05-canvas-formats.png`

---

### Step 6: Canvas カスタマイズコード `img-06-canvas-custom-code.png`

**撮影方法**:
1. VS Code で以下ファイルを開く:
```javascript
// MyCustomCanvas.jsx
import { Canvas } from "@github/copilot-sdk";

export const MyCustomCanvas = () => {
  return (
    <Canvas type="custom">
      <div style={{ padding: "20px" }}>
        <h1>Custom Canvas Component</h1>
        <p>ここに独自の React コンポーネントを置ける</p>
      </div>
    </Canvas>
  );
};
```

2. **テーマ**: Dracula / One Dark Pro など濃い背景
3. シンタックスハイライトがはっきり見える設定に
4. **フォントサイズ**: 14～16px（読みやすく）
5. **スクリーンショット**: コード全体
6. **ファイルに保存**: `/computer-use-canvas-images/img-06-canvas-custom-code.png`

---

### Step 7: 画像生成 API 例 & 結果 `img-07-image-gen-result.png`

**撮影方法**:
1. **スプリットビュー構成**:
   - 左: Python コード
   - 右: 生成された画像

2. **左側 - Python コード**:
```python
import google.genai as genai

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=["Create a diagram..."],
    config={"response_modalities": ["IMAGE"]},
)
```

3. **右側 - 生成画像**:
   - Gemini API で実際に生成した画像
   - または、[IMAGE_PATH] というプレースホルダー画像

4. **スクリーンショット**: コード＋画像が同時に見える範囲
5. **ファイルに保存**: `/computer-use-canvas-images/img-07-image-gen-result.png`

---

### Step 8: 統合ワークフロー実行 `img-08-workflow-output.png`

**撮影方法**:
1. 統合スクリプト（`main.py`）を実行:
```bash
python main.py
```

2. **ターミナル出力の例**:
```
✅ スクリーンショット取得: 1920x1080
✅ UI 要素認識: 34個
✅ JSON 構造化: 完了
✅ Canvas 生成: 2.1秒
✅ 画像生成: 1.2秒で完了
🎉 最終成果物: architecture-diagram.png + metadata.json
```

3. **スクリーンショット**: ターミナル全体（スクロール後の最終出力）
4. **ファイルに保存**: `/computer-use-canvas-images/img-08-workflow-output.png`

💡 **リアルに実行できない場合**: モックスクリーンショットを作成
```bash
# シミュレーション出力をテキストファイルで作成し、スクリーンショット
echo "✅ スクリーンショット取得..." > output.txt
echo "🎉 最終成果物: architecture-diagram.png" >> output.txt
```

---

### Step 9: コスト推定テーブル `img-09-cost-table.png`

**撮影方法**:
1. Google Sheets / Excel で以下テーブルを作成:

```
シナリオ | トークン数 | 推定コスト
Computer Use 1回 | 5,000～10,000 | $0.15～0.30
Canvas 生成 10回 | 50,000 | $0.15
画像生成 1回 | - | $0.05～0.10
合計 | 60,000 | $0.35～0.55
```

2. 「合計」行を太字＋背景色で目立たせる
3. **スクリーンショット**: テーブル全体
4. **ファイルに保存**: `/computer-use-canvas-images/img-09-cost-table.png`

---

## 🎯 撮影後の処理

### 1. 画像最適化

各画像を以下の仕様に調整：

```bash
# ImageMagick を使用して最適化
convert img-01-computer-tools.png \
  -resize 1280x720 \
  -quality 85 \
  -strip \
  img-01-computer-tools-opt.png
```

または、オンラインツール:
- [TinyPNG](https://tinypng.com/)
- [Squoosh](https://squoosh.app/)

### 2. ファイル配置

```
computer-use-canvas-images/
├── article.md                        # 記事本文
├── img-00-tldr-overview.png         # TL;DR 用概要
├── img-01-computer-tools.png
├── img-02-benchmark-osworld.png
├── img-03-api-code-example.png
├── img-04-canvas-demo.png
├── img-05-canvas-formats.png
├── img-06-canvas-custom-code.png
├── img-07-image-gen-result.png
├── img-08-workflow-output.png
├── img-09-cost-table.png
└── demo-guide.md                    # このファイル
```

### 3. 記事内での画像参照方法

記事の各セクションで、以下のように画像を挿入：

```markdown
## 3. 画像生成との組み合わせ

![画像生成 API と結果](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/computer-use-canvas-images/img-07-image-gen-result.png)
```

### 4. GitHub にプッシュ

```bash
cd /home/shahin/Qiita-github

git add computer-use-canvas-images/
git commit -m "feat: Add Computer Use + Canvas article with demo screenshots"
git push origin main
```

画像の Raw URL が有効になるまで 1～2 分待つ

---

## 🎬 ライブデモ実施時のチェックリスト

実際にワークショップ・LT で Live Demo をする際のチェックリスト：

- [ ] インターネット接続を確認
- [ ] 各 API キー（Anthropic, Gemini）がセットされているか確認
- [ ] 画面解像度を 1920x1080 に設定
- [ ] VS Code テーマを「Dark Modern」に統一
- [ ] ターミナルフォントサイズを 14px に統一
- [ ] スクリーン共有ソフト（OBS Studio など）をセットアップ
- [ ] 実行スクリプト（`main.py` など）を事前テスト
- [ ] API レート制限を確認（課金額の上限を設定）
- [ ] バックアップスクリーンショット（代替画像）を用意

---

## 📝 記事投稿前の最終チェック

- [ ] 全ての画像が正しくパス参照されているか
- [ ] 画像の Raw URL が有効か（ブラウザで確認）
- [ ] Qiita 記事のプレビューで画像が表示されるか
- [ ] コードブロックに言語指定がされているか
- [ ] タグが最大 5 個まで（本記事は 5 個）
- [ ] タイトルに具体的なキーワードが含まれているか
- [ ] TL;DR セクションが読みやすいか
- [ ] まとめセクションが充実しているか

---

## 🔗 参考資料へのリンク

記事内で言及した公式ドキュメント：

- [Anthropic - Computer Use API](https://docs.anthropic.com/computer-use)
- [Claude 3 モデル比較](https://docs.anthropic.com/claude/reference/models)
- [GitHub Copilot Canvas ドキュメント](https://github.blog/news-insights/product-news/)
- [Gemini 画像生成 API](https://ai.google.dev/gemini-api/docs/vision)

---

**Last Updated**: 2026-10-30  
**Author**: Shahin  
**Status**: 撮影・編集ガイド完成
