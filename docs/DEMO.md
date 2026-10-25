# Demo: Next.js configuration checks

A short, reproducible way to show what this repository currently does.

## Walkthrough

Run `python audit_headers.py examples/next.config.mjs` then point the command at a local `next.config.*` file. Remove a header name from a test copy to observe the changed report.

## Suggested content for a public demo

- Show your terminal with the command and actual output.
- Explain the developer problem in one sentence.
- Share the repository link and the specific limitation below.
- Invite practical feedback or a reproducible issue instead of asking for stars.

## Honest limitations

This tool checks text, not deployed HTTP headers. Header names in comments can trigger false confidence.

## Validation

Run the project's tests where applicable:

```bash
python -m unittest discover -s tests -v
```

Avoid presenting a demo output as a real performance measurement unless you actually collected it.
