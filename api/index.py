"""Vercel serverless entrypoint: re-exports the FastAPI app from main.py."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app  # noqa: F401  (Vercel looks for `app` in api/index.py)
