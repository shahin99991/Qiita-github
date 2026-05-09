# DevOps × AI 記事アイデアストック（MLSA / MVP目標向け）

Microsoft Learn Student Ambassador (MLSA) の活動実績や、「DevOps × AI」領域でのMicrosoft MVP受賞を見据えた記事のアイデアストックです。

## アイデア1: GitHub Copilot × Bicep / Terraform による爆速インフラ構築

- **概要**: IaC（BicepやTerraform）は初学者にとって学習ハードルが高いが、GitHub Copilotの自然言語プロンプトを活用することで、Azureリソースのコードを瞬時に生成・構築できることを実証するチュートリアル。
- **アピールポイント**:
  - プロンプトエンジニアリングとIaCの融合。
  - AIがインフラエンジニア（DevOps）の生産性をどう変えるかという実践的なデモ。
  - 初学者（他の学生など）向けのAzure入門記事としても価値が高い。

## アイデア2: ちょうど今試した「Copilot Agent Hooks」でDevOpsの安全性を守る

- **概要**: VS Codeの機能「GitHub Copilot Agent Hooks」をIaCに応用する検証記事。「AIにTerraformやBicepを任せるが、`terraform destroy`（全削除）や本番DBのリソース削除が走る時だけHookでブロックし、承認フローを挟む」という仕組みを構築する。
- **アピールポイント**:
  - AIをDevOpsに組み込む際の最大の課題である「安全性・ガバナンス」の解決策を提示。
  - 最新のプレビュー機能（Agent Hooks）をキャッチアップし、実践的なユースケースを作れる（Microsoftコミュニティで高く評価されるポイント）。

## アイデア3: Azure OpenAI を組み込んだ DevOps CI/CD パイプライン

- **概要**: GitHub Actions や Azure DevOps のパイプラインに Azure OpenAI を組み込む実装例。「Terraformの変更計画（`terraform plan`）の結果をパイプライン上でAIに読み込ませ、変更の要約やリスク評価をPull Requestに自動コメントさせる」仕組みを作る。
- **アピールポイント**:
  - Microsoft製品（Azure OpenAI + GitHub / Azure DevOps）をフル活用した最新のDevOpsプラクティス。
  - 運用現場のリアルなペイン（Plan結果が長すぎてレビューが大変）をAIで解決する実用性の高さ。

---

**📝 今後のステップ**
まずは一番着手しやすい「アイデア1（Copilot × Bicepの基礎）」か、直近で検証に成功した新機能である「アイデア2（Agent HooksでIaC実行をブロック）」から執筆を進めるのがおすすめです。
