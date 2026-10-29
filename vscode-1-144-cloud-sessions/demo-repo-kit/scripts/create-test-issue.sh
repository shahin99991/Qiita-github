#!/usr/bin/env bash
# Issue トリガーのデモ用: 再現手順が足りない Issue を1件立てる。実行した瞬間に Automation が発火する。
# 先に Automation を保存して Enabled にしてから実行すること。
set -euo pipefail

REPO="${REPO:-YJK-Inc/Test-Repo}"

gh issue create --repo "$REPO" \
  --title "在庫を登録すると動かない" \
  --label automation-test \
  --body "動きません。"
