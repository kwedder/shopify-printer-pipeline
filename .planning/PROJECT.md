# Kworqs Shopify Printer Pipeline

## What This Is

A formal GSD-compliant pipeline that transforms Shopify custom text orders into production-ready 3D printable models via Blender-MCP. Integrates Shopify order intake, Dilmun Protocol orchestration, and Blender-MCP geometry generation to automate the creation of custom license plates and similar products.

## Core Value

Users can order custom text designs through Shopify and receive 3D printable 3MF files without manual intervention.

## Requirements

### Validated

(None yet - ship to validate)

### Active

- [ ] **SHOP-01**: Fetch pending orders from Shopify API
- [ ] **DILM-01**: Orchestrate workflow via Dilmun Protocol memory middleware
- [ ] **BLEND-01**: Generate 3D text geometry via Blender-MCP
- [ ] **BLEND-02**: Apply boolean operations to create final plate mesh
- [ ] **OUTPUT-01**: Export as 3MF with material/color data
- [ ] **DISPATCH-01**: Route completed models to appropriate printer queue (K2 Plus or Bambu)

### Out of Scope

- [ ] Custom Liquid frontend - Deferred to later iteration
- [ ] Real-time dashboard - Covered by existing lab telemetry
- [ ] Mobile app - Web-first pipeline

## Context

### Existing Skills Integration

1. **shopify-skill** (`~/.pi/skills/shopify-skill/`)
   - Provides `ShopifyClient` for API access
   - Fetches orders with pending financial status

2. **dilmun-protocol** (`~/.pi/skills/dilmun-protocol/`)
   - Memory middleware using `DilmunMemoryMiddleware`
   - Pub/Sub event coordination
   - Wedderburn-Kasczinski ring-theoretic memory management

3. **blender-mcp-goon-plates** (`~/skills1/skills/blender-mcp-goon-plates/`)
   - Blender-MCP skill for geometry generation
   - Text extrusion and boolean operations

4. **goon-plates** (`~/.pi/skills/goon-plates/`)
   - Existing Blender scripts for plate creation
   - Reference for current workflow

### Architecture Overview

```
Shopify Order
    ↓
shopify-skill (fetch)
    ↓
Dilmun Memory (order.received event)
    ↓
blender-mcp-goon-plates (geometry generation)
    ↓
3MF Output
    ↓
Printer Queue (K2 Plus or Bambu)
```

### Current Workflow (from lab telemetry)

1. **Intake**: Shopify Builder accepts custom text via Liquid
2. **QC Gate**: Manual review for geometry errors
3. **Blender Pipeline**: Potrace + Blender-MCP for CAD
4. **Dispatch**: Auto to K2 Plus, Manual to Bambu
5. **Telemetry**: 30s polling to dashboard

## Constraints

- **Tech Stack**: Python, Blender-MCP, Dilmun Protocol, Shopify API
- **Timeline**: Research phase first, then formalization
- **Dependencies**: Existing skills must be integrated
- **Naming**: Must not use "goon plates" - use "kworqs shopify printer pipeline"

## Key Decisions

| Decision | Rationale | Outcome |
| -------- | --------- | ------- |
| Project name | Avoid "goon plates" branding | shopify-printer-pipeline |
| Integration approach | Use existing blender-mcp-goon-plates | - Pending |
| v1 scope | Shopify → Dilmun → Blender-MCP → 3MF | - Pending |

---
*Last updated: 2026-06-18 after initialization*

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):

1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):

1. Full review of all sections
2. Core Value check - still the right priority?
3. Audit Out of Scope - reasons still valid?
4. Update Context with current state
