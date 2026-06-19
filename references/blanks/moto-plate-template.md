# Motorcycle Plate Template Reference

## Template File
- **File**: `moto-standard.stl`
- **Vehicle Type**: `moto-standard`
- **Use Case**: Motorcycle license plates

## Specifications

### Physical Dimensions
- **Plate Thickness (Bolt-on)**: 0.1 in (thinnest for weight savings)
- **Plate Thickness (Magnetic)**: 0.3 in
- **Text Engraving Depth**: 0.05 mm (fixed, never change)

### Text Parameters
- **Font**: GoonPlates.ttf (licensed only)
- **Extrusion Depth**: 0.05 mm (0.00005 Blender units, negative)
- **Boolean Operation**: DIFFERENCE (cuts into plate)

### STL Naming Convention
```
[TopText]_moto-standard.stl
```

Example: `RIDE_moto-standard.stl`

## Decision Tree

```
Is it a car plate?
  ├─ Yes → load blank: car-standard.stl
  └─ No → motorcycle?
            └─ Yes → load blank: moto-standard.stl
```

## Critical Rules

1. **Confirm vehicle type before geometry** - wrong blank = wasted print
2. **Text depth: 0.05mm** - never change
3. **Validate manifold before slicing** - prevents silent failures
4. **Use licensed font only** - GoonPlates.ttf

## CLI Commands

```bash
plate-builder orders check          # Check pending orders
plate-builder orders view 1235      # View motorcycle order
plate-builder build --order 1235    # Generate & slice
```

## Integration

See also:
- [[Skill: goon-plates]] - Main pipeline
- [[Skill: blender-mcp-goon-plates]] - Geometry generation
- [[Skill: shopify-skill]] - Order parsing