---
title: "IaCの壁をぶっ壊せ！GitHub Copilot × Terraform/Bicep でAzureインフラを爆速構築するチュートリアル"
tags:
  - Azure
  - GitHubCopilot
  - Terraform
  - Bicep
  - IaC
---

## はじめに

「インフラをコードで管理（IaC）したいけど、TerraformやBicepの構文を覚えるのが大変…」  
特に学生やインフラ未経験のアプリエンジニアにとって、IaCの学習ハードルは意外と高いものです。

しかし、**GitHub Copilot** の登場により状況は一変しました。自然言語（日本語）で「〇〇を作って」と指示するだけで、適切なインフラコードを瞬時に生成してくれる時代になったのです。

この記事では、**GitHub Copilot を活用して Azure のインフラ（Terraform / Bicep）を爆速で自動生成し、デプロイする** 実践的なチュートリアルをお届けします。

**対象読者:**

- クラウドやIaCの学習を始めたばかりの学生・初学者
- アプリ開発がメインで、インフラ構築を手早く終わらせたいエンジニア
- CopilotがDevOpsの生産性をどう変えるか体験したい方

---

## なぜ GitHub Copilot × IaC なのか？

GitHub CopilotをIaCのコーディングに用いると、以下のような絶大なメリットがあります。

1. **構文（リファレンス）を調べる時間の消滅**
   「App ServiceのLinux版はどう書くんだっけ？」「SKUの指定方法は？」と公式ドキュメントを検索する時間がほぼゼロになります。
2. **学習効率の圧倒的向上**
   自分がやりたいことを自然言語で書き、生成されたコードを読むことで「こう書けばいいのか！」と直感的に学習できます。
3. **タイポや必須パラメータ漏れの防止**
   AIが依存関係を考慮してリソースを定義するため、手書きによるつまらないシンタックスエラーが減少します。

---

## 環境準備

以下の環境が揃っていることを前提とします。

- **VS Code**（推奨エディタ）
- **GitHub Copilot 拡張機能**（VS Code にインストール済み）
- **Azure サブスクリプション**（学生なら[Azure for Students](https://azure.microsoft.com/ja-jp/free/students/)がおすすめ）
- **Terraform**, **Bicep CLI**, **Azure CLI** のインストール

---

## 実践1：CopilotでTerraformを生成する

まずは汎用性の高い **Terraform** を使って、Webアプリをホストするための「Azure App Service」環境を作ってみましょう。

### 1. プロンプト（指示）を書く

VS Codeで `main.tf` という空のファイルを作成し、以下のコメントを打ち込みます。

```hcl
# Azureプロバイダーの設定
# 東日本リージョンにリソースグループ "rg-ai-demo" を作成する
# LinuxベースのApp Service Plan (SKUは B1) を作成する
# Node.js 18 で動くApp Service を作成する
```

### 2. Copilot にコードを自動生成させる

そのまま改行（Enter）を押して待つと、Copilotが続きのコードをグレーの文字（ゴーストテキスト）で提案してくれます。`Tab` キーを押して適用していきましょう。

![VS Code上でCopilotがコードを提案（ゴーストテキスト）しているスクショ](ここにスクショ①のURLを配置)

最終的に、以下のようなコードが数秒〜数十秒で完成します。

```hcl
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

# リソースグループの作成
resource "azurerm_resource_group" "example" {
  name     = "rg-ai-demo"
  location = "japaneast"
}

# App Service Planの作成
resource "azurerm_service_plan" "example" {
  name                = "plan-ai-demo"
  resource_group_name = azurerm_resource_group.example.name
  location            = azurerm_resource_group.example.location
  os_type             = "Linux"
  sku_name            = "B1"
}

# App Serviceの作成
resource "azurerm_linux_web_app" "example" {
  name                = "app-ai-demo-${random_integer.ri.result}" # 名前被り防止
  resource_group_name = azurerm_resource_group.example.name
  location            = azurerm_service_plan.example.location
  service_plan_id     = azurerm_service_plan.example.id

  site_config {
    application_stack {
      node_version = "18-lts"
    }
  }
}

# 名前衝突を防ぐためのランダム整数
resource "random_integer" "ri" {
  min = 10000
  max = 99999
}
```

### 3. デプロイを実行

あとはターミナルで以下のコマンドを叩くだけで、Azure上に環境がバッチリ構築されます。

```bash
terraform init
terraform plan
terraform apply
```

![Azure Portal上で実際に作成されたリソースのスクショ](ここにスクショ②のURLを配置)

---

## 実践2：CopilotでBicepを生成する

次に、AzureネイティブなIaC言語である **Bicep** を試してみます。BicepはTerraformよりもAzureに特化しており、より簡潔に書けるのが特徴です。

VS Codeで `main.bicep` を作成し、今度は **Copilot Chat（チャット画面）** を使ってお願いしてみます。

**ユーザーの入力:**

> `ストレージアカウント（Standard_LRS）を作成するBicepコードを書いて。名前は一意になるようプレフィックスに uniquestring を使ってね。`

**Copilot の出力:**

```bicep
@description('リソースのロケーション。デフォルトはリソースグループのロケーション。')
param location string = resourceGroup().location

@description('ストレージアカウントのプレフィックス')
param storagePrefix string = 'store'

// 一意なストレージアカウント名を生成
var storageAccountName = '${storagePrefix}${uniqueString(resourceGroup().id)}'

resource storageAccount 'Microsoft.Storage/storageAccounts@2022-09-01' = {
  name: storageAccountName
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    accessTier: 'Hot'
  }
}

output storageAccountId string = storageAccount.id
```

Azure特有の組み込み関数である `uniqueString()` や、リソースAPIのバージョン設定まで完璧にカバーしてくれました。

---

## AIと一緒にインフラを作る「プロンプト」のコツ

Copilotを使って期待通りのインフラコードを引き出すには、いくつかのコツがあります。

1. **前提バージョンを伝える**
   「Terraform Azure Provider v3系で〜」などと指定すると、非推奨になった古い書き方を提案されるのを防げます。
2. **クラウド特有の設定値を明確にする**
   「OSはLinux」「ランタイムはNode.js 18」など、具体的なスペック（SKU）を伝えると手戻りが減ります。
3. **セキュリティや命名規則を指示する**
   「リソースには環境タグ(env=dev)をつけて」「パブリックアクセスは無効化して」などと指示すると、本番運用を見据えたコードを生成してくれます。

---

## まとめ

インフラの構築（IaC）は、かつて分厚いドキュメントと睨めっこしながら進める修行のような作業でしたが、今は **GitHub Copilot と壁打ちしながら最速でベストプラクティスを組み上げる** 時代に突入しました。

初学者や学生にとって、Copilotは「いつでも質問できる凄腕の先輩エンジニア」です。「どう書くの？」ではなく「何を作りたいか？」という本来のアーキテクチャ設計に集中するためにも、ぜひ Copilot を使い倒してみてください！

---

## 参考

- [Azure Bicep のドキュメント](https://learn.microsoft.com/ja-jp/azure/azure-resource-manager/bicep/)
- [Terraform Azure Provider ドキュメント](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)
- [GitHub Copilot の使い方](https://docs.github.com/ja/copilot)
