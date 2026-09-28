# デモ手順 & スクショ撮影タイミング

「Teams/Slack の GitHub Copilot 9月25日アップデート」記事用のデモ手順と、各画像の撮影タイミングをまとめたファイルです。

- 記事本体: [article-qiita.md](./article-qiita.md)
- 画像保存先: `./Images/`
- 画像URL形式: `https://raw.githubusercontent.com/shahin99991/Qiita-github/main/copilot-teams-slack-updates/Images/<ファイル名>`

> ⚠️ **公開前の注意**: 画像を GitHub に push するまで raw URL は 404 になります。記事公開前に必ず画像を先に push してください（リポジトリ規約より）。

---

## 事前準備（デモ環境）

| 項目        | 内容                                                                                            |
| ----------- | ----------------------------------------------------------------------------------------------- |
| プラン      | GitHub Copilot Business / Enterprise の組織                                                     |
| 管理者設定  | Copilot cloud agent ポリシー有効化 ＋ クラウドサンドボックス有効化                              |
| Teams       | GitHub app for Microsoft Teams を最新版にインストール/アップグレード                            |
| アカウント  | Teams で `@GitHub` メンション → GitHub アカウント連携済みにしておく                             |
| リポジトリ  | **https://github.com/YJK-Inc/Test-Repo**（デモ構築済み。書き込み権限を確認）                    |
| ネタ仕込み① | エラー画面のスクショ：後述の「エラー再現手順」でターミナルに `ZeroDivisionError` を表示して撮る |
| ネタ仕込み② | 別チャネルに「転送元」となる会話（要件のやり取りなど）を作っておく                              |

### デモ用リポジトリの中身

- `app/main.py` : 在庫管理アプリ。**意図的に `ZeroDivisionError` バグを含む**
- `docs/error-screenshot.md` : エラー再現手順とスクショ撮影メモ
- `.github/workflows/ci.yml` : CI（バグが直るまでは失敗する）

### エラー再現手順（img-02 用のネタ）

ローカルまたは GitHub Codespaces で以下を実行し、トレースバックが出たターミナル画面を撮影する。

```bash
git clone https://github.com/YJK-Inc/Test-Repo.git
cd Test-Repo
python app/main.py
# => ZeroDivisionError: division by zero が出る
```

撮影した画像は、デモ時に Teams へ**インライン画像**として貼り付けて使う。

:::note warn
社内テナントで撮影する場合、**社名・人名・メールアドレス・内部URL**は必ずモザイク or ダミー環境で撮影すること。
:::

---

## 撮影フロー（6枚）

### 📷 1. `img-01-teams-mention.png` — @GitHub メンションでセッション開始

**記事内の位置**: 「前提：Teams/Slack の GitHub Copilot って何ができるんだっけ」セクション

**手順**:

1. Teams のパブリックチャネル（デモ用）を開く
2. 初回のみ `@GitHub settings` でデフォルトリポジトリを `YJK-Inc/Test-Repo` に設定しておく
3. `@GitHub` とメンションし、「`YJK-Inc/Test-Repo` の README を最新の構成に更新して」など分かりやすいタスクを入力
4. Copilot が応答してセッション開始した直後の画面を撮影

**撮影ポイント**: メンション文と Copilot の最初の応答（セッション開始・計画の提示）が両方写るように撮る

---

### 📷 2. `img-02-image-context.png` — インライン画像の解析【目玉】

**記事内の位置**: 「📷 Teams のインライン画像をそのまま理解する」セクション

**手順**:

1. 事前準備で撮影した `ZeroDivisionError` のターミナル画像を、Teams のスレッドに**インラインで貼り付ける**
2. `@GitHub このエラー直して` とだけ書いて送信（`repo=YJK-Inc/Test-Repo` が必要なら付ける）
3. Copilot が画像の内容（`ZeroDivisionError`、`app/main.py` の該当行など）を読み取った旨を含む応答を返した直後を撮影

**撮影ポイント**: 「貼ったエラー画像」と「画像内容を言及している Copilot の回答」の両方が1画面に入るようにスクロールして撮る。**この記事で一番大事な1枚！**

---

### 📷 3. `img-03-forwarded-message.png` — 転送メッセージをコンテキスト化【目玉】

**記事内の位置**: 「🔁 転送メッセージの中身まで読む」セクション

**手順**:

1. 別チャネルに「在庫 0 の商品でもエラーにならないようにしてほしい」「税込み金額は整数で表示したい」といった要件のやり取りを用意しておく
2. その1件を「共有」→ 転送でデモ用チャネル/スレッドへ送る
3. 転送メッセージに続けて `@GitHub この内容を踏まえて Issue を立てて` と送信
4. Copilot が転送元の会話内容（要件）を言及した応答が返った直後を撮影

**撮影ポイント**: 転送メッセージのカード（転送元であることが分かる表示）と Copilot の応答がセットで写るように

---

### 📷 4. `img-04-thread-history.png` — スレッド履歴の保持【目玉】

**記事内の位置**: 「🧵 チャネル・スレッド履歴の保持が強化」セクション

**手順**:

1. スレッド内で数往復の会話を積む（例:「`app/main.py` のバグを調査して」「修正方針は例外にする？」など）
2. 続けて `@GitHub さっきの方針で進めて` など、**履歴を参照しないと答えられない指示**を送る
3. Copilot が過去のやり取り（`app/main.py` / 方針）を踏まえた回答を返した直後を撮影

**撮影ポイント**: 過去のメッセージ数件と、それを踏まえていることが分かる Copilot の回答を1画面に収める

---

### 📷 5. `img-05-model-switch.png` — セッション内モデル切り替え

**記事内の位置**: 「🧠 セッション内でモデル切り替えができる」セクション

**手順**:

1. セッション中に「今使ってるモデルは？」と聞く → 回答を確認
2. 「次から ○○（別モデル）に切り替えて」と送信
3. モデル切り替えの**確認メッセージ**が返ってきた直後を撮影

**撮影ポイント**: 切り替え依頼と確認応答のペアが見える構成で。公式 changelog のスクリーンショット（Slack でモデルを聞いて→切り替え確認）と同じ構図を意識する

---

### 📷 6. `img-06-work-links.png` — Issue 作成結果とリンク

**記事内の位置**: 「🔗 Issue 作成まわりも地味〜に賢くなってる」セクション

**手順**:

1. `@GitHub YJK-Inc/Test-Repo に「在庫0でエラーになる不具合」の Issue を作成して` と依頼（手順3の続きでもOK）
2. 作成完了の応答に含まれる **Issue への直接リンク** と **元スレッドへのリンク** が表示された状態を撮影
3. （余力があれば）類似 Issue のチェック結果に言及している応答も撮る

**撮影ポイント**: リンクがクリッカブルな状態で写っていること。リンク先URLはモザイク要否を確認

---

## 画像ファイル ↔ 記事内URL 対応表

| ファイル名                   | 記事内URL（raw）                                                                                                                | セクション         |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | ------------------ |
| img-01-teams-mention.png     | https://raw.githubusercontent.com/shahin99991/Qiita-github/main/copilot-teams-slack-updates/Images/img-01-teams-mention.png     | 前提のおさらい     |
| img-02-image-context.png     | https://raw.githubusercontent.com/shahin99991/Qiita-github/main/copilot-teams-slack-updates/Images/img-02-image-context.png     | インライン画像解析 |
| img-03-forwarded-message.png | https://raw.githubusercontent.com/shahin99991/Qiita-github/main/copilot-teams-slack-updates/Images/img-03-forwarded-message.png | 転送メッセージ     |
| img-04-thread-history.png    | https://raw.githubusercontent.com/shahin99991/Qiita-github/main/copilot-teams-slack-updates/Images/img-04-thread-history.png    | スレッド履歴保持   |
| img-05-model-switch.png      | https://raw.githubusercontent.com/shahin99991/Qiita-github/main/copilot-teams-slack-updates/Images/img-05-model-switch.png      | モデル切り替え     |
| img-06-work-links.png        | https://raw.githubusercontent.com/shahin99991/Qiita-github/main/copilot-teams-slack-updates/Images/img-06-work-links.png        | Issue作成・リンク  |

---

## 撮影Tips

- ブラウザ/Teams の表示倍率は **100〜125%** で統一（文字が読めるサイズ優先）
- ウィンドウ幅は全枚数で揃える（目安: 1200〜1400px 程度）
- 1枚あたりの情報量を絞り、「この1枚で何が分かるか」を明確にする
- 撮影後はファイル名を対応表どおりにリネームして `./Images/` に入れる
- 差し替えるだけなら URL 変更不要（同名で上書き → push でOK）
