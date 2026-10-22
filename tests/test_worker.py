"""Worker (JS) unit tests bridged into the Python suite (issue #31).

The Worker's pure functions — UA bucketing, sanitizing, stats shaping — are
implemented in JavaScript and tested with node:test (worker/test/). This
wrapper runs that suite so that \`python3 -m unittest discover -s tests\` and
the guard workflow's test job cover them too.

Test files are passed to node explicitly (node --test <dir> is unreliable
across node versions); skipped on machines without node — CI runners ship
node 22, so guard always executes the real tests.
"""
import shutil
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


@unittest.skipUnless(shutil.which("node"), "node not available on this machine")
class WorkerJsTests(unittest.TestCase):
    def test_node_test_suite_passes(self):
        test_files = sorted(
            str(p.relative_to(ROOT)) for p in (ROOT / "worker" / "test").glob("*.test.mjs")
        )
        self.assertTrue(test_files, "no worker/test/*.test.mjs found")
        proc = subprocess.run(
            ["node", "--test", *test_files],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            timeout=120,
        )
        self.assertEqual(
            proc.returncode, 0, "\n--- stdout ---\n{}\n--- stderr ---\n{}".format(proc.stdout, proc.stderr)
        )


if __name__ == "__main__":
    unittest.main()
