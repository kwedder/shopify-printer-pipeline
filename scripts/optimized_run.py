#!/usr/bin/env python3
"""Optimized Dilmun Protocol Runner - Fast, token-efficient."""
import sys, os, json, argparse
from pathlib import Path
from datetime import datetime

# Minimal path setup
SCRIPT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(SCRIPT_DIR.parent))  # /home/kworqs/.pi/skills
sys.path.insert(0, str(SCRIPT_DIR.parent / "memory-store"))

from memory_store import read_memory, write_memory, ensure_partitions

VAULT = Path(os.environ.get("MEMORY_STORE_VAULT", "/home/kworqs/.pi/subdilmun"))

# Cached state
_state_cache = None

def get_state():
    """Fast state check - cached."""
    global _state_cache
    if _state_cache is None:
        facts = read_memory("fact", include_conflicting=False)
        conflicts = len(list((VAULT / "conflict").glob("conflict_*.md")))
        _state_cache = {"facts": len(facts), "conflicts": conflicts, "vault": str(VAULT)}
    return _state_cache

def action_init():
    """Initialize - minimal output."""
    ensure_partitions()
    write_memory("fact", "", {"entity": "protocol", "predicate": "status", "value": "initialized", "scope": "system"})
    print(json.dumps({"status": "ok", "vault": str(VAULT)}))

def action_state():
    """Show cached state."""
    s = get_state()
    print(json.dumps({"facts": s["facts"], "conflicts": s["conflicts"], "vault": s["vault"]}))

def action_workflow(text="GOON"):
    """Quick workflow - minimal output."""
    write_memory("fact", "", {"entity": "workflow", "predicate": "plate", "value": text, "scope": "goon-plates"})
    print(json.dumps({"status": "ok", "workflow": text}))

def action_resolve():
    """Resolve conflicts - fast."""
    from pathlib import Path
    conflict_dir = VAULT / "conflict"
    resolved = 0
    for cf in conflict_dir.glob("conflict_*.md"):
        try:
            content = cf.read_text()
            meta = json.loads(content.split("---")[1].strip())
            if meta.get("resolution") == "unresolved":
                meta["resolution"] = "resolved-temporal"
                meta["resolved_at"] = datetime.now().isoformat()
                cf.rename(conflict_dir / "resolved" / cf.name)
                resolved += 1
        except: pass
    print(json.dumps({"resolved": resolved}))
    return resolved

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--action", required=True, choices=["init", "state", "workflow", "resolve-conflicts"])
    parser.add_argument("--plate-text", default="GOON", help="Text for plate creation")
    args = parser.parse_args()
    
    {
        "init": action_init,
        "state": action_state,
        "workflow": lambda: action_workflow(args.plate_text),
        "resolve-conflicts": action_resolve,
    }[args.action]()

if __name__ == "__main__":
    main()
