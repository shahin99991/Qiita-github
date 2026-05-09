---
title: "長すぎるterraform planをAIが自動レビュー！Azure OpenAI × GitHub ActionsでPRにリスク評価を自動コメントする"
tags:
  - AzureOpenAI
  - GitHubActions
  - Terraform
  - DevOps
  - IaC
---

## はじめに

インフラエンジニアなら一度は感じたことがあるはずです——「`terraform plan` の出力、長すぎて全部読めない問題」。

数十・数百行に及ぶ Plan 結果から「本当に危ない変更」を見つけ出すのは、人間がやるには非効率です。見落としが起きやすく、レビューに時間もかかります。

この記事では、**Azure OpenAI（GPT-4o）** を GitHub Actions のパイプラインに組み込んで、Pull Request の `terraform plan` 結果を **AIが自動で読み込み、変更の要約とリスク評価をPRに自動コメント**する仕組みを実装します。

この記事を読むと、以下のことができるようになります：

- ✅ GitHub Actions で `terraform plan` を自動実行する
- ✅ Plan 結果を Azure OpenAI（GPT-4o）に渡して分析させる
- ✅ リスク評価コメントを Pull Request に自動投稿する

**対象読者**: Terraform と GitHub Actions の基本的な操作に慣れている中級者向けです。Azure OpenAI の事前知識は不要です。

---

## 環境・前提条件

| 項目                     | バージョン / 備考                         |
| ------------------------ | ----------------------------------------- |
| Terraform                | v1.7 以上                                 |
| Python                   | 3.11 以上                                 |
| GitHub Actions           | GitHub.com（クラウド版）                  |
| Azure OpenAI             | `gpt-4o` デプロイ済み                     |
| Azure サブスクリプション | 有効なもの（Azure OpenAI リソース作成用） |

:::note info
💡 **Azure OpenAI の申請について**  
Azure OpenAI は申請制です。[こちらのフォーム](https://aka.ms/oai/access)から利用申請を行い、承認を受けてからリソースを作成してください。
:::

---

## 全体アーキテクチャ

```
┌──────────────────────────────────────────────┐
│             開発者が Pull Request を作成       │
└─────────────────────┬────────────────────────┘
                      │ トリガー
                      ▼
┌──────────────────────────────────────────────┐
│           GitHub Actions ワークフロー          │
│                                              │
│  1. terraform init / plan 実行               │
│  2. plan.txt を保存                          │
│  3. Python スクリプトを起動                   │
└─────────────────────┬────────────────────────┘
                      │ API呼び出し
                      ▼
┌──────────────────────────────────────────────┐
│           Azure OpenAI（GPT-4o）              │
│                                              │
│  - Plan 結果を解析                           │
│  - 変更サマリーを生成                        │
│  - リスク評価（高・中・低）を付与             │
└─────────────────────┬────────────────────────┘
                      │ Markdown コメント
                      ▼
┌──────────────────────────────────────────────┐
│           Pull Request                        │
│   🤖 AI によるレビューコメントが自動投稿      │
└──────────────────────────────────────────────┘
```

---

## Step 1: Azure OpenAI リソースのセットアップ

### 1-1. Azure ポータルでリソースを作成

[Azure ポータル](https://portal.azure.com)にログインし、以下の手順でリソースを作成します。

1. 「Azure OpenAI」を検索してリソースを作成
2. リージョン: `East US 2`（GPT-4o が安定して利用可能）
3. 価格レベル: `Standard S0`

### 1-2. GPT-4o モデルをデプロイ

Azure OpenAI Studio（または Azure AI Foundry）で GPT-4o をデプロイします。

1. 「モデルのデプロイ」→「基本モデルをデプロイ」を選択
2. モデル: `gpt-4o`
3. デプロイ名: `gpt-4o`（この名前を後で使用します）

### 1-3. エンドポイントと API キーを確認

リソースの「キーとエンドポイント」から以下の情報をメモします。

- **エンドポイント**: `https://<your-resource-name>.openai.azure.com/`
- **API キー**: キー1 または キー2

---

## Step 2: GitHub リポジトリの準備

### 2-1. ディレクトリ構成

```
your-repo/
├── .github/
│   └── workflows/
│       └── terraform-ai-review.yml   # ワークフロー定義
├── infra/
│   ├── main.tf                        # Terraform 設定ファイル
│   ├── variables.tf
│   └── terraform.tfvars.example
└── scripts/
    └── analyze_plan.py                # AI 分析スクリプト
```

### 2-2. GitHub Secrets の設定

リポジトリの `Settings` → `Secrets and variables` → `Actions` で以下の Secrets を登録します。

| Secret 名               | 値                                |
| ----------------------- | --------------------------------- |
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI のエンドポイント URL |
| `AZURE_OPENAI_API_KEY`  | Azure OpenAI の API キー          |

:::note warn
⚠️ **セキュリティの注意**  
API キーはコードに直接書かず、必ず GitHub Secrets を使用してください。`.gitignore` に `*.tfvars` と `.env` を追加し、機密情報がリポジトリにコミットされないよう注意してください。
:::

---

## Step 3: AI 分析スクリプトの実装

`scripts/analyze_plan.py` を作成します。このスクリプトが `terraform plan` の出力を受け取り、Azure OpenAI で分析して PR コメント用の Markdown を生成します。

```python:scripts/analyze_plan.py
"""
terraform plan の出力を Azure OpenAI で分析し、
PR コメント用 Markdown を生成するスクリプト。
"""

import os
import sys
from datetime import datetime, timezone
from openai import AzureOpenAI


def analyze_terraform_plan(plan_text: str) -> dict:
    """terraform plan の出力を Azure OpenAI で分析する。"""

    client = AzureOpenAI(
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        api_version="2024-02-01",
    )

    system_prompt = """あなたはシニア DevOps エンジニアです。
terraform plan の出力を分析し、以下の構成で日本語の Markdown レポートを作成してください。

### 📋 変更サマリー
追加・変更・削除されるリソースの種類と数を簡潔にまとめる。

### 🔴🟡🟢 リスク評価
全体のリスクレベルを「🔴 高」「🟡 中」「🟢 低」のいずれかで評価し、理由を2〜3文で説明する。

### 🔍 注目すべき変更点
レビュアーが特に確認すべき変更を箇条書きで列挙する（最大5点）。

### ✅ 推奨アクション
マージ前に実施すべき確認事項を箇条書きで記載する。

レポートは簡潔で実用的な内容にしてください。"""

    user_prompt = f"""以下の terraform plan 出力を分析してください：

```

{plan_text[:8000]}

```
"""

    response = client.chat.completions.create(
        model=os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4o"),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=1500,
        temperature=0.2,  # 再現性を高めるため低めに設定
    )

    return {
        "analysis": response.choices[0].message.content,
        "tokens_used": response.usage.total_tokens,
        "model": os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4o"),
    }


def build_pr_comment(result: dict) -> str:
    """PR コメント用の Markdown 文字列を構築する。"""

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    return f"""## 🤖 AI による terraform plan レビュー

> このコメントは **Azure OpenAI ({result['model']})** により自動生成されました。
> 内容は参考情報です。最終的な判断は人間のレビュアーが行ってください。

{result['analysis']}

---

<details>
<summary>📊 分析メタデータ</summary>

- **モデル**: {result['model']}
- **使用トークン数**: {result['tokens_used']}
- **生成日時**: {timestamp}

</details>
"""


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python analyze_plan.py <plan_file>", file=sys.stderr)
        sys.exit(1)

    plan_file = sys.argv[1]

    with open(plan_file, "r", encoding="utf-8") as f:
        plan_text = f.read()

    if not plan_text.strip():
        print("⚠️  plan ファイルが空です。スキップします。", file=sys.stderr)
        # 空のコメントファイルを作成して後続ステップを通す
        with open("pr_comment.md", "w", encoding="utf-8") as f:
            f.write("## 🤖 AI レビュー\n\nterraform plan に変更はありませんでした。\n")
        return

    print("🔍 Azure OpenAI で terraform plan を分析中...")
    result = analyze_terraform_plan(plan_text)

    comment = build_pr_comment(result)

    with open("pr_comment.md", "w", encoding="utf-8") as f:
        f.write(comment)

    print(f"✅ 分析完了！（使用トークン: {result['tokens_used']}）")
    print("📄 pr_comment.md に出力しました")


if __name__ == "__main__":
    main()
```

:::note info
💡 **`plan_text[:8000]` について**  
Azure OpenAI のコンテキスト長には上限があります。非常に大きな Plan 出力の場合は先頭 8,000 文字で切り捨てています。より大きな Plan に対応するには、`max_tokens` を増やすか、Plan の差分部分のみを抽出する前処理を追加するとよいでしょう。
:::

---

## Step 4: GitHub Actions ワークフローの実装

`.github/workflows/terraform-ai-review.yml` を作成します。

```yaml:.github/workflows/terraform-ai-review.yml
name: Terraform Plan AI Review

on:
  pull_request:
    branches:
      - main
    paths:
      - "infra/**.tf"
      - "infra/**.tfvars"

# PR へのコメント書き込みに必要な権限
permissions:
  contents: read
  pull-requests: write

jobs:
  terraform-plan-review:
    name: Plan & AI Review
    runs-on: ubuntu-latest

    env:
      AZURE_OPENAI_ENDPOINT: ${{ secrets.AZURE_OPENAI_ENDPOINT }}
      AZURE_OPENAI_API_KEY: ${{ secrets.AZURE_OPENAI_API_KEY }}
      AZURE_OPENAI_DEPLOYMENT: gpt-4o
      TF_IN_AUTOMATION: true

    defaults:
      run:
        working-directory: ./infra

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: "1.9.0"

      - name: Terraform Format Check
        run: terraform fmt -check -recursive

      - name: Terraform Init
        run: terraform init

      - name: Terraform Validate
        run: terraform validate

      - name: Terraform Plan
        run: |
          terraform plan -no-color -out=tfplan 2>&1 | tee plan.txt
        continue-on-error: true  # Plan 失敗でも AI コメントを投稿する

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install Python dependencies
        run: pip install openai==1.30.0
        working-directory: .  # リポジトリルートから実行

      - name: Analyze Plan with Azure OpenAI
        run: python ${{ github.workspace }}/scripts/analyze_plan.py plan.txt

      - name: Post AI Review Comment to PR
        uses: marocchino/sticky-pull-request-comment@v2
        with:
          header: terraform-ai-review
          path: infra/pr_comment.md
```

### ワークフローのポイント解説

| 設定                                | 説明                                                         |
| ----------------------------------- | ------------------------------------------------------------ |
| `paths`                             | `.tf` ファイルに変更があった PR のみトリガー                 |
| `permissions: pull-requests: write` | PR へのコメント投稿に必要                                    |
| `sticky-pull-request-comment`       | 同じ PR への重複コメントを防ぎ、更新時は既存コメントを上書き |
| `continue-on-error: true`           | Plan がエラーでもAIコメントを届ける                          |

---

## Step 5: 動作確認

### 実際のコメント出力例

Pull Request を作成すると、数分後にこのようなコメントが自動投稿されます。

```markdown
## 🤖 AI による terraform plan レビュー

> このコメントは Azure OpenAI (gpt-4o) により自動生成されました。
> 内容は参考情報です。最終的な判断は人間のレビュアーが行ってください。

### 📋 変更サマリー

- **追加**: 3リソース（`azurerm_storage_account` × 1、`azurerm_storage_container` × 2）
- **変更**: 1リソース（`azurerm_resource_group` のタグ更新）
- **削除**: 0リソース

### 🔴🟡🟢 リスク評価

**🟡 中**

新規ストレージアカウントの追加は比較的安全な変更ですが、
パブリックアクセス設定が `enabled` になっている点は要注意です。
誤設定の場合、意図しないデータ公開につながる可能性があります。

### 🔍 注目すべき変更点

- `azurerm_storage_account.main` の `public_network_access_enabled = true`
  → 本番環境では `false` が推奨されます
- コンテナのアクセスレベルが `blob`（匿名読み取り可）に設定されています

### ✅ 推奨アクション

- [ ] ストレージアカウントのパブリックアクセス設定を再確認する
- [ ] `blob` アクセスレベルが意図的かどうか確認する
- [ ] 本番環境への適用前に `terraform plan` を再実行して差分がないことを確認する
```

---

## 発展的な活用法

### Azure DevOps パイプラインへの移植

Azure DevOps をお使いの場合、同じスクリプトを `azure-pipelines.yml` で利用できます。

```yaml:azure-pipelines.yml
trigger: none

pr:
  branches:
    include:
      - main
  paths:
    include:
      - "infra/*.tf"

pool:
  vmImage: ubuntu-latest

variables:
  - group: azure-openai-secrets  # Variable Group に API キーを格納

steps:
  - task: TerraformInstaller@1
    inputs:
      terraformVersion: "1.9.0"

  - task: TerraformTaskV4@4
    displayName: "Terraform Init"
    inputs:
      provider: azurerm
      command: init
      workingDirectory: "$(System.DefaultWorkingDirectory)/infra"

  - task: TerraformTaskV4@4
    displayName: "Terraform Plan"
    inputs:
      provider: azurerm
      command: plan
      workingDirectory: "$(System.DefaultWorkingDirectory)/infra"
      commandOptions: "-no-color -out=tfplan"

  - script: |
      terraform show -no-color tfplan > plan.txt
      pip install openai==1.30.0
      python scripts/analyze_plan.py plan.txt
    displayName: "AI Review with Azure OpenAI"
    workingDirectory: "$(System.DefaultWorkingDirectory)/infra"
    env:
      AZURE_OPENAI_ENDPOINT: $(AZURE_OPENAI_ENDPOINT)
      AZURE_OPENAI_API_KEY: $(AZURE_OPENAI_API_KEY)

  - task: PostComment@1
    displayName: "Post AI Review to PR"
    inputs:
      filePath: "$(System.DefaultWorkingDirectory)/infra/pr_comment.md"
```

### コスト管理のヒント

Azure OpenAI の利用コストを抑えるためのポイントをまとめます。

:::note info
💡 **コスト削減のTips**

- `max_tokens` を 1,500 に制限することで、1回の分析コストを抑える
- `terraform plan` の出力が変更なし（`No changes.`）の場合は API 呼び出しをスキップするロジックを追加する
- Plan 出力の全文ではなく、`Changes to Outputs:` 以降の差分部分だけを抽出して渡す
  :::

**変更がない場合のスキップ処理**を追加するには、スクリプトに以下を加えます。

```python:scripts/analyze_plan.py（追記例）
def has_changes(plan_text: str) -> bool:
    """terraform plan に実質的な変更があるかチェックする。"""
    no_change_markers = [
        "No changes. Your infrastructure matches the configuration.",
        "No changes. Infrastructure is up-to-date.",
    ]
    return not any(marker in plan_text for marker in no_change_markers)
```

`main()` 関数の冒頭でこのチェックを追加することで、変更がない PR への不要な API 呼び出しを防げます。

---

## トラブルシューティング

### Q: `AuthenticationError` が発生する

API キーかエンドポイントが間違っています。GitHub Secrets の値を確認してください。エンドポイントは末尾に `/` を含む形式（`https://xxx.openai.azure.com/`）が正しいです。

### Q: `DeploymentNotFound` エラーが出る

`AZURE_OPENAI_DEPLOYMENT` 環境変数に設定したデプロイ名が、Azure OpenAI Studio でのデプロイ名と一致しているか確認してください。

### Q: Plan ファイルが空になる

`terraform plan` の出力先パスが正しいか確認してください。`working-directory` の設定とファイルパスの相対位置に注意してください。

### Q: PR コメントが投稿されない

`permissions: pull-requests: write` がワークフローに設定されているか確認してください。また、リポジトリの設定で「Actions のワークフローに PR への書き込みを許可」が有効になっているか確認してください（`Settings` → `Actions` → `General` → `Workflow permissions`）。

---

## まとめ

この記事では、**Azure OpenAI × GitHub Actions** を組み合わせて、`terraform plan` の結果を AI が自動分析し、Pull Request にリスク評価コメントを投稿する仕組みを構築しました。

| ポイント             | 内容                                                  |
| -------------------- | ----------------------------------------------------- |
| **解決した課題**     | 長大な Plan 出力のレビュー負荷を AI が軽減            |
| **主な技術スタック** | Azure OpenAI (GPT-4o)、GitHub Actions、Terraform      |
| **実装のコア**       | Python スクリプト 1 本 + YAML ワークフロー 1 ファイル |
| **拡張性**           | Azure DevOps Pipelines でも同じスクリプトが再利用可能 |

AI によるレビューはあくまで **人間のレビューを補助するもの** です。最終的な承認判断は人間のエンジニアが行う設計を維持することが、安全な AI 活用の第一歩です。

ぜひ自分のプロジェクトに組み込んで、インフラレビューの効率化を試してみてください！

---

## 参考

- [Azure OpenAI Service ドキュメント](https://learn.microsoft.com/ja-jp/azure/ai-services/openai/)
- [Azure OpenAI Python ライブラリ](https://learn.microsoft.com/ja-jp/azure/ai-services/openai/quickstart?tabs=python)
- [GitHub Actions: Pull Request トリガー](https://docs.github.com/ja/actions/using-workflows/events-that-trigger-workflows#pull_request)
- [marocchino/sticky-pull-request-comment](https://github.com/marocchino/sticky-pull-request-comment)
- [hashicorp/setup-terraform Action](https://github.com/hashicorp/setup-terraform)
