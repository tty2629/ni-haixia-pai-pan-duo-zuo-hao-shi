---
name: ni-haixia-pai-pan-duo-zuo-hao-shi
description: Use this skill for offline work with a user's local Ni Haixia Tian Ji study materials, including Tian Ji lectures, notes, Yi Jing, Zi Wei Dou Shu, four-pillars charts, hexagrams, feng shui, physiognomy, and related references. Use it to locate, extract, summarize, compare, or organize local source files, and to provide traditional-metaphysics readings grounded in the user's supplied materials.
---

# 倪海厦帮你排盘要多做好事 SKILL

## Scope

Use only the user's supplied local source library unless the user explicitly asks for outside research. This skill is platform-neutral: the source directory is configured by the user, not hard-coded to one computer.

This skill supports:

- Searching and extracting local Tian Ji materials.
- Summarizing lectures, notes, tables, and source passages.
- Comparing concepts across Tian Ji, Yi Jing, Zi Wei Dou Shu, four pillars, and hexagram references.
- Building study notes, reading outlines, flashcards, and source-grounded interpretations.
- Performing traditional metaphysics calculations when the required birth data and calculation rules are available in the local sources.

## Source directory

Before using the bundled search script, resolve the user's source directory in this order:

1. A path explicitly supplied in the current request.
2. `NI_HAIXIA_TIANJI_ROOT` environment variable.
3. A local path configured by the host platform.
4. Ask the user to provide or attach the source files.

Never assume that `/Users/...` or another machine-specific path exists on the current platform.

The bundled search helper accepts:

```bash
python3 scripts/search_sources.py "关键词" --root "/path/to/tianji-materials"
```

It can inspect text, Markdown, CSV, DOCX, XLSX, PDF, and legacy DOC files when the host has the corresponding extraction utility.

## Workflow

1. Identify whether the user wants source lookup, calculation, interpretation, summary, comparison, or a study artifact.
2. Resolve the source directory before making source-grounded claims.
3. Search filenames and text with `scripts/search_sources.py`.
4. Prefer primary Tian Ji works and detailed lecture notes over broad secondary references.
5. Inspect the relevant source passages before interpreting them.
6. Separate:
   - Calculated data, such as a chart, date conversion, or star placement.
   - What the local source says about that data.
   - The assistant's cautious synthesis.
7. State assumptions when birth location, calendar type, time zone, true solar time, 子时换日, or school-specific rules affect the result.
8. If the source material does not contain a complete formula, do not invent one. Report what is confirmed and what remains uncertain.

## Metaphysics and safety

- Present divination, fortune-telling, feng shui, physiognomy, and related interpretations as traditional/source-based frameworks, not verified facts.
- Use wording such as “按这套资料的说法”, “资料中把它解释为”, or “这是基于该排法的参考”.
- Do not make medical, legal, investment, or other high-stakes decisions from metaphysical material.
- Do not infer a person's honesty, criminality, health, or guaranteed future from a chart.
- For relationship, business, or financial questions, pair any traditional interpretation with practical checks based on observable behavior, contracts, records, and current circumstances.

## Citations

When using local material, cite the filename or path in the response. Do not upload the user's source library to a public repository unless the user has confirmed they have the rights and explicitly requests that upload.

## Calculation discipline

For birth-chart work:

- Confirm whether the date is Gregorian or lunar.
- Use the stated location and time zone.
- Check whether true solar time changes the hour pillar or hour branch.
- Identify the calendar boundary used for the year and month pillars.
- Declare the school-specific rules used for Zi Wei Dou Shu, four pillars, luck cycles, and hexagram calculations.
- Recalculate if a prior assumption changes.
- Avoid false precision when the birth time is approximate or close to a 子时/时辰 boundary.
