# Pipeline Scripts

This directory contains the main pipeline scripts for the Kworqs Shopify Printer Pipeline.

## Scripts

### pipeline.py

Main entry point for the formal GSD-compliant pipeline.

```bash
# Initialize pipeline
python pipeline.py --action init

# Fetch pending Shopify orders
python pipeline.py --action fetch-orders

# Process a specific order
python pipeline.py --action process-order --order-id 1234 --text "YOURTEXT"

# Run plate creation workflow
python pipeline.py --action workflow --text "YOURTEXT"

# Check pipeline state
python pipeline.py --action state
```

## Dependencies

This pipeline integrates with existing skills:

- **shopify-skill**: `~/.pi/skills/shopify-skill/` - Shopify API client
- **dilmun-protocol**: `~/.pi/skills/dilmun-protocol/` - Memory middleware
- **obsidian_dilmun**: `~/.pi/skills/obsidian_dilmun/` - DilmunMemoryMiddleware

## Running from Project Root

```bash
cd /home/kworqs/shopify-printer-pipeline
python scripts/pipeline.py --action init
```

## GSD Integration

This pipeline follows GSD phases:

- **Phase 1**: Shopify API Integration (SHOP-01, SHOP-02, SHOP-03)
- **Phase 2**: Dilmun Orchestration (DILM-01 through DILM-04)
- **Phase 3**: Geometry Generation (BLEND-01 through BLEND-03)
- **Phase 4**: Printer Dispatch (DISP-01 through DISP-03)
