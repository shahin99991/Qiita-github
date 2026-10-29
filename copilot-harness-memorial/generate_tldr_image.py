#!/usr/bin/env python3
"""TL;DR 用の解説イメージを Gemini API（Nano Banana 2.1）で生成する"""
import base64
import json
import os
import urllib.request
from pathlib import Path


def _load_env():
    for env_path in [Path(__file__).parents[1] / ".env", Path(".env")]:
        if env_path.exists():
            for line in open(env_path, encoding="utf-8"):
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, _, v = line.partition("=")
                    os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
            return


_load_env()

MODEL = "gemini-nano-banana-2.1"
ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/interactions"
OUTPUT = Path(__file__).parent / "Images" / "img-00-tldr-overview.jpg"
PROMPT = """日本語の技術ブログ用 TL;DR 解説バナー画像を作成。16:9 横長、テキスト主役のインフォグラフィック。
【テーマ】追悼サイト（GitHub Copilot SDK の追悼式場）を Azure Static Web Apps と Azure Functions で作った
【画像内に描画する日本語テキスト（正確に）】
- 大見出し: 「追悼式場を Azure で作ってみた」
- 左ボックス 見出し「画面（Static Web Apps）」 箇条書き「HTML / CSS / JS だけ」「日本語・英語の切り替え」「CSP をヘッダーで返す」
- 中央ボックス 見出し「API（Azure Functions）」 箇条書き「5秒ごとにまとめて送信」「Node.js 24」「通信先はここだけ」
- 右ボックス 見出し「データ（Table Storage）」 箇条書き「カウンターを32分割」「300人同時でも欠落なし」「弔辞は全員に公開」
- ボックス同士を右向きの矢印でつなぐ
【スタイル】フラット・モダン、夜空のような濃紺の背景に、金色とろうそくの炎色のアクセント。墓石とろうそくの小さなイラストを添える。日本語フォントは太めで読みやすく、文字は誤字なく正確に。
"""

body = {
    "model": MODEL,
    "input": PROMPT,
    "store": False,
    "response_format": {"type": "image", "mime_type": "image/jpeg", "aspect_ratio": "16:9", "image_size": "2K"},
}
req = urllib.request.Request(
    ENDPOINT,
    data=json.dumps(body).encode("utf-8"),
    headers={"Content-Type": "application/json", "x-goog-api-key": os.environ["GEMINI_API_KEY"]},
)


def find_image(node):
    if isinstance(node, dict):
        if node.get("type") == "image" and isinstance(node.get("data"), str):
            return node
        for v in node.values():
            r = find_image(v)
            if r:
                return r
    elif isinstance(node, list):
        for v in node:
            r = find_image(v)
            if r:
                return r
    return None


try:
    with urllib.request.urlopen(req, timeout=180) as res:
        img = find_image(json.load(res))
except urllib.error.HTTPError as e:
    raise SystemExit(f"HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:500]}")
if not img:
    raise SystemExit("画像が返ってきませんでした")
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_bytes(base64.b64decode(img["data"]))
print(f"保存完了: {OUTPUT}")
