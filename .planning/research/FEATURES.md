# Feature Research: Kworqs Shopify Printer Pipeline

## Table Stakes (Must Have for v1)

Users will abandon if these are missing:

| Feature | Description | Complexity |
|---------|-------------|------------|
| Order Intake | Fetch pending Shopify orders | Low |
| Text Processing | Convert order text to 3D geometry | Medium |
| Plate Creation | Boolean subtract text from blank | Medium |
| Export 3MF | Generate printable file format | Low |
| Dispatch | Route to correct printer queue | Medium |

## Differentiators

Competitive advantages:

| Feature | Description | Complexity |
|---------|-------------|------------|
| Dual Printer Support | K2 Plus (auto) + Bambu (manual) | Medium |
| Material Preservation | Color/material slots in 3MF | Medium |
| Telemetry | Live status to dashboard | Low |
| Error Recovery | Handle geometry failures | High |

## Anti-Features (Explicitly NOT Building)

| Feature | Reason |
|---------|--------|
| Real-time dashboard | Covered by existing lab telemetry |
| Custom Liquid frontend | Deferred to later iteration |
| Mobile app | Web-first, mobile later |
| OAuth login | Email/password sufficient for v1 |

## Dependencies

- Shopify API access (credentials in config)
- Blender-MCP running (headless mode)
- Dilmun Protocol memory store
- 3D printer queues (Moonraker for K2, Bambu Studio for Bambu)

---
*Source: wedderburn.systems/lab telemetry*
*Confidence: High (based on existing pipeline)*
