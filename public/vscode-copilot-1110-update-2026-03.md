---
title: VS Code 1.110 + GitHub Copilot 2026年3月アップデートまとめ：エージェント実用化時代が来た
tags:
  - VSCode
  - GitHubCopilot
  - AI
  - 生産性向上
  - アップデート情報
private: false
updated_at: ''
id: null
organization_url_name: null
slide: false
ignorePublish: false
---

## はじめに

2026年3月、VS Code 1.110（February 2026リリース）とGitHub Copilotに立て続けに大型アップデートが入りました。

今回のアップデートを一言で表すなら「**エージェントの実用化**」です。

これまでもCopilot Agentは使えましたが、「長時間・複雑なタスクを安心して任せる」ための仕組みが不十分でした。今回のアップデートで、その土台となる機能が一気に揃っています。

### この記事でわかること

- ✅ VS Code 1.110 で追加された Agent 実用化機能（Lifecycle hooks / SKILL.md / Session memory など）
- ✅ GPT-5.4 GA や Copilot コードレビューのアーキテクチャ刷新など Copilot 側の変更点
- ✅ Figma MCP 双方向連携・Jira 連携など、周辺エコシステムの拡張
- ✅ 実際の使い方イメージとエンジニアへの影響

### 対象読者

VS Code と GitHub Copilot を日常業務で使っている中級者エンジニアを想定しています。

---

## VS Code 1.110 の主要変更点

公式ブログ「[Making agents practical for real-world development](https://code.visualstudio.com/blogs/2026/03/05/making-agents-practical-for-real-world-development)」というタイトルが示すとおり、今回のテーマはエージェントを実際の開発で使えるものにすることです。

### 1. Lifecycle Hooks

エージェントの**開始・終了タイミングに処理を差し込める**仕組みです。

たとえば「エージェントが作業を開始する前に、最新の `main` ブランチを必ず pull してほしい」「作業終了後に自動でテストを走らせてほしい」といったユースケースに対応できます。

```yaml
# .github/agents/my-agent.agent.md のフロントマター例
lifecycle:
  onStart: |
    git pull origin main
  onFinish: |
    npm test
```

これにより、エージェントに任せた処理が「前後の文脈を無視した暴走」になるリスクを減らせます。

### 2. Agent Skills（SKILL.md）

`.github/skills/<skill-name>/SKILL.md` に置いた手順書をエージェントに組み込める機能です。

**「この手順書を読んでその通りにやってくれ」をファイルとして管理できる**ようになりました。

```
.github/
└── skills/
    └── deploy-to-staging/
        └── SKILL.md   ← デプロイ手順を記述
```

```markdown
<!-- SKILL.md の例 -->
# Deploy to Staging

## 手順

1. `npm run build` を実行する
2. `docker build -t myapp:staging .` でイメージをビルドする
3. `docker push myregistry/myapp:staging` でプッシュする
4. `kubectl rollout restart deployment/myapp -n staging` でデプロイを反映する

## 確認事項

- デプロイ後、`/health` エンドポイントが 200 を返すことを確認する
```

エージェントに `#skill:deploy-to-staging` と指定するだけで、この手順を自動実行してもらえます。反復する複雑な手順の標準化に有用です。

### 3. Session Memory

会話をまたいでエージェントが記憶を保持できる仕組みです。

従来はセッションを閉じると文脈がリセットされていましたが、Session Memory を使うことで「先週話した設計方針」「プロジェクト固有の制約事項」などを次回以降の会話にも引き継げます。

```markdown
<!-- /memories/session/current-task.md の例 -->
## 現在のタスク
- 機能: ユーザー認証モジュールのリファクタリング
- 方針: JWT から session-based に移行（理由: マイクロサービス間の負荷分散のため）
- 注意: 既存の `/api/v1/auth` エンドポイントの後方互換性を維持すること
```

### 4. 統合ブラウザツール

エージェントが**ブラウザを直接操作**できるようになりました。

「このページの最新ドキュメントを確認してコードを修正してくれ」「このURLのAPIレスポンスを確認してテストを書いてくれ」といった指示がそのまま実行できます。エージェントが途中でブラウザ操作を必要とするタスクの自動化範囲が大幅に広がります。

### VS Code 1.110.1（バグ修正版）

1.110 リリース直後に発見されたバグへの修正版として、**2026-03-07 に 1.110.1 がリリース**されました。1.110 を使っている場合は 1.110.1 への更新が推奨されます。

詳細は [公式リリースノート](https://code.visualstudio.com/updates/v1_110) を参照してください。

---

## GitHub Copilot 側の主要アップデート

### GPT-5.4 が Copilot で GA

OpenAI の最新エージェント特化モデル **GPT-5.4 が一般提供（GA）** になりました。

コーディングエージェント系タスク（複数ファイルにわたるリファクタリング、テスト生成、PR レビューなど）で精度が大幅に向上しているとされています。Copilot Pro・Business・Enterprise の全プランで利用可能です。

> 参考: [GPT-5.4 is generally available in GitHub Copilot](https://github.blog/changelog/2026-03-05-gpt-5-4-is-generally-available-in-github-copilot)

### Copilot コードレビューがエージェントアーキテクチャに刷新

Copilot のコードレビュー機能が **tool-calling 型のエージェントアーキテクチャに全面移行**しました。

従来はプロンプト→回答の1ショット型でしたが、エージェント型になることで「コードを読む→関連ファイルを調べる→コンテキストを理解した上でレビューする」という人間に近い手順でレビューできるようになっています。

Pro・Pro+・Business・Enterprise の全プランで GA です。

> 参考: [Copilot code review now runs on an agentic architecture](https://github.blog/changelog/2026-03-05-copilot-code-review-now-runs-on-an-agentic-architecture)

### Next Edit Suggestions がファイル全体に拡張

以前は**近くの行への編集提案**しかできなかった Next Edit Suggestions が、**ファイル全体を対象**にした提案に拡張されました。

たとえば関数の引数の型を変更したとき、そのファイル内の全ての呼び出し箇所にまとめて修正提案が表示されるようになります。

```typescript
// 例: 引数の型を number → string に変更したとき
function formatId(id: string): string {
  return `ID-${id}`;
}

// ファイル内の他の呼び出し箇所にも提案が出るようになった
const result1 = formatId(42);   // ← string に直すよう提案
const result2 = formatId(100);  // ← string に直すよう提案（離れた行でも）
```

> 参考: [Long-distance Next Edit Suggestions](https://code.visualstudio.com/blogs/2026/02/26/long-distance-nes)

### PRコメントでモデルを選択可能に

`@copilot` メンションを使った PR コメントで、**使用モデルを直接指定**できるようになりました。

```
@copilot [model: gpt-5.4] このPRのパフォーマンス面でのリスクをレビューしてください
```

タスクの性質に合わせてモデルを使い分けることで、速度とコストのバランスを取れます。

> 参考: [Pick a model for Copilot in pull request comments](https://github.blog/changelog/2026-03-05-pick-a-model-for-copilot-in-pull-request-comments)

---

## 周辺エコシステムのアップデート

### Figma MCP サーバーが VS Code と双方向連携

Figma MCP サーバーのアップデートで、**コード → Figma 方向のデザイン生成**が可能になりました。

| 方向 | できること |
|------|-----------|
| Figma → コード（従来） | Figmaのデザインを参照してコードを生成 |
| コード → Figma（新機能） | VS Code で作ったUIをFigmaに「編集可能なフレーム」として書き出し |

デザイナーとエンジニアが「Figmaに戻って修正」「コードに反映」を繰り返すループが VS Code + Figma MCP で自動化できるようになります。

> 参考: [Figma MCP server can now generate design layers from VS Code](https://github.blog/changelog/2026-03-06-figma-mcp-server-can-now-generate-design-layers-from-vs-code)

### エージェントセッションへの画像追加

GitHub.com のエージェントセッションで、**スクリーンショットをペースト・ドラッグ&ドロップでエージェントに渡せる**ようになりました。

「このUIのバグを直してほしい（スクリーンショット添付）」「このエラー画面を見てもらえますか（画面キャプチャ添付）」という使い方が直感的にできます。

> 参考: [Add images to agent sessions](https://github.blog/changelog/2026-03-05-add-images-to-agent-sessions)

### Copilot Coding Agent が Jira 連携（Public Preview）

**Jira の issue を Copilot に割り当てると、自動で PR を作成してくれる**機能が Public Preview になりました。

```
Jira Issue: PROJ-1234 「ログイン画面にパスワード強度インジケーターを追加」
     ↓ Copilotに割り当て
GitHub PR: 「feat: add password strength indicator to login form」を自動作成
```

バックログのタスクを Jira で管理している場合、コーディングエージェントとの連携が大幅に楽になります。

> 参考: [GitHub Copilot coding agent for Jira is now in public preview](https://github.blog/changelog/2026-03-05-github-copilot-coding-agent-for-jira-is-now-in-public-preview)

### Grok Code Fast 1 が Copilot Free に追加

xAI の高速モデル **Grok Code Fast 1** が、Copilot Free プランの auto model selection に追加されました。無料プランでも高速レスポンスのモデルが使えるようになっています。

> 参考: [Grok Code Fast 1 is now available in Copilot Free auto model selection](https://github.blog/changelog/2026-03-04-grok-code-fast-1-is-now-available-in-copilot-free-auto-model-selection)

---

## エンジニアへの影響まとめ

今回のアップデートで何が変わるのか、実務目線で整理します。

| 変化 | 実現する機能 |
|------|-------------|
| **エージェントに長時間タスクを任せやすくなった** | Lifecycle Hooks でエージェントの前後処理を制御 + Session Memory で文脈を維持 |
| **手順書をエージェントに丸ごと覚えさせられる** | SKILL.md でデプロイ・テスト・レビュー手順を外部化 |
| **コードレビューの質が上がった** | エージェント型アーキテクチャ + GPT-5.4 の精度向上 |
| **デザイン⇔コードのループが自動化できる** | Figma MCP の双方向連携 |
| **Jiraタスクの消化を自動化できる** | Copilot Coding Agent の Jira 連携 |
| **ファイル全体への一括修正提案** | Next Edit Suggestions の全ファイル対応 |

---

## まとめ

VS Code 1.110 と 2026年3月の GitHub Copilot アップデートは、「エージェントを実際の開発で使い物にする」という明確な方向性でまとまっています。

特に **Lifecycle Hooks + SKILL.md + Session Memory** の組み合わせは、これまで「なんとなく怖くてエージェントに任せられなかった」タスクの自動化を現実的にする変化です。

一方で、Figma MCP の双方向連携や Jira 連携など周辺エコシステムとの統合も進んでおり、「VS Code を中心にした開発ループ」がさらに完結していく流れを感じます。

今後のアップデートにも注目していきましょう。

---

## 参考

- [VS Code 1.110 リリースノート](https://code.visualstudio.com/updates/v1_110)
- [Making agents practical for real-world development（VS Code Blog）](https://code.visualstudio.com/blogs/2026/03/05/making-agents-practical-for-real-world-development)
- [GitHub Copilot Changelog](https://github.blog/changelog/label/copilot/)
- [GPT-5.4 is generally available in GitHub Copilot](https://github.blog/changelog/2026-03-05-gpt-5-4-is-generally-available-in-github-copilot)
- [Copilot code review now runs on an agentic architecture](https://github.blog/changelog/2026-03-05-copilot-code-review-now-runs-on-an-agentic-architecture)
- [Figma MCP server can now generate design layers from VS Code](https://github.blog/changelog/2026-03-06-figma-mcp-server-can-now-generate-design-layers-from-vs-code)
- [Long-distance Next Edit Suggestions](https://code.visualstudio.com/blogs/2026/02/26/long-distance-nes)
- [GitHub Copilot coding agent for Jira is now in public preview](https://github.blog/changelog/2026-03-05-github-copilot-coding-agent-for-jira-is-now-in-public-preview)
