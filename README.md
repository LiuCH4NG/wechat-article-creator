# wechat-article-creator

创建微信公众号技术解读文章并生成配图。

## 功能

- 阅读素材，制定写作计划
- 撰写符合公众号风格的正文
- 调用 `ui-ux-pro-max` skill 生成设计系统
- 创建 HTML 配图并自动截图
- 整合配图、去除 AI 写作痕迹

## 触发场景

- "写一篇关于 X 的公众号文章"
- "根据这些素材生成公众号内容"
- "创建文章配图"
- "写文章并配图"

## 目录结构

```
wechat-article-creator/
├── SKILL.md              # Skill 核心指令
├── README.md             # 本文件
└── scripts/
    └── screenshot.py     # Playwright 自适应截图脚本
```

## 依赖

### Obsidian

文章使用 Obsidian 内嵌语法 `![[path/to/image.png]]` 嵌入配图，frontmatter 格式也遵循 Obsidian 规范。确保在 Obsidian 中打开项目目录以正常预览配图。

## 依赖 Skill 安装

本 Skill 依赖以下两个 Skill，请确保它们已安装：

### 1. ui-ux-pro-max

用于生成配图的设计系统。

```bash
/plugin marketplace add nextlevelbuilder/ui-ux-pro-max-skill
/plugin install ui-ux-pro-max@ui-ux-pro-max-skill
/reload-plugins
```

### 2. Humanizer-zh

用于去除文章中的 AI 写作痕迹。

**方式一（推荐）**：
```bash
npx skills add https://github.com/op7418/Humanizer-zh.git
```

**方式二**：Git 克隆
```bash
git clone https://github.com/op7418/Humanizer-zh.git ~/.claude/skills/humanizer-zh
```

**方式三**：手动安装
下载 ZIP 并解压到 `.claude/skills/` 目录，确保文件夹结构为：
```
.claude/skills/humanizer-zh/
├── SKILL.md
└── README.md
```

安装完成后执行 `/reload-plugins` 重新加载。

## 截图脚本

`scripts/screenshot.py` 扫描目录下所有 `.html` 文件，从 `body` 的 CSS 尺寸读取宽高后截图。每张图的尺寸由 HTML 自己定义，无需在脚本中配置。

```bash
python3 scripts/screenshot.py <images-directory>
```

## 工作流程

1. **阅读素材并制定计划** → 写入 `tasks/todo.md`
2. **撰写文章正文** → 遵循公众号行文规范
3. **生成配图** → 调用 `ui-ux-pro-max` 获取设计系统，创建 HTML
4. **截图** → 运行 `screenshot.py`
5. **整合配图** → 嵌入文章
6. **去 AI 痕迹** → 调用 `Humanizer-zh`
7. **更新 Review** → 写入 `tasks/todo.md`
