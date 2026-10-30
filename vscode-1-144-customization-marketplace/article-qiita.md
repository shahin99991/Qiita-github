---
title: VS Code 1.144：Customizations の新ホーム Browse と Copilot connectors。探す・つなぐ・整える・配るを整理する
tags:
  - VSCode
  - GitHubCopilot
  - MCP
  - AIエージェント
  - GitHub
private: false
updated_at: "2026-10-30T12:00:00+09:00"
id: null
organization_url_name: mspjp
slide: false
ignorePublish: false
posting_campaign_uuid: null
agreed_posting_campaign_term: false
---

<!--
【タイトル候補】
1. VS Code 1.144：Customizations の新ホーム Browse と Copilot connectors。探す・つなぐ・整える・配るを整理する
2. MCP の設定ファイルを書かずに Slack や Notion をつなぐ。VS Code 1.144 の Copilot connectors と Browse
3. 入れる前に何を見る？ VS Code 1.144 のマーケットプレイスと Copilot connectors を安全に使うための整理

【画像について】
- img-00 〜 img-05 は Gemini で生成した解説画像（generate_images.py）
- demo-* は実機スクリーンショット（2026/10/30 に撮影。個人情報はマスク済み）
- 撮れていない画面（MCP Servers ページの Connector 表示、共有リンクの確認ダイアログ）は画像なしで、ドキュメントの記述として書いている
- 画像の URL は https://raw.githubusercontent.com/shahin99991/Qiita-github/main/vscode-1-144-customization-marketplace/images/<ファイル名> で統一
- 同名のファイルを images/ に上書きして push すれば、記事側の URL は変更不要

【公開前チェック】
- images/ を push してから公開する（push 前は raw URL が 404）
- 許可画面・チャット画面のマスクが十分か、公開前にもう一度見る
-->

## はじめに

こんにちは！最新アプデの検証が趣味になってしまっているMicrosoft Student Ambassador/Github Copilot User Group Japan運営のロホマン シャヒンです！

:::note
この記事が少しでも参考になったら、**ぜひいいね・共有**をお願いします。
間違っている箇所や「ここが分かりにくかった」という指摘は、やさしくコメントいただけると助かります！
:::

2026年10月28日にGithubUniverseと同時にリリースされた **VS Code 1.144** は、Copilot Fusion や Cloud セッションの話題が先に出ていました。でも、毎日の使い心地に効いてくるのは、地味な「カスタマイズまわり」の変更かもしれません。リリースノートの Agent customizations には、こんな項目が並んでいます。

- **Browse**（Customizations の新しいホーム）で、GitHub Feed とプラグインのマーケットプレイスを横断して探せる（Preview）
- **Copilot connectors** で、Slack / Notion / Sentry / Postman / Work IQ などを、MCP の設定なしでつなげる（Preview）
- GitHub Copilot 向けのカスタムエージェント（`.agent.md`）で、`model` / `tools` / `skills` の補完・hover・検証が強くなった
- プラグインやカスタマイズの**共有リンク**（`vscode://` のディープリンク）と、チャットから使える `/plugin` `/mcp` `/skills`

この記事では、この4つを「**探す → つなぐ → 整える → 配る**」の順で整理します。公式ドキュメントと GitHub の changelog、海外の記事を読んだうえで、動かすときに迷いそうなところ（条件・設定・安全面）を中心にまとめました。

:::note warn
この記事は公式ドキュメントの内容をもとに、**自分の環境（VS Code 1.144）で実際に触った画面**を載せています。スクリーンショットで確認できたことは「私の環境では〜」と書き、確認できていないものはドキュメントの記述として区別しています。Browse も Copilot connectors も **Preview** なので、今後変わる可能性があります。
:::

## TL;DR

![VS Code 1.144 のカスタマイズ機能を、探す・つなぐ・整える・配るの4ステップで説明した概要図](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/vscode-1-144-customization-marketplace/images/img-00-tldr-overview.png)

**何が起きた？**
VS Code 1.144 で、Customizations の入口が **Browse** に変わり、スキル・プラグイン・MCP サーバー・コネクターを一か所から探して入れられるようになりました。外部サービスとの接続は、**Copilot connectors**（GitHub が管理する MCP サーバー）を使えば、ローカルのサーバー設定なしでつなげます。

**押さえておきたいポイント**

| 項目                          | 内容                                                                                                                                  |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| Browse の開き方               | ✅ コマンド `Chat: Open Customizations`、または `vscode://chat-customizations/open?page=discover`                                     |
| Browse のソース               | ✅ GitHub Feed / MCP Gallery / Copilot Connectors / 自分や組織が登録したプラグインマーケットプレイス                                  |
| GitHub Feed                   | ⚠️ Local セッションでは使えない（対応ハーネスが必要）                                                                                 |
| Copilot connectors            | ⚠️ Preview。Copilot ハーネスのみ。全プランで既定オンだが、Business / Enterprise は管理者が Editor preview features を有効にする       |
| コネクターの接続              | ✅ Connect → ブラウザで許可。同じアカウントでサインインした対応クライアントで使い回せる                                               |
| GitHub Actions 上のセッション | ❌ コネクターは未対応（Issue を Copilot に割り当てる場合など）                                                                        |
| カスタムエージェント編集      | ✅ `model` / `tools` / `skills` に補完・hover・検証。Copilot 固有の属性もチェックされる                                               |
| 共有リンク                    | ✅ マーケットプレイス追加・プラグインのインストール・Customizations のページを `vscode://` リンクで共有。実行前に確認ダイアログが出る |

**対象**: VS Code 1.144 以降（2026/10/28 リリース）。Copilot ハーネスでの利用が前提です。

## 探す：Browse は Customizations の新しいホーム

### 何がまとまったのか

これまで、スキル・プラグイン・MCP サーバーは、それぞれ別の画面や別の場所で探す必要がありました。1.144 では、Customizations の入口が **Browse** に変わり、探す場所が一つになっています。

![Browse が GitHub Feed、プラグインマーケットプレイス、Copilot Connectors を一つの入口にまとめていることを示した図](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/vscode-1-144-customization-marketplace/images/img-01-browse-map.png)

リリースノートによると、Browse には次のものが集まります。

- **GitHub Feed**: GitHub が用意している公開フィード
- **プラグインのマーケットプレイス**: 自分や組織（エンタープライズ）が登録したもの
- **Copilot Connectors**: 後述の外部サービス接続

私の環境でソースメニューを開くと、**All Sources / GitHub Feed / MCP Gallery / Copilot Connectors / `github/awesome-copilot#marketplace`** が並んでいました（GitHub Feed が出る条件は、少し下の注意書きにまとめました）。左のサイドバーには、Plugins・MCP Servers・Skills・Instructions・Agents・Hooks・Tools・Migrations といった種類別のページも並びます。

### 開いてみる

開き方は2通りあります。

- コマンドパレットで `Chat: Open Customizations`
- リンクから開く: `vscode://chat-customizations/open?page=discover`

コマンドパレットで `Chat: Open Customizations` と打つと、先頭に出てきます。`Chat: Configure Custom Agents...` や `Chat: New Custom Agent...` といった近いコマンドも一緒に並ぶので、迷いにくいです。

![コマンドパレットに「Chat: Open Customizations」と入力した画面。先頭の候補が赤枠で囲まれている](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/vscode-1-144-customization-marketplace/images/demo-00-open-customizations.png)

開くと、**Browse customizations** の画面が出ます。ソースが **All Sources** のときは、**Editor's picks**、**Plan, build, and ship**、**Connect your work** といった GitHub Feed のセクションに続けて、**Copilot Connectors**、**MCP Gallery**、**awesome-copilot** が縦に並びました。各行には、種類（Plugin / Skill / MCP server）と提供元（GitHub Feed / Copilot Connectors / MCP Gallery / awesome-copilot）が表示されます。

![Browse のホーム画面（All Sources）。Editor's picks から awesome-copilot まで、複数のソースが縦に並んでいる](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/vscode-1-144-customization-marketplace/images/demo-01-browse-home.png)

ソースを **GitHub Feed** に絞ると、Editor's picks と、用途別のセクションだけになります。

![ソースを GitHub Feed にした Browse。Azure DevOps Copilot Plugin や Figma MCP Server などが並んでいる](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/vscode-1-144-customization-marketplace/images/demo-01b-github-feed.png)

ソースメニューを開いた状態がこちらです。末尾の **Configure Marketplaces** から、自分のマーケットプレイスを足せます（次の節）。

![ソースメニューを開いた画面。All Sources、MCP Gallery、Copilot Connectors、github/awesome-copilot#marketplace、Configure Marketplaces が並んでいる](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/vscode-1-144-customization-marketplace/images/demo-02-source-menu.png)

:::note warn
この画面は、タイトルが **`Agent Customizations (Local · <ワークスペース名>)`** のときに撮ったものです。メニューに **GitHub Feed がありません**。一方、タイトルが **`Agent Customizations (Copilot)`** の画面（上の2枚）では GitHub Feed が選べました。ソースを GitHub Feed にしたまま、対応していないエージェントを選んでいると、一覧が空のまま「**GitHub Feed: The selected agent cannot retrieve curated customizations.**」という警告が右下に出ました。Browse の中身が空のときは、まず今どのハーネスを選んでいるかを見てください。
:::

### 絞り込みと共有リンク

リンクには検索語も付けられます。たとえば MCP サーバーだけに絞った状態で開くなら、次のようになります。

```text
vscode://chat-customizations/open?page=discover&search=%40type%3Amcp
```

`%40type%3Amcp` は `@type:mcp` をエンコードしたものです。検索欄には `@type:` で種類を指定する書き方があり、リリースノートには `@type:canvas` の例も載っていました。Canvases の記事にも出てくる種類です。

私の環境で `@type:canvas` と入れると、Azure DevOps Copilot Plugin、Microsoft Foundry Canvas、Jira Sprint Dashboard、Sentry Triage Plugin など、**Copilot の Canvas を使うプラグイン**が一覧になりました。そのときのソースは All Sources でした。

![検索欄に @type:canvas を入力した状態。Canvas を使うプラグインだけが一覧に出ている](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/vscode-1-144-customization-marketplace/images/demo-03-filter-type-canvas.png)

### 使う前に確認したい条件

| 項目                  | 内容                                                                                                                                                     |
| --------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ステータス            | Preview                                                                                                                                                  |
| 設定                  | `chat.customizations.marketplace.enabled`、GitHub Feed の公開フィードは `chat.customizations.marketplace.sources.publicFeed.enabled`（ドキュメント記載） |
| GitHub Feed           | 対応ハーネスが必要で、**Local セッションでは使えない**（私の環境でも、Local ではソースメニューに出ませんでした）                                         |
| Business / Enterprise | 管理者が Editor preview features を有効にする必要がある                                                                                                  |
| 提供元の範囲          | 利用可能なソースは、選んでいるハーネスと組織のポリシーで変わる                                                                                           |

### 自分のマーケットプレイスを足す

Browse のソースメニューから **Configure Marketplaces** を開き、**Add Marketplace** で GitHub リポジトリ・Git の URL・ローカルのリポジトリを指定します。マーケットプレイスは「プラグインの定義を入れた Git リポジトリ」です。登録しただけではインストールも有効化もされません。

settings.json に書くこともできます（実験的な設定です）。

```json:settings.json
{
  "chat.plugins.marketplaces": [
    "github/copilot-plugins",
    "your-org/plugin-marketplace#<コミットSHA>"
  ]
}
```

`#<ref>` でブランチやタグ、40文字のコミット SHA を固定できます。公式ドキュメントでは、**再現性が必要なら SHA を使う**よう書かれていました。ブランチやタグは、取得した時点の中身に解決されます。

`/plugin` 系のスラッシュコマンドや Copilot CLI でも同じことができますが、後で触れるとおり、画面側とコマンド側では管理している一覧が別になっています。

## 入れる前に確認したい4つのこと

マーケットプレイスは、探す手間が減るぶん、**何でも入れられる状態**にもなります。公式ドキュメントにも、プラグインには「あなたのマシンでコードを実行できるフックや MCP サーバーが含まれることがある」と明記されています。

![マーケットプレイスのプラグインやコネクターを入れる前の4つのチェック（公開元・同梱物・権限・ポリシー）](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/vscode-1-144-customization-marketplace/images/img-05-trust-checklist.png)

**1. 公開元（Publisher と Source）を見る**
詳細画面で、誰が公開していて、どのマーケットプレイスから来たのかを確認します。初めてのマーケットプレイスからインストールするときは、信頼確認のダイアログも出ます。

**2. 同梱物を見る**
プラグインの詳細には、含まれているカスタマイズ（スキル・MCP サーバー・フック・カスタムエージェントなど）と README が出ます。フックや MCP サーバーは、手元で実行されるものです。ここは省略しないほうがいいところです。

**3. 権限を見る**
コネクターは、接続のときにブラウザの許可画面が出ます。そこに出る権限の内容を読んでから承認します（実際の画面は、後の「接続の流れ」に載せました）。サービスによっては、管理者の承認が別途必要です。

**4. ポリシーを見る**
Business / Enterprise では、組織の設定が優先されます。組織が管理しているマーケットプレイスは削除できず、ポリシーで管理されているプラグインは有効・無効の切り替えもロックされます。

入れたあとの確認も、公式ドキュメントに手順があります。

1. Customizations の **Plugins** で、インストール済みで有効になっているかを見る
2. 公開元のセットアップ手順があれば完了させる（同梱の MCP サーバーは接続要件も確認）
3. **新しいセッション**で、使いたい対象のハーネスとワークスペースを選んで、必要な部品が見えるかを確認する
4. 小さなタスクを一つ試して、エージェントの動きと結果を見る

「入れたからエージェントが必ず使う」わけではない、とドキュメントにもあります。最後の「小さく試す」は、手を抜かないでおきたいところです。

## つなぐ：Copilot connectors

### MCP を自分で設定するのとの違い

Copilot connectors は、**GitHub が管理する MCP サーバー**です。Slack の議論、Notion のプロジェクト情報、Microsoft Learn のドキュメントといった外部の文脈を、エージェントのセッションに持ち込めます。

![MCP サーバーを自分で探して設定する手順と、Browse で Connect を押すだけの手順を左右で比較した図](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/vscode-1-144-customization-marketplace/images/img-02-connector-vs-mcp.png)

従来の MCP サーバーは、サーバーを探して、`mcp.json` に書いて、認証を設定して、使うクライアントごとに繰り返す必要がありました。コネクターは、リリースノートの説明では次のような流れです。

1. Browse を開く
2. ソースメニューで **Copilot Connectors** を選ぶ
3. つなぎたいサービスの **Connect** を押す
4. ブラウザで許可する

つないだあとは、**同じアカウントでサインインしている対応クライアント**で、同じ接続を使い回せます。

![一度つないだコネクターが、VS Code、Copilot CLI、Copilot アプリ、Copilot cloud、GitHub Mobile から使えることを示したハブ図](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/vscode-1-144-customization-marketplace/images/img-03-connect-once.png)

GitHub Docs には、対応しているクライアントとして **Copilot アプリ / Copilot CLI / VS Code / Copilot cloud** が挙がっていました。一方で、**GitHub Actions 上で動くセッション**（たとえば Issue を Copilot に割り当てて起動する場合）は未対応です。

### どんなサービスがあるのか

リリースノートのスクリーンショットには、Port / Postman / Sentry / Slack / Statsig / Work IQ が並んでいました。私の環境で Copilot Connectors を開くと、**Microsoft Learn Docs / Miro / Neon / Netlify / Notion / Port / Postman / Sentry / Slack / Statsig / Work IQ** が一覧に並び、All Sources のほうには Airtable / Amplitude / Apify / Atlassian Rovo も出ていました。どれも名前の横に青いチェックマークが付いていて、右側に **Connect** ボタンがあります（チェックマークの意味は、画面からは確認できていません）。

GitHub Docs の一覧では、ほかに Figma、Linear、Grafana Cloud、Azure Data Explorer などがあり、合計で26個ほどのコネクターが挙がっていました（数は今後変わると思います）。

Visual Studio Magazine も、Slack・Notion・Microsoft Learn を例に、コネクターの一覧画面を載せています。

### Install と Connect の違い

Browse を眺めていて気づいたのは、**同じサービスの入口が2つある**ことです。たとえば Work IQ は、GitHub Feed の「Connect your work」に **WorkIQ Tools for Microsoft 365**（Plugin、ボタンは **Install**）があり、Copilot Connectors には **Work IQ**（MCP server、ボタンは **Connect**）があります。Sentry も、GitHub Feed に **Sentry Triage Plugin**（Canvas でイシューを整理するプラグイン）、Copilot Connectors に **Sentry**（MCP server）があります。

![Connect your work のセクション。WorkIQ Tools for Microsoft 365 などの Plugin / MCP server に Install ボタンがあり、1つが赤枠で囲まれている](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/vscode-1-144-customization-marketplace/images/demo-04a-plugin-install-button.png)

プラグインの **Install** は、スキルやフック、MCP サーバーなどが入ったパッケージを手元に入れる操作です。コネクターの **Connect** は、GitHub が管理する MCP サーバーに、自分のアカウントでつなぐ操作です。中身が同じなのかどうかは、私は確認していません。入れる前に、詳細画面で同梱物を見てください。

### 使う前に確認したい条件

| 項目             | 内容                                                                                               |
| ---------------- | -------------------------------------------------------------------------------------------------- |
| ステータス       | Preview                                                                                            |
| ハーネス         | **Copilot ハーネスのみ**（ドキュメント記載。私の環境では Local 表示でも一覧と Connect ボタンは出ました）  |
| プラン           | 全 Copilot プランで既定オン。Business / Enterprise は管理者が Editor preview features を有効にする |
| 設定             | `chat.customizations.copilotConnectors.enabled`（ドキュメント記載）                                |
| 組織の制限       | 組織の MCP 制限が適用される。サービスによっては管理者の承認が必要                                  |
| 対応クライアント | Copilot アプリ / Copilot CLI / VS Code / Copilot cloud。GitHub Actions 上のセッションは未対応      |
| 接続の解除       | MCP Servers のページで `Connector:<サービス名>` を選んで **Disconnect**（Browse のボタンも Disconnect に変わる）                  |

### 接続の流れ

ここでは、私が実際に **Work IQ**（Microsoft 365 のメール・会議・ファイル・Teams を自然言語で検索できるコネクター）をつないだ流れを載せます。

**手順1: Browse でコネクターを開く**

`vscode://chat-customizations/open?page=discover` から Browse を開き、ソースメニューで **Copilot Connectors** を選びます。サービスの一覧と、それぞれの **Connect** ボタンが出ます。一覧の末尾に **Work IQ** がありました。

![Copilot Connectors の一覧の末尾。Slack、Statsig、Work IQ が並び、Work IQ の Connect ボタンが赤枠で囲まれている](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/vscode-1-144-customization-marketplace/images/demo-04-connectors-list.png)

**手順2: Connect して、ブラウザで許可する**

**Connect** を押すと、ブラウザが開きます。私の GitHub アカウントは、所属する Organization が、シングルサインオンによる認証を求めていたので、先に **Single sign-on to your organization** の画面が出ました。ここで **Authorize** を押して、組織への認証を済ませます（組織名は伏せています）。

![Single sign-on to your organization の画面。Organization の横にある Authorize ボタンが赤枠で囲まれている](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/vscode-1-144-customization-marketplace/images/demo-05a-sso.png)

次に出たのが、**Visual Studio Code is requesting additional permissions** の許可画面です。追加で求められているのは **Plugin gateway connections（Manage plugin gateway connections）** で、その下の **Existing access** には、すでに許可済みの権限（ユーザープロフィールの読み取り、プライベートリポジトリのフルコントロール、メールアドレスの読み取り、GitHub Actions ワークフローの更新）が並んでいます。末尾の「Authorizing will redirect to `https://vscode.dev`」も確認してから **Authorize Visual-Studio-Code** を押します。

![Visual Studio Code is requesting additional permissions の画面。Plugin gateway connections と Existing access、Authorize ボタンが見える](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/vscode-1-144-customization-marketplace/images/demo-05-connector-authorize.png)

:::note info
Existing access の一覧は、すでに許可済みの権限の表示だと読めます（画面の見出しからの推測です）。今回の操作で新しく増えるのは Plugin gateway connections です。それでも、権限の画面は「読み流さずに一度読む」習慣にしておくのが安全です。
:::

承認すると、**Work IQ connection has been created** と表示されます。補足として「Works across Copilot: the GitHub Copilot app, CLI, VS Code, and cloud agents.」とあり、前の節で触れた「つないだ接続を使い回せる」がそのまま書かれていました。

![Work IQ connection has been created と表示された完了画面](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/vscode-1-144-customization-marketplace/images/demo-05b-connection-created.png)

**手順3: 接続済みになったことを確認する**

VS Code に戻ると、Browse の Work IQ のボタンが **Connect** から **Disconnect** に変わっていました。

![接続後の Browse。Work IQ のボタンが Disconnect に変わり、赤枠で囲まれている](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/vscode-1-144-customization-marketplace/images/demo-06-connected.png)

ドキュメントには、MCP Servers のページにも `Connector:<サービス名>` として出ると書かれています。こちらは私の環境では画面を確認していません。

**手順4: 新しいセッションで小さなタスクを試す**

つないだサービスから読み取れる範囲のことだけを頼みます。たとえば Microsoft Learn Docs なら、次のような読み取り専用のプロンプトにします。

```text
Microsoft Learn Docs のコネクターを使って、Azure Functions の Flex Consumption プランの
スケール上限について公式ドキュメントで確認して。回答には参照した URL も付けて。
ファイルの編集やコマンドの実行はしないで。
```

私は Work IQ をつないだ直後なので、「WorkIQコネクタを接続したテストして」とだけ頼んでみました（モデルは Claude Haiku 4.5）。10ステップ・約2分で、SharePoint のファイル、Outlook のメール、Teams のチャット、カレンダーの予定を、それぞれ取得できたと報告されました。画像は、メールの件名や予定のタイトルを赤く塗りつぶしています。

![Work IQ コネクターのテストを頼んだチャット。SharePoint、Outlook、Teams、カレンダーがすべて正常と表示され、対応可能な操作の一覧が赤枠で囲まれている](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/vscode-1-144-customization-marketplace/images/demo-08-connector-in-chat.png)

ここで注意したい点が2つあります。

- **実際の自分のメールや予定が、そのままチャットに出てきます**。スクリーンショットを撮る、画面共有をする、といった場面では、写り込みに気をつけてください。
- 返答の「対応可能な操作」には「メール検索・読込・**送信**」とありました。これはモデルの説明で、私は送信までは試していません。読み取りだけで済ませたいときは、上のサンプルのように「編集や実行はしないで」とプロンプトで明示しておきます。

### コネクターと自前の MCP サーバーの使い分け

コネクターが増えたからといって、自前の MCP サーバーが不要になるわけではありません。私の整理は次のとおりです。

| 観点               | Copilot connectors                                       | 自前の MCP サーバー                           |
| ------------------ | -------------------------------------------------------- | --------------------------------------------- |
| セットアップ       | Browse で Connect                                        | `mcp.json` などに書く                         |
| 管理者             | GitHub                                                   | 自分（またはチーム）                          |
| 使えるクライアント | Copilot ハーネスの対応クライアント                       | 設定したクライアント（ハーネスによる）        |
| 対象サービス       | カタログにあるもの                                       | 何でも（社内システムなど）                    |
| 向いている場面     | Slack・Notion・Sentry など、定番サービスの文脈を足したい | 社内 API や、カタログにないサービスを使いたい |

「定番のサービスはコネクター、社内固有のものは自前の MCP」と分けておくと、設定の手間と管理の責任範囲が見通しやすいと思います。

## 整える：スラッシュコマンドとカスタムエージェント編集

### チャットから管理する `/plugin` `/mcp` `/skills`

Copilot ハーネスのセッションでは、画面を開かなくても、チャットの入力欄から管理できます。`/plugin`、`/mcp`、`/skills` のあとにスペースを入れると、使えるサブコマンドの補完が出ます。

| 対象               | コマンド                                                                            |
| ------------------ | ----------------------------------------------------------------------------------- |
| プラグイン         | `/plugin list` / `install` / `update` / `enable` / `disable` / `uninstall`          |
| マーケットプレイス | `/plugin marketplace list` / `browse <name>` / `add <source>` / `update` / `remove` |
| MCP サーバー       | `/mcp show <名前>` / `/mcp enable <名前>` / `/mcp disable <名前>`                   |
| スキル             | `/skills info <名前>`                                                               |

補完は、プラグイン・マーケットプレイス・サーバー・スキルの名前まで候補に出してくれます。使えるコマンドは Copilot のランタイムに依存して、結果はそのままチャットに表示されます。

:::note warn
⚠️ 公式ドキュメントには、**`/plugin` コマンドと Customizations エディタは、別のプラグイン一覧を使っている**と書かれています。どちらで入れたかを覚えておいて、同じ画面（コマンド）から管理するのが安全です。
:::

同名のプラグインが複数のマーケットプレイスにある場合は、`<plugin>@<marketplace>` という形式で指定します。

チャット欄に `/plugin` と入力すると、`disable` / `enable` / `install` / `list` / `marketplace` / `uninstall` / `update` の補完が、それぞれの説明つきで出ました。

![チャット入力欄に /plugin と入力した画面。disable、enable、install、list、marketplace、uninstall、update の補完候補が出ている](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/vscode-1-144-customization-marketplace/images/demo-09-slash-plugin.png)

`/plugin list` を実行すると、インストール済みのプラグインが **Installed plugins** として返ってきました。私の環境では `azure@awesome-copilot`（v1.2.97）が2行出ていました。理由は確認していません。

![/plugin list の実行結果。Installed plugins として azure@awesome-copilot が表示されている](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/vscode-1-144-customization-marketplace/images/demo-09b-plugin-list.png)

サブコマンドを付けずに入力の途中だと、`/plugins`（**Manage plugins**）のほか、自分のプロンプトファイル（`/LambdaMigration-...` のようなもの）もあいまい一致で候補に混ざります。補完は、ファイル名の一部でも拾ってくれる動きです。

![/plugin と入力した途中の補完。/plugins（Manage plugins）と、あいまい一致したプロンプトファイルの候補が並んでいる](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/vscode-1-144-customization-marketplace/images/demo-09c-slash-fuzzy.png)

### カスタムエージェントの編集が賢くなった

GitHub Copilot ハーネス向けの `.agent.md` を編集するとき、**補完・hover・検証**で、使えるモデル・ツール・スキルを選べるようになり、設定ミスも実行前に気づけるようになりました。

| 属性     | 補完・検証の内容                                                                                                     |
| -------- | -------------------------------------------------------------------------------------------------------------------- |
| `model`  | Copilot のモデル ID が候補に出る。**1つの値**でも、**優先順のリスト**でも書ける                                      |
| `tools`  | `read` / `edit` / `execute` などの Copilot のツールエイリアスと、拡張機能のツールが候補に出る                        |
| `skills` | 使えるスキルが、説明とソースの情報つきで補完・hover に出る                                                           |
| そのほか | フックやエージェント専用の MCP サーバーなど、Copilot 固有の属性と入れ子の構造にも補完・hover・検証がある             |
| 本文     | プレースホルダーが認識されて hover が出る。不明なプレースホルダーや、Local 専用の `#tool:` `#file:` 参照は警告される |

たとえば、こんな形のファイルです。モデル ID は、実際の補完候補から選んでください。

```markdown:.github/agents/doc-reviewer.agent.md
---
name: doc-reviewer
description: ドキュメントの変更をレビューして、古い記述と抜けを指摘する
model: ["<優先するモデルID>", "<フォールバックのモデルID>"]
tools: ["read", "edit"]
skills: ["<使いたいスキル名>"]
---

変更されたドキュメントを読んで、次の3点を確認してください。
1. 古くなった記述
2. 手順の抜け
3. リンク切れ
```

細かいところですが、リリースノートに書かれている挙動で、いいなと思った点が2つあります。

**不明なモデル・ツール・スキルの警告は、探索が終わってから**出ます。インベントリの読み込み中に、正しい値が一瞬エラー扱いになることを避けるためです。

**`target` がなければ、いま選んでいるハーネスに合わせて**補完・hover・診断が出ます。ハーネスを切り替えると、ファイルを開き直さなくてもガイダンスが更新されます。`target: vscode` や `target: github-copilot` を明示すれば、そちらが優先されます。

公式ドキュメントでは、ハーネスによって使える属性が分かれていました。

| 項目                                    | Copilot ハーネス | Local ハーネス |
| --------------------------------------- | ---------------- | -------------- |
| `skills` / `mcp-servers`                | 使える           | 使えない       |
| `handoffs` / `agents` / `argument-hint` | 使えない         | 使える         |

どの属性がどのハーネスで効くかは、書く前に確認しておくと手戻りが減ります。変換のときに、`model-policy` や `mcp-servers` などが転送されないという記述もありました。

### 実際に `.agent.md` を編集してみた

私の環境の `.github/agents/doc-reviewer.agent.md` で試しました。`model:` `tools:` `skills:` を値なしで書くと、3つとも赤い波線が付き、`tools:` の上には **Configure Tools...** のリンクが出ました。

![doc-reviewer.agent.md のフロントマター。model、tools、skills が空で、赤い波線が付いている。tools の上に Configure Tools... が出ている](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/vscode-1-144-customization-marketplace/images/demo-10a-agent-empty.png)

`model:` の続きを打つと、グレーの**インライン提案**で `gpt-4` が出ました（Tab で確定、Ctrl + → で1語ずつ）。`skills:` の側にも `doc-reviewing` というグレーの提案が出ています。

![model: の行に gpt-4 というグレーのインライン提案が出ている画面。Accept / Accept Word の操作バーが見える](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/vscode-1-144-customization-marketplace/images/demo-10-agent-completion.png)

![skills: の行に doc-reviewing というグレーのインライン提案が出ている画面](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/vscode-1-144-customization-marketplace/images/demo-10b-skills-suggestion.png)

:::note warn
このグレーの文字は、エディタの**インライン提案**（ゴーストテキスト）です。リリースノートの「補完・hover・検証」が出す候補リストとは別物かもしれません。実際、`gpt-4` は私の環境で使えるモデルとは限らず、`doc-reviewing` というスキルも、手元のスキル一覧から出したものかは確認できていません。**モデル ID やスキル名は、提案をそのまま受け入れずに、使えるものかを確認してください**。
:::

一方、検証のほうははっきり確認できました。存在しないモデル名 `this-model-does-not-exist` を書いて、その上にカーソルを置くと、hover に次のメッセージが出ました。

```text
Model 'this-model-does-not-exist' is not available for the GitHub Copilot harness.
The model to use. An array is treated as an ordered list of model preferences.
```

モデルの値の部分が強調表示され、**Quick Fix... (Ctrl+.)** と **Fix** も並びます。2行目の説明が、前の表にある「`model` は優先順のリストでも書ける」の根拠になっています。ここで撮ったファイルの `tools: ["read", "not-a-real-tool"]` と `skills: ["not-a-real-skill"]` の警告は、画面では確認できていません。

![存在しないモデル名に対する hover。Model 'this-model-does-not-exist' is not available for the GitHub Copilot harness. と表示され、Quick Fix と Fix が出ている](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/vscode-1-144-customization-marketplace/images/demo-11-agent-validation.png)

## 配る：共有リンクとリポジトリの設定

### vscode:// の共有リンク

README やチームのガイドに貼っておけば、読んだ人がワンクリックでマーケットプレイスの追加やプラグインのインストールに進めます。

![マーケットプレイスの追加、プラグインのインストール、Customizations のページを開く、の3種類の共有リンク](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/vscode-1-144-customization-marketplace/images/img-04-share-links.png)

| 目的                                           | リンク                                                              |
| ---------------------------------------------- | ------------------------------------------------------------------- |
| マーケットプレイスを追加                       | `vscode://chat-plugin/add-marketplace?ref=owner/repo`               |
| マーケットプレイスを追加してプラグインを入れる | `vscode://chat-plugin/install?source=owner/repo&plugin=plugin-name` |
| Plugins ページを検索つきで開く                 | `vscode://chat-customizations/open?page=plugins&search=github`      |

`owner/repo` はマーケットプレイスの GitHub リポジトリ、`plugin-name` はそのマーケットプレイスでのプラグイン名に置き換えます。ページ名は `plugins` のほか、`agents`、`skills`、`instructions`、`hooks`、`mcp-servers`、`tools`、`migrations` が使えます。`search` を省けば絞り込みなしで開きます。Insiders に向けたいときは、`vscode://` を `vscode-insiders://` にします。

大事なのは、**実行前に VS Code が確認を出す**ことです。これらの操作は Copilot ハーネスのセッションを使い、使えるセッションがなければ作成するかどうかも聞かれます。公式ドキュメントでも、**信頼できる提供元の場合だけ進める**よう書かれています。

リリースノートでは、プラグインの README に置く **Install in VS Code** ボタンにも使える、と紹介されていました。例として、Microsoft の `vscode-team-kit` リポジトリの Session timeline プラグインの Getting started が挙がっています。共有リンクを開いたときの確認ダイアログは、私の環境では画面を撮れていないので、ドキュメントの記述（実行前に確認が出る）の紹介にとどめます。

### リポジトリで既定のプラグインを決める

チームに使ってほしいマーケットプレイスとプラグインは、リポジトリの `.github/copilot/settings.json` に書いておけます（`.claude/settings.json` も対象です）。Copilot ハーネスでは、これがリポジトリの既定値になります。

```json:.github/copilot/settings.json
{
  "extraKnownMarketplaces": {
    "company-tools": {
      "source": {
        "source": "github",
        "repo": "your-org/plugin-marketplace"
      }
    }
  },
  "enabledPlugins": {
    "code-formatter@company-tools": true
  }
}
```

- `extraKnownMarketplaces`: プロジェクトにマーケットプレイスを登録する。Customizations のソースに出てくる
- `enabledPlugins`: 既定で有効にするプラグイン。`<plugin>@<marketplace>` の形式で書く

**マーケットプレイスのキー（上の例なら `company-tools`）は、そのマーケットプレイスの `marketplace.json` の `name` と一致させる**必要があります。プラグイン ID は、リポジトリ名ではなく `<plugin>@<marketplace>` です。名前を変えると、共有している設定が別のものを指してしまうので、安定させておきます。

個人側では、任意のプラグインなら Plugins ページでオフにでき、共有の既定値は変わりません。エンタープライズの管理設定は、リポジトリの既定値や個人の選択より優先されます。GitHub の changelog でも、同じ日に **repository plugin defaults** が一般提供になったことが紹介されていました。

## 海外ではどう見られている？

公式情報に加えて、発表から数日のあいだに公開された海外の記事も読みました。個人の検証記事はまだ少なく、ニュースサイトや解説記事が中心です。

- **Visual Studio Magazine**（[VS Code 1.144 Unleashes Copilot Fusion, AI Image Generation and Computer Use](https://visualstudiomagazine.com/articles/2026/10/28/vs-code-1-144-unleashes-copilot-fusion-ai-image-generation-and-computer-use.aspx)）は、「Agent Marketplace, Connectors and Shared Memory」という見出しで、Browse を「プラグインやスキルなどを探すマーケットプレイス風のインターフェース」、Copilot connectors を「Preview で、GitHub 管理の MCP サーバーを通じて外部サービスにアクセスできるもの」と整理しています。コネクターのカタログ画面も載っています。
- **NT Compatible**（[Visual Studio Code 1.144 Ships: Microsoft Turns Editor Into an AI Agent Command Center](https://www.ntcompatible.com/story/visual-studio-code-1144-ships-microsoft-turns-editor-into-an-ai-agent-command-center/)）は、Copilot ハーネスの話に絡めて「**カスタマイズを一度書けば、VS Code・Copilot CLI・Copilot アプリ・Cloud セッションで一貫して動く**」点を押さえています。コネクターは「Slack、Notion、Postman、Sentry、Microsoft Learn、Statsig、Work IQ から、ローカルのサーバー設定なしで文脈を持ってくる」、Browse は「GitHub Feed とサードパーティのマーケットプレイスを集約し、`vscode://` リンクでワンクリックのインストールができる」という書き方でした。
- **dev.to**（Muhammad Hamid Raza 氏の [VS Code 1.144: Cloud Sessions, Copilot Fusion, Image Generation, and More](https://dev.to/hamidrazadev/vs-code-1144-cloud-sessions-copilot-fusion-image-generation-and-more-a-friendly-guide-4d0d)）は初心者向けの解説です。マーケットプレイスの項では、「**信頼できない提供元のプラグインを入れない。プラグインは手元でコードを実行できるから**」と、注意を Don't の一つに入れていました。

海外の記事を読んでいて印象に残ったのは、「コネクターが便利」という話より、**ハーネスをまたいでカスタマイズが共通になる**という文脈で語られていることです。スキルやプラグインを書く側にとっては、「一度書けば、いろんなクライアントで使える」ほうが効いてくる、という見方なんだと思いました。

一方で、NT Compatible は「オープンなプロトコルを前面に出しつつ、有料の Copilot エコシステムへの結びつきも深める」という見方も添えていました。コネクターが Copilot ハーネス限定である点は、使うかどうかを決めるときに頭に置いておきたいところです。

## ハマりそうなポイント

### Q: Browse に Copilot Connectors が出てこない

**A**: 次を順に確認してください。

1. VS Code が 1.144 以降か
2. Copilot ハーネスのセッションを選んでいるか（ドキュメントでは Copilot ハーネスのみ。私の環境では Local 表示でも一覧は出ましたが、使えるかは別なので Copilot のセッションで試すのが確実です）
3. `chat.customizations.copilotConnectors.enabled` がオンか
4. Business / Enterprise の場合、管理者が **Editor preview features** を有効にしているか
5. 組織の MCP の制限で、そのサービスがブロックされていないか

### Q: GitHub Feed が選べない・一覧が空になる

**A**: GitHub Feed は、対応しているハーネスが必要で、**Local セッションでは使えません**。私の環境では、Local 表示のソースメニューに GitHub Feed が出ませんでした。ソースを GitHub Feed にしたまま対応していないエージェントを選ぶと、一覧が空になって「`GitHub Feed: The selected agent cannot retrieve curated customizations.`」という警告が出ます。**Retry** を押す前に、ハーネスを Copilot にして開き直してください。

### Q: Connect を押したら、組織の Single sign-on 画面が出た

**A**: 所属する Organization が、シングルサインオンでの認証を求めている場合の動きだと思います。**Authorize** で組織を認証してから、VS Code の許可画面に進みます。組織のポリシーによっては、管理者の承認が必要になることもあります。

### Q: Issue を Copilot に割り当てたセッションで、コネクターが使えない

**A**: GitHub Actions 上で動くセッションはコネクターが未対応です。ドキュメントでは、対応クライアントとして Copilot アプリ / Copilot CLI / VS Code / Copilot cloud が挙がっていました。

### Q: `/plugin` で入れたプラグインが、Customizations の画面に出てこない

**A**: 両者は別のプラグイン一覧を使っています。`/plugin` で入れたものは `/plugin list` で、画面で入れたものは Plugins ページで確認します。

### Q: 入れたプラグインのスキルが読み込まれない

**A**: 公式のトラブルシューティングでは、`SKILL.md` の `name` が素の kebab-case（`test-runner` のように）で、名前空間のプレフィックスが付いていないこと、ディレクトリ名と `name` が一致していることが挙がっていました。名前が不正だと、**エラーなしでスキップされる**そうです。

### Q: プラグインが一覧に出ない

**A**: `chat.plugins.enabled` が `true` か、プラグインの `name` が命名規則に合っているか（Agent Plugins 1.0 は小文字・数字・ハイフン・ピリオド）、`plugin.json` が認識される場所にあるかを確認します。

### Q: 接続したコネクターをやめたい

**A**: MCP Servers のページで `Connector:<サービス名>` を選び、**Disconnect** します。

## まとめ

- Customizations の新しい入口 **Browse** で、GitHub Feed・MCP Gallery・プラグインのマーケットプレイス・Copilot Connectors を一か所から探せる（Preview）。GitHub Feed は Local 表示では選べなかった
- **Copilot connectors** は、GitHub 管理の MCP サーバー。Connect してブラウザで許可すれば、`mcp.json` を書かずに Slack や Notion などの文脈を使える。私は Work IQ をつないで、メール・Teams・予定が取れるところまで確認した。GitHub Actions 上のセッションは未対応
- 入れる前に、**公開元・同梱物・権限・ポリシー**の4点を確認して、入れたあとは新しいセッションで小さなタスクを試す。Work IQ のように、**自分のメールがそのままチャットに出る**コネクターは、写り込みにも注意
- `.agent.md` は、`model`（優先順リスト可）・`tools`・`skills` に補完・hover・検証が付く。存在しないモデル名は、hover で「そのハーネスでは使えない」と教えてくれた
- `vscode://` の共有リンクと `.github/copilot/settings.json` で、チームへの配布が楽になる。`/plugin` `/mcp` `/skills` でチャットから管理もできる

個人的には、「定番のサービスはコネクター、社内固有のものは自前の MCP、チームに配るものはリポジトリの設定」という分け方が、いちばん整理しやすいと思いました。Preview の機能なので、挙動が変わったらまた記事を更新します！

---

## 📣 GitHub Copilot User Group Japan（Gh-CUG）のお知らせ

今回のようなVSCode/GithubCopilotのコミュニティです！是非さんかして交流しましょう！＃ghcugでのポストも歓迎です
月一回ほどConnpassでもイベントしているので興味ある方参加してください
🔗 **Connpass グループページ：** [GitHub Copilot User Group Japan](https://gh-cug.connpass.com/)

公式ハッシュタグは **#GhCUG** です。

## 参考

**公式**

- [Visual Studio Code 1.144（Agent customizations）](https://code.visualstudio.com/updates/v1_144#_agent-customizations)
- [Copilot connectors（VS Code Docs）](https://code.visualstudio.com/docs/agent-customization/copilot-connectors)
- [Agent plugins in VS Code（VS Code Docs）](https://code.visualstudio.com/docs/agent-customization/agent-plugins)
- [Customizations overview：Discover marketplace customizations（VS Code Docs）](https://code.visualstudio.com/docs/agent-customization/overview#_discover-marketplace-customizations-preview)
- [GitHub Copilot in VS Code, Universe releases（GitHub Changelog）](https://github.blog/changelog/2026-10-28-github-copilot-in-vs-code-universe-releases)

**海外記事**

- [VS Code 1.144 Unleashes Copilot Fusion, AI Image Generation and Computer Use（Visual Studio Magazine）](https://visualstudiomagazine.com/articles/2026/10/28/vs-code-1-144-unleashes-copilot-fusion-ai-image-generation-and-computer-use.aspx)
- [Visual Studio Code 1.144 Ships: Microsoft Turns Editor Into an AI Agent Command Center（NT Compatible）](https://www.ntcompatible.com/story/visual-studio-code-1144-ships-microsoft-turns-editor-into-an-ai-agent-command-center/)
- [VS Code 1.144: Cloud Sessions, Copilot Fusion, Image Generation, and More（dev.to）](https://dev.to/hamidrazadev/vs-code-1144-cloud-sessions-copilot-fusion-image-generation-and-more-a-friendly-guide-4d0d)

**関連する私の記事**

- [VS Code 1.144：PC を閉じてもエージェントが働く。Cloud セッションと Cloud Automations を試した](https://qiita.com/shahin0809/items/26e401dc28c1ca60d8c7)
