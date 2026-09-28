---
title: "Teams の GitHub Copilot が「コンテキストを読む」ようになったので、全部試してみた【2026年9月アプデ】"
tags:
  - GitHubCopilot
  - MicrosoftTeams
  - Slack
  - GitHub
  - AI
---

<!--
【タイトル候補】
1. Teams の GitHub Copilot が「コンテキストを読む」ようになったので、全部試してみた【2026年9月アプデ】
2. 【実況18枚】Teams の GitHub Copilot でエラー修正・Issue作成・モデル切り替えまで全部やってみた
3. GitHub Copilot in Teams/Slack 9月25日アプデを実機検証。リポジトリ切り替えのハプニングも乗り越えた話

【画像について】
この記事のスクリーンショット18枚はすべて実機検証の実画像（2026-09-28 撮影）。
`copilot-teams-slack-updates/Images/img-XX-*.png` として push 済み。詳細は `demo-procedure.md` を参照。
-->

## はじめに

GitHub Copilot のアップデートを追いかけるのが完全に日課になっているGH-CUG運営兼、マイクロソフト学生アンバサダーのShahinです！

:::note
～この記事にいいねを押した人に幸あれ～
※発言は個人の見解です
本記事はdocumentベースに検証したものです、もっとこんな活用の仕方があるよ！私はこう使っているなどの意見がありましたら、是非コメント欄で教えてください＞＜
:::

2026年9月25日、**GitHub Copilot の Slack / Microsoft Teams 連携に激アツのアップデート**が降ってきました！

> [Updates to GitHub Copilot for Slack and Microsoft Teams](https://github.blog/changelog/2026-09-25-updates-to-github-copilot-for-slack-and-microsoft-teams/)

このアップデート、何がそんなに熱いのか。一言で言うと――

**「チャットに転がっているコンテキストを、GitHubCopilot がちゃんと読むようになった」**

これに尽きます！

- 📷 Teams に貼った**画像**を読む
- 🔁 **転送されたメッセージ**の中身まで読む
- 🧵 **チャネルやスレッドの履歴**を保持する
- 🧠 セッション内で**モデルを切り替え**られる

「メンションしたらエージェントが動く」だけでも十分すごかったのに、そこに「目」と「記憶」が追加された感じです。

……というわけで、今回は**検証用リポジトリを用意して Teams から実際に全部試してきました**！ スクリーンショット全18枚で実況します。リポジトリ設定のハプニング（後述）もあったんですが、それすら Copilot が上手く捌いてくれたのが最高だったので、そのまま全部載せます！

---

## 前提：Teams/Slack の GitHub Copilot って何ができるんだっけ

まず土台のおさらいです。2026年8月21日に、**「Shared agentic work with GitHub Copilot in Microsoft Teams」**がパブリックプレビューとして公開されました。

> [Shared agentic work with GitHub Copilot in Microsoft Teams](https://github.blog/changelog/2026-08-21-shared-agentic-work-with-github-copilot-in-microsoft-teams/)

これが何なのかというと、**Teams のチャネルやスレッド、DM で `@GitHub` とメンションするだけで、Copilot クラウドエージェントのセッションが始まる**というやつです。

ここがすごいポイント：

- 会話に参加している**全員**がエージェントの調査・作業を見られる
- 誰かが質問を足したり、コンテキストを追加したり、作業の舵取りができる
- リポジトリへの書き込み権限を持つ人なら、実際の変更作業まで指示できる
- 作業は**セキュアなクラウドサンドボックス**で非同期に進行する

しかも、Teams で始めたタスクはあとから**ターミナル・GitHub Copilot アプリ・IDE など好きな場所で続きを触れる**という、サーフェス横断の仕様になっています。

会議中に出たアクションアイテムを、その場で `@GitHub` に投げて「会議が終わる頃には調査が終わってる」みたいな世界観。夢がありますよね！

---

## 9月25日アップデートの要点まとめ

で、今回のアップデートです。ざっくり表にするとこんな感じ。

| カテゴリ            | 内容                                                                                           |
| ------------------- | ---------------------------------------------------------------------------------------------- |
| 🧠 コンテキスト強化 | Slack のファイル・添付・メッセージリンクをコンテキストに利用可能に                             |
| 🧠 コンテキスト強化 | Teams で**インライン画像**・**転送メッセージ**・**チャネル/スレッド履歴**を読めるように        |
| 🎛️ コントロール強化 | 次のメッセージから**モデルを切り替え**可能に。その選択は会話中ずっと維持される                 |
| 🎛️ コントロール強化 | Slack でもデフォルトのオーナー・リポジトリを設定可能に（Teams はセットアップ時に設定する仕様） |
| 🔗 作業との紐付け   | Issue 作成前に**類似 Issue をチェック**。成果物への直接リンクと元スレッドへのリンクを保持      |
| 🛠️ 信頼性向上       | 長時間タスクの進捗表示、中断・再接続の改善、Teams での重複回答の抑制など                       |

この中でも、私が**ぶち上がったのが「コンテキスト強化」**です。ここを深掘りします！

---

## 【実況】Teams で実際に全部試してみた

ここからは実機検証です。検証用リポジトリとして `YJK-Inc/Test-Repo` を用意しました。中身は Python の在庫管理スクリプト（`app/main.py`）で、**デモ用にわざと `ZeroDivisionError` が出るバグを仕込んであります**。

### セットアップ：アカウント連携は数クリックで終わる

Teams のチャネルで `@GitHub` とメンションすると、まずアカウント連携を促されます。このメッセージは**自分にだけ表示される**タイプなので、チャネルのメンバーには見えません。

![Teams 上で GitHub アカウント連携を促される](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/copilot-teams-slack-updates/Images/img-01-connect-prompt.png)

ボタンを押すとブラウザで連携画面が開きます。

![GitHub と Teams のアカウント連携画面](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/copilot-teams-slack-updates/Images/img-02-connect-accounts.png)

![GitHub Connector for Teams の認可画面](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/copilot-teams-slack-updates/Images/img-03-authorize-connector.png)

連携が終わると、Teams 上にできることのガイドカードが出ます。`@Github signin` / `signout` / `settings` といったコマンドや、プロンプト例が一覧で見えるのは親切でした！

![連携後に表示される機能ガイドカード](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/copilot-teams-slack-updates/Images/img-04-guide-card.png)

### デフォルトリポジトリを Test-Repo に切り替える

次に `@GitHub settings` でこのチャネルのデフォルトリポジトリを設定します。ここで通知に注目。

> The repository changed from **YJK-Inc/Foundry-** to **YJK-Inc/Test-Repo**.

![デフォルトリポジトリの変更通知](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/copilot-teams-slack-updates/Images/img-05-repo-changed.png)

そう、**以前の会話で別リポジトリ（Foundry-）を選択した名残**が残っていたんです。チャネルのデフォルトは Test-Repo に変わった――これが後で効いてきます（伏線です）。

### デモ① README を最新の構成に更新してもらう

まずは軽いタスクから。「**README を最新の構成に更新して**」とだけ投げました。

![README 更新タスクを依頼するとタスク分解が始まる](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/copilot-teams-slack-updates/Images/img-06-readme-start.png)

すぐにタスクが分解されて進捗バーが出ます（「リポジトリの現状構成を確認」→「既存 README の確認」→「更新」→「コミット・プッシュ」の 0/4）。右上にモデル名のバッジ（この時点では `gpt-5.6-sol`）が出ているのも分かりやすいですね。

しばらくすると完了報告。4/4 done です。

![README 更新が完了し PR が作られた報告](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/copilot-teams-slack-updates/Images/img-07-readme-complete.png)

「もともと README.md は存在しなかったため新規作成という形になっています」という補足まで添えてくれるの、地味に誠実で良いです。

GitHub 側で PR を見てみると、説明文に **「Created from a Microsoft Teams conversation.」** と明記されていました。会話 → PR のトレーサビリティがちゃんと確保されてます！

![Teams の会話から作られた PR #2（README 更新）](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/copilot-teams-slack-updates/Images/img-08-readme-pr.png)

### デモ② エラーを直してもらう（ここでハプニング発生）

本番です。`app/main.py` の在庫 0 バグを直させます。トレースバックをスレッドに貼って「**このエラー直して**」。

![ZeroDivisionError のトレースバックを貼って修正依頼](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/copilot-teams-slack-updates/Images/img-09-error-prompt.png)

すると Copilot から返ってきたのが、予想外の回答でした。

![リポジトリの不一致を検出して選択肢を提示する Copilot](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/copilot-teams-slack-updates/Images/img-10-repo-mismatch.png)

要約すると、

1. トレースバック自体は正確に解析済み（`app/main.py` の `calculate_total_price` で `quantity == 0` のときに `100 / quantity` が走っている、と行レベルで特定）
2. **ただしこのスレッドは古い方のリポジトリ（Foundry-）に接続されたまま**で、該当ファイルが見つからない
3. 「チャンネルのデフォルトは Test-Repo に変わっているようですが、このスレッドは Foundry- のままです」と状況まで説明した上で、**「このスレッドを Test-Repo に切り替えて修正する」か「Foundry- のまま進めるか」の選択肢**を提示してくれた

これ、さっきのデフォルトリポジトリ変更の伏線回収です。**スレッド単位でリポジトリが紐づく**仕様なので、古いスレッドは前のリポジトリを見たままだったわけですね。勝手に見当違いのリポジトリを探しに行かず、状況を説明して確認を取ってくるの、かなり賢くないですか!?

「切り替えて」と返すと、即座にリポジトリを切り替えて修正まで完走しました。

![リポジトリ切り替え後に修正が完了し PR #1 が作られた](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/copilot-teams-slack-updates/Images/img-11-fix-complete.png)

報告内容も「原因」「修正内容（条件反転・`round()` 追加・古いコメント整理）」「動作確認（`python app/main.py` で税込み合計 0 円を確認）」までフルセット。GitHub 側の PR もこのとおりです。

![Teams から作られた修正 PR #1 の詳細](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/copilot-teams-slack-updates/Images/img-12-fix-pr.png)

:::note warn
⚠️ **正直レポート**: このデモでは画像添付も試したんですが、「**I couldn't read these images. Try attaching them again.**」と読み取りに失敗しました（上のスクショにも通知が写っています）。テキストのトレースバックは一発で解析できたので実害はなかったですが、インライン画像の解析は**段階ロールアウト中**とのことなので、環境によってはまだ不安定なのかもしれません。皆さんの環境ではぜひ画像でも試してみてほしいです！
:::

### デモ③ 転送した要件メッセージから Issue を立ててもらう

次はコンテキスト読解の本領発揮です。「在庫 0 の商品でもエラーにならないようにしてほしい」「税込み金額は整数で表示したい」という**要件のやり取りを転送・引用した上で**、「この内容を踏まえて Issue を立てて」と依頼。

![転送した要件を踏まえて Issue #2 が作成された](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/copilot-teams-slack-updates/Images/img-13-issue-created.png)

返ってきたのは「Issue を作成しました ✅（重複する既存 Issue はありませんでした）」の報告。さらに「**これらは既に PR #1 で修正済みであることも Issue 本文に記載しています**」とのこと。前のデモの修正と今回の要件を頭の中で繋げてくれてる……！

![作成された Issue #2 の詳細（内容・背景・対応の3段構成）](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/copilot-teams-slack-updates/Images/img-14-issue-detail.png)

Issue 本文は「内容 → 背景（`quantity == 0` で `ZeroDivisionError`、金額が float のまま）→ 対応（PR #1 で修正済み）」の3段構成。エンジニアが読んでそのまま判断できる粒度でした。

### デモ④ モデルを切り替えてみる

ここでお待ちかね、**セッション内モデル切り替え**です。「今使っているモデルは？ Change可能なモデル一覧も出して」と聞くと、自分にだけ見えるモデル選択プロンプトが出ました。

![モデル一覧を要求すると選択プロンプトが表示される](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/copilot-teams-slack-updates/Images/img-15-model-select.png)

一覧を開いたら、思った以上のラインナップでした！

![選択可能なモデル一覧（Auto / Claude / GPT / MAI / Kimi など）](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/copilot-teams-slack-updates/Images/img-16-model-list.png)

`Auto` を筆頭に、Claude 系（Sonnet 5 / Opus 4.8 / Haiku 4.5）、GPT 系（5.5 / 5.4 mini / 5.3-Codex / 5 mini）、そして **`MAI-Code-1.1-Flash`** や `Kimi K3` まで。マルチベンダーの模型店と化しています。今回は `MAI-Code-1.1-Flash` に切り替えてみます。

### デモ⑤ わざと重複する Issue を頼んでみる（切り替えたモデル、生きてる？）

最後の検証です。さっき作った Issue #2 と**ほぼ同じ内容**の Issue をあえて依頼します。「『在庫 0 でエラーになる不具合』の Issue を作成して」。

![重複 Issue を検出して新規作成を止めた（モデルは MAI-Code-1.1-Flash）](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/copilot-teams-slack-updates/Images/img-17-duplicate-issue.png)

Copilot の回答は「**同内容の Issue はすでに作成済みです。重複を避けるため、新規作成はせず既存の Issue を使ってください**」。類似 Issue チェック、本当に効いてました！

そしてここ、注目ポイントなんですが――**右下のモデルバッジが `MAI-Code-1.1-Flash` に変わっている**んです。さっき切り替えたモデルが、会話の後半でもちゃんと維持されている。changelog の「switch models for the next message and **keep that choice throughout the conversation**」が、スクショ上で確認できた瞬間でした！

![Issue #2 ページ全体。Assign to Agent ボタンも確認できる](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/copilot-teams-slack-updates/Images/img-18-issue-final.png)

ついでに Issue ページのサイドバーには「**Assign to Agent**」ボタンもあって、GitHub 側からもエージェントに仕事を振れる動線ができているのを確認しました。

---

## 今回のアップデート、触ってみた感想まとめ

実際に全部試した上で、9月25日アップデートの体感を整理します。

- **コンテキスト読解は本物**。トレースバックの行特定、転送要件からの Issue 化、スレッドの会話履歴を踏まえた補足（「PR #1 で修正済みです」）まで、会話の中の情報をちゃんと拾って動く
- **リポジトリ不一致の検出と対話での切り替え**が想像以上に賢かった。9/25 アプデの「信頼性改善」が効いている場面を実体験できた
- **モデル切り替えは会話中ずっと維持**される。バッジ表示で今どのモデルか分かるのも安心感がある
- **画像添付の読み取りだけ、今回は失敗**した。ロールアウト中の機能なので今後に期待

---

## 始め方（Microsoft Teams の場合）

導入手順はシンプルです。

1. 管理者が **Copilot cloud agent ポリシー**と**クラウドサンドボックス**を有効化する
2. [GitHub app for Microsoft Teams](https://teams.microsoft.com/l/app/836ecc9e-6dca-4696-a2e9-15e252cd3f31) をインストール（またはアップグレード）する
3. Teams で `@GitHub` とメンションして、案内に従い GitHub アカウントを連携する
4. パブリックチャネルの場合は、案内が出たら**デフォルトリポジトリ**を設定する（DM では不要）
5. `@GitHub` に続けてタスクを書いて送信！（`@GitHub help` で利用可能なコマンドも確認できる）

Slack の場合もほぼ同じで、管理者によるポリシー有効化 → GitHub app for Slack のインストール/アップグレード → アカウント連携 → `@GitHub` メンション、という流れです。

:::note warn
⚠️ **注意**: パブリックプレビューは **GitHub Copilot Business / Enterprise プランの組織**が対象です。機能によっては段階的ロールアウト中のため、まだ自分のワークスペースで使えないものもある点にご注意ください。
:::

---

## 気になる料金まわり

せっかちな人（私含む）が真っ先に気にするコスト面も整理しておきます。

- Teams/Slack から起動したクラウドエージェントの利用は、**既存の Copilot 利用枠（AI クレジット）を消費**します
- 組織の場合、AI クレジットの消費は**従量課金の予算（usage-based billing budgets）**で管理できます
- **クラウドサンドボックスの利用は別途課金**で、プロダクト単位/SKU 単位の予算で制御できます

要するに「Teams から気軽に呼べるようになった分、使いすぎ注意」ではあるんですが、既存の予算管理の仕組みに乗るので、運用でカバーできる範囲だと思います！

ちなみにガバナンス面では、**Teams 連携経由で作られた PR に追加の承認を必須にする**設定も用意されています（例：2人承認のリポジトリなら3人必要になる）。スピードとコンプラのバランスを取れるのはエンプラ利用だと重要ですね。

---

## まとめ

今回は9月25日アップデートを受けて、Teams から GitHub Copilot クラウドエージェントを**実際に動かしまくって**きました。

- **README 更新・バグ修正 PR・Issue 作成**まで、Teams の会話から全部完結した
- **リポジトリ設定のハプニング**（古いスレッドが前のリポジトリを見たままだった問題）も、Copilot が状況を説明して対話で切り替えられて感動した
- **モデル切り替えは会話中維持**されることを、バッジ表示（`MAI-Code-1.1-Flash`）で確認できた
- **重複 Issue の自動検出**も本当に効いた。重複乱立防止になる
- 画像添付の解析だけ今回は読み取り失敗。ロールアウト中とのことなので今後に期待

「**メンションしたら動くエージェント**」に「**目と記憶**」が実装されつつあるのを、実機で体感できた検証でした。チャットから Issue・PR へのトレーサビリティ（`Created from a Microsoft Teams conversation`）が自動で残るのも、チーム開発だとかなり効くはずです。

チャットに貼いたトレースバックから修正 PR が生える世界線、ぜひみなさんも体感してみてください！

---

## 参考

- [Updates to GitHub Copilot for Slack and Microsoft Teams - The GitHub Blog](https://github.blog/changelog/2026-09-25-updates-to-github-copilot-for-slack-and-microsoft-teams/)（2026年9月25日）
- [Shared agentic work with GitHub Copilot in Microsoft Teams - The GitHub Blog](https://github.blog/changelog/2026-08-21-shared-agentic-work-with-github-copilot-in-microsoft-teams/)（2026年8月21日）
- [Integrating GitHub Copilot cloud agent with Microsoft Teams - GitHub Docs](https://docs.github.com/copilot/how-tos/copilot-integrations/integrate-cloud-agent-with-teams)
- [Using Copilot coding agent with Slack - GitHub Docs](https://docs.github.com/copilot/how-tos/use-copilot-agents/coding-agent/integrate-coding-agent-with-slack)
- [About cloud and local sandboxes - GitHub Docs](https://docs.github.com/copilot/concepts/about-cloud-and-local-sandboxes#cloud-sandboxing)
