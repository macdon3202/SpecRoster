"""Fail-fast local verification. Run: py -3.12 scripts/verify.py."""
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
env = dict(os.environ, PYTHONUTF8="1")
commands = [
    ([sys.executable,"-m","pytest","tests","-q","--tb=short","-p","no:cacheprovider"], ROOT),
    ([sys.executable,"-m","genvm_linter.cli","check","contracts/spec_roster.py"], ROOT),
    (["npm.cmd" if os.name=="nt" else "npm","ci","--ignore-scripts"], ROOT/"frontend"),
    (["npm.cmd" if os.name=="nt" else "npm","run","verify"], ROOT/"frontend"),
]
for command, cwd in commands:
    print("RUN", " ".join(command), flush=True)
    subprocess.run(command,cwd=cwd,env=env,check=True)
print("LOCAL_VERIFIED — deployment and signed browser journey still pending")
