# VS CodeのExtension Bisectでメモリ使用量が大きい拡張機能を調べてみた

## はじめに

VS Codeを使用している際、操作自体に明確な重さを感じていたわけではありませんが、`Developer: Open Process Explorer` を確認すると、WSL環境の `extension-host` が比較的大きなメモリを使用していました。

そこで今回は、VS Codeの **Extension Bisect** を使って、

> どの拡張機能の有効・無効が WSL Extension Host のメモリ使用量に関係しているのか

を調べてみました。

なお、Extension Bisectは本来「問題が再現する / 再現しない」を回答しながら、問題を引き起こしている拡張機能を二分探索で特定する機能です。

今回は操作上の不具合ではなく、**WSL側の `extension-host` のメモリ使用量**を判断材料として検証しました。

---

## 検証環境

- Visual Studio Code
- WSL: Ubuntu
- 同一のワークスペースを使用
- VS Codeの `Developer: Open Process Explorer` でメモリ使用量を確認
- 主な測定対象: WSL側の `extension-host`

---

## 1. Extension Bisect開始前

まず、`Start Extension Bisect` を実行する前の通常状態を確認しました。

すべての拡張機能が通常どおり有効になっている状態では、

| 項目 | Memory |
|---|---:|
| WSL `extension-host` | **724 MB** |

でした。

今回はこの **724 MB** をBaseline（基準値）として扱います。

---

## 2. Extension Bisectを開始

コマンドパレットから、

`Help: Start Extension Bisect`

を実行します。

Extension Bisectを開始すると、拡張機能が一定数無効化された状態でVS Codeが再読み込みされます。

その状態でProcess Explorerを確認し、Baselineの724 MB程度のメモリ使用量が再現しているかを確認しました。

---

## 3. Bisect中のメモリ使用量

今回観測した値は以下のとおりです。

| 無効化された拡張機能数 | WSL `extension-host` | 判定 |
|---:|---:|---|
| 0（Baseline） | **724 MB** | 基準 |
| 49 | **394 MB** | I can't reproduce |
| 25 | **504 MB** | I can't reproduce |
| 13 | **614 MB** | I can't reproduce |
| 7 | **598 MB** | I can't reproduce |
| 4 | **693 MB** | I can reproduce |
| 2 | `extension-host`を同条件で確認できず | I can't reproduce |
| 1 | **646 MB** | I can't reproduce |
| 1（別パターン） | **630 MB** | I can't reproduce |

49個の拡張機能を無効化した状態では、Baselineの724 MBから394 MBまで低下しました。

一方、Bisectが進み、拡張機能が有効に戻っていく過程では、504 MB、614 MB、598 MB、693 MBなどの値が観測されました。

今回はBaselineに近い **693 MB** となったタイミングで `I can reproduce` と判定しました。

---

## 4. Extension Bisectの結果

最終的にExtension Bisectから、次の拡張機能が問題を引き起こしている候補として表示されました。

`ms-windows-ai-studio.windows-ai-studio`

表示名は、

**Foundry Toolkit for VS Code**

です。

ただし、ここで単純に

> 「Foundry Toolkitが原因だった」

と結論付けるのではなく、本当にON/OFFで差が出るのか追加検証しました。

---

# Foundry Toolkit単体で検証

## ONの場合

Foundry Toolkitを有効にした状態でWSL側の `extension-host` を測定しました。

複数回確認したところ、代表的な測定値は以下でした。

| 状態 | Memory |
|---|---:|
| ON 1回目 | **724 MB** |
| ON 2回目 | **740 MB** |

平均すると、

`(724 + 740) / 2 = 732 MB`

となります。

### ON平均

**732 MB**

---

## OFFの場合

次にFoundry Toolkitを無効にして、同じように測定しました。

| 状態 | Memory |
|---|---:|
| OFF 1回目 | **614 MB** |
| OFF 2回目 | **630 MB** |

平均すると、

`(614 + 630) / 2 = 622 MB`

となります。

### OFF平均

**622 MB**

---

# ON/OFFの比較

| Foundry Toolkit | 1回目 | 2回目 | 平均 |
|---|---:|---:|---:|
| ON | 724 MB | 740 MB | **732 MB** |
| OFF | 614 MB | 630 MB | **622 MB** |

平均値の差は、

`732 - 622 = 110 MB`

でした。

割合で見ると、

`110 / 732 × 100 ≒ 15.0%`

となります。

今回の環境では、Foundry ToolkitをOFFにした場合、ONの場合と比較して **WSL Extension Hostのメモリ使用量が平均約110 MB（約15%）低い**結果になりました。

---

# 結論

今回の検証では、VS CodeのExtension Bisectを利用して、WSL Extension Hostのメモリ使用量が変化する拡張機能を調査しました。

Extension Bisectによって最終的に候補として特定されたのは、

**Foundry Toolkit for VS Code**

（`ms-windows-ai-studio.windows-ai-studio`）

でした。

さらに単体でON/OFFを2回ずつ比較したところ、

- ON平均: **732 MB**
- OFF平均: **622 MB**
- 差: **約110 MB**
- OFF時の減少率: **約15%**

となりました。

少なくとも今回の環境・ワークスペース・測定条件では、**Foundry Toolkitを無効化した状態のほうが、WSL側のExtension Hostのメモリ使用量が低い傾向を2回の測定で確認できました。**

---

## 注意点

今回の結果だけから、

> 「Foundry Toolkitは常に約110 MBのメモリを使用する」

と断定することはできません。

VS Codeのメモリ使用量は、

- 開いているワークスペース
- 他の拡張機能
- Language Server
- WSLの状態
- 拡張機能のActivation状況
- 測定タイミング
- Garbage Collection

などによって変動する可能性があります。

また、Extension Bisectは本来、メモリ使用量そのものを測定するための機能ではありません。

今回は `I can reproduce` / `I can't reproduce` の判断を、WSL Extension Hostのメモリ値を基準として行っています。

そのため、今回の検証結果は、

**「今回使用した環境でFoundry Toolkitの有効・無効を切り替えたところ、Extension Hostのメモリ使用量に約15%の差が観測された」**

という範囲で捉えるのが適切だと考えます。

---

## まとめ

今回の検証で分かったことをまとめます。

- Extension Bisectで拡張機能を段階的に絞り込めた
- Bisectでは `ms-windows-ai-studio.windows-ai-studio` が候補として特定された
- これは **Foundry Toolkit for VS Code**
- Foundry Toolkit ON時は平均 **732 MB**
- Foundry Toolkit OFF時は平均 **622 MB**
- 今回の2回の比較では約 **110 MB / 15%** の差が観測された
- ただし、メモリ使用量は環境やタイミングによって変動するため、Foundry Toolkit単体の固定的なメモリ消費量を示す結果ではない

Extension Bisectは「VS Codeがなんとなくおかしいけれど、どの拡張機能が関係しているのか分からない」という状況で、候補を絞り込む最初の手段としてかなり便利でした。

一方で、Bisectが特定した拡張機能をそのまま「犯人」と考えるのではなく、今回のように **候補となった拡張機能だけをON/OFFして再検証することが重要**だと感じました。