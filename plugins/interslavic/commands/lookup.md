---
description: Look up words in the Interslavic dictionary
argument-hint: <word> [word2] [word3] ...
allowed-tools: Bash(python:*)
---

Look up the following word(s) in the Interslavic dictionary: $ARGUMENTS

Use the dictionary tool:
```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/translate/translate.py --json $ARGUMENTS
```

Present results showing:
- The Interslavic form (ISV)
- Part of speech
- English translation
- Intelligibility ratings across Slavic languages
- One example Slavic translation (e.g., Russian or Polish) for context

If multiple matches exist, briefly explain the differences (meaning, part of speech, or type/frequency).
