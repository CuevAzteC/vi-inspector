"""vi-inspector: read LabVIEW project files without LabVIEW installed.

Two halves:
  vi.py       parse .vi/.ctl binaries (RSRC container) via pylabview
  project.py  parse .lvproj/.lvlib/.lvclass XML (project tree + class hierarchy)
"""

__version__ = "0.1.0"
