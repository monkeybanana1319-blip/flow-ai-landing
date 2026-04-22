"""Split the monolithic landing page HTML into index.html + css/styles.css + js/main.js
and extract the embedded base64 logo to assets/logo-original.jpg."""
import re
import base64
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = Path.home() / "Downloads" / "flow-ai-landing-page.html"

html = SRC.read_text(encoding="utf-8")

# 1) Extract CSS
css_match = re.search(r"<style>\s*(.*?)\s*</style>", html, re.DOTALL)
css = css_match.group(1)
(ROOT / "css" / "styles.css").write_text(css, encoding="utf-8")

# 2) Extract JS
js_match = re.search(r"<script>\s*(.*?)\s*</script>", html, re.DOTALL)
js = js_match.group(1)
(ROOT / "js" / "main.js").write_text(js, encoding="utf-8")

# 3) Extract embedded base64 JPEG logo
img_match = re.search(r'<img\s+src="data:image/jpeg;base64,([A-Za-z0-9+/=]+)"([^>]*)>', html)
b64_data = img_match.group(1)
img_bytes = base64.b64decode(b64_data)
(ROOT / "assets" / "logo-original.jpg").write_bytes(img_bytes)
print(f"Logo extracted: {len(img_bytes) // 1024} KB")

# 4) Rebuild body: replace base64 img with file reference
body_match = re.search(r"<body>(.*?)</body>", html, re.DOTALL)
body = body_match.group(1)
body_clean = re.sub(
    r'<img\s+src="data:image/jpeg;base64,[A-Za-z0-9+/=]+"([^>]*)>',
    r'<img src="assets/logo.png" alt="Flow AI Consulting"\1>',
    body,
)
# Strip inline `alt="..."` duplicates that may result
body_clean = re.sub(r'(alt="Flow AI Consulting")(\s+alt="[^"]*")', r"\1", body_clean)

# 5) Write a placeholder — the final index.html will be written separately with head/tracking
(ROOT / ".body.tmp").write_text(body_clean.strip(), encoding="utf-8")

print("Done. CSS:", len(css), "chars. JS:", len(js), "chars. Body:", len(body_clean), "chars.")
