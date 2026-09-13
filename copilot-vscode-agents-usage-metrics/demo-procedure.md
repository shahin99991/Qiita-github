# デモ手順書 & スクショチェックリスト

## 記事「GitHub CopilotのUsage MetricsにVS Code Agentsウィンドウの指標が追加されたので、実際にAPIを叩いて検証してみた」

対象記事: `copilot-vscode-agents-usage-metrics/article-qiita.md`

**ステータス: 検証・撮影済み。** 以下は実際に行った手順の記録であり、`images/` 配下の7枚は記事本文に反映済み。

---

## 実施環境

- `gh` CLI ログイン済み（アカウント: `srohoman-bot`、スコープ: `gist`, `read:org`, `repo`, `workflow`）
- 検証対象: `YJK-Inc`（自分がインターンをしているYJK株式会社のOrganization、Enterprise配下）
- Enterprise owner権限あり（`https://github.com/enterprises/YJK-Inc/settings/copilot` を操作可能）

---

## 実施した手順と対応スクリーンショット

### 手順1: トークンのスコープを確認

```bash
gh auth status
```

`Token scopes` に `read:org` が含まれていることを確認した。

📸 `images/01-gh-auth-status.png`

### 手順2: 未認証リクエストを試す

```bash
curl -s -o /dev/null -w "HTTP %{http_code}\n" \
  https://api.github.com/orgs/YJK-Inc/copilot/metrics/reports/organization-1-day
```

`HTTP 401` が返ることを確認した。

📸 `images/02-unauthenticated-401.png`

### 手順3: 認証ありでリクエストを試す（ポリシー無効時）

```bash
curl -s -D - -o response.json \
  -H "Authorization: Bearer $(gh auth token)" \
  -H "Accept: application/vnd.github+json" \
  "https://api.github.com/orgs/YJK-Inc/copilot/metrics/reports/organization-1-day?day=2026-09-13"

cat response.json
```

`403` + `"The 'Copilot usage metrics' policy must be enabled to use this API"` が返ることを確認した。

📸 `images/03-authenticated-403-policy-disabled.png`

### 手順4: Enterprise の AI Controls > Copilot 設定画面を開く

`https://github.com/enterprises/YJK-Inc` の **AI Controls > Copilot** を開いた。「Copilot usage metrics」ポリシーは **Organizationの設定画面ではなく、Enterprise側にある**ことを確認した。

📸 `images/04-enterprise-ai-controls-copilot.png`

### 手順5: Billing & usage セクションで未設定状態を確認

ページ下部の「Billing & usage」までスクロールし、`Copilot metrics API`（Enabled everywhere）とは別に `Copilot usage metrics` が `Select a policy`（未設定）のままであることを確認した。

📸 `images/05-billing-usage-select-a-policy.png`

### 手順6: ポリシーを Enabled everywhere に変更

ドロップダウンを開き、`Enabled everywhere` を選択した。

📸 `images/06-enable-policy-dropdown.png`

### 手順7: 同じリクエストを再実行してステータス変化を確認

```bash
curl -s -D - -o response.json \
  -H "Authorization: Bearer $(gh auth token)" \
  -H "Accept: application/vnd.github+json" \
  "https://api.github.com/orgs/YJK-Inc/copilot/metrics/reports/organization-1-day?day=$(date -u +%F)"

cat response.json
```

`403` → `204 No Content` に変化したことを確認した（`200` + `download_links` は手順8で別途取得）。

📸 `images/07-after-enable-204.png`

### 手順9: 翌日に再実行し、実際のレポート（200）を取得する

`204`のまま記事を書き進めていたが、翌日に同じ種類のリクエストを打ち直したところ`200`が返り、`download_links`から実際のNDJSONレポートを取得できた。

```bash
curl -s -D - -o response.json \
  -H "Authorization: Bearer $(gh auth token)" \
  -H "Accept: application/vnd.github+json" \
  "https://api.github.com/orgs/YJK-Inc/copilot/metrics/reports/organization-1-day?day=2026-09-12"

curl -s "$(python3 -c "import json;print(json.load(open('response.json'))['download_links'][0])")" -o report.ndjson
python3 -m json.tool report.ndjson
```

ディレクトリーヘッダーと`response.json`の中身（`200`と`download_links`）をキャプチャした。

📸 `images/08-report-200-download-links.png`

実データを確認したところ、`monthly_active_agent_users`（値あり）に対して`daily_active_vscode_agent_users`・`totals_by_vscode_agent`は完全に欠落していた（`grep vscode`で0件ヒット）。検証対象のOrganizationにVS Code Agentsウィンドウの利用実績が無かったためで、「未使用時はオプションフィールドごと省略される」という仕様を実データで確認できた。

📸 `images/09-report-actual-data.png`

---

## 撮影済みチェックリスト

| #   | ファイル名                                 | 内容                                                         | モザイク処理                                                                         |
| --- | ------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------------------------------ |
| 01  | `01-gh-auth-status.png`                    | `gh auth status` の実行結果                                  | トークン値は元から `*` マスク済み                                                    |
| 02  | `02-unauthenticated-401.png`               | 未認証リクエストで `401`                                     | なし                                                                                 |
| 03  | `03-authenticated-403-policy-disabled.png` | 認証ありリクエストで `403`（ポリシー無効）                   | なし                                                                                 |
| 04  | `04-enterprise-ai-controls-copilot.png`    | Enterprise の AI Controls > Copilot 画面全体                 | なし（Enterprise名は記事で開示済み）                                                 |
| 05  | `05-billing-usage-select-a-policy.png`     | Billing & usage、ポリシー未設定状態                          | なし                                                                                 |
| 06  | `06-enable-policy-dropdown.png`            | Enabled everywhere を選択するドロップダウン                  | なし                                                                                 |
| 07  | `07-after-enable-204.png`                  | ポリシー有効化後、同じリクエストが `204` に変化              | `x-oauth-client-id` / `x-github-request-id` は画像内で既にマスク済み                 |
| 08  | `08-report-200-download-links.png`         | 翌日再実行で `200` + `download_links` を取得                 | `etag` / `x-oauth-client-id` / `x-github-request-id` / 署名付きURLの一部はマスク済み |
| 09  | `09-report-actual-data.png`                | 実際のNDJSONレポートの中身（vscode_agent系フィールドは不在） | なし（organization_id/enterprise_idは記事で開示済み）                                |

---

## 記事への反映状況

すべて `article-qiita.md` の「実際にAPIを叩いて検証してみた」セクション内に反映済み。画像パスは以下の形式。

```
https://raw.githubusercontent.com/shahin99991/Qiita-github/main/copilot-vscode-agents-usage-metrics/images/<ファイル名>
```

`images/` フォルダの内容をGitHubにpushすれば、Qiita側の画像リンクもそのまま有効になる。

## 未実施のまま残っている項目

- VS Code Agentsウィンドウ（Preview機能）自体のスクリーンショットは未撮影。記事では「VS Code側の実UIキャプチャは今回省略し、公式ドキュメントの説明に留めた」扱いとしている。撮る場合は以下の手順で追加できる。
  1. VS Code で `chat.agent.enabled` を有効化
  2. アクティビティバーのチャット/エージェントアイコン、またはコマンドパレットで `Agents` と入力してAgentsウィンドウを開く
  3. セッション一覧・新規セッション作成画面が見える状態でキャプチャし、`images/08-vscode-agents-window.png` として保存
  4. 記事の「VS Code Agentsウィンドウ」と「エディタ内のAgent Mode」を説明しているセクションに挿入する
