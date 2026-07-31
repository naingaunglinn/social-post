# Skills

Skills in this repo are **vendored** — copied in, not installed via a package manager. Nothing
auto-updates. To refresh one, re-copy it from the upstream source listed below.

Claude Code discovers a skill only at `.claude/skills/<name>/SKILL.md`, and the `name:` in the
frontmatter must match the directory name.

## Local

| Skill | What it does |
|---|---|
| `night-ace-posts` | Social content batches + carousel/hero rendering via `design/night-ace-v2/`. |

## Vendored — Anthropic (Apache 2.0, `LICENSE.txt` in each folder)

Source: <https://github.com/anthropics/skills> — path `skills/<name>/`

| Skill | Notes |
|---|---|
| `frontend-design` | Design-thinking pass before writing UI code. Byte-identical to the copy in `anthropics/claude-code` under `plugins/frontend-design/`. |
| `theme-factory` | 10 preset themes. Needs `themes/` alongside `SKILL.md` — it reads them at runtime. |
| `canvas-design` | Posters / static art as PNG + PDF. Needs `canvas-fonts/` (~5.6 MB, OFL-licensed). Drop it only if you accept degraded output. |
| `brand-guidelines` | ⚠️ Ships with **Anthropic's** brand, not Night Ace's. See below. |

## Vendored — Figma (no license file upstream)

Source: <https://github.com/figma/mcp-server-guide> — path `skills/figma-design-to-code/`

| Skill | Notes |
|---|---|
| `figma-design-to-code` | Formerly `figma-implement-design`; renamed upstream at Skills v2.2.87. **Requires the Figma MCP server** — see below. |

Its `SKILL.md` links to a sibling `figma-generate-design` skill (code → Figma, the reverse
direction) that isn't vendored here, so that one relative link is dead. Add it if you ever need
to push designs back into Figma.

## Two things to fix before relying on these

### 1. `brand-guidelines` currently fights the Night Ace brand

Out of the box this skill enforces Anthropic's palette and typography. The repo's existing design
pipeline already uses:

- Ink `#141419` · paper `#F5F5F5` · accent `#2E6BFF` · grays `#55555C` / `#DFDFE4`
- Archivo VF (display) · IBM Plex Sans VF (body) · IBM Plex Mono (code/labels)

Until the tokens are swapped, this skill will pull generated artifacts *away* from brand.
Treat it as a template to rewrite, not a skill to use as-is.

### 2. `figma-design-to-code` needs the Figma MCP server

Connecting Figma inside a claude.ai chat does **not** carry over to Claude Code — it's a separate
connection, same as the Canva note in `night-ace-posts`:

```
claude mcp add --transport http figma https://mcp.figma.com/mcp
```

Then complete the OAuth flow it opens. Without it the skill loads but `get_design_context` fails.

## Known wart

`.claude/skills/SKILL.md` sits loose at the top of this directory. It's an older draft of
`night-ace-posts` and Claude Code will **never** load it — skills must live one level deeper, in
their own folder. Safe to delete.
