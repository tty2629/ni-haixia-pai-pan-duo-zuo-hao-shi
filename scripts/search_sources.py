#!/usr/bin/env python3
"""Search a local Ni Haixia Tian Ji source directory."""

from __future__ import annotations

import argparse
import csv
import os
import subprocess
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


TEXT_EXTENSIONS = {".txt", ".md", ".csv"}
WORD_EXTENSIONS = {".docx"}
SHEET_EXTENSIONS = {".xlsx"}
PDF_EXTENSIONS = {".pdf"}
LEGACY_DOC_EXTENSIONS = {".doc"}


def normalize(value: str) -> str:
    return value.casefold()


def safe_read_text(path: Path) -> str:
    for encoding in ("utf-8", "utf-16", "gb18030", "big5", "latin-1"):
        try:
            return path.read_text(encoding=encoding, errors="ignore")
        except (OSError, UnicodeError):
            continue
    return ""


def docx_text(path: Path) -> str:
    try:
        with zipfile.ZipFile(path) as archive:
            names = [
                "word/document.xml",
                *[
                    name
                    for name in archive.namelist()
                    if name.startswith("word/header") or name.startswith("word/footer")
                ],
            ]
            parts: list[str] = []
            for name in names:
                if name not in archive.namelist():
                    continue
                root = ET.fromstring(archive.read(name))
                for node in root.iter():
                    if node.tag.endswith("}t") and node.text:
                        parts.append(node.text)
            return "\n".join(parts)
    except Exception:
        return ""


def xlsx_text(path: Path) -> str:
    try:
        with zipfile.ZipFile(path) as archive:
            shared_strings: list[str] = []
            if "xl/sharedStrings.xml" in archive.namelist():
                root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
                for si in root.iter():
                    if si.tag.endswith("}si"):
                        shared_strings.append(
                            "".join(node.text or "" for node in si.iter() if node.tag.endswith("}t"))
                        )

            values: list[str] = []
            for name in archive.namelist():
                if not name.startswith("xl/worksheets/sheet") or not name.endswith(".xml"):
                    continue
                root = ET.fromstring(archive.read(name))
                for cell in root.iter():
                    if not cell.tag.endswith("}c"):
                        continue
                    value_node = next(
                        (child for child in cell if child.tag.endswith("}v")),
                        None,
                    )
                    if value_node is None or value_node.text is None:
                        continue
                    if cell.attrib.get("t") == "s":
                        try:
                            values.append(shared_strings[int(value_node.text)])
                        except (ValueError, IndexError):
                            values.append(value_node.text)
                    else:
                        values.append(value_node.text)
            return "\n".join(values)
    except Exception:
        return ""


def command_exists(name: str) -> bool:
    try:
        subprocess.run(
            ["which", name],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )
        return True
    except (OSError, subprocess.CalledProcessError):
        return False


def pdf_text(path: Path) -> str:
    if not command_exists("pdftotext"):
        return ""
    try:
        result = subprocess.run(
            ["pdftotext", "-layout", str(path), "-"],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            timeout=30,
        )
        return result.stdout if result.returncode == 0 else ""
    except (OSError, subprocess.SubprocessError):
        return ""


def legacy_doc_text(path: Path) -> str:
    commands = [
        ["textutil", "-stdout", "-convert", "txt", str(path)],
        ["antiword", str(path)],
    ]
    for command in commands:
        if not command_exists(command[0]):
            continue
        try:
            result = subprocess.run(
                command,
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True,
                timeout=20,
            )
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout
        except (OSError, subprocess.SubprocessError):
            continue
    return ""


def extract_text(path: Path) -> str:
    suffix = path.suffix.casefold()
    if suffix in TEXT_EXTENSIONS:
        return safe_read_text(path)
    if suffix in WORD_EXTENSIONS:
        return docx_text(path)
    if suffix in SHEET_EXTENSIONS:
        return xlsx_text(path)
    if suffix in PDF_EXTENSIONS:
        return pdf_text(path)
    if suffix in LEGACY_DOC_EXTENSIONS:
        return legacy_doc_text(path)
    return ""


def iter_files(root: Path) -> list[Path]:
    ignored_names = {".DS_Store"}
    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file() and path.name not in ignored_names
    )


def snippets(text: str, needle: str, context: int, limit: int) -> list[str]:
    haystack = normalize(text)
    query = normalize(needle)
    found: list[str] = []
    start = 0
    while len(found) < limit:
        index = haystack.find(query, start)
        if index < 0:
            break
        left = max(0, index - context)
        right = min(len(text), index + len(needle) + context)
        found.append(" ".join(text[left:right].split()))
        start = index + len(query)
    return found


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", help="Keyword or phrase to search for.")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(os.environ.get("NI_HAIXIA_TIANJI_ROOT", ".")),
        help="Source root. Defaults to NI_HAIXIA_TIANJI_ROOT or the current directory.",
    )
    parser.add_argument("--names-only", action="store_true")
    parser.add_argument("--max-files", type=int, default=30)
    parser.add_argument("--context", type=int, default=70)
    parser.add_argument("--snippets", type=int, default=3)
    parser.add_argument("--csv", action="store_true")
    args = parser.parse_args()

    root = args.root.expanduser().resolve()
    if not root.exists():
        print(f"Source root not found: {root}", file=sys.stderr)
        return 2

    rows: list[tuple[str, str, str]] = []
    query_normalized = normalize(args.query)
    for path in iter_files(root):
        relative = str(path.relative_to(root))
        name_hit = query_normalized in normalize(relative)
        text_hits: list[str] = []
        if not args.names_only:
            text = extract_text(path)
            if text:
                text_hits = snippets(text, args.query, args.context, args.snippets)
        if name_hit or text_hits:
            rows.append((str(path), "filename" if name_hit else "content", " | ".join(text_hits)))
            if len(rows) >= args.max_files:
                break

    if args.csv:
        writer = csv.writer(sys.stdout)
        writer.writerow(["path", "match_type", "snippets"])
        writer.writerows(rows)
    else:
        for index, (path, match_type, hit_snippets) in enumerate(rows, 1):
            print(f"{index}. [{match_type}] {path}")
            if hit_snippets:
                print(f"   {hit_snippets}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
