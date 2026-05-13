---
title: "Playwright MCPをVS Code Copilotから使う — ブラウザ自動化からAzure連携まで"
tags:
  - PlaywrightMCP
  - GitHubCopilot
  - VSCode
  - MCP
  - Azure
---

## はじめに

`#fetch` ツールを使ってWebページを取得しようとしたとき、JavaScriptで描画されているSPAだとほとんど何も返ってこない、という場面に一度は当たったことがあると思います。

Playwright MCP（`@playwright/mcp`）はそこを埋めるツールです。Playwright のブラウザ操作能力を MCP サーバーとして公開し、VS Code の Copilot Agent モードや Claude Desktop から直接呼び出せるようにします。GitHubスター数は 32,000 を超え、2026年5月時点でも活発に開発が続いています。

この記事では以下をカバーします：

- ✅ Playwright MCP の仕組みと `#fetch` との使い分け
- ✅ VS Code への設定手順
- ✅ Agent モードでの実際のプロンプト例
- ✅ Azure 環境での活用シナリオと注意点

対象読者は、VS Code で Copilot を使っていて「ブラウザ操作もAIに任せてみたい」という方です。Playwright の使用経験は不要です。

## Playwright MCP とは

### MCP サーバーとしての Playwright

MCP（Model Context Protocol）は、AIモデルが外部ツール・データソースと通信するための標準プロトコルです。VS Code 1.99（2025年3月）でエージェントモードとともに正式サポートされました。

Playwright MCP はその MCP サーバー実装で、Playwright のブラウザ操作ツール群をLLMが呼び出せる形で公開します。

### スクリーンショット系 MCP との違い

Playwright MCP が選ばれる理由として、**アクセシビリティツリー（ARIA スナップショット）をテキストでLLMに渡す**設計があります。

|                | Playwright MCP（`browser_snapshot`） | スクリーンショット系     |
| -------------- | ------------------------------------ | ------------------------ |
| 出力形式       | ARIAテキストツリー（Markdown）       | PNG/JPEG画像             |
| 必要なモデル   | テキストモデルで処理可               | ビジョンモデルが必要     |
| 操作の精度     | セマンティックな要素参照で安定       | 座標指定なのでブレやすい |
| トークンコスト | 低い                                 | 高い（画像エンコード）   |

座標の「当て感」で操作するのではなく、`button[name="送信"]` のような要素の意味で操作するため、レイアウトが少し変わっても壊れにくいのが実務上のメリットです。

### `#fetch` との使い分け

| シナリオ                            | 向いているツール                             |
| ----------------------------------- | -------------------------------------------- |
| 静的なドキュメントページの取得      | `#fetch`（軽量・速い）                       |
| React/Vue/Angular 等のSPA           | **Playwright MCP**（JSフル実行）             |
| フォーム操作・ログイン・クリック    | **Playwright MCP**                           |
| Azure Portal など認証が必要なページ | **Playwright MCP**（`--storage-state` 使用） |
| 単純なAPIレスポンス確認             | `#fetch`                                     |

## セットアップ

### VS Code への追加

3通りの方法があります。一番手軽なのは方法 2 です。

**方法 1：Extensions ビューから検索**
`Ctrl+Shift+X` → `@mcp playwright` で検索 → Install

**方法 2：コマンド 1 行で追加**

```bash
code --add-mcp '{"name":"playwright","command":"npx","args":["@playwright/mcp@latest"]}'
```

**方法 3：`.vscode/mcp.json` を手書き**

```json
{
  "servers": {
    "playwright": {
      "type": "stdio",
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    }
  }
}
```

デフォルトはブラウザウィンドウが表示される headed モードです。バックグラウンドで動かしたい場合は `--headless` を追加します。

**CI や testing 用途向けの設定例：**

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
        "chrome",
        "--caps",
        "testing"
      ]
    }
  }
}
```

`--caps` で有効化できる追加機能は `testing`、`network`、`storage`、`devtools`、`vision`、`pdf` などがあります。デフォルトではコア操作ツール（navigate / click / fill / snapshot / screenshot など）のみが有効です。

### Claude Desktop への追加

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    }
  }
}
```

設定ファイルの場所：

- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

### Docker で動かす場合

公式イメージ `mcr.microsoft.com/playwright/mcp` を使います。

```bash
docker run --rm -it \
  -p 8931:8931 \
  mcr.microsoft.com/playwright/mcp:latest \
  --headless \
  --browser chromium \
  --port 8931
```

MCP クライアント側の設定：

```json
{
  "servers": {
    "playwright": {
      "url": "http://localhost:8931/mcp"
    }
  }
}
```

## VS Code Agent モードでの使い方

設定後、VS Code の Chat ビューで Agent モードを選ぶと、Playwright MCP のツールが自動的に認識されます。ツール使用時に承認ダイアログが出るので、`Continue` で許可します（`chat.tools.autoApprove` で自動承認も可）。

### プロンプト例

**デプロイ後のスモークテスト：**

```
https://my-app.azurestaticapps.net にアクセスして、
1. トップページが正常に表示されているか確認する
2. ナビゲーションリンクが壊れていないかチェックする
3. 主要なCTAボタンが表示・クリック可能か確認する
問題があればスクリーンショット付きで報告してください。
```

**フォームのバリデーション確認：**

```
https://example.com/contact の問い合わせフォームを以下のケースで操作してください：
1. 必須項目を空のまま送信 → バリデーションエラーが表示されるか確認
2. メールアドレスに "not-email" を入力 → 適切なエラーメッセージが出るか確認
各ケースの結果を PASS/FAIL 形式でまとめてください。
```

**アクセシビリティ確認：**

```
https://example.com のアクセシビリティツリーを取得して、
aria-label が未設定のボタンや、alt が空の画像がないか確認してください。
問題箇所があればセレクターと修正案を添えて報告してください。
```

**Playwright テストコードの生成：**

```
https://localhost:3000/login にアクセスし、ログインフローを操作してください。
操作が終わったら、同じフローを再現する Playwright TypeScript テストコードを生成してください。
```

`--caps testing` を有効にすると `browser_generate_locator` や `browser_verify_text_visible` などのテスト支援ツールも使えます。

## Azure 環境での活用（考察）

### GitHub Actions でデプロイ後の確認を自動化する

Azure Static Web Apps にデプロイした後、Playwright MCP サーバーをヘッドレスで起動してスモークテストを走らせるパターンです。

```yaml
name: Playwright MCP Smoke Test

on:
  deployment_status:
  workflow_dispatch:
    inputs:
      target_url:
        description: "テスト対象URL"
        required: true
        default: "https://my-app.azurestaticapps.net"

jobs:
  smoke-test:
    if: github.event_name == 'workflow_dispatch' || github.event.deployment_status.state == 'success'
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: "20"

      - run: npx playwright install --with-deps chromium

      - name: MCP サーバーをバックグラウンドで起動
        run: |
          npx @playwright/mcp@latest --headless --browser chrome --port 8931 &
          echo "MCP_SERVER_PID=$!" >> $GITHUB_ENV
          sleep 3

      - name: スモークテストを実行
        env:
          TARGET_URL: ${{ github.event.inputs.target_url || github.event.deployment_status.environment_url }}
          MCP_SERVER_URL: "http://localhost:8931"
        run: node scripts/run-smoke-test.js

      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: smoke-test-results
          path: test-results/

      - name: MCP サーバーを停止
        if: always()
        run: kill $MCP_SERVER_PID || true
```

### Azure DevOps パイプラインで使う場合

```yaml
pool:
  vmImage: "ubuntu-latest"

steps:
  - task: NodeTool@0
    inputs:
      versionSpec: "20.x"

  - script: npx playwright install --with-deps chromium

  - script: |
      npx @playwright/mcp@latest \
        --headless \
        --browser chrome \
        --port 8931 &
      echo "##vso[task.setvariable variable=MCP_PID]$!"
      sleep 3
    displayName: "MCP サーバー起動"

  - script: node scripts/run-smoke-test.js
    env:
      TARGET_URL: $(TARGET_URL) # Variable Groups で管理する
      MCP_SERVER_URL: "http://localhost:8931"

  - script: kill $(MCP_PID) || true
    condition: always()
    displayName: "MCP サーバー停止"
```

:::note warn
⚠️ **`--no-sandbox` について**: CI エージェントの環境によっては sandbox 関連のエラーが出る場合があります。その場合は `args` に `--no-sandbox` を追加します。ただし非 root 実行が保証されている場合のみ。
:::

### Azure Container Apps で MCP サーバーをホストする

チームで共有したい場合や、ローカルに Node.js を入れたくない環境では、Container Apps に MCP サーバーをホストしてリモートから接続するパターンが使えます。

```bash
# ⚠️ 外部公開する場合は Azure AD 認証を必ず設定する
az containerapp create \
  --name "playwright-mcp-server" \
  --resource-group "my-rg" \
  --environment "my-aca-env" \
  --image "mcr.microsoft.com/playwright/mcp:latest" \
  --target-port 8931 \
  --ingress internal \
  --command "/app/cli.js" \
  --args "--headless,--browser,chromium,--port,8931,--host,0.0.0.0"
```

MCP クライアント側：

```json
{
  "servers": {
    "playwright": {
      "url": "https://playwright-mcp-server.internal.azurecontainerapps.io/mcp"
    }
  }
}
```

### 認証が必要なページへのアクセス

Azure Portal や社内システムなど認証が必要な場合は、`--storage-state` で事前にセッションを保存しておく方法が使えます。

```bash
# ① Playwright 本体の codegen でログイン状態を保存する
npx playwright codegen --save-storage=./auth.json https://example.com
# → ブラウザが開くので手動でログインし、ウィンドウを閉じると auth.json に保存される

# ② 保存したセッションを使って MCP サーバーを起動
npx @playwright/mcp@latest --storage-state ./auth.json
```

```json
{
  "servers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest", "--storage-state", "./auth.json"]
    }
  }
}
```

:::note alert
🚨 `auth.json` には認証済みクッキーが含まれます。`.gitignore` に追加し、リポジトリにコミットしないようにしてください。CI で使う場合は GitHub Secrets や Azure Key Vault から取得する仕組みにします。
:::

### Azure AI Foundry UI の操作（あくまで考察）

Azure AI Foundry（旧 Azure OpenAI Studio）は JavaScript 多用の SPA なので `#fetch` では取得できませんが、Playwright MCP では操作できます。ただし Azure Portal 系は権限操作と直結しているため、**本番環境への直接操作は推奨しません**。検証するなら Dev 環境 / サンドボックスサブスクリプション限定です。

## セキュリティの注意点

公式ドキュメントに明記されていますが、**Playwright MCP is not a security boundary** です。

具体的に気をつけるべき点：

- `browser_run_code_unsafe` ツールは任意の JavaScript を実行します。本番環境では絶対に使わない
- `--allowed-origins` / `--blocked-origins` はリダイレクトに適用されないため、セキュリティ境界にはなりません
- MCP サーバーをネットワーク公開する場合（`--port` 使用時）は、ファイアウォールまたは Azure AD 認証で保護する
- `secrets` 設定でパスワードフィールドの値をレスポンスから除外できます（`mcp.json` の `env.PLAYWRIGHT_MCP_SECRETS` で指定）

## まとめ

| やりたいこと             | 設定・コマンド                                                                             |
| ------------------------ | ------------------------------------------------------------------------------------------ |
| VS Code に追加           | `code --add-mcp '{"name":"playwright","command":"npx","args":["@playwright/mcp@latest"]}'` |
| ヘッドレスで動かす       | `args` に `"--headless"` を追加                                                            |
| テスト機能を使う         | `"--caps", "testing"` を追加                                                               |
| 認証済みセッションを使う | `"--storage-state", "./auth.json"` を追加                                                  |
| Docker で起動            | `mcr.microsoft.com/playwright/mcp` イメージを使用                                          |
| Container Apps でホスト  | `--ingress internal` で内部専用公開                                                        |

`#fetch` で取れないSPAを操作したい、CIでスモークテストを自動化したい、AIにUIの確認をやらせたい — そういう場面での第一候補として、Playwright MCP は現状かなり有力です。ただし「セキュリティ境界にはならない」という制約を理解したうえで使ってください。

Azure 連携については、Container Apps でのホストと `--storage-state` を組み合わせたパターンがチームで使う際の現実的な落とし所だと考えています。

## 参考

- [microsoft/playwright-mcp — GitHub](https://github.com/microsoft/playwright-mcp)
- [@playwright/mcp — npm](https://www.npmjs.com/package/@playwright/mcp)
- [VS Code MCP サーバードキュメント](https://code.visualstudio.com/docs/copilot/chat/mcp-servers)
- [VS Code 1.99 リリースノート（MCP サポート初搭載）](https://code.visualstudio.com/updates/v1_99)
- [Model Context Protocol 公式サイト](https://modelcontextprotocol.io/)
- [mcr.microsoft.com/playwright/mcp — Microsoft Container Registry](https://mcr.microsoft.com/en-us/artifact/mar/playwright/mcp/about)
