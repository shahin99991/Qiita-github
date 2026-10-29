# YJK-Inc/Test-Repo デモ用キット（VS Code 1.144 記事用）

`YJK-Inc/Test-Repo`（private）に追加して、Cloud セッションと Cloud Automations のデモを撮るためのファイルです。既存の `app/` や `README.md` は変更しません。

## 追加されるもの

| ファイル                               | 目的                                                                       |
| -------------------------------------- | -------------------------------------------------------------------------- |
| `docs/setup.md`                        | 実行コマンドが古い（`python main.py`。実際は `python app/main.py`）        |
| `docs/known-issues.md`                 | 修正済みの `ZeroDivisionError` が未解決のまま。関数名も古い                |
| `docs/ci.md`                           | 「CI は失敗する」と書いてあるが、不具合は直っている                        |
| `.github/ISSUE_TEMPLATE/bug_report.md` | Issue トリガーのデモで、再現手順の有無を確認する土台                       |
| `scripts/seed-demo.sh`                 | `automation-test` ラベルと、マージ済み PR 3件を作る（Weekly 要約のデモ用） |
| `scripts/create-test-issue.sh`         | 再現手順のない Issue を1件立てて、Issue トリガーを発火させる               |

`docs/` の「古い記述」は、Cloud セッションのデモ（「README と docs の古い箇所を3つ挙げて」）で見つけてもらう想定です。

## 手順

```bash
git clone https://github.com/YJK-Inc/Test-Repo.git
cd Test-Repo
git checkout -b demo/vscode-1-144-kit

# このキットの docs/ .github/ scripts/ をリポジトリ直下にコピーする
cp -r /path/to/vscode-1-144-cloud-sessions/demo-repo-kit/{docs,.github,scripts} .
chmod +x scripts/*.sh

git add docs .github scripts
git commit -m "docs: VS Code 1.144 デモ用の資料とスクリプトを追加"
git push -u origin demo/vscode-1-144-kit
gh pr create --base main --title "docs: VS Code 1.144 デモ用の資料とスクリプトを追加" --body "デモ用です。"
gh pr merge --squash --delete-branch
git checkout main && git pull --ff-only

./scripts/seed-demo.sh            # ラベル + マージ済み PR 3件
```

`docs/` が既にある場合は、同名ファイルがないか先に確認してください。

## デモ中の使い方

- **Cloud セッション（demo-02〜05）**: 「README と docs を読んで、古くなっていそうな箇所を3つ挙げて」と頼みます。`docs/setup.md`、`docs/known-issues.md`、`docs/ci.md` が見つかる想定です。
- **Weekly 要約（demo-07〜08）**: Manual で Run now → 直近7日のマージ済み PR（seed の3件 + 既存 PR）が要約されます。
- **Issue トリガー（demo-09〜10）**: Automation を保存して Enabled にしたあと、`./scripts/create-test-issue.sh` を実行します。

## 片付け

```bash
gh issue close <番号> --repo YJK-Inc/Test-Repo
# Automation は Agents ウィンドウの Automations から Disable / Delete
```
