# Playwright MCP コード例集

# 記事「Playwright MCPの活用方法 + Azure連携考察」用

---

## 1. VS Code 設定（`.vscode/mcp.json`）

```json
{
  "servers": {
    // ── パターン①: 基本設定（ブラウザウィンドウを表示しながら確認したい場合） ──
    "playwright": {
      "type": "stdio",
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    }

    // ── パターン②: ヘッドレス + Chrome指定 + testing capabilities 追加版 ──
    // CI環境・バックグラウンド実行・テスト自動化向け
    // パターン①と切り替える場合は、上記ブロックをコメントアウトしてこちらを有効化
    //
    // "playwright": {
    //   "type": "stdio",
    //   "command": "npx",
    //   "args": [
    //     "@playwright/mcp@latest",
    //     "--headless",          // ヘッドレスモード（ブラウザ非表示）
    //     "--browser", "chrome", // Chrome を明示指定（デフォルトは chromium）
    //     "--caps", "testing"    // testing capabilitiesを有効化（スクリーンショット・アクセシビリティツリー等）
    //   ]
    // }
  }
}
```

---

## 2. Claude Desktop 設定（`claude_desktop_config.json`）

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"],
      // ヘッドレスで動かす場合は以下のように args を変更:
      // "args": ["@playwright/mcp@latest", "--headless"]
      "env": {}
    }
  }
}
```

> **設定ファイルの場所**
>
> - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
> - Windows: `%APPDATA%\Claude\claude_desktop_config.json`

---

## 3. VS Code Copilot Agent モード プロンプト例

### 3-1. E2Eテストフロー確認

```
@agent playwright MCPを使って https://example.com のログインフローを確認してください。

手順:
1. トップページにアクセスし、スクリーンショットを撮る
2. メールアドレスフィールドに test@example.com を入力
3. パスワードフィールドに入力（⚠️ 実際の認証情報は入力しないこと）
4. ログインボタンをクリック
5. ダッシュボードへの遷移を確認しスクリーンショットを撮る
6. 各ステップの結果をまとめて報告する
```

### 3-2. デプロイ後のスモークテスト

```
@agent 以下のURLにデプロイされたアプリのスモークテストを実施してください。

対象URL: https://my-app.azurestaticapps.net

確認項目:
1. トップページが正常に表示されるか（ステータスコード・タイトル確認）
2. ナビゲーションリンクがすべて壊れていないか（404チェック）
3. 主要なCTAボタンが表示・クリック可能か
4. レスポンシブ表示（モバイル幅 375px）でレイアウト崩れがないか

問題があれば箇所を特定してスクリーンショット付きで報告してください。
```

### 3-3. アクセシビリティ確認

```
@agent https://example.com のアクセシビリティ問題を確認してください。

以下の観点でチェックしてください:
1. アクセシビリティツリーを取得し、主要な操作要素にrole・aria-labelが設定されているか確認
2. キーボードのみでログインフォームを操作できるか（Tab順序が自然か）
3. 画像にalt属性が設定されているか
4. 色コントラストが不十分に見える箇所があるか（目視確認で構わない）

WCAG 2.1 AA 基準で問題のある箇所をリストアップしてください。
```

### 3-4. フォームの動作確認

```
@agent https://example.com/contact の問い合わせフォームの動作を確認してください。

テストケース:
1. 【正常系】全必須項目を入力して送信 → 完了メッセージが表示されるか
2. 【異常系①】必須項目を空のまま送信 → バリデーションエラーが表示されるか
3. 【異常系②】メールアドレス形式が不正（例: "not-email"）→ 適切なエラーが出るか
4. 【異常系③】テキストエリアに1001文字以上入力 → 文字数制限エラーが出るか

各テストケースの結果をPASSまたはFAILで表形式にまとめてください。
```

---

## 4. GitHub Actions スモークテスト（`playwright-mcp-smoke.yml`）

```yaml
name: Playwright MCP Smoke Test

on:
  # Azure Static Web Apps のデプロイ完了後に実行
  deployment_status:
  # 手動実行も可能にしておく
  workflow_dispatch:
    inputs:
      target_url:
        description: "テスト対象のURL"
        required: true
        default: "https://my-app.azurestaticapps.net"

jobs:
  smoke-test:
    # デプロイ成功時のみ実行
    if: github.event_name == 'workflow_dispatch' || github.event.deployment_status.state == 'success'
    runs-on: ubuntu-latest

    steps:
      - name: リポジトリをチェックアウト
        uses: actions/checkout@v4

      - name: Node.js 20 をセットアップ
        uses: actions/setup-node@v4
        with:
          node-version: "20"
          cache: "npm"

      - name: 依存パッケージをインストール
        run: npm ci

      # Chromium とシステム依存ライブラリを一括インストール
      - name: Playwright (Chromium) をインストール
        run: npx playwright install --with-deps chromium

      # ⚠️ MCPサーバーはバックグラウンド起動し、PIDを保持しておく
      - name: Playwright MCP サーバーをヘッドレス起動
        run: |
          npx @playwright/mcp@latest --headless --browser chrome --port 8931 &
          echo "MCP_SERVER_PID=$!" >> $GITHUB_ENV
          # サーバーが起動するまで少し待機
          sleep 3

      # テストスクリプトを実行（MCPクライアントとしてサーバーに接続）
      - name: スモークテストを実行
        env:
          # ⚠️ シークレットは GitHub Secrets で管理すること
          TARGET_URL: ${{ github.event.inputs.target_url || github.event.deployment_status.environment_url }}
          MCP_SERVER_URL: "http://localhost:8931"
        run: node scripts/run-smoke-test.js

      # テスト結果のスクリーンショットをアーティファクトとして保存
      - name: テスト結果をアップロード
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: smoke-test-results
          path: test-results/
          retention-days: 7

      # MCP サーバーを停止
      - name: MCP サーバーを停止
        if: always()
        run: kill $MCP_SERVER_PID || true
```

---

## 5. Azure DevOps Pipeline（`azure-pipelines.yml`）

```yaml
trigger:
  - main

# ⚠️ セルフホステッドエージェントを使う場合は pool の設定を変更すること
pool:
  vmImage: "ubuntu-latest"

variables:
  # ⚠️ 機密情報は Azure DevOps の Variable Groups / Key Vault で管理する
  NODE_VERSION: "20.x"
  TARGET_URL: "https://my-app.azurestaticapps.net"

stages:
  - stage: SmokeTest
    displayName: "Playwright MCP スモークテスト"
    jobs:
      - job: RunSmokeTest
        displayName: "ヘッドレスブラウザでスモークテスト実行"
        steps:
          - task: NodeTool@0
            displayName: "Node.js $(NODE_VERSION) をインストール"
            inputs:
              versionSpec: $(NODE_VERSION)

          - script: npm ci
            displayName: "依存パッケージをインストール"

          # Chromium とシステム依存ライブラリを一括インストール
          - script: npx playwright install --with-deps chromium
            displayName: "Playwright Chromium をインストール"

          # ⚠️ バックグラウンド起動 & PID保持
          - script: |
              npx @playwright/mcp@latest \
                --headless \
                --browser chrome \
                --port 8931 &
              echo "##vso[task.setvariable variable=MCP_PID]$!"
              sleep 3
            displayName: "Playwright MCP サーバーをヘッドレス起動"

          - script: node scripts/run-smoke-test.js
            displayName: "スモークテストを実行"
            env:
              TARGET_URL: $(TARGET_URL)
              MCP_SERVER_URL: "http://localhost:8931"

          # テスト結果をパイプライン成果物として発行
          - task: PublishPipelineArtifact@1
            displayName: "テスト結果を発行"
            condition: always()
            inputs:
              targetPath: "test-results"
              artifact: "smoke-test-results"
              publishLocation: "pipeline"

          # MCP サーバーを終了
          - script: kill $(MCP_PID) || true
            displayName: "MCP サーバーを停止"
            condition: always()
```

---

## 6. Docker で Playwright MCP 起動

### 6-1. 基本的な起動コマンド

```bash
# Playwright 公式 Docker イメージで MCP サーバーを起動
# ⚠️ ポート 8931 をホスト側に開放するため、公開環境では認証・ファイアウォール設定を忘れずに
docker run --rm -it \
  -p 8931:8931 \
  mcr.microsoft.com/playwright/mcp:latest \
  --headless \
  --browser chromium \
  --port 8931
```

### 6-2. Azure Container Apps へのデプロイ用設定

```bash
# ── ① コンテナレジストリにイメージをプッシュ ──
# ⚠️ ACR 名は自分の環境に合わせて変更すること
ACR_NAME="myacr"
IMAGE_TAG="${ACR_NAME}.azurecr.io/playwright-mcp:latest"

# Dockerfile を使って独自イメージをビルド（カスタム設定を埋め込む場合）
docker build -t "${IMAGE_TAG}" .

# ⚠️ ACR へのログインには適切な権限（AcrPush ロール）が必要
az acr login --name "${ACR_NAME}"
docker push "${IMAGE_TAG}"

# ── ② Azure Container Apps にデプロイ ──
# ⚠️ --ingress external にするとインターネットから直接アクセス可能になる
#    本番運用では認証（managed identity / Entra ID）を必ず設定すること
az containerapp create \
  --name "playwright-mcp-server" \
  --resource-group "my-rg" \
  --environment "my-aca-env" \
  --image "${IMAGE_TAG}" \
  --target-port 8931 \
  --ingress internal \
  --min-replicas 1 \
  --max-replicas 3 \
  --cpu 1.0 \
  --memory 2.0Gi \
  --command "npx" \
  --args "@playwright/mcp@latest,--headless,--browser,chromium,--port,8931"
```

---

## 7. `--storage-state` を使った認証フロー

### 7-1. ログイン状態を事前に保存する

```bash
# ① ブラウザを起動して手動ログイン → 認証状態を auth.json に保存
# ⚠️ auth.json には認証トークンが含まれるため .gitignore に追加すること
npx @playwright/mcp@latest \
  --browser chromium \
  --save-storage ./auth.json

# ターミナル出力の指示に従い、ブラウザでログイン操作を完了してから Ctrl+C で終了
# → auth.json にセッション Cookie / localStorage が保存される
```

### 7-2. 保存した認証状態を再利用する（`.vscode/mcp.json`）

```json
{
  "servers": {
    "playwright": {
      "type": "stdio",
      "command": "npx",
      "args": [
        "@playwright/mcp@latest",
        "--headless",
        "--browser",
        "chromium",
        // ⚠️ auth.json はリポジトリにコミットしないこと（.gitignore に追加）
        // CI環境では Secrets からファイルを復元する仕組みを用意する
        "--load-storage",
        "./auth.json"
      ]
    }
  }
}
```

### 7-3. CI環境での auth.json 管理例（GitHub Actions）

```yaml
# ⚠️ auth.json の中身を GitHub Secret に保存しておき、実行時にファイルとして展開する方法
- name: 認証状態ファイルを復元
  run: |
    echo '${{ secrets.PLAYWRIGHT_AUTH_JSON }}' > ./auth.json
  # auth.json はジョブ終了時に自動削除される（runner の一時ディレクトリを使う方が安全）
```

---

> **前提パッケージのインストール**
>
> ```bash
> # Playwright MCP は npm から直接 npx で実行可能（インストール不要）
> # ただし Node.js 18 以上が必要
> node --version  # v18.x 以上であることを確認
>
> # プロジェクトに固定バージョンで導入する場合
> npm install --save-dev @playwright/mcp
> ```
