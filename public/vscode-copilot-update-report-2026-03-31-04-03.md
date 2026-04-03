---
title: GitHub Copilot / VS Code 更新まとめ（2026/03/30-04/03）
tags:
  - VSCode
  - ソフトウェア開発
  - GitHubCopilot
  - 生成AI
  - 開発生産性
private: false
updated_at: '2026-04-03T15:59:10+09:00'
id: 0d83c8d5149b9ff55702
organization_url_name: null
slide: false
ignorePublish: false
---

## はじめに

2026/03/30-04/03 に公開された GitHub Copilot / VS Code 関連の更新を、実務への影響に絞って整理します。

対象は、チーム開発で Copilot を継続運用しているエンジニアです。想定読了は約10分です。

## 本文

### 全体像: 単発機能より「運用可能な基盤」の拡張

今回の更新は、単体の便利機能追加だけではありません。次の4つが同時に進んだ点が特徴です。

- モデル運用（廃止予定と代替準備）
- IDE/クライアント更新（VS Code / Mobile / Visual Studio）
- 組織管理（Organization custom instructions と利用可視化）
- 組み込み基盤（Copilot cloud agent と Copilot SDK）

本記事では、Copilot cloud agent（旧称 Copilot coding agent）、Copilot SDK、
Organization custom instructions（以下 org instructions）という表記で統一します。

### 主要アップデート

#### 1. 開発フローとの接続が強化

- Create issues from Slack with Copilot
  - Slack 上の会話から Issue 起票につなげやすくなり、起票の入口を統一しやすくなります。
- Research, plan, and code with Copilot cloud agent
  - 調査・計画・実装まで含めたエージェント利用が進み、PR補助に閉じない活用設計が取りやすくなります。
- Copilot SDK in public preview
  - 内製ツールや既存ワークフローに Copilot 機能を組み込む選択肢が広がりました。
  - Public Preview のため、仕様変更の可能性を前提に小さく検証する運用が有効です。

#### 2. モデル運用の見直しポイントが明確化

- Upcoming deprecation of Claude Sonnet 4 in GitHub Copilot
  - モデル固定運用のチームは、代替モデルの選定と検証を計画化する必要があります。
- GPT-5.4 mini in Copilot Student auto model selection
  - 自動モデル選択の更新が進んでおり、モデル選択を「個人設定任せ」にしない運用設計が有効です。

#### 3. IDE/クライアント側の運用範囲が拡大

- VS Code 1.114.0 リリース
  - Copilot を日常利用するなら、拡張機能と設定を含めたアップデート検証の継続が有効です。
- GitHub Mobile: refreshed Copilot tab and native session logs
  - モバイルでもセッション確認がしやすくなり、レビューやトリアージの参加経路が増えます。
- GitHub Mobile: faster agent assignment from issues
  - 課題からのエージェント割り当てが素早くなり、外出先でも作業委任しやすくなります。
- GitHub Copilot in Visual Studio - March update
  - VS Code 以外の IDE でも機能拡張が続き、開発環境の違いをまたいだ運用がしやすくなっています。

#### 4. 組織導入に必要な管理機能が前進

- Copilot organization custom instructions are generally available
  - 組織単位での指示標準化がしやすくなり、回答品質のばらつきを抑えやすくなります。
  - 利用には対象プランと管理者権限が必要なため、導入前に権限設計を確認するのが安全です。
- per-user Copilot CLI activity in organization reports
  - 使われ方をユーザー単位で把握しやすくなり、ガイドライン改善の根拠を作りやすくなります。

### エンジニア向けの実務アクション

組織ポリシー・監査要件・プライバシー方針に合わせて、次の順で進めると運用しやすくなります。

1. モデル依存を棚卸しし、廃止予定モデルの代替候補と切替条件を明文化する。
2. Organization custom instructions（org instructions）を作成し、レビュー観点や禁止事項を最初に固定する。
3. per-user の活動データを週次で確認し、使われていない機能の教育対象を決める。
4. Copilot cloud agent か Copilot SDK のどちらか1つに絞って、小さな業務フローで PoC を回す。

## まとめ

3/30-4/3の更新は、便利機能の追加というより、Copilot を開発基盤として運用するための要素の強化が進んだ期間でした。

- モデル移行計画を先に作る
- org instructions と利用可視化をセットで回す
- Copilot cloud agent / Copilot SDK を小さく試して適用範囲を決める

この3点を並行して進めると、導入の速度と統制のバランスを取りやすくなります。

## 参考

- 2026-03-30 / Create issues from Slack with Copilot: https://github.blog/changelog/2026-03-30-create-issues-from-slack-with-copilot
- 2026-03-31 / Upcoming deprecation of Claude Sonnet 4 in GitHub Copilot: https://github.blog/changelog/2026-03-31-upcoming-deprecation-of-claude-sonnet-4-in-github-copilot
- 2026-04-01 / VS Code 1.114.0: https://github.com/microsoft/vscode/releases/tag/1.114.0
- 2026-04-01 / Research, plan, and code with Copilot cloud agent: https://github.blog/changelog/2026-04-01-research-plan-and-code-with-copilot-cloud-agent
- 2026-04-01 / GPT-5.4 mini is now available in Copilot Student auto model selection: https://github.blog/changelog/2026-04-01-gpt-5-4-mini-is-now-available-in-copilot-student-auto-model-selection
- 2026-04-01 / GitHub Mobile: Stay in flow with a refreshed Copilot tab and native session logs: https://github.blog/changelog/2026-04-01-github-mobile-stay-in-flow-with-a-refreshed-copilot-tab-and-native-session-logs
- 2026-04-01 / GitHub Mobile: Faster, more flexible agent assignment from issues: https://github.blog/changelog/2026-04-01-github-mobile-faster-more-flexible-agent-assignment-from-issues
- 2026-04-02 / Copilot SDK in public preview: https://github.blog/changelog/2026-04-02-copilot-sdk-in-public-preview
- 2026-04-02 / Copilot usage metrics now includes per-user GitHub Copilot CLI activity in organization reports: https://github.blog/changelog/2026-04-02-copilot-usage-metrics-now-includes-per-user-github-copilot-cli-activity-in-organization-reports
- 2026-04-02 / GitHub Copilot in Visual Studio - March update: https://github.blog/changelog/2026-04-02-github-copilot-in-visual-studio-march-update
- 2026-04-02 / Copilot organization custom instructions are generally available: https://github.blog/changelog/2026-04-02-copilot-organization-custom-instructions-are-generally-available
