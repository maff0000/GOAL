"""Pytest bootstrap: put ``tools/`` on ``sys.path``.

This lets every test under ``tests/`` do ``from goal_dcp import model`` without
a packaging file, which is an explicit non-goal of GOAL-DCP-001.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools"))
