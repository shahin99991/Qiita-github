---
title: "GH-900（GitHub Foundations）合格体験記 — 特にIT業界志望の学生におすすめしたい資格"
tags:
  - GitHub
  - Git
  - 資格
  - 勉強法
  - 初心者
private: false
updated_at: "2026-09-16T12:00:00+09:00"
id: ea071b25d62da902719a
organization_url_name: mspjp
slide: false
ignorePublish: false
---

## はじめに

GitHub Copilot User Group Japan運営兼、Microsoft Student Ambassadorのロホマン シャヒンです。
![詳細なプロフィールはこちらから（Portfolio）](https://shahin99991.github.io/Myportfolio/)

:::note
この記事が少しでも参考になったら、**ぜひいいね・共有**をお願いします。
:::

2026年9月8日、GH-900（GitHub Foundations）に合格しました（得点：855/700）。先日 [AI-901の合格体験記](https://qiita.com/shahin0809/items/aa9ca5194843559806be) を書いたばかりですが、今回はGitHubの資格です。

![試験結果スコアレポート（得点：855 / 合格点：700）](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/GH-900/Images/img-exam-result.png)

勉強期間は約1週間、使った教材は「書籍1冊 + Udemy問題集」のみ。この組み合わせが思った以上に相性が良かったので、試験の紹介とあわせて勉強法をまとめておきます。

---

## なぜGH-900を受けるべきか — GitHubはIT業界の登竜門

先に言わせてください。**学生やITを勉強し始めた人こそ、この試験を受けてほしいです！**

GitHubはもはや、IT業界で働く上での登竜門だと思っています。コードのバージョン管理、Issueでのタスク管理、Pull Requestでのレビュー、Actionsでの自動化。どの会社の開発現場を見ても、GitHubか同等のGitサービスが必ず回っています。就活やインターンの面接で「GitHubアカウントを見せてください」と言われることも普通になってきました。

ただ、GitHubって「使っているつもり」になりがちなツールでもあります。`clone`・`commit`・`push` だけはできるけど、PRのレビュー運用やブランチ保護、Projectsでの管理はよく分からない。そういう方多いと思います。

GH-900は、その「基礎が本当にできているか」を**客観的に証明できる資格**です。GitHub公式の認定資格で、前提資格もなし。難易度はFundamentals級なので、学生でも十分に手が届きます。

毎日GitHubを触っている自分が言うのもアレですが、**本当におすすめです！**

---

## GH-900（GitHub Foundations）とは

GitHub Foundationsは、GitHub公式の認定資格です（現在はMicrosoft Credentialsとして提供されています）。Gitやリポジトリ、コラボレーション機能、プロジェクト管理、最新の開発プラクティスなど、GitHubの基礎知識を持っているかを測る試験で、対象は**開発者・非開発者を問わないすべてのGitHubユーザー**。エンジニア志望じゃなくても受けられる設計になっています。

### 試験の基本情報

| 項目       | 内容                                               |
| ---------- | -------------------------------------------------- |
| 試験コード | GH-900                                             |
| 認定資格名 | GitHub Foundations                                 |
| レベル     | 初級（Fundamentals）                               |
| 合格点     | 700点（1000点スケール）                            |
| 試験時間   | 100分                                              |
| 前提資格   | なし                                               |
| 対応言語   | 英語・日本語・スペイン語・ポルトガル語・韓国語     |
| 受験料     | 国・地域によって異なる（試験ページで確認できます） |

日本語で受けられるのは地味にありがたいポイントです。自分も日本語で受験しました。

### 出題範囲（2026年1月の大幅更新後）

GH-900は比較的新しい試験で、**2026年1月に出題範囲が大幅に更新**されています（目標の追加・削除・再編成が行われました）。最新の出題構成は7セクションです。

| セクション                                  | 出題比率 |
| ------------------------------------------- | -------- |
| 1. GitとGitHubの基本を理解する              | 25〜30%  |
| 2. GitHubリポジトリを操作する               | 10〜15%  |
| 3. GitHubを使用した共同作業                 | 10〜15%  |
| 4. 最新の開発プラクティスを適用する         | 10〜15%  |
| 5. GitHubを使用してプロジェクトを管理する   | 5〜10%   |
| 6. プライバシー、セキュリティ、管理について | 10〜15%  |
| 7. GitHubコミュニティを探索する             | 5〜10%   |

最大ウェイトは「GitとGitHubの基本」。バージョン管理の目的、GitとGitHubの違い、GitHub Flow、Markdownあたりがここに入ります。

注目なのがセクション4で、**GitHub ActionsやGitHub Copilotも出題範囲**です。Copilotに至っては、エージェントモードやマルチモデル対応、個人・Business・Enterpriseプランの違いまで問われます。Actions・Copilot・Codespacesと、いまどきのGitHub開発をちゃんとカバーしている試験なんですよね。だからこそ、取っておくと「最近のGitHubも分かってる人」の証明になります。

:::note info
💡 Microsoft公式の無料リソースも充実しています。[GitHub Foundationsのラーニングパス](https://learn.microsoft.com/ja-jp/training/paths/github-foundations/)（パート1・2）、本番形式の[練習評価](https://learn.microsoft.com/ja-jp/credentials/certifications/github-foundations/)、試験画面を体験できる[サンドボックス](https://GHCertDemo.starttest.com)が無料で使えます。
:::

---

## 実際の勉強方法（約1週間）

自分は普段からGitHubを触っていたので、勉強は**約1週間**で仕上げました。やったことは3ステップだけです。

### ① 書籍「読んでつなげる GitHub」を一周読む

最初に手を付けたのが、書店で買える[『読んでつなげる GitHub GH-900 GitHub Foundations 対応』（Compass Books）](https://www.amazon.co.jp/dp/4839991418)です。

GH-900は新しい試験なのに、もうちゃんとした対策本が本屋に並んでいるんですよね。これがありがたかった。この本は、GitとGitHubの違いから始まって、リポジトリ・コミット・ブランチ・Pull Request・Actions・Copilot・Projects・セキュリティまで、試験範囲を順番に網羅しています。

いきなり問題集から入る手もあったんですが、範囲が広い試験なので、まず**本で全体像を分かりやすく理解する**ルートを選びました。結果としてこれが正解だったと思います。

### ② 本の問題集を解く

本を読み終えたら、巻末・章末の問題を一周解きました。読んだばかりの内容をすぐ問題で確認する形です。

ここでの間違いは、だいたい「読み飛ばしていた箇所」そのままでした。答え合わせしながら該当ページに戻る、を繰り返して土台を固めた感じです。

### ③ Udemyの問題集を9割超えるまで解く

仕上げはUdemyの[【うかる！】GH-900：GitHub Foundations 最強問題集](https://www.udemy.com/course/gh-900github-foundations-certification/)です。

![Udemy 問題集のコースページ](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/GH-900/Images/img-udemy-course.png)

模擬試験が6セット収録されていて、1セット50問・計300問というボリューム。各セットは85分の制限時間付きで、本番を想定した演習ができます。

![収録されている模擬試験（6セット）](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/GH-900/Images/img-udemy-curriculum.png)

実際の正答率がこちらです。

<div>
<img src="https://raw.githubusercontent.com/shahin99991/Qiita-github/main/GH-900/Images/img-quiz-scores-1-3.png" width="49%" alt="模擬試験1〜3の結果（74% / 82% / 88%）">
<img src="https://raw.githubusercontent.com/shahin99991/Qiita-github/main/GH-900/Images/img-quiz-scores-4-6.png" width="49%" alt="模擬試験4・6の結果（92% / 91%）">
</div>

| 問題セット | 正答率 | スコア |
| ---------- | ------ | ------ |
| セット 1   | 74%    | 37/50  |
| セット 2   | 82%    | 41/50  |
| セット 3   | 88%    | 44/50  |
| セット 4   | 92%    | 46/50  |
| セット 6   | 91%    | 46/50  |

初回は74%しか取れませんでした。出題範囲の広さが見えて正直ちょっと怖くなったので、**9割を安定して超えるまで解き直す**ことにしました。間違えた問題は解説を読んで、本の該当箇所にも戻る。これを繰り返して、4セット目で92%、6セット目でも91%と安定してきたタイミングで受験を決めました。

本番は問題集より少しひねった聞かれ方をする問題もありましたが、問題集で9割安定していれば合格ラインには届く感触でした（実際855点でした）。

### この順番がおすすめな理由

- **本 → 問題集の順が大事**です。広い範囲をいきなり問題で攻めると、知らない用語の連続で心が折れかけます。先に本で「GitHubってこういう作りなんだ」という地図を持っておくと、間違えた問題が地図のどの場所か分かるので、復習が一気に速くなります
- 逆に本だけだと「分かったつもり」で終わるので、Udemyの問題集でアウトプットして抜けを潰す。この2段構成が一番効率が良かったです

---

## 受けてみて分かったこと

### 領域別スコアを見ての反省

スコアレポートの領域別の結果がこちらです。

| 領域                               | 正答率 |
| ---------------------------------- | ------ |
| 基本的なトピック、製品、概念の理解 | 97%    |
| GitHub での作業                    | 87%    |
| GitHub での貢献                    | 77%    |
| GitHub での共同作業                | 71%    |

基本概念はほぼ満点だったんですが、**共同作業（Issue・Pull Request・Discussion・通知まわり）が71%で最低**でした。毎日使っているつもりでも、テンプレートや通知設定みたいな細かい機能は曖昧だったようです。日常で使う範囲と、試験で問われる範囲はやっぱり違うな、と痛感しました。

### 範囲の広さが唯一の敵

GH-900で大変なのは難しさよりも**広さ**です。GitHub MarketplaceやGitHub Sponsors、InnerSourceのような、普段の開発では触れない領域からも出題されます。「そんな機能あったんだ」というのが問題集を解いていて何度かありました。

### 触ってみるのが一番。でも最低限この2教材で受かる

一番のおすすめは、**実際にGitHubを触ること**です。無料アカウントでリポジトリを作ってIssueを立てて、Actionsを回して、Projectsでカンバンを並べてみる。検証すると知識の定着がまったく違います。

その上であえて最低ラインを言うなら、**今回紹介した本とUdemy問題集をやり切れば受かります**。範囲が広い試験なので、教材を絞って繰り返すのが近道でした。

---

## まとめ

- GH-900はGitHubの基礎を証明できる公式資格。**学生・IT初心者の登竜門として本当におすすめ**です
- 2026年1月に出題範囲が大幅更新され、ActionsやCopilotなど最新の話題も出るようになった
- 勉強は約1週間。「読んでつなげる GitHub」を一周 → 本の問題集 → Udemy問題集を9割安定まで
- 本で全体像を掴んでから問題を解く順番が一番効率的
- 触って検証するのが一番。最低限、本 + 問題集の2教材で合格できる

GitHubの認定資格には他にも、Actions（GH-200）やGitHub Copilot（GH-300）、Administration（GH-100）などがあります。自分はこの調子でGitHub系の資格も攻めていくつもりです。また受かったら体験記を書きます！

---

## 参考

- [GitHub Foundations 認定資格 — Microsoft Learn](https://learn.microsoft.com/ja-jp/credentials/certifications/github-foundations/)
- [試験 GH-900 の学習ガイド — Microsoft Learn](https://learn.microsoft.com/ja-jp/credentials/certifications/resources/study-guides/gh-900)
- [GitHub Foundations ラーニングパス パート1 — Microsoft Learn](https://learn.microsoft.com/ja-jp/training/paths/github-foundations/)
- [GitHub Foundations ラーニングパス パート2 — Microsoft Learn](https://learn.microsoft.com/ja-jp/training/paths/github-foundations-2/)
- [『読んでつなげる GitHub GH-900 GitHub Foundations 対応』（Compass Books）— Amazon](https://www.amazon.co.jp/dp/4839991418)
- [【うかる！】GH-900：GitHub Foundations 最強問題集 — Udemy](https://www.udemy.com/course/gh-900github-foundations-certification/)
