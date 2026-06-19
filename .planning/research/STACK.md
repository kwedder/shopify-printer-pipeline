# Stack Research: Kworqs Shopify Printer Pipeline

## Shopify API Integration

**Current State**: Using legacy REST Admin API (deprecated Oct 2024)
**Recommendation**: Migrate to GraphQL Admin API

### Recommended Stack (2025)

| Layer | Technology | Rationale |
|-------|------------|-----------|
| Language | Python 3.9+ | Existing skills are Python-based |
| HTTP Client | httpx | Modern async support, connection pooling |
| Shopify SDK | shopify-graphql (new) or shopify-app-python | Official support for GraphQL |
| Auth | OAuth 2.0 with minimum scopes | Security best practice |
| Rate Limiting | Built-in retry with exponential backoff | Shopify rate limits |

### Key Packages

```bash
pip install shopify-graphql-api httpx tenacity
```

## Dilmun Protocol

**Source**: `~/.pi/skills/dilmun-protocol/`

- Uses `DilmunMemoryMiddleware` from `obsidian-dilmun`
- Pub/Sub event coordination
- Wedderburn-Kasczinski ring-theoretic memory management
- Memory store at `/home/kworqs/.pi/subdilmun`
- Obsidian REST API on port 27124

## Blender-MCP

**Source**: `~/skills1/skills/blender-mcp-goon-plates/`

- 218 MCP tools for Blender automation
- Headless batch export support
- Geometry nodes support
- HTTP REST API available

### Available Operations (Relevant)

- `blender_mesh` - Mesh creation and manipulation
- `blender_export` - Export to 3MF, STL
- `blender_modifier` - Boolean operations
- `blender_object` - Text object creation

## Output Format

**3MF (3D Manufacturing Format)**:

- Preserves material/color data
- Multi-material support (AMS/CFS)
- Required for Bambu multi-material printing

## Printer Dispatch

| Printer | Mode | Routing |
|---------|------|---------|
| K2 Plus | Local, dev mode | Auto-dispatch |
| Bambu | Cloud, warranty mode | Manual gate |

---
*Confidence: High (based on existing skills)*
*Next: Verify blender-mcp-goon-plates API surface*
