#!/usr/bin/env python3
"""Heuristic, read-only static check for common HTTP security header names in Next.js config."""
import argparse
import json
import re
import sys
from pathlib import Path

HEADERS = {
    "Content-Security-Policy": "Consider a tailored CSP; test thoroughly before enforcing.",
    "X-Content-Type-Options": "Consider X-Content-Type-Options: nosniff.",
    "Referrer-Policy": "Choose a suitable Referrer-Policy, e.g. strict-origin-when-cross-origin.",
    "Permissions-Policy": "Restrict browser features your app does not use.",
    "Strict-Transport-Security": "Consider HSTS only for sites consistently served via HTTPS.",
    "X-Frame-Options": "Consider clickjacking protection using CSP frame-ancestors (and/or X-Frame-Options).",
}
CONFIGS = ("next.config.js", "next.config.mjs", "next.config.ts", "next.config.cjs")

def audit_text(text):
    # This is deliberately a string-based heuristic, not JavaScript execution or parsing.
    findings = []
    for header, advice in HEADERS.items():
        if not re.search(r"(?i)(?<![A-Za-z0-9-])" + re.escape(header) + r"(?![A-Za-z0-9-])", text):
            findings.append({"header": header, "reason": "Header name not found in config text", "suggestion": advice})
    return findings

def audit_path(path):
    path = Path(path)
    if path.is_dir():
        matches = [path / name for name in CONFIGS if (path / name).is_file()]
        if not matches:
            raise ValueError("No next.config.{js,mjs,ts,cjs} found in this directory")
        path = matches[0]
    if not path.is_file():
        raise ValueError(f"File not found: {path}")
    if path.name not in CONFIGS:
        raise ValueError("Expected a Next.js configuration file named next.config.js/mjs/ts/cjs")
    data = path.read_text(encoding="utf-8")
    return {"file": str(path), "checked_headers": len(HEADERS), "missing_name_findings": audit_text(data)}

def main(argv=None):
    parser = argparse.ArgumentParser(description="Static Next.js security header name audit (heuristic)")
    parser.add_argument("path", nargs="?", default=".", help="Next.js project directory or config path")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args(argv)
    try:
        result = audit_path(args.path)
    except (ValueError, OSError, UnicodeError) as exc:
        if args.json:
            print(json.dumps({"error": str(exc)}, indent=2))
        else:
            print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    missing = result["missing_name_findings"]
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Examined {result['file']}")
        for item in missing:
            print(f"[CHECK] {item['header']}: name not found")
            print(f"  {item['suggestion']}")
        print(f"Missing header names: {len(missing)}/{result['checked_headers']}")
        print("NOTE: Static string search only. Check actual deployed response headers separately.")
    return 1 if missing else 0

if __name__ == "__main__":
    sys.exit(main())
