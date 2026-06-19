# Roadmap: Kworqs Shopify Printer Pipeline

**Created:** 2026-06-18
**Phases:** 5
**Requirements:** 14 mapped

## Phase Overview

| # | Phase | Goal | Requirements | Success Criteria |
|---|-------|------|--------------|------------------|
| 1 | Shopify API Integration | Connect to Shopify and fetch orders | SHOP-01, SHOP-02, SHOP-03 | Orders fetched and parsed successfully |
| 2 | Dilmun Orchestration | Wire up middleware for event flow | DILM-01, DILM-02, DILM-03, DILM-04 | Events published and tracked |
| 3 | Geometry Generation | Create 3D models via Blender-MCP | BLEND-01, BLEND-02, BLEND-03 | 3MF files generated from text |
| 4 | Printer Dispatch | Route models to printer queues | DISP-01, DISP-02, DISP-03 | Models reach correct printer |
| 5 | Integration & Testing | End-to-end pipeline validation | All v1 | Pipeline runs without manual intervention |

## Phase Details

### Phase 1: Shopify API Integration

**Goal:** Connect to Shopify and fetch orders

**Requirements:**

- SHOP-01: Fetch pending orders from Shopify API
- SHOP-02: Parse order variants to extract text
- SHOP-03: Handle API rate limits with retry logic

**Success criteria:**

1. ShopifyClient connects to test store
2. Pending orders retrieved successfully
3. Text variants extracted from order data
4. Rate limiting handled gracefully

**Risks:**

- Shopify REST API deprecated - migrate to GraphQL

### Phase 2: Dilmun Orchestration

**Goal:** Wire up middleware for event flow

**Requirements:**

- DILM-01: Initialize Dilmun middleware connection
- DILM-02: Subscribe to `order.received` events
- DILM-03: Publish `plate.create` events
- DILM-04: Track plate status in `fact/` partition

**Success criteria:**

1. DilmunMemoryMiddleware initialized
2. Event subscription working
3. Events published to correct topics
4. Plate status tracked correctly

**Risks:**

- Existing Dilmun state conflicts
- Memory store connection issues

### Phase 3: Geometry Generation

**Goal:** Create 3D models via Blender-MCP

**Requirements:**

- BLEND-01: Generate 3D text geometry from order text
- BLEND-02: Apply boolean operations to plate blank
- BLEND-03: Export as 3MF with material data

**Success criteria:**

1. Text converted to 3D geometry
2. Boolean operation produces clean mesh
3. 3MF exported with material data
4. File saved to correct location

**Risks:**

- Blender-MCP API differences from goon-plates
- Geometry validation failures

### Phase 4: Printer Dispatch

**Goal:** Route models to printer queues

**Requirements:**

- DISP-01: Route to K2 Plus (auto) or Bambu (manual)
- DISP-02: Handle dispatch failures with retry
- DISP-03: Update status after successful dispatch

**Success criteria:**

1. Correct printer selected based on type
2. Models queued in appropriate system
3. Failures handled with retry
4. Status updated in Dilmun

**Risks:**

- Printer API connectivity
- Queue management differences

### Phase 5: Integration & Testing

**Goal:** End-to-end pipeline validation

**Requirements:**

- All v1 requirements

**Success criteria:**

1. Complete order-to-print flow works
2. Manual intervention not required
3. Telemetry reports status correctly
4. Error handling robust

---
*Roadmap created: 2026-06-18*
