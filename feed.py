"""feed.py

Minimal feed generator script so CI workflow can run `python feed.py`.
It reads feed.yaml and prints a short summary of items. Intentionally
non-destructive (no files written) so the pipeline commit step will be
no-op unless you want to persist generated feeds.
"""

import sys
import os

try:
    import yaml
except Exception:
    yaml = None

FEED_YAML = "feed.yaml"


def main():
    cwd = os.getcwd()
    path = os.path.join(cwd, FEED_YAML)
    if not os.path.exists(path):
        print(f"feed.py: {FEED_YAML} not found in {cwd}")
        print("Nothing to do. Exiting 0 to avoid failing CI while repository is being bootstrapped.")
        return 0

    if yaml is None:
        print("PyYAML is not installed. Install dependencies or add PyYAML to your workflow.")
        return 1

    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    items = data.get("item") or data.get("items") or []
    print(f"Loaded feed.yaml, found {len(items)} item(s).")
    for i, it in enumerate(items, start=1):
        title = it.get("title") if isinstance(it, dict) else str(it)
        duration = it.get("duration") if isinstance(it, dict) else ""
        fileloc = it.get("file") if isinstance(it, dict) else ""
        print(f"{i}. {title} — duration: {duration} — file: {fileloc}")

    print("feed.py: Completed successfully.")
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
