# Kworqs Shopify Printer Pipeline

A pipeline that transforms Shopify custom text orders into production-ready 3D printable models.

## Overview

This pipeline integrates:

- **shopify-skill** - Order intake from Shopify API
- **Dilmun Protocol** - Memory middleware for orchestration
- **Blender** - 3D geometry generation and boolean operations

## Architecture

```
Shopify Order
    ↓
shopify-skill (fetch)
    ↓
Dilmun Memory (order.received event)
    ↓
Blender (text extrusion + boolean ops)
    ↓
STL Output (to slicer)
    ↓
Printer Queue (K2 Plus or Bambu)
```

## Quick Start

```bash
# 1. Initialize Dilmun Protocol
python scripts/run.py --action init

# 2. Fetch Shopify orders
python scripts/run.py --action shopify-orders

# 3. Run workflow
python scripts/run.py --action workflow --text "YOURTEXT"
```

## Scripts

| Script | Purpose |
|--------|---------|
| `run.py` | Unified runner for all operations |
| `optimized_run.py` | Fast operations (<200ms) |
| `shopify_orders.py` | Fetch pending Shopify orders |
| `pipeline.py` | Main pipeline orchestrator |
| `create_plate_from_order.py` | Main plate creation (Blender) |
| `create_goon_plate_english.py` | English text plate generator |
| `create_full_plate_workflow.py` | Full workflow automation |

## Reference Files

| Directory | Contents |
|-----------|----------|
| `references/blanks/` | STL blank templates (moto, moto-bolt, car) |
| `references/fonts/` | DealerPlate font for text extrusion |

## Configuration

Set these environment variables:

```bash
export SHOPIFY_SHOP="your-shop.myshopify.com"
export SHOPIFY_ACCESS_TOKEN="your-token"
export DILMUN_VAULT="/home/kworqs/.pi/subdilmun"
```

## Requirements

- Python 3.9+
- Obsidian
  
## Status

- **Phase 1**: Shopify API Integration (In Progress)
- **Phase 2**: Dilmun Orchestration (Pending)
- **Phase 3**: Geometry Generation (Pending)
- **Phase 4**: Printer Dispatch (Pending)

## Related Skills

- [dilmun-memory-middleware](https://github.com/kwedder/dilmun-memory-middleware) - Memory middleware


** Shopify API has to be created via Shopify dev dashboard. - See docs here (https://shopify.dev/docs/apps/build/authentication-authorization/access-tokens/generate-app-access-tokens-admin)

## License

MIT
