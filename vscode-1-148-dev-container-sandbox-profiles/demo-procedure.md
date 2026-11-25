# VS Code 1.148 Dev Container ＋ Sandbox profiles デモ手順と撮影メモ

記事 [article-qiita.md](./article-qiita.md) に入れる実機スクリーンショットの撮影手順です。
画像は撮影済みで、記事に入れてあります。差し替えるときは、`images/` に**同じファイル名**で上書きして push すれば表示されます。

- 画像保存先: `./images/`
- 画像URL形式: `https://raw.githubusercontent.com/shahin99991/Qiita-github/main/vscode-1-148-dev-container-sandbox-profiles/images/<ファイル名>`
- 解説図（`img-00` 〜 `img-04`）は生成済み。実機スクリーンショットは `demo-01` 〜 `demo-25`（下の表）

> ⚠️ **公開前の注意**: 画像を GitHub に push するまで raw URL は 404 になります。記事公開前に必ず画像を先に push してください。

## 記事に使った画像（確定版）

実機で撮った 65 枚から選んで、半角英数のファイル名にコピーしました。元のスクリーンショットは、記事から参照していません。

| ファイル名 | 元のスクショ（撮影時刻） | 内容 | 記事内の位置 |
| ---------- | ------------------------ | ---- | ------------ |
| `demo-01-devcontainer-settings.png` | 21:37:15 | `chat.agentHost.devContainer` の設定一覧 | ① B |
| `demo-02-handoff-setting.png` | 21:51:01 | Handoff: Enabled にチェック | ① B |
| `demo-03-remote-environments-create.png` | 21:49:43 | Create Dev Container リンク（赤枠） | ① B |
| `demo-04-dev-container-listed.png` | 21:49:59 | Dev Container Ubuntu の行（赤枠） | ① B |
| `demo-05-env-picker.png` | 21:50:33 | Environment ピッカーに Dev Container | ① B |
| `demo-06-handoff-prompt.png` | 22:06:12 | handoff の依頼を入力 | ② |
| `demo-07-approve-create-container.png` | 22:06:40 | Create Dev Container? の承認 | ② |
| `demo-08-approve-remote-session.png` | 22:08:55 | Create Remote Session? の承認 | ② |
| `demo-09-handoff-open-link.png` | 22:09:19 | 元の会話に出たセッションへのリンク | ② |
| `demo-10-approve-terminal.png` | 22:13:23 | Python を入れるコマンドの承認 | ② |
| `demo-11-handoff-result.png` | 22:14:23 | Python 3.15.2 のインストール結果 | ② |
| `demo-12-origin-report.png` | 22:16:04 | 元の会話に戻った報告 | ② |
| `demo-13-container-os-check.png` | 22:01:22 | OS と作業ディレクトリ | ② |
| `demo-14-no-files-no-gh.png` | 22:04:16 | ファイルなし、gh なし（赤枠） | ② |
| `demo-15-manage-sandbox-profiles.png` | 22:18:46 | Manage Sandbox Profiles | ③ |
| `demo-16-profile-whole.png` | 22:20:41 | GitHub Only の編集画面 | ③ |
| `demo-17-assign-profile.png` | 22:22:16 | Sandbox Profile 列で割り当て | ③ |
| `demo-18-policy-network.png` | 22:24:33 | `/sandbox policy` の Network / Capabilities | ③ |
| `demo-19-unshare-error.png` | 22:25:53 | unshare 失敗の説明 | ③ 先にハマった点 |
| `demo-20-bwrap-missing.png` | 22:28:55 | bubblewrap が無い | ③ 先にハマった点 |
| `demo-21-curl-both-200.png` | 22:37:54 | Bypass オンのとき、どちらも 200 | ③ |
| `demo-22-proxy-env.png` | 22:58:04 | プロキシの環境変数 | ③ |
| `demo-23-noproxy-test.png` | 23:00:53 | `curl -sv` と `--noproxy` | ③ |
| `demo-24-allow-sandbox-bypass.png` | 23:01:58 | Allow Sandbox Bypass（赤枠） | ③ |
| `demo-25-curl-blocked-403.png` | 23:03:11 | Bypass オフ後、example.com が 403 | ③ |

> 以下の手順は、撮影前に書いた計画です。ファイル名は上の表が最新です。

撮れなかった画像は、記事の該当する `![...](...)` の1行を削除してください（文章だけで成立するようにしてあります）。

## 撮影前のチェック

- [ ] 個人情報・API キー・トークン・**社内のリポジトリ名やホスト名・IP アドレス・SSH のユーザー名**が映り込んでいない
- [ ] 通知、ブラウザのタブ、メニューバー、ユーザー名（パスなど）にも注意する
- [ ] ダークテーマ、ウィンドウ幅は広め（全画像で揃える。目安 1200〜1400px）
- [ ] 1枚で「何が分かるか」を1つに絞る
- [ ] 保存するファイル名は ASCII のみ（日本語・スペースは URL で壊れやすい）
- [ ] VS Code は **1.148 以降**（`Help > About` で確認）
- [ ] ステータス表記（Experimental）が画面に出るものは、必ず写す

## 事前準備

| 項目 | 内容 |
| ---- | ---- |
| VS Code | 1.148 以降の Stable（`Check for Updates`） |
| Docker | 動いていること。`docker version` が通ること。**Dev Container を作るホストに必要**。今回は **WSL（Ubuntu 24.04, aarch64）の中に Docker Engine 29.1.3（apt の `docker.io`）を入れた**。入れたあとは `wsl --shutdown` で WSL を再起動して、docker グループを反映させた |
| リモート環境 | デモ③（Sandbox profiles）に1つ。テスト計画は SSH か Dev Tunnel だが、今回は**作成済みの Dev Container（`Dev Container Ubuntu`）と WSL（Ubuntu）**を使う。SSH の2行（`alias` / `vscode145-demo`）は Available のままで、ドロップダウンが選べない |
| サンドボックスの依存 | WSL / コンテナの Linux には `bubblewrap`（0.5.0 以降）、`slirp4netns`、util-linux 2.35 以降、`iptables` が必要。**WSL の Ubuntu は、`bubblewrap` と `slirp4netns` が未インストール**（確認済み）。デモ③の前に、`/sandbox policy` が動くかを確認する（3-0 を参照） |
| リモート側 | VS Code Server が最新であること（Sandbox profiles の前提） |
| Copilot | Agents ウィンドウでセッションを動かせる状態（Copilot harness を選ぶ） |
| 検証用 | 公開してよい小さなリポジトリ（Dev Container の A は使わないなら不要） |

`settings.json`（User）に次を入れて、ウィンドウを再読み込みします。

```json
{
  "chat.agentHost.devContainer.environments.enabled": true,
  "chat.agentHost.devContainer.handoff.enabled": true,
  "chat.agent.sandbox.profiles.enabled": true
}
```

Agents ウィンドウは、`Chat: Open Agents window` か、`code --agents` で開きます。

使う環境をここにメモしておきます（記事の [TODO] に書く）。

- OS / バージョン: Windows 上の WSL2（Ubuntu 24.04.4 LTS、aarch64 / ARM の Surface）
- Docker の種類: Docker Engine 29.1.3（WSL の Ubuntu に apt で導入。Docker Desktop ではない）
- リモートの種類: WSL（Ubuntu）と、その上に作った Dev Container（`Dev Container Ubuntu`）

> ARM（aarch64）の環境です。記事には「検証は WSL2 / ARM」と一言入れておくと、再現するときの手がかりになります。

---

## デモ 1: 設定ファイル不要の Dev Container を作る（demo-01 〜 demo-04）

### 1-1. 設定を撮る（demo-01）

1. `Ctrl+,`（Mac は `Cmd+,`）で設定を開き、検索欄に `chat.agentHost.devContainer` と入力する
2. `environments.enabled` と `handoff.enabled` がオンになっている状態にする
3. 📸 **撮影タイミング**: 2つの設定が1画面に収まっていて、Experimental のタグが見えている瞬間

### 1-2. Remote Environments でコンテナを作る（demo-02, demo-03）

**今回の状況**: コンテナ `Dev Container Ubuntu` は**作成済み**（Dev Containers グループに Connected で並んでいる。行に **New Session** ボタンと **`...`**、Sandbox Profile のドロップダウンがある）。以降は、これを使う。

実際にハマった点（記事の「注意」に使える）:

- 最初は、Dev Containers グループが出なかった。原因は **WSL に Docker が入っていなかった**こと。Docker を入れて `wsl --shutdown` したあとに、グループが出た
- WSL の Ubuntu 行の **`...`（More Actions）** には、Docker が無い間は **Create Dev Container が出なかった**（New Session / Disconnect / Share as GitHub Environment / Hide from Environment Picker / Rename / Troubleshoot Connection だけ）。作成は、**Dev Containers グループの Create Dev Container リンク**から行った
- 「Allow Connections Here」（Off / GitHub Environments / Dev Tunnels）は、この PC を**外部に共有する**スイッチで、Dev Container の作成とは無関係。Off のままにする

手順:

1. コマンドパレットで **Agents: Manage Remote Environments** を実行する
2. 検索欄右の **Filter（じょうご）** を開いて、**Group By > Type** を選ぶ
3. 📸 **撮影タイミング①（demo-02）**: **Dev Containers** グループが見えている画面。コンテナを作る**前**なら「No Dev Containers yet.」と **Create Dev Container** リンクが出ている（撮れていればそれ。作成済みなら、手順 5 の画面で代用してよい）
4. 📸 **撮影タイミング②（demo-03）**: 作成**後**の行。`Dev Container Ubuntu` が **Connected**、System が Linux、右に **New Session** と **`...`** が見える
   - 作成中の進捗を撮りたい場合は、**Delete して作り直す**必要がある（Delete はコンテナと Docker ボリュームを消す。今のコンテナは後続のデモで使うので、デモがすべて終わってから）
   - 記事の alt テキストも、これに合わせて「作成された Dev Container が Connected で並んでいる様子」に変えてある
5. 作成にかかった時間は、記録していないので不明。作り直すときに計る: ____________ 秒
6. `...` のメニューにある項目を、記事の補足用にメモする（Create Dev Container 以外に何があるか）: ____________

### 1-3. コンテナで新しいセッションを始める（demo-04）

1. Agents ウィンドウで **New Session** を押す（Remote Environments の `Dev Container Ubuntu` の行の **New Session** ボタンからも始められる）
2. **Environment** ピッカーを開く
3. 📸 **撮影タイミング**: `Dev Container Ubuntu` がピッカーに並んでいて、選ぼうとしている瞬間
4. コンテナを選んで、ハーネスを選ぶ（Copilot）

> 撮影のコツ: 次の demo-07 でこのセッションを使うので、まだ依頼は送らなくていい。

---

## デモ 2: handoff で「隔離環境で試して」と頼む（demo-05 〜 demo-07）

前提: `handoff.enabled` がオン。**元のセッションは、コンテナの中ではなく、Docker が入っているホストのセッション**にする。

今回、Docker は **WSL の Ubuntu だけ**に入っている。handoff は、既定で「今のセッションが動いているホスト」にコンテナを作るので、**元のセッションは WSL（Ubuntu）で動かす**（Windows 側の This Computer には Docker が無いので、失敗しうる）。テスト計画も、「This Computer か WSL のセッションから頼む」としている。

すでにある `Dev Container Ubuntu` は使わず、handoff が**もう1つ新しいコンテナ**を作る流れになる。Remote Environments の Dev Containers グループが、1 → 2 に増えるのも撮っておくと、記事に使える。

### 2-1. 依頼する（demo-05）

1. Agents ウィンドウで **New Session** を押して、Environment ピッカーで **Ubuntu（WSL）** を選ぶ。ハーネスは Copilot
2. 次の依頼を送る

   ```text
   最新の Python を試したいので、この WSL の Ubuntu に隔離された Dev Container を作って、
   その中の新しいセッションで続きをやって。終わったらここで報告して。
   ```

3. 📸 **撮影タイミング**: コンテナを作るホストと、新しいセッションの**承認**が出ている瞬間（ホスト名が内部 ID ではなく、分かる名前で出ているかも見る）
   - **実際の結果**: 1つ目の承認「Create Dev Container?」は「on Ubuntu」と分かる名前で出た（`Allow in this Session` / `Skip`）。コンテナ作成後は、チャットに「Created Dev Container 2 on Ubuntu」のリンクが出た
   - 2つ目の承認「Create Remote Session?」は、ホストが `agenthost-devcontainer_<ID>` という**内部 ID の形**で出た（Issue #349763「承認が内部 ホスト ID を出す」と同じ症状。Issue はクローズ済みだが、この環境では出た）。承認文には、日本語の依頼が英語に要約されて入り、「This Dev Container (Ubuntu base image) is empty; nothing was copied from the origin session.」と書かれていた。次のステップに「必要なら、元のセッションにコードベースの中身を聞く」とある
   - 📸 `demo-05b-handoff-remote-session-approval.png` として、この2つ目の承認も撮っておく（記事の「渡るのは要約だけ」で使える）
4. 承認する

### 2-2. 新しいセッションを確認する（demo-06）

1. コンテナの中で、新しいセッションが始まるのを待つ
2. 📸 **撮影タイミング**: コンテナの中のセッションが動いていて、元の会話から**リンク**が出ている状態（2画面を並べるか、元の会話側に出たリンクを撮る）
3. セッションが終わったら、元の会話に**報告**が戻るかを確認する（結果をメモ: ____________）
   - **実際の結果（1つ目）**: 元の会話に「Try latest Python in Dev Container を開く」というリンクが出た。「Completed 7 steps in 46s」（承認待ちを含む）、モデルは Claude Sonnet 5.5（Copilot Fusion が自動選択）、10.1 credits。本文には、コンテナ名「Dev Container 2」、新セッションの作業（最新の安定版 Python を入れて `python --version` で確認）、「完了またはブロックされた時点で、こちらのセッションに報告が届く」と書かれていた
   - **注意として書かれていたこと**: 入力欄の `codebase` の添付内容は、エージェントが読めず、コンテナにも渡せなかった。新セッションには、必要なら元のセッションにリポジトリやファイルを問い合わせるよう伝えてある。つまり、**添付も渡らない**（要約だけ）。記事の「渡るのは要約だけ」の裏付けになる
   - 📸 `demo-06-handoff-new-session.png`: このリンクを赤枠で囲んだ画面でもよい。リンクを押して開いた、コンテナ内のセッションも撮る
   - **リンクの不具合**: 元の会話の「Try latest Python in Dev Container を開く」を押すと、「Unable to open '<セッションID>'. The editor could not be opened because the file was not found.」（Create File / Cancel）が出た。**Create File は押さない**。サイドバーのセッション一覧から開けた（📸 `demo-error-handoff-link.png`）
   - **コンテナ内のセッション**: ワークスペースは `/workspaces/ubuntu-2`、モデルは Claude Haiku 4.5（元は Claude Sonnet 5.5）、作成元は「WSL UbuntuでDev Container作成」と表示された。最初に「Fetch URL?」で `https://astral.sh/uv/install.sh` の承認が出た（Allow Once）。続けて、元のセッションへ報告する「Send Remote Message」の承認が出た（Allow in this Session。宛先は `remote-hex-...` の内部 ID の形）
   - **結果**: 「Completed 5 steps in 23s」。Python 3.15.2 を uv で入れて `python3.15 --version` を確認（インタープリターは `/home/vscode/.local/share/uv/python/cpython-3.15-linux-aarch64-gnu/bin/python3.15`、uv は `~/.local/bin`）。コンテナには**システムの Python が元々無かった**。コンテナは空で `Codebase` の添付も渡らなかったので、実作業はまだ始めず、元のセッションに「リポジトリの URL かファイル、タスクの詳細」を聞くメッセージを送った（キューに入った）
   - **裏取り（WSL 側から）**: 動いていたコンテナは `mcr.microsoft.com/devcontainers/base:ubuntu` を使う 2 つ（1つ目、handoff で作った 2 つ目）。2 つ目のコンテナの中で `python3.15 --version` は 3.15.2。WSL 側は `python3` が 3.12.3 のままで、uv も入っていない（隔離できている）
   - 📸 `demo-06b-container-session-python.png`（承認前の画面）、`demo-06c-report-back-approval.png`（報告の承認）、完了の画面もあれば撮る

### 2-3. コンテナの中を確認する（demo-07）

目的は、「本当に隔離された Linux で動いている」ことと、「元のファイルが渡っていない」ことを示すことです。**ファイルは変更させません**。

1. コンテナの中のセッションに、次の依頼を送る

   ```text
   ファイルは変更しないで、OS の種類と、今の作業ディレクトリを教えて。
   ```

2. 📸 **撮影タイミング**: OS（Ubuntu など）と作業ディレクトリが返ってきた瞬間
3. 続けて、読み取りだけの依頼で、元のプロジェクトのファイルが無いことを確認する

   ```text
   ファイルは変更しないで、今の作業ディレクトリのファイル一覧を教えて。
   ```

4. 結果をメモする

   - 返ってきた OS / 作業ディレクトリ: Linux / `/home/vscode/.copilot/chats/<セッションID>`（ユーザーは `vscode`。プロジェクトのフォルダではなく、チャット専用のディレクトリ）
   - 初回の送信は「new session is not ready」で失敗し、再送信で成功した（#348707 と似た症状）。応答は 15 秒、3 ステップ
   - 元のプロジェクトのファイル: **無い**（「現在の作業ディレクトリにはファイルがありません」。5 秒、2 ステップ）
   - 作成からセッション開始までの時間: ____________

### 2-4. 認証情報が渡っているかを確認する（記事の [TODO] 用。画像は不要）

記事で「コンテナにどの認証情報が入るかは確認していない」と書いている点です。**値は絶対にチャットや画像に出さない**でください。

1. コンテナ内のセッションに、読み取りだけで頼む

   ```text
   ファイルは変更しないで、gh auth status と git config --global --list を実行して、
   ログイン状態（ログイン済みか）だけ教えて。トークンやメールアドレスの値は表示しないで。
   ```

2. 結果をメモする: `gh` コマンドは**コンテナに入っていない**（インストールされていない）ので、GitHub のログイン状態は確認できなかった。`git config --global --list` は実行済み（中身の有無は未確認）。画面上部は「No workspace [Dev Container]」、入力欄は「Chat with Copilot [Dev Container on Ubuntu]」と出ていた
3. 結果を、記事の `<!-- [TODO] 実機で試した結果を書く -->` の場所に書く

---

## デモ 3: Sandbox profiles（demo-08 〜 demo-11）

前提: `chat.agent.sandbox.profiles.enabled` がオン（Remote Environments に **Sandbox Profile 列**が出ているので、オンになっている）。

**割り当て先**: SSH の2行は Available のままで選べないので、**接続済みの行**を使う。候補は2つ。

| 候補 | 良い点 | 注意 |
| ---- | ------ | ---- |
| `Dev Container Ubuntu`（おすすめ） | 「リモートのコンテナにプロファイルを割り当てる」という、提案 Issue（#349201）の例そのもの。記事の流れとも合う | Ubuntu の素のコンテナに、サンドボックスの依存（`bubblewrap` など）が入っているか分からない |
| `Ubuntu`（WSL） | 手元で依存を入れやすい | WSL に `bubblewrap` と `slirp4netns` が**未インストール**。入れないと、サンドボックスがオンのコマンドは動かない（黙って外では動かない） |

### 3-0. サンドボックスが動くか、先に確認する

1. 割り当て先のホストで**新しいセッション**を始めて、`/sandbox policy` を実行する（プロファイル無し、Default のままでよい）
2. レポートが開いて、実行マシンと状態が出れば OK
3. 「依存が足りない」のようなメッセージが出たら、メモして（記事の「ハマった点」に使える）、次のどちらかをする
   - WSL の場合: Ubuntu に `bubblewrap` と `slirp4netns` を入れる。**今回は入れた**（`bubblewrap` 0.9.0、`slirp4netns` 1.2.1）。公式の要件は、`bubblewrap` 0.5.0 以降、`slirp4netns`、util-linux 2.35 以降、互換性のある `iptables`。WSL1 は非対応
   - コンテナの場合: **`Dev Container Ubuntu`（1つ目。Ubuntu 26.04.1）には、`bwrap`・`slirp4netns`・`iptables` はすでに入っていた**（読み取りだけで確認）。ただし、`/dev/net/tun` が**無く**、Docker の `SecurityOpt` / `Devices` も**空**。公式ドキュメントは、サンドボックスを使うには `--security-opt seccomp=unconfined` / `apparmor=unconfined` / `systempaths=unconfined` と `--device /dev/net/tun` が要り、**サンドボックスをオンにして新しく作った Dev Container セッションには VS Code がこれを足す。それ以前に作ったコンテナは、サンドボックスをオンにして作り直す必要がある**と書いている。このコンテナは、作成時にサンドボックスがオフだったので、**サンドボックス付きのコマンドが失敗する可能性が高い**
   - その場合の手順: ①まず、そのまま `/sandbox policy` と `curl` を試して、エラーの文面を撮る（記事の「ハマった点」）。②動かなければ、コンテナを Delete して、**サンドボックスをオンにしてから**作り直す（`chat.agent.sandbox.enabled` を `on`）。③それでも動かなければ、WSL の Ubuntu 行に切り替える
4. 結果をメモする: **`Dev Container Ubuntu`（1つ目）では、`/sandbox policy` は動いた（許可ドメイン `github.com`、Local network blocked など、プロファイルの値が出た。画面には `□[1m` のような制御文字が見えた）が、サンドボックス付きの `curl` は起動しなかった**
   - エージェントの返答: 「1. `curl -sI https://github.com`: 失敗。サンドボックスのネットワークが使えず、コマンドが起動しませんでした。2. example.com: 未実行」。原因は「サンドボックス用のプライベートネットワークを作れない（`unshare --user --net` が失敗）。Ubuntu 24.04 以降なら AppArmor の `kernel.apparmor_restrict_unprivileged_userns=1` が考えられる」と推測していた（Claude Sonnet 5.5、8 秒、3 ステップ）
   - **裏取り（WSL 側から）**: コンテナの中では、**root でも** `unshare --user --net true` が「Operation not permitted」で失敗した。一方、WSL（Ubuntu）では `bwrap` も `unshare` も成功し、AppArmor の該当設定も存在しない。つまり、エージェントの推測（AppArmor）とは違い、コンテナ側の制限（公式ドキュメントが言う、Docker の既定の seccomp など）が原因と考えられる。コンテナには `SecurityOpt` も `/dev/net/tun` も無い
   - **やってはいけない対処**: エージェントの提案どおりにホストの sysctl を変えたり、サンドボックスのポリシーを緩めたりしない（隔離を弱めるだけ）
   - 📸 `demo-error-sandbox-in-container.png`: このエラーの返答。記事の「ハマった点」に使う
   - 次の対処: ①（すぐ撮れる）プロファイルの割り当て先を **WSL の Ubuntu 行**に切り替えて、`curl` を試す。②（公式の対処）`chat.agent.sandbox.enabled` を `on` にして、コンテナを作り直す（Delete して Create）。②で、サンドボックス付きの Dev Container が動くかも確かめる

### 3-1. プロファイルを作る（demo-08）

1. コマンドパレットで **Sandbox: Manage Sandbox Profiles** を実行する
2. **New Profile** を選ぶ。作成直後の値が、Settings エディタのサンドボックス設定と同じかを確認する
3. 名前を `GitHub Only` にして、**Enabled** を `on`、**Allowed Domains** を `github.com` にする
4. 📸 **撮影タイミング**: プロファイルの編集画面（名前・Enabled・Allowed Domains が見える）。**実際の画面は、Create ボタンが無く、自動保存**だった（「Changes are saved automatically and update the connected hosts using this profile」）
5. 編集できる項目（記事に反映済み）: Sandbox（Enabled / Allow Sandbox Bypass / Sandbox MCP Servers / Sandbox LSP Servers）、Network（Allow Outbound Connections / Allowed Domains / Denied Domains / Allow Local Network）、File System（Allow Dev Tool Access / User-Configured Paths）、Credentials（Authenticate git / Authenticate gh）
6. 左の一覧に `GitHub Only` が出ていることを確認する

### 3-2. ホストに割り当てる（demo-09）

1. **Agents: Manage Remote Environments** を開く（Group By > Type のままでよい）
2. 📸 **撮影タイミング**: 3-0 で決めた行（`Dev Container Ubuntu` か `Ubuntu`）の **Sandbox Profile** 列のドロップダウンを開いて、`GitHub Only` と `Default` が見えている瞬間
3. `GitHub Only` を選ぶ
4. 撮影のときは、`alias`、`vscode145-demo`、`surface007` にモザイクを入れる（`demo-02` も同様）

### 3-3. 効いているか確認する（demo-10, demo-11）

1. 割り当てたホスト（`Dev Container Ubuntu` か `Ubuntu`）で**新しいセッション**を始めて、`/sandbox policy` を実行する
2. 📸 **撮影タイミング①（demo-10）**: レポートが開いて、許可ドメインが `github.com` だけになっている画面
3. エージェントに、次の2つを頼む（**読み取りだけ**のコマンド）

   ```text
   次の2つを順番に実行して、それぞれ成功したか失敗したかだけ教えて。
   1. curl -sI https://github.com
   2. curl -sI https://example.com
   ```

4. 📸 **撮影タイミング②（demo-11）**: 1つ目が成功、2つ目が失敗している結果
5. 失敗しないとき / 両方失敗するときは、メモして、次の2点を確認する

   - **実際の結果（WSL の Ubuntu、`GitHub Only` 割り当て、サンドボックス有効）**: 初回は github.com も example.com も `200`・exit 0。Denied Domains に `example.com` を足して新しいセッションで試しても 200 のままで、レポートには `Deny: example.com` と `Allow (layer 1): github.com` が出ていた（ポリシー表示と通信が食い違った）
   - **原因（ユーザーが特定）**: プロファイルの **Allow Sandbox Bypass がオン**だった。オフにして新しいセッションで試したら、github.com は `200`・exit 0、example.com は `curl: (56) CONNECT tunnel failed, response 403`・`000`・exit 56 になった（プロキシが拒否）。ユーザーの観察では、オンのときは CONNECT の形跡がなく、`--noproxy '*'` でも同じ結果、プロキシ環境変数が無いセッションもあった（※私が見たセッションでは、プロキシ環境変数 `10.0.2.2:41819` はあった。セッションによって違う）
   - 承認ダイアログは、オンのときも見ていない（公式は「ユーザー確認のうえで」と書く）。なぜ外で動いたかは断定しない。**要再現**: オンに戻して、承認の画面が出るかを確認する
   - 📸 `demo-12-allow-sandbox-bypass.png`（Bypass がオンの画面。赤枠）、`demo-11-curl-allowed-denied.png`（オフにした後の `curl` 結果）。`demo-11b`（両方 200）は、記事では使っていないが、「オンのとき」の画面として別途撮れていれば記事に足してもよい
   - 設定変更は、新しいセッションかウィンドウの再読み込みで確実に反映される
   - Windows のリモートか（`chat.agent.sandbox.network.allowLocalNetwork` が要る場合がある）（`chat.agent.sandbox.network.allowLocalNetwork` が要る場合がある）
   - `/sandbox policy` が、プロファイルの値を示しているか

### 3-4. 記事の表の裏取り（任意。画像は不要）

記事の「動きのルールを整理」の表は、テスト計画からの引用です。時間があれば、自分でも確認して、結果を記事に書き足します。

| 試すこと | 期待する結果（テスト計画より） | 実際の結果 |
| -------- | ------------------------------ | ---------- |
| プロファイルを編集して、新しいセッションを始める | 割り当て直さなくても、反映される | |
| 割り当て中のプロファイルを削除する | ブロックされ、リモート名が出る | |
| 接続を切って、列のドロップダウンにカーソルを置く | 無効になり、接続を促す表示が出る | |
| 別の端末から同じリモートに繋ぐ | `(on host)` 付きで出て、Save to My Profiles がある | |
| セッションの **Sandboxing for terminal** をオフにして、`curl` を実行する | そのセッションだけ成功する。他のセッションには影響しない | |
| `profiles.enabled` を `false` にする | コマンドと列が消える。リモートの割り当ては残る | |

---

## 撮影後のチェック

- [ ] `images/` に `demo-01` 〜 `demo-11` が揃っている（撮れなかった分は、記事から該当の行を削除した）
- [ ] 個人情報、ホスト名、IP アドレス、トークン、ユーザー名が映っていない
- [ ] 記事の `<!-- [TODO] ... -->` コメント3か所（handoff の結果・Sandbox profiles の結果・Dev Container × Sandbox）を、撮影時の結果で書き換えた
- [ ] 記事冒頭の `<!-- 【公開前 TODO】 ... -->` コメントを削除した
- [ ] `git add` → `commit` → `push` して、raw URL が表示されることを確認した

## 片付け

撮影が終わったら、作ったものを消します。

- [ ] 設定ファイル不要のコンテナは、Remote Environments の行の **Delete** で消す（**コンテナと Docker ボリュームが消えます**。必要なものは先に保存）
- [ ] 検証用の `GitHub Only` プロファイルは、割り当てを **Default** に戻してから削除する（割り当て中は削除できません）
- [ ] 必要なら、`chat.agentHost.devContainer.*` と `chat.agent.sandbox.profiles.enabled` を元に戻す
