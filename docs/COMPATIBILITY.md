# LabVIEW Version Compatibility

Verified 2026-10-01 against real `.vi` files (106 total). "Review" means the
full pipeline: parse → run rules → render diagram.

| Saved in | Files tested | Version detected | Diagram review |
|----------|-------------|------------------|----------------|
| 21.0     | 103         | ✓ | ✓ |
| 14.0     | 2           | ✓ | ✓ |
| 8.6      | 1           | ✓ | ✗ — block-diagram extraction fails (`vi_BDHb.xml` not produced) |

## What this means

- **21.0 and 14.0 are the verified working versions.** Every tested file from
  these versions parses and reviews cleanly.
- **8.6 is a known limitation**, not a supported version. Version detection
  works (via `pylabview`), but `lvkit`'s diagram extractor does not produce
  block-diagram XML for the one 8.6 file tested.
- Versions not listed here (15.0–20.0, 22.0+, 2023+) are **untested** —
  they may work, but no claim is made.
- 32-bit vs 64-bit LabVIEW saves have not been compared; no claim is made
  that they behave identically.

## Expanding the matrix

To verify a new version: add real `.vi` files saved in that version under
`fixtures/`, run `pytest tests/test_versions.py`, and update this table.
Do not claim support for a version without files tested.
