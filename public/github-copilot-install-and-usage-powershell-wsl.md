---
title: "【入門】GitHub Copilot CLIとは？PowerShellとWSLどちらでもできるインストール・使い方完全ガイド"
tags:
  - GitHubCopilot
  - CopilotCLI
  - PowerShell
  - WSL
  - AI
---

## はじめに

この記事では、ターミナルから直接AIエージェントを呼び出せる **GitHub Copilot CLI** の概要から、**PowerShell（Windows）** と **WSL（Ubuntu）** それぞれの環境でのインストール・認証・実際の使い方までを丁寧に解説します。

GitHub Copilot CLI はターミナルで `copilot` とタイプするだけで起動する対話型AIエージェントです。コードの変更・ファイル作成・シェルコマンドの実行・GitHubへのPR作成まで、自然言語で指示するだけで自律的にこなしてくれます。

この記事を読むと、以下のことができるようになります：

- ✅ GitHub Copilot CLIが何者かを理解できる
- ✅ PowerShell（Windows）環境でセットアップできる
- ✅ WSL（Ubuntu）環境でセットアップできる
- ✅ 対話モードとプログラムモードを使いこなせる
- ✅ スラッシュコマンドで高度な操作ができる

## 環境・前提条件

| 項目                 | バージョン・条件                                    |
| -------------------- | --------------------------------------------------- |
| OS                   | Windows 11（PowerShell v6以降 / WSL2 Ubuntu 22.04） |
| Node.js              | v22以上（npmインストールの場合）                    |
| GitHubアカウント     | 要サインアップ                                      |
| GitHub Copilotプラン | 無料枠 or 有料プラン（要有効化）                    |

:::note info
💡 **GitHub Copilotの無料枠について**
GitHubアカウントがあれば月2,000回のコード補完と50回のChatリクエストが**無料**で使えます。Copilot CLIの利用はプレミアムリクエストとして消費されます。クレジットカード登録不要です。
:::

:::note warn
⚠️ **`gh copilot suggest` との違い**
以前存在した `gh extension install github/gh-copilot`（`gh copilot suggest/explain`）は**廃止済み（deprecated）**です。この記事で紹介するのは、これとは全く別の新しいスタンドアロンツール「GitHub Copilot CLI」です。
:::

---

## GitHub Copilot CLIとは？

**GitHub Copilot CLI** は、ターミナルで `copilot` と入力するだけで起動する**自律型AIエージェント**です。GitHub CLIの拡張機能ではなく、**独立したツール**として提供されています。

チャット形式でAIに指示を出すと、AIが自律的にファイルを読み書きし、シェルコマンドを実行して、タスクを完了します。

### 何ができるの？

| カテゴリ             | できること                                                            |
| -------------------- | --------------------------------------------------------------------- |
| **コード変更**       | 「H1のCSSをダークブルーに変えて」→ 対象ファイルを探して変更してくれる |
| **新機能実装**       | 自然言語で仕様を伝えると、コードを書いてくれる                        |
| **デバッグ**         | エラーを貼り付けると原因を調査して修正してくれる                      |
| **Git操作**          | 「変更をコミットして」「最後のコミットを元に戻して」                  |
| **GitHub操作**       | PRの作成・マージ・クローズ、Issue作成、コードレビューリクエスト       |
| **ドキュメント更新** | READMEを改善・日本語化するなど                                        |
| **テスト生成**       | 既存コードのユニットテストを書く                                      |

### 対応OS

- Linux
- macOS
- **Windows PowerShell（v6以降）**
- **WSL（Windows Subsystem for Linux）**

---

## インストール手順

GitHub Copilot CLIは複数の方法でインストールできます。環境に合わせて選んでください。

### PowerShell（Windows）でのセットアップ

#### 方法A：WinGetでインストール（おすすめ）

PowerShellを開いて実行します：

```powershell
winget install GitHub.Copilot
```

インストール後、PowerShellを再起動してバージョンを確認します：

```powershell
copilot --version
```

#### 方法B：npmでインストール

Node.js v22以上がインストールされている場合：

```powershell
npm install -g @github/copilot
```

:::note info
💡 **Node.jsがない場合**

```powershell
winget install OpenJS.NodeJS.LTS
```

でインストールしてから再度実行してください。
:::

#### 認証

プロジェクトのディレクトリに移動して `copilot` を起動します：

```powershell
cd C:\Users\yourname\projects\my-app
copilot
```

初回起動時に `/login` スラッシュコマンドで認証するよう促されます：

```
> /login
```

ブラウザが開いてGitHub認証が行われます。認証完了後ターミナルに戻るとCopilotが使えるようになります。

---

### WSL（Ubuntu）でのセットアップ

#### Step 1：WSL2の確認（まだWSLを使っていない場合）

PowerShellで確認します：

```powershell
wsl --list --verbose
```

```
  NAME      STATE           VERSION
* Ubuntu    Running         2
```

未インストールの場合：

```powershell
wsl --install
```

:::note warn
⚠️ VERSION が `1` の場合はWSL2に変換してください：

```powershell
wsl --set-version Ubuntu 2
```

:::

#### Step 2：Copilot CLIをインストール

WSLのターミナルで実行します。

**方法A：インストールスクリプト（おすすめ）**

```bash
curl -fsSL https://gh.io/copilot-install | bash
```

**方法B：Homebrewがある場合**

```bash
brew install copilot-cli
```

**方法C：npmがある場合**

```bash
npm install -g @github/copilot
```

インストール後、バージョン確認：

```bash
copilot --version
```

#### Step 3：認証（WSL）

WSLターミナルでプロジェクトディレクトリに移動して起動します：

```bash
cd ~/projects/my-app
copilot
```

```
> /login
```

WSL2環境ではWindowsのブラウザが自動的に開いて認証できます。ブラウザが開かない場合はターミナルに表示されるURLをWindowsブラウザで手動アクセスしてください。

---

## 実際の使い方

### 使い方①：対話モード（基本）

プロジェクトのディレクトリで `copilot` を起動するだけです。あとは日本語で話しかけます：

```
> src/app.js のバグを探して修正してほしい
```

Copilotがファイルを読み込み、問題を見つけて修正案を提示し、承認すると実際にファイルを書き換えます。

**モード切り替え：** `Shift + Tab` を押すと「ask/executeモード」と「planモード」を切り替えられます。

| モード                              | 説明                                               |
| ----------------------------------- | -------------------------------------------------- |
| **ask/executeモード**（デフォルト） | 即座に実行                                         |
| **planモード**                      | 実行前に計画を立てて確認を求める。複雑な作業に向く |

---

### 使い方②：ツール実行の承認

Copilotがファイル変更やコマンド実行をしようとすると、確認を求めてきます：

```
Copilot wants to run: npm test

1. Yes
2. Yes, and approve for the rest of the session
3. No, and tell Copilot what to do differently (Esc)
```

| 選択肢       | 意味                     |
| ------------ | ------------------------ |
| **1（Yes）** | この1回だけ許可          |
| **2**        | セッション中はずっと許可 |
| **3（Esc）** | 拒否して別の方法を指示   |

:::note warn
⚠️ `--allow-all-tools` オプションを使うと確認なしですべてのコマンドを実行します。信頼できるプロジェクトディレクトリでのみ使用してください。
:::

---

### 使い方③：プログラムモード（ワンライナー）

対話なしで1つのタスクを実行させることもできます：

```bash
# gitコマンドを許可して今週のコミットを要約させる
copilot -p "今週のコミットを一覧して要約してほしい" --allow-tool='shell(git)'

# ファイル書き込みを許可してREADMEを翻訳させる
copilot -p "READMEを日本語に翻訳して" --allow-tool='write'
```

スクリプトと組み合わせることも可能です：

```bash
echo "テストが通ったらコミットしてPRを作成して" | copilot --allow-all-tools
```

---

### 使い方④：よく使うスラッシュコマンド

対話セッション中に使えるスラッシュコマンドです：

| コマンド     | 説明                                       |
| ------------ | ------------------------------------------ |
| `/login`     | GitHubアカウントで認証                     |
| `/model`     | 使用するAIモデルを変更                     |
| `/compact`   | 会話履歴を手動で圧縮（長いセッション時に） |
| `/context`   | 現在のトークン使用量を確認                 |
| `/pr`        | PRの表示・作成・修正・マージ・クローズ     |
| `/fleet`     | 複数ステップのタスクを高速化               |
| `/chronicle` | 過去のセッション履歴を参照・再開           |
| `/feedback`  | フィードバックの送信・バグレポート         |
| `/mcp`       | MCPサーバーの状態確認                      |

---

### 使い方⑤：GitHub操作の例

Copilot CLIはGitHub.comとも連携できます：

```
> 自分のオープンなPRを一覧してほしい
> OWNER/REPOで自分にアサインされているIssueを全部出して
> このIssueに取り組んで: https://github.com/owner/repo/issues/1234
> 変更をコミットしてPRを作成して
> PR#57のコードをレビューしてバグを報告してほしい
```

---

### 使い方⑥：ツール許可のカスタマイズ

特定のコマンドだけ自動許可・拒否したい場合：

```bash
# git pushとrmだけ禁止して他は自動許可
copilot --allow-all-tools --deny-tool='shell(rm)' --deny-tool='shell(git push)'

# ファイル書き込みだけ自動許可
copilot --allow-tool='write'

# shellのgitコマンドだけ自動許可
copilot --allow-tool='shell(git)'
```

---

## PowerShell vs WSL：どちらを使うべき？

| 観点                           | PowerShell              | WSL（Ubuntu）       |
| ------------------------------ | ----------------------- | ------------------- |
| **インストールの手軽さ**       | ◎ `winget install` 一発 | ○ スクリプト or npm |
| **Windowsアプリとの連携**      | ◎                       | △                   |
| **Linux系ツール（git/npm等）** | ○                       | ◎ ネイティブ        |
| **Dockerとの相性**             | ○                       | ◎                   |
| **本番Linuxサーバーとの一致**  | △                       | ◎                   |
| **PowerShell v6の要件**        | 必須                    | 不要                |

:::note info
💡 **どちらを選ぶか**
Windows向け開発なら **PowerShell**、Linux/Dockerが絡む開発なら **WSL** を選ぶと、Copilotが実行するコマンドが環境にマッチします。どちらでも機能は同じです。
:::

---

## トラブルシューティング

### Q：`copilot` コマンドが見つからない

インストールが正常に完了しているか確認します：

```powershell
# PowerShell
where.exe copilot
```

```bash
# WSL/Bash
which copilot
```

見つからない場合はシェルを再起動するか、`npm install -g @github/copilot` で再インストールしてください。

---

### Q：`/login` でブラウザが開かない（WSL）

WSL2ではWindowsのブラウザが自動的に開きます。開かない場合はターミナルに表示されるURLをWindowsブラウザで手動アクセスしてください。

代替として、Personal Access Token（PAT）で認証する方法もあります：

```bash
export COPILOT_GITHUB_TOKEN="your_pat_here"
```

PATはGitHub Settings > Developer settings > Personal access tokens で「Copilot requests」権限を付けて生成してください。

---

### Q：信頼するディレクトリの確認が毎回出る

初回起動時にディレクトリを信頼するか聞かれます。設定詳細は対話セッション内で `copilot help config` を実行してください。

---

### Q：VPN環境でエラーになる

一部の企業VPNではGitHub APIがブロックされることがあります。IT管理者に `*.github.com` および `*.githubcopilot.com` への通信許可を申請してください。

---

### Q：プレミアムリクエストを節約したい

Copilot CLIはプレミアムリクエストを消費します（デフォルトモデルは Claude Sonnet 4.5 / 1倍消費）。`/model` コマンドで消費量の少ないモデルに変更できます。

---

## まとめ

| ポイント                   | 内容                                                                                   |
| -------------------------- | -------------------------------------------------------------------------------------- |
| **GitHub Copilot CLIとは** | ターミナルで動く自律型AIエージェント。ファイル変更・コマンド実行・GitHub操作までこなす |
| **起動方法**               | プロジェクトディレクトリで `copilot` と入力するだけ                                    |
| **PowerShellインストール** | `winget install GitHub.Copilot`                                                        |
| **WSLインストール**        | `curl -fsSL https://gh.io/copilot-install \| bash`                                     |
| **認証**                   | 初回起動後 `/login` で認証                                                             |
| **2つのモード**            | 対話モード（`copilot`）/ プログラムモード（`copilot -p "..."` ）                       |
| **安全に使う**             | ツール実行の承認プロンプトをよく確認する                                               |

VS CodeのCopilot Chatと違い、ターミナルから離れることなくコードの変更からGitHubへのPR作成まで一気通貫で行えるのが最大の魅力です。ぜひプロジェクトディレクトリで `copilot` と入力してみてください。

---

## 参考リンク

- [GitHub Copilot CLI について（公式ドキュメント）](https://docs.github.com/ja/copilot/concepts/agents/about-copilot-cli)
- [GitHub Copilot CLI のインストール](https://docs.github.com/ja/copilot/how-tos/set-up/install-copilot-cli)
- [GitHub Copilot CLI の使用](https://docs.github.com/ja/copilot/how-tos/copilot-cli/use-copilot-cli)
- [copilot-cli リリース一覧（GitHub）](https://github.com/github/copilot-cli/releases/)
