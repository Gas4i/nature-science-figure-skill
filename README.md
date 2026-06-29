# Nature/Science Figure Skill

Unofficial Codex skill for creating, auditing, and packaging publication-style scientific data figures for Nature- or Science-oriented workflows.

This skill focuses on:

- journal-sized matplotlib figures;
- Nature/Science profile selection;
- data-driven chart choice;
- colorblind-aware palette presets;
- PPT-friendly SVG and transparent PNG export;
- visual QA for clipping, tick overlap, legend placement, and color-accessibility warnings.

## Installation

Copy this folder into your Codex skills directory:

```text
~/.codex/skills/nature-science-figure-skill
```

On Windows:

```text
C:\Users\<YOUR_USER>\.codex\skills\nature-science-figure-skill
```

Restart Codex or refresh the skill index after installation.

## Typical Use

Ask Codex to use this skill when you need a manuscript-style scientific figure, for example:

```text
Use nature-science-figure-skill to plot this CSV as a Nature-style figure for PPT assembly.
```

By default, the skill exports:

- editable `svg`;
- transparent high-resolution `png`;
- an audit/provenance note.

## Important Notes

This is an unofficial helper skill. It is not affiliated with, endorsed by, or certified by Nature, Springer Nature, Science, or AAAS.

The repository does not redistribute third-party journal guideline PDFs, article figures, or Illustrator templates. Official-source links and provenance notes are kept in `references/source-links.md`. Always verify current journal instructions before final submission.

Article-inspired palettes in this skill are approximate extractions for research-figure styling. They are not official journal palettes.

## License

MIT License. See `LICENSE`.
