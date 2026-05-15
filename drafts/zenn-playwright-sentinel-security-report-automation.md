---
title: "Playwright MCP × Microsoft Sentinel MCP Server × VS Code Skills で顧客向けセキュリティレポートを全自動生成してみる"
emoji: "🛡️"
type: "tech"
topics: ["azure", "githubcopilot", "security", "playwright", "mcp"]
published: false
---

## はじめに

セキュリティレポートの作成は、まだ多くの現場で「ポータルを開いてスクリーンショットを撮る」「KQL クエリをコピペする」「PowerPoint にペーストする」という手作業です。週次で顧客向けレポートを用意するなら、その工数だけで半日は消えます。

この記事では、以下の3つを組み合わせてそのフローを自動化する方法を扱います。

- **Microsoft Sentinel MCP Server** — Sentinel のデータレイクに自然言語でアクセスする公式マネージドサーバー（2025年11月 GA）
- **Playwright MCP** — Azure Portal / Microsoft Defender ポータルのブラウザ操作とスクリーンショット取得
- **SentinelMCP フレームワーク** — Tier1/2/3 の SOC 調査構造をプロンプトに組み込む

最終的には GitHub Actions の定期実行で PPTX レポートまで生成し、Azure Blob Storage に納品するパイプラインを目指します。

この記事を読むと以下ができるようになります：

- ✅ Microsoft Sentinel MCP Server を VS Code に接続してインシデントデータを自然言語で取得する
- ✅ Playwright MCP で Sentinel ダッシュボードのスクリーンショットを自動取得する
- ✅ SentinelMCP の Tier 構造を `.prompt.md` に組み込んでレポートを構造化する
- ✅ python-pptx / marp で Markdown → PPTX に変換する
- ✅ GitHub Actions + OIDC 認証で週次自動実行する

## 全体アーキテクチャ

```
GitHub Actions (cron: 毎週月曜 8:00 UTC)
         │
         ▼
  VS Code / Agent Mode
  .github/prompts/security-report.prompt.md
         │
    ┌────┴────┐
    │         │
    ▼         ▼
Playwright   Microsoft Sentinel
   MCP       MCP Server（公式）
    │         │
    │ SS取得  │ インシデント・エンティティ取得
    └────┬────┘
         │
         ▼
  Markdown レポート生成
  (SentinelMCP Tier 構造)
         │
         ▼
  python-pptx / marp で PPTX 変換
         │
         ▼
  Azure Blob Storage にアップロード
```

**事前に1点確認してください。**

SentinelMCP（eshlomo1/SentinelMCP）は npx で起動する MCP サーバーではなく、Tier1〜3 の調査手順を定義した **YAML フレームワーク**です。Microsoft 公式の Sentinel MCP Server（後述）とは別物なので、混同しないよう注意してください。

## 前提条件

| 項目                     | 要件                                                |
| ------------------------ | --------------------------------------------------- |
| VS Code                  | 1.99 以降（Agent モード + MCP サポート）            |
| GitHub Copilot           | Pro / Business / Enterprise                         |
| Azure サブスクリプション | Microsoft Sentinel 有効化済み                       |
| Sentinel Data Lake       | オンボーディング済み（Sentinel MCP の前提条件）     |
| Node.js                  | 18 以上（Playwright MCP 用）                        |
| Python                   | 3.10 以上（PPTX 生成ステップのみ）                  |
| 権限                     | Security Reader 以上（Sentinel MCP サーバー接続用） |

## Step 1: MCP サーバーのセットアップ

### Microsoft Sentinel MCP Server を VS Code に追加する

Sentinel MCP Server はフルマネージドのクラウドサービスです。`npx` のインストールは不要で、エンドポイント URL を登録するだけで使えます。

1. `Ctrl+Shift+P` → **MCP: Add Server** を選択
2. **HTTP または Server-Sent Events** を選択
3. URL に `https://sentinel.microsoft.com/mcp/data-exploration` を入力
4. サーバー名（例: `sentinel`）を設定
5. スコープ（ワークスペース全体 / 現在のワークスペース）を選択
6. 認証を求められたら **Security Reader 権限を持つアカウント**で許可

この操作で `.vscode/mcp.json` に以下のエントリが追加されます：

```json
{
  "servers": {
    "sentinel": {
      "type": "http",
      "url": "https://sentinel.microsoft.com/mcp/data-exploration"
    },
    "playwright": {
      "type": "stdio",
      "command": "npx",
      "args": [
        "@playwright/mcp@latest",
        "--headless",
        "--browser",
        "msedge",
        "--storage-state",
        "./.auth/azure-session.json",
        "--output-dir",
        "./reports/screenshots",
        "--caps",
        "testing"
      ]
    }
  }
}
```

| ツールコレクション                        | エンドポイント URL                                                   |
| ----------------------------------------- | -------------------------------------------------------------------- |
| データ探索（KQL・インシデント照会）       | `https://sentinel.microsoft.com/mcp/data-exploration`                |
| エージェント作成（Security Copilot 連携） | `https://sentinel.microsoft.com/mcp/security-copilot-agent-creation` |

:::message
💡 Sentinel MCP Server は **Sentinel Data Lake** へのオンボーディングが前提です。従来の Log Analytics ワークスペースのみの環境では使用できません。Data Lake が未設定の場合は、後述の「Azure MCP フォールバック」を参照してください。
:::

### Playwright 用の Azure Portal セッションを事前保存する

Azure Portal は MFA が必須のため、自動でログインできません。一度だけ手動でログインしてセッションを保存しておきます。

```bash
# セッション保存スクリプトを実行（ブラウザが開くので手動でログイン）
npx playwright codegen \
  --save-storage=./.auth/azure-session.json \
  https://portal.azure.com
# ブラウザで Azure AD ログイン（MFA 含む）を完了させてから閉じる
```

:::message alert
🚨 `.auth/azure-session.json` には認証済みクッキーが含まれます。必ず `.gitignore` に追加し、CI では GitHub Secrets 経由で取り扱います。
:::

```bash
# .gitignore に追加
echo ".auth/" >> .gitignore
```

## Step 2: Microsoft Sentinel MCP Server でデータを取得する

サーバーを登録後、Agent モードで自然言語のまま照会できます。KQL を書く必要はありません。

```text
過去7日間のインシデントをサマリーしてください。
重大度別（High/Medium/Low）と未解決件数、解決済み件数を表形式で出してください。
```

```text
最もリスクの高いユーザーを3人挙げて、それぞれのリスク理由を説明してください。
```

```text
今週検出された ATT&CK タクティクスの分布を教えてください。
どの攻撃フェーズが最も多いですか？
```

Sentinel MCP Server が自動的に適切なデータソース（Identity Protection、Defender for Identity、SigninLogs など）を横断して照会し、構造化された回答を返します。

### Entity Analyzer で高リスクエンティティを分析する

GA と同時に追加された **Entity Analyzer** ツールを使うと、ユーザーや URL のリスク評価を一発で取得できます。

```text
ユーザー alice@contoso.com のリスク評価を実施してください。
どのようなリスクイベントが関連していますか？
```

```text
https://suspicious-domain.example.com のリスク評価をしてください。
```

### カスタム KQL ツールを活用する

Defender Advanced Hunting に保存済みの KQL クエリは、Sentinel MCP Server で **MCP ツール化**できます。保存クエリのページから「MCP ツールとして保存」を選択するだけで、Agent がそのクエリをツールとして呼び出せるようになります。

### Azure MCP フォールバック（Sentinel Data Lake 未使用の場合）

Sentinel Data Lake に未オンボードの環境では、Azure MCP Server を代替として使えます。

```bash
npx -y @azure/mcp@latest server start &
```

実用的な KQL クエリは以下の4本です。

:::details KQL クエリ集（フォールバック用）

**① 週次インシデントサマリー**

```kql
SecurityIncident
| where TimeGenerated > ago(7d)
| summarize
    Total = count(),
    Open = countif(Status != "Closed"),
    High = countif(Severity == "High"),
    Medium = countif(Severity == "Medium"),
    Low = countif(Severity == "Low")
```

**② MTTR（平均解決時間）の計算**

```kql
SecurityIncident
| where Status == "Closed"
| where TimeGenerated > ago(30d)
| extend MTTR_hours = datetime_diff('hour', ClosedTime, CreatedTime)
| summarize
    avg_MTTR = round(avg(MTTR_hours), 1),
    median_MTTR = round(percentile(MTTR_hours, 50), 1)
```

**③ ATT&CK タクティクス分布**

```kql
SecurityIncident
| where TimeGenerated > ago(7d)
| mv-expand todynamic(AdditionalData)
| where AdditionalData.tactics != ""
| summarize count() by tostring(AdditionalData.tactics)
| order by count_ desc
```

**④ サインインリスク（Entra ID）**

```kql
SigninLogs
| where TimeGenerated > ago(7d)
| where RiskLevelDuringSignIn in ("high", "medium")
| summarize
    RiskySignins = count(),
    UniqueUsers = dcount(UserPrincipalName)
  by RiskLevelDuringSignIn, AppDisplayName
| order by RiskySignins desc
| take 10
```

:::

## Step 3: Playwright MCP でダッシュボードを撮影する

Azure Portal のセッションを保存済みの状態で、以下を Agent モードで実行します。

```text
Playwright MCP を使って以下を実施してください：

1. https://portal.azure.com にアクセスし、ページが読み込まれるまで待つ
2. Microsoft Sentinel の概要ダッシュボード画面に移動する
   （URL: https://portal.azure.com/#blade/Microsoft_Azure_Security_Insights/MainMenuBlade/overview）
3. ページ全体のスクリーンショットを取得し、reports/screenshots/sentinel-overview.png として保存
4. アクティブなインシデント一覧のスクリーンショットも取得し、reports/screenshots/incidents.png として保存
5. 取得した画像のパスを返答してください
```

`--output-dir` を設定しておくと、スクリーンショットが自動的に指定フォルダに保存されます。

:::message
💡 `--headless` モードでは Azure Portal の一部コンポーネント（動的な SVG グラフ等）が正しく描画されない場合があります。その場合は `--headless` を外して headed モードで実行してください。
:::

## Step 4: SentinelMCP の Tier 構造をプロンプトに組み込む

SentinelMCP（eshlomo1/SentinelMCP）は、SOC 運用の階層構造を YAML で定義したフレームワークです。この構造を `.prompt.md` の中に落とし込んで使います。

| Tier         | 役割                                       | 対応するデータ取得                   |
| ------------ | ------------------------------------------ | ------------------------------------ |
| Tier 1       | アラートトリアージ・正規化・FP 除去        | インシデント数・重大度分布           |
| Tier 2       | 深掘り調査（マルウェア・ネットワーク・ID） | Entra サインインリスク・不審プロセス |
| Tier 3       | フォレンジック・根本原因分析               | TI マッチ・MTTR・証拠パッケージ      |
| Cloud Hunter | 脅威ハンティング（並列実行）               | 異常通信・データ転送量               |

### `.github/prompts/sentinel-weekly-report.prompt.md` の構成

```markdown
---
mode: agent
description: "Sentinel 週次セキュリティレポート — Tier1/2/3 構造で自動生成"
tools:
  - sentinel/get_incidents
  - sentinel/analyze_entity
  - sentinel/run_hunting_query
  - playwright/browser_navigate
  - playwright/browser_take_screenshot
  - playwright/browser_snapshot
---

# Sentinel 週次セキュリティレポート生成

## Tier 1: トリアージ（Sentinel MCP で照会）

1. 過去7日間のインシデントサマリーを取得（重大度別・ステータス別）
2. 未解決インシデント Top 10 を取得
3. 今週検出された ATT&CK タクティクス分布を取得

## Tier 2: 調査分析

1. Entity Analyzer で Top 5 リスクユーザーのリスク評価を取得
2. カスタム KQL ツール（事前登録済み）でリスクサインインを取得
3. カスタム KQL ツールで特権操作ログを取得

## Tier 3: フォレンジック

1. Entity Analyzer で検出された高リスク URL・IOC の評価を取得
2. カスタム KQL ツールで MTTR（平均解決時間）を計算

## 視覚資料（Playwright MCP）

1. Sentinel 概要ダッシュボードのスクリーンショット取得
2. アクティブインシデント一覧のスクリーンショット取得

## レポート出力

すべての結果を reports/weekly-security-report.md に保存してください。
以下の構成で出力すること：

- エグゼクティブサマリー（指標表）
- Tier 1 結果
- Tier 2 結果
- Tier 3 結果
- 推奨アクション（Critical/High/Medium 優先度付き）
```

このファイルを `Chat: Use Prompt...` から呼び出すだけで、Agent がツールを順番に実行してレポートを組み立てます。

## Step 5: Markdown → PPTX に変換する

レポートの Markdown が揃ったら、PPTX に変換して顧客に提出できる形にします。

### 方法 A: marp（シンプル・CLI 完結）

```bash
npm install -g @marp-team/marp-cli

npx @marp-team/marp-cli \
  reports/weekly-security-report.md \
  --pptx \
  --output reports/security-report.pptx \
  --theme default
```

Markdown の先頭に以下のフロントマターを追加すると marp として認識されます。

```markdown
---
marp: true
theme: default
paginate: true
---

# Weekly Security Report

## Week of 2026-05-15
```

### 方法 B: python-pptx（細かいレイアウト制御が必要な場合）

```bash
pip install python-pptx
```

```python
# scripts/generate_report.py
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
import json, sys
from datetime import datetime

def build_report(data_path: str, screenshot_dir: str, output_path: str) -> None:
    with open(data_path) as f:
        data = json.load(f)
    prs = Presentation()

    # タイトルスライド
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    slide.shapes.title.text = "Weekly Security Report"
    slide.placeholders[1].text = f"Week of {datetime.now().strftime('%Y-%m-%d')}"

    # サマリースライド
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = "Executive Summary"
    tf = slide.placeholders[1].text_frame
    for severity, count in data.get("by_severity", {}).items():
        p = tf.add_paragraph()
        p.text = f"{severity}: {count} incidents"

    # スクリーンショットスライド
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    title = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(9), Inches(0.8))
    title.text_frame.text = "Sentinel Dashboard"
    slide.shapes.add_picture(
        f"{screenshot_dir}/sentinel-overview.png",
        Inches(0.5), Inches(1.2), Inches(9), Inches(5.3)
    )

    prs.save(output_path)
    print(f"Saved: {output_path}")

if __name__ == "__main__":
    build_report(sys.argv[1], sys.argv[2], sys.argv[3])
```

```bash
python scripts/generate_report.py \
  reports/incident-data.json \
  reports/screenshots \
  reports/security-report.pptx
```

:::message
💡 **PPTX Skill への発展**: VS Code の `.github/skills/` に PPTX 生成手順を SKILL.md として定義しておけば、`@agent #skill:pptx-report` のように呼び出せます。組織の PPTX テンプレート（`.potx` ファイル）を参照させることでブランドガイドライン準拠の資料を自動生成できます。
:::

## Step 6: GitHub Actions で週次自動実行する

### OIDC 認証でシークレットレス化する

パスワードや Client Secret を使わず、Federated Identity を使って Azure に認証します。

```bash
# GitHub Actions 用のサービスプリンシパルを作成
az ad app create --display-name "github-sentinel-reporter"

# フェデレーション ID を設定
az ad app federated-credential create \
  --id <app-object-id> \
  --parameters '{
    "name": "github-actions",
    "issuer": "https://token.actions.githubusercontent.com",
    "subject": "repo:YOUR_ORG/YOUR_REPO:ref:refs/heads/main",
    "audiences": ["api://AzureADTokenExchange"]
  }'

# Security Reader 権限を付与
az role assignment create \
  --role "Security Reader" \
  --assignee <app-client-id> \
  --scope /subscriptions/<sub-id>/resourceGroups/rg-sentinel
```

### ワークフロー全体

```yaml
# .github/workflows/weekly-security-report.yml
name: Weekly Security Report

on:
  schedule:
    - cron: "0 8 * * 1" # 毎週月曜 08:00 UTC
  workflow_dispatch:

permissions:
  id-token: write # OIDC に必要
  contents: read

jobs:
  generate-report:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Azure ログイン（OIDC）
        uses: azure/login@v2
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}

      - uses: actions/setup-node@v4
        with:
          node-version: "20"

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: 依存パッケージをインストール
        run: |
          npm install -g @playwright/mcp@latest @marp-team/marp-cli
          npx playwright install chromium --with-deps
          pip install python-pptx

      - name: Playwright 認証セッションを復元
        # ⚠️ セッションファイルは GitHub Secrets に BASE64 エンコードして保存
        run: |
          mkdir -p .auth
          echo "${{ secrets.AZURE_SESSION_B64 }}" | base64 -d > .auth/azure-session.json

      - name: Sentinel MCP でインシデントデータを取得
        env:
          SENTINEL_WORKSPACE_ID: ${{ secrets.SENTINEL_WORKSPACE_ID }}
          AZURE_SUBSCRIPTION_ID: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
        run: |
          mkdir -p reports/screenshots
          # トークンを変数に格納（コマンドライン引数に露出させない）
          ACCESS_TOKEN=$(az account get-access-token \
            --resource https://management.azure.com \
            --query accessToken -o tsv)
          # curl の --header オプションで Bearer トークンをセット
          curl -s \
            --header "Authorization: Bearer ${ACCESS_TOKEN}" \
            --header "Content-Type: application/json" \
            --output reports/incident-data.json \
            "https://management.azure.com/subscriptions/${AZURE_SUBSCRIPTION_ID}/resourceGroups/rg-sentinel/providers/Microsoft.OperationalInsights/workspaces/sentinel-law/providers/Microsoft.SecurityInsights/incidents?api-version=2024-03-01&%24filter=properties%2Fstatus%20ne%20%27Closed%27"
          unset ACCESS_TOKEN

      - name: Playwright MCP でスクリーンショット取得
        run: |
          npx @playwright/mcp@latest \
            --headless \
            --storage-state .auth/azure-session.json \
            --output-dir reports/screenshots \
            --port 8931 &
          MCP_PID=$!
          sleep 3
          node scripts/capture-screenshots.js
          kill $MCP_PID || true

      - name: PPTX レポートを生成
        run: |
          python scripts/generate_report.py \
            reports/incident-data.json \
            reports/screenshots \
            reports/security-report.pptx

      - name: Azure Blob Storage にアップロード
        # ⚠️ --local-file-path は仮のフラグ名。実行前に `azmcp storage blob upload --help` で確認してください
        run: |
          azmcp storage blob upload \
            --subscription ${{ secrets.AZURE_SUBSCRIPTION_ID }} \
            --account "securityreportsstorage" \
            --container "weekly-reports" \
            --blob "$(date +%Y-%m-%d)-security-report.pptx" \
            --local-file-path reports/security-report.pptx

      - name: レポートをアーティファクトとして保存
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: security-report-${{ github.run_number }}
          # セッションファイル・認証情報をアーティファクトに含めない
          path: |
            reports/security-report.pptx
            reports/weekly-security-report.md
          retention-days: 90

      - name: 認証セッションファイルを削除
        if: always()
        run: rm -f .auth/azure-session.json
```

:::message alert
⚠️ **セッションファイルの CI 管理について3点**

1. **base64 はエンコードであり暗号化ではありません。** GitHub Secrets に保存する際は secrets として扱い、ログへの出力を避けてください。
2. セッションには有効期限があるため、定期的な再生成が必要です。期限切れを検知して Slack 通知する仕組みを設けることを推奨します。
3. 本番環境では Managed Identity + Playwright の認証キャッシュを Azure Key Vault に保管する構成を検討してください。
   :::

:::details `scripts/capture-screenshots.js` の最小実装例

GitHub Actions で呼び出す `capture-screenshots.js` は、Playwright MCP の HTTP API にリクエストを送ってスクリーンショットを取得します。

```javascript
// scripts/capture-screenshots.js
const http = require("http");

const MCP_PORT = 8931;

async function callMcpTool(toolName, params) {
  return new Promise((resolve, reject) => {
    const body = JSON.stringify({ tool: toolName, params });
    const options = {
      hostname: "localhost",
      port: MCP_PORT,
      path: "/call",
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Content-Length": Buffer.byteLength(body),
      },
    };
    const req = http.request(options, (res) => {
      let data = "";
      res.on("data", (chunk) => (data += chunk));
      res.on("end", () => resolve(JSON.parse(data)));
    });
    req.on("error", reject);
    req.write(body);
    req.end();
  });
}

async function main() {
  await callMcpTool("browser_navigate", {
    url: "https://portal.azure.com/#view/Microsoft_Azure_Security_Insights/MainMenuBlade/~/overview",
  });
  await callMcpTool("browser_take_screenshot", {
    filename: "sentinel-overview.png",
  });

  await callMcpTool("browser_navigate", {
    url: "https://portal.azure.com/#view/Microsoft_Azure_Security_Insights/MainMenuBlade/~/incidents",
  });
  await callMcpTool("browser_take_screenshot", { filename: "incidents.png" });

  console.log("Screenshots saved to reports/screenshots/");
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
```

Playwright MCP の HTTP API 仕様はバージョンによって変わる場合があります。`--port 8931` で起動後、`curl http://localhost:8931/list-tools` でツール一覧を確認してから実装してください。

:::

## 発展: PPTX Skill で企業テンプレート対応にする

VS Code の `.github/skills/` に PPTX 生成スキルを定義しておくと、記事作成フローと同様に呼び出せます。

`.github/skills/pptx-report/SKILL.md` の内容（フロントマターはファイル先頭行から始める必要があります）：

```markdown
---
name: pptx-report
description: "Markdown レポートを企業テンプレート準拠の PPTX に変換する"
---

## 手順

1. reports/ 以下の Markdown ファイルを確認する
2. .github/templates/corporate.potx テンプレートを参照する
3. python-pptx で変換スクリプトを実行する（scripts/generate_report.py）
4. 出力先: reports/output/<date>-report.pptx
5. Azure Blob Storage にアップロードする（任意）
```

`@agent` に対して `#skill:pptx-report` とメンションするだけで、レポート生成から Blob アップロードまでを実行できます。

**marp** で企業カラーのテーマを当てる場合：

```css
/* .github/themes/corporate.css */
section {
  background: #0078d4;
  color: white;
  font-family: "Segoe UI", sans-serif;
}
h1,
h2 {
  color: #ffffff;
  border-bottom: 2px solid #50e6ff;
}
```

```bash
npx @marp-team/marp-cli \
  reports/weekly-security-report.md \
  --pptx \
  --theme .github/themes/corporate.css \
  --output reports/security-report.pptx
```

## まとめ

| やりたいこと                     | 使うツール                                           |
| -------------------------------- | ---------------------------------------------------- |
| Sentinel データを自然言語で取得  | Microsoft Sentinel MCP Server（公式・GA）            |
| エンティティのリスク評価         | Sentinel MCP Server — Entity Analyzer                |
| ポータルのスクリーンショット取得 | Playwright MCP + `--storage-state`                   |
| SOC 調査の構造化                 | SentinelMCP フレームワーク（eshlomo1）→ `.prompt.md` |
| レポートワークフローの定義       | `.github/prompts/*.prompt.md`                        |
| Markdown → PPTX 変換             | marp（シンプル）または python-pptx（細かい制御）     |
| 週次自動化                       | GitHub Actions + OIDC 認証                           |
| 企業テンプレート対応             | `.github/skills/pptx-report/SKILL.md`                |

各ツールの役割は明確です：

- **Microsoft Sentinel MCP Server** — 自然言語でインシデント・エンティティ・脅威インテリジェンスにアクセスする公式ゲートウェイ
- **Playwright MCP** — ポータルを自動撮影する視覚資料収集ツール
- **SentinelMCP（eshlomo1）** — Tier1/2/3 という「何を調べるか」の思考フレームワーク

この3つを `.prompt.md` 一枚に束ねると、週次レポートをエージェントに投げるだけで生成できます。PPTX 変換まで含めると、顧客への提出物を週次で自動生成できます。

実装上の注意点は2つあります。Azure Portal の MFA セッションは有効期限があるため定期的な再生成が必要で、Playwright のヘッドレスモードでは動的な SVG グラフが描画されないケースがあります。まず headed モードで動作確認してから、headless + CI の順で移行してください。

## 参考

- [Microsoft Sentinel MCP Server — Microsoft Learn](https://learn.microsoft.com/azure/sentinel/datalake/sentinel-mcp-overview)
- [Sentinel MCP Server 入門ガイド — Microsoft Learn](https://learn.microsoft.com/azure/sentinel/datalake/sentinel-mcp-get-started)
- [Sentinel MCP Server GA 発表ブログ — Microsoft](https://techcommunity.microsoft.com/blog/microsoft-security-blog/microsoft-sentinel-mcp-server---generally-available-with-exciting-new-capabiliti/4470125)
- [microsoft/playwright-mcp — GitHub](https://github.com/microsoft/playwright-mcp)
- [eshlomo1/SentinelMCP — GitHub](https://github.com/eshlomo1/SentinelMCP)
- [VS Code Prompt Files ドキュメント](https://code.visualstudio.com/docs/copilot/customization/prompt-files)
- [Azure Federated Identity Credentials — Microsoft Learn](https://learn.microsoft.com/azure/active-directory/develop/workload-identity-federation)
- [Marp — Markdown Presentation Ecosystem](https://marp.app/)
- [python-pptx ドキュメント](https://python-pptx.readthedocs.io/)
