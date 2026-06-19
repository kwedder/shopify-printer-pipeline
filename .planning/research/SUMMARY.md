# Research Summary: Kworqs Shopify Printer Pipeline

## Key Findings

### Stack

- **Backend**: Python 3.9+, httpx for Shopify API (GraphQL recommended)
- **Middleware**: Dilmun Protocol with Wedderburn-Kasczinski memory
- **Automation**: Blender-MCP (218 tools, headless export)
- **Output**: 3MF for multi-material support
- **Dispatch**: K2 Plus (auto) + Bambu (manual)

### Table Stakes

1. Shopify order intake (GraphQL, not REST)
2. Text-to-3D geometry via Blender-MCP
3. 3MF export with material preservation
4. Dual printer routing logic

### Watch Out For

- Shopify REST API deprecated (Oct 2024) - use GraphQL
- Geometry validation needed before export
- Rate limiting on Shopify API
- Printer-specific file requirements

## Recommendations

1. **Migrate Shopify client** from REST to GraphQL
2. **Verify Blender-MCP API** against goon-plates scripts
3. **Implement retry logic** for API calls
4. **Add geometry validation** step before export

---
*Research completed: 2026-06-18*
*Files: `.planning/research/`*
