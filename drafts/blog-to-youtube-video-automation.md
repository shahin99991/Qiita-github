---
title: "社内技術ブログをYouTube解説動画に自動変換する方法【アプローチ比較＋ベストプラクティス】"
tags:
  - GitHub Copilot
  - VOICEVOX
  - Remotion
  - 動画自動化
  - Python
---

## はじめに

社内の技術ブログって、書いた本人以外にあまり読まれていない……なんてこと、うちだけですかね？

記事として公開されていても、「Confluenceに埋もれてる」「Slackに流れた」「あとで読もうと思ってそのまま」みたいな状況、けっこうあるんじゃないかなと思っています。

そんな中、[こちらのZenn記事](https://zenn.dev/microsoft/articles/github-update-movie-agent)を見て「これ社内ブログにも使えるのでは？」となりました。GitHub Copilot Agent Skills + VOICEVOX + Remotion でブログ記事を YouTube 動画にする仕組みを作ったという話で、正直かなりテンション上がりました！

この記事では、その方法をベースにして「他のやり方も含めてどれが社内ブログに向いているか」を整理してみました。技術力や使える環境によって選択肢が変わってくるので、自分のチームに近いケースを参考にしてもらえると嬉しいです。

**対象読者**

- 社内ブログの情報発信を改善したいエンジニア・DevRel 担当
- ブログ記事を動画にして社内に広めてみたい人
- AI や自動化ツールに興味がある人（初心者〜中級者）

---

## なぜブログを動画にしたいのか

文章で読むのとは、消費のハードルが全然違います。

- 文章：集中力が必要、読む気分のときにしか開かない
- 動画：流し見できる、聞くだけでもOK、移動中や休憩中にも消費できる

元の Zenn 記事でも「Changelog を『読まなきゃ』から『流しておこう』に変えられた」と書かれていましたが、これ、社内技術情報にもそのまま当てはまる話です。

同じ情報でも、動画の形にするだけで「これ昨日Slackに流れてた動画見たよ！」みたいな会話が生まれる可能性が高くなります。

---

## アプローチの全体像

社内ブログを動画にするアプローチは、大きく3種類あります。

| アプローチ                                            | 難易度 | コスト        | カスタマイズ性 | セキュリティ            |
| ----------------------------------------------------- | ------ | ------------- | -------------- | ----------------------- |
| ① フルスタック自動化（Copilot + VOICEVOX + Remotion） | ★★★    | 低（OSS中心） | ★★★            | ★★★（ローカル実行可）   |
| ② Python スクリプト方式（OpenAI TTS + MoviePy）       | ★★     | 中（API課金） | ★★             | ★★（APIに送信）         |
| ③ SaaS 利用（Lumen5 / Pictory.ai）                    | ★      | 中〜高        | ★              | ★（外部サービスに送信） |

どれがベストかは「チームのスキルセット」と「社内情報をどこまで外に出せるか」によって変わります。以降で1つずつ見ていきます。

---

## アプローチ①：フルスタック自動化（Copilot Agent Skills + VOICEVOX + Remotion）

### 概要

元の Zenn 記事で紹介されているやり方で、3つのツールを組み合わせます。

- **GitHub Copilot Agent Skills**：ブログ記事を読んで台本を生成する「監督兼放送作家」
- **VOICEVOX**：台本を音声に変換する「声優」（無料・ローカル動作）
- **Remotion**：音声・スライド・字幕を1本の動画に仕上げる「動画編集マン」

```
ブログ URL
    ↓
Copilot Agent Skill（記事取得 → 台本生成）
    ↓
VOICEVOX API（テキスト → wav）
    ↓
Remotion（スライド + キャラ + 字幕 + 音声 → mp4）
```

### 実装のポイント

Agent Skill は `.github/skills/<skill-name>/SKILL.md` に Markdown 1枚を置くだけで呼び出せます。ポイントは「手順をステップ番号付きで書く」こと。Copilot はその通りの順番で処理を進めてくれます。

```markdown
# ブログ動画化スキル

## 手順

### Step 1: 記事の取得

指定された URL から記事本文を取得してください。

### Step 2: 台本の生成

以下のルールで台本を生成してください。

- 1シーン30秒程度を目安に分割する
- 専門用語は簡単な言葉に言い換える
  ...

### Step 3: 音声合成

`scripts/generate-audio.sh` を実行して台本から wav を生成してください。

### Step 4: 動画レンダリング

`scripts/render-video.sh` を実行して mp4 を出力してください。
```

Copilot Chat で `この記事を動画にして：<URL>` と入力するだけで、上記の手順が順に走ります。

VOICEVOX はローカルで動く HTTP API なので、社内情報が外部に漏れる心配がありません！

```bash
# VOICEVOX エンジンを起動
./voicevox_engine

# テキストを音声に変換（ローカル API に送るだけ）
curl -s -X POST "http://localhost:50021/audio_query?text=こんにちは&speaker=1" \
  | curl -s -H "Content-Type: application/json" \
    -d @- -X POST "http://localhost:50021/synthesis?speaker=1" \
    > output.wav
```

Remotion は React で動画を書けるライブラリで、コンポーネントがそのまま動画のシーンになります。

```tsx
// 例：スライドシーンのコンポーネント
const SlideScene: React.FC<{ title: string; body: string }> = ({
  title,
  body,
}) => {
  return (
    <AbsoluteFill style={{ background: "#1a1a2e" }}>
      <h1 style={{ color: "#fff", fontSize: 48 }}>{title}</h1>
      <p style={{ color: "#ccc", fontSize: 28 }}>{body}</p>
    </AbsoluteFill>
  );
};
```

### 向いている場面

- エンジニアチームが主体で、React の知識がある
- 社内情報を外部サービスに送りたくない（ローカルでフル完結できる）
- 将来的に CI/CD に組み込んで完全自動化したい
- キャラクターや見た目にこだわりたい

### 難しい部分

- 初期構築に数日〜1週間くらいはかかる
- Remotion の学習コストがある（React に慣れていれば全然大丈夫ですが）
- VOICEVOX のキャラ利用規約を確認する必要がある（商用利用の場合は要チェック）

---

## アプローチ②：Python スクリプト方式（OpenAI TTS + MoviePy）

### 概要

Python だけで完結させたい場合の選択肢です。OpenAI の API を使って台本生成と音声合成を行い、MoviePy や ffmpeg で動画を組み立てます。

```
ブログ URL
    ↓
BeautifulSoup（記事本文のスクレイピング）
    ↓
OpenAI GPT-4（台本生成）
    ↓
OpenAI TTS / VOICEVOX（音声合成）
    ↓
MoviePy + ffmpeg（スライド画像 + 音声 → mp4）
```

### 実装例

```python
import openai
import requests
from bs4 import BeautifulSoup
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips

def fetch_article(url: str) -> str:
    """ブログ記事の本文を取得"""
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")
    # 記事本文の取得（サイトによって要調整）
    article = soup.find("article") or soup.find("main")
    return article.get_text(separator="\n") if article else ""

def generate_script(text: str) -> list[dict]:
    """GPT-4 で台本（シーン分割）を生成"""
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": (
                    "あなたは技術解説動画の台本ライターです。"
                    "記事の内容を5〜8シーンに分割し、"
                    "各シーンを{'title': '...', 'narration': '...'}のJSONリストで返してください。"
                    "ナレーションは1シーン30秒程度で、話し言葉に変換してください。"
                ),
            },
            {"role": "user", "content": f"以下の記事を動画台本にしてください:\n\n{text[:3000]}"},
        ],
        response_format={"type": "json_object"},
    )
    import json
    return json.loads(response.choices[0].message.content)["scenes"]

def text_to_speech(text: str, output_path: str) -> None:
    """OpenAI TTS で音声ファイルを生成"""
    client = openai.OpenAI()
    with client.audio.speech.with_streaming_response.create(
        model="tts-1",
        voice="nova",  # alloy / echo / fable / onyx / nova / shimmer
        input=text,
    ) as response:
        response.stream_to_file(output_path)

def create_slide_image(title: str, body: str, output_path: str) -> None:
    """スライド画像を生成（Pillow使用）"""
    from PIL import Image, ImageDraw, ImageFont
    img = Image.new("RGB", (1280, 720), color=(26, 26, 46))
    draw = ImageDraw.Draw(img)
    # タイトル描画（フォントは環境に合わせて指定）
    draw.text((80, 200), title, fill=(255, 255, 255))
    draw.text((80, 320), body, fill=(200, 200, 200))
    img.save(output_path)
```

### 向いている場面

- Python は書けるけど React は難しい
- 短期間（数時間〜1日）でプロトタイプを作りたい
- Remotion ほどの映像クオリティは求めていない
- 社内 Confluence や Notion の記事を対象にしたい

### 注意点

- OpenAI TTS は API に記事テキストを送信するため、機密情報が含まれる記事は注意
- 音声品質は VOICEVOX のキャラ音声と比べて「ナレーション寄り」な印象
- MoviePy でのアニメーション表現は Remotion より限られる

---

## アプローチ③：SaaS 利用（Lumen5 / Pictory.ai）

### 概要

ノーコードで使えるオンラインサービスを使う方法です。URL を貼り付けるだけで動画が生成されるので、エンジニア以外のメンバーでも使えます。

| サービス                          | URL入力            | 日本語対応     | AI音声            | 月額目安 |
| --------------------------------- | ------------------ | -------------- | ----------------- | -------- |
| [Lumen5](https://www.lumen5.com/) | ✅                 | △（UI は英語） | ✅                | $29〜    |
| [Pictory.ai](https://pictory.ai/) | ✅                 | △              | ✅（ElevenLabs）  | $19〜    |
| HeyGen                            | ❌（テキスト入力） | ✅             | ✅（AI アバター） | $24〜    |

### 使い方イメージ（Lumen5の場合）

1. Lumen5 にサインアップ
2. 「Blog Post to Video」を選択
3. ブログの URL を貼り付ける
4. AI が自動でシーンを分割・ストック動画を当てはめてくれる
5. テキスト・フォント・配色を好みに調整
6. エクスポート

ほんとにこれだけで、5〜10分で動画の雛形ができます。最初に試してみるならここから入るのが一番早いです。

### 向いている場面

- とにかく試してみたい（今日中に動画を作りたい）
- エンジニア以外のメンバーも使う可能性がある
- 社内ブログが外部公開されていて、URL が public にアクセスできる

### 注意点

- 社内限定のブログ（Confluence, Notion 等）は URL で取得できない場合が多い
- 記事テキストを外部サービスに送ることになる
- 日本語の自動ナレーションは品質がまだ不安定なことがある
- 月額コストがかかる（無料プランは制限あり）

---

## どれを選ぶべきか？ベストプラクティス

状況別のおすすめをまとめました。

### ケース1：「まず試してみたい」

→ **SaaS（Lumen5/Pictory）から始める**

外部公開されているブログ記事を1本、今日試してみてください。環境構築ゼロで動画の完成イメージが掴めます。「これ良いな」と思えたら、次のステップへ。

### ケース2：「社内限定ブログを動画にしたい」

→ **Pythonスクリプト方式 or フルスタック方式**

社内 Confluence や Notion の記事は URL が外部からアクセスできないことが多いので、スクレイピングか API で本文を取得する必要があります。OpenAI API に送るテキストに機密情報が含まれる場合は、VOICEVOX + Remotion のフルローカル構成が安心です。

### ケース3：「チームで継続的に運用したい」

→ **フルスタック自動化（Copilot Agent Skills + VOICEVOX + Remotion）**

Skill の Markdown がプロンプトを Git で管理できるというのは、地味に大きなメリットです。「台本の品質を上げたい」「特定の話し方に統一したい」という改善がチーム全員に効きます。GitHub Actions と組み合わせれば、記事が公開されるたびに自動で動画を生成する仕組みも作れます。

```yaml
# .github/workflows/blog-to-video.yml の例
name: Blog to Video
on:
  push:
    paths:
      - "blog/**/*.md" # ブログ記事が追加・更新されたとき

jobs:
  generate-video:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: "20"
      - name: Generate video
        run: |
          # VOICEVOX Engine の起動 + 動画生成スクリプトの実行
          npm run generate-video -- --input ${{ github.event.head_commit.added[0] }}
```

---

## 社内ブログへの適用で気をつけること

### セキュリティ・プライバシー

外部 API（OpenAI, Lumen5 等）を使う場合は、以下を確認しておくと安心です。

- 記事に個人情報・顧客情報・未公開の製品情報が含まれていないか
- 所属会社の AI ツール利用ポリシーに準拠しているか
- API のデータ保存・学習ポリシー（OpenAI は opt-out 設定が可能）

VOICEVOX + Remotion のローカル構成は、テキストがネットワーク越しに出ていかないため、機密情報を含む記事でも外部サービスより使いやすい選択肢です。

### 著作権・利用規約

- VOICEVOX の各キャラクターには個別の利用規約があります。商用利用する場合は必ず確認を
- ストック動画サービス（Pexels, Pixabay 等）を使う場合も利用規約の確認が必要

### 品質のコントロール

最初から全部自動化しようとすると、品質が安定しないことがあります。最初は「台本だけ AI 生成 → 人間がレビュー → 音声・動画は自動生成」という半自動の形から始めるのがおすすめです。

---

## まとめ

社内技術ブログを YouTube 動画にする方法を3つ紹介しました。

| アプローチ                      | こんな人に向いている                                           |
| ------------------------------- | -------------------------------------------------------------- |
| ① Copilot + VOICEVOX + Remotion | React が書けるエンジニア、長期運用・チーム利用、機密情報を扱う |
| ② Python スクリプト             | Python は書けるエンジニア、手軽にプロトタイプを作りたい        |
| ③ Lumen5 / Pictory.ai           | 今日試したい人、エンジニア以外も含むチーム、外部公開ブログ     |

個人的には、「まず③で体験 → 良さを確認したら①で本格構築」という流れが一番スムーズだと思っています。

情報発信の手段を一つ増やすだけで、「見てなかった記事を動画で見た」という同僚が現れるかもしれません。「文字で読む気にならなかったけど動画で流れてきたから見た！」という反応が1件でも出たら、それだけで作った甲斐があります！

---

## 参考

- [GitHub のアップデートを、Youtube ショート感覚でダラダラ見られる動画にしてみた（Zenn）](https://zenn.dev/microsoft/articles/github-update-movie-agent)
- [GitHub Copilot Agent Skills 公式ドキュメント](https://docs.github.com/ja/copilot/concepts/agents/about-agent-skills)
- [VOICEVOX 公式サイト](https://voicevox.hiroshiba.jp/)
- [Remotion 公式ドキュメント](https://www.remotion.dev/)
- [Lumen5 公式サイト](https://www.lumen5.com/)
- [Pictory.ai 公式サイト](https://pictory.ai/)
- [OpenAI TTS ドキュメント](https://platform.openai.com/docs/guides/text-to-speech)
