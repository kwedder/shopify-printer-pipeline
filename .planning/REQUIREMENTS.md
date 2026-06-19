# Requirements: Kworqs Shopify Printer Pipeline

**Defined:** 2026-06-18
**Core Value:** Users can order custom text designs through Shopify and receive 3D printable 3MF files without manual intervention.

## v1 Requirements

Requirements for initial release. Each maps to roadmap phases.

### Shopify Integration

- [ ] **SHOP-01**: Fetch pending orders from Shopify API
- [ ] **SHOP-02**: Parse order variants to extract text
- [ ] **SHOP-03**: Handle API rate limits with retry logic

### Dilmun Protocol

- [ ] **DILM-01**: Initialize Dilmun middleware connection
- [ ] **DILM-02**: Subscribe to `order.received` events
- [ ] **DILM-03**: Publish `plate.create` events
- [ ] **DILM-04**: Track plate status in `fact/` partition

### Blender-MCP Integration

- [ ] **BLEND-01**: Generate 3D text geometry from order text
- [ ] **BLEND-02**: Apply boolean operations to plate blank
- [ ] **BLEND-03**: Export as 3MF with material data

### Printer Dispatch

- [ ] **DISP-01**: Route to K2 Plus (auto) or Bambu (manual)
- [ ] **DISP-02**: Handle dispatch failures with retry
- [ ] **DISP-03**: Update status after successful dispatch

## v2 Requirements

Deferred to future release. Tracked but not in current roadmap.

### Notification System

- **NOTF-01**: Email notification on plate completion
- **NOTF-02**: Webhook to Shopify on dispatch

### Advanced Features

- **ADV-01**: Custom fonts support
- **ADV-02**: Batch processing for multiple orders
- **ADV-03**: Material/color selection per order

## Out of Scope

| Feature | Reason |
|---------|--------|
| Custom Liquid frontend | Deferred to later iteration |
| Real-time dashboard | Covered by existing lab telemetry |
| Mobile app | Web-first pipeline |
| OAuth login | Not needed for backend pipeline |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
| ----------- | ----- | ------ |
| SHOP-01 | Phase 1 | Pending |
| SHOP-02 | Phase 1 | Pending |
| SHOP-03 | Phase 1 | Pending |
| DILM-01 | Phase 2 | Pending |
| DILM-02 | Phase 2 | Pending |
| DILM-03 | Phase 2 | Pending |
| DILM-04 | Phase 2 | Pending |
| BLEND-01 | Phase 3 | Pending |
| BLEND-02 | Phase 3 | Pending |
| BLEND-03 | Phase 3 | Pending |
| DISP-01 | Phase 4 | Pending |
| DISP-02 | Phase 4 | Pending |
| DISP-03 | Phase 4 | Pending |

**Coverage:**

- v1 requirements: 14 total
- Mapped to phases: 14
- Unmapped: 0 ✓

---
*Requirements defined: 2026-06-18*
*Last updated: 2026-06-18 after initial definition*
