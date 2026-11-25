# VS Code 軽量化記事 デモ撮影メモ（撮影済み）

記事 [article-qiita.md](./article-qiita.md) のスクショは撮影・配置済みです。考察は [memo.md](./memo.md)、元のスクショは `images/_original/` にあります。

## 使った画像

| ファイル名 | 元スクショ（撮影時刻） | 記事内の位置 |
| --- | --- | --- |
| `demo-01-process-explorer-menu.png` | 18:58:58 | 手順0: Help > Open Process Explorer |
| `demo-02-extension-host-baseline.png` | 19:20:48（トリミング） | 手順0: Baseline 724 MB |
| `demo-03-running-extensions.png` | 19:23:18（トリミング） | 手順0: Show Running Extensions |
| `demo-04-bisect-start.png` | 19:24:31 | Extension Bisect: 開始ダイアログ |
| `demo-05-bisect-judge.png` | 19:25:50 + 19:32:52 | Extension Bisect: 回答（49個 / 4個） |
| `demo-06-bisect-result.png` | 19:36:42 | Extension Bisect: 結果 |
| `demo-07-foundry-toolkit-toggle.png` | 19:44:40 | 単体 ON/OFF: 拡張機能ページ |
| `demo-08-foundry-on-off.png` | 19:40:19 + 19:42:16（トリミング） | 単体 ON/OFF: 724 MB と 614 MB |
| `demo-09-watcher-exclude.png` | 19:57:03 | ファイル監視: settings.json |
| `demo-10-after-watcher-exclude.png` | 19:57:55（トリミング） | ファイル監視: 追加後 646 MB |
| `demo-11-agents-window.png` | 20:02:13（トリミング） | Copilot / エージェント周り |

ローカルのパス（ユーザー名）は黒塗りしてあります。Process Explorer の画像は、文字が読めるよう左右をトリミングし、WSL 側 `extension-host` のメモリを赤枠で囲んであります。

## 公開前チェック

- [ ] 画像を `main` に push して raw URL が開ける（push するまで 404）
- [x] 画像内の Windows / WSL のユーザー名は黒塗り済み（`images/` の `demo-*.png`）
- [x] マスク前の元画像は `images/_original/` にあり、`.gitignore` でコミット対象外
