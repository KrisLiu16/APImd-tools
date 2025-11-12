# API Markdown 可视化向导

这个项目提供了一个基于浏览器的界面，帮助你按照固定的规范编写后端 API 的 Markdown 文档。填写接口的名称、请求方式、路径、请求头、请求体字段以及请求/响应示例，右侧会实时展示生成的 Markdown 文档，方便复制或保存。

## 功能概览

- 支持维护多个接口条目，自动编号章节标题
- 图形化管理请求头与请求体字段，包含必填标记
- 请求与响应示例自动识别 JSON、cURL 等常见格式并渲染代码块
- 一键复制生成的 Markdown 文档
- 支持导入 OpenAPI JSON 文件，自动还原接口信息
- 内置默认请求头，开箱即用

## 一键启动

无需安装任何依赖，也不需要敲命令行。根据你的操作系统选择下面的方式即可：

- **Windows**：双击仓库根目录下的 `start-windows.bat`，系统会自动在默认浏览器中打开页面。
- **macOS**：首次右键点击 `start-macos.command` 选择“打开”，通过安全提示后，之后即可直接双击启动。
- **Linux**：给 `start-linux.sh` 添加可执行权限（`chmod +x start-linux.sh`），之后双击或在文件管理器中选择“在终端中运行”即可打开。

如果你更习惯手动操作，也可以直接双击 `public/index.html` 通过浏览器访问所有功能。

## 导入 OpenAPI JSON 的方法

1. 在页面左侧“接口列表”区域点击 **“导入 OpenAPI JSON”** 按钮。
2. 选择符合 OpenAPI 3.x 规范的 JSON 文件（通常是通过 Swagger、Apifox 等工具导出的接口描述）。
3. 工具会读取文档的标题、描述、路径与方法信息，同时尽可能填充请求头、参数表以及请求/响应示例。
4. 导入后仍然可以继续在界面中调整字段或补充示例内容，右侧 Markdown 预览会实时刷新。

## 目录结构

```
public/
  index.html   # 页面骨架
  app.js       # 表单逻辑和 Markdown 生成
  styles.css   # 页面样式
start-windows.bat   # Windows 下一键启动脚本
start-macos.command # macOS 下一键启动脚本
start-linux.sh      # Linux 下一键启动脚本
```

欢迎根据团队规范对字段或样式进行拓展。
