"""
Pytest configuration for the Stroke Severity API tests.

This ensures that the `src` directory is on `sys.path` so that imports like
`from app.db import ...` work correctly after the project was restructured
into a `src/` layout.
"""

from __future__ import annotations

import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"

if str(SRC_DIR) not in sys.path:
    # Prepend so that `app` is resolved from `src/app`
    sys.path.insert(0, str(SRC_DIR))

