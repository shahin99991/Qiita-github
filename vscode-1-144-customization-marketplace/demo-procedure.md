# デモ手順 & スクショ撮影タイミング

「VS Code 1.144：Customizations の新ホーム Browse と Copilot connectors。探す・つなぐ・整える・配るを整理する」記事用のデモ手順と、各画像の撮影タイミングをまとめたファイルです。

- 記事本体: [article-qiita.md](./article-qiita.md)
- 画像保存先: `./images/`
- 画像URL形式: `https://raw.githubusercontent.com/shahin99991/Qiita-github/main/vscode-1-144-customization-marketplace/images/<ファイル名>`
- 差し替え方法: 同名で `./images/` に上書き → push（記事側の URL 変更は不要）
- 解説画像（img-00 〜 img-05）は Gemini で生成済み。このファイルの対象は **実機スクリーンショット（demo-*）** のみ

> ⚠️ **公開前の注意**: 画像を GitHub に push するまで raw URL は 404 になります。記事公開前に必ず画像を先に push してください。

## 撮影状況（2026/10/30 時点）

撮影済みの19枚は記事に組み込み済みです。残りは、撮れたら追加する任意の画像です。

| 状況        | ファイル                                                                                                                                      |
| ----------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| ✅ 記事に反映 | demo-00 / 01 / 01b / 02 / 03（`@type:canvas`）/ 04 / 04a / 05 / 05a / 05b / 06 / 08（Work IQ）/ 09 / 09b / 09c / 10 / 10a / 10b / 11            |
| ⬜ 未撮影     | **demo-07**（MCP Servers の `Connector:` エントリ）、**demo-12**（共有リンクの確認ダイアログ）。撮れたら記事の該当箇所（手順3・共有リンク）に追記 |
| ⬜ 任意       | `model` の候補リスト（Ctrl+Space の IntelliSense）、`tools` / `skills` の誤り値に対する警告、`@type:mcp` での絞り込み、Microsoft Learn Docs での読み取りテスト |

記事は「撮れていない画面はドキュメントの記述として書く」方針で、demo-07 / demo-12 の画像なしでも公開できる状態です。

> 📝 撮影時の注意（実機で分かったこと）: Browse の GitHub Feed は、タイトルが `Agent Customizations (Local · …)` の画面ではソースメニューに出ません。`(Copilot)` の画面で撮ってください。

---

## 事前準備

| 項目                       | 内容                                                                                                                                                                |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| VS Code                    | 1.144 以降（Help > About でバージョン確認。Insiders でも可）                                                                                                        |
| Copilot プラン             | 任意の Copilot プラン。Business / Enterprise は管理者が **Editor preview features** を有効にしている必要あり                                                        |
| 設定                       | `chat.customizations.marketplace.enabled` / `chat.customizations.copilotConnectors.enabled`（設定画面で検索して、存在しない・名前が違う場合はメモ）                 |
| ハーネス                   | **Copilot ハーネス**のセッションを選んでおく（Local だと GitHub Feed とコネクターが出ない）                                                                         |
| 接続するコネクター         | 読み取り中心で、撮影してよいサービスを1つ決める。第一候補は **Microsoft Learn Docs**（ワークスペースの情報が写らない）。Slack / Notion を使う場合は後述の注意を参照 |
| 検証ワークスペース         | 空に近いテスト用フォルダ。`.github/agents/` を作れる場所（手順B で使う）                                                                                            |
| テスト用マーケットプレイス | 自分の GitHub リポジトリ、または `github/copilot-plugins`（手順A-3 の追加確認用）                                                                                   |
| 共有リンク用               | 手順C で使うマーケットプレイスの `owner/repo` とプラグイン名を1つ決めておく                                                                                         |

:::note warn
撮影前に、**組織名・メールアドレス・ワークスペース名・Slack / Notion のチャンネル名やページ名・トークン**が写り込まないか確認すること。コネクターの許可画面（demo-05）はとくに、アカウント名やワークスペース名が出やすい。必要ならモザイクをかける。
:::

### 撮影の共通ルール

- 表示倍率は 100〜125%、ウィンドウ幅は全枚数で揃える（目安 1200〜1400px）
- 1枚で「何が分かるか」を1つに絞る
- ファイル名は下の対応表どおり（`demo-XX-*.png`）
- **Preview** などのステータス表記が画面に出るものは、必ず写す
- テーマ（ライト / ダーク）は全枚数で統一する

### 画像と記事内位置の対応表

| ファイル名                          | 記事内の位置                     | 撮影する内容                                          |
| ----------------------------------- | -------------------------------- | ----------------------------------------------------- |
| `demo-00-open-customizations.png`   | 探す：Browse                     | コマンドパレットの `Chat: Open Customizations`        |
| `demo-01-browse-home.png`           | 探す：Browse                     | Browse のホーム（All Sources）                        |
| `demo-01b-github-feed.png`          | 探す：Browse                     | ソースを GitHub Feed にした Browse                    |
| `demo-02-source-menu.png`           | 探す：Browse                     | ソースメニュー（Local 表示。GitHub Feed なし）        |
| `demo-03-filter-type-canvas.png`    | 探す：Browse                     | `@type:canvas` で絞り込んだ状態                       |
| `demo-04a-plugin-install-button.png`| つなぐ：Install と Connect       | プラグインの Install ボタン                           |
| `demo-04-connectors-list.png`       | つなぐ：手順1                    | Copilot Connectors の一覧と Work IQ の Connect        |
| `demo-05a-sso.png`                  | つなぐ：手順2                    | 組織の Single sign-on 画面                            |
| `demo-05-connector-authorize.png`   | つなぐ：手順2                    | ブラウザの許可画面                                    |
| `demo-05b-connection-created.png`   | つなぐ：手順2                    | Work IQ connection has been created                   |
| `demo-06-connected.png`             | つなぐ：手順3                    | Disconnect に変わった Browse                          |
| `demo-07-mcp-servers-connector.png` | （未撮影）                       | MCP Servers に出た `Connector:` サーバー              |
| `demo-08-connector-in-chat.png`     | つなぐ：手順4                    | チャットで Work IQ をテストした画面（マスク済み）     |
| `demo-09-slash-plugin.png`          | 整える：スラッシュコマンド       | `/plugin` のサブコマンド補完                          |
| `demo-09b-plugin-list.png`          | 整える：スラッシュコマンド       | `/plugin list` の結果                                 |
| `demo-09c-slash-fuzzy.png`          | 整える：スラッシュコマンド       | あいまい一致の補完                                    |
| `demo-10a-agent-empty.png`          | 整える：カスタムエージェント編集 | 値が空の `model` / `tools` / `skills`                 |
| `demo-10-agent-completion.png`      | 整える：カスタムエージェント編集 | `model` のインライン提案                              |
| `demo-10b-skills-suggestion.png`    | 整える：カスタムエージェント編集 | `skills` のインライン提案                             |
| `demo-11-agent-validation.png`      | 整える：カスタムエージェント編集 | 存在しないモデル名の hover 警告                       |
| `demo-12-share-link-confirm.png`    | （未撮影）                       | 共有リンクを開いたときの確認ダイアログ                |

---

## パートA: Browse（demo-01 〜 demo-03）

### 📷 demo-01 `demo-01-browse-home.png` — Browse のホーム

**記事内の位置**: 「探す：Browse は Customizations の新しいホーム」

**手順**:

1. コマンドパレット（`Ctrl+Shift+P`）で `Chat: Open Customizations` を実行
2. Browse（ホーム）が表示されるのを確認
3. 画面を上から下までスクロールして、**Editor's picks** / **Plan, build, and ship** / **Connect your work** の見出しがあるか確認

**撮影タイミング**: 最初に開いた直後の状態。セクション見出しが2つ以上見えるのが望ましい。1枚に収まらなければ縦に2枚撮って結合する

**撮影ポイント**: **Preview** の表記が見えていれば写す

**メモ（記事の TODO 用）**:

- セクション名が記事の記述（Editor's picks / Plan, build, and ship / Connect your work）と一致しているか
- 検索欄と、ソース・種類の絞り込みがどこにあるか

---

### 📷 demo-02 `demo-02-source-menu.png` — ソースメニュー

**記事内の位置**: 同上

**手順**:

1. Browse の上部にある**ソースのメニュー**を開く
2. 選べる項目（GitHub Feed / Copilot Connectors / マーケットプレイス）を確認
3. **Configure Marketplaces** があるか確認（あれば、開いて **Add Marketplace** の画面も1枚撮る。余力があれば）

**撮影タイミング**: メニューが開いて、全項目が見えている状態

**メモ（TODO 用）**:

- 実際に出た項目名（記事の「GitHub Feed / Copilot Connectors / プラグインマーケットプレイス」と一致するか）
- Local ハーネスのセッションに切り替えたとき、GitHub Feed や Copilot Connectors が選べなくなるか（記事の「Local では使えない」の確認。余力があれば Local の状態も1枚撮る）

---

### 📷 demo-03 `demo-03-filter-type-mcp.png` — `@type:mcp` で絞り込む

**記事内の位置**: 同上

**手順**:

1. ブラウザ（またはターミナル）から、次のリンクを開く。または Browse の検索欄に `@type:mcp` と入力する

```text
vscode://chat-customizations/open?page=discover&search=%40type%3Amcp
```

2. 検索欄に `@type:mcp` が入った状態で、MCP サーバーだけに絞られているのを確認

**撮影タイミング**: 検索欄の入力内容と、絞り込まれた結果の一覧が同時に見えている状態

**撮影ポイント**: リンクから開いた場合は、**確認ダイアログが出るか**も見ておく（出たら demo-12 の参考にする）

**メモ（TODO 用）**:

- リンクで開いたとき、検索欄に値が入ったか
- `@type:canvas` でも試して、結果が変わるか（記事にはリリースノートの記述として書いている）

---

## パートB: Copilot connectors（demo-04 〜 demo-08）

:::note warn
Slack / Notion などの業務サービスを使うと、**ワークスペース名・チャンネル名・ページのタイトル**が写り込みます。撮影用の個人アカウントやテスト用ワークスペースを使うか、**Microsoft Learn Docs** にするのが安全です。許可画面（demo-05）に出る**権限の一覧**は、記事の「権限を見る」の根拠になるので、読める状態で撮ってください。
:::

### 📷 demo-04 `demo-04-connectors-list.png` — Copilot Connectors の一覧

**記事内の位置**: 「接続の流れ」手順1

**手順**:

1. Browse のソースメニューで **Copilot Connectors** を選ぶ
2. サービスの一覧と **Connect** ボタンが出るのを確認
3. 一覧に出ているサービス名を、記事の記述と照合してメモする

**撮影タイミング**: 一覧が表示されて、複数のサービスと Connect ボタンが見えている状態

**メモ（TODO 用）**:

- 実際に出たサービス名（記事ではリリースノートの Port / Postman / Sentry / Slack / Statsig / Work IQ と、GitHub Docs の26個前後を紹介している）
- 表示されたコネクターの数（スクロールして数える。数値は記事に書く前に実値で確認）
- Copilot Connectors が出ない場合は、記事の Q&A の確認項目（バージョン / ハーネス / 設定 / ポリシー）を順に試して、**どこで解消したか**を記録する

---

### 📷 demo-05 `demo-05-connector-authorize.png` — ブラウザの許可画面

**記事内の位置**: 手順2

**手順**:

1. 接続するサービスの **Connect** を押す
2. ブラウザが開くので、許可画面を表示する
3. **要求されている権限の内容**を読む（承認する前に撮影）
4. 問題なければ承認する

**撮影タイミング**: 許可画面が表示されて、権限の一覧が読める状態（承認ボタンを押す前）

**撮影ポイント**: アカウント名、メールアドレス、ワークスペース名にモザイクをかける。権限の文言は残す

**メモ（TODO 用）**:

- 要求された権限の内容（読み取りのみか、書き込みも含むか）
- 管理者の承認が必要なサービスだった場合は、その表示
- Connect からブラウザが開くまで、承認後に VS Code へ戻るまでの流れ（手動で戻る必要があったか）

---

### 📷 demo-06 `demo-06-connected.png` — 接続後の Browse

**記事内の位置**: 手順3

**手順**:

1. 承認後に VS Code へ戻る
2. Browse の Copilot Connectors で、接続したサービスのボタンが **Disconnect** に変わっているか確認

**撮影タイミング**: 接続したサービスのカードが、接続済みの表示になっている状態

---

### 📷 demo-07 `demo-07-mcp-servers-connector.png` — MCP Servers の Connector エントリ

**記事内の位置**: 手順3

**手順**:

1. Customizations の **MCP Servers** のページを開く（`vscode://chat-customizations/open?page=mcp-servers` でも可）
2. `Connector:<サービス名>` の名前のサーバーが出ているのを確認

**撮影タイミング**: `Connector:` で始まるサーバー名が一覧にはっきり見えている状態

**メモ（TODO 用）**:

- 実際に表示された名前の形式（記事では `Connector:<サービス名>` と書いている）
- ここから **Disconnect** できるか（記事の「接続の解除」の確認。撮影後に実際に解除して、挙動を記録する）
- 自分で `mcp.json` に書いたサーバーとの見た目の違い（あれば）

---

### 📷 demo-08 `demo-08-connector-in-chat.png` — チャットでコネクターを使う

**記事内の位置**: 手順4

**手順**:

1. **新しいセッション**を作り、Copilot ハーネスを選ぶ
2. 以下のプロンプトを送信する（Microsoft Learn Docs を接続した場合。別のサービスなら、読み取り専用の内容に置き換える）

```text
Microsoft Learn Docs のコネクターを使って、Azure Functions の Flex Consumption プランの
スケール上限について公式ドキュメントで確認して。回答には参照した URL も付けて。
ファイルの編集やコマンドの実行はしないで。
```

3. コネクターのツールが呼ばれている様子と、回答を確認

**撮影タイミング**: ツール呼び出しの表示（ツール名が分かる状態）と、回答の冒頭が同じ画面に入る状態

**メモ（TODO 用）**:

- ツール呼び出しの前に承認の確認が出たか
- 回答に参照 URL が付いたか、内容が公式ドキュメントと合っているか（記事に結果を書く場合は、必ず公式ページで裏取りする）
- コネクターを使わない（切断した）状態で同じ質問をしたときの違い（余力があれば）
- 既存の GitHub Copilot ハーネス以外（Local）で同じことを試したとき、コネクターが使えない挙動（記事の「Copilot ハーネスのみ」の確認）

---

## パートC: 整える・配る（demo-09 〜 demo-12）

### 📷 demo-09 `demo-09-slash-plugin.png` — `/plugin` の補完

**記事内の位置**: 「整える：チャットから管理する `/plugin` `/mcp` `/skills`」

**手順**:

1. **Copilot ハーネス**のセッションを開く
2. 入力欄に `/plugin ` と入力（末尾にスペース）して、サブコマンド補完を表示する
3. 続けて `/plugin list` を実行して、結果を確認
4. 余力があれば `/mcp show` と `/skills info` も試す

**撮影タイミング**: 補完候補が開いていて、`list` / `install` / `marketplace` などが見えている状態。もう1枚、`/plugin list` の結果が出た状態も撮っておく

**メモ（TODO 用）**:

- 補完に出たサブコマンドの一覧（記事の表と差がないか）
- `/plugin list` と、Customizations の Plugins ページの表示が**一致するか**（記事では「別の一覧」と紹介している。実際の差を確認）
- Local ハーネスで `/plugin` を入力したときの挙動（余力があれば）

---

### 📷 demo-10 `demo-10-agent-completion.png` — `.agent.md` の補完

**記事内の位置**: 「カスタムエージェントの編集が賢くなった」

**手順**:

1. ワークスペースに `.github/agents/doc-reviewer.agent.md` を作る
2. Copilot ハーネスを選んだ状態で、次の内容を貼る（`model` と `skills` は、補完で出た実際の値に後から置き換える）

```markdown
---
name: doc-reviewer
description: ドキュメントの変更をレビューして、古い記述と抜けを指摘する
model:
tools:
skills:
---

変更されたドキュメントを読んで、古くなった記述・手順の抜け・リンク切れを指摘してください。
```

3. `model:` の後ろにカーソルを置いて `Ctrl+Space` で候補を出す
4. `tools:` でも同様に補完を出して、`read` / `edit` / `execute` が出るか確認
5. `skills:` でも補完を出して、説明やソースの情報が付くか確認。候補の上で hover も試す

**撮影タイミング**: `model` の補完リストが開いていて、モデルIDの候補が複数見えている状態。`tools` と `skills` も撮れたら、`demo-10-agent-completion.png` に横並びで結合してよい

**メモ（TODO 用）**:

- 補完で出たモデルIDの例（記事の `<優先するモデルID>` を実在する値に置き換える場合に使う）
- `model` を単一値で書いた場合と、`["...", "..."]` のリストで書いた場合の両方が受け入れられるか
- `tools` の候補に出たエイリアスの一覧
- スキルが1つもない場合は、`skills` の補完が空になるか（先にテスト用のスキルを置いておくと撮りやすい）

---

### 📷 demo-11 `demo-11-agent-validation.png` — 誤った値の警告

**記事内の位置**: 同上

**手順**:

1. 手順 demo-10 のファイルを、次のように**わざと間違った値**に変える

```markdown
---
name: doc-reviewer
description: ドキュメントの変更をレビューして、古い記述と抜けを指摘する
model: this-model-does-not-exist
tools: ["read", "not-a-real-tool"]
skills: ["not-a-real-skill"]
---
```

2. 数秒待って、波線と警告（Problems パネル）が出るのを確認
3. 該当箇所に hover して、警告メッセージを表示する

**撮影タイミング**: 波線と hover の警告文が同時に見えている状態。Problems パネルも一緒に写すとさらに分かりやすい

**メモ（TODO 用）**:

- 警告が出るまでの時間（記事では「探索が終わってから出る」と書いている。ファイルを開いた直後は警告が出ないかを確認）
- 警告のメッセージ文面
- ハーネスを **Local** に切り替えたとき、同じファイルの警告が変わるか（記事の「`target` がなければハーネスに合わせて補完・診断が出る」の確認。ファイルを開き直さなくても更新されるか）

---

### 📷 demo-12 `demo-12-share-link-confirm.png` — 共有リンクの確認ダイアログ

**記事内の位置**: 「配る：共有リンクとリポジトリの設定」

**手順**:

1. 次のいずれかのリンクを、ブラウザのアドレスバー、または README を開いたプレビューからクリックして開く

```text
vscode://chat-plugin/add-marketplace?ref=<owner>/<repo>
```

```text
vscode://chat-plugin/install?source=<owner>/<repo>&plugin=<plugin-name>
```

2. VS Code に切り替わって、**確認ダイアログ**が出るのを確認
3. **まだ許可しない**状態で撮影する
4. 撮影後、問題なければ許可 or キャンセルして、その後の挙動を確認

**撮影タイミング**: ダイアログが出て、追加しようとしているマーケットプレイス（またはプラグイン）の情報が読める状態

**撮影ポイント**: 自分の組織の内部リポジトリを使う場合、`owner/repo` が写り込むので、公開しても問題ないリポジトリにするか、モザイクをかける

**メモ（TODO 用）**:

- 確認ダイアログの文言
- 使えるセッションがない状態で開いたとき、「セッションを作成するか」を聞かれるか（記事の記述の確認）
- 信頼確認（初めてのマーケットプレイス）のダイアログが別に出るか
- 許可したあと、`/plugin marketplace list` や Plugins ページに追加されたか

---

## 撮影後のチェックリスト

- [ ] 撮影済みの画像（demo-*）を `./images/` に置いた（19枚。リネーム済み）
- [ ] 個人情報・組織名・ワークスペース名・トークンが写っていないか、全枚数を確認した（とくに demo-05a / 05 / 05b / 08 のマスク）
- [ ] Preview の表記が出る画面は、表記が見えている
- [x] 記事内の `TODO(デモ後)` は削除済み（未撮影の demo-07 / demo-12 はドキュメントの記述として記載）
- [ ] 実機で確認できなかった項目は、記事の「ドキュメントの記述」のままにしてある（「確認した」と書いていない）
- [ ] `<優先するモデルID>` `<使いたいスキル名>` などのプレースホルダーを、実在する値に置き換えるか、プレースホルダーのままでよいか判断した
- [ ] 参考リンクが開ける（とくに GitHub changelog と海外記事）
- [ ] 画像を GitHub に push して、raw URL が表示される
- [ ] 記事の `updated_at` を公開日に更新した

---

## 記事とデモの対応（撮影後の反映状況）

記事から `TODO(デモ後)` は削除済みです。実機で確認できた内容と、未確認のまま残してある内容は次のとおりです。

| セクション             | 確認できた内容                                                                                            | 未確認（記事ではドキュメントの記述として表記）                         |
| ---------------------- | --------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| 探す                   | ソース名（GitHub Feed / MCP Gallery / Copilot Connectors / awesome-copilot）、Local では GitHub Feed が出ない、`@type:canvas` | `@type:mcp`、Configure Marketplaces の操作                             |
| つなぐ                 | Work IQ の接続（SSO → 許可画面 → 完了 → Disconnect）、チャットでの取得結果                                  | MCP Servers ページの `Connector:` 表示、送信などの書き込み操作         |
| 整える（スラッシュ）   | `/plugin` の補完、`/plugin list` の結果                                                                    | `/mcp` `/skills` のサブコマンド、Customizations 画面との一覧の差       |
| 整える（エージェント） | 存在しないモデルの hover 警告、インライン提案の挙動                                                        | `tools` / `skills` の誤り値の警告、ハーネス切り替え時の変化            |
| 配る                   | （なし）                                                                                                   | 共有リンクの確認ダイアログ                                             |

---

## 当日の所要時間の目安

| パート                | 内容                             | 備考                                             |
| --------------------- | -------------------------------- | ------------------------------------------------ |
| 準備                  | 設定・ハーネス・テスト用ファイル | 設定名が違う場合は、検索して実際の名前をメモする |
| A: Browse             | demo-01 〜 03                    | ソースを切り替えながら撮ると効率がいい           |
| B: Copilot connectors | demo-04 〜 08                    | 承認が絡むので、先に許可画面から撮る             |
| C: 整える・配る       | demo-09 〜 12                    | demo-10 → demo-11 は同じファイルを書き換えて撮る |

撮影順は **A → B → C** がおすすめです。B で接続したコネクターは、撮影が終わったら **Disconnect** して、不要な権限を残さないようにしてください。
