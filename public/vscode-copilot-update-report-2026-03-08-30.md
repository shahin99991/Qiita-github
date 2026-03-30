---
title: "GitHub Copilot / VS Code 更新レポート（2026年3月版）"
tags:
  - GitHubCopilot
  - VSCode
  - アップデート情報
  - 生成AI
  - 開発生産性
private: false
updated_at: ''
id: null
organization_url_name: null
slide: false
ignorePublish: false
---

## はじめに

この記事は、2026年3月に観測された GitHub Copilot / VS Code の更新を、
**レポート形式（時系列・URL中心）**でまとめたものです。

解説や提言は最小限にし、まず全体像を短時間で把握できるように整理しています。

対象読者:

- 更新の事実を先に把握したい人
- チーム展開前に変更点を俯瞰したい人
- 詳細解説記事を読む前に要点をつかみたい人

## 主要更新（時系列）

### 2026-03-08

- VS Code 1.110.1 リリース
- Copilot in VS Code v1.110（Febリリース関連）
- GPT-5.4 GA
- Figma MCP の VS Code 連携強化
- Agent session への画像追加

### 2026-03-10

- VS Code 1.111.0 リリース

### 2026-03-12〜03-14

- GitHub CLI から Copilot code review 要求
- JetBrains で agentic capabilities 強化
- Web 上での repository 探索機能
- JetBrains で auto model selection GA
- Actions ワークフロー承認スキップ（任意）
- 学生向け Copilot 更新

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

### 2026-03-24〜03-27

- PR 変更依頼を Copilot に指示
- repository access 管理 API
- Jira 連携強化
- active coding agent user 識別メトリクス
- VS Code 1.113.0 リリース
- Gemini 3 Pro 廃止案内
- プライバシー規約/利用規約の更新
- PR マージコンフリクト解消支援

## 影響の要点（短縮版）

- 補完中心から、PR/CI/運用メトリクスを含む agent 活用へ比重が移動
- 速度改善と可視性向上により、チーム導入時の説明可能性が上がる
- モデル提供の更新が早いため、運用側は「バージョン/モデル/権限」をセット管理する必要がある

## 関連リンク

### 公式まとめページ

- VS Code Releases: https://github.com/microsoft/vscode/releases
- VS Code Updates: https://code.visualstudio.com/updates/
- Copilot Changelog Label: https://github.blog/changelog/label/copilot/

## まとめ

2026年3月後半は、単なる新機能追加よりも、
**「Copilotを開発プロセスに組み込むための更新」が連続した期間**でした。

先に本記事で全体像を押さえ、必要に応じて詳細解説記事を読むと追いやすくなります。
