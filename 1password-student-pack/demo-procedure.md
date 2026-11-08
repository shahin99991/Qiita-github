# デモ手順 & スクショ撮影タイミング

「学生なら1Passwordが2年間無料！GitHub Student Developer Pack の特典を、必要性とセキュリティの面から整理した」記事用の、デモ手順と画像の一覧です。

- 記事本体: [article-qiita.md](./article-qiita.md)
- レビュー用プレビュー: [article-preview.md](./article-preview.md)
- 画像保存先: `./images/`
- 画像URL形式: `https://raw.githubusercontent.com/shahin99991/Qiita-github/main/1password-student-pack/images/<ファイル名>`
- 差し替え方法: 同名で `./images/` に上書き → push（記事側の URL 変更は不要）

> ⚠️ **公開前の注意**: 画像を GitHub に push するまで raw URL は 404 になります。記事の `ignorePublish: true` は、画像を push したあとで `false` にしてください。

---

## 1. 撮影済みの画像（記事で使用中）

2026-11-07 / 11-08 に撮影。赤枠は撮影時に入れたもの。元ファイルは `images/_original/`（`.gitignore` 済み）に退避してあります。

| ファイル | 記事内の位置 | 写っているもの |
| -------- | ------------ | -------------- |
| `demo-01-claim-page` | Step 1 | 学生向けページ。見出し「Get two years of 1Password for free」と Sign in with GitHub |
| `demo-02a-github-account-select` | Step 2 | GitHub のアカウント選択（Continue） |
| `demo-02b-github-authorize` | Step 2 | 認可画面。権限は Public data only |
| `demo-03a-region-select` | Step 3 | 保管地域の選択（US / CA / EU） |
| `demo-03b-create-account-button` | Step 3 | Create an account / Sign in |
| `demo-04-welcome-add-extension` | Step 4 | 日本語の案内ページ「2年間無料で利用しましょう」 |
| `demo-05a-chrome-web-store` | Step 5 | Chrome ウェブストアの拡張ページ |
| `demo-05b-chrome-add-extension` | Step 5 | 拡張の追加ダイアログ（要求される権限） |
| `demo-06a-signup-form` | Step 6 | アカウント作成フォーム（空）。URL は黒塗り済み |
| `demo-06b-signup-form-filled` | Step 6 | 氏名入力済み。メールアドレスは赤塗り済み |
| `demo-07a-setup-start` | Step 7 | セットアップを開始 |
| `demo-07b-setup-ready` | Step 7 | 準備、設定、インターネット |
| `demo-08-extension-vault` | Step 7 | 拡張の保管庫。アカウント情報のユーザー名は赤塗り済み |
| `demo-09a-github-ssh-title` | SSH キー作成 | Title 欄に出る「SSHキーの作成...」 |
| `demo-09b-github-ssh-key-field` | SSH キー作成 | Key 欄のメニュー。Key type は Authentication Key |
| `demo-09c-create-ssh-dialog` | SSH キー作成 | 作成ダイアログ（Ed25519・保管庫「個人」） |
| `demo-09d-ssh-key-saved` | SSH キー作成 | 公開鍵が自動入力され、保存完了の通知が出た画面 |
| `demo-10a-desktop-signin` | SSH Agent | デスクトップアプリのサインイン画面 |
| `demo-10b-desktop-developer-page` | SSH Agent | 「開発者」画面（SSH エージェント / 環境 / CLI / Watchtower / MCP サーバー） |
| `demo-10c-ssh-agent-setup-button` | SSH Agent | SSH エージェントの設定ボタン |
| `demo-10d-key-name-dialog` | SSH Agent | キー名をディスクに保存するかの確認ダイアログ |
| `demo-10e-openssh-disable-dialog` | SSH Agent | OpenSSH を無効にしているかの確認ダイアログ |
| `demo-10f-ssh-agent-running` | SSH Agent | 「実行中」と、利用できる SSH キーに GitHub が出た画面 |

解説図（GPT Image 2.5 で生成。ウォーターマークなしで再生成済み）は `img-00-tldr-overview` / `img-01-why-secrets` / `img-02-ssh-agent-before-after` / `img-03-agent-credentials` です。

### 公開前に目視で確認すること

- [ ] `demo-06b` / `demo-08` / `demo-09d` の赤塗りが、拡大しても読めない状態になっている
- [ ] `demo-09d` に写っている公開鍵（赤塗り以外の部分）に問題がない（公開鍵は秘密ではないが、念のため）
- [ ] `demo-06a` のアドレスバーが黒塗りされている
- [ ] `demo-10f` のキーのフィンガープリントが赤塗りされ、拡大しても読めない
- [ ] 解説図 `img-02` の Before パネルで、`~/.ssh/id_ed25519` が2か所に出ている（気になる場合は再生成）

---

## 2. 未撮影・未検証（記事では「公式ドキュメントより・未検証」と明記）

実際に試して、結果を記事に反映したい項目です。試したら、記事の「ここから先」の節を実機ベースに書き換えてください。

### 事前準備

- [x] 1Password のデスクトップアプリをインストールし、SSH Agent を有効化した（demo-10a〜10f）
- [ ] Git が 2.34 以降か確認する: `git --version`
- [ ] 検証用の空リポジトリを GitHub に作る
- [ ] 画面に出るメールアドレス・Secret Key・Emergency Kit・マスターパスワードは写さない（写ったらモザイク）
- [ ] 作業環境（Windows / WSL / macOS / Linux）をメモする。WSL から Git を使う場合は、公式ドキュメントの「1Password WSL integration」が必要

### 撮影ごとの手順（優先度順）

| 優先 | 予定ファイル名 | 操作 | 撮るタイミング | 確認すること |
| ---- | -------------- | ---- | -------------- | ------------ |
| 高 | `demo-11-ssh-auth-test` | ターミナルで `ssh -T git@github.com` | 1Password の承認ダイアログが出た瞬間と、`Hi <ユーザー名>! You've successfully authenticated` が出た結果（2枚に分けてもよい） | SSH Agent 経由で本当に認証できたか。承認の求められ方 |
| 高 | `demo-12-github-signing-key` | GitHub の SSH キー登録画面で、同じ公開鍵を Key type: Signing Key として登録 | Key type が Signing Key になった状態（保存前） | Authentication Key と別に登録できたか |
| 高 | `demo-13-commit-signing-config` | 保管庫の SSH キーを開く → メニュー → Configure Commit Signing → Edit Automatically | Edit Automatically と Copy Snippet の2択が見えるダイアログ | `git config --global --list` に `gpg.format=ssh` / `commit.gpgsign=true` が入ったか |
| 高 | `demo-14-verified-badge` | 検証用リポジトリで `git commit --allow-empty -m "test: signed commit with 1Password"` → `git log --show-signature -1` → `git push` し、GitHub のコミット一覧を開く | コミットに Verified バッジが付いた状態 | Verified になったか。ならなければ原因（Key type、`user.email`）。承認が出る回数 |
| 中 | `demo-15-subscription-end-date` | 1Password のアカウント設定（プラン・請求まわり） | 無料期間の終了日が分かる画面。メールアドレスは伏せる | 「2年」が契約情報として確認できるか。クレジットカード登録を求められていないか |
| 低 | `demo-16-op-run` | `op run --env-file=.env -- <コマンド>` | シークレット参照（`op://...`）が展開された結果。値そのものは写さない | 1Password CLI のインストールが必要 |

### 撮影後にやること

1. 画像を `./images/` に保存する
2. 記事の「ここから先」の節を、結果に合わせて書き換える（「未検証」の注意書きを外す）
3. 記事冒頭コメントの「未検証」リストと、TL;DR の表を更新する
4. `article-preview.md` を作り直す（記事を変更したら再生成）
5. push して raw URL が開けることを確認し、`ignorePublish` を `false` にして公開する
