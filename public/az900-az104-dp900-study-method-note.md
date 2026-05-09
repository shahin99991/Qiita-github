# インフラ未経験の大学1年生が3ヶ月でAZ-104まで五つ取得した方法｜AIプロンプト×2タブ学習法とAZ-305への道

Azureの勉強環境は無料で作れます。Azure for Studentsなら、クレジットカード不要で始められます。  
https://azure.microsoft.com/free/students?wt.mc_id=studentamb_486039

## はじめに：自己紹介

はじめまして。現在大学1年生のロホマンシャヒンです。

ソフトウェア開発の経験はありましたが、インフラ・クラウドは完全に未経験の状態から、インターン開始前の約3ヶ月で

- AZ-900
- AI-900
- SC-900
- AZ-104

を取得し、さらに**AZ-104の次にDP-900も取得**しました（合計5資格）。

現在は地方電力会社で、Azureインフラの設計・構築・運用・保守のインターンに従事しています。この記事では、そのときに使ったAI活用学習法と、最終的にAZ-305取得を目指す上でのポイントを共有します。

## 取得した資格の概要

| 試験   | 正式名                                         | レベル | 合格点   | 受験料（日本） |
| ------ | ---------------------------------------------- | ------ | -------- | -------------- |
| AZ-900 | Azure Fundamentals                             | 初級   | 700/1000 | ¥12,180        |
| AI-900 | Azure AI Fundamentals                          | 初級   | 700/1000 | ¥12,180        |
| SC-900 | Security, Compliance and Identity Fundamentals | 初級   | 700/1000 | ¥12,180        |
| AZ-104 | Azure Administrator                            | 中級   | 700/1000 | ¥20,300        |
| DP-900 | Azure Data Fundamentals                        | 初級   | 700/1000 | ¥12,180        |
| AZ-305 | Designing Azure Infrastructure Solutions       | 上級   | 700/1000 | ¥20,300        |

※ 「700/1000点 = 正答率70%」ではありません。問題難易度によってスコアがスケーリングされます。

### AZ-104とAZ-305の違いを知っておく

AZ-305を意識してAZ-104を勉強すると効率が上がります。2つは別の思考法を問われます。

|            | AZ-104（管理者）                   | AZ-305（設計者）                                 |
| ---------- | ---------------------------------- | ------------------------------------------------ |
| 問いかけ   | このVMをどう設定するか             | このビジネス要件を満たす設計は何か               |
| 軸         | 操作・設定・トラブルシューティング | なぜこの設計かの根拠                             |
| キーワード | 手順・コマンド・制約               | トレードオフ・Well-Architected・コスト vs 信頼性 |

AZ-305は単なる操作の延長ではなく、Azure Well-Architected Frameworkの5柱（信頼性・セキュリティ・コスト最適化・オペレーショナルエクセレンス・パフォーマンス効率）をベースに「なぜこの構成か」を答える試験です。

## 学生は絶対使うべき：Azure for Students

Azure for Studentsに申し込むと、クレジットカード不要で$100分（約1.5万円相当）のクレジット + 多数の無料サービスが使えます。

### 申請方法

1. https://azure.microsoft.com/ja-jp/free/students/ にアクセス
2. 大学の組織メールアドレス（例: @学籍番号.大学名.ac.jp）でサインアップ
3. 学生認証が通れば利用開始

注意:

- 商用・本番用途には利用できません。
- 無料枠の内容は変更される場合があります。
- 最新情報は公式ページをご確認ください。

### 検証環境として活用できる主なサービス

| サービス                      | 無料枠                                |
| ----------------------------- | ------------------------------------- |
| Azure Virtual Machines（B1s） | 750時間/月（常時）                    |
| Azure SQL Database            | 100,000 vCore秒/月（常時）            |
| Azure Container Registry      | Standard 1レジストリ・100GB（12ヶ月） |
| Azure DevOps                  | 5ユーザー無制限（常時）               |

AZ-104の勉強で「実際に手を動かしたい」場面にかなり有効です。仮想マシンを立て、NSGを設定し、Bastionで接続する、といった操作を無料で反復できます。

## 私のAI活用学習法

核心は「AIを問題生成マシン兼、解説パートナーとして徹底活用する」ことです。主にGeminiを使いましたが、ChatGPTでも同様に実践可能です。

### 2タブ同時起動が効率の鍵

| タブ  | 役割                                       |
| ----- | ------------------------------------------ |
| タブ1 | AIが出した問題を解く（理解度チェック）     |
| タブ2 | 解説・深掘り専用（わからない問題を即質問） |

この2タブ構成で「解く -> 詰まる -> 解説 -> 次へ」を止めずに回せます。

### Step 1：目次を出してもらう

まずAIに試験範囲の地図を作ってもらいます。

参考書を使っている場合:

```text
現在この本を使って〇〇試験の勉強をしている。
この本と併用してGemini/ChatGPTで問題を出してもらって理解を深めたい。
まず、目次を出して。
```

参考書を使わない場合:

```text
現在〇〇試験の勉強をしている。
公式の試験範囲をもとに目次を出して。
```

AZ-900・AI-900・SC-900・DP-900はMicrosoft Learnを中心に進め、AZ-104は学習ガイドを軸にしました。これで学習範囲の取りこぼしが減ります。

### Step 2：章ごとにUIベースの問題を出してもらう

1回あたりの出題数はGeminiの方が多く、章単位で回しやすいです。

| AI      | 1回あたりの最大出題数 |
| ------- | --------------------- |
| Gemini  | 50問                  |
| ChatGPT | 20問                  |

使用したプロンプト例:

```text
第1章の問題を50問出題して。UIベースの選択問題で。
【出力形式の指示】生成する回答において、選択肢の文章全体を太字にすることを禁止します。
質問文、選択肢A, B, C, Dの本文は、すべて標準の文字（太字ではない）で出力してください。
```

太字禁止を入れないと、正解選択肢だけ強調されてしまうことがあり、演習として成立しません。UIベース指定も、本番形式に寄せるために有効でした。

### Step 3：わからない問題はすぐ解説タブへ

わからない問題は、別タブで即質問します。

```text
現在AZ-〇〇試験を勉強している。わからない部分や理解が浅い部分を聞くので解説して。

解説した後に、同じような問題が出た時に答えられる知識を教えて。
また305をいずれ取ろうと思うので、そのアーキテクチャ思考でも別で解説して。
305合格につながる形で教えて。
```

「アーキテクチャ思考でも解説して」を入れることで、AZ-104の学習内容がAZ-305の土台になります。

## ロードマップ（私の場合）

```text
月1：AZ-900（クラウド基礎）
     ↓ Azure for Studentsを申請
     ↓ 検証環境で実際に触る
月2：AI-900 + SC-900（同時並行）
     ↓
月3：AZ-104（手を動かす）
     ↓
月4：DP-900（AZ-104の次に取得。データ基礎を補強）
     ↓
現在：AZ-305勉強中（アーキテクチャ思考を鍛える）
```

## AZ-305を見据えたAZ-104の勉強法

AZ-104を学ぶ段階から、次の問いを常に持つと理解が深まります。

- このサービスはどんなビジネス課題を解決するのか
- どんな時に選び、どんな時に選ばないのか

例: VPN GatewayとExpressRoute

- AZ-104視点: 設定項目・SKU・制約を把握する
- AZ-305視点: コスト・可用性・セキュリティのトレードオフで設計判断する

この2視点を往復する癖がつくと、設計問題への対応力が上がります。

### AZ-104試験中はMicrosoft Learnを参照できる

AZ-104は試験中にMicrosoft Learnを参照できます。普段からLearn中心で勉強すると、本番で必要情報に素早く辿り着けます。

## まとめ

この記事の要点です。

- Azure for Studentsで無料の検証環境を確保する
- AIに「目次 -> 章ごと問題作成」をさせ、演習量を増やす
- 問題タブ + 解説タブの2タブ構成で学習を止めない
- AZ-104の次にDP-900を取得し、データ領域の基礎も補強する
- 解説プロンプトに「AZ-305の設計思考」を含め、次資格の土台を作る
- 普段からMicrosoft Learnを使い、本番での検索速度を上げる

資格は通過点ですが、学習段階で「なぜこの設計か」を考える習慣を持つと、現場での理解速度が大きく変わります。次はAZ-305に向けて一緒に頑張りましょう。

## 参考

- AZ-900: https://learn.microsoft.com/ja-jp/credentials/certifications/azure-fundamentals/
- AI-900: https://learn.microsoft.com/ja-jp/credentials/certifications/azure-ai-fundamentals/
- SC-900: https://learn.microsoft.com/ja-jp/credentials/certifications/security-compliance-and-identity-fundamentals/
- AZ-104: https://learn.microsoft.com/ja-jp/credentials/certifications/azure-administrator/
- DP-900: https://learn.microsoft.com/ja-jp/credentials/certifications/azure-data-fundamentals/
- AZ-305: https://learn.microsoft.com/ja-jp/credentials/certifications/exams/az-305/
- Azure Well-Architected Framework: https://learn.microsoft.com/ja-jp/azure/well-architected/pillars
- Azure for Students: https://azure.microsoft.com/ja-jp/free/students/
- 学生向け認定資格割引: https://learn.microsoft.com/ja-jp/credentials/certifications/student-discounts
