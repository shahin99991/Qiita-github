# Azure Sentinel Skill ガイド

> ソース: [MicrosoftDocs/Agent-Skills](https://github.com/MicrosoftDocs/Agent-Skills/blob/main/skills/azure-sentinel/SKILL.md)  
> カテゴリ: 🔒 Security  
> 最終更新: 2026-05-03（Microsoft Learn ドキュメントから自動生成）

---

## これは何？

AIエージェント（GitHub Copilot・Claude Code・Cursor など）に **Microsoft Sentinel（クラウドネイティブ SIEM/SOAR）** の専門知識を与えるスキル。

Microsoft Learn の公式ドキュメントへのリンクを構造化して持ち、エージェントが必要な情報をオンデマンドで取得できるようにする。

> ⚠️ このスキルの対象外（別スキルを使うこと）
>
> - Azure Defender for Cloud → `azure-defender-for-cloud`
> - Azure Security 全般 → `azure-security`
> - Azure Monitor → `azure-monitor`
> - Azure Network Watcher → `azure-network-watcher`

---

## インストール方法（Agent Skills Ninja 経由）

```
# Copilot Chat
@skill /search sentinel

# Agent Mode で自然言語
「Azure Sentinelに関するSkillをインストールして」
```

または Agent Skills Ninja サイドバー → Remote Skills → `MicrosoftDocs/Agent-Skills` → `azure-sentinel` → Install

---

## できること（9カテゴリ）

### 1. 🔧 トラブルシューティング

AIエージェントがSentinelの問題を診断・解決するための知識を提供。

| 対応できる問題                 | 例                                          |
| ------------------------------ | ------------------------------------------- |
| データコネクタの障害           | AWS S3、Azure Storage Blob、Syslog/CEF、GCP |
| KQL クエリ・ジョブの失敗       | データレイクのクエリタイムアウト            |
| SAP コネクタエージェントの問題 | コンテナ接続エラー、SAP認証エラー           |
| Jupyter ノートブックのエラー   | データレイク上のノートブック実行失敗        |
| 分析ルールの問題               | AUTO DISABLED、ルールパッケージングの失敗   |
| ASIM 正規化の問題              | パーサーの既知の問題                        |
| Sentinel MCP ツールの問題      | AI接続のトラブルシューティング              |

**使い方例:**

```
「SyslogのCEF取り込みが失敗している。原因を調べて修正方法を教えて」
「Sentinelの分析ルールがAUTO DISABLEDになっている。なぜ？」
```

---

### 2. ✅ ベストプラクティス

Sentinel の運用・設計における推奨事項を提供。

| 分野                     | 内容                               |
| ------------------------ | ---------------------------------- |
| ワークスペース管理       | マルチワークスペースの管理指針     |
| データ収集               | 効果的なログ収集設計               |
| 分析ルールのチューニング | ノイズ低減・誤検知削減             |
| UEBA（ユーザー行動分析） | インシデント調査での活用方法       |
| SOC 運用                 | SOC向け運用ベストプラクティス      |
| SAP 脅威検出             | SAP統合の設定・検出ルール          |
| Zero Trust / TIC 3.0     | Sentinelを使った監視アーキテクチャ |
| ウォッチリスト           | データのエンリッチメントと相関分析 |

**使い方例:**

```
「Sentinelの誤検知を減らすためのベストプラクティスを教えて」
「SOCチームの運用効率を上げるSentinelの使い方は？」
```

---

### 3. 🤔 意思決定支援

設計・移行・コスト最適化における判断をサポート。

| 判断が必要な場面     | Sentinelスキルが提供する情報                           |
| -------------------- | ------------------------------------------------------ |
| **SIEM移行**         | Splunk・QRadar・ArcSightからの移行手順と検出ルール変換 |
| **エージェント移行** | MMA → AMA への移行計画                                 |
| **データ階層の選択** | Basic・Analytics・データレイクの使い分け               |
| **コネクタ選択**     | 用途に応じたコネクタの優先順位付け                     |
| **コスト最適化**     | 価格プラン・コミットメントプランの選択                 |
| **ログ保持戦略**     | 保持期間とアーカイブ階層の設計                         |
| **デプロイ方式**     | 既存SIEMと並行運用するか移行するか                     |

**使い方例:**

```
「SplunkからSentinelに移行する場合の検出ルールの変換方法を教えて」
「データレイクとAnalyticsログのどちらを使うべきか判断したい」
「Sentinelのコストを削減する方法は？」
```

---

### 4. 🏗️ アーキテクチャ＆デザインパターン

マルチワークスペース・マルチテナント構成の設計指針を提供。

| アーキテクチャパターン       | 内容                                       |
| ---------------------------- | ------------------------------------------ |
| マルチワークスペース設計     | 複数ワークスペースの構成パターンと選択基準 |
| マルチテナント（MSSP向け）   | MSP/MSSPによる複数テナント管理             |
| BCP/DR（事業継続・災害復旧） | Sentinelの継続性設計                       |
| SAP マルチワークスペース     | SAP統合のクロスワークスペース設計          |
| Defender ポータル統合        | Defenderポータルでの複数ワークスペース管理 |

**使い方例:**

```
「MSSPとして複数のお客様のSentinelを管理する構成を設計したい」
「Sentinelのワークスペース設計パターンを教えて」
```

---

### 5. ⚖️ 制限・クォータ

SLAやサービス制限に関する情報を提供。

| 項目                     | 内容                                |
| ------------------------ | ----------------------------------- |
| サービス制限             | Sentinelのクォータと制限値          |
| データレイク制限         | データレイク階層のパラメータ        |
| MCP価格・制限            | Sentinel MCP サーバーの課金・可用性 |
| クエリタイムアウト       | 検索ジョブのタイムアウト設定        |
| ウォッチリストサイズ制限 | 最大行数・取り込みSLA               |
| オフボード時の影響       | Sentinelを無効化する際の注意事項    |

---

### 6. 🔐 セキュリティ設定

Sentinel環境のセキュリティ強化に関する知識を提供。

| 分野                         | 内容                                     |
| ---------------------------- | ---------------------------------------- |
| 認証・RBAC                   | プレイブックの認証設定、ロールと権限     |
| カスタマー管理キー（CMK）    | 暗号化キーの管理設定                     |
| ネットワークセキュリティ     | Blobコネクタ用のネットワーク境界         |
| データ主権・コンプライアンス | データ保存場所と地理的可用性             |
| MSSP知的財産保護             | MSSP向けのIP保護設計                     |
| リソースコンテキストRBAC     | データアクセスのスコーピング             |
| SAP セキュリティ             | ABAP認可要件、SAP セキュリティパラメータ |

**使い方例:**

```
「Sentinelのデータアクセス権を細かく制御するRBACの設定方法は？」
「CMKを使ってSentinelデータを暗号化するには？」
```

---

### 7. ⚙️ 構成・設定

Sentinelの詳細設定に関する広範な知識を提供。最も多くのトピックをカバー。

#### データコネクタの設定

| コネクタ           | 内容                                      |
| ------------------ | ----------------------------------------- |
| AWS (S3)           | EKS・WAF・各種AWSサービスのログ取り込み   |
| GCP Pub/Sub        | Google Cloudのログ取り込み                |
| Microsoft Entra ID | Entra IDログコネクタ                      |
| Defender XDR       | Defender XDR のインシデント・イベント連携 |
| Syslog / CEF (AMA) | Syslog・CEF形式ログの取り込み             |
| SAP                | SAP HANA、SAP BTP、SAPアプリのログ        |
| カスタムログ (AMA) | テキストファイルログの取り込み            |

#### 分析ルール・自動化

| 機能                          | 内容                                 |
| ----------------------------- | ------------------------------------ |
| スケジュール分析ルール        | テンプレートからの作成・カスタム作成 |
| NRT（ほぼリアルタイム）ルール | 数分以内の検出ルール                 |
| Fusion マルチステージ攻撃検出 | 複数の弱いシグナルを組み合わせた検出 |
| 異常検出（ML）                | カスタマイズ可能なML異常検出         |
| 自動化ルール（SOAR）          | インシデント対応の自動化             |
| プレイブック                  | Logic Appsを使った対応自動化         |

#### ASIM（Advanced Security Information Model）

Sentinelのログ正規化スキーマ。様々なログソースを標準フォーマットに変換。

| スキーマ        | 対象             |
| --------------- | ---------------- |
| Authentication  | 認証イベント     |
| Network Session | ネットワーク通信 |
| DNS             | DNS クエリ       |
| Process Event   | プロセス実行     |
| File Event      | ファイル操作     |
| Web Session     | Webアクセス      |
| DHCP            | DHCP リース      |
| Registry Event  | レジストリ変更   |

#### データレイク（Sentinel Data Lake）

| 機能                 | 内容                               |
| -------------------- | ---------------------------------- |
| KQL ジョブ           | バッチKQLクエリのスケジュール実行  |
| サマリールール       | データの集計・要約                 |
| 検索ジョブ           | 大規模データセットの検索           |
| Jupyter ノートブック | データレイク上の分析ノートブック   |
| MCP ツール連携       | ChatGPT・Claude・VS Codeとの連携   |
| Sentinel Graph       | GQL によるセキュリティグラフクエリ |

#### Sentinel MCP ツール（特に重要）

AIエージェントがSentinelデータに直接アクセスできるMCPサーバー。

| 連携先                   | 内容                                        |
| ------------------------ | ------------------------------------------- |
| Visual Studio Code       | VS Code Agent Mode から Sentinel にアクセス |
| Microsoft Copilot Studio | Copilotエージェントへの組み込み             |
| Microsoft Foundry        | Foundryプロジェクトでの活用                 |
| Security Copilot         | Microsoft Security Copilot との統合         |
| ChatGPT / Claude         | 汎用AIとのコネクタ設定                      |
| Azure Logic Apps         | ワークフロー自動化との統合                  |

**使い方例:**

```
「AWS S3からSentinelにログを取り込む設定を教えて」
「Fusionによるマルチステージ攻撃検出を有効にしたい」
「VS CodeからSentinel MCP ツールを使う設定方法は？」
「ASIMパーサーを使ってKQLクエリを書きたい」
```

---

### 8. 🔗 統合・コーディングパターン

APIや自動化コードを使った高度な統合のための知識を提供。

| 統合パターン                      | 内容                                           |
| --------------------------------- | ---------------------------------------------- |
| REST API                          | DCR・ハンティングクエリ・インシデント操作      |
| Data Collection Rules API         | カスタムログ取り込みAPI                        |
| KQL via REST API                  | データレイクのKQLクエリをAPIで実行             |
| Sentinel Graph REST API           | GQLでカスタムセキュリティグラフをクエリ        |
| Azure Functions コネクタ          | Functions を使ったカスタムデータコネクタ       |
| Logstash 統合                     | DCRベースAPIとのLogstash連携                   |
| 脅威インテリジェンス (STIX/TAXII) | STIX/TAXIIフィードの取り込みAPI                |
| Teams 統合                        | インシデントをTeamsで協力対応                  |
| Power BI                          | SentinelデータのPower BIレポート               |
| プレイブック                      | Logic AppsトリガーとIPアドレスエンリッチメント |
| MCP エージェント作成ツール        | Sentinelデータを使ったCopilotエージェント構築  |

**コーディング例でできること:**

```
「SentinelのREST APIを使ってハンティングクエリを一括管理したい」
「カスタムデータコネクタをAzure Functionsで作りたい」
「STIXオブジェクトをSentinelに一括インポートするコードを書いて」
「Teams botでSentinelインシデントに対応する自動化を作りたい」
```

---

### 9. 🚀 デプロイメント

Sentinelソリューションやコンテンツのデプロイ・CI/CD に関する知識を提供。

| 分野                          | 内容                                              |
| ----------------------------- | ------------------------------------------------- |
| CI/CD パイプライン            | GitリポジトリからのSentinelコンテンツ自動デプロイ |
| ARM テンプレート              | 分析ルール・自動化ルールのインポート/エクスポート |
| SAP コネクタデプロイ          | コンテナ/CLIによるSAPコネクタエージェント展開     |
| Power Platform ソリューション | Power Platform向けセキュリティコンテンツデプロイ  |
| Dynamics 365 ソリューション   | D365 F&O向けセキュリティコンテンツデプロイ        |
| Marketplace 公開              | SentinelソリューションのAzure Marketplace公開     |
| SAP BTP ソリューション        | SAP BTP向けSentinelソリューション展開             |

**使い方例:**

```
「SentinelのCI/CDパイプラインをGitHubで構築したい」
「分析ルールをARMテンプレートでエクスポートする方法は？」
「SAPコネクタエージェントをCLIでデプロイしたい」
```

---

## 典型的なユースケース（実践例）

### ユースケース1: SIEMの移行

```
「現在SplunkをSIEMとして使っている。Microsoft Sentinelに移行したい。
検出ルールの変換方法と、過去データの移行手順を教えて」
```

→ スキルが Decision Making + Deployment カテゴリのドキュメントを提供

### ユースケース2: インシデント対応の自動化

```
「Sentinelでインシデントが発生したとき、自動的にTeamsに通知して
IPアドレスの評判を確認するプレイブックを作りたい」
```

→ スキルが Configuration（プレイブック）+ Integrations（Teams/プレイブックAPI）のドキュメントを提供

### ユースケース3: SAP セキュリティ監視

```
「SAP環境をSentinelで監視したい。コネクタのデプロイと
どのような攻撃を検出できるか教えて」
```

→ スキルが Configuration（SAP）+ Best Practices（SAP）+ Deployment（SAP）のドキュメントを提供

### ユースケース4: AIエージェントとの統合

```
「VS CodeのCopilot Agent ModeからSentinelデータを直接クエリできるようにしたい」
```

→ スキルが Configuration（Sentinel MCP）+ Integrations（MCP）のドキュメントを提供

### ユースケース5: コスト最適化

```
「Sentinelの月次コストが高い。削減できる方法を分析して」
```

→ スキルが Decision Making（コスト）+ Limits & Quotas のドキュメントを提供

---

## セキュリティ周辺の関連スキル

| スキル名                         | 用途                                                           |
| -------------------------------- | -------------------------------------------------------------- |
| `azure-sentinel`                 | **このスキル** — SIEM/SOAR、インシデント対応、データ収集・分析 |
| `azure-defender-for-cloud`       | クラウドセキュリティ態勢管理（CSPM）、ワークロード保護         |
| `azure-security`                 | Azureセキュリティ全般（ベースライン・ベンチマーク）            |
| `azure-firewall`                 | Azure ファイアウォール設定                                     |
| `azure-web-application-firewall` | WAF設定                                                        |
| `azure-key-vault`                | 秘密・証明書・キーの管理                                       |
| `azure-rbac`                     | ロールベースアクセス制御                                       |
| `azure-ddos-protection`          | DDoS対策                                                       |

---

## 前提条件

このスキルを使うエージェントには**ネットワークアクセス**が必要（Microsoft Learn からドキュメントをオンデマンドで取得するため）。

- **推奨**: `mcp_microsoftdocs` MCP サーバーをインストール
  - [インストールガイド](https://github.com/MicrosoftDocs/mcp/blob/main/README.md)
- **代替**: `fetch_webpage` ツール（Agent Mode で自動的に利用可能）

---

## 関連リンク

- [SKILL.md 本体](https://github.com/MicrosoftDocs/Agent-Skills/blob/main/skills/azure-sentinel/SKILL.md)
- [Microsoft Sentinel ドキュメント](https://learn.microsoft.com/azure/sentinel/)
- [Sentinel データレイク](https://learn.microsoft.com/azure/sentinel/datalake/)
- [Sentinel MCP ツール](https://learn.microsoft.com/azure/sentinel/datalake/sentinel-mcp-get-started)
- [ASIM スキーマ一覧](https://learn.microsoft.com/azure/sentinel/normalization-parsers-list)
- [Sentinel SOC 最適化](https://learn.microsoft.com/azure/sentinel/soc-optimization/soc-optimization-access)
