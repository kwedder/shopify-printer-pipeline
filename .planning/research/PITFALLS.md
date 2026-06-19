# Pitfalls Research: Kworqs Shopify Printer Pipeline

## Critical Mistakes to Avoid

### 1. Shopify API Versioning

- **Warning**: REST Admin API deprecated Oct 2024
- **Prevention**: Use GraphQL Admin API exclusively
- **Phase**: Phase 1 (Stack Setup)

### 2. Geometry Validation

- **Warning**: Text may produce unprintable geometry
- **Prevention**: Validate mesh before export
- **Phase**: Phase 3 (Geometry Generation)

### 3. Rate Limits

- **Warning**: Shopify API has strict rate limits
- **Prevention**: Implement exponential backoff
- **Phase**: Phase 1 (API Integration)

### 4. Printer Compatibility

- **Warning**: K2 Plus and Bambu have different requirements
- **Prevention**: Test both printer paths early
- **Phase**: Phase 5 (Dispatch)

## Common Failure Modes

| Failure | Detection | Recovery |
|---------|-----------|----------|
| API timeout | Request > 30s | Retry with backoff |
| Invalid text | Geometry check fails | Flag for manual review |
| Blender crash | Process exit code != 0 | Restart Blender session |
| File not found | Export path missing | Retry export |

## Phase Mapping

| Pitfall | Phase to Address |
|---------|------------------|
| API versioning | Phase 1 |
| Rate limits | Phase 1 |
| Geometry validation | Phase 3 |
| Printer compatibility | Phase 5 |

---
*Source: Shopify API deprecation notices, Blender crash logs*
*Confidence: Medium*
