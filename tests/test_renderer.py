from apimd_tools.document import Document
from apimd_tools.renderer import MarkdownRenderer


def test_render_from_dictionary() -> None:
    data = {
        "title": "GPU 资源配额接口文档",
        "sections": [
            {
                "endpoints": [
                    {
                        "title": "资源配额修改接口",
                        "status": "新接口",
                        "summary": "用于修改某配额",
                        "method": "PUT",
                        "path": "/api/v1/quotas/:tenant",
                        "headers": [
                            {"name": "Content-type", "value": "application/json"},
                            {"name": "Authorization", "value": "Bearer {token}"},
                        ],
                        "request": {
                            "parameter_groups": [
                                {
                                    "title": "请求体参数",
                                    "items": [
                                        {
                                            "name": "region",
                                            "type": "string",
                                            "required": True,
                                            "description": "资源选区",
                                        },
                                        {
                                            "name": "quota_source",
                                            "type": "string",
                                            "required": True,
                                            "description": "配额来源",
                                            "enum": ["purchase", "assign"],
                                        },
                                    ],
                                }
                            ],
                            "examples": [
                                {
                                    "title": "请求示例",
                                    "language": "JSON",
                                    "content": "{\n  \"region\": \"TW\"\n}",
                                }
                            ],
                        },
                        "response": {
                            "examples": [
                                {
                                    "title": "响应示例",
                                    "language": "JSON",
                                    "content": "{\n  \"code\": 0\n}",
                                }
                            ]
                        },
                    }
                ]
            }
        ],
    }

    document = Document.from_dict(data)
    renderer = MarkdownRenderer()
    markdown = renderer.render(document)

    assert markdown.startswith("# GPU 资源配额接口文档")
    assert "## 1. 资源配额修改接口（新接口）" in markdown
    assert "- **请求方式**: `PUT`" in markdown
    assert "`quota_source`" in markdown
    assert "可选值: purchase/assign" in markdown
