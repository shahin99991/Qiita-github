---
title: GitHub Copilot / VS Code 更新レポート（2026年3月版）
tags:
  - VSCode
  - GitHubCopilot
  - 生成AI
  - 開発生産性
  - アップデート情報
private: false
updated_at: '2026-03-30T23:15:29+09:00'
id: 6a1dcbc7f6e075900d0a
organization_url_name: null
slide: false
ignorePublish: true
---

## はじめに

この記事は、2026年3月に公開された GitHub Copilot / VS Code 関連の更新を、
**時系列と出典URL中心**で整理したレポートです。

対象は、日々の開発で Copilot を利用し、チーム展開前に変更点を素早く把握したい中級者エンジニアです。

観測条件:

- 観測期間: 2026/03/08-2026/03/30
- 主な参照元: GitHub Copilot Changelog / VS Code Releases / VS Code Updates
- 抽出基準: Copilot・VS Code・Agent運用に関係する公開更新

## 本文

### 主要更新（時系列）

### 2026-03-08

- VS Code 1.110.1 リリース
- Copilot in VS Code v1.110（Febリリース関連）
- GPT-5.4 GA
- Figma MCP の VS Code 連携強化
- Agent session への画像追加
- 実務での確認ポイント: VS Code/Copilot の更新タイミングをそろえ、拡張機能の互換性を先に確認する。
- 主な出典: [VS Code 1.110.1](https://github.com/microsoft/vscode/releases/tag/1.110.1), [GPT-5.4 is generally available in GitHub Copilot](https://github.blog/changelog/2026-03-05-gpt-5-4-is-generally-available-in-github-copilot)

### 2026-03-10

- VS Code 1.111.0 リリース
- 実務での確認ポイント: チーム標準環境の VS Code バージョン更新手順を明文化する。
- 主な出典: [VS Code 1.111.0](https://github.com/microsoft/vscode/releases/tag/1.111.0)

### 2026-03-12〜03-14

- GitHub CLI から Copilot code review 要求
- JetBrains で agentic capabilities 強化
- Web 上での repository 探索機能
- JetBrains で auto model selection GA
- Actions ワークフロー承認スキップ（任意）
- 学生向け Copilot 更新
- 実務での確認ポイント: CLI・IDE・Web のどこから Copilot を使うかを運用ガイドに分けて定義する。
- 主な出典: [Request Copilot code review from GitHub CLI](https://github.blog/changelog/2026-03-11-request-copilot-code-review-from-github-cli), [Optionally skip approval for Copilot coding agent Actions workflows](https://github.blog/changelog/2026-03-13-optionally-skip-approval-for-copilot-coding-agent-actions-workflows)

### 2026-03-18〜03-21

- semantic code search による coding agent 高速化
- GPT-5.4 mini GA
- VS Code 1.112.0 リリース
- validation tools 構成の更新
- GPT-5.3-Codex LTS
- coding agent 起動 50% 高速化
- セッション可視性向上
- コミットとセッションログの追跡
- Raycast でのライブ監視
- auto model selection の実モデル解決
- 実務での確認ポイント: 速度改善の体感だけでなく、ログ追跡の手順を定義して再現性を高める。
- 主な出典: [Copilot coding agent now starts work 50% faster](https://github.blog/changelog/2026-03-19-copilot-coding-agent-now-starts-work-50-faster), [VS Code 1.112.0](https://github.com/microsoft/vscode/releases/tag/1.112.0)

### 2026-03-24〜03-27

- PR 変更依頼を Copilot に指示
- repository access 管理 API
- Jira 連携強化
- active coding agent user 識別メトリクス
- VS Code 1.113.0 リリース
- Gemini 3 Pro 廃止案内
- プライバシー規約/利用規約の更新
- PR マージコンフリクト解消支援
- 実務での確認ポイント: 権限設定・監査ログ・モデル移行の3点をセットで見直す。
- 主な出典: [Ask Copilot to make changes to any pull request](https://github.blog/changelog/2026-03-24-ask-copilot-to-make-changes-to-any-pull-request), [VS Code 1.113.0](https://github.com/microsoft/vscode/releases/tag/1.113.0)

### 影響の要点

- 補完中心から、PR/CI/運用メトリクスを含む agent 活用へ比重が移っている。
- 速度改善と可視性向上により、チーム導入時の説明可能性が上がる可能性がある。
- モデル提供の更新が早いため、「バージョン/モデル/権限」をセットで管理する検討が必要。

## まとめ

2026年3月の更新は、単なる新機能追加だけでなく、
Copilot を開発プロセスに組み込むための運用要素が強化された期間でした。

まずは本記事で全体像を押さえ、必要に応じて個別テーマを深掘りすると追いやすくなります。

## 参考

- [VS Code Releases](https://github.com/microsoft/vscode/releases)
- [VS Code Updates](https://code.visualstudio.com/updates/)
- [GitHub Copilot Changelog](https://github.blog/changelog/label/copilot/)
