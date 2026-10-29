# デモ手順 & スクショ撮影タイミング

「VS Code 1.144：PC を閉じてもエージェントが働く。Cloud セッションと Cloud Automations を試した」記事用のデモ手順と、各画像の撮影タイミングをまとめたファイルです。

- 記事本体: [article-qiita.md](./article-qiita.md)
- 画像保存先: `./images/`
- 画像URL形式: `https://raw.githubusercontent.com/shahin99991/Qiita-github/main/vscode-1-144-cloud-sessions/images/<ファイル名>`
- 差し替え方法: 同名で `./images/` に上書き → push（記事側の URL 変更は不要）

> ⚠️ **公開前の注意**: 画像を GitHub に push するまで raw URL は 404 になります。記事公開前に必ず画像を先に push してください。

---

## 事前準備

| 項目                  | 内容                                                                                                             |
| --------------------- | ---------------------------------------------------------------------------------------------------------------- |
| VS Code               | 1.144 以降（Help > About でバージョン確認。Insiders でも可）                                                     |
| Copilot プラン        | 有料プラン（Pro / Pro+ / Max / Business / Enterprise）。Business / Enterprise は管理者のポリシー許可も必要       |
| 検証リポジトリ        | **private** のリポジトリ（write 権限あり）。Cloud Automations は public 不可。例: `YJK-Inc/Test-Repo`            |
| 設定                  | `chat.agentHost.cloudSandbox.enabled` と `chat.automations.cloud.enabled`（必要なら `chat.automations.enabled`） |
| Copilot CLI           | 最新版をインストールし、同じ GitHub アカウントでログイン済み                                                     |
| 別クライアント        | github.com（Copilot ページ）を開けるブラウザ。余力があれば GitHub Mobile                                         |
| テスト用 Issue ラベル | 手順B-3 で使う絞り込み用ラベル（例: `automation-test`）を作成済み                                                |
| ネタ仕込み            | README / docs に「少し古い記述」を1〜2か所わざと残しておく（手順A-3 の結果が見やすくなる）                       |

:::note warn
撮影前に、**組織名・メールアドレス・内部URL・トークン**が写り込まないか確認すること。必要ならモザイクをかける。
:::

### 撮影の共通ルール

- 表示倍率は 100〜125%、ウィンドウ幅は全枚数で揃える（目安 1200〜1400px）
- 1枚で「何が分かるか」を1つに絞る
- ファイル名は下の対応表どおり（`demo-XX-*.png`）
- ステータス表記（Preview / Experimental）が画面に出るものは、必ず写す

---

## パートA: Cloud セッション（demo-01 〜 demo-05）

### 📷 demo-01 `demo-01-settings.png` — 設定の確認

**記事内の位置**: 「試してみた：リサーチを任せて…」手順1

**手順**:

1. `Ctrl+,` で設定を開き、検索欄に `chat.agentHost.cloudSandbox` と入力
2. チェックをオンにする
3. 続けて `chat.automations.cloud` を検索して状態を確認

**撮影タイミング**: 2つの設定が上下に見える状態（検索欄は `chat.agentHost.cloudSandbox` と `chat.automations.cloud` を OR で出したいので、1枚で収まらなければ2回撮って横に並べる）

**撮影ポイント**: オンになっていることが分かること。Experimental / Preview のタグが付いていればそれも写す

---

### 📷 demo-02 `demo-02-env-picker-cloud.png` — Cloud 環境とリポジトリの選択

**記事内の位置**: 手順2

**手順**:

1. Agents ウィンドウを開く（コマンドパレットで `Agents` と入力）
2. **New** を押す
3. 環境のドロップダウンを開いて **Cloud** を選ぶ
4. **Choose Repository...** を押して、検証リポジトリを選ぶ

**撮影タイミング**: ドロップダウンに Local / Remote / Cloud が並んでいて、Cloud にカーソルがある瞬間。もう1枚、リポジトリ選択後の状態も撮っておく（どちらを使うか後で選ぶ）

---

### 📷 demo-03 `demo-03-cloud-session-running.png` — Cloud セッション実行中

**記事内の位置**: 手順3

**手順**: 以下のプロンプトを送信する。

```text
このリポジトリの README と docs を読んで、内容が古くなっていそうな箇所を3つ挙げて。
根拠になるファイルパスも付けて。
ファイルの編集、依存関係のインストール、コードの実行、Issue や PR の作成はしないで。
結果はこの会話に返して。
```

**撮影タイミング**: 送信直後〜エージェントがファイルを読み始めて、ツール呼び出しやストリーミング出力が見えている状態

**メモ（記事の TODO 用）**: 接続完了までの体感時間、最初の応答までの時間、承認リクエストが出たか（ストップウォッチで測る）

---

### 📷 demo-04 `demo-04-lid-closed-github-com.png` — VS Code を閉じたあと別クライアントで確認【目玉】

**記事内の位置**: 手順4

**手順**:

1. demo-03 のセッションがまだ実行中のうちに、セッションのタイトルをメモする
2. **VS Code を完全に終了**する（ウィンドウを閉じるだけでなくアプリごと）
3. ブラウザで github.com の Copilot ページを開く（または GitHub Mobile を開く）
4. 同じセッションが一覧に出て、進んでいる／完了していることを確認

**撮影タイミング**: 同じセッションのタイトルと、進捗または完了した結果が見えている画面

**撮影ポイント**: **「VS Code が閉じている」ことが伝わる**ようにしたい。デスクトップに VS Code が無い状態でブラウザを撮る、またはスマホ画面を撮る。この記事で一番大事な1枚

**メモ（TODO 用）**: 本当に閉じても進んだか。別クライアントにセッションが出るまでの時間。表示の違い

---

### 📷 demo-05 `demo-05-cli-sessions-remote.png` — Copilot CLI で続きを話す【目玉】

**記事内の位置**: 手順5

**手順**:

1. ターミナルで `copilot` を起動（未ログインなら先にログイン）
2. `/sessions` を実行し、**Remote** タブを開く
3. demo-03 のセッションを選んで接続（ID がわかるなら `copilot --connect=<session-or-task-id>` でも可）
4. 以下を送信する。

```text
2つ目に挙げた箇所を直すための手順を、変更するファイルと確認方法つきで短くまとめて。
まだ実装はしないで。
```

**撮影タイミング**: 「2つ目」を正しく特定して答えている応答が出た直後

**撮影ポイント**: `/sessions` の Remote タブの一覧と、続きの会話が成立していることの両方が分かるように。1枚に収まらなければ2枚撮って結合してよい

**メモ（TODO 用）**: 会話が引き継がれたか。つまずいた点（アカウント違い、CLI のバージョンなど）

---

## パートB: Cloud Automations（demo-06 〜 demo-11）

### 📷 demo-06 `demo-06-automations-view.png` — Automations ビュー

**記事内の位置**: 「試してみた①」手順1

**手順**: Agents ウィンドウのサイドバーで **Automations** を開く

**撮影タイミング**: **Create Automation** ボタンが見える状態。既存の Automation があればそれも一覧に写る

---

### 📷 demo-07 `demo-07-create-cloud-automation.png` — 作成フォーム

**記事内の位置**: 手順2

**手順**:

1. **Create Automation** を押す
2. Name: `weekly-merged-pr-summary` など
3. **Run in the Cloud** をオンにする
4. リポジトリに private のものを選ぶ
5. Trigger: **Manual**
6. Prompt に以下を入力する。許可ツールは何も選ばない。

```text
直近7日間にマージされた PR をまとめて。
機能追加・修正・メンテナンスに分けて、PR 番号を付けて。
ドキュメントの更新が必要そうな変更には印を付けて。
ファイルは変更しないで。
```

**撮影タイミング**: 保存する直前。Run in the Cloud のトグル・Trigger・プロンプト・許可ツール（未選択）が1画面に入る状態

**撮影ポイント**: 縦に長い場合は2枚撮ってもよい。AI クレジット上限の欄があれば写しておく

---

### 📷 demo-08 `demo-08-run-history.png` — Run now と実行履歴

**記事内の位置**: 手順3

**手順**:

1. 保存した Automation を選び、**Run now** を押す
2. History に queued → running → completed と状態が変わるのを待つ
3. 完了した実行を選び、Agents ウィンドウでセッションが開くことを確認

**撮影タイミング**: ステータスが **completed** になった履歴一覧。可能なら running 中の画面も別に撮っておく（状態遷移の説明に使える）

**メモ（TODO 用）**: 実行開始までの待ち時間、完了までの時間、まとめの質、消費した AI クレジット

---

### 手順B-3 の補足: Weekly への変更（スクショ任意）

記事の手順4に対応。撮るなら以下。

1. Automation を選び、Trigger を **Weekly** に変更（曜日・時刻を指定。分は 00 / 15 / 30 / 45 から）
2. 保存して、VS Code を閉じる

特定の画像枠は無いので、記事に載せたい場合は `demo-08` と同様に追加ファイル名（例 `demo-08b-weekly-trigger.png`）で撮り、記事に1行追記する。

---

### 📷 demo-09 `demo-09-event-trigger-issue.png` — Issue トリガーの設定

**記事内の位置**: 「試してみた②」手順2

**手順**:

1. 新しい Automation を作成し、**Run in the Cloud** をオン
2. Trigger に **Issue** を選び、イベントは Issue 作成にする
3. **Advanced** を開き、特定のラベル（例 `automation-test`）で絞り込む
4. Prompt に以下を入力する。

```text
新しく作られた Issue を読んで、再現手順・期待する動作・実際の動作が書かれているか確認して。
足りない項目があれば、その項目だけを聞くコメントを1件だけ返して。
ラベルや担当者は変更しないで。
```

5. 許可ツールは **Issue へのコメント** だけを選ぶ（クローズ・ラベル変更は許可しない）

**撮影タイミング**: Trigger の Issue 設定、Advanced の絞り込み、許可ツール（コメントのみ）が見える状態

**メモ（TODO 用）**: 実際の UI 上のトリガー名・ツール名、絞り込みに使った条件

---

### 📷 demo-10 `demo-10-result-github.png` — Issue にコメントが付いた結果【目玉】

**記事内の位置**: 手順3

**手順**:

1. 対象リポジトリで、情報が足りないテスト用 Issue を立てる（例: タイトルだけで本文は「動きません」のみ。`automation-test` ラベルを付ける）
2. 数分待ち、Issue にコメントが付くことを確認

**撮影タイミング**: Issue 本文と、Copilot（Personal の場合は自分の名義）の聞き返しコメントが同じ画面に入った状態

**撮影ポイント**: **誰の名義でコメントされたか**が分かるように（Personal = 自分、Shared = Copilot）。Agents ウィンドウの履歴側も別に撮っておくと、起動の裏付けとして使える

**メモ（TODO 用）**: 発火までの時間、コメントの質

---

### 📷 demo-11 `demo-11-open-on-github.png` — 止め方（Disable / Open on GitHub）

**記事内の位置**: 手順4

**手順**: Automation のメニュー（…）を開く

**撮影タイミング**: **Disable**・**Delete**・**Open on GitHub** が選べるメニューが開いた状態

**撮影ポイント**: 履歴の実行側に **Stop** が出ていれば、それも別途撮る

---

## 画像ファイル ↔ 記事内URL 対応表

### Gemini 生成済み（差し替え不要）

| ファイル名                       | セクション                                   |
| -------------------------------- | -------------------------------------------- |
| img-00-tldr-overview.png         | TL;DR                                        |
| img-01-where-it-runs.png         | 「PC を閉じても動く」は3種類ある             |
| img-02-session-continuity.png    | Cloud セッション > 何ができるのか            |
| img-03-session-vs-automation.png | Cloud Automations > Cloud セッションとの違い |
| img-04-automation-anatomy.png    | Cloud Automations > 何が設定できるのか       |
| img-05-guardrails.png            | 放置する前に確認したい4つのこと              |

再生成する場合: `python vscode-1-144-cloud-sessions/generate_images.py [キー]`（`GEMINI_API_KEY` は `.env`）

### 実機スクショ（撮影して差し替える）

| ファイル名                          | 記事内の位置           | 優先度     |
| ----------------------------------- | ---------------------- | ---------- |
| demo-01-settings.png                | Cloud セッション 手順1 | 中         |
| demo-02-env-picker-cloud.png        | Cloud セッション 手順2 | 中         |
| demo-03-cloud-session-running.png   | Cloud セッション 手順3 | 高         |
| demo-04-lid-closed-github-com.png   | Cloud セッション 手順4 | **最重要** |
| demo-05-cli-sessions-remote.png     | Cloud セッション 手順5 | **最重要** |
| demo-06-automations-view.png        | Automations① 手順1     | 中         |
| demo-07-create-cloud-automation.png | Automations① 手順2     | 高         |
| demo-08-run-history.png             | Automations① 手順3     | 高         |
| demo-09-event-trigger-issue.png     | Automations② 手順2     | 高         |
| demo-10-result-github.png           | Automations② 手順3     | **最重要** |
| demo-11-open-on-github.png          | Automations② 手順4     | 低         |

URL 形式（全画像共通）: `https://raw.githubusercontent.com/shahin99991/Qiita-github/main/vscode-1-144-cloud-sessions/images/<ファイル名>`

---

## デモ後に記事へ反映する TODO

記事内の `<!-- TODO(デモ後) -->` コメントは5か所あります。検索 `TODO(デモ後)` で探して、メモした実測値に置き換えてください。

| 場所                   | 書く内容                                                   |
| ---------------------- | ---------------------------------------------------------- |
| Cloud セッション 手順3 | 接続完了・最初の応答までの時間、承認リクエストの有無       |
| Cloud セッション 手順4 | VS Code を閉じても進んだか、別クライアントに出るまでの時間 |
| Cloud セッション 手順5 | CLI で会話が引き継がれたか、つまずいた点                   |
| Automations① 手順3     | 開始までの待ち時間、完了時間、まとめの質、消費クレジット   |
| Automations② 手順2・3  | 実際の UI 表記、発火時間、コメントの質、コメントの名義     |

あわせて以下も確定させる。

- [ ] TL;DR の表の ✅ / ⚠️ / ❌ を実機結果に合わせる
- [ ] 冒頭の HTML コメント（画像・TODO のメモ）を削除する
- [ ] 画像を push してから公開（`public/<slug>.md` に配置し、front matter は `id: null`）

---

## 撮影の流れ（おすすめの順番）

実行に時間がかかるものを先に回して、待ち時間に他を撮ると効率が良いです。

1. 設定確認（demo-01）
2. Cloud セッションを開始（demo-02 → demo-03）
3. **待ち時間に** Automations の作成と Run now（demo-06 → demo-07 → demo-08）
4. Cloud セッションの途中経過を確認 → VS Code を終了 → 別クライアントで撮影（demo-04）
5. VS Code を再起動し、CLI で続きを話す（demo-05）
6. Issue トリガーの Automation を作って、テスト Issue を立てる（demo-09 → demo-10）
7. 止め方のメニューを撮る（demo-11）
8. **終わったら Automation を Disable / Delete**（放置による課金・誤起動を防ぐ）

## デモ後の片付け

- 作成した Automation（特に Issue トリガー / Weekly）を Disable か Delete する
- テスト用 Issue をクローズする
- 不要になった Cloud セッションを削除する（成果物は先にリポジトリへ push）
