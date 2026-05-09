---
name: commit-message
description: "Conventional Commitsに従ったコミットメッセージを対話形式で生成する。USE FOR: コミットメッセージを書く、コミット文を作る、git commitのメッセージ、コミット内容をまとめる。DO NOT USE FOR: PRの説明文、リリースノートの作成。"
argument-hint: '変更内容を簡単に説明してください（例: "ログイン機能を追加"、"決済バグを修正"）'
---

# コミットメッセージ生成スキル

## 目的

Conventional Commits仕様に従ったコミットメッセージを、対話形式で収集した情報をもとに生成します。

## Step 1: ユーザー入力

このスキルが呼び出されたら、以下をユーザーに **1つずつ** 確認する：

1. **変更タイプ** — `feat`（新機能）/ `fix`（バグ修正）/ `docs`（ドキュメント）/ `refactor` / `test` / `chore`（デフォルト: `feat`）

2. **スコープ**（省略可）— 変更が影響するモジュール名（例: `auth`, `api`, `ui`）

3. **破壊的変更の有無** — `あり` または `なし`

## Step 2: 出力

受け取った情報をもとに以下のフォーマットで出力する：

```
<type>(<scope>): <description>

[body: 変更の背景や詳細。argument-hint の内容をもとに補完する。省略可]

[footer: BREAKING CHANGE または Refs: #issue番号。省略可]
```

**制約**:

- `description` は50文字以内・命令形・現在形（「追加した」→「追加」）
- 日本語・英語どちらでも対応（argument-hint と同じ言語に揃える）
- 破壊的変更がある場合は footer に `BREAKING CHANGE: <説明>` を必ず含める

## 出力例

```
feat(auth): JWTを使ったログイン機能を追加

ユーザー認証にJWT（JSON Web Token）を採用。
アクセストークンの有効期限は24時間、リフレッシュトークンは30日。

Refs: #123
```
