#!/usr/bin/env python3
import json, os, subprocess, sys

keywords = ("codex", "claude")
current_pid = os.getpid()
count = 0
sample = []

try:
    out = subprocess.check_output(["ps", "-eo", "pid=,command="], text=True)
    for line in out.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            pid_s, cmd = line.split(None, 1)
            pid = int(pid_s)
        except Exception:
            continue
        lower = cmd.lower()
        if pid != current_pid and any(k in lower for k in keywords):
            count += 1
            if len(sample) < 3:
                sample.append(cmd[:120])
except Exception:
    count = 0

msg = None
if count:
    msg = f"Best-effort process hygiene check: found {count} local processes matching Claude/Codex keywords. Inspect manually if they should be stopped."

sys.stdout.write(json.dumps({"systemMessage": msg} if msg else {}))
