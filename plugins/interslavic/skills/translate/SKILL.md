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

The script outputs matching entries with translations in all available languages.

**Human-readable output:**
```
=== Results for "water" (1 match) ===

[ISV] voda
  EN: water
  RU: вода
  UK: вода
  PL: woda
  ...

Total: 1 match
```

**JSON output (recommended for translation):**
```bash
python ./translate.py --json water
```
```json
[
  {
    "isv": "voda",
    "addition": "(vody)",
    "partofspeech": "f.",
    "type": "1",
    "en": "water",
    "ru": "вода",
    "uk": "вода",
    "pl": "woda",
    "intelligibility": "bg+ cs+ hr+ mk+ pl+ ru+ sk+ sl+ sr+ uk+",
    "using_example": "Voda jest žitje!",
    ...
  }
]
```
The JSON format includes all metadata fields useful for choosing the correct translation.

## Instructions for Translation

### Translating INTO Interslavic

When the user asks to translate text into Interslavic:

1. **Look up every content word** in the input text using the dictionary with JSON output:
   ```bash
   python ./translate.py --json <word1> <word2> <word3> ...
   ```
   Run the script on all words to find their Interslavic equivalents. Use `--json` for structured output that includes metadata useful for translation.

2. **Use Latin script by default.** Output Interslavic in Roman/Latin characters unless the user explicitly requests Cyrillic.

3. **For grammar and sentence construction:**
   - The dictionary provides individual word translations, not grammatical rules
   - When unsure about correct Interslavic grammar (verb conjugations, noun declensions, word order), draw on your knowledge of other Slavic languages
   - Aim for constructions that maximize mutual intelligibility across the Slavic language family
   - When in doubt, prefer forms that are common across multiple Slavic languages (e.g., SVO word order is widely understood)

4. **Handle ambiguity:** If multiple dictionary entries match, choose the one whose meaning best fits the context. Consider the part of speech (noun, verb, adjective) indicated in the results.

### Translating FROM Interslavic

When translating Interslavic text to another language:

1. Look up ISV words in the dictionary to find equivalents in the target language
2. The dictionary includes translations for EN, RU, UK, PL, CS, HR, BG, and many other languages

### Single Word Lookups

For simple "How do you say X?" questions:

1. Run: `python ./translate.py <word>`
2. Present the ISV translation along with related Slavic forms if helpful for context

### Handling Multiple Matches

The dictionary uses substring matching, so searches may return multiple entries. Review all matches and select the most appropriate based on:
- Part of speech (partofspeech field)
- Semantic context
- Frequency (higher frequency words are more common)

## Key Dictionary Fields

When using `--json` output, entries include these useful fields for translation:

### `partofspeech`
Grammatical category of the word. Common values:
- `m.` / `f.` / `n.` - masculine/feminine/neuter noun
- `adj.` - adjective
- `v.tr.` / `v.intr.` - transitive/intransitive verb
- `pf.` / `ipf.` - perfective/imperfective aspect
- `conj.` - conjunction
- `prep.` - preposition
- `adv.` - adverb

### `intelligibility`
Cross-Slavic intelligibility ratings showing how well the word is understood across languages. Format: `bg+ cs+ hr+ ru-` where language codes have `+` (well understood) or `-` (less understood). Prefer entries with more `+` ratings for broader comprehension.

### `using_example`
Example sentence showing the word in context. Helps disambiguate meaning when multiple entries match a search term.

### `type`
Entry classification indicating word status. Values (inferred from distribution analysis):
- `1` (74% of entries) - Standard/core vocabulary - **prefer these for translation**
- `2` (18%) - Less common or alternate forms
- `3` (2.4%) - Specialized/technical vocabulary
- `4` (0.2%) - Rare or archaic forms
- `5` (0.7%) - Neologisms/newer additions
- `#1`, `#2`, `#3` - Numbered variant markers
- (empty) - Unclassified entries

*Note: Type meanings are inferred from analyzing entry patterns, not from official documentation.*

## Important: Non-Standard ISV Characters

The source dictionary occasionally contains words with non-standard characters borrowed from other Slavic languages (e.g., Polish `ę`, `ą`). When translating INTO Interslavic, replace these with standard Interslavic equivalents:

| Non-standard | Replace with |
|--------------|--------------|
| ę | e |
| ą | a |
| ų | u |
| ȯ | o |
| ė | e |
| å | a |
| ń | n |
| ť | t |
| ľ | l |
| ŕ | r |
| ď | d |
| ś | s |
| ź | z |
| ć | c |

Standard ISV characters (`č`, `š`, `ž`, `ě`) should be preserved.

## About Interslavic

Interslavic (Medžuslovjansky) is a zonal constructed language designed to be mutually intelligible to speakers of Slavic languages. It serves as a lingua franca for the Slavic world, similar to how Latin functions in Romance language contexts.

Key features:
- Based on common Slavic vocabulary and grammar
- Uses both Latin and Cyrillic scripts
- Understandable to speakers of Russian, Polish, Czech, Croatian, and other Slavic languages without prior study
