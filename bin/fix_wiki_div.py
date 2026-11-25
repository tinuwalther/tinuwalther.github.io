#!/usr/bin/env python3

"""Remove Jetpack Markdown wrappers and update Jekyll layouts."""

import argparse
import re
from pathlib import Path


def remove_jetpack_divs(content: str) -> tuple[str, int]:
    pattern = re.compile(
        r"<div\b[^>]*>|</div\s*>",
        re.IGNORECASE,
    )
    jetpack = re.compile(
        r"""class\s*=\s*["'][^"']*\bwp-block-jetpack-markdown\b[^"']*["']""",
        re.IGNORECASE,
    )

    stack = []
    remove = []

    for match in pattern.finditer(content):
        tag = match.group()

        if tag.lower().startswith("</"):
            if stack:
                opening, is_jetpack = stack.pop()

                if is_jetpack:
                    remove.append(opening.span())
                    remove.append(match.span())
        else:
            stack.append((match, bool(jetpack.search(tag))))

    for start, end in sorted(remove, reverse=True):
        content = content[:start] + content[end:]

    return content, len(remove) // 2


def replace_layout(content: str) -> tuple[str, int]:
    """Replace default layout with post in YAML front matter."""

    pattern = re.compile(
        r"\A(---\n)(.*?)(\n---(?:\n|$))",
        re.DOTALL,
    )

    match = pattern.match(content)

    if not match:
        return content, 0

    opening, frontmatter, closing = match.groups()

    frontmatter, count = re.subn(
        r"""^layout:[ \t]*(?:default|"default"|'default')[ \t]*$""",
        "layout: post",
        frontmatter,
        flags=re.MULTILINE,
    )

    if not count:
        return content, 0

    content = (
        opening
        + frontmatter
        + closing
        + content[match.end():]
    )

    return content, count


def replace_author(content: str) -> tuple[str, int]:
    """Replace Martin Walther with Tinu in YAML front matter."""

    pattern = re.compile(
        r"\A(---\n)(.*?)(\n---(?:\n|$))",
        re.DOTALL,
    )

    match = pattern.match(content)

    if not match:
        return content, 0

    opening, frontmatter, closing = match.groups()

    frontmatter, count = re.subn(
        r"""^author:[ \t]*(?:Martin Walther|"Martin Walther"|'Martin Walther')[ \t]*$""",
        "author: Tinu",
        frontmatter,
        flags=re.MULTILINE,
    )

    if not count:
        return content, 0

    content = (
        opening
        + frontmatter
        + closing
        + content[match.end():]
    )

    return content, count


def remove_wp_figures(content: str) -> tuple[str, int]:
    """Remove WordPress image figure wrappers."""

    pattern = re.compile(
        r"<figure\b[^>]*>|</figure\s*>",
        re.IGNORECASE,
    )

    wp_figure = re.compile(
        r"""class\s*=\s*["'][^"']*\bwp-block-image\b[^"']*["']""",
        re.IGNORECASE,
    )

    stack = []
    remove = []

    for match in pattern.finditer(content):
        tag = match.group()

        if tag.lower().startswith("</"):
            if stack:
                opening, is_wp_figure = stack.pop()

                if is_wp_figure:
                    remove.append(opening.span())
                    remove.append(match.span())
        else:
            stack.append((match, bool(wp_figure.search(tag))))

    for start, end in sorted(remove, reverse=True):
        content = content[:start] + content[end:]

    return content, len(remove) // 2


def main():
    parser = argparse.ArgumentParser(
        description="Remove WordPress wrappers and update Jekyll metadata."
    )
    parser.add_argument(
        "--path",
        type=Path,
        default=Path("_wiki"),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
    )
    args = parser.parse_args()

    if not args.path.is_dir():
        parser.error(f"Directory not found: {args.path}")

    updated = 0
    removed = 0
    figures = 0
    layouts = 0
    authors = 0

    for file in sorted(args.path.rglob("*.md")):
        content = file.read_text(encoding="utf-8")

        # Remove WordPress Jetpack DIV wrappers
        new_content, div_count = remove_jetpack_divs(content)

        # Remove WordPress figure wrappers
        new_content, figure_count = remove_wp_figures(new_content)

        # Replace Jekyll layout
        new_content, layout_count = replace_layout(new_content)

        # Replace author
        new_content, author_count = replace_author(new_content)

        if new_content == content:
            continue

        if not args.dry_run:
            file.write_text(new_content, encoding="utf-8")

        status = "WOULD UPDATE" if args.dry_run else "UPDATED"

        print(
            f"{status}: {file} "
            f"(wrappers: {div_count}, "
            f"figures: {figure_count}, "
            f"layouts: {layout_count}, "
            f"authors: {author_count})"
        )

        updated += 1
        removed += div_count
        figures += figure_count
        layouts += layout_count
        authors += author_count

    print()
    print(f"Affected files:   {updated}")
    print(f"Removed wrappers: {removed}")
    print(f"Removed figures:  {figures}")
    print(f"Updated layouts:  {layouts}")
    print(f"Updated authors:  {authors}")


if __name__ == "__main__":
    main()