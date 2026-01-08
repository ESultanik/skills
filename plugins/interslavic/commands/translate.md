---
description: Translate text to or from Interslavic
argument-hint: <text to translate>
allowed-tools: Bash(python:*)
---

Translate the following text: $ARGUMENTS

## Instructions

1. **Auto-detect direction**:
   - **Latin ISV markers** (č, š, ž, ě) or recognizable ISV words → translate FROM Interslavic to English
   - **Cyrillic script** → auto-detect source language (RU/UK/BG/SR/MK/BE) and translate INTO Interslavic
   - **Latin non-ISV** (English or other) → translate INTO Interslavic

2. **For translation INTO Interslavic:**
   - Look up each content word using: `python ${CLAUDE_PLUGIN_ROOT}/skills/translate/translate.py --json <words>`
   - For Cyrillic input, use `--lang <code>` to filter by source language
   - Use Latin script by default for output
   - Apply proper Interslavic grammar (draw on Slavic language knowledge)
   - Replace non-standard characters (ę→e, ą→a, ń→n, etc.) per standard ISV

3. **For translation FROM Interslavic:**
   - Look up ISV words to find English equivalents
   - Use the dictionary tool with --json for structured output

4. **Output format:**
   - Provide the translation
   - Optionally show 2-3 key vocabulary words with their ISV forms
