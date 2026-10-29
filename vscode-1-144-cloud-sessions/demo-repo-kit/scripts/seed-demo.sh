#!/usr/bin/env bash
# Cloud Automations デモ用: ラベル作成と、直近にマージされた PR を3件作る。
# 事前に `gh auth login` 済みで、対象リポジトリの write 権限があること。
set -euo pipefail

REPO="${REPO:-YJK-Inc/Test-Repo}"

gh label create automation-test --repo "$REPO" --color 0E8A16 \
  --description "Cloud Automation のテスト用" 2>/dev/null || true

git checkout main
git pull --ff-only

for n in 1 2 3; do
  branch="demo/changelog-$n"
  git checkout -b "$branch" main
  mkdir -p docs
  echo "- デモ用の変更 $n ($(date +%F))" >> docs/changelog.md
  git add docs/changelog.md
  git commit -m "docs: changelog にデモ用の変更 $n を追加"
  git push -u origin "$branch"
  gh pr create --repo "$REPO" --base main --head "$branch" \
    --title "docs: changelog にデモ用の変更 $n を追加" \
    --body "Cloud Automations デモ用の PR です。"
  gh pr merge --repo "$REPO" "$branch" --squash --delete-branch
  git checkout main
  git pull --ff-only
done
