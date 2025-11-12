"""Render :class:`Document` into Markdown."""

from __future__ import annotations

from typing import Iterable, List

from .document import Document, Endpoint, ErrorGroup, Parameter, ParameterGroup


class MarkdownRenderer:
    """Render a :class:`Document` into Markdown text."""

    def __init__(self, show_numbering: bool = True) -> None:
        self.show_numbering = show_numbering

    def render(self, document: Document) -> str:
        lines: List[str] = []
        if document.title:
            lines.append(f"# {document.title}")
            lines.append("")
        if document.description:
            lines.extend(self._split_paragraph(document.description))
            lines.append("")

        endpoint_index = 1
        for section in document.sections:
            if section.title:
                lines.append(f"## {section.title}")
                lines.append("")
                if section.description:
                    lines.extend(self._split_paragraph(section.description))
                    lines.append("")
            for endpoint in section.endpoints:
                lines.extend(self._render_endpoint(endpoint, endpoint_index))
                lines.append("")
                endpoint_index += 1

        # Trim trailing blank lines
        while lines and lines[-1] == "":
            lines.pop()
        return "\n".join(lines) + "\n"

    def _render_endpoint(self, endpoint: Endpoint, index: int) -> List[str]:
        lines: List[str] = []
        title = endpoint.title
        if self.show_numbering:
            title_prefix = f"{index}. " if title else f"{index}."
        else:
            title_prefix = ""
        status = f"（{endpoint.status}）" if endpoint.status else ""
        heading = f"## {title_prefix}{title}{status}".rstrip()
        lines.append(heading)
        lines.append("")

        if endpoint.summary:
            lines.extend(self._split_paragraph(endpoint.summary))
            lines.append("")

        lines.extend(self._render_basic_info(endpoint))

        if endpoint.request:
            lines.extend(self._render_request(endpoint.request))
        if endpoint.response:
            lines.extend(self._render_response(endpoint.response))
        if endpoint.notes:
            lines.append("#### 备注")
            lines.append("")
            for note in endpoint.notes:
                lines.append(f"- {note}")
            lines.append("")
        return lines

    def _render_basic_info(self, endpoint: Endpoint) -> List[str]:
        lines = [
            f"- **请求方式**: `{endpoint.method.upper()}`",
            f"- **请求路径**: `{endpoint.path}`",
        ]
        if endpoint.headers:
            lines.append("- **请求头**:")
            for header in endpoint.headers:
                header_line = f"  - `{header.name}`: {header.value}"
                if header.description:
                    header_line += f" — {header.description}"
                lines.append(header_line)
        lines.append("")
        return lines

    def _render_request(self, request) -> List[str]:
        lines: List[str] = []
        if request.description:
            lines.extend(self._split_paragraph(request.description))
            lines.append("")
        for group in request.parameter_groups:
            lines.extend(self._render_parameter_group(group))
        for example in request.examples:
            lines.extend(self._render_example(example))
        return lines

    def _render_response(self, response) -> List[str]:
        lines: List[str] = []
        if response.description:
            lines.extend(self._split_paragraph(response.description))
            lines.append("")
        for group in response.parameter_groups:
            lines.extend(self._render_parameter_group(group))
        for example in response.examples:
            lines.extend(self._render_example(example))
        for error_group in response.errors:
            lines.extend(self._render_error_group(error_group))
        return lines

    def _render_parameter_group(self, group: ParameterGroup) -> List[str]:
        lines: List[str] = []
        if group.title:
            lines.append(f"#### {group.title}")
            lines.append("")
        if group.description:
            lines.extend(self._split_paragraph(group.description))
            lines.append("")
        lines.extend(self._render_parameter_table(group.parameters))
        lines.append("")
        return lines

    def _render_parameter_table(self, parameters: Iterable[Parameter]) -> List[str]:
        lines: List[str] = []
        lines.append("| 字段名 | 类型 | 必填 | 说明 |")
        lines.append("| ------ | ---- | ---- | ---- |")
        for parameter in parameters:
            name = f"`{parameter.name}`" if parameter.name else ""
            type_ = f"`{parameter.type}`" if parameter.type else ""
            required = self._format_required(parameter.required)
            description = self._compose_description(parameter)
            lines.append(
                f"| {name} | {type_} | {required} | {description} |"
            )
        if len(lines) == 2:
            lines.append("| （无） |  |  |  |")
        return lines

    def _compose_description(self, parameter: Parameter) -> str:
        parts: List[str] = []
        if parameter.description:
            parts.append(parameter.description)
        if parameter.default is not None:
            parts.append(f"默认值: {parameter.default}")
        if parameter.example is not None:
            parts.append(f"示例: {parameter.example}")
        if parameter.enum:
            parts.append("可选值: " + "/".join(str(item) for item in parameter.enum))
        if parameter.notes:
            parts.extend(parameter.notes)
        return "<br>".join(parts) if parts else ""

    def _render_example(self, example) -> List[str]:
        lines: List[str] = []
        lines.append(f"#### {example.title}")
        lines.append("")
        language = example.language or ""
        lines.append(f"```{language}")
        lines.append(example.content.rstrip())
        lines.append("```")
        lines.append("")
        return lines

    def _render_error_group(self, error_group: ErrorGroup) -> List[str]:
        lines: List[str] = []
        lines.append(f"#### {error_group.title}")
        lines.append("")
        lines.append("| 错误码 | 错误信息 | 说明 |")
        lines.append("| ------ | -------- | ---- |")
        for item in error_group.items:
            description = item.description or ""
            lines.append(f"| {item.code} | {item.message} | {description} |")
        lines.append("")
        return lines

    @staticmethod
    def _format_required(required) -> str:
        if required is None:
            return "-"
        return "是" if required else "否"

    @staticmethod
    def _split_paragraph(text: str) -> List[str]:
        if not text:
            return []
        return [line.rstrip() for line in text.splitlines()]
