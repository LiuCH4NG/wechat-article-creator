# wechat-article-creator

创建微信公众号技术解读文章并生成配图。覆盖从意图理解、大纲设计、初稿撰写到审读自检的完整写作工作流。

## 功能特性

- **9 步写作工作流**：从理解意图到终稿完成，每一步有明确的输入输出和质量标准
- **独立审读 + 事实核查**：通过 subagent 对初稿进行 AI 味检测、逻辑连贯性检查、事实性核查
- **活人感终审**：以读者视角判断文章读起来是「朋友在聊天」还是「AI 在输出」
- **配图自动生成**：调用 `ui-ux-pro-max` skill 生成设计系统，创建 HTML 配图并自动截图
- **去 AI 痕迹**：调用 `Humanizer-zh` skill 去除 AI 写作痕迹
- **自检清单**：硬性规则、风格一致性、HKR 质检、活人感四层自检，附带结构化报告

## 触发场景

- "写一篇关于 X 的公众号文章"
- "根据这些素材生成公众号内容"
- "创建文章配图"
- "写文章并配图"

## 工作流概览

```
Step 1  理解作者意图    → 确认切入角度、深度、主旨、素材、配图需求
Step 2  阅读素材与参考  → 阅读素材 + 行文风格指南 + 范文风格分析
Step 3  设计大纲        → 呈现大纲，等待确认
Step 4  编写初稿        → 按规则写作
Step 5  独立审读        → AI 味检测、逻辑、结构、信息密度
Step 6  事实核查        → 数据来源、场景真实性、术语拼写
Step 7  修改+去AI痕迹  → 逐条处理反馈 + Humanizer-zh
Step 8  生成配图并整合  → UI/UX skill → HTML → 截图 → 嵌入
Step 9  终审自检        → 四层自检清单 + 终稿交付
```

## 目录结构

```
wechat-article-creator/
├── SKILL.md                          # Skill 核心指令，定义工作流和全部写作规则
├── README.md                         # 本文件
├── scripts/
│   └── screenshot.py                 # Playwright 自适应截图脚本
└── references/
    ├── 行文风格指南.md                # 行文排版、标点符号、文本样式规范（源自少数派风格指南）
    └── 范文风格分析.md                # 从历史文章中提炼的写作模式和风格特征（需自定义）
```

## 安装

将本仓库克隆到 Claude Code 的 skills 目录：

```bash
git clone https://github.com/LiuCH4NG/wechat-article-creator.git ~/.claude/skills/wechat-article-creator
```

然后执行 `/reload-plugins` 重新加载。

## 自定义配置

安装后，你可以根据自身情况修改以下内容：

### 1. 作者声音（SKILL.md）

修改「核心价值观」「读者画像」「作者声音」章节，描述你自己的写作调性和目标读者。

### 2. 范文风格分析（references/范文风格分析.md）

这是 Skill 校准语感的依据。从你自己的历史文章中选取 2-3 篇风格最满意的，按以下维度逐篇拆解：

1. **叙事策略**：文章用了什么叙事框架？（英雄之旅 / 悬疑破案 / 横向对比 / 对话体……）
2. **结构拆解**：把文章切成段落级的功能块，标注每段的叙事角色（钩子 / 方法论 / 转折 / 结论 / 收束）
3. **关键技法**：哪些写作手法是这篇文章的亮点？具体到句子级别举例
4. **语言特征**：用 3-5 句话概括这篇文章的语感（正式/随意、冷静/热情、技术/生活化……）

拆解完成后，在末尾写一段「跨文章共性模式」，总结所有范文中反复出现的风格特征。

### 3. 行文风格指南（references/行文风格指南.md）

基于少数派创作手册风格指南，可根据个人偏好调整。一般无需修改。

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

安装完成后执行 `/reload-plugins` 重新加载。

## 截图脚本

`scripts/screenshot.py` 扫描目录下所有 `.html` 文件，从 `body` 的 CSS 尺寸读取宽高后截图。每张图的尺寸由 HTML 自己定义，无需在脚本中配置。

```bash
python3 scripts/screenshot.py <images-directory>
```

## 致谢

- `references/行文风格指南.md` 基于 [少数派风格指南](https://manual.sspai.com/rules/style/) 精简，保留了与行文规范直接相关的内容。原文采用 [知识共享署名 4.0 国际许可协议](https://creativecommons.org/licenses/by/4.0/deed.zh-hans) 进行许可。
- 写作工作流设计参考了 [mp-article-writor](https://github.com/balabalabalading/mp-article-writor)。
