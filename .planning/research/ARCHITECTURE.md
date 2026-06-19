# Architecture Research: Kworqs Shopify Printer Pipeline

## Current Architecture (Working)

```
┌─────────────────┐
│   Shopify       │
│   Store         │
└────────┬────────┘
         │ API Poll
         ▼
┌─────────────────┐
│  shopify-skill  │
│  (Order Fetch)  │
└────────┬────────┘
         │ publish
         ▼
┌─────────────────┐
│Dilmun Protocol  │
│  (Middleware)   │
└────────┬────────┘
         │ subscribe
         ▼
┌─────────────────┐
│ goon-plates     │
│  (Blender)      │
└────────┬────────┘
         │ export
         ▼
┌─────────────────┐
│ Printer Queue   │
│  K2/Bambu       │
└─────────────────┘
```

## Proposed Architecture (Formal)

```
┌────────────────────────────────────────┐
│         Shopify Printer Pipeline       │
└─────────────────┬──────────────────────┘
                  │
    ┌─────────────┼─────────────┐
    │             │             │
    ▼             ▼             ▼
┌─────────┐  ┌──────────┐  ┌───────────┐
│ Shopify │  │ Dilmun   │  │ Blender   │
│ Skill   │──│ Protocol │──│ MCP Skill │
└─────────┘  └──────────┘  └─────┬─────┘
                                  │
                            ┌─────┴─────┐
                            │           │
                            ▼           ▼
                       ┌────────┐  ┌────────┐
                       │ K2     │  │ Bambu  │
                       │ Queue  │  │ Queue  │
                       └────────┘  └────────┘
```

## Component Boundaries

### 1. Shopify Skill

- **Responsibility**: Order intake, validation
- **Events**: `order.received`, `order.failed`
- **Output**: Order data with text variant

### 2. Dilmun Protocol

- **Responsibility**: Orchestration, state management
- **Events**: `plate.create`, `plate.complete`, `plate.failed`
- **Storage**: `fact/` partition for plate status

### 3. Blender-MCP Skill

- **Responsibility**: Geometry generation
- **Events**: `geometry.generate`, `geometry.export`
- **Output**: 3MF file

### 4. Dispatch Layer

- **Responsibility**: Route to correct printer
- **Criteria**: Printer type, warranty requirements
- **Output**: Queue entry in Moonraker or Bambu

## Data Flow

1. **Order Received**
   - Shopify API → `order.received` event
   - Dilmun stores: `fact/order/{id} = pending`

2. **Plate Creation**
   - Event → Blender-MCP → 3MF export
   - Dilmun updates: `fact/plate/{id} = complete`

3. **Dispatch**
   - Check printer type
   - Route to K2 (auto) or Bambu (manual)
   - Update: `fact/dispatch/{id} = queued`

## Build Order

| Phase | Component | Dependencies |
|-------|-----------|--------------|
| 1 | Shopify Skill Integration | None |
| 2 | Dilmun Protocol Wiring | Shopify Skill |
| 3 | Blender-MCP Integration | Dilmun Protocol |
| 4 | Export Pipeline | Blender-MCP |
| 5 | Dispatch Logic | Export Pipeline |

---
*Confidence: Medium (needs blender-mcp-goon-plates API verification)*
