---
name: lookup
description: >-
  Look up words in the Interslavic cross-language dictionary and show meanings,
  related Slavic forms, parts of speech, and intelligibility. Use for standalone
  vocabulary searches rather than translating a passage.
---

# Look up Interslavic vocabulary

## Contents

- [Lookup workflow](#lookup-workflow)

## Lookup workflow

Use the word or words from the user's request. Ask for them if missing. Resolve
the bundled helper at `skills/translate/translate.py` from this installed plugin's
location: `lookup` and `translate` are sibling skill directories. Do not resolve
it from the user's working directory or require `${CLAUDE_PLUGIN_ROOT}`.

Set `dictionary_tool` to that absolute helper path, then run a JSON lookup:

```sh
uv run --python 3.13 --no-project "$dictionary_tool" --json "water"
```

Pass the user's words as individually quoted arguments, never evaluated shell
text. Use `--lang CODE` to keep results with a translation in that language;
Searches still span all dictionary columns. The helper uses only the standard
library; an existing Python 3.9+ interpreter can
run it directly when `uv` is unavailable. Its first lookup downloads a public
dictionary into `~/.cache/interslavic/`; later lookups use SQLite. Report download
failures and empty results accurately.

Present the Interslavic form, part of speech, English meaning, intelligibility
ratings, and a related Slavic form. Include a usage example when present. Explain
competing substring matches using their meanings and parts of speech. Do not
invent missing fields or silently treat an unsuccessful lookup as a match.
