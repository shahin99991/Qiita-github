---
title: >-
  【速報】VS Code 1.142 に Canvas が来た！チャットの横でエージェントと同じ画面を触れる「Interactive
  Canvases」を整理してみた
tags:
  - VSCode
  - GitHubCopilot
  - AIエージェント
  - canvas
  - GitHub
private: false
updated_at: '2026-10-23T16:54:48+09:00'
id: 81e6a6737b2254bdc6ed
organization_url_name: mspjp
slide: false
ignorePublish: false
posting_campaign_uuid: null
agreed_posting_campaign_term: false
---

## はじめに

常に VS Code / GitHub Copilot の動向を追っている、Microsoft Student Ambassador 兼 GitHub Copilot User Group Japan（Gh-CUG）運営のロホマン シャヒンです！

:::note
この記事が少しでも参考になったら、**ぜひいいね・共有**をお願いします。
間違っている箇所や「ここが分かりにくかった」という指摘は、やさしくコメントいただけると助かります！
:::

2026年10月14日にリリースされた **VS Code 1.142** の目玉が、**Canvases（Preview）** です。

公式のリリースノートでは、こう紹介されています。

> Canvases are interactive interfaces to collaborate with an agent. A canvas opens beside the chat, where you and the agent can inspect and update the same artifact instead of coordinating solely through prompts.
>
> （出典: [VS Code 1.142 Release Notes - Canvases (Preview)](https://code.visualstudio.com/updates/v1_142#_canvases-preview)）

ざっくり言うと、**チャットの横に「エージェントと自分が同じものを一緒に触れる画面」が開く**機能です。「ついに VS Code にも Canvas が来た！」という感じですね。

この記事では、公式ドキュメントと海外の記事・事例を読み込んだうえで、次の内容をまとめます。

- ✅ Canvases とは何か、チャットだけの協業と何が違うのか
- ✅ 有効化の手順と `/create-canvas` の使い方
- ✅ 使える環境・使えない環境（ここ、地味にハマりどころです）
- ✅ 海外で話題になっている使い方と、すでに公開されている Canvas 拡張
- ✅ VS Code と GitHub Copilot アプリ、どっちで使えばいいのか

対象読者は、VS Code と GitHub Copilot のエージェント機能をすでに触っている方です。

## TL;DR

![VS Code 1.142 の Canvases を、設定ON・/create-canvas・一緒に操作の3ステップで説明した概要図](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/VSCode-canvas-article/images/img-00-tldr-overview.png)

**何が起きた？**
VS Code 1.142（2026/10/14）で、チャットの横にエージェントと共有できる操作画面を開く **Canvases** が Preview で入りました。`chat.canvases.enabled` を ON にして、新しい Copilot セッションで `/create-canvas` と打つと、自分のプロジェクト向けの画面を作ってもらえます。

**押さえておきたいポイント**

| 項目                  | 内容                                                              |
| --------------------- | ----------------------------------------------------------------- |
| 有効化                | ✅ `chat.canvases.enabled` を ON（新規セッションから反映）       |
| 画面の作り方          | ✅ `/create-canvas` で日本語で説明するだけ（実際に作れた）        |
| 人とエージェントの共有 | ✅ 手で足したカードを、エージェントが説明なしで読み取れた        |
| 既存の Canvas を使う  | ⚠️ 今は GitHub Copilot アプリでプラグインを入れてから VS Code へ  |
| 動く環境              | ⚠️ デスクトップ版 × Copilot ハーネス × ローカルセッションのみ（私の WSL 環境ではタブで開けず） |
| Claude / Codex / Web  | ❌ 現時点では非対応                                               |

**対象**: VS Code 1.142 以降（デスクトップ版）。Preview 機能なので、今後仕様が変わる可能性があります。

## Canvases って何が嬉しいの？

### チャットは「意図を伝える」のは得意、でも「状態を持つ」のは苦手

エージェントに作業を任せていると、こんな経験ありませんか？

- 「さっき追加した3つ目のタスク、完了にして」と毎回チャットで伝える
- 計画や進捗がチャットのログに埋もれて、今どうなってるのか分からなくなる
- 小さな修正のたびに、もう一度プロンプトを書き直す

GitHub のブログでも、チャットは「意図を伝える場所としては最高だが、実際の作業が始まるとログと修正の長いスクロールになる」と整理されています。計画・判断ポイント・検証結果・承認のタイミングが、履歴に埋もれてしまうんですよね。

Canvases は、そこに「作業の置き場所」を作る発想です。

![チャットだけの協業と、Canvasありの協業の違いを比較した図](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/VSCode-canvas-article/images/img-04-chat-vs-canvas.png)

公式の例は **Kanban（カンバン）Canvas** です。

- 自分は、カードをその場で作ったり、ドラッグして動かしたりできる
- エージェントは、機能をタスクに分解したり、ステータスを更新したり、作業中に見つけた課題を追加したりできる

**同じボードを、人とエージェントの両方が直接いじれる**のがポイントです。「エージェントが作った結果を眺める」だけの画面じゃなくて、双方向に操作できる点が大事だと感じました。

### 仕組み：Canvas は「Canvas 拡張機能」が提供する

VS Code の公式ドキュメントによると、**すべての Canvas は「Canvas 拡張機能」によって提供**されます。

![人とエージェントが、Canvas拡張機能の共有ステートを双方向に操作する仕組みの図](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/VSCode-canvas-article/images/img-06-architecture.png)

GitHub Copilot アプリ側のドキュメントでは、Canvas 拡張機能の構成が次のように説明されています。

```text
.github/extensions/<拡張機能名>/   ← プロジェクト用（チームで共有）
~/.copilot/extensions/<拡張機能名>/ ← 個人用（自分のマシンだけ）
├─ package.json     … メタデータと依存関係
├─ extension.mjs    … Canvas の挙動と、エージェント向けアクションの定義
└─ artifacts/       … （任意）永続化したい状態の JSON など
```

UI のボタンやカードを人が操作すると状態が変わり、エージェントは **`get_board` / `add_card` / `move_card` のような「エージェントが呼べるアクション」** を通じて、同じ状態を読んだり更新したりします。

:::note info
💡 **Canvas 拡張機能は、VS Code Marketplace の拡張機能とは別物です。**
`/create-canvas` で自分で作るか、Canvas 拡張機能を含む「チャットプラグイン」を入れて使います。「Canvas 対応の VS Code 拡張機能を探す」と考えると迷子になりやすいので注意です。
:::

## 有効化して使ってみる

### Step 1: 設定を ON にする

まず設定画面で `chat.canvases.enabled` を検索します。初期状態は OFF です。

![設定画面で chat.canvases.enabled がOFFの状態](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/VSCode-canvas-article/images/img-01-setting-off.png)

チェックを入れて ON にします。説明文には「Agents Window と Editor Window の両方で、ローカルの Agent Host の Copilot セッションが Canvas を開ける」と書かれています。

![chat.canvases.enabled をONにした状態](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/VSCode-canvas-article/images/img-02-setting-on.png)

`settings.json` で直接書く場合はこうです。

```json:settings.json
{
  "chat.canvases.enabled": true
}
```

ちなみに、説明文に **"Newly created sessions pick up changes to this setting."** とあります。**設定を変えたあとは、新しいセッションを作り直す必要があります。** すでに開いているチャットでは反映されません。

### Step 2: Copilot ハーネスで新しいセッションを始める

Canvases は **Copilot ハーネス** のセッション専用です。新しいセッションを始めるときに、ハーネスが Copilot になっているか確認しておきましょう。

### Step 3: `/create-canvas` で作りたい画面を説明する

チャット欄に `/create-canvas` と入力すると、「What should the canvas show or let users do?（その Canvas は何を表示して、ユーザーに何をさせたい？）」と聞かれます。

![チャット入力欄で /create-canvas を入力した状態](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/VSCode-canvas-article/images/img-03-create-canvas-prompt.png)

ここに、作りたい画面を日本語で書きます。awesome-copilot の学習ハブでは、プロンプトに **「人が UI でやること」と「エージェントがアクションとして呼べること」を両方書く**のがコツだと紹介されています。

私は、記事執筆の進捗管理ボードを例にします。

```text
/create-canvas 記事執筆用のカンバン Canvas を作って。
列は「ネタ」「執筆中」「レビュー」「公開済み」。
人はカードの追加とドラッグでの移動ができる。
エージェントは get_board / add_card / move_card を呼べるようにして。
```

すると、エージェントが `.github/extensions/qiita-article-board/` に Canvas 拡張機能を作ってくれます。4列のカンバン画面と `get_board` / `add_card` / `move_card` の3アクションが入っていて、カードは同じフォルダの `artifacts/board.json` に保存される作りでした。拡張機能のリロードと、アクションが動くかの確認までやってくれたのは、地味に助かりました！

生成されたファイルは、エクスプローラーではこんな見た目です。`extension.mjs` が Canvas の定義、`server.mjs` と `ui/` が画面、`store.mjs` が保存処理で、`board.test.mjs` はテストです。

![.github/extensions/qiita-article-board/ 配下に生成されたファイル構成](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/VSCode-canvas-article/images/demo-06-extension-files.png)

### Step 4: 人とエージェントで同じボードを触る

まず、自分の手でカードを追加・移動してみました。「ネタ」「執筆中」「公開済み」にそれぞれカードを置いて、プルダウンやドラッグで動かせます。

![手でカードを追加して列を移動したカンバンボード](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/VSCode-canvas-article/images/demo-01-board-manual.png)

次に、エージェントにカードを足してもらいます。

![チャットでエージェントにカード追加を頼んでいる画面](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/VSCode-canvas-article/images/demo-02-agent-prompt.png)

```text
この記事を公開するまでに必要なタスクを、ボードに5枚追加して。
```

そうすると、ボードに5枚のカードが追加されました（赤枠が追加されたカードです）。

![エージェントが追加した5枚のカードに赤枠をつけたボード](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/VSCode-canvas-article/images/demo-03-agent-adds-cards.png)

ちなみに、列を指定しなかったので、エージェントが自分で振り分けて、まだ終わっていない「GitHub へ push して Qiita に公開する」が「公開済み」に入っていました（笑）。「ネタに入れて」のように列まで伝えたほうが確実です。

そのあと、今度は自分の手で「AI-103記事」というカードを「執筆中」に足して、チャットでこう聞いてみます。

![手でAI-103記事のカードを追加したボード](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/VSCode-canvas-article/images/demo-04-manual-add-card.png)

```text
いまボードで「執筆中」にあるカードを教えて。
```

エージェントは、チャットに `Invoking canvas action` と出しながらボードを読み取って、手で追加したカードも含めて答えてくれました。

![エージェントがボードを読み取り、執筆中のカードを答えた画面](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/VSCode-canvas-article/images/demo-05-agent-reads-board.png)

「AI-103記事を追加したよ」とは一言も伝えていないのに、状態が共有されています。**ここがこの機能の核心**だと思いました。プロンプトで状況を説明し直さなくていいのは、思ったよりラクです。

### Canvas を閉じてしまったときは

公式ドキュメントによると、一度閉じてもメニューから開き直せます（私の環境では前述のとおり試せていません）。

| 場所                      | 操作                                                 |
| ------------------------- | ---------------------------------------------------- |
| エディタウィンドウ        | Chat ビューの **New Chat (+) > Canvas**              |
| Agents ウィンドウ         | エディタ領域の **Add Tab (+) > Canvas**              |

エディタウィンドウの **Canvas サブメニューは、サポート対象の Copilot ハーネスのセッションで最初のメッセージを送ったあと**に表示されます。「メニューが出ない！」となったら、まずここを疑ってみてください。

## 使える環境・使えない環境

ここが一番ハマりやすいところなので、表にまとめておきます。

![Canvasesが使える環境と、まだ使えない環境の早見表](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/VSCode-canvas-article/images/img-05-requirements.png)

公式ドキュメントの注意書きをそのまま整理すると、次のとおりです。

| 環境                                        | 対応            |
| ------------------------------------------- | --------------- |
| VS Code デスクトップ版 × Copilot ハーネス × ローカルのAgent Hostセッション | ✅ 使える |
| Claude ハーネス / Codex ハーネス            | ❌ 非対応       |
| 拡張機能ホストの Local セッション           | ❌ 非対応       |
| リモートの Agent Host セッション            | ❌ 非対応       |
| ブラウザ / Web クライアント                 | ❌ 非対応       |
| 別ウィンドウ（auxiliary window）での表示    | ❌ 非対応       |

特に「**Local ハーネスだと出ない**」のが引っかかりやすいと思います。Local は VS Code 内蔵のハーネスで、Copilot ハーネスは GitHub Copilot SDK ベースの別物です。

:::note warn
⚠️ **企業・組織で使っている方へ**
VS Code 1.142 では、管理者がサンドボックスや権限ポリシーを設定していると、チャットが Copilot ハーネスで動くことが必須になり、既存の Local チャットは自動で Copilot へ移されます（Visual Studio Magazine / byteiota の報道による）。Canvases を使うこと自体にはむしろ追い風ですが、Claude や Codex が使えなくなる点は事前に確認しておくと安心です。
:::

## 海外ではどう話題になってる？

公式情報に加えて、海外のブログ・ニュース・コミュニティの反応も調べました。

### 「プロンプトの往復」から「同じものを共同編集」へ

byteiota は、Canvases を **「prompting ではなく co-editing（共同編集）」** という転換だと評価しています。同記事では、Windsurf の Agent Command Center にも Kanban 風のビューがあるものの、VS Code の Canvases は「単なるタスク一覧ではなく、エージェントと開発者が実際の成果物の状態を共有する」点でもう一歩進んでいる、と書かれていました。

個人ブログの theblackcloud は、「ボードに何が残ってる？」と何度もチャットで聞くより、一緒に更新できるボードのほうが便利そうだと素直にコメントしています。リリースチェックリストや、トラブルシューティング時の「調査結果と未確認項目のボード」といった使い方を想像しているのが印象的でした。

### GitHub の中の人は「毎日使ってる」

GitHub 公式ブログ（"How canvases make agentic workflows visible, steerable, and cost-efficient"）では、書き手が Canvases を **ほぼ毎日使っている**と紹介しています。この記事から押さえておきたいのは次の2点です。

**① 使える型は4つ**

1. ワークフローの状態を明確に定義する
2. 重要な判断ポイントを画面に出す
3. 進捗と下書きをすぐ永続化する
4. 人間の承認ポイントを明示する

実例として、Java モダナイゼーションの工程（評価 → 修正 → 検証 → 出荷）を可視化する **Java Modernization Studio** や、個人サイトのコンテンツ管理をする **Site Studio** が紹介されていました。

**② コストの話も正直に書かれている**

Canvas を作る投資は軽くなく、Site Studio で約 2,000 AI クレジット、モダナイゼーション用で約 3,000 AI クレジットかかった、とのことです。そのうえで「繰り返し使うワークフローなら、プロンプトの繰り返しや文脈の喪失、手戻りが減って元が取れる」という整理でした。

また Microsoft の開発者ブログでは、フィルタやオプション選択のような日常的な操作は **AI モデルを呼ばずにコード側で処理**できるため、待ち時間も AI クレジットも節約できる、と説明されています。

:::note info
💡 「毎回 AI に頼むと遅くて高い操作」を Canvas 側の UI に逃がせるのが、実務ではいちばん効きそうです。
:::

### すでに公開されている Canvas 拡張が面白い

[awesome-copilot の Extensions ページ](https://awesome-copilot.github.com/extensions/)には、コミュニティ製の Canvas 拡張が並んでいます。

| 拡張                            | できること                                                                 |
| ------------------------------- | -------------------------------------------------------------------------- |
| Agent Arcade                    | エージェントが作業している間に、レトロなミニゲーム6本で遊べる              |
| Agent Radar                     | 手元の Copilot エージェントやサブエージェントの構成・通信先をマップ表示   |
| Artifact Explorer               | PR や GitHub Actions の成果物（テスト結果・静的サイト等）を安全に閲覧     |
| Apng Studio                     | フレームから APNG アニメーションを作って書き出し                          |
| Azure Cost Health Check         | Azure のコスト・予測・予算アラート・Advisor 推奨を読み取り専用で確認      |
| Azure Functions Hosted Skills   | Azure Functions のホステッドスキルを Canvas からビルド・実行・デバッグ    |

Agent Arcade みたいな遊び心のあるものから、Azure のコスト分析のようなガチな業務向けまで幅があって、Canvas が「ただのカンバン」で終わらないことが分かります。

### Azure 向けは「作る」ためのプラグインも出ている

9月末には Microsoft が **Azure Canvases**（Azure Functions Hosted Skills / Azure Resources Query / Azure Cost Health Check）を公開しました。さらに10月6日には、自分で Azure 用の Canvas を作るための **Canvas authoring plugin** と、その土台になる **`@microsoft/canvas-toolkit`**（npm パッケージ）が紹介されています。

ブログでは、次のような例が挙げられています。

- 「リソースグループを一覧する読み取り専用の Azure Canvas」を、`create-canvas` スキル経由でスキャフォールドする
- 「Azure Container Apps のスケールを管理する Canvas」を作る（変更は適用前にプレビューする設計）

toolkit には、Azure 認証、テーマ対応の UI 部品、ローカルバックエンド、状態管理とライブ更新、エージェント連携の橋渡しが入っているそうです。「Azure 向けの専用画面を自分で作りたい」場合の選択肢として覚えておくと良さそうです。

## VS Code と GitHub Copilot アプリ、どっちで使う？

ここまで読んで、「Canvas は GitHub Copilot アプリの話じゃなかったっけ？」と混乱した方もいるかもしれません。私も整理するまでごちゃっとしていました。

Canvas 拡張機能は **VS Code と GitHub Copilot アプリの両方でサポート**されています。使い分けの感覚はこんな感じです。

| 観点             | GitHub Copilot アプリ                                          | VS Code（1.142〜）                                                |
| ---------------- | -------------------------------------------------------------- | ----------------------------------------------------------------- |
| 得意な場面       | 既存の公式・コミュニティ Canvas をそのまま使う                 | 今書いているコードと同じ場所で、開発支援用の画面を使う・作る      |
| Canvas の入手    | Customize > Canvas / Plugins からインストール                 | `/create-canvas` で作る、またはアプリで入れたプラグインを呼び出す |
| 表示場所         | 右サイドパネル                                                 | エディタのタブ（Agents ウィンドウでは Add Tab > Canvas）          |
| 例               | Azure のコスト分析、リソース検索、Functions の進捗             | コードのデバッグ状況、タスクのカンバン、リリースチェックリスト    |

VS Code の公式ドキュメントでも、**既存の Canvas を使いたいなら、まず GitHub Copilot アプリで Canvas 拡張入りのチャットプラグインをインストールし、VS Code に戻ってエージェントに「使える Canvas を一覧して、1つ開いて」と頼む**流れが案内されています。

使い分けは次のとおりです。

- 📊 **既製品を使いたい** → Copilot アプリでプラグインを入れる（VS Code から呼び出すこともできる）
- 💻 **自分のプロジェクト専用の画面が欲しい** → VS Code で `/create-canvas`

私は後者で、記事用のカンバンを作りました。

## 活用アイデア

awesome-copilot の学習ハブには、`/create-canvas` のプロンプト例がいくつか載っています。「アクション名を明示する」のが書き方のコツです。

```text
/create-canvas Create an issue triage canvas with list filtering, label editing, and quick-priority actions. Add capabilities for get_issues, update_priority, and apply_label.
```

```text
/create-canvas Create a release checklist canvas that tracks milestones and owners. Add capabilities for add_item, assign_owner, mark_done, and export_summary.
```

日本語で書いても作れるので、私なら次のあたりを試したいです。

- **記事・登壇資料の進捗ボード**（さっきのデモの発展形）
- **Gh-CUG のイベント準備チェックリスト**（担当者・期限つき）
- **Azure の調査結果ボード**（「確認済み」「要確認」をカードで管理）

あと、作ったあとの育て方も大事です。学習ハブでは「最初の `/create-canvas` の結果は version 1 と考えて、使いながら摩擦を見つけて、アクションを足したり減らしたりする」ことが推奨されています。**破壊的な操作には承認ステップを入れておく**のも忘れずに。

## ハマりそうなポイント

### Q: 設定を ON にしたのに Canvas が出ない

**A**: 次の4つを順番に確認してください。

1. 設定変更後に **新しいセッション** を作ったか
2. ハーネスが **Copilot** になっているか（Local や Claude / Codex では動きません）
3. エディタウィンドウでは **最初のメッセージを送ったあと** にメニューが出ること
4. **WSL や SSH などのリモート接続で使っていないか**（私はこれでタブが出ませんでした。公式ドキュメントでもリモートセッションは非対応です）

タブで開けなくても、自作の Canvas 拡張がローカルサーバーを立てている場合は、その URL を内蔵ブラウザで開けば画面だけは触れます。あくまで回避策ですが、動作確認には使えました。

### Q: `/create-canvas` が候補に出ない

**A**: ドキュメントには「`/create-canvas` スキルが利用可能なとき」とあるので、まずは VS Code を最新（1.142 以降）にして、新しいセッションで試してみてください。

### Q: Canvas の状態は残る？

**A**: 学習ハブによると、状態の保存先は拡張機能の作り次第です。そのセッションだけでよければセッション用のパス、複数セッションをまたいで残したいなら拡張機能用のパスに保存する、という使い分けが推奨されています。今回の記事ボードは、リポジトリ内の `artifacts/board.json` に保存する形で作ってもらいました。

## まとめ

この記事では、VS Code 1.142 で入った Canvases について整理しました。

- Canvases は、**チャットの横でエージェントと同じ成果物を直接触れる**共有画面（Preview）
- 有効化は `chat.canvases.enabled` を ON → **新規セッション**で `/create-canvas`
- 動くのは **デスクトップ版 × Copilot ハーネス × ローカルセッション** だけ
- 海外では「prompting から co-editing へ」という評価。Azure 向けや遊び心のある拡張もすでに公開されている
- 既製品は Copilot アプリ経由、プロジェクト専用の画面は VS Code で `/create-canvas`、という使い分けがしっくりきそう
- 実際に記事用カンバンを作ってみたら、**人が手で足したカードも、エージェントが説明なしで読み取ってくれた**（ただし WSL などのリモート接続ではタブで開けなかった）

個人的には、「チャットのログに埋もれていた状態を、ちゃんと目に見える場所に置ける」のが一番の価値だと思いました。まだ Preview なので、今後の変化も追いかけていきます！

---

## 📣 GitHub Copilot User Group Japan（Gh-CUG）のお知らせ

ここまで読んでくれた方へ、ちょっとだけ宣伝させてください！

私が運営に参加している **GitHub Copilot User Group Japan（Gh-CUG / ジーカグ）** は、「もっと世の中に GitHub Copilot を広げたい！」という思いから生まれたユーザーコミュニティです。

モットーは **「なんでもは知らない、しってることだけ」**。完璧な知見もすごい実績もいりません。「こんなんできた！」「ここでつまずいた！」を持ち寄って、みんなでゆるく楽しく学ぶ場です。学生・初心者・ノンデベロッパーの方も大歓迎です！

| シリーズ           | スタイル         | 雰囲気                   |
| ------------------ | ---------------- | ------------------------ |
| 🌙 ゆるよな Gh-CUG | オンライン（夜） | ゆるふわ。ふらっと参加OK |
| 🔥 Gh-CUG Night    | オンライン       | 実践的な知見をがっつり   |
| 🤝 Gh-CUG Meetup   | オフライン       | リアルでワイワイ交流     |

今回の Canvases のような「出たばかりの新機能を触ってみた」話は、コミュニティでもよく盛り上がります。「こんな Canvas 作ってみた！」という話もお待ちしています！

🔗 **Connpass グループページ：** [GitHub Copilot User Group Japan](https://gh-cug.connpass.com/)

公式ハッシュタグは **#GhCUG** です。

## 参考

**公式**

- [Visual Studio Code 1.142 - Canvases (Preview)](https://code.visualstudio.com/updates/v1_142#_canvases-preview)
- [VS Code Docs - Use canvases with the Copilot harness](https://code.visualstudio.com/docs/agents/run/agent-harnesses#_use-canvases-with-the-copilot-harness)
- [Working with canvas extensions in the GitHub Copilot app（GitHub Docs）](https://docs.github.com/en/copilot/how-tos/github-copilot-app/working-with-canvas-extensions)
- [How canvases make agentic workflows visible, steerable, and cost-efficient（GitHub Blog）](https://github.blog/ai-and-ml/github-copilot/how-canvases-make-agentic-workflows-visible-steerable-and-cost-efficient/)
- [Build with Azure Canvases: a shared workspace for agents（Microsoft Developer Blog）](https://developer.microsoft.com/blog/azure-canvases/)
- [Build Azure canvases with the Canvas authoring plugin（Microsoft Developer Blog）](https://developer.microsoft.com/blog/build-azure-canvases-with-canvas-authoring/)

**コミュニティ・海外記事**

- [Working with Canvas Extensions（awesome-copilot Learning Hub）](https://awesome-copilot.github.com/learning-hub/working-with-canvas-extensions/)
- [Community Canvas Extensions（awesome-copilot）](https://awesome-copilot.github.com/extensions/)
- [VS Code 1.142 Brings AI Canvases, Tighter Agent Controls and a New Model Picker（Visual Studio Magazine）](https://visualstudiomagazine.com/articles/2026/10/15/vs-code-1,-d-,142-brings-ai-canvases-tighter-agent-controls-and-a-new-model-picker.aspx)
- [VS Code 1.142: Copilot Canvases, Portable Chats, Harness Mandate（byteiota）](https://byteiota.com/vs-code-1-142-copilot-canvases-portable-chats-harness-mandate/)
- [VSCode 1.142 - Canvases bring interactive workspaces to agent workflows（The Black Cloud）](https://theblackcloud.tech/blog/vscode1.142canvasespreview/)
