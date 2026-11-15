---
name: translate
description: >-
  Translate text between Interslavic, English, and other Slavic languages using
  the bundled cross-language dictionary. Use for text translation or vocabulary
  selection during translation; use lookup for a standalone dictionary search.
---

# Translate Interslavic

## Contents

- [Translation workflow](#translation-workflow)
- [Dictionary tool](#dictionary-tool)
- [Supported languages](#supported-languages)
- [Dictionary fields](#dictionary-fields)
- [Standard Interslavic characters](#standard-interslavic-characters)

## Translation workflow

Use the user's text and requested target language as input. Ask for missing text
or an ambiguous target. Otherwise, infer direction: recognizable Interslavic words
or Latin ISV markers such as č, š, ž, and ě suggest translation from Interslavic to
English; Cyrillic suggests a source such as Russian, Ukrainian, Bulgarian, or
Serbian; other Latin text defaults to translation into Interslavic. A marker alone
is not conclusive because other Slavic languages share these characters.

Look up every content word when translating into Interslavic. For translation
from Interslavic, look up the source vocabulary to choose the target meaning.
Use JSON output and batch searches when useful. `--lang CODE` keeps results with
a translation in that language; it does not restrict the searched columns.
The tool performs substring searches: inspect competing matches, parts of speech,
meanings, and usage examples before choosing a form.

Use Latin script for Interslavic unless the user requests Cyrillic. Apply
Interslavic grammar, inflection, and word order after choosing dictionary forms;
the dictionary is not a grammar engine. Prefer forms broadly understandable
across Slavic languages, using the intelligibility information when available.
Do not invent a dictionary match when the tool fails or finds none; explain the
gap and qualify any proposed translation.

Return the translation and, when useful, two or three key vocabulary choices.

## Dictionary tool

Resolve `translate.py` from the directory containing this installed `SKILL.md`,
not from the user's working directory. Use the skill path supplied by the host to
obtain the absolute helper path. This works in both Claude Code and Codex without
`${CLAUDE_PLUGIN_ROOT}`. Set `dictionary_tool` to that resolved path and quote it
and every user-provided argument; never evaluate the text as shell code.

The helper uses Python's standard library. These examples use Python 3.13 via `uv`:

```sh
uv run --python 3.13 --no-project "$dictionary_tool" --json water fire
uv run --python 3.13 --no-project "$dictionary_tool" --json --lang ru "вода"
uv run --python 3.13 --no-project "$dictionary_tool" --info
```

An existing Python 3.9+ interpreter can run the helper directly when `uv` is
unavailable. Do not install dependencies or change the target repository to run it.
The first lookup downloads the public dictionary into `~/.cache/interslavic/`;
later lookups use SQLite. `--refresh` replaces this cache and `--info` reports its
metadata. Explain download failures instead of claiming a successful lookup.

## Supported languages

| Code | Language |
| --- | --- |
| ISV | Interslavic |
| EN | English |
| RU | Russian |
| UK | Ukrainian |
| BE | Belarusian |
| PL | Polish |
| CS | Czech |
| SK | Slovak |
| SL | Slovenian |
| HR | Croatian |
| SR | Serbian |
| MK | Macedonian |
| BG | Bulgarian |
| CU | Old Church Slavonic |
| DE | German |
| NL | Dutch |
| EO | Esperanto |

## Dictionary fields

JSON output contains dictionary records with language columns such as `isv`,
`en`, and `ru`. Use `partofspeech` to distinguish nouns, verbs, adjectives, and
aspect, and `using_example` to clarify meaning. `intelligibility` contains
language markers such as `bg+` and `ru-`, indicating greater or lower expected
intelligibility for those languages.

The `type` field appears to distinguish standard/core vocabulary (`1`) from less
common, specialized, archaic, or newer entries. This interpretation is inferred,
not an official guarantee; prioritize meaning and usage evidence over the code.

## Standard Interslavic characters

Some source entries contain non-standard characters. Normalize these when
producing Latin-script Interslavic, preserving standard č, š, ž, and ě:

| Source | Replacement |
| --- | --- |
| ę, ė | e |
| ą, å | a |
| ų | u |
| ȯ | o |
| ń | n |
| ť | t |
| ľ | l |
| ŕ | r |
| ď | d |
| ś | s |
| ź | z |
| ć | c |
