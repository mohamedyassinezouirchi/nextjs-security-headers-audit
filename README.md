# nextjs-security-headers-audit

**A tiny, read-only static checklist for HTTP security header names in Next.js configuration files.**

[![Unit tests](https://github.com/mohamedyassinezouirchi/nextjs-security-headers-audit/actions/workflows/ci.yml/badge.svg)](https://github.com/mohamedyassinezouirchi/nextjs-security-headers-audit/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

When building Next.js apps, security headers are easy to overlook. This lightweight Python utility checks whether common header **names** appear in your `next.config.js`, `next.config.mjs`, `next.config.ts`, or `next.config.cjs` file, and suggests topics to review.

> **Important:** This project is a *name-based static heuristic*, not a vulnerability scanner, HTTP response validator, or guarantee of security. A header name present in code does **not** mean it is correctly configured or delivered. Headers may also be set in middleware, hosting infrastructure, proxies, or other files and therefore be absent from the scanned file.

## Features

- No third-party dependencies; requires only Python 3.10+.
- Reads a local Next.js configuration file without executing JavaScript or TypeScript.
- Searches for six common security header names.
- Displays suggestions for names it cannot find.
- Outputs human-readable text or machine-readable JSON.
- Includes basic tests and GitHub Actions CI.

## Checks

| Header name | What to consider |
| --- | --- |
| `Content-Security-Policy` | Configure an app-specific CSP to restrict resource loading. |
| `X-Content-Type-Options` | Consider `nosniff` to prevent MIME sniffing. |
| `Referrer-Policy` | Select a policy suited to your app's privacy needs. |
| `Permissions-Policy` | Limit browser features not required by the app. |
| `Strict-Transport-Security` | Consider HSTS *only* for consistently HTTPS-served origins. |
| `X-Frame-Options` | Review clickjacking protection; CSP `frame-ancestors` is another option. |

These are prompts for manual review, **not pass/fail judgments about your deployed site's security**.

## Quick start

```bash
git clone https://github.com/mohamedyassinezouirchi/nextjs-security-headers-audit.git
cd nextjs-security-headers-audit
python audit_headers.py examples/next.config.mjs
```

For your own project, pass its Next.js project root or the path to its config file:

```bash
python audit_headers.py /path/to/my-nextjs-app
python audit_headers.py /path/to/my-nextjs-app/next.config.ts
```

On Windows you can use a Windows path:

```powershell
python audit_headers.py "C:\\Projects\\my-next-app"
```

### Example output for an empty config

```text
Examined next.config.mjs
[CHECK] Content-Security-Policy: name not found
  Consider a tailored CSP; test thoroughly before enforcing.
...
Missing header names: 6/6
NOTE: Static string search only. Check actual deployed response headers separately.
```

The ellipsis abbreviates similar check lines.

### JSON output

```bash
python audit_headers.py /path/to/my-nextjs-app --json
```

Output includes the examined file, the number of header names checked, and a `missing_name_findings` array.

### Exit codes

| Code | Meaning |
| --- | --- |
| `0` | All six names appear in the scanned file (not a security guarantee). |
| `1` | One or more names could not be found. |
| `2` | Missing/invalid file or read error. |

## How it works

1. Looks for a supported `next.config.*` file in the supplied directory, or accepts a direct file path.
2. Reads its contents as UTF-8.
3. Performs case-insensitive literal header-name matching in the text.
4. Reports which names are missing, along with guidance.

It does **not** parse ASTs, resolve imported config, analyze actual values, execute code, or make network requests.

## Run tests

```bash
python -m unittest discover -s tests -v
```

Tests require no Next.js installation or running website. GitHub Actions runs these tests on Python 3.10 and 3.12.

## Repository structure

```text
nextjs-security-headers-audit/
├── audit_headers.py
├── tests/
│   └── test_audit.py
├── examples/
│   └── next.config.mjs
├── .github/workflows/
│   └── ci.yml
├── .gitignore
├── LICENSE
└── README.md
```

## Known limitations

- Comments or unused strings containing a header name can produce false negatives.
- Headers configured outside `next.config.*` can produce false positives.
- Does not validate CSP directives, header values, route coverage, HTTPS, or runtime behavior.
- Does not check against live websites or make remote requests.
- The included `examples/next.config.mjs` is illustrative only; **do not copy it unreviewed into production**.
- A clean result does not prove that your Next.js application is secure.

For deployed apps, separately review real HTTP response headers and your hosting configuration, ideally as part of an authorized security review.

## Roadmap

Possible future work: safe parsing of configuration syntax, configurable rules, additional configuration locations, optional reports in CI, and test fixtures for different Next.js setups. These are not implemented in this initial release.

## Contributing

Focused bug reports, reproducible samples, documentation updates, and tested rule improvements are welcome. Do not include secrets, credentials, or sensitive production configurations in public issues.

## Author

**Mohamed Yassine Zouirchi** · [GitHub](https://github.com/mohamedyassinezouirchi)

## License

MIT — see [LICENSE](LICENSE).
