---
description: Translate between English, Slavic languages, and Interslavic using a comprehensive cross-language dictionary
tags:
  - translation
  - slavic
  - interslavic
  - language
  - dictionary
---

# Interslavic Translation Skill

This skill provides translation between English, major Slavic languages, and Interslavic using the comprehensive Interslavic dictionary.

## Supported Languages

| Code | Language |
|------|----------|
| ISV | Interslavic |
| EN | English |
| RU | Russian |
| BE | Belarusian |
| UK | Ukrainian |
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

## Dictionary Lookup Tool

A Python script is provided at `./translate.py` for searching the Interslavic dictionary. The script downloads and caches the dictionary locally for fast lookups.

### Usage

```bash
# Basic search (substring matching)
python ./translate.py water

# Search multiple words
python ./translate.py water fire earth

# Filter by language
python ./translate.py --lang ru вода

# Output as JSON
python ./translate.py --json water

# Refresh the cached dictionary
python ./translate.py --refresh

# Show cache info
python ./translate.py --info
```

### First Run

On first run, the script automatically downloads and indexes the dictionary. This requires an internet connection. Subsequent searches use the local cache.

### Output Format

The script outputs matching entries with translations in all available languages:

```
=== Results for "water" (1 match) ===

[ISV] voda
  EN: water
  RU: вода
  UK: вода
  PL: woda
  HR: voda
  CS: voda
  BG: вода

Total: 1 match
```

## Instructions for Translation

When asked to translate text:

1. **Identify the source language** from context or ask the user
2. **Use the dictionary lookup tool** to find translations:
   ```bash
   python ./translate.py <word>
   ```
3. **For phrases**, look up individual content words
4. **Present translations** clearly with all available language variants

### Example Workflow

User asks: "How do you say 'water' in Interslavic?"

1. Run: `python ./translate.py water`
2. Find the ISV entry: `voda`
3. Respond with the translation and additional context if helpful

### Handling Multiple Matches

The dictionary uses substring matching, so a search may return multiple entries. Review all matches and select the most appropriate based on context.

## About Interslavic

Interslavic (Medžuslovjansky) is a zonal constructed language designed to be mutually intelligible to speakers of Slavic languages. It serves as a lingua franca for the Slavic world, similar to how Latin functions in Romance language contexts.

Key features:
- Based on common Slavic vocabulary and grammar
- Uses both Latin and Cyrillic scripts
- Understandable to speakers of Russian, Polish, Czech, Croatian, and other Slavic languages without prior study
