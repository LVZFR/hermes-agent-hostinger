#!/usr/bin/env python3
"""Verify a sanitized backup ACTUALLY landed clean on GitHub (don't trust push success).

Usage: verify-remote-backup.py OWNER/REPO [branch] [env_path]
  Reads GITHUB_TOKEN from env_path (default /opt/data/.env, falls back to ~/.hermes/.env).
Prints HEAD sha, top-level tree, a forbidden-file scan, and a config.yaml secret-field check.
Exit 1 if any forbidden file or populated secret field is found on the remote.
"""
import sys, json, re, base64, os, urllib.request

if len(sys.argv) < 2:
    print("usage: verify-remote-backup.py OWNER/REPO [branch] [env_path]"); sys.exit(2)
repo = sys.argv[1]
branch = sys.argv[2] if len(sys.argv) > 2 else "main"
env_path = sys.argv[3] if len(sys.argv) > 3 else None

candidates = [env_path] if env_path else ["/opt/data/.env", os.path.expanduser("~/.hermes/.env")]
token = ""
for p in candidates:
    if p and os.path.exists(p):
        for line in open(p):
            if line.startswith("GITHUB_TOKEN=***                token = line.split("=", 1)[1].strip().strip('"').strip("'"); break
    if token:
        break
if not token:
    print("ERROR: GITHUB_TOKEN not found in", candidates); sys.exit(2)

API = f"https://api.github.com/repos/{repo}"
def get(url):
    req = urllib.request.Request(url, headers={"Authorization": f"token {token}",
                                               "Accept": "application/vnd.github+json"})
    return json.load(urllib.request.urlopen(req))

rc = 0
c = get(f"{API}/commits/{branch}")
print("=== remote HEAD ===")
print("sha:", c["sha"][:12])
print("msg:", c["commit"]["message"].splitlines()[0])

t = get(f"{API}/git/trees/{branch}")
print("\n=== top-level entries ===")
for e in t["tree"]:
    print(" ", e["path"], f"({e['type']})")

tr = get(f"{API}/git/trees/{branch}?recursive=1")
paths = [x["path"] for x in tr["tree"] if x["type"] == "blob"]
forbidden = re.compile(
    r"(^|/)(\.env|auth\.json|\.claude\.json|.*\.db|.*\.db-wal|.*\.db-shm|"
    r".*\.pid|.*\.lock|.*_state\.json|channel_directory\.json|"
    r"\.hermes_history|.*_cache\.json)$|^(logs|sessions|pairing)/", re.I)
bad = [p for p in paths if forbidden.search(p)]
print("\n=== security check ===")
print("total files on remote:", len(paths))
print("FORBIDDEN files:", bad if bad else "NONE")
if bad:
    rc = 1

try:
    cfg = get(f"{API}/contents/config.yaml")
    content = base64.b64decode(cfg["content"]).decode()
    populated = re.findall(r"(?:api_key|password|secret|token):\s*['\"]?[A-Za-z0-9]{12,}", content, re.I)
    print("populated secret fields in remote config.yaml:", populated if populated else "NONE")
    if populated:
        rc = 1
except Exception as e:
    print("config.yaml check skipped:", e)

print("\nRESULT:", "CLEAN" if rc == 0 else "FAILED — sensitive data on remote")
sys.exit(rc)
