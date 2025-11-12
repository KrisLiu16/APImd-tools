# APImd Tools

APImd Tools 提供了一组用于根据结构化定义生成 Markdown 后端 API 文档的命令行工具。通过一份 YAML 或 JSON 配置文件即可快速输出符合规范的接口文档，避免重复编写 Markdown。

## 特性

- ✅ 支持 YAML 和 JSON 配置文件
- ✅ 自动生成带编号的小节标题、请求/响应表格与示例
- ✅ 请求参数支持路径参数、查询参数、请求体参数、Header 等多种形式
- ✅ 响应信息支持字段说明、示例、错误码等拓展
- ✅ 可扩展的文档模型，方便按照团队规范进行定制

## 快速开始

```bash
pip install -e .
```

如需渲染 YAML 定义，请额外安装可选依赖：

```bash
pip install PyYAML
```

示例渲染命令：

```bash
apimd render examples/quotas.json --output docs/quotas.md
```

运行后会在 `docs/quotas.md` 中生成 Markdown 文档。若希望直接查看渲染结果，可省略 `--output` 参数让内容输出到终端。

常用命令：

- `apimd render <definition>`：渲染 Markdown 文档
- `apimd render <definition> --no-numbering`：关闭自动编号
- `apimd validate <definition>`：仅校验定义文件是否有效

## 可视化文档向导（Node.js）

如果希望通过可视化页面引导填写接口信息、实时生成 Markdown，可以启动随项目提供的 Node.js 前端：

```bash
cd web
npm install
npm run dev
```

随后访问终端中提示的地址（默认 `http://localhost:5173`）。页面左侧可以维护文档标题、简介以及多个接口条目，支持：

- 增删接口条目、填写请求方式、路径、简介等元信息
- 管理请求头、请求体字段（含必填与说明）
- 为请求与响应添加示例片段，自动推断代码块语言
- 右侧实时预览规范化的 Markdown 文档，并一键复制到剪贴板

生成的 Markdown 风格与 CLI 工具保持一致，可直接保存或粘贴到团队文档中。
