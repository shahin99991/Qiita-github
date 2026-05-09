# デモ手順書 & スクショチェックリスト

## 記事「GitHub Copilot × MCP × Azure DevOps」

---

## 事前準備

- [ ] Azure DevOps の組織にアクセスできる状態にする
- [ ] VS Code を最新版にアップデート済み
- [ ] Node.js v20以上がインストール済み（`node -v` で確認）
- [ ] GitHub Copilot が VS Code で有効になっている

---

## PHASE 1: Azure DevOps でユーザー・ストーリーを用意する

### 手順 1-1: Azure DevOps にログイン

1. ブラウザで `https://dev.azure.com/<組織名>` を開く
2. 対象のプロジェクトをクリックして開く

### 手順 1-2: Issueを作成する

:::note info
💡 **プロセステンプレートについて**  
Azure DevOpsのプロジェクトがBasicテンプレートの場合、Work ItemはEpic・Issue・Taskの3種類のみです。AgileやScrumテンプレートであればUser Storyが使えますが、BasicではIssueがUser Storyに相当します。
:::

1. 左サイドバーの **「Boards」** をクリック
2. **「Work items」** をクリック
3. 右上の **「+ New Work Item」** をクリック
4. ドロップダウンから **「Issue」** を選択
5. タイトルに `ログイン機能` と入力して Enter
6. 作成されたWork Itemをクリックして詳細画面を開く
7. **「Description」** 欄に以下を入力（BasicテンプレートはAcceptance Criteriaフィールドがないため、Descriptionにまとめて書く）：

   ```
   ユーザーとして、メールアドレスとパスワードを入力してログインし、ダッシュボードへ遷移できる。

   【受け入れ条件】
   - 正しい認証情報でログインできること
   - 誤ったパスワードでエラーメッセージが表示されること
   - 3回連続失敗でアカウントがロックされること
   ```

8. 右上の **「Save」** ボタンをクリック
9. URLバーに表示されるWork Item IDをメモしておく（例: `42`）

> 📸 **スクショ #6** ← ここで撮る  
> 受け入れ条件が入力済みのIssue詳細画面。タイトルとDescriptionが全部見えている状態。

---

## PHASE 2: PAT（Personal Access Token）を発行する

### 手順 2-1: PAT発行画面を開く

1. Azure DevOps 画面の**右上のアイコン（自分のアバター）** をクリック
2. ドロップダウンから **「Personal access tokens」** をクリック
3. 「Personal Access Tokens」ページが開く

### 手順 2-2: 新しいPATを作成する

1. 右上の **「+ New Token」** ボタンをクリック
2. 以下を設定する：
   - **Name**: `copilot-mcp-demo`（任意の名前）
   - **Organization**: 対象の組織を選択
   - **Expiration**: `30 days`（デモ用なので短くてOK）
   - **Scopes**: **「Custom defined」** を選択
3. スコープ一覧をスクロールして **「Work Items」** を探す
4. **「Work Items」の「Read & Write」** にチェックを入れる
5. さらに **「Project and Team」の「Read」** にチェックを入れる

> 📸 **スクショ #1** ← ここで撮る  
> スコープのチェックボックスが選択された状態のPAT作成フォーム。「Work Items: Read & Write」と「Project and Team: Read」が見えている画面。

6. 下部の **「Create」** ボタンをクリック
7. 表示されたトークン文字列をコピーして安全な場所に保存する（この画面を閉じると二度と見られない）

---

## PHASE 3: VS Code に MCP を設定する

### 手順 3-1: 環境変数を設定する

ターミナル（VS Code の統合ターミナル）を開いて以下を実行：

```bash
export AZURE_DEVOPS_PAT="ここにさっきコピーしたトークンを貼る"
export AZURE_DEVOPS_ORG="https://dev.azure.com/あなたの組織名"
```

※ `.bashrc` や `.zshrc` に追記しておくと次回以降も有効。

### 手順 3-2: プロジェクトに mcp.json を作成する

1. VS Code で対象のプロジェクトフォルダを開く
2. ルートに `.vscode` フォルダがなければ作成する
3. `.vscode/mcp.json` を新規作成して以下を貼り付ける：

```json
{
  "servers": {
    "azure-devops": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@azure-devops/mcp-server"],
      "env": {
        "AZURE_DEVOPS_PAT": "${env:AZURE_DEVOPS_PAT}",
        "AZURE_DEVOPS_ORG": "${env:AZURE_DEVOPS_ORG}"
      }
    }
  }
}
```

4. ファイルを保存（`Ctrl+S` / `Cmd+S`）

### 手順 3-3: MCP接続を確認する

1. VS Code を**コマンドパレット**（`Ctrl+Shift+P` / `Cmd+Shift+P`）で開く
2. `MCP: List Servers` と入力してEnter（または `Reload Window` でVS Codeを再起動）
3. Copilotのチャットパネルを開く（左サイドバーの Copilot アイコン、またはショートカット `Ctrl+Alt+I`）
4. チャット入力欄の左にある **🔧（ツール）アイコン** をクリック
5. ツール一覧に **「azure-devops」** が表示されていることを確認する

> 📸 **スクショ #2** ← ここで撮る  
> Copilotチャットのツール一覧（または Available Tools パネル）に「azure-devops」が表示されている画面。

---

## PHASE 4: ユーザー・ストーリーからテストを自動生成する

### 手順 4-1: プロンプトを入力する

1. Copilot チャットパネルで **Agent モード**（「Ask」ではなく「Agent」）を選択
2. 以下のプロンプトを入力して Enter：

```
#azure-devops
Work Item ID 42（ログイン機能）の詳細と受け入れ条件を読み込んで、
Playwright を使ったE2Eテストを日本語コメント付きで生成してください。
ファイルは tests/e2e/login.spec.ts に保存してください。
```

※ `42` の部分はPHASE 1でメモしたWork Item IDに変更すること。

### 手順 4-2: 生成中の様子を撮る

Copilotがレスポンスを返し始めたタイミング（ツール呼び出しのログが流れているとき）を狙う。

> 📸 **スクショ #7** ← ここで撮る  
> チャット画面に「Using azure-devops > get_work_item」などのツール呼び出しログが表示されている状態。

### 手順 4-3: ファイル生成を確認する

1. Copilotがコードを出力し終わったら、`tests/e2e/login.spec.ts` が作成されているか確認する
2. VS Code のエクスプローラーパネルで該当ファイルをクリックして開く

> 📸 **スクショ #3** ← ここで撮る  
> 左にエクスプローラー（ファイルツリー）、右にCopilotチャット（生成済みのレスポンス）が両方見えるよう、画面を分割して撮る。

> 📸 **スクショ #4** ← ここで撮る  
> `login.spec.ts` をエディタで開いた状態。コードが全文表示されている画面。

---

## PHASE 5: 生成されたテストを実行する

### 手順 5-1: Playwright をインストールする（未インストールの場合）

```bash
npm install -D @playwright/test
npx playwright install chromium
```

### 手順 5-2: テストを実行する

```bash
npx playwright test tests/e2e/login.spec.ts --reporter=list
```

実際のアプリがない場合は失敗するが、「テストが構造として実行された」ことが伝われば十分。

> 📸 **スクショ #8** ← ここで撮る  
> ターミナルにテスト結果（PASS / FAIL）が表示されている状態。テスト名（日本語）が読めるように撮る。

---

## PHASE 6: 大きなタスクを子タスクに自動細分化する

### 手順 6-1: Epic チケットを用意する（まだなければ）

> BasicテンプレートにはFeatureがないため、Epicで代用します。

1. Azure DevOps の Work items ページに戻る
2. **「+ New Work Item」** → **「Epic」** を選択
3. タイトルに `決済機能の実装` と入力して保存
4. Work Item IDをメモ（例: `10`）

### 手順 6-2: 細分化プロンプトを入力する

Copilot チャットに戻り、以下を入力して Enter：

```
#azure-devops
Epic ID 10「決済機能の実装」を読み込んで、
フロントエンド・バックエンド・インフラ・テストの観点で
実装タスクに分解してください。
各タスクには工数の見積もりと担当領域を含め、
Azure Boards上にEpic 10の子Work Item（Task）として登録してください。
```

※ `10` の部分はメモしたWork Item IDに変更すること。

### 手順 6-3: 登録完了後にボードを確認する

1. Azure DevOps の Backlogs ページを開く
2. 左上のビュー切り替えで **「Backlogs」** を選択（スプリントではなくバックログ全体）
3. Epic-10 の左にある **「▶（展開矢印）」** をクリック
4. 子タスクがEpic-10の下に階層表示されていることを確認

> 📸 **スクショ #5** ← ここで撮る  
> Work itemsビューでEpic-10が展開され、子タスク（Task）が階層表示されている状態。タスク名・担当領域のカラムが見えるように画面を広げて撮る。

---

## 撮影後のチェックリスト

| #   | スクショ                        | 撮れた？ | モザイク必要？      |
| --- | ------------------------------- | -------- | ------------------- |
| 1   | PAT作成フォーム（スコープ選択） | ☐        | ✅ 組織名・トークン |
| 2   | VS Code MCPツール一覧           | ☐        | ✅ 組織名（URL内）  |
| 3   | Copilotチャット＋ファイルツリー | ☐        | —                   |
| 4   | login.spec.ts エディタ全文      | ☐        | —                   |
| 5   | Boardsの子タスク階層ビュー      | ☐        | ✅ 組織名・メアド   |
| 6   | US-42 詳細画面                  | ☐        | ✅ 組織名・メアド   |
| 7   | MCPツール呼び出しログ           | ☐        | ✅ 組織名（URL内）  |
| 8   | Playwright テスト結果           | ☐        | —                   |

---

## 記事へのスクショ貼り付け位置

| スクショ | 記事のどこに貼るか                                        |
| -------- | --------------------------------------------------------- |
| #6       | 「ユースケース1 > シナリオ」の直後                        |
| #1       | 「Step 1-2 > PATの取得」の直後                            |
| #2       | 「Step 1-3 > VS Code の MCP 設定」の直後                  |
| #3 / #7  | 「ユースケース1 > Copilotへのプロンプト例」の直後         |
| #4       | 「ユースケース1 > Copilotが生成するテストコード例」の直後 |
| #8       | ユースケース1の末尾（補足として）                         |
| #5       | 「ユースケース2 > Copilotが生成・登録するタスク例」の直後 |
