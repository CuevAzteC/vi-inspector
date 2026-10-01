"""vi-inspector: automated code review for LabVIEW, in CI, without LabVIEW.

Two halves:
  vi.py       parse .vi/.ctl binaries (RSRC container) via pylabview
  project.py  parse .lvproj/.lvlib/.lvclass XML (project tree + class hierarchy)
  review.py   static-analysis rules (ERR-1, ERR-1b, ERR-2, RACE-1, CPLX-1)
  report.py   HTML dashboard + per-VI findings with diagram renders
"""

__version__ = "1.0.0"
