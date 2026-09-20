"""Entrypoint wrapper script for benchmark execution."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
script = ROOT / "scripts" / "benchmark_heading.py"

if __name__ == "__main__":
    result = subprocess.run([sys.executable, str(script)] + sys.argv[1:])
    sys.exit(result.returncode)

