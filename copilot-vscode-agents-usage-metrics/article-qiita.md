---
title: "GitHub CopilotのUsage MetricsにVS Code Agentsウィンドウの指標が追加されたので、実際にAPIを叩いて検証してみた"
tags:
  - GitHubCopilot
  - VSCode
  - GitHub
  - API
  - 生産性向上
private: false
updated_at: ""
id: null
organization_url_name: mspjp
slide: false
ignorePublish: false
---

## はじめに

Microsoft Student Ambassador、GitHub Copilot User Group Japan（Gh-CUG）の運営として Github Copilot の最新動向をキャッチアップ/検証しているShahinです！

:::note
この記事が少しでも参考になったら、**ぜひいいね・共有**をお願いします。
間違っている箇所や「ここが分かりにくかった」という指摘は、やさしくコメントいただけると助かります！
:::

2026年9月11日、GitHub Copilot の Usage Metrics（使用状況メトリクス）に新しい項目が追加されました。

> [Add VS Code Agents to Copilot usage metrics - GitHub Changelog](https://github.blog/changelog/2026-09-11-add-vs-code-agents-to-copilot-usage-metrics/)

内容をひとことで言うと、「VS Code の **Agentsウィンドウ** をどれだけの人が、どれくらい使っているか」を Enterprise / Organization の管理者が API で追えるようになった、というアップデートです。

地味なアップデートに見えるかもしれませんが、個人的には結構気になったポイントがありました。それが「Agentsウィンドウと、エディタ内のAgent Modeは別カウントされる」という一文です。「え、分けて数えるんだ」と思ったので、実際にAPIを叩いて自分の目で確認してみることにしました。

この記事では、公式アナウンスの内容整理と、実際にAPIを検証した結果、そして「この数字は何に使えそうか」を実務目線でまとめます。

## 何が追加されたのか

まず公式アナウンスの要点を整理します。Copilot usage metrics API のレポートに、以下のフィールドが新しく追加されました。

### Enterprise / Organization の集計レポート（1日単位・28日単位）

| フィールド                        | 内容                                                                                |
| --------------------------------- | ----------------------------------------------------------------------------------- |
| `daily_active_vscode_agent_users` | その日にVS Code Agentsウィンドウを使った、ユニークユーザー数                        |
| `totals_by_vscode_agent`          | `session_count`（セッション数）と `total_user_messages`（送信メッセージ数）の集計値 |

### ユーザー単位のレポート（1日単位・28日単位）

| フィールド               | 内容                                                                         |
| ------------------------ | ---------------------------------------------------------------------------- |
| `used_vscode_agent`      | そのユーザーがその日にVS Code Agentsウィンドウを使ったかどうか（true/false） |
| `totals_by_vscode_agent` | ユーザーごとの `session_count` と `total_user_messages`                      |

どちらもオプションフィールド扱いで、該当データがない場合は `null` または項目自体が存在しない形になります。既存のレポート構造を壊さない後方互換の追加、というのがGitHub側のスタンスです。

## 「VS Code Agentsウィンドウ」と「エディタ内のAgent Mode」は別物として数えられる

今回のアップデートで一番押さえておきたいのがここです。公式の Important notes にはこう書かれています。

> These metrics cover the dedicated VS Code Agents window only. They remain separate from editor-window Agent Mode and generic usage rollups.

日本語にすると「これらの指標は専用のVS Code Agentsウィンドウのみを対象とし、エディタ内のAgent Modeや汎用の集計とは別カウントである」という意味です。

普段VS Codeを使っていると、Agent Modeというと「チャットパネルでモデルを選んでコードを書かせるやつ」を思い浮かべる人が多いと思います。ただ、VS Code側のドキュメントを見ると、それとは別に **Agentsウィンドウ（Preview）** という独立したインターフェースが存在します。

> [Ways to work with agents - Build with agents in VS Code](https://code.visualstudio.com/docs/agents/overview#_ways-to-work-with-agents)

Agent Windowは次のような画面です（検証時のキャプチャ）。

![VS CodeのAgentsウィンドウの画面例。ここでセッションを一覧し、作業を切り替えて管理できる](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/copilot-vscode-agents-usage-metrics/image.png)

Agentsウィンドウは、プロジェクトを横断して複数のエージェントセッションを管理したり、SSHやdev tunnel越しに別マシンのセッションを操作したりするための専用UIです。エディタの中で完結するチャットビュー（Chat view）とは役割が違っていて、「複数の作業を並行して走らせたい」「別デバイスからセッションを続けたい」ときに使う画面、という位置づけになっています。

今回追加された指標は、Copilot全体の利用状況ではなく、**この専用ウィンドウをどれだけ使っているか**にピンポイントで絞ったものです。Agent Mode全体の利用率を知りたい場合は、既存の `used_agent` や `monthly_active_agent_users` を見る必要があり、今回の指標だけでは代用できません。この切り分けを理解しないまま数字だけ見ると、「Agent利用率が低い」と誤解しかねないので注意が必要です。

## 実際にAPIを叩いて検証してみた

ここまでは公式アナウンスの要約ですが、せっかくなので自分でも動かして確認してみました。

### 検証環境

自分がインターンをしているOrganizationに対して、`gh` CLI経由のトークンで実際にAPIを叩いてみます。

```bash
# トークンのスコープ確認（read:org を含む）
gh auth status
```

```
✓ Logged in to github.com account srohoman-bot
- Token scopes: 'gist', 'read:org', 'repo', 'workflow'
```

![gh auth status の実行結果。srohoman-botアカウントでログイン済み、read:orgスコープを保持している状態](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/copilot-vscode-agents-usage-metrics/images/01-gh-auth-status.png)

再現性のため、以降のリクエストでは `X-GitHub-Api-Version: 2026-03-10` を明示します。

### 検証①: 未認証でのリクエスト

まずは認証なしでどう返ってくるか確認します。

```bash
curl -s -o /dev/null -w "HTTP %{http_code}\n" \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2026-03-10" \
  https://api.github.com/orgs/YJK-Inc/copilot/metrics/reports/organization-1-day
```

```
HTTP 401
```

![未認証でAPIを叩いた結果、HTTP 401が返ってきたターミナル画面](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/copilot-vscode-agents-usage-metrics/images/02-unauthenticated-401.png)

これは想定通りですね。認証なしでは弾かれます。

### 検証②: 認証ありでのリクエスト

次に、`read:org` スコープ付きのトークンで同じエンドポイントを叩いてみます。

```bash
curl -s -D - -o response.json \
  -H "Authorization: Bearer $(gh auth token)" \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2026-03-10" \
  "https://api.github.com/orgs/YJK-Inc/copilot/metrics/reports/organization-1-day?day=2026-09-13"

cat response.json
```

返ってきたのはこちらです。

```json
{
  "message": "The 'Copilot usage metrics' policy must be enabled to use this API",
  "documentation_url": "https://docs.github.com/copilot/concepts/copilot-metrics#organization-level-metrics",
  "status": "403"
}
```

![認証ありでAPIを叩いた結果。403とCopilot usage metricsポリシーが無効という理由が返ってきたターミナル画面](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/copilot-vscode-agents-usage-metrics/images/03-authenticated-403-policy-disabled.png)

`403 Forbidden`。理由は「Copilot usage metricsポリシーが有効になっていない」でした。

これ、実際に自分の手で403を引いてみて初めて実感したんですが、公式アナウンスに書かれていた「Access is available to enterprise owners and billing managers, organization owners, and anyone with a custom organization or enterprise role granting `View Copilot Metrics`. The Copilot usage metrics policy must be enabled.」という一文は、単なる注意書きではなくて**実際に叩くとそのままの文言でブロックされる**、というところまで確認できました。

### 検証③: Enterprise側でポリシーを実際に有効化してみる

ここで終わっても良かったんですが、自分がインターンをしているEnterprise ownerの権限を持つ環境だったので、実際にポリシーを有効化するところまで踏み込んでみました。

「Copilot usage metrics」ポリシーは、Organizationの設定画面ではなく **Enterprise側の「AI Controls」→「Copilot」** の中にあります。

![Enterprise の AI Controls > Copilot 画面。左下にhttps://github.com/enterprises/YJK-Incと表示されており、Organization設定ではなくEnterprise設定であることがわかる](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/copilot-vscode-agents-usage-metrics/images/04-enterprise-ai-controls-copilot.png)

ページ下部の「Billing & usage」セクションまでスクロールすると、`Copilot metrics API`（旧来の基本メトリクスAPI）とは別に `Copilot usage metrics` という項目があります。ここが今回の403の原因で、`Select a policy` のまま何も選ばれていない状態でした。

![Billing & usageセクション。Copilot metrics APIはEnabled everywhereだが、Copilot usage metricsはSelect a policyのまま未設定になっている](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/copilot-vscode-agents-usage-metrics/images/05-billing-usage-select-a-policy.png)

ドロップダウンを開くと `Enabled everywhere` と `Disabled everywhere` の2択が出てくるので、`Enabled everywhere` を選択します。

![ドロップダウンでEnabled everywhereを選択している画面。組織・Enterprise配下の全ユーザーがこの機能にアクセスできるようになる、という説明が表示されている](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/copilot-vscode-agents-usage-metrics/images/06-enable-policy-dropdown.png)

ポリシーを有効化したあと、**同じトークン・同じコマンドで**もう一度APIを叩き直してみました。

```bash
curl -s -D - -o response.json \
  -H "Authorization: Bearer $(gh auth token)" \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2026-03-10" \
  "https://api.github.com/orgs/YJK-Inc/copilot/metrics/reports/organization-1-day?day=$(date -u +%F)"

cat response.json
```

```
HTTP/2 204
```

![ポリシー有効化後に同じコマンドを再実行した結果。ステータスが403から204に変わっている](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/copilot-vscode-agents-usage-metrics/images/07-after-enable-204.png)

`403` から `204 No Content` に変わりました。トークンやスコープは何も変えていないので、**今回の環境ではEnterprise側のポリシー有効化が効いている**ことを確認できました。`204` は「アクセス自体は許可されたが、その日のレポートがまだ生成されていない、または返せるデータがない」状態を示します。

### 検証④: 一晩置いてから再実行し、実際にレポートを取得する

`204`のまま記事を書き進めていたんですが、翌日になってから同じリクエストをもう一度叩き直したところ、**今回の環境では**`200`が返ってきました。

```bash
curl -s -D - -o response.json \
  -H "Authorization: Bearer $(gh auth token)" \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2026-03-10" \
  "https://api.github.com/orgs/YJK-Inc/copilot/metrics/reports/organization-1-day?day=2026-09-12"

cat response.json
```

```json
{
  "download_links": [
    "https://copilot-reports.github.com/organization-1-day-report/...(署名付きURL、有効期限付き)..."
  ],
  "report_day": "2026-09-12"
}
```

![翌日に同じコマンドを再実行した結果。HTTP/2 200とdownload_linksを含むJSONが返ってきている（etag・x-oauth-client-id・x-github-request-id・署名付きURLの一部はマスキ済み）](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/copilot-vscode-agents-usage-metrics/images/08-report-200-download-links.png)

`download_links`には署名付きURLが入っていて、ここを直接`curl`で叩くと実際のNDJSONレポートがダウンロードできます。

```bash
curl -s "$(python3 -c "import json;print(json.load(open('response.json'))['download_links'][0])")" | python3 -m json.tool
```

`organization-1-day` のように1オブジェクトが返るケースではこの方法で見やすく整形できます。`users-1-day` など複数行のNDJSONを扱う場合は、次のように `jq` で1行ずつ処理すると安定して確認できます。

```bash
SIGNED_URL=$(python3 -c "import json;print(json.load(open('response.json'))['download_links'][0])")
curl -s "$SIGNED_URL" | jq -c .
```

返ってきた実データの一部がこちらです。

```json
{
  "day": "2026-09-12",
  "organization_id": "277658765",
  "enterprise_id": "612428",
  "daily_active_users": 0,
  "weekly_active_users": 4,
  "monthly_active_users": 6,
  "monthly_active_agent_users": 5,
  "monthly_active_chat_users": 5,
  "totals_by_ide": [],
  "totals_by_feature": []
}
```

![実際のNDJSONレポートの内容。daily_active_usersやmonthly_active_agent_usersなどの既存フィールドは並んでいるが、vscode_agent系のフィールドはどこにも見当たらない](https://raw.githubusercontent.com/shahin99991/Qiita-github/main/copilot-vscode-agents-usage-metrics/images/09-report-actual-data.png)

ここで正直に書いておきたいのですが、**この実データには`daily_active_vscode_agent_users`も`totals_by_vscode_agent`も一切含まれていませんでした**（レポート全文を`grep vscode`しても1件もヒットしません）。理由ははっきりしていて、検証に使ったOrganizationで実際にVS Code Agentsウィンドウを使った人が誰もいなかったからです。

これは検証の失敗ではなく、むしろ公式アナウンスにあった「オプションフィールドで、該当データがない場合は項目自体が存在しない」という仕様を実データで確認できた、という収穫でした。`monthly_active_agent_users`（既存のagent関連アクティブユーザー指標として5の値が入っている）は存在する一方で、`vscode_agent`系のフィールドだけ丸ごと欠落している——この対比がそのまま「別カウントで管理されていて、未使用なら省略される」という設計を裏付けています。

### 検証でわかったこと・わからなかったこと

正直ベースで、今回の検証の到達点をまとめます。

- ✅ 未認証・権限不足のときのエラーレスポンスを実際に確認できた（`401`）
- ✅ ポリシー未設定だと `403` で明確に理由が返ってくることを確認できた
- ✅ Enterprise側で「Copilot usage metrics」ポリシーを実際に有効化し、同じリクエストが `403` → `204` → `200` と変化することを確認できた
- ✅ 実際のNDJSONレポートを取得し、`monthly_active_agent_users`（値あり）と`vscode_agent`系フィールド（丸ごと欠落）を比較して、「未使用時は項目自体が省略される」というオプションフィールドの挙動を確認できた
- ❌ 実際にVS Code Agentsウィンドウを使った状態でのレポート（`daily_active_vscode_agent_users`に値が入っている状態）はまだ確認できていない。検証対象のOrganizationにAgentsウィンドウの利用実績がなかったため

### 参考: フィールドに値が入るとどんな形になるか（イメージ）

実データでは`vscode_agent`系フィールドが欠落することまでは確認できましたが、実際に値が入った状態はまだ手元で再現できていません。公式ドキュメントの [Example schema for Copilot usage metrics](https://docs.github.com/en/copilot/reference/copilot-usage-metrics/example-schema) にも、まだ今回追加された `vscode_agent` 関連フィールドを含む例が載っていませんでした（記事執筆時点）。なので、以下はあくまで**アナウンス文面から組み立てた構造イメージ**として見てください。

```json
{
  "daily_active_users": 42,
  "daily_active_vscode_agent_users": 6,
  "totals_by_vscode_agent": {
    "session_count": 11,
    "total_user_messages": 58
  }
}
```

ユーザー単位のレポートだと、こういう形になるはずです。

```json
{
  "user_id": 1,
  "user_login": "example-user",
  "used_vscode_agent": true,
  "totals_by_vscode_agent": {
    "session_count": 3,
    "total_user_messages": 14
  }
}
```

## この指標が使えそうな場面

管理者目線で考えると、この指標は以下のような場面で使えそうです。

- **Agentsウィンドウの導入効果を個別に見たい**: Agent Mode全体の数字は伸びているけど、「新しく入ったAgentsウィンドウ機能自体がどれだけ使われているか」は別で切り出して見たい、というケースに直接答えられます
- **プレビュー機能の展開判断**: Preview段階の機能なので、社内展開を広げる前に「実際どのくらいのメンバーが触っているか」を`daily_active_vscode_agent_users`で見てから判断する、という使い方ができます
- **セッション数とメッセージ数から使い方の濃さを見る**: `session_count`と`total_user_messages`を組み合わせると、「セッションは開いているけどメッセージはあまり送っていない」ユーザーと「がっつり使い込んでいる」ユーザーの差が見えてきます

Gh-CUGのようなコミュニティ運営の立場だと、こういう「新機能の実利用データ」はイベントのネタとしても使いやすい部分です。今後、参加者の会社でこの指標を実際に使ってみた話が聞けたら面白そうだなと思っています。

## 注意点まとめ

公式アナウンスのImportant notesを、実務で気をつけたいポイントとして整理しておきます。

:::note warn

- Agentsウィンドウの指標は、エディタ内のAgent Modeや他の汎用集計とは**別カウント**。Agent Mode全体の利用率と混同しないこと
- データがない場合は項目が`null`または欠落する。既存のレポートパース処理を壊さない設計だが、null許容の実装にしておく必要がある
- APIを叩くには、Enterprise owner / billing manager、Organization owner、または`View Copilot Metrics`権限を持つカスタムロールが必要
- 加えて「Copilot usage metrics」ポリシーは、**Enterprise配下Organizationのケースでは Enterprise 側の「AI Controls」→「Copilot」→「Billing & usage」**で設定する。Enabledにしないと、権限があっても`403`で弾かれる（実際に検証で確認済み）
- ポリシーを有効化した直後は、その日のレポートがまだ生成されておらず`204 No Content`が返ることがある（今回の検証でも実際にこの状態を経由した。今回の環境では翌日に`200`へ変化したが、反映タイミングは前後する可能性がある）
  :::

## まとめ

今回のアップデートは、Copilot全体の話ではなく「VS CodeのAgentsウィンドウ」という一つの機能にピンポイントで絞った指標追加でした。地味な変更に見えて、実際にAPIを叩いてみると「エディタ内Agent Modeとは別カウント」という設計判断がちゃんとエラーメッセージやレスポンスの中身に反映されていて、確認しがいがありました。

個人的に一番良かったのは、`401` → `403` → ポリシー有効化 → `204` → `200`（今回の環境では翌日に変化）という流れを自分の手で全部再現できたことです。しかも`200`で返ってきた実データには`vscode_agent`系フィールドが丸ごと欠落していて、「未使用なら項目自体が省略される」という仕様まで実際に確認できました。ドキュメントを読むだけだと「権限がいる」「ポリシーが必要」で終わってしまうところを、挙動が変わる瞬間まで一通り追えたのは、検証してよかったポイントでした。

Enterprise / Organization管理者の方は、`daily_active_vscode_agent_users`や`used_vscode_agent`をダッシュボードの他の指標と組み合わせて、Agentsウィンドウの実際の浸透度を追いかけてみると新しい発見があるかもしれません。

またGitthub Copilotのアップデートが来たら検証して記事にします！お楽しみに＞＜

## 📣 GitHub Copilot User Group Japan（Gh-CUG）のお知らせ

ここまで読んでくれた方へ、ちょっとだけ宣伝させてください！

私が運営に参加している **GitHub Copilot User Group Japan（Gh-CUG / ジーカグ）** は、「もっと世の中に GitHub Copilot を広げたい！」という思いから生まれたユーザーコミュニティです。

モットーは **「なんでもは知らない、しってることだけ」**。完璧な知見もすごい実績もいりません。「こんなんできた！」「ここでつまずいた！」を持ち寄って、みんなでゆるく楽しく学ぶ場です。学生・初心者・ノンデベロッパーの方も大歓迎です！

| シリーズ           | スタイル         | 雰囲気                   |
| ------------------ | ---------------- | ------------------------ |
| 🌙 ゆるよな Gh-CUG | オンライン（夜） | ゆるふわ。ふらっと参加OK |
| 🔥 Gh-CUG Night    | オンライン       | 実践的な知見をがっつり   |
| 🤝 Gh-CUG Meetup   | オフライン       | リアルでワイワイ交流     |

今回のような「公式アップデートを実際に検証してみた」系の話や、Copilot Metrics周りの運用Tipsもコミュニティでよく話題にしているので、気になった方はぜひ覗いてみてください！

🔗 **Connpass グループページ：** [GitHub Copilot User Group Japan](https://gh-cug.connpass.com/)

## 参考

- [Add VS Code Agents to Copilot usage metrics - GitHub Changelog](https://github.blog/changelog/2026-09-11-add-vs-code-agents-to-copilot-usage-metrics/)
- [REST API endpoints for Copilot usage metrics](https://docs.github.com/en/rest/copilot/copilot-usage-metrics)
- [Data available in Copilot usage metrics](https://docs.github.com/en/copilot/reference/copilot-usage-metrics/copilot-usage-metrics)
- [Example schema for Copilot usage metrics](https://docs.github.com/en/copilot/reference/copilot-usage-metrics/example-schema)
- [Build with agents in VS Code](https://code.visualstudio.com/docs/agents/overview)
- [Use chat in VS Code](https://code.visualstudio.com/docs/chat/chat-overview)
