#!/usr/bin/env python3
"""
WordPress 画像アップロード & src 置換スクリプト（ai-901-exam-experience 専用）
Usage: python articles/blog/ai-901-exam-experience/upload_images.py [--site security|main]
"""
import base64
import mimetypes
import os
import re
import sys
from pathlib import Path

def _load_env():
    for env_path in [Path(__file__).parents[3] / ".env", Path(".env")]:
        if env_path.exists():
            with open(env_path, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, _, v = line.partition("=")
                        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
            return
    print("⚠️  .env が見つかりません。環境変数を直接設定してください。")

_load_env()

_site = "security"
if "--site" in sys.argv:
    _idx = sys.argv.index("--site")
    if _idx + 1 < len(sys.argv):
        _site = sys.argv[_idx + 1].lower()

if _site == "main":
    WP_URL  = os.environ.get("WP_URL_MAIN", "").rstrip("/")
    WP_USER = os.environ.get("WP_USER_MAIN", "")
    WP_PASS = os.environ.get("WP_APP_PASS_MAIN", "")
else:
    WP_URL  = os.environ.get("WP_URL_SECURITY", os.environ.get("WP_URL", "")).rstrip("/")
    WP_USER = os.environ.get("WP_USER_SECURITY", os.environ.get("WP_USER", ""))
    WP_PASS = os.environ.get("WP_APP_PASS_SECURITY", os.environ.get("WP_APP_PASS", ""))

if not all([WP_URL, WP_USER, WP_PASS]):
    print("❌ .env に WP_URL_SECURITY / WP_USER_SECURITY / WP_APP_PASS_SECURITY を設定してください。")
    sys.exit(1)

try:
    import requests
except ImportError:
    print("❌ requests をインストールしてください: pip install requests")
    sys.exit(1)

ARTICLE_DIR = Path(__file__).parent
IMAGES_DIR  = ARTICLE_DIR / "Images"
ARTICLE_HTML = ARTICLE_DIR / "article.html"
OUTPUT_HTML  = ARTICLE_DIR / "article-wp.html"
SLUG = "ai-901-exam-experience"

# eyecatch.png はアップロード対象から除外（WordPress設定欄で別途設定）
EXCLUDE = {"eyecatch.png"}

if not IMAGES_DIR.exists():
    print(f"❌ Images/ が見つかりません: {IMAGES_DIR}")
    sys.exit(1)

if not ARTICLE_HTML.exists():
    print(f"❌ article.html が見つかりません: {ARTICLE_HTML}")
    sys.exit(1)

token = base64.b64encode(f"{WP_USER}:{WP_PASS}".encode()).decode()
HEADERS = {"Authorization": f"Basic {token}"}

png_files = sorted(f for f in IMAGES_DIR.glob("*.png") if f.name not in EXCLUDE)

if not png_files:
    print(f"⚠️  Images/ にアップロード対象の PNG ファイルが見つかりません。")
    sys.exit(1)

print(f"\n🚀 {len(png_files)} 件の画像を WordPress にアップロードします...")
print(f"   対象: {WP_URL}")

src_map: dict[str, str] = {}  # "Images/xxx.png" -> "https://.../wp-content/..."

for i, png_path in enumerate(png_files, start=1):
    wp_filename = f"{SLUG}-{png_path.stem}.png"
    mime = mimetypes.guess_type(str(png_path))[0] or "image/png"

    with open(png_path, "rb") as f:
        data = f.read()

    resp = requests.post(
        f"{WP_URL}/wp-json/wp/v2/media",
        headers={**HEADERS, "Content-Disposition": f'attachment; filename="{wp_filename}"',
                 "Content-Type": mime},
        data=data,
        timeout=60,
    )

    if resp.status_code in (200, 201):
        wp_url = resp.json().get("source_url", "")
        src_map[f"Images/{png_path.name}"] = wp_url
        print(f"  ✅ [{i}/{len(png_files)}] {png_path.name} → {wp_url}")
    else:
        print(f"  ❌ [{i}/{len(png_files)}] {png_path.name} アップロード失敗: {resp.status_code} {resp.text[:200]}")

html = ARTICLE_HTML.read_text(encoding="utf-8")
replaced = 0

for local_src, wp_url in src_map.items():
    new_html = html.replace(f'src="{local_src}"', f'src="{wp_url}"')
    if new_html != html:
        replaced += 1
    html = new_html

OUTPUT_HTML.write_text(html, encoding="utf-8")

print(f"\n📝 置換完了: {replaced} 件")
print(f"   出力: {OUTPUT_HTML}")

remaining = len(re.findall(r'src="Images/', html))
if remaining:
    print(f"\n⚠️  未置換の Images/ 参照が {remaining} 件残っています。")
else:
    print("✅ すべての Images/ 参照が WordPress URL に置換されました。")
