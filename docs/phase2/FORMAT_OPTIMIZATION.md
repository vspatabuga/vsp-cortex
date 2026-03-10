# FORMAT OPTIMIZATION & INTEROPERABILITY
**Phase 2 Component**  
**Status:** Planning  
**Last Updated:** 2026-03-10

## Objective
Standardisasi format data untuk interoperabilitas antara Markdown, Wiki, dan Logseq di ekosistem vsp-docs.

## Supported Formats

### 1. CommonMark (Base Format)
```markdown
# Heading
- Bullet point
[Link](URL)
```

### 2. Logseq Flavor
```markdown
- Concept A
  - Sub-concept
- [[Document A]]
- TODO Task
```

### 3. Wiki Format
```markdown
[[Internal Link]]
{backlinks}
Categories
```

## Metadata Standard
```yaml
---
title: Document Title
created: 2026-03-10T11:05:00Z
modified: 2026-03-10T11:05:00Z
author: Agent/Operator
tags: [tag1, tag2]
category: experiments | logs | decisions | knowledge
archive-source: vsp-cortex | copilot-ops | gemini-ops
---
```

## Conversion Tools
- pandoc: Markdown ↔ Logseq
- custom scripts: Format normalization
- validators: Metadata compliance

## Templates
Each archive category has template in `/templates/`
