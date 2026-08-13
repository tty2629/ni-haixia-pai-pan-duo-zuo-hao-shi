# 倪海厦帮你排盘要多做好事 SKILL

用倪海厦老师的《天纪》解释天机道、地脉道、人间道、四柱、紫微斗数、六十四卦等内容。做了个蒸馏 SKILL，谢谢倪海厦老师。
拒绝排盘焦虑

## 重要说明

“倪海厦帮你排盘要多做好事 SKILL”是这个 Skill 的对外展示名称。当前版本本质上是**离线资料检索、排盘和传统术数参考 Skill**，不包含微信小程序前端或支付功能。

这个仓库只包含 Skill 指令、检索脚本和资料索引模板，**不包含任何《天纪》原始书籍或你的私人资料**。每位使用者都需要自己准备有权使用的本地资料，并在聊天平台中指定资料目录或上传相关文件。

一个 Skill 不能自动注入到所有聊天平台。这个仓库提供通用的 `SKILL.md`，可以被支持自定义指令、项目文件、技能目录或知识库的工具复用；不同平台仍需要按各自方式导入。

Skill 的内部安装标识为 `ni-haixia-pai-pan-duo-zuo-hao-shi`。平台通常用这个英文小写标识来安装和调用，中文名称用于展示和搜索。

## 文件结构

```text
SKILL.md                         核心指令
agents/openai.yaml               支持 Skill 元数据的界面配置
scripts/search_sources.py        离线资料检索脚本
references/source-map.md         资料分类和检索路由模板
```

## 在 Codex 中安装

将整个仓库复制到 Codex skills 目录：

```bash
git clone <仓库地址> ~/.codex/skills/ni-haixia-pai-pan-duo-zuo-hao-shi
```

然后把本地资料目录设置为环境变量：

```bash
export NI_HAIXIA_TIANJI_ROOT="/path/to/你的天纪资料"
```

也可以在请求中直接指定目录：

```text
请使用 ni-haixia-pai-pan-duo-zuo-hao-shi，资料目录是 /path/to/我的天纪资料。
帮我查找“紫微四化”相关内容。
```

## 在其他聊天平台中使用

如果平台支持上传 Markdown 文件、项目级 instructions、system prompt 或知识库：

1. 导入 `SKILL.md`。
2. 按需导入 `references/source-map.md`。
3. 把你的本地资料上传到该平台允许的私有知识库，或使用该平台的本地文件连接能力。
4. 在对话中明确要求“只使用我提供的本地资料，不联网”。

如果平台不支持本地目录访问，单独导入 `SKILL.md` 只能提供工作流程，不能凭空提供《天纪》原文；需要同时上传资料或粘贴相关章节。

## 直接运行检索脚本

```bash
python3 scripts/search_sources.py "紫微" \
  --root "/path/to/你的天纪资料" \
  --max-files 10 \
  --context 120
```

支持检索：TXT、Markdown、CSV、DOCX、XLSX、PDF 和部分 legacy DOC 文件。PDF 和 DOC 的全文提取取决于本机是否安装 `pdftotext`、`textutil` 或 `antiword`。

## 使用边界

这个 Skill 将术数解读定位为传统资料框架下的参考，不把排盘或预测说成经过科学验证的事实。涉及健康、法律、投资、婚姻或合作等现实决定时，应同时检查可观察的行为、合同、财务记录和专业意见。

## 示例问题

```text
只使用我提供的本地《天纪》资料，帮我找出“流年卦”的完整起法；找不到公式时请明确说不确定，不要自行补公式。

请按本地资料排这个人的四柱，并分开列出：计算结果、资料原文口径、你的谨慎综合判断。

请比较两个人的合作适配度，但不要把八字当成人品证明；请同时列出需要写进合作合同的现实条款。
```
