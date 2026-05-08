---
name: wechat-article-creator
description: |
  创建微信公众号技术解读文章并生成配图。当用户要求写一篇公众号文章、生成公众号配图、为某个主题创作公众号内容时触发。也适用于"根据调研写公众号"、"生成文章配图"、"写文章并配图"等场景。
  流程包括：制定写作计划、撰写文章正文、使用 UI/UX skill 生成设计系统并创建 HTML 配图、Playwright 截图、整合配图、去除 AI 写作痕迹。
---

# 微信公众号文章创作 Skill

## 触发条件

用户要求：
- "写一篇关于 X 的公众号文章"
- "根据这些素材生成公众号内容"
- "创建文章配图"
- "写文章并配图"
- 任何涉及公众号文章创作和配图生成的任务

## 输入要求

用户提供：
1. **素材路径**：调研报告、图片、项目源码等素材的位置
2. **标题方向**（可选）：如果没有指定，根据素材提炼 1-2 个含 SEO 关键词的标题
3. **特殊要求**（可选）：如特定的文章结构、侧重点等

## 输出格式

- **文章**：`.md` 文件，放在素材同级目录下
- **配图**：若干张 PNG，放在 `images/` 子目录下
  - 封面：1260×540（21:9）
  - 章节配图：按需创建，比例根据内容决定（1:1、4:3、16:9 均可）
  - 原始信息图（如有）：直接嵌入

## 工作流程

### 步骤 1：阅读素材并制定计划

1. 阅读用户提供的所有素材（调研报告、图片、源码等）
2. 将计划写入 `tasks/todo.md`，包含：
   - 文章核心结构
   - 标题方向（含 SEO 关键词）
   - Todo 列表（撰写正文、生成配图、整合、去 AI 痕迹、Review）
3. **等待用户确认计划后再继续**

### 步骤 2：撰写文章正文

遵循公众号行文规范：

- **语气**：诙谐、带点幽默，像和人聊天
- **结构**：
  ```
  ---
  title: 文章标题
  date: YYYY-MM-DD
  tags: [标签1, 标签2]
  ---

  # 吸引人的完整标题

  > 场景引入（一句话，抓眼球）

  ---

  ## 一句话总结

  核心观点概括。

  ---

  ## 正文（用 --- 分隔章节）

  ### 小节标题
  内容...

  ---

  ## 总结
  收尾。
  ```
- **格式**：多用加粗标记关键信息，善用表格、列表做对比，适当用 `> 引用` 强调
- **技术术语**：用通俗类比解释，不要太学术

### 步骤 3：生成配图

**必须调用 `ui-ux-pro-max` skill 生成设计系统。**

通过 `Skill` 工具调用：

```
skill: ui-ux-pro-max
args: 为 [文章主题] 公众号配图生成设计系统。风格要求：浅色主题、现代简洁、技术博客配图。使用 --design-system 参数。
```

该命令会返回完整的设计系统推荐，包括：
- **Pattern**：内容优先 / 新闻通讯风格
- **Style**：Swiss Modernism 2.0（瑞士现代主义）
- **Colors**：主色、强调色、背景色、边框色等完整配色
- **Typography**：推荐的字体组合（通常是 Space Mono + Inter）
- **Effects**：网格布局、数学比例间距

**根据设计系统的推荐创建 HTML 文件：**

1. 提取配色：背景 `#FAFAFA`、主文字 `#18181B`、强调色（通常是蓝色 `#2563EB` 或粉色 `#EC4899`，按设计系统推荐选用）
2. 提取字体：标题用 `Space Mono`，正文用 `Inter`
3. 根据文章章节按需创建 HTML 配图，全部放在 `images/` 目录：
   - 1 张封面（1260×540）
   - 若干张章节配图，数量和比例根据章节内容决定
4. 风格统一：细边框、色块点缀、不用 emoji、编号替代图标

**截图：**

```bash
python3 .claude/skills/wechat-article-creator/scripts/screenshot.py <images-dir>
```

截图脚本会扫描目录下所有 `.html` 文件，自动从 `body` 的 CSS 尺寸读取宽高并截图。每张图的尺寸由 HTML 自己定义，无需在脚本中配置。

### 步骤 4：整合配图

在文章中适当位置插入配图，使用 Obsidian 内嵌语法：
```markdown
![[cursor/images/cover.png]]
```

### 步骤 5：去除 AI 写作痕迹

使用 Humanizer-zh skill 处理文章，重点检查：
- 删除"你有没有想过"等 AI 开场白
- 去掉"标志着""体现了"等夸大表达
- 减少过度加粗
- 将总结段从宣传性排比改为直白分析
- 变化句子长度，混合长短句

### 步骤 6：更新 Review 总结

在 `tasks/todo.md` 末尾添加 Review 总结，包含：
- 已交付内容（文章路径、配图列表）
- 关键改动说明

## 配图 HTML 模板规范

每个 HTML 文件遵循以下结构：

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  width: 800px; height: 800px;  /* 按内容需求调整尺寸 */
  font-family: 'Inter', sans-serif;
  background: #FAFAFA;
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  padding: 48px;
}
/* 具体内容样式 */
</style>
</head>
<body>
<!-- 内容 -->
</body>
</html>
```

## 注意事项

- 始终使用中文回复用户
- 每步只做最少修改，保持简单
- 配图必须先通过 UI/UX skill 生成设计系统
- 去 AI 痕迹后再做最终交付
- 不主动 git commit，除非用户明确要求
