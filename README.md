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
