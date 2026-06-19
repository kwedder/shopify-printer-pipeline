# Kworqs Shopify Printer Pipeline

A GSD-compliant pipeline that transforms Shopify custom text orders into production-ready 3D printable models.

## Overview

This pipeline integrates:

- **shopify-skill** - Order intake from Shopify API
- **Dilmun Protocol** - Memory middleware for orchestration
- **Blender-MCP** - 3D geometry generation and boolean operations

## Architecture

```
Shopify Order
    ↓
shopify-skill (fetch)
    ↓
Dilmun Memory (order.received event)
    ↓
Blender-MCP (geometry generation)
    ↓
3MF Output
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
- `obsidian_dilmun` package
- `shopify` package
- `httpx`, `tenacity` for API calls

## Status

- **Phase 1**: Shopify API Integration (In Progress)
- **Phase 2**: Dilmun Orchestration (Pending)
- **Phase 3**: Geometry Generation (Pending)
- **Phase 4**: Printer Dispatch (Pending)

## Related Skills

- [dilmun-protocol](https://github.com/kwedder/dilmun-protocol) - Memory middleware
- [shopify-skill](https://github.com/kwedder/shopify-skill) - Shopify API client
- [goon-plates](https://github.com/kwedder/goon-plates) - Blender scripts

## License

MIT
