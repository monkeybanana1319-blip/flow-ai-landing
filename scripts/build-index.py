"""Assemble the final index.html from .body.tmp + HEAD/TRACKING snippets,
and rewrite every WhatsApp CTA with a context-specific prefilled message."""
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
WA = "601133151341"

def wa(msg: str) -> str:
    return f"https://wa.me/{WA}?text={quote(msg)}"

# Map each CTA in the body to a prefilled WhatsApp message.
# The message text itself tells us which CTA the lead clicked.
CTA_MESSAGES = [
    # (old_href -> new_href, css_class_hint_for_matching)
    ('class="nav-cta"',       wa("你好，想了解 Flow AI Consulting 的落地页服务。")),
    ('class="btn-primary"',   wa("我要预约 RM168 体验官名额（Essential 落地页）✨")),
    # 2 "我也要拥有" — the showcase block
    ('>我也要拥有这样的页面', wa("看了 Flow AI 的案例，我也想做这样的专业落地页。")),
    ('class="final-btn fade-up"', wa("锁定 RM168 体验官名额 · 立刻开始 🔥")),
    ('class="fab"',           wa("你好，我从 Flow AI 落地页过来咨询。")),
]

body = (ROOT / ".body.tmp").read_text(encoding="utf-8")

# Strip inline <script>...</script> — we load js/main.js externally
import re
body = re.sub(r"<script>.*?</script>\s*", "", body, flags=re.DOTALL)

# Rewrite WhatsApp links by locating each anchor and replacing the href.
# Generic pattern for any remaining plain wa.me link (e.g. showcase link near class-less anchor):
def rewrite(body_text: str, marker: str, new_href: str) -> str:
    """Replace the href of the first <a> tag that contains `marker`."""
    # Pattern matches an anchor tag where the marker appears anywhere in the tag or its content start
    pattern = re.compile(
        r'<a\s+href="https://wa\.me/' + WA + r'"([^>]*' + re.escape(marker) + r'[^>]*>|[^>]*>[^<]{0,80}' + re.escape(marker) + r')',
        re.DOTALL,
    )
    def sub(m):
        return m.group(0).replace(f'href="https://wa.me/{WA}"', f'href="{new_href}"')
    return pattern.sub(sub, body_text, count=1)

for marker, new_href in CTA_MESSAGES:
    # Try class-based first
    before = body
    body = rewrite(body, marker, new_href)
    if body == before:
        print(f"WARN: no match for {marker[:40]}")

# Any remaining bare wa.me/601133151341 → give it a generic prefill
body = body.replace(
    f'href="https://wa.me/{WA}"',
    f'href="{wa("你好，想了解 Flow AI Consulting 的服务。")}"',
)

# ============ HEAD ============
HEAD = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<!-- Primary SEO -->
<title>Flow AI Consulting · 专业落地页 48h 交付 · RM168 体验官</title>
<meta name="description" content="首批10位体验官专属价 RM168（正价 RM1,288）。48h 交付 · 双端适配 · 品牌感定制 · WhatsApp 直达。让流量变客户，马来西亚本地 + 中英文支持。">
<meta name="keywords" content="落地页,landing page,马来西亚建站,Flow AI,品牌网页,WhatsApp 落地页,小红书落地页">
<meta name="author" content="Flow AI Consulting">
<meta name="robots" content="index,follow">
<link rel="canonical" href="https://flow-ai-consulting.netlify.app/">

<!-- Favicon -->
<link rel="icon" type="image/png" href="assets/favicon.png">
<link rel="apple-touch-icon" href="assets/favicon.png">
<meta name="theme-color" content="#f5f1ea">

<!-- Open Graph (Facebook / WhatsApp preview) -->
<meta property="og:type" content="website">
<meta property="og:site_name" content="Flow AI Consulting">
<meta property="og:title" content="一张专业落地页，让客户立刻下单 · Flow AI">
<meta property="og:description" content="首批10位体验官 RM168（原价 RM1,288）· 48h 交付 · 双端适配 · WhatsApp 直达。">
<meta property="og:image" content="https://flow-ai-consulting.netlify.app/assets/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:url" content="https://flow-ai-consulting.netlify.app/">
<meta property="og:locale" content="zh_CN">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Flow AI Consulting · 专业落地页 48h 交付">
<meta name="twitter:description" content="首批10位体验官 RM168（原价 RM1,288）· WhatsApp 直达。">
<meta name="twitter:image" content="https://flow-ai-consulting.netlify.app/assets/og-image.jpg">

<!-- Fonts -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Noto+Serif+SC:wght@400;500;600;700;900&family=Inter:wght@300;400;500;600&family=Playfair+Display:ital,wght@0,400;0,500;0,700;1,400&display=swap" rel="stylesheet">

<!-- Stylesheet -->
<link rel="stylesheet" href="css/styles.css">

<!--
  ================================================================
  TRACKING — enable by uncommenting and replacing the placeholder IDs.

  1) Google Analytics 4
     - Get ID: https://analytics.google.com → 管理 → 数据流 → 添加 → Web
     - ID 格式: G-XXXXXXXXXX

  2) Meta (Facebook) Pixel
     - Get ID: https://business.facebook.com → 事件管理工具 → 创建 Pixel
     - ID 格式: 16 位数字

  3) After pasting IDs, also check js/main.js for the `trackWhatsAppClick` hook.
  ================================================================
-->

<!-- Google Analytics 4 (disabled) -->
<!--
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
-->

<!-- Meta Pixel (disabled) -->
<!--
<script>
  !function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?
  n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;
  n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;
  t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,
  document,'script','https://connect.facebook.net/en_US/fbevents.js');
  fbq('init', 'XXXXXXXXXXXXXXXX');
  fbq('track', 'PageView');
</script>
<noscript><img height="1" width="1" style="display:none"
  src="https://www.facebook.com/tr?id=XXXXXXXXXXXXXXXX&ev=PageView&noscript=1"/></noscript>
-->

</head>
<body>
"""

TAIL = """
<script src="js/main.js"></script>
</body>
</html>
"""

final = HEAD + body.strip() + "\n" + TAIL
(ROOT / "index.html").write_text(final, encoding="utf-8")
print(f"index.html written ({len(final) // 1024} KB)")

# Clean up temp file
(ROOT / ".body.tmp").unlink()
print("Done.")
