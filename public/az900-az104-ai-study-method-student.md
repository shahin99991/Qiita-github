---
title: "インフラ未経験の大学1年生が3ヶ月でAZ-104まで取得した方法｜AIプロンプト×2タブ学習法とAZ-305への道"
tags:
  - Azure
  - 資格
  - AI
  - 勉強法
  - 学生
private: false
updated_at: ''
id: null
organization_url_name: null
slide: false
ignorePublish: false
---

## はじめに：自己紹介

はじめまして。現在大学1年生のshahinと申します。

ソフトウェア開発の経験はありましたが、**インフラ・クラウドは完全に未経験**の状態から、**インターン開始前の約3ヶ月でAZ-900・AI-900・SC-900・AZ-104を取得**しました。現在は地方電力会社でAzureインフラの設計・構築・運用・保守のインターン（2ヶ月目）に従事しています。

この記事では、そのときに使ったAI活用学習法と、最終的にAZ-305取得を目指す上でのポイントを共有します。

<details><summary>📋 詳しいプロフィール（読み飛ばしOK）</summary>

**高校時代**
- XAIについて学会発表
- 技育CAMPハッカソン参加（完走）
- 42Tokyo Piscine受験（250時間のC言語集中学習）
- 2025技育祭春 学生アンバサダー就任
- Google × Zennハッカソン参加（完走・award受賞）
- Python業務委託システム開発
- 技育展 学生審査員
- Google Chrome拡張機能リリース（音声ブラウザ操作・アクセシビリティ向上）

**大学1年**
- SaaSスタートアップ：Python / GraphQLバックエンド開発（4ヶ月）
- AI・データサイエンス系スタートアップ：Python / ML（3ヶ月）
- EngineerGuildハッカソン 決勝進出（Next.js・Python・PostgreSQL・GCP・Kafka・Prometheus・Grafana・CI/CD）
- 学内コンテスト：Gemini API + RAGを用いたSlackBot開発
- 2025技育祭秋 アンバサダー
- プログラミング教室講師（1ヶ月）
- **地方電力会社にてAzureインフラの設計・構築・運用・保守（現在）**
- AzureコミュニティYonaAZにて登壇

**取得資格**：AZ-900 / AI-900 / SC-900 / AZ-104 → 現在AZ-305勉強中

</details>

---

## 取得した資格の概要

| 試験 | 正式名 | レベル | 合格点 | 受験料（日本） |
|------|--------|--------|--------|--------------|
| AZ-900 | Azure Fundamentals | 初級 | 700/1000 | ¥12,180 |
| AI-900 | Azure AI Fundamentals | 初級 | 700/1000 | ¥12,180 |
| SC-900 | Security, Compliance and Identity Fundamentals | 初級 | 700/1000 | ¥12,180 |
| AZ-104 | Azure Administrator | 中級 | 700/1000 | ¥20,300 |
| **AZ-305** | **Designing Azure Infrastructure Solutions** | **上級** | **700/1000** | **¥20,300** |

:::note info
💡 **スコアについて**: 「700/1000点＝正答率70%」ではありません。問題の難易度によってスコアがスケーリングされるため、実際の合格ラインは問題セットごとに異なります。
:::

### AZ-104とAZ-305の違いを知っておく

AZ-305を意識してAZ-104を勉強すると効率が上がります。この2つはまったく別の「思考法」を問います。

| | AZ-104（管理者） | AZ-305（設計者） |
|--|--|--|
| 問いかけ | 「このVMをどう設定するか」 | 「このビジネス要件を満たす設計は？」 |
| 軸 | 操作・設定・トラブルシューティング | なぜこの設計か、の根拠 |
| キーワード | 手順・コマンド・制約 | トレードオフ・Well-Architected・コスト vs 信頼性 |

AZ-305は単なる操作の延長ではなく、**Azure Well-Architected Framework の5柱**（信頼性・セキュリティ・コスト最適化・オペレーショナルエクセレンス・パフォーマンス効率）をベースに「なぜこの構成か」を答える試験です。

---

## 学生は絶対使うべき：Azure for Students

Azure for Studentsに申し込むと、**クレジットカード不要で$100分（約1.5万円相当）のクレジット + 65種類以上の常時無料サービス**が使えます。

### 申請方法

1. [azure.microsoft.com/ja-jp/free/students/](https://azure.microsoft.com/ja-jp/free/students/) にアクセス
2. 大学の**組織メールアドレス**（`@学籍番号.大学名.ac.jp` など）でサインアップ
3. 学生認証が通れば即日利用開始

:::note warn
⚠️ **注意**: 商用・本番用途には利用できません。あくまで学習・検証目的での活用です。無料枠の内容は変更される場合があります。最新情報は[公式ページ](https://azure.microsoft.com/ja-jp/free/students/)でご確認ください。
:::

### 検証環境として活用できる主なサービス

| サービス | 無料枠 |
|--------|--------|
| Azure Virtual Machines（B1s） | 750時間/月（常時） |
| Azure SQL Database | 100,000 vCore秒/月（常時） |
| Azure Container Registry | Standard 1レジストリ・100GB（12ヶ月） |
| Azure DevOps | 5ユーザー無制限（常時） |

AZ-104の勉強で「実際に手を動かしたい」場面で大活躍します。仮想マシンを立て、NSGを設定し、Bastionで接続する……という操作を**無料で何度でも試せる**のは本当に助かりました。

---

## 私のAI活用学習法

この学習法の核心は **「AIを問題生成マシン＆解説パートナーとして徹底活用する」** ことです。主にGeminiを使用しました（ChatGPTでも同様に動きます）。

### 2タブ同時起動が効率の鍵

| タブ | 役割 |
|------|------|
| **タブ①** | AIが出した問題を解くタブ（理解度チェック） |
| **タブ②** | 解説・深掘り専用タブ（わからない問題をすぐ質問） |

この2タブ構成により、「問題を解く→わからない→すぐ解説→次の問題」のサイクルが途切れません。

### Step 1：目次を出してもらう

まずAIに試験範囲の地図を作らせます。

**参考書を使っている場合：**
```
現在この本を使って〇〇試験の勉強をしている。
この本と併用してGemini/ChatGPTで問題を出してもらって理解を深めたい。
まず、目次を出して。
```

**参考書を使わない場合：**
```
現在〇〇試験の勉強をしている。
公式の試験範囲をもとに目次を出して。
```

私はAZ-900・AI-900・SC-900はMicrosoft公式の無料学習パス（Microsoft Learn）を使い、AZ-104は「[試験AZ-104：Microsoft Azureの管理](https://learn.microsoft.com/ja-jp/credentials/certifications/azure-administrator/)」の学習ガイドを参照しました。こうすることで「今自分はどこを学んでいるか」が俯瞰でき、範囲の網羅性を保てます。

### Step 2：章ごとにUIベースの問題を50問出してもらう

```
第1章の問題を50問出題して。UIベースの選択問題で。
【出力形式の指示】生成する回答において、選択肢の文章全体を太字にすることを禁止します。
質問文、選択肢A, B, C, Dの本文は、すべて標準の文字（太字ではない）で出力してください。
```

:::note info
💡 **「UIベース」がポイント**: 「試験画面のような形式で出して」という意味です。これを指定しないとAIが自由なフォーマットで出力してしまい、本番試験の形式に慣れられません。また太字禁止の指示を入れると、問題が読みやすくなります。
:::

こうして出てきた問題を「作業しながら画面の端で解きまくる」のが私のスタイルです。通勤・隙間時間・ながら作業の全てを学習時間に変えられます。

### Step 3：わからない問題はすぐ解説タブへ

問題を解いていてわからない部分が出たら、別タブのAIに即聞きます。

```
現在AZ-〇〇試験を勉強している。わからない部分や理解が浅い部分を聞くので解説して。

解説した後に、同じような問題が出た時に答えられる知識を教えて。
また305をいずれ取ろうと思うので、そのアーキテクチャ思考でも別で解説して。
305合格につながる形で教えて。
```

このプロンプトの **「アーキテクチャ思考でも別で解説して」** という部分が重要です。

例えば「Azure SQL DatabaseとAzure SQL Managed Instanceの違い」をAZ-104の観点で聞くと「設定方法の違い」が返ってきます。でもこのプロンプトを使うと追加で：

> 「AZ-305の視点では、SQL MIを選ぶのはオンプレミスのSQL Serverからのリフト＆シフト移行で互換性を最大化したいシナリオ。Azure SQL Databaseは新規開発でスケールとコスト最適化を優先する場合。Well-Architected FrameworkのコストとパフォーマンスのトレードオフとしてXXXを考慮する……」

というように、**今の試験勉強が将来の305に自動的に繋がる解説**が返ってきます。AZ-104を勉強しながら305の土台を積める一石二鳥の学習法です。

---

## ロードマップ（私の場合）

```
月1：AZ-900（Azureって何？クラウドって何？）
     ↓ Azure for Studentsを申請
     ↓ 検証環境で実際に触る
月2：AI-900 + SC-900（同時並行でOK。両方基礎レベル）
     ↓
月3：AZ-104（実際に手を動かす。Azure for Studentsフル活用）
     ↓
現在：AZ-305勉強中（アーキテクチャ思考を鍛える）
```

:::note info
💡 **AI-900とSC-900は同時並行がおすすめ**: どちらも45分の試験でAZ-900の知識を前提に構成されています。別々に集中するより、AZ-900直後の知識が新鮮なうちに2つまとめて仕上げる方が効率的です。
:::

---

## AZ-305を見据えたAZ-104の勉強法

AZ-104を勉強する段階から305を意識すると、理解の深さが変わります。

### 意識すること

**AZ-104で各サービスを学ぶとき、この問いを常に持つ：**

> 「このサービスはどんなビジネス課題を解決するために存在するのか？」
> 「どんな時にこのサービスを選び、どんな時に選ばないのか？」

例えば VPN GatewayとExpressRouteを勉強する時：

- **AZ-104的理解**: 「VPN GatewayはIKEv2/IKEv1を使う。SKUがBasic/VpnGw1…の違いは〇〇」
- **AZ-305的理解**: 「ExpressRouteは帯域保証・プライベート接続が必要な金融・医療系に選ぶ。VPN Gatewayはコスト優先・インターネット回線で許容できるシナリオ向け。ただしExpressRoute + VPN GatewayのフェイルオーバーをHigh Availabilityのトレードオフとして設計するパターンも出る」

前述の解説プロンプトを使えば、この「AZ-305的理解」が自動で付いてきます。

---

## まとめ

この記事の内容を整理します：

- **Azure for Students** を申請して無料の検証環境を手に入れる
- **AIに目次 → 章ごと50問** のサイクルで問題を量産させる
- **問題タブ + 解説タブ** の2タブ構成で学習を途切れさせない
- 解説プロンプトに **「305のアーキテクチャ思考でも解説して」** を入れることで、AZ-104勉強が305の土台になる

資格はあくまで通過点ですが、インフラ系の業務に入る前にAZ-104相当の知識があると、現場での理解速度が全然違います。特に**「なぜこの設計か」を考える習慣**は、資格の勉強中から意識するだけで、エンジニアとしての質が上がると感じています。

一緒にAZ-305目指しましょう！

## 参考

- [AZ-900 試験ページ](https://learn.microsoft.com/ja-jp/credentials/certifications/azure-fundamentals/)
- [AI-900 試験ページ](https://learn.microsoft.com/ja-jp/credentials/certifications/azure-ai-fundamentals/)
- [SC-900 試験ページ](https://learn.microsoft.com/ja-jp/credentials/certifications/security-compliance-and-identity-fundamentals/)
- [AZ-104 試験ページ](https://learn.microsoft.com/ja-jp/credentials/certifications/azure-administrator/)
- [AZ-305 試験ページ](https://learn.microsoft.com/ja-jp/credentials/certifications/exams/az-305/)
- [Azure Well-Architected Framework](https://learn.microsoft.com/ja-jp/azure/well-architected/pillars)
- [Azure for Students](https://azure.microsoft.com/ja-jp/free/students/)
- [学生向け認定資格割引](https://learn.microsoft.com/ja-jp/credentials/certifications/student-discounts)
