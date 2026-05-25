---
title: "GitHub Copilot App が来た。VSCode のCopilotと何が違うの？インストールから使い方まで全部まとめた"
tags:
  - GitHubCopilot
  - GitHub
  - VSCode
  - AI
  - 生産性向上
private: false
updated_at: ""
id: null
organization_url_name: null
slide: false
ignorePublish: false
---

## はじめに

「GitHub Copilot App って何？VSCode のやつとどう違うの？」

最近こういう声をよく聞くようになってきました。2026年に入ってから GitHub が **デスクトップアプリ版の GitHub Copilot** をパブリックプレビューとして公開しています。名前は **GitHub Copilot app**（通称：Copilot アプリ）。

正直なところ、最初は「別にVSCodeで十分じゃない？」って思ってたんですが、実際に触ってみたら結構コンセプトが違いました。エージェント駆動の開発を念頭に置いて設計されていて、IDE の外でも動くのがキモでした。

この記事では以下のことをまとめています！

- ✅ GitHub Copilot App のインストール方法（スクショ付きで全手順）
- ✅ VSCode 内の Copilot Chat・GitHub.com の Copilot との違い
- ✅ Claude Code との比較
- ✅ 実際に使ってみてわかった強みと弱み

:::note warn
⚠️ **現在パブリックプレビュー中です**
Copilot Business・Enterprise ユーザーはすぐ使えます。Pro / Pro+ は早期アクセス申請が必要です（2026年5月時点）。
:::

---

## GitHub Copilot App とは？

一言でいうと、「**IDE に縛られない、エージェント専用のデスクトップ Copilot**」です。

公式リポジトリの説明を引用するとこんな感じです。

> "The GitHub Copilot app is a desktop application for agent-driven development that brings parallel workstreams, GitHub integration, and PR lifecycle management into one place."

Copilot CLI をベースに作られていて、リポジトリ・ブランチ・CI パイプラインと GitHub から直接操作できます。複数のエージェントを並列で走らせながら、「自分でやるより指示する」ワークフローを想定して作られています。

![GitHub Copilot App のホーム画面。左に Sessions・Inbox・Workflows などのサイドバーが並ぶ](./Github-Copilot-Apps-Image/スクリーンショット%202026-05-24%20231725.png)

---

## インストール方法

### Step 1: 公式リポジトリにアクセス

まず GitHub の公式リポジトリ（`github/app`）にアクセスします。

🔗 https://github.com/github/app

README にインストール手順と各プラットフォーム向けのダウンロードリンクが掲載されています。

![公式リポジトリ（github/app）のREADME画面](./Github-Copilot-Apps-Image/スクリーンショット%202026-05-24%20230542.png)

### Step 2: 自分の環境に合ったファイルをダウンロード

README の Install セクションに各 OS 向けのリンクがあります。

| OS                          | 推奨           |
| --------------------------- | -------------- |
| Mac (Apple Silicon)         | ✅ 推奨        |
| Windows                     | ✅ 推奨        |
| Linux                       | ✅ 推奨        |
| Mac (Intel) / Windows (ARM) | 旧デバイス向け |

自分の OS に合ったリンクをクリックしてダウンロードします。今回は **Windows (ARM)** でやってみました。

![READMEのInstallセクション - ダウンロードリンク一覧](./Github-Copilot-Apps-Image/スクリーンショット%202026-05-24%20230559.png)

ダウンロードが完了するとこんな感じです。ファイルサイズは約 123MB でした。

![ダウンロード完了 - GitHub-Copilot-windows-arm64-setup.exe](./Github-Copilot-Apps-Image/スクリーンショット%202026-05-24%20230640.png)

### Step 3: セットアップウィザードを進める

ダウンロードした `.exe` をダブルクリックするとウィザードが起動します。

![セットアップウィザード起動 - Welcome to GitHub Copilot Setup](./Github-Copilot-Apps-Image/スクリーンショット%202026-05-24%20230709.png)

「Next >」でインストール先を選択します。デフォルトのままで問題ないです。

![インストール先選択 - Choose Install Location](./Github-Copilot-Apps-Image/スクリーンショット%202026-05-24%20230725.png)

インストールが始まります。1分もかからず終わります。

![インストール中 - プログレスバー](./Github-Copilot-Apps-Image/スクリーンショット%202026-05-24%20230731.png)

「Installation Complete」と表示されたら成功です！

![インストール完了 - Installation Complete](./Github-Copilot-Apps-Image/スクリーンショット%202026-05-24%20230822.png)

最後のページで「Run GitHub Copilot」にチェックが入っていることを確認して「Finish」をクリック。

![セットアップ完了 - Finish](./Github-Copilot-Apps-Image/スクリーンショット%202026-05-24%20230833.png)

### Step 4: GitHub アカウントでサインイン

アプリが起動すると、サインイン画面が出てきます。「Sign in to GitHub」をクリック。

![アプリ起動 - Sign in to GitHub](./Github-Copilot-Apps-Image/スクリーンショット%202026-05-24%20230944.png)

デバイス認証のコードが表示されます。このコードを GitHub.com の認証ページに入力します。コードはクリップボードに自動コピーされているので貼り付けるだけです！

![デバイス認証コード表示](./Github-Copilot-Apps-Image/スクリーンショット%202026-05-24%20231004.png)

GitHub.com でコードを入力して「Continue」をクリック。

![GitHub.com でのデバイス認証](./Github-Copilot-Apps-Image/スクリーンショット%202026-05-24%20231118.png)

組織の SSO を使っている場合は、追加の認証が入ります。「Authorize」を押せば OK です。

![SSO 認証画面](./Github-Copilot-Apps-Image/スクリーンショット%202026-05-24%20231153.png)

「Congratulations, you're all set!」と表示されれば認証完了です！

![認証完了 - you're all set!](./Github-Copilot-Apps-Image/スクリーンショット%202026-05-24%20231506.png)

### Step 5: リポジトリを接続してホームへ

アクティビティをもとに、接続するリポジトリの候補が表示されます。そのまま「Continue」で進みます。

![リポジトリ接続画面](./Github-Copilot-Apps-Image/スクリーンショット%202026-05-24%20231612.png)

テーマを選んで「Finish」でセットアップ完了！

![テーマ選択画面](./Github-Copilot-Apps-Image/スクリーンショット%202026-05-24%20231651.png)

ホーム画面が表示されます。左サイドバーに Sessions・Inbox・Workflows などが並んでいます。

![GitHub Copilot App ホーム画面](./Github-Copilot-Apps-Image/スクリーンショット%202026-05-24%20231725.png)

---

## 各 Copilot の違いを整理する

「Copilot ってもういろんな場所にあるよね」ってなってきたので、一度整理します。

### 比較表

|                           | Copilot Chat in VSCode | Copilot Chat on GitHub.com | **GitHub Copilot App** | Claude Code            |
| ------------------------- | ---------------------- | -------------------------- | ---------------------- | ---------------------- |
| **場所**                  | VSCode 内              | ブラウザ                   | デスクトップアプリ     | ターミナル / アプリ    |
| **IDE 依存**              | ✅ VSCode 必須         | ❌                         | ❌                     | ❌                     |
| **コードコンテキスト**    | 開いているファイル     | リポジトリ全体             | リポジトリ全体         | リポジトリ全体         |
| **GitHub ネイティブ連携** | 弱め                   | 普通                       | **最強**               | ❌                     |
| **PR / Issue 管理**       | ❌                     | 一部                       | **✅ 一体化**          | ❌                     |
| **並列エージェント**      | ❌                     | ❌                         | **✅**                 | ❌                     |
| **Workflow 自動化**       | ❌                     | ❌                         | **✅**                 | ❌                     |
| **対象ユーザー**          | 日常コーディング       | コードレビュー・Q&A        | エージェント駆動開発   | CLI 派・ヘビーユーザー |

![GitHub Copilot App の4つの強み：Parallel Agents・No IDE needed・Full PR Lifecycle・GitHub Native が中央のロゴを囲む円形インフォグラフィック](./Github-Copilot-Apps-Image/demo-copilot-app-strengths.png)

### Copilot Chat in VSCode との違い

VSCode 内の Copilot Chat は「今開いているファイル・プロジェクトに対して質問・指示する」のが得意です。インライン補完との組み合わせで、コーディング中に頭を使う部分を減らすのがメインの用途ですね。

一方で Copilot App は「タスクを投げて、エージェントが勝手に動く」イメージが強いです。PR を作るまでの一連の流れを自分でやらずに進められます。

![Copilot Chat in VSCode vs GitHub Copilot App の使い方の違いを示す比較図。左：開発者がタイピングしながらチャットで質問、右：開発者がリラックスしながらロボットエージェントが Issue→Code→PR→Merge を自動処理](./Github-Copilot-Apps-Image/demo-vscode-vs-app-comparison.png)

### Copilot Chat on GitHub.com との違い

GitHub.com の Copilot Chat はブラウザで使えるのが利点で、リポジトリのコードを参照しながら質問できます。でも基本は「聞いて答えてもらう」スタイルで、アクションを起こすのは自分です。

Copilot App の Inbox ではリポジトリに紐づいた Issue・PR がリアルタイムで一覧できて、そこから直接エージェントを走らせてコードを書かせることができます。

![Inbox タブに Issue と PR が一覧表示されている様子](./Github-Copilot-Apps-Image/demo-inbox.png)

### Claude Code との違い

Claude Code（Anthropic）も同じようなターミナル・CLI ベースのコーディングエージェントです。モデル単体の性能は相当強いですが、GitHub との連携は都度手作業が入る感じで、Copilot App みたいに PR や Issue が最初から見えてる状態とはちょっと違います。

Copilot App の強みは、**GitHub アカウント・リポジトリ・CI との統合が最初から完結している**ところです。PR を作って確認してマージするまでが一つのアプリで終わるのは、触ってみて初めて「あ、これか」ってなりました。

---

## 実際に使ってみた

### Quick chats でサクッと質問

ホーム画面の中央にチャット欄があって、ここから気軽に質問を投げられます。セッションをわざわざ作らなくていいので、「ちょっと聞きたいだけ」なときに地味に便利です！

![ホーム画面中央のQuick chatに質問を入力している様子](./Github-Copilot-Apps-Image/demo-home-quickchat.png)

送信すると、リポジトリのコンテキストなしでも普通に回答が返ってきます。コード片を貼り付けて「これ何してる？」とか「バグっぽい箇所ある？」みたいな雑な使い方にちょうどいいです。

![Quick chat の回答が返ってきた様子](./Github-Copilot-Apps-Image/demo-quickchat-result.png)

---

### セッションを作ってリポジトリに紐づける

本格的に使いたいときは**セッション**を作ります。左サイドバーの「+」ボタンをクリックするとセッション作成画面が開きます。

![左サイドバーの「+」ボタンからセッション作成画面を開いた様子](./Github-Copilot-Apps-Image/demo-new-session.png)

セッション作成時に対象リポジトリを選択します。ここで選んだリポジトリのコード全体がコンテキストになるので、「このファイルの〇〇を直して」という指示が通るようになります。

![セッション作成時にリポジトリを選択している画面](./Github-Copilot-Apps-Image/demo-session-repo-select.png)

---

### エージェントにタスクを投げる

セッションが開くと、チャット欄に指示を打ち込めます。ここが VSCode の Copilot Chat と一番違う点で、**コードを書くのではなく「やること」を指示する**感覚です。

たとえばこんな感じで投げると、エージェントが自分でファイルを読んで修正案を出してきます。

```
#42 の Issue を修正して、テストも追加して PR を作って
```

![エージェントへの指示を入力している様子](./Github-Copilot-Apps-Image/demo-agent-instruction.png)

指示を送るとエージェントが動き始めます。ファイルの読み込み・コードの修正・テスト実行の様子がリアルタイムで流れてくるのが見えます。

![エージェントがコードを読んで修正を進めている様子](./Github-Copilot-Apps-Image/demo-agent-running.png)

完了すると修正内容のサマリーと、そのまま PR を作るかどうかの確認が出てきます。「Create PR」を押せばそのまま GitHub 上に PR が飛びます。

![エージェントが作業完了し、PR 作成の確認が表示された様子](./Github-Copilot-Apps-Image/demo-agent-done.png)

---

### Inbox で Issue・PR をまとめて確認する

左サイドバーの「Inbox」タブを開くと、連携しているリポジトリの Issue・PR が一覧表示されます。ここから直接エージェントを起動できるので、「Issue を見てそのまま修正を指示する」流れがアプリ内で完結します。

![Inbox タブに Issue と PR が一覧表示されている様子](./Github-Copilot-Apps-Image/demo-inbox.png)

Issue の行にカーソルを乗せると「Fix with Copilot」みたいなボタンが出てきて、ワンクリックでエージェントにタスクを渡せます。

---

### Workflows で定型タスクを登録する

「Workflows」タブでは、繰り返しやる作業をテンプレート化して保存できます。「毎朝このリポジトリの未解決 Issue をまとめて」とか「PR がマージされたらリリースノートのドラフトを作って」みたいなやつです。

![Workflows タブの画面。定型タスクの一覧が表示されている](./Github-Copilot-Apps-Image/demo-workflows.png)

右上の「+」でワークフローを新規作成できます。トリガーとプロンプトを設定するだけなので、コードを書く必要はないです。

---

## 利用条件まとめ

| プラン             | 利用可否               |
| ------------------ | ---------------------- |
| Copilot Free       | ❌ 不可                |
| Copilot Pro / Pro+ | 早期アクセス申請が必要 |
| Copilot Business   | ✅ すぐ使える          |
| Copilot Enterprise | ✅ すぐ使える          |

早期アクセスの申請は公式リポジトリの README にリンクがあります。

---

## まとめ

- **GitHub Copilot App** は IDE に依存しないエージェント専用のデスクトップアプリ
- インストールはウィザード形式で5分くらいで完了する
- VSCode の Copilot Chat とは「補助ツール vs エージェントに任せる」という使い分けになる
- GitHub ネイティブ統合（PR・Issue・CI 管理）が最大の強みで、これは他のツールにはない
- 現在パブリックプレビュー中。Business/Enterprise はすぐ使える、Pro/Pro+ は申請が必要

個人的に「コードを書く」より「何を作るか・どう動かすか」に集中したいときは Copilot App が向いてると感じました。毎日のコーディングには VSCode の Copilot、大きめのタスクを丸投げしたいときは App、という使い分けが今のところしっくりきてます！

ぜひ試してみてください 🚀

---

## おわりに

はじめまして、大学2年生の Shahin（ロホマン シャヒン）です。

普段は Azure インフラや GitHub Copilot 周りをさわりながら、コミュニティ活動もしています。この記事、パブリックプレビューのアプリをとにかく触ってみた記録なので、まだ把握しきれていない部分もあると思います。

**「ここ間違ってるよ」「こういう使い方もあるよ」というのがあれば、コメントで優しく教えてもらえると本当に助かります！** 学生なりに誠実に直していきます。

記事が参考になったら **いいね・ストック・拡散** してもらえると励みになります！ X（Twitter）で感想をポストしてくれる場合は `#GhCUG` もつけてもらえると嬉しいです 🙌

---

## 📣 GitHub Copilot のコミュニティやってます

この記事を書いている Shahin は、**GitHub Copilot User Group Japan（通称：Gh-CUG / ジーカグ）** というコミュニティの運営メンバーをやっています。

Microsoft のエンジニアや MVP の方々と一緒に立ち上げたコミュニティで、GitHub Copilot をもっと広めたい・もっと使いこなしたいという人が集まっています。

:::note info
🌙 **ゆるよな Gh-CUG #01**（記念すべき第 1 回！）
📅 2026年5月26日（火）21:00〜
🖥️ オンライン開催・参加無料
👉 [申し込みはこちら（connpass）](https://gh-cug.connpass.com/event/391857/)

聴くだけ・カメラオフ・途中参加、全部 OK です！
:::

学生でも初心者でも「なんか面白そう」と思ったらぜひ！

🔗 **コミュニティページ：** https://gh-cug.connpass.com/

---

    ## 参考

    - [GitHub Copilot app 公式リポジトリ](https://github.com/github/app)
    - [GitHub Copilot app ドキュメント](https://docs.github.com/ja/copilot/github-copilot-app)
    - [GitHub Copilot User Group Japan（Gh-CUG）](https://gh-cug.connpass.com/)
