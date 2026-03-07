---
title: GitHub Copilot のカスタムAgentを4つ連携させてQiita記事生成を半自動化した話
tags:
  - AI
  - VSCode
  - 個人開発
  - 生産性向上
  - GitHubCopilot
private: false
updated_at: '2026-03-08T06:28:31+09:00'
id: b978e6f5338960b2a9ee
organization_url_name: null
slide: false
ignorePublish: false
---

## はじめに

「Qiita記事を書くたびにリサーチ・コード作成・レビューを全部自分でやるのが面倒」

そう思って、GitHub Copilotのカスタムエージェント（`.agent.md`）とSkill（`SKILL.md`）を使って**Qiita記事執筆を半自動化するシステム**を作りました。トピックを伝えるだけで、リサーチ・コード作成・レビューまで4つのエージェントが連携して記事を仕上げてくれます。

書いた記事はGitHubにpushするだけでQiitaに自動公開される仕組みも整えたので、その全容を紹介します。

### この記事でわかること

- ✅ Custom Agent（`.agent.md`）とSkill（`SKILL.md`）の違いと使い分け
- ✅ 複数エージェントを連携させる「コーディネーターパターン」
- ✅ 実際に作ったQiita記事自動生成システムの構成
- ✅ つまずきやすいポイントと注意点

---

## VS Code Copilotカスタマイズの全体像

まず「何が作れるか」を整理します。4種類あります。

| 種類 | ファイル名 | 役割 | 使い時 |
|------|-----------|------|--------|
| **Custom Agent** | `*.agent.md` | 専門ペルソナを持つAI | 繰り返す専門タスク |
| **Skill** | `SKILL.md` | 手順書＋スクリプトのセット | 複雑な手順を再利用 |
| **Instructions** | `*.instructions.md` | 常時適用のルール | コーディング規約など |
| **Prompt** | `*.prompt.md` | 一回限りのタスク | 決まったフォーマットで出力 |

**一言で言うと：**
- 「常にこのルールで動いてほしい」→ Instructions
- 「この役割のAIをいつでも呼び出したい」→ Agent
- 「この手順をいつでも再実行したい」→ Skill
- 「このフォーマットで一回出力してほしい」→ Prompt

---

## Custom Agent（`.agent.md`）とは

```
.github/agents/
├── my-reviewer.agent.md   ← ワークスペーススコープ
└── my-coder.agent.md
```

VS Code 1.106以降の正式機能です（旧称 `.chatmode.md` から名称変更）。

### 最小構成

```markdown
---
description: "セキュリティ観点のコードレビュー専門エージェント。Use for: セキュリティレビュー、脆弱性チェック、OWASP確認。"
tools: [read, search]
---

あなたはセキュリティエンジニアです。OWASPトップ10の観点でコードをレビューします。
```

### フル構成（使えるプロパティ一覧）

```yaml
---
name: セキュリティレビューアー          # 省略するとファイル名が使われる
description: "説明文"                  # 必須・エージェントピッカーに表示される
tools: [read, search, edit, execute]  # 使えるツールを制限
model: 'gpt-4o'                       # VS Codeのモデルピッカーに表示される識別子を指定
user-invocable: true                  # false = ピッカー非表示（サブエージェント専用にする場合）
disable-model-invocation: true        # true = 他エージェントからの自動呼び出しを禁止
agents: ['sub-agent-a']               # 使えるサブエージェントを限定（tools に agent も必要）
---
```

### 使えるtoolsの主な値

| エイリアス | できること |
|-----------|-----------|
| `read` | ファイル読み取り |
| `edit` | ファイル編集 |
| `search` | ワークスペース検索 |
| `execute` | ターミナルコマンド実行 |
| `web` | Webページ取得 |
| `agent` | サブエージェントの呼び出し |
| `todo` | タスクリスト管理 |

:::note warn
⚠️ **`infer` プロパティは deprecated**：古い記事やサンプルで見かける `infer: true/false` は廃止されました。現在は `user-invocable` と `disable-model-invocation` の2つに分離されています。
:::

---

## Skill（`SKILL.md`）とは

```
.github/skills/
└── qiita-article/
    ├── SKILL.md              ← 必須・フォルダ名と name が一致すること
    ├── assets/
    │   └── article-template.md
    └── references/
        └── qiita-format.md
```

Skillは「手順書＋関連ファイルのパッケージ」です。

```yaml
---
name: qiita-article                   # フォルダ名と一致させる（必須）
description: 'Qiita記事を作成するスキル。Use for: 記事を書く、Qiita投稿、技術ブログ。'
argument-hint: '記事のトピックを入力'
---

# Qiita記事作成の手順

## 手順
1. トピックを確認する
2. [記事テンプレート](./assets/article-template.md) を使って構成を決める
...
```

### AgentとSkillの使い分け

| | Agent | Skill |
|---|---|---|
| 呼び出し方 | エージェントピッカーで選択 | `/スキル名` or 自動検出 |
| 持続性 | セッション中ずっと同じペルソナ | 必要なときだけ読み込み |
| 付随するファイル | なし | スクリプト・テンプレートを同梱できる |
| オープンスタンダード | なし | あり（Claude・Copilot CLIでも使える） |

---

## 実際に作ったシステム：Qiita記事自動生成

コーディネーターエージェントが3つの専門エージェントを指揮する構成です。

```
ユーザー
  ↓ トピックを伝える
qiita-writer（コーディネーター）
  ├─► qiita-researcher（リサーチ専門）
  ├─► qiita-coder（コード例作成専門）
  └─► qiita-reviewer（レビュー専門）
        ↓ 完成記事を
  Qiita-github/public/ に保存
        ↓ git push
  GitHub Actions
        ↓ 自動実行
  Qiitaに公開 🎉
```

### ディレクトリ構成

```
quita-agent/
├── .github/
│   ├── agents/
│   │   ├── qiita-writer.agent.md     ← コーディネーター
│   │   ├── qiita-researcher.agent.md ← リサーチ専門
│   │   ├── qiita-coder.agent.md      ← コード作成専門
│   │   └── qiita-reviewer.agent.md   ← レビュー専門
│   └── skills/
│       └── qiita-article/
│           ├── SKILL.md
│           ├── assets/article-template.md
│           └── references/qiita-format.md
└── Qiita-github/                     ← 記事公開リポジトリ
    ├── public/                       ← 記事.mdを置く場所
    └── .github/workflows/publish.yml ← GitHub Actions
```

### コーディネーターエージェント（qiita-writer）

```markdown
---
description: "Qiita記事作成の総合エージェント。Use for: 記事を書く、Qiitaに投稿したい。"
tools: [read, edit, search, web, agent, todo]
---

あなたはQiita記事作成の総合プロデューサーです。

## 作業フロー
1. トピック確認
2. qiita-researcher に調査を依頼
3. 記事構成を作成
4. qiita-coder にコード例を依頼
5. 記事を執筆（#skill:qiita-article を参照）
6. qiita-reviewer にレビューを依頼
7. Qiita-github/public/<slug>.md に保存
```

### 専門エージェントの設計

専門エージェントは「コーディネーターから呼ばれる」だけでなく、「直接使いたい」場面もあるため `user-invocable: true` にしています。

```yaml
---
description: "Qiita記事のリサーチ専門。技術背景・最新動向・参考リンクを調査する。"
tools: [web, search, read]
user-invocable: true    # ピッカーに表示 → 直接呼び出しもできる
---
```

コーディネーターからしか使わない完全サブエージェント専用にする場合は `user-invocable: false` にします。

```yaml
---
description: "内部専用のリサーチエージェント。"
tools: [web, search, read]
user-invocable: false   # ピッカー非表示・サブエージェントとしてのみ呼び出し可
---
```

### description が「発見の鍵」

コーディネーターがサブエージェントを呼び出す判断は**description の文章**で行われます。「このタスクにはどのエージェントを使うか」を決めるのがdescriptionです。

```yaml
# ❌ 悪い例（どんな時に使うか不明）
description: "便利なエージェント"

# ✅ 良い例（トリガーワードが明確）
description: "Qiita記事のリサーチ専門。Use for: 技術トピックの調査、最新動向の調査、背景情報収集。"
```

---

## つまずきポイント

### ① Skillのフォルダ名とnameを一致させる（必須）

```
.github/skills/qiita-article/   ← フォルダ名
                  └── SKILL.md
                       name: qiita-article  ← ここが一致しないと読み込まれない
```

### ② サブエージェントを使うには `agent` ツールも必要

```yaml
# ❌ agentsだけ書いてもサブエージェントは使えない
tools: [read, edit]
agents: ['my-sub-agent']

# ✅ tools に agent も含める
tools: [read, edit, agent]
agents: ['my-sub-agent']
```

### ③ サブエージェントは会話履歴を引き継がない

サブエージェントは独立したコンテキストウィンドウで動くため、`.instructions.md` の内容や会話の流れは渡されません。**タスクの指示は詳細に書いて渡す**必要があります。

---

## GitHub Actionsで自動公開する仕組み

Qiita CLIとGitHub Actionsを組み合わせると、pushするだけでQiitaに公開されます。

```yaml
# Qiita-github/.github/workflows/publish.yml
# ※ このファイルは Qiita-github/ リポジトリ内に置く
name: Publish articles
on:
  push:
    branches: [main]
  workflow_dispatch:
permissions:
  contents: write
jobs:
  publish_articles:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: increments/qiita-cli/actions/publish@v1
        with:
          qiita-token: ${{ secrets.QIITA_TOKEN }}
          root: "."  # Qiita-github/ リポジトリのルートを指す
```

**記事のフロントマター（Qiita CLI形式）：**

```markdown
---
title: "記事タイトル"
tags:
  - タグ1
private: false
updated_at: ''
id: null          ← 初回はnull、公開後にQiita記事IDが自動で入る
---
```

---

## 使い方のデモ

VS Code のチャットでエージェントを選択して話しかけるだけです。

```
【Qiita Writerを選択】

「VS Code Copilot Agentの自作について記事を書きたい。
 対象は中級者エンジニア。サンプルコード多めで。」

→ 自動でリサーチ・コード例作成・レビューが実行され、
  Qiita-github/public/vscode-copilot-agent.md に記事が保存される
```

---

## まとめ

- **Custom Agent**（`.agent.md`）は「専門ペルソナを持つAI」を定義する
- **Skill**（`SKILL.md`）は「手順書＋ファイルのパッケージ」
- コーディネーター＋ワーカーの**サブエージェントパターン**で複雑タスクを自動化できる
- descriptionの書き方が**発見の鍵**：トリガーワードを明確に書く
- `infer` は deprecated → `user-invocable` / `disable-model-invocation` を使う
- Qiita CLI + GitHub Actionsで**pushするだけの公開フロー**が作れる

Agent/Skillを作っておくと、同じ作業を何度でも再現できるのが最大のメリットです。ぜひ自分のワークフローに合わせてカスタマイズしてみてください。

## 参考

- [VS Code カスタムエージェント 公式ドキュメント](https://code.visualstudio.com/docs/copilot/customization/custom-agents)
- [VS Code エージェントスキル 公式ドキュメント](https://code.visualstudio.com/docs/copilot/customization/agent-skills)
- [VS Code Copilotカスタマイズ概要](https://code.visualstudio.com/docs/copilot/customization/overview)
- [サブエージェント（Experimental）](https://code.visualstudio.com/docs/copilot/agents/subagents)
- [Agent Skills オープンスタンダード](https://agentskills.io/)
- [Qiita CLI 公式](https://github.com/increments/qiita-cli)
