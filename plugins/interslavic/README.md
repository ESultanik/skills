# Interslavic translation

Translate between Interslavic, English, and other Slavic languages, or look up
vocabulary, in Claude Code and Codex. The bundled Python dictionary helper uses
only the standard library and supports Python 3.9 or later. Repository validation
uses Python 3.13 through `uv`.

## Install

Claude Code:

```text
/plugin marketplace add esultanik/skills
/plugin install interslavic@esultanik-skills
```

Codex CLI:

```sh
codex plugin marketplace add ESultanik/skills
codex plugin add interslavic@esultanik-skills
```

## Look up words

Use `/interslavic:lookup water fire` in Claude Code or
`$interslavic:lookup water fire` in Codex.
Results show the Interslavic form, part of speech, English meaning,
intelligibility ratings, and related Slavic forms.

## Translate text

Use `/interslavic:translate Hello, world` in Claude Code or
`$interslavic:translate Hello, world` in Codex. You can also select either skill
in Codex's `/skills` menu.
Specify the target language when you want to override inferred direction.

The skill looks up source vocabulary and applies Interslavic grammar. It uses
Latin-script Interslavic unless you request Cyrillic. Recognizable Interslavic
defaults to English translation; other input defaults to Interslavic.

Supported dictionary languages are ISV, EN, RU, UK, BE, PL, CS, SK, SL, HR, SR, MK,
BG, CU, DE, NL, and EO.

## Dictionary cache

The first lookup downloads the public dictionary into `~/.cache/interslavic/`.
Later lookups use SQLite. The helper's `--refresh` flag replaces the cache and
`--info` reports its metadata. Both skills locate the helper relative to their
installed package, so you can invoke them from any repository.

## License

AGPL-3.0
