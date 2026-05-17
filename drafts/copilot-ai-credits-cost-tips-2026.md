---
title: "【2026年6月〜】GitHub Copilot が重量課金制に変わる。AI クレジット時代のコスト節約術まとめ"
tags:
  - GitHubCopilot
  - VSCode
  - 生産性向上
  - AI
  - GitHub
private: false
updated_at: ""
id: null
organization_url_name: null
slide: false
ignorePublish: false
---

## はじめに

「え、Copilot の課金体系が変わるの？」

GitHub Copilot がこれまでの**プレミアムリクエスト制（回数ベース）** から、**2026 年 6 月 1 日に重量課金制（トークンベース）** へ移行します。

正直なところ、「回数制のほうがわかりやすかったのに…」と思った人も多いんじゃないかなと思います。でも仕組みを理解すると、**使い方次第でコストをかなり抑えられる** ことがわかってきます！

この記事では、新しい課金の仕組みをざっくり解説しつつ、コンテキストとトークンを減らして賢く使う方法を国内外のコミュニティで話題になっているやり方も含めてまとめました。

### この記事でわかること

- ✅ 新しい課金単位「AI クレジット」の仕組み
- ✅ プランごとの包含クレジット量と実際のコスト感
- ✅ モデルごとのコスト比較（どのモデルが安いか）
- ✅ トークン・コンテキストを減らす具体的な節約術
- ✅ 海外コミュニティで話題の「賢い使い方」まとめ

---

## 重量課金制ってどういうこと？

これまでは**プレミアムリクエスト（PRU）** という「回数」でカウントしていました。モデルによって 1 倍〜15 倍のかけ算がかかる仕組みです。

新しい課金は**GitHub AI クレジット**という単位に変わります。

:::note info
**1 AI クレジット = $0.01 USD**

コストは「モデル × 使ったトークン数」で決まります。
:::

トークンとは、モデルに送られるテキストの断片みたいなものです。「入力トークン（あなたが送る内容）」「出力トークン（モデルが返す内容）」「キャッシュトークン（再利用されるコンテキスト）」の 3 種類があって、それぞれ異なる単価がかかります。

重量課金制の大事なポイントは、**「何回聞いたか」より「どれだけ長い会話をしたか」のほうがコストに直結する** という点です。

---

## プランごとの包含クレジット

2026 年 6 月以降の個人プランの包含クレジットはこんな感じです。

| プラン           | 月額 | ベースクレジット | フレックス | 合計                        |
| ---------------- | ---- | ---------------- | ---------- | --------------------------- |
| **Copilot Free** | 無料 | —                | —          | 少量（コード補完 2,000 回） |
| **Copilot Pro**  | $10  | 1,000            | 500        | **1,500**                   |
| **Copilot Pro+** | $39  | 3,900            | 3,100      | **7,000**                   |
| **Copilot Max**  | $100 | 10,000           | 10,000     | **20,000**                  |

フレックス分は毎月変動する可能性がある追加バッファです（AI の経済状況に応じて調整されると GitHub は説明しています）。

包含クレジットを使い切ったら $0.01/クレジット で追加購入できます（Free プランは不可）。予算上限を設定して使いすぎを防ぐこともできます！

:::note warn
コードの**インライン補完（グレーのサジェスト）とネクストエディットサジェストは引き続き無制限・無料**です。クレジットを消費するのは Chat・Agent Mode・CLI・Cloud Agent などです。
:::

---

## モデル別コスト比較

新課金制では**モデル選択がコストに直撃**します。主要モデルのざっくりコスト感はこんな感じです（単位：100 万トークンあたりの USD）。

| モデル                         | 種別 | 入力  | キャッシュ | 出力   | コスト感      |
| ------------------------------ | ---- | ----- | ---------- | ------ | ------------- |
| **GPT-5 mini**                 | 軽量 | $0.25 | $0.025     | $2.00  | ⭐ 超安       |
| **Gemini 3 Flash**             | 軽量 | $0.50 | $0.05      | $3.00  | ⭐ 超安       |
| **Raptor mini**（GitHub 独自） | 軽量 | $0.25 | $0.025     | $2.00  | ⭐ 超安       |
| **Claude Haiku 4.5**           | 汎用 | $1.00 | $0.10      | $5.00  | ✅ 安い       |
| **GPT-4.1**                    | 汎用 | $2.00 | $0.50      | $8.00  | ✅ 標準       |
| **Gemini 3.1 Pro**             | 強力 | $2.00 | $0.20      | $12.00 | 💰 高め       |
| **Claude Sonnet 4.6**          | 汎用 | $3.00 | $0.30      | $15.00 | 💰 高め       |
| **GPT-5.4**                    | 強力 | $2.50 | $0.25      | $15.00 | 💰 高め       |
| **Claude Opus 4.7**            | 最強 | $5.00 | $0.50      | $25.00 | 💸 かなり高い |
| **GPT-5.5**                    | 最強 | $5.00 | $0.50      | $30.00 | 💸 かなり高い |

ちなみに GPT-5 mini と Raptor mini は**インクルードドモデル（追加コストゼロ）** として特別扱いされています。Copilot Pro の 1,500 クレジット = $15 なので、GPT-5 mini で出力 100 万トークン生成してもクレジットを使い切れない計算です。正直、軽量モデルで済む作業はどんどん GPT-5 mini に任せてしまうのが賢いと思います！

---

## コストを抑える 6 つの戦略

### 1. モデルを「タスクの重さ」で使い分ける

一番効果が大きい節約術です。

「ちょっとコメント書いて」「変数名どう思う？」みたいな軽いタスクに GPT-5.5 を使うのはもったいないです。

| タスクの種類                       | 推奨モデル                         |
| ---------------------------------- | ---------------------------------- |
| 簡単な質問・コメント生成・短い補完 | GPT-5 mini / Gemini 3 Flash        |
| 一般的なコーディング・リファクタ   | GPT-4.1 / Claude Haiku 4.5         |
| 設計相談・難しいバグ調査           | Claude Sonnet 4.6 / Gemini 3.1 Pro |
| 複雑なアーキテクチャ・長い推論     | Claude Opus 4.7 / GPT-5.5          |

海外コミュニティでよく言われているのは **「Tier 1 → 無理なら Tier 2 に昇格」** という戦略です。まず軽量モデルで試して、解決しなかったら強力なモデルに切り替える流れで使うとコストを抑えやすいです！

### 2. 会話を短く保つ（コンテキスト窓の管理）

重量課金制で地味に効いてくるのが**会話の長さ**です。

チャット履歴が長くなるほど「入力トークン」が増えます。30 ターン続いた会話の 31 ターン目は、その前の 30 ターン全部がコンテキストとして送られます。これが結構くさいです。

**実践的な対策：**

- 同じ話題が一段落したら**新しいチャットを始める**
- GitHub.com の Copilot Chat には「スレッドを終了」機能がある
- VS Code では `Ctrl+L` で会話をリセット（ウィンドウタイトルの右のゴミ箱アイコンでも可）

「1 タスク 1 セッション」で使うのが海外で推奨されているやり方です。セッションをまたぐと前の文脈が引き継がれない分、コンテキストが増えなくて済みます。

### 3. インライン補完を積極活用する（無料！）

これは盲点になりがちですが、**コードを書くときはなるべく Chat を使わず、インライン補完に任せる** という意識が大事です。

インライン補完とネクストエディットサジェストは AI クレジットを消費しません。課金されるのは Chat に送ったメッセージのみです。

「ここのロジックを書いて」と Chat で頼むより、コードを書き始めて補完に乗っかるほうがコストゼロです！エディタ上で少し書き出すだけで、意外と欲しいコードが出てきます。

### 4. コンテキストファイルを整備して「往復回数」を減らす

1 回のやり取りで答えが出れば、それだけ安くなります。「前提を共有する質問」を毎回やり取りするのをなくすのが目標です。

**おすすめの構成：**

```
.github/
  copilot-instructions.md  ← プロジェクトの前提・ルール・スタック
  skills/
    your-domain/SKILL.md   ← 専門的な操作手順・コンテキスト
```

`copilot-instructions.md` にプロジェクトの技術スタックやコーディングルールを書いておくと、毎回「このプロジェクトは TypeScript で〜」と説明する必要がなくなります。

SKILL.md はさらに深い手順書で、「Azure Bicep のレビュー頼むとき」「Qiita 記事書くとき」みたいに使い分けると便利です。

この方法は **Agent Skills Ninja**（`yamapan.agent-skill-ninja`）という VS Code 拡張で一元管理できます（別記事で詳しく書きました！）。

<details>
<summary>▼ Agent Skills Ninja のダウンロードはこちら</summary>

- [Agent Skills Ninja - VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=yamapan.agent-skill-ninja)
- [Agent Resources Ninja - VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=yamapan.agent-resources-ninja)（姉妹拡張。エージェント・プロンプト・MCP なども管理できる）

または VS Code のコマンドパレットから：

```
ext install yamapan.agent-skill-ninja
ext install yamapan.agent-resources-ninja
```

</details>

---

### コラム：Agent Skills Ninja / Agent Resources Ninja をコスト削減にも活かす

「スキル管理ツール」として紹介されることが多い Agent Skills Ninja ですが、実はトークン節約にも効いてくる設定がいくつかあります。

#### compact フォーマットで instruction ファイルを軽量化

Agent Skills Ninja が `AGENTS.md` に書き込むスキル一覧の形式を変えられます。

```json
{
  "skillNinja.outputFormat": "compact"
}
```

| フォーマット | 1 スキルあたりの文字数 | 特徴                                |
| ------------ | ---------------------- | ----------------------------------- |
| `full`       | 約 200 文字            | IMPORTANT プロンプト + 詳細テーブル |
| `compact`    | 約 100 文字            | 圧縮インデックス（トークン節約！）  |
| `legacy`     | 最小                   | IMPORTANT なし（後方互換用）        |

スキルを 10 個入れている場合、`full` → `compact` 切り替えだけで instruction ファイルのスキル一覧部分が約半分になります。毎回のチャットでそのファイルがコンテキストに含まれる場合、**会話のたびに節約が積み上がる**構造です！

#### AGENTS.md への記載内容を絞る（Agent Resources Ninja と併用時）

Agent Resources Ninja と一緒に使っている場合、`resourceNinja.kindsExcluded` でブロックに含める種別を絞れます。

```json
{
  "resourceNinja.kindsExcluded": ["agent", "instruction"]
}
```

Agent 定義や Instructions を instruction ブロックから除外することで、AGENTS.md のサイズを抑えられます。「毎回全部のリソースが読まれる必要はない」タスクが多いなら試す価値あります。

#### SKILL.md は「When to Use」を必ず書く

SKILL.md に `## When to Use`（いつ使うか）セクションを書いておくと、エージェントが「このタスクにはこのスキルは不要」と判断して、**スキルの中身を読みにいかない**ことがあります。

```markdown
## When to Use

Azure Bicep のテンプレート作成・レビューを依頼されたとき。
他の IaC（Terraform など）や一般的なコーディングには使わない。
```

スキルを全部読み込まずに済む分、1 ターンあたりの入力トークンが増えにくくなります。

---

抽象的で長い質問は、長い回答 = 高い出力コストを生みます。

```
❌ 「このコードを見て全体的に改善できるところを教えて。
    パフォーマンスとか、読みやすさとか、セキュリティとか
    いろいろ見てほしい」

✅ 「この関数の計算量を O(n) 以下に改善してください」
```

「一質問一目的」でやり取りすると、出力が短くなってコストも下がります。海外の Copilot ユーザーの間では **"Atomic prompting"（原子的なプロンプト）** と呼ばれているやり方で、一度に複数のことを頼まないのがポイントです！

### 6. 使用量ダッシュボードで現状を把握する

コスト意識を持つには、まず自分がどのくらい使っているかを知るのが大事です。

- **GitHub.com** → `Settings` → `Copilot` → `Usage` から使用量を確認できます
- `premium request analytics page` から CSV ダウンロードも可能
- [Billing Preview Tool](https://copilot-billing-preview.github.com/) にアップすると、旧課金と新課金の比較ができます

移行前に一度チェックしてみると「意外と自分はこのモデルを使いすぎている」という気づきがあって面白いです。

---

## 海外コミュニティで話題になっているやり方

### ① "Context Diet"（コンテキストダイエット）

Reddit や GitHub Discussions で最近よく見かけるコンセプトです。

- 大きなファイルを `#file` で丸ごと添付しない
- 「関係あるクラスだけ」「このメソッドだけ」を選択して送る
- `.copilotignore` や `files.exclude` で不要ファイルをコンテキストから除外する

エディタが自動でコンテキストに含める範囲を絞ることで、知らないうちにトークンを消費している状況を防げます。

### ② "Model Routing"（モデルのルーティング）

VS Code 1.120 以降では `Auto` モデルを使うと、Copilot がタスクの難易度を見て自動でモデルを選んでくれます。

```
# settings.json
{
  "github.copilot.chat.models.preferred": "auto"
}
```

`auto` 設定を使うと、Copilot 自身がシンプルなタスクには軽量モデル、複雑なタスクには強力なモデルを割り当てます。手動でモデルを選び続けるのが面倒な人に向いています！

### ③ キャッシュトークンを活かす

Anthropic モデル（Claude 系）はキャッシュトークン価格がかなり安い（入力の約 1/10）です。

同じプロジェクト・同じ instruction ファイルを繰り返し使う会話ではキャッシュが効きやすいので、セッションをリセットしすぎると逆にキャッシュが使えなくなります。バランスが必要です。

長い instruction ファイルを持っている場合は、同一プロジェクト内での会話を続けるほうがキャッシュが効いてコスト節約になることがあります。

### ④ Agent Mode の使いすぎに注意

Agent Mode（エージェントモード）はすごく便利ですが、**内部で複数回のモデル呼び出しが発生**します。

複雑なタスクをエージェントに丸投げすると、ツール呼び出し・コード生成・確認・修正…とループが続いてコストが積み上がります。

海外の "Responsible Copilot Usage" 系のガイドで推奨されているのは：

- **Chat（会話）で設計を固めてから**、Agent Mode に実装を頼む
- タスクを小さく分割して、1 ステップずつ頼む

「大きな仕事を 1 回で頼む」よりも「小さく分けて確認しながら進める」ほうが、結果的にコストが安くなることが多いです。

---

## 予算上限の設定（使いすぎ防止）

包含クレジットを使い切った後も自動で課金が続くのが心配な場合は、**追加使用の予算上限**を設定できます。

`Settings` → `Billing & plans` → Copilot の `Spending limit` からドル建てで上限を設定できます（$0 にすると包含クレジット超過後は使用停止）。

個人利用なら最初は $0 にしておいて、必要なら都度上げるのが安心です！

---

## まとめ

重量課金制への移行は「使えば使うほど払う」仕組みになるので、最初は不安かもしれません。でも、**「何に払っているか」が明確になる**という点では旧課金よりわかりやすいとも言えます。

節約のポイントをおさらいすると：

- **モデルは用途で使い分ける**（軽いタスクは GPT-5 mini で十分！）
- **会話は短く保つ**（1 タスク 1 セッションが基本）
- **インライン補完は無料**（積極的に使い倒す）
- **instruction ファイルを整備する**（往復回数を減らす）
- **質問は具体的に**（原子的なプロンプト）
- **ダッシュボードで使用量を定期チェック**

最初から全部やろうとするとしんどいので、まずはモデルの使い分けと会話の短さを意識するだけでも変わると思います。あとは `auto` モデルに任せてしまうのも全然アリです！

私もまだ試しながら最適なやり方を探っている最中なので、もし「このやり方が効いた！」とかあればぜひコメントで教えてもらえると嬉しいです🙇‍♂️

---

## 参考

<details>
<summary>📄 公式ドキュメント（クリックで展開）</summary>

- [Usage-based billing for individuals - GitHub Docs](https://docs.github.com/en/copilot/concepts/billing/usage-based-billing-for-individuals)
- [Models and pricing for GitHub Copilot - GitHub Docs](https://docs.github.com/en/copilot/reference/copilot-billing/models-and-pricing)
- [Preparing for your move to usage-based billing - GitHub Docs](https://docs.github.com/en/copilot/how-tos/manage-and-track-spending/prepare-for-your-move-to-usage-based-billing)
- [About individual GitHub Copilot plans - GitHub Docs](https://docs.github.com/en/copilot/managing-copilot/managing-copilot-as-an-individual-subscriber/about-github-copilot-free)
- [Model multipliers for annual plans - GitHub Docs](https://docs.github.com/en/copilot/reference/copilot-billing/model-multipliers-for-annual-plans)

</details>

<details>
<summary>🔧 ツール・拡張機能（クリックで展開）</summary>

- [Copilot Billing Preview Tool（旧課金 vs 新課金の比較）](https://copilot-billing-preview.github.com/)
- [Agent Skills Ninja - VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=yamapan.agent-skill-ninja)
- [Agent Resources Ninja - VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=yamapan.agent-resources-ninja)

</details>

<details>
<summary>🛒 プラン・価格ページ（クリックで展開）</summary>

- [GitHub Copilot 価格ページ](https://github.com/features/copilot#pricing)
- [GitHub Copilot プランの比較 - GitHub Docs](https://docs.github.com/en/copilot/about-github-copilot/subscription-plans-for-github-copilot)
- [使用量ダッシュボード（要ログイン）](https://github.com/settings/copilot)

</details>
