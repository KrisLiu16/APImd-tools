"""Command line interface for APImd Tools."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Iterable

from .loader import load_document
from .renderer import MarkdownRenderer


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate Markdown API documentation from structured definitions.",
    )
    subparsers = parser.add_subparsers(dest="command")

    render_parser = subparsers.add_parser("render", help="Render Markdown from a definition file.")
    render_parser.add_argument("definition", type=Path, help="Path to the YAML/JSON document definition.")
    render_parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Write the generated Markdown to the given file instead of stdout.",
    )
    render_parser.add_argument(
        "--no-numbering",
        action="store_true",
        help="Disable automatic numbering for endpoint headings.",
    )

    validate_parser = subparsers.add_parser("validate", help="Validate a definition file without rendering.")
    validate_parser.add_argument("definition", type=Path, help="Definition file to validate.")

    parser.set_defaults(func=_handle_root)
    render_parser.set_defaults(func=_handle_render)
    validate_parser.set_defaults(func=_handle_validate)
    return parser


def _handle_root(args: argparse.Namespace) -> int:
    build_parser().print_help()
    return 0


def _handle_render(args: argparse.Namespace) -> int:
    document = load_document(args.definition)
    renderer = MarkdownRenderer(show_numbering=not args.no_numbering)
    markdown = renderer.render(document)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(markdown, encoding="utf-8")
        print(f"Markdown written to {args.output}")
    else:
        sys.stdout.write(markdown)
    return 0


def _handle_validate(args: argparse.Namespace) -> int:
    load_document(args.definition)
    print("Definition is valid.")
    return 0


def main(argv: Iterable[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)
    func = getattr(args, "func", _handle_root)
    return func(args)


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    raise SystemExit(main())
