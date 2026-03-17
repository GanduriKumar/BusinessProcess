from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(r"C:\Users\kumar.gn\HCLProjects\BusinessProcess")
TARGET = ROOT / "tools" / "one-off" / "generate_model_eval_weekly_digest.py"


def main() -> int:
    if not TARGET.exists():
        print(f"Target script not found: {TARGET}", file=sys.stderr)
        return 1
    completed = subprocess.run([sys.executable, str(TARGET), *sys.argv[1:]], check=False)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
