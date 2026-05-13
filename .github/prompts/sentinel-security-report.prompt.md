---
mode: agent
description: "Azure Sentinel + SentinelMCP フレームワークを使ってセキュリティレポートを自動生成する。Azure MCP の Log Analytics ツールで KQL クエリを実行し、Tier1〜3 の階層構造でレポートにまとめる。"
tools:
  - azure_monitor_log_analytics_query
  - azure_resource_management_resources_list
---

# Sentinel セキュリティレポート自動生成

あなたは Microsoft Sentinel の SOC アナリストとして、以下の手順でセキュリティレポートを生成してください。
レポート期間は **過去 24 時間** とします（指示があれば変更してください）。

## 前提確認

レポート生成を開始する前に以下を確認してください：

- Azure サブスクリプション ID: `${{ env.AZURE_SUBSCRIPTION_ID }}`
- Log Analytics ワークスペース ID（不明な場合は `azure_resource_management_resources_list` で Microsoft.OperationalInsights/workspaces を検索して取得する）

---

## Step 1: Tier 1 — アラートトリアージ（所要目安: 5〜15 分）

以下の KQL クエリを **`azure_monitor_log_analytics_query`** ツールで実行してください。

### 1-1. 直近 24 時間のインシデント一覧

```kql
SecurityIncident
| where TimeGenerated > ago(24h)
| summarize
    TotalIncidents = count(),
    Critical = countif(Severity == "High"),
    Medium = countif(Severity == "Medium"),
    Low = countif(Severity == "Low"),
    Informational = countif(Severity == "Informational")
  by bin(TimeGenerated, 1h)
| order by TimeGenerated desc
```

### 1-2. 未解決インシデントの上位10件

```kql
SecurityIncident
| where TimeGenerated > ago(24h)
| where Status != "Closed"
| project
    IncidentName,
    Severity,
    Status,
    Owner = tostring(parse_json(Owner).userPrincipalName),
    AlertsCount,
    CreatedTime,
    LastModifiedTime,
    Classification
| order by Severity asc, CreatedTime desc
| take 10
```

### 1-3. 重大度別インシデント数のサマリ

```kql
SecurityIncident
| where TimeGenerated > ago(24h)
| summarize Count = count() by Severity, Status
| order by Severity asc
```

---

## Step 2: Tier 2 — 調査分析（所要目安: 30〜60 分相当）

### 2-1. サインインリスクイベント（Entra ID）

```kql
SigninLogs
| where TimeGenerated > ago(24h)
| where RiskLevelDuringSignIn in ("high", "medium")
| project
    TimeGenerated,
    UserPrincipalName,
    AppDisplayName,
    IPAddress,
    Location = tostring(LocationDetails),
    RiskLevelDuringSignIn,
    RiskState,
    ResultType,
    ConditionalAccessStatus
| order by RiskLevelDuringSignIn asc, TimeGenerated desc
| take 20
```

### 2-2. 不審なプロセス実行（Defender for Endpoint）

```kql
DeviceProcessEvents
| where TimeGenerated > ago(24h)
| where FileName in~ ("powershell.exe", "cmd.exe", "wscript.exe", "cscript.exe", "mshta.exe", "regsvr32.exe", "rundll32.exe")
| where InitiatingProcessFileName !in~ ("explorer.exe", "svchost.exe", "services.exe")
| summarize
    CommandCount = count(),
    Devices = dcount(DeviceName),
    UniqueUsers = dcount(AccountName)
  by FileName, InitiatingProcessFileName
| order by CommandCount desc
| take 15
```

### 2-3. ネットワーク異常通信（送信トラフィック上位）

```kql
AzureNetworkAnalytics_CL
| where TimeGenerated > ago(24h)
| where FlowDirection_s == "O"
| summarize
    TotalBytes = sum(InboundBytes_d + OutboundBytes_d),
    FlowCount = count()
  by DestIP = DestPublicIPs_s, DestPort = DestPort_d
| where TotalBytes > 10000000  // 10 MB 以上
| order by TotalBytes desc
| take 20
```

### 2-4. 特権操作（Azure アクティビティログ）

```kql
AzureActivity
| where TimeGenerated > ago(24h)
| where CategoryValue == "Administrative"
| where ActivityStatusValue == "Success"
| where OperationNameValue has_any ("delete", "write", "action")
| summarize
    OperationCount = count()
  by Caller, OperationNameValue, ResourceGroup, SubscriptionId
| order by OperationCount desc
| take 20
```

---

## Step 3: Tier 3 — フォレンジック / クラウドハンティング（並行実行）

### 3-1. TI（脅威インテリジェンス）マッチ

```kql
ThreatIntelligenceIndicator
| where TimeGenerated > ago(7d)
| where Active == true
| join kind=inner (
    SecurityEvent
    | where TimeGenerated > ago(24h)
) on $left.NetworkIP == $right.IpAddress
| project
    TimeGenerated,
    ThreatType,
    IndicatorId,
    ConfidenceScore,
    IpAddress,
    Account,
    Computer,
    EventID
| order by ConfidenceScore desc
| take 10
```

### 3-2. 異常なデータ転送（データ漏洩リスク）

```kql
OfficeActivity
| where TimeGenerated > ago(24h)
| where Operation in ("FileDownloaded", "FileCopied", "FileDeleted", "SharingInvitationCreated")
| summarize
    EventCount = count(),
    DistinctFiles = dcount(SourceFileName)
  by UserId, Operation, SiteUrl
| where EventCount > 50
| order by EventCount desc
| take 10
```

### 3-3. Sentinel 分析ルールのアラート分布

```kql
SecurityAlert
| where TimeGenerated > ago(24h)
| summarize
    AlertCount = count(),
    UniqueEntities = dcount(SystemAlertId)
  by AlertName, Severity, ProductName
| order by AlertCount desc
| take 20
```

---

## Step 4: レポート生成

上記すべてのクエリ結果を取得したら、以下のフォーマットで Markdown レポートを生成してください。
データが取得できなかったクエリは「データなし」と記載してください。

---

```markdown
# セキュリティレポート — {YYYY-MM-DD} 24時間サマリ

**生成日時**: {timestamp}
**対象期間**: 過去 24 時間
**ワークスペース**: {workspace_id}
**作成者**: GitHub Copilot Agent + Azure MCP + SentinelMCP Framework

---

## エグゼクティブサマリ

| 指標               | 件数         |
| ------------------ | ------------ |
| 総インシデント数   | {total}      |
| 重大（High）       | {critical}   |
| 中（Medium）       | {medium}     |
| 低（Low）          | {low}        |
| 未解決インシデント | {open}       |
| TI マッチ          | {ti_matches} |

**主要リスク**: {top_risk_summary_1行}

---

## Tier 1: アラートトリアージ結果

### インシデント時系列

{1-1 の結果を表形式で}

### 未解決インシデント Top 10

{1-2 の結果を表形式で}

---

## Tier 2: 調査分析結果

### Entra ID サインインリスク

{2-1 の結果。問題がなければ「検知なし」}

### 不審プロセス実行

{2-2 の結果。問題がなければ「検知なし」}

### 特権操作ログ

{2-4 の結果を表形式で}

---

## Tier 3: フォレンジック / 脅威ハンティング

### 脅威インテリジェンスマッチ

{3-1 の結果。検知がなければ「一致なし（良好）」}

### データ転送異常

{3-2 の結果。問題がなければ「異常なし」}

---

## 推奨アクション

クエリ結果に基づいて、以下のカテゴリで優先度付きのアクション一覧を生成してください：

### 🔴 即時対応（Critical）

{該当するものがあれば列挙}

### 🟠 24時間以内（High）

{該当するものがあれば列挙}

### 🟡 今週中（Medium）

{該当するものがあれば列挙}

---

## 付記

- このレポートは GitHub Copilot Agent + Azure MCP (Log Analytics ツール) によって自動生成されました
- SentinelMCP フレームワーク（Tier1/2/3 構造）に基づいて構成しています
- クエリで取得できなかったデータは環境の設定（テーブルの有効化状況）によります
```

---

## 注意事項

- KQL クエリの実行には Log Analytics ワークスペースへの **Reader 権限以上** が必要です
- テーブル（`DeviceProcessEvents`, `SigninLogs` など）は Sentinel / Defender のデータコネクターが有効な場合のみ存在します
- データが存在しないテーブルのクエリはエラーではなく空の結果を返します。その場合は「データなし（コネクター未設定の可能性）」と記載してください
- 本番環境のデータを扱うため、レポート出力先のアクセス権管理に注意してください
