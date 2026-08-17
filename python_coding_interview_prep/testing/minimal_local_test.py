#!/usr/bin/env python3
import subprocess as sp, sys, threading, time

def run(cmd, t=30):
    p = sp.Popen(cmd, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
    timer = threading.Timer(t, lambda: p.kill() if p.poll() is None else None)
    print("Setting timeout for:", cmd, "with", t, "seconds")
    timer.start()
    print("Running:", cmd)
    o, e = p.communicate()
    timer.cancel()
    print("Return code:", p.returncode)
    return p.returncode, o.decode(), e.decode()

rc, _, e = run("python -m pytest")
if rc: print("Tests failed"); sys.exit(1)

rc = sp.call("flake8 . --select=E9,F63,F7,F82", shell=True)
if rc: print("Flake8 errors"); sys.exit(1)

rc = sp.call("grep -q 'print(' *.py 2>/dev/null", shell=True)
if rc == 0: print("Remove prints"); sys.exit(1)

print("OK")