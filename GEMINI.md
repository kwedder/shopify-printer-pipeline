# Kworqs Shopify Printer Pipeline - GSD Context

This file provides GSD workflow guidance and current project context for AI agents.

## Project Overview

**Name:** Kworqs Shopify Printer Pipeline
**Goal:** Transform Shopify custom text orders into production-ready 3D printable models via Blender-MCP
**Core Value:** Users can order custom text designs through Shopify and receive 3D printable 3MF files without manual intervention.

## GSD Workflow Guidance

When working on this project, follow these GSD conventions:

1. **Phases and Plans**: Work in phases as defined in ROADMAP.md. Each phase contains 2-5 plans.
2. **Requirements Traceability**: Every plan must map to a requirement from REQUIREMENTS.md
3. **Verification**: After each phase, verify deliverables match success criteria
4. **Evolution**: Update PROJECT.md after phase transitions

## Current State

- **Phase**: Planning
- **Next Step**: `/gsd-discuss-phase 1` - gather context and clarify approach

## Key Files

| File | Purpose |
|------|---------|
| `.planning/PROJECT.md` | Living project context |
| `.planning/config.json` | Workflow configuration |
| `.planning/REQUIREMENTS.md` | Checkable requirements (REQ-IDs) |
| `.planning/ROADMAP.md` | Phased execution plan |
| `.planning/STATE.md` | Current project state |
| `.planning/research/` | Research findings |

## Integration Points

- **shopify-skill**: `~/.pi/skills/shopify-skill/` - Order intake
- **dilmun-protocol**: `~/.pi/skills/dilmun-protocol/` - Orchestration
- **blender-mcp-goon-plates**: `~/skills1/skills/blender-mcp-goon-plates/` - Geometry generation

## Commands

```bash
# Initialize Dilmun
cd ~/.pi/skills/dilmun-protocol
python scripts/fast_init.py --action init

# Fetch orders
python scripts/fast_init.py --action shopify-orders

# Run workflow
python scripts/fast_init.py --action workflow --text "YOURTEXT"
```

---
*Generated: 2026-06-18*
*For GSD workflow enforcement*
