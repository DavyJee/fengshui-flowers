# 🌸 玄花秘典

> 风水花卉智能推荐系统 — 基于生肖、方位、房间与诉求，AI 智能推荐最适合你的花卉。

**在线体验：** https://davyjee.github.io/fengshui-flowers

---

## ✨ 功能特色

- 🏠 **9大方位** — 东/东南/南/西南/西/西北/北/东北/中
- 🐾 **12生肖五行** — 自动匹配相生相助的花卉
- 🛋️ **8种房间** — 客厅/卧室/书房/厨房/卫生间/阳台/玄关/餐厅
- ✨ **4大诉求** — 招财 / 桃花 / 事业 / 健康
- 🎨 **神秘科技风界面** — 深色星云 + 霓虹发光效果

---

## 🛠️ 技术栈

| 层级 | 技术 |
|------|------|
| 后端 | Python 3 + Flask |
| 规则引擎 | 自研 FengShuiFlowerEngine |
| 前端 | HTML5 + CSS3 (无框架) |
| 知识库 | Excel 规则表 |

---

## 🚀 本地运行

```bash
# 克隆项目
git clone https://github.com/DavyJee/fengshui-flowers.git
cd fengshui-flowers

# 安装依赖
pip install flask openpyxl

# 启动服务
python3 api.py
```

打开 http://localhost:5678 即可体验。

---

## 📁 项目结构

```
fengshui-flowers/
├── fengshui_engine.py     # 推荐引擎核心
├── fengshui_flowers.py    # 知识库生成脚本
├── api.py                 # Flask API 服务
├── templates/
│   └── index.html         # 前端页面
├── 风水花卉推荐知识库.xlsx  # 完整知识表格
└── README.md
```

---

## 🌐 部署

### GitHub Pages 静态部署
```bash
# 将 templates/index.html 作为入口
# 可通过 Netlify / Vercel / Cloudflare Pages 托管
```

### Docker 部署
```bash
docker build -t fengshui-flowers .
docker run -p 5678:5678 fengshui-flowers
```

---

## 📜 License

MIT License
