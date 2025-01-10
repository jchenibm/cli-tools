# cli-tools

Some cli tools to make my(your?) life easier

## 依赖工具

使用前请确保安装以下工具：

- `llm` - 用于命令行中与 LLM 交互
- `pdftotext` - 用于将 PDF 转换为文本
- `pptx2md` - 用于将 PPT/PPTX 转换为 Markdown
- `glow` - 用于在终端中渲染 Markdown
- `pbpaste` (MacOS) 或 `xclip` (Linux) - 用于剪贴板操作

## 安装依赖

### MacOS

```bash
brew install glow pkg-config poppler python
pip install llm pptx2md pdftotext
```

### Linux (Ubuntu/Debian)

```bash
# 安装 llm
pip install llm
# 安装 pdftotext
sudo apt-get install poppler-utils
# 安装 glow
sudo snap install glow
# 安装 pptx2md
pip install pptx2md
# 安装剪贴板工具
sudo apt-get install xclip
```

## 工具说明

### doc-chat

与文档进行对话的交互式工具。支持多种输入源：
- 本地文件 (.md, .txt, .pdf, .ppt, .pptx)
- 剪贴板内容
- 网页 URL

#### 使用方法

```bash
# 基本用法
./doc-chat document.md # 与 Markdown 文件对话
./doc-chat document.pdf # 与 PDF 文件对话
./doc-chat presentation.pptx # 与 PPT 文件对话
./doc-chat clipboard # 与剪贴板内容对话
./doc-chat https://example.com # 与网页内容对话

# 使用特定模型
./doc-chat -m gpt-4 document.md
./doc-chat -m claude-3-opus document.pdf

# 使用本地模型
./doc-chat -l document.md
```

### doc-qa

向文档提出单个问题并获取答案的工具。支持与 doc-chat 相同的文件格式。

#### 使用方法

```bash
# 基本用法
./doc-qa document.pdf "这篇文档的主要内容是什么？"
./doc-qa presentation.pptx "总结一下这个演示文稿"

# 使用特定模型
./doc-qa -m qwen2:latest document.md "文档的关键点是什么？"
```

## 注意事项

1. 首次使用前请确保已配置 LLM API 密钥
2. 对于大文件，处理可能需要一些时间
3. URL 访问需要确保网络连接正常
4. 使用剪贴板功能时确保有内容在剪贴板中