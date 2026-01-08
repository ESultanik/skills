# Interslavic Translation Plugin

A Claude Code plugin for translating between English, major Slavic languages, and Interslavic.

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

## Installation

```
/plugin marketplace add esultanik/skills
/plugin install interslavic@esultanik-skills
```

## Commands

### /lookup

Look up words in the Interslavic dictionary.

```
/lookup <word> [word2] [word3] ...
```

Shows the ISV form, part of speech, English translation, and intelligibility ratings across Slavic languages.

### /translate

Translate text to or from Interslavic.

```
/translate <text to translate>
```

Auto-detects translation direction:
- Latin text with ISV markers (č, š, ž, ě) → translates from Interslavic to English
- Cyrillic text → detects source language and translates into Interslavic
- Other Latin text → translates into Interslavic

## Skills

### translate

Translate text between supported languages.

## License

AGPL-3.0
