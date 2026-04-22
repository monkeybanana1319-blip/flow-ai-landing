# Flow AI Consulting · Landing Page

Essential 体验版落地页。静态站，无构建步骤，纯 HTML + CSS + JS。

## 目录结构

```
.
├── index.html          # 主页
├── css/styles.css      # 所有样式
├── js/main.js          # 动画 + FAQ + WhatsApp 追踪
├── assets/
│   ├── logo.png        # 透明背景 logo（浅色区用）
│   ├── logo-white.png  # 反色 logo（深色区用）
│   ├── logo-original.jpg
│   ├── favicon.png
│   └── og-image.jpg    # 社交分享预览（1200x630）
├── scripts/            # 本地构建辅助脚本（不部署）
│   ├── split.py        # 从单文件 HTML 拆分
│   ├── make-logo.py    # 生成 logo 变体
│   └── build-index.py  # 组装 index.html
├── robots.txt
├── sitemap.xml
├── netlify.toml        # Netlify 部署配置（缓存头 / redirect）
└── .gitignore
```

## 本地预览

不需要构建。任选一种方式：

```bash
# 方式 A：Python 内建
python3 -m http.server 8000
# 浏览器打开 http://localhost:8000

# 方式 B：Node
npx serve .
```

## 启用追踪代码

`index.html` 已预置 GA4 + Meta Pixel 代码，默认注释。

### Google Analytics 4
1. https://analytics.google.com → 管理 → 数据流 → 添加 → Web
2. 复制 Measurement ID（格式 `G-XXXXXXXXXX`）
3. 在 `index.html` 搜索 `G-XXXXXXXXXX`，替换两处
4. 移除外层 `<!--` 和 `-->` 注释标记

### Meta (Facebook) Pixel
1. https://business.facebook.com → 事件管理工具 → 创建 Pixel
2. 复制 Pixel ID（16 位数字）
3. 在 `index.html` 搜索 `XXXXXXXXXXXXXXXX`，替换两处
4. 移除外层 `<!--` 和 `-->` 注释标记

启用后，`js/main.js` 会自动把每次 WhatsApp 点击记录为 `whatsapp_click`（GA4）和 `Contact`（Pixel）事件。

## WhatsApp CTA 预填消息

所有 CTA 都会带不同的预填文字，方便你在 WA 上分辨来源：

| CTA 位置 | 预填消息 |
|---|---|
| 顶部导航「立即咨询」 | 你好，想了解 Flow AI Consulting 的落地页服务。 |
| 首屏「立即预约」 | 我要预约 RM168 体验官名额（Essential 落地页）✨ |
| 案例「我也要拥有这样的页面」 | 看了 Flow AI 的案例，我也想做这样的专业落地页。 |
| 底部「WhatsApp 锁定名额」 | 锁定 RM168 体验官名额 · 立刻开始 🔥 |
| 浮动按钮 | 你好，我从 Flow AI 落地页过来咨询。 |

## 部署

部署到 Netlify：见 `DEPLOY.md`。

## 修改源文件注意

- 改样式 → `css/styles.css`
- 改文案 → `index.html`
- 改 logo → 替换 `assets/logo-original.jpg` 后重跑 `python3 scripts/make-logo.py`
- `scripts/` 下的文件是辅助脚本，不需要提交给访客浏览，Netlify 会部署但不影响访问
