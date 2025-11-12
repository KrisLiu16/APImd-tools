"""Data models for API documentation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Header:
    name: str
    value: str
    description: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "Header":
        return cls(
            name=data["name"],
            value=data["value"],
            description=data.get("description"),
        )


@dataclass
class Parameter:
    name: str
    type: str
    required: Optional[bool] = None
    description: str = ""
    default: Optional[str] = None
    example: Optional[str] = None
    enum: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> "Parameter":
        enum = data.get("enum") or []
        notes = data.get("notes") or []
        return cls(
            name=data["name"],
            type=data.get("type", ""),
            required=data.get("required"),
            description=data.get("description", ""),
            default=data.get("default"),
            example=data.get("example"),
            enum=list(enum),
            notes=list(notes),
        )


@dataclass
class ParameterGroup:
    title: str
    parameters: List[Parameter]
    description: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "ParameterGroup":
        parameters = [Parameter.from_dict(item) for item in data.get("items", [])]
        return cls(
            title=data.get("title", ""),
            parameters=parameters,
            description=data.get("description"),
        )


@dataclass
class Example:
    title: str
    content: str
    language: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> "Example":
        return cls(
            title=data.get("title", "示例"),
            content=data.get("content", ""),
            language=data.get("language", ""),
        )


@dataclass
class ErrorItem:
    code: str
    message: str
    description: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "ErrorItem":
        return cls(
            code=str(data.get("code", "")),
            message=data.get("message", ""),
            description=data.get("description"),
        )


@dataclass
class ErrorGroup:
    title: str
    items: List[ErrorItem]

    @classmethod
    def from_dict(cls, data: dict) -> "ErrorGroup":
        items = [ErrorItem.from_dict(item) for item in data.get("items", [])]
        return cls(
            title=data.get("title", "错误码"),
            items=items,
        )


@dataclass
class RequestBlock:
    description: Optional[str]
    parameter_groups: List[ParameterGroup]
    examples: List[Example]

    @classmethod
    def from_dict(cls, data: dict) -> "RequestBlock":
        parameter_groups = [
            ParameterGroup.from_dict(group)
            for group in data.get("parameter_groups", [])
        ]
        examples = [Example.from_dict(item) for item in data.get("examples", [])]
        return cls(
            description=data.get("description"),
            parameter_groups=parameter_groups,
            examples=examples,
        )


@dataclass
class ResponseBlock:
    description: Optional[str]
    parameter_groups: List[ParameterGroup]
    examples: List[Example]
    errors: List[ErrorGroup]

    @classmethod
    def from_dict(cls, data: dict) -> "ResponseBlock":
        parameter_groups = [
            ParameterGroup.from_dict(group)
            for group in data.get("parameter_groups", [])
        ]
        examples = [Example.from_dict(item) for item in data.get("examples", [])]
        errors = [ErrorGroup.from_dict(item) for item in data.get("errors", [])]
        return cls(
            description=data.get("description"),
            parameter_groups=parameter_groups,
            examples=examples,
            errors=errors,
        )


@dataclass
class Endpoint:
    identifier: Optional[str]
    title: str
    status: Optional[str]
    summary: Optional[str]
    method: str
    path: str
    headers: List[Header]
    request: Optional[RequestBlock]
    response: Optional[ResponseBlock]
    notes: List[str]

    @classmethod
    def from_dict(cls, data: dict) -> "Endpoint":
        headers = [Header.from_dict(item) for item in data.get("headers", [])]
        request = data.get("request")
        response = data.get("response")
        return cls(
            identifier=data.get("id"),
            title=data.get("title", ""),
            status=data.get("status"),
            summary=data.get("summary"),
            method=data.get("method", "GET"),
            path=data.get("path", ""),
            headers=headers,
            request=RequestBlock.from_dict(request) if request else None,
            response=ResponseBlock.from_dict(response) if response else None,
            notes=data.get("notes", []),
        )


@dataclass
class Section:
    title: str
    description: Optional[str]
    endpoints: List[Endpoint]

    @classmethod
    def from_dict(cls, data: dict) -> "Section":
        endpoints = [Endpoint.from_dict(item) for item in data.get("endpoints", [])]
        return cls(
            title=data.get("title", ""),
            description=data.get("description"),
            endpoints=endpoints,
        )


@dataclass
class Document:
    title: str
    description: Optional[str]
    sections: List[Section]

    @classmethod
    def from_dict(cls, data: dict) -> "Document":
        sections = [Section.from_dict(item) for item in data.get("sections", [])]
        return cls(
            title=data.get("title", ""),
            description=data.get("description"),
            sections=sections,
        )
