import io
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from audit_headers import HEADERS, audit_text, audit_path, main

class AuditTests(unittest.TestCase):
    def test_empty_config_flags_all(self):
        self.assertEqual(len(audit_text("module.exports = {}")), len(HEADERS))

    def test_named_headers_are_recognized(self):
        config = " ".join(f"name: '{name}'" for name in HEADERS)
        self.assertEqual(audit_text(config), [])

    def test_case_insensitive(self):
        self.assertEqual(len(audit_text("content-security-policy")), len(HEADERS) - 1)

    def test_directory_lookup(self):
        with TemporaryDirectory() as d:
            (Path(d) / "next.config.js").write_text("module.exports = {}")
            result = audit_path(d)
            self.assertEqual(len(result["missing_name_findings"]), len(HEADERS))

    def test_cli_exit_code(self):
        with TemporaryDirectory() as d:
            (Path(d) / "next.config.mjs").write_text("export default {}")
            with patch("sys.stdout", new_callable=io.StringIO):
                self.assertEqual(main([d]), 1)

    def test_missing_file(self):
        with patch("sys.stderr", new_callable=io.StringIO):
            self.assertEqual(main(["/path/not/found/next.config.js"]), 2)

if __name__ == "__main__":
    unittest.main()
