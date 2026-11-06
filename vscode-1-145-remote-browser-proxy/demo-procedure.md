# デモ手順とスクショ撮影ガイド：Remote browser proxy（VS Code 1.145）

記事: [article-qiita.md](./article-qiita.md)
保存先: `vscode-1-145-remote-browser-proxy/images/`（記事の画像パスと同じファイル名で保存する）

## 撮影済みスクショ（2026-11-06）

| ファイル名                                | 内容                                                          |
| ----------------------------------------- | ------------------------------------------------------------- |
| `demo-01-setting-description.png`         | Enable Remote Proxy の説明文（オフ）                          |
| `demo-01-enable-remote-proxy.png`         | Enable Remote Proxy をオン                                    |
| `demo-01-data-storage.png`                | `workbench.browser.dataStorage` = default                     |
| `demo-02a-environment-picker.png`         | 接続先ドロップダウン（SSH を選択）                            |
| `demo-02b-connect-via-ssh.png`            | Connect via SSH で `vscode145-demo` を選択                    |
| `demo-02c-select-folder.png`              | リモートのフォルダーを選択                                    |
| `demo-03-prompt-start-app.png`            | プロンプト入力                                                |
| `demo-04a-agent-working.png`              | エージェント作業中                                            |
| `demo-04-browser-remote-preview.png`      | 統合ブラウザにリモートのアプリが表示                          |
| `demo-05-playwright-duplicate-check.png`  | 重複登録テスト後の画面                                        |
| `demo-06-share-with-agent.png`            | ツールバー（Sharing with Agent）の切り出し                    |
| `demo-07-agent-summary.png`               | エージェントの完了報告                                        |

**未撮影（記事では「未検証」と明記）**: Comment on Elements、モバイル幅での再確認、切断時のインジケーター（旧 demo-05 / demo-07 / demo-08）。
元のスクショは `images/_original/` に退避済み。

以下は撮影前に作った元の手順（追加検証用に残している）。

## スクショ一覧（元の計画）

| ファイル名                           | 記事内の位置                 | 撮るタイミング                                                       |
| ------------------------------------ | ---------------------------- | -------------------------------------------------------------------- |
| `demo-01-enable-remote-proxy.png`    | 設定をオンにする             | 設定画面で `workbench.browser.enableRemoteProxy` がオンの状態        |
| `demo-02-connect-remote-host.png`    | リモートホストに接続         | 環境ドロップダウンでリモートホストに接続し、フォルダー選択後         |
| `demo-03-prompt-start-app.png`       | エージェントに依頼           | プロンプトを送信した直後のチャット画面                               |
| `demo-04-browser-remote-indicator.png` | 統合ブラウザで確認         | 統合ブラウザに `localhost:3000` が表示され、アドレスバーのインジケーターが見える状態 |
| `demo-05-comment-on-elements.png`    | プレビューしてコメント       | Comment on Elements で要素を選び、コメントを入力している途中         |
| `demo-06-share-with-agent.png`       | Share with Agent             | ツールバーで共有済みの表示（インジケーター）が出ている状態           |
| `demo-07-after-fix.png`              | 直してもらった後             | エージェントが修正し、モバイル幅で再確認した画面                     |
| `demo-08-disconnected.png`（任意）   | 知っておきたい挙動           | ホスト切断時にインジケーターが切断状態になっている様子               |

## 事前準備

- [ ] 手元の VS Code を 1.145 以降に更新する（Check for Updates）
- [ ] リモートホスト側の VS Code（Agent Host）も 1.145 以降にする
  - SSH 先: 接続時に VS Code が必要な CLI を入れる。古い場合は一度接続し直して更新を確認する
- [ ] 接続方法を決める（SSH が一番手軽。Dev Tunnels の場合は**認証必須**で作る）
- [ ] リモートホストに Node.js を入れておく（デモ用の小さな Web アプリを動かすため）
- [ ] デモ用の空フォルダー（例: `~/demo-signup-app`）をリモートに作る
- [ ] 機密情報が映り込まない画面にする（ホスト名やユーザー名、トークンは撮影前に確認。必要ならモザイクを入れる）
- [ ] スクショは同じウィンドウサイズ・ダークテーマ or ライトテーマで統一する

## 手順

### 0. 設定をオンにする（demo-01）

1. 設定（`Ctrl+,`）を開く
2. `workbench.browser.enableRemoteProxy` で検索してオンにする
3. `workbench.browser.dataStorage` が `default` のままであることを確認する
4. 📸 **demo-01**: 2 つの設定が見える画面を撮る

### 1. リモートホストに接続する（demo-02）

1. Agents ウィンドウを開き、`Ctrl+N` で新しいセッションを作る
2. 環境のドロップダウンで **SSH** を選び、`user@hostname` を入力する（Dev Tunnels の場合は **Dev Tunnels** → アカウント → トンネルを選ぶ）
3. 接続後、リモートのデモ用フォルダーを選んでセッションを開始する
4. 📸 **demo-02**: 接続先ホスト名とフォルダーが分かる画面を撮る

### 2. エージェントに起動と確認を頼む（demo-03）

次のプロンプトを送る。

```text
このセッションのリモートホストで、サインアップフォーム付きの小さな Web アプリ（Node.js + Express）を作って起動してください。localhost の URL を統合ブラウザで開いて、サインアップのフローを確認し、問題があれば直して、結果を検証してください。
```

英語版（公式ドキュメントのプロンプト例）:

```text
Start the app on this session's remote host, open its localhost URL in the integrated browser, and test the sign-up flow. Fix any issues and verify the result.
```

📸 **demo-03**: プロンプトを送信した直後のチャット画面を撮る

### 3. 統合ブラウザで確認する（demo-04）

1. エージェントが開いたページ（またはアドレスバーに `http://localhost:3000` を自分で入力したページ）を表示する
2. アドレスバーのリモートインジケーター（`Connected via ホスト名` のような表示）がセッションのホストを指しているか確認する
3. 手元のマシンでは同じポートが動いていないことを確認しておく（手元の `localhost:3000` ではなく、リモートの画面が見えている証拠になる）
4. 📸 **demo-04**: ページ本体とアドレスバーのインジケーターが両方入るように撮る

### 4. 要素にコメントして直してもらう（demo-05 → demo-07）

1. **Add to Chat** のドロップダウン → **Comment on Elements** を選ぶ
2. ナビゲーションを選んで `狭い画面ではメニューボタンにまとめる` とコメントする
3. フォームを選んで `入力欄をそろえて、エラーは各入力欄の下に表示する` とコメントする
4. 📸 **demo-05**: コメントを入力している途中の画面を撮る
5. チャット欄に `デスクトップとモバイルの表示幅で結果を確認して` と入力して送信する
6. エージェントが修正して再確認するまで待つ
7. 📸 **demo-07**: 修正後の画面（モバイル幅で確認している状態）を撮る

### 5. Share with Agent を試す（demo-06）

1. 自分でリモートアプリを開いたタブで、ツールバーの **Share with Agent** を押して共有を確認する
2. 共有中のインジケーターが出ていることを確認する
3. 📸 **demo-06**: ツールバーの共有表示を撮る
4. 共有を解除（もう一度 **Share with Agent**）して、取り消せることも確認しておく

### 6. 切断時の挙動を確認する（demo-08・任意）

1. リモートホストとの接続を切る（ホストのネットワークを切る、または Disconnect する）
2. アドレスバーのインジケーターが切断状態になるか、ページがローカルのネットワークにフォールバックしないか確認する
3. 📸 **demo-08**: 切断状態のインジケーターを撮る
4. 再接続してページを再読み込みし、復帰することを確認する

## 記事に反映するメモ（検証して書き換える箇所）

実機で確認した結果を、下の表に残してから記事の該当箇所を調整する。

| 確認項目                                       | 結果（実機で記入） |
| ---------------------------------------------- | ------------------ |
| 接続方法（SSH / Dev Tunnels / WSL / Dev Container） |                    |
| ホスト OS / VS Code のバージョン               |                    |
| 元の URL（localhost:3000）でそのまま開けたか   |                    |
| インジケーターの表示文言                       |                    |
| ホットリロード / WebSocket の動作              |                    |
| 切断時の表示とフォールバックの有無             |                    |
| ホストが未対応バージョンのときの表示           |                    |
| Comment on Elements → 修正 → 再検証がリモートで動いたか |                    |
| 日本語プロンプトで期待どおり動いたか           |                    |

## 公開前チェック

- [ ] `images/` に demo-01 〜 demo-07（必要なら demo-08）を配置した
- [ ] 記事内の `<!-- DEMO -->` コメントが付いた画像パスとファイル名が一致している
- [ ] ホスト名・ユーザー名・IP・トークンなどが映り込んでいない
- [ ] 記事内の「〜でした」「〜と感じました」を実機の結果に合わせた
- [ ] `images/` を GitHub に push して raw URL で表示できる
- [ ] front matter の `ignorePublish: true` を `false` に戻した
