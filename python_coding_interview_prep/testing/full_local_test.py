#!/usr/bin/env python3
# .git/hooks/pre-commit (executable)

import subprocess, sys, os, time, threading

def timeout_cmd(cmd, secs=30):
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    def kill():
        time.sleep(secs)
        if proc.poll() is None:
            proc.kill()
    t = threading.Thread(target=kill)
    t.daemon = True
    t.start()
    out, err = proc.communicate()
    return proc.returncode, out.decode(), err.decode()

# 1) Run tests with 30s timeout
code, out, err = timeout_cmd("python -m pytest", 30)
if code:
    print("❌ Tests failed or timed out (>30s)")
    print(err or out)
    sys.exit(1)

# 2) Static analysis (no network)
code = subprocess.call("flake8 . --count --select=E9,F63,F7,F82 --show-source", shell=True)
if code:
    print("❌ Flake8 errors found")
    sys.exit(1)

# 3) No debug/print statements
code = subprocess.call("grep -r 'print(' *.py", shell=True)
if code == 0:  # grep found matches
    print("❌ Print statements found. Remove them.")
    sys.exit(1)

print("✅ All checks passed")
sys.exit(0)