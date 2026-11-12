# デモ手順 & スクショ一覧

「VS Code の Local harness は2027年2月に削除：Copilot harness へ移行する手順とつまずきポイント」記事用の、デモ手順と画像の一覧です。

- 記事本体: [article-qiita.md](./article-qiita.md)
- レビュー用プレビュー: [article-preview.md](./article-preview.md)
- **デモ用リポジトリ（再検証用・最新）**: https://github.com/YJK-Inc/Qiita-harness-demo2 （Internal。中身はすべてダミー）
- 初回の撮影に使ったリポジトリ: https://github.com/YJK-Inc/Qiita-github-harness-demo
- 画像保存先: `./images/`
- 画像URL形式: `https://raw.githubusercontent.com/shahin99991/Qiita-github/main/vscode-local-harness-deprecation/images/<ファイル名>`
- 差し替え方法: 同名で `./images/` に上書き → push（記事側の URL 変更は不要）
- 元のスクショ（赤枠つき・撮影時のファイル名）は `./images/_original/` に退避済み（`.gitignore` 済みで push されない）

> ⚠️ **公開前の注意**: 画像を GitHub に push するまで raw URL は 404 になります。記事の `ignorePublish: true` は、画像を push して、下の「追試」を終えてから `false` にしてください。

---

## 1. 撮影環境

- Windows / VS Code **1.145.3**（Policy Diagnostics の Product 表示）
- デモ用リポジトリを `harness-migration-demo` ブランチで開いて撮影
- 赤枠は撮影時に入れたもの

## 2. 記事で使っている画像

### 実機スクリーンショット

| ファイル | 記事内の位置 | 元のスクショ | 写っているもの |
| -------- | ------------ | ------------ | -------------- |
| `demo-01-harness-title-prefix` | 2. 確認 | 154632 + 155759 を合成 | チャットタイトルの接頭辞（左: `Local ·` / 右: `Copilot ·`） |
| `demo-02-session-target-picker` | 2. 確認 | 153333 | Session Target で Copilot にホバー |
| `demo-02b-session-target-local` | 2. 確認 | 153343 | Session Target で Local にホバー |
| `demo-03-open-customizations-button` | 3. 移行画面の開き方 | 153447 | チャット右上の Customizations ボタンとセッション一覧 |
| `demo-03b-mcp-migration-available` | 3. 移行画面の開き方 | 153457 | MCP Servers の「Migration available」と Migrations（9） |
| `demo-04-migrations-tree` | 3. 移行画面の開き方 | 153526 | Migrations 画面（グループ一覧） |
| `demo-05-mcp-migrate` | 3. MCP | 153618 | 「Migrate 2 MCP servers to .mcp.json?」ダイアログ |
| `demo-05b-mcp-migrated` | 3. MCP | 153631 | 「Migrated 2 MCP servers.」と Needs manual review |
| `demo-05c-mcp-manual-review` | 3. MCP | 153735 | 「Not supported by Copilot」の詳細 |
| `demo-06-prompt-to-skill` | 3. プロンプト → スキル | 153951 | 変換ダイアログ（元ファイル削除が既定でオン） |
| `demo-06b-prompt-converted-toast` | 3. プロンプト → スキル | 154004 | 変換後の通知（mode, model, tools） |
| `demo-06c-skill-md` | 3. プロンプト → スキル | 154103 | 生成された `SKILL.md` |
| `demo-07-custom-location-migrate` | 3. 探索場所 | 154434 | 探索場所の移行ダイアログ |
| `demo-07b-custom-location-result` | 3. 探索場所 | 154533 | 移行後の Source Control |
| `demo-11-hook-denied-copilot` | （記事では未使用。フック節は公式情報のみ） | 154823 | Copilot で preToolUse フックが拒否 |
| `demo-11b-hook-errored` | （記事では未使用。フック節は公式情報のみ） | 155759 | 保護対象外のスクリプトの読み込みまで拒否 |
| `demo-12-hook-blocks-skill` | （記事では未使用。フック節は公式情報のみ） | 161642（パンくずのユーザー名を塗りつぶし） | `git status` / `git diff` まで拒否され、`/code-review` を実行できなかった |
| `demo-08-handoff-local-to-copilot` | 4. Local の会話を続ける | 154729 | Continue In → Copilot |
| `demo-08b-after-handoff` | 4. Local の会話を続ける | 154740 | 引き継ぎ後 |
| `demo-09b-skill-slash-menu` | 5. 動作確認 | 155930 | `/code-review` の補完 |
| `demo-09-verify-skill-run` | 5. 動作確認 | 160240 | `/code-review` の実行結果 |
| `demo-10-policy-diagnostics` | 6. 組織の管理者向け | 160337 を上部だけ切り抜き | Policy Diagnostics の Summary と System Information |

※ 元のスクショ名は `スクリーンショット 2026-11-12 HHMMSS.png` の時刻部分。

### 生成画像（GPT Image 2.5）

| ファイル | 記事内の位置 |
| -------- | ------------ |
| `img-00-tldr-overview` | TL;DR |
| `img-01-timeline` | 1. タイムライン |
| `img-02-migration-map` | 3. 移行マップ |
| `img-03-personal-vs-org` | 6. 組織の管理者向け |

### 記事に使っていない元スクショ

152554（Local セッションでの質問入力）、153605・153914・154426（Migrate ボタンの赤枠）、153719・153800・153822（Review の画面と元の `mcp.json`）、154053・154520（Source Control の差分）、154632（Local セッションの返答）、155541・155554（`production.json` の編集前後）、160328（コマンドパレット）、160350（Policy Diagnostics の中盤）。

---

## 3. 追試（公開前にやること）

### 3-1. フックの検証（Qiita-harness-demo2 で再検証）

**初回の確認済み事項（2026-11-12 / VS Code 1.145.3）**: Local 形式のフックは Copilot のセッションでも発火する。エラー（`hook errored`）で `git status` / `git diff` や `/code-review` まで拒否され、**フックのファイルを削除したらスキルを実行できた**（`demo-12-hook-blocks-skill`）。

**未確認**: エラーの原因（`python3` が Windows にない / `cwd` の違い）と、書き直し版が動くか。VS Code を更新したので、`Qiita-harness-demo2` で原因を切り分ける。

`hooks-lab/guard.py` は動作を `hooks-lab/logs/hook.log` に記録するので、**ログが残るか**で「コマンドが起動できていない」のか「出力形式の問題」なのかを分けられます。

1. セットアップは [README](https://github.com/YJK-Inc/Qiita-harness-demo2#セットアップwindows--powershell) のとおり（クローン → 作業ブランチ → `code .`）
2. `.\hooks-lab\check-guard.ps1` で、`python` / `python3` / `py` が使えるかと、単体の出力を確認する
   - **`[python3]` が見つからないか**を控える（原因の有力候補）
3. パターンを A → B → C の順に配置して、それぞれ新しい Copilot セッションで試す

   | パターン | 試すこと | 記録する結果 |
   | -------- | -------- | ------------ |
   | A（`command: python3` のみ） | `src/app.py` を要約 / `git status` / `/code-review` | 拒否されるか。`hook.log` が残るか |
   | B（`bash` / `powershell` / `cwd`） | 同上 + `config/production.json` の `debug` を `true` に | 保護対象だけ拒否され、他は通るか |
   | C（Copilot 形式） | 同上 | 同上 |

4. 結果を次の表に沿って記事に反映する

   | 結果 | 記事の直し方 |
   | ---- | ------------ |
   | A でエラー、`hook.log` なし。B・C は動く | 原因を「`python3` が Windows にない（または `cwd`）」と確定させ、「と考えています」を削る。B / C の動作確認済みを明記 |
   | A でも動く（`hook.log` あり） | 前回のエラーは別原因。`hook.log` の内容で原因を書き直す |
   | B・C でもエラー | `hook.log` の有無と内容を載せて、未解決として書く |

5. 動いたパターンで、拒否された画面（`config/production.json`）を撮り直して `demo-11-hook-denied-copilot.png` に差し替える（任意）
6. 記事の「書き直し案（未検証）」のコード例は、実際に動いたパターンの JSON に合わせる。記事のコード例は `hooks-lab/guard.py` を呼ぶ形に揃える（現状は `scripts/hooks/protect-config.py`）
7. 終わったら `.\hooks-lab\use-variant.ps1 off` で無効に戻す

### 3-2. VS Code 1.146 で画面を見直す

- Check for Updates で 1.146 にして、Migrations 画面や Session Target の文言が変わっていないか確認する
- 変わっていなければ、記事の「検証環境について」の注記を「1.145.3 と 1.146 の両方で確認」に書き換える
- 変わっていれば、該当のスクショを撮り直す

### 3-3. 未検証の項目（任意）

| 項目 | 方法 | 記事への反映 |
| ---- | ---- | ------------ |
| ユーザープロファイルのエージェント・指示 | Windows は `user-profile-demo/` の 2 ファイルを `%APPDATA%\Code\User\prompts\` にコピーして、Migrations の **User Data** を確認 | 「デモでは試せていません」の注記を、結果に置き換える |
| 移行の通知（Review Migrations） | 新しいワークスペースを開いて、チャットに通知が出るか確認 | 「通知は確認できなかった」の記述を、結果に合わせる |
| `/sandbox policy` | Copilot セッションで実行 | 6 章に結果を追記 |

### 3-4. 公開前の最終確認

- [ ] スクショにWindows のユーザー名（`C:\Users\...` のパス）が写っている。伏せたい場合は塗りつぶす（該当: `demo-03b` / `demo-04` / `demo-05` / `demo-05b` / `demo-06` / `demo-07` / `demo-07b` / `demo-09`）
- [ ] 記事の冒頭コメント（公開前チェック）を削除した
- [ ] 画像を GitHub に push した（`main` にマージされるまで raw URL は 404）
- [ ] `ignorePublish: true` → `false` に変更した

---

## 4. デモ環境のリセット

デモ用リポジトリは、作業用ブランチを捨てるか、クローンし直せば元に戻ります（`main` には push しないこと）。

```powershell
git checkout -- . ; git clean -fd
git checkout main ; git branch -D harness-migration-demo
```

リポジトリの外に作られたファイルは、手動で削除します。

- `~/.copilot/mcp-config.json`（ユーザーの MCP サーバーを移行した場合。普段使っているファイルは消さないこと）
- ユーザープロファイルにコピーしたダミーの 2 ファイル（`demo-reviewer.agent.md` / `demo-style.instructions.md`）と、移行で `~/.copilot/agents`・`~/.copilot/instructions` に作られた同名ファイル
