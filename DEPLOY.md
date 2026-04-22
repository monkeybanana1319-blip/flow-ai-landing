# 部署指南

## 步骤 1：推到 GitHub

```bash
cd ~/flow-ai-consulting

# （已经 git init 完了，只需要关联远程）
# 先到 https://github.com/new 创建一个仓库
# 仓库名建议：flow-ai-landing  （不要选 "Add README"，保持空白）

git remote add origin git@github.com:YOUR_GITHUB_USERNAME/flow-ai-landing.git
# 或 HTTPS：git remote add origin https://github.com/YOUR_GITHUB_USERNAME/flow-ai-landing.git

git branch -M main
git push -u origin main
```

## 步骤 2：连接 Netlify

1. 打开 https://app.netlify.com/
2. 点击 **Add new site** → **Import an existing project**
3. 选 **Deploy with GitHub**，授权后选刚才创建的 `flow-ai-landing` 仓库
4. 构建设置全部留空：
   - Base directory: *（留空）*
   - Build command: *（留空）*
   - Publish directory: `.`
5. 点 **Deploy site**

部署完成后 Netlify 会给你一个随机子域名，例如 `https://super-cat-abc123.netlify.app/`。

## 步骤 3：改子域名

Netlify 默认域名可以自定义子域名，免费：

1. **Site configuration** → **Domain management** → **Options** → **Edit site name**
2. 改成 `flow-ai-consulting`（如果被占用，试 `flow-ai-my`、`flowai-consulting` 等）
3. 站点变成 `https://flow-ai-consulting.netlify.app/`

**重要：** 如果改了子域名，记得回头更新 `index.html`、`sitemap.xml`、`robots.txt` 里的 URL，然后 push 重新部署。

## 步骤 4：后续买域名

等流量稳定想绑自己的域名（如 `flow-ai.my` / `flowai.com`）：

1. 在 Namecheap / GoDaddy / Cloudflare 买域名（马来西亚 .my 域名约 RM80–120/年）
2. Netlify → **Domain management** → **Add custom domain**
3. Netlify 会给你两条 DNS 记录（通常是 A + CNAME），在域名商后台配置
4. SSL 证书自动签发，约 10–60 分钟生效

## 自动部署

连接 GitHub 之后每次 `git push` 都会自动触发 Netlify 重建。改内容流程：

```bash
# 改完文件
git add .
git commit -m "Update pricing"
git push
# 30 秒后线上生效
```

## 常用链接

- Netlify 后台：https://app.netlify.com/
- GA4：https://analytics.google.com/
- Meta 事件管理：https://business.facebook.com/events_manager
- 域名推荐：https://www.cloudflare.com/products/registrar/ （成本价）
