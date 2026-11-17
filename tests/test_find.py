import json
import os
import subprocess
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIND = ROOT / "find-skill" / "scripts" / "find.py"
HARVEST = ROOT / "find-skill" / "scripts" / "harvest.py"
COMMIT = "a" * 40


def vector(text):
    text = text.lower()
    values = [0.01 + text.count("pdf"), 0.01 + text.count("image"), 0.01 + text.count("audio")]
    norm = sum(value * value for value in values) ** 0.5
    return [value / norm for value in values]


class EmbeddingHandler(BaseHTTPRequestHandler):
    payloads = []

    def log_message(self, *args):
        pass

    def do_POST(self):
        payload = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        type(self).payloads.append(payload)
        data = [{"index": index, "embedding": vector(text)} for index, text in enumerate(payload["input"])]
        body = json.dumps({"data": data}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


class FindIntegrationTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.tmp = Path(self.temporary.name)
        EmbeddingHandler.payloads = []
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), EmbeddingHandler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.env = os.environ.copy()
        self.env["SKILL_FINDER_EMBED_URL"] = f"http://127.0.0.1:{self.server.server_port}/voyage/embeddings"
        self.env["SKILL_FINDER_EMBED_MODEL"] = "fixture-embedding-v1"
        self.env.pop("SKILL_FINDER_EMBED_KEY", None)

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()
        self.temporary.cleanup()

    def run_cli(self, script, *args, check=True, env=None):
        return subprocess.run(
            [sys.executable, str(script), *args], cwd=ROOT, env=env or self.env,
            text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=check,
        )

    def catalog_record(self, keyword):
        return {
            "id": f"vendor/skills/{keyword}",
            "name": f"{keyword} Skill",
            "description": f"Create and transform {keyword} files into verified results",
            "source": "vendor/skills",
            "path": f"skills/{keyword}",
            "commit": COMMIT,
            "url": f"https://github.com/vendor/skills/tree/{COMMIT}/skills/{keyword}",
            "kind": "community",
            "has_scripts": False,
        }

    def write_catalog(self):
        records = [self.catalog_record(keyword) for keyword in ("pdf", "image", "audio")]
        path = self.tmp / "skills.json"
        path.write_text(json.dumps(records), encoding="utf-8")
        return path

    def build_fixture_index(self):
        catalog = self.write_catalog()
        index = self.tmp / "index"
        result = self.run_cli(FIND, "build", str(catalog), "--out", str(index))
        self.assertIn("Indexed 3 Skills", result.stdout)
        return index

    def test_harvest_fake_repo_and_skip_missing_description(self):
        repo = self.tmp / "repo"
        documented = repo / "skills" / "documented"
        documented.mkdir(parents=True)
        (documented / "SKILL.md").write_text(
            "---\nname: documented-skill\ndescription: Convert a document into a report\n---\n# Documented\n",
            encoding="utf-8",
        )
        scripts = documented / "scripts"
        scripts.mkdir()
        (scripts / "convert.py").write_text("print('fixture')\n", encoding="utf-8")
        missing = repo / "skills" / "missing"
        missing.mkdir(parents=True)
        (missing / "SKILL.md").write_text("---\nname: missing-description\n---\n# Missing\n", encoding="utf-8")
        sources = self.tmp / "sources.yaml"
        sources.write_text(
            f"sources:\n  - repo: vendor/skills\n    commit: {COMMIT}\n    kind: community\n    local_path: {repo}\n",
            encoding="utf-8",
        )
        output = self.tmp / "catalog" / "skills.json"
        result = self.run_cli(HARVEST, "--sources", str(sources), "--out", str(output))
        records = json.loads(output.read_text(encoding="utf-8"))
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["id"], "vendor/skills/skills/documented")
        self.assertEqual(records[0]["name"], "documented-skill")
        self.assertEqual(records[0]["description"], "Convert a document into a report")
        self.assertTrue(records[0]["has_scripts"])
        self.assertIn(COMMIT, records[0]["url"])
        self.assertIn("Skipped 1 Skills without description", result.stdout)

    def test_build_and_search_catalog(self):
        index = self.build_fixture_index()
        meta = json.loads((index / "meta.json").read_text(encoding="utf-8"))
        self.assertEqual(meta["skill_count"], 3)
        self.assertEqual(meta["text_source"], "name+description")
        result = self.run_cli(
            FIND, "search", "transform a PDF file", "--index", str(index), "--top", "2", "--json"
        )
        output = json.loads(result.stdout)
        self.assertEqual(output["results"][0]["id"], "vendor/skills/pdf")
        self.assertEqual(
            set(output["results"][0]),
            {"id", "name", "description", "url", "commit", "kind", "has_scripts", "score"},
        )
        self.assertTrue(all(payload["input_type"] in ("document", "query") for payload in EmbeddingHandler.payloads))
        self.assertTrue(all(COMMIT not in json.dumps(payload["input"]) for payload in EmbeddingHandler.payloads))

    def test_model_mismatch_fails_before_query_request(self):
        index = self.build_fixture_index()
        before = len(EmbeddingHandler.payloads)
        env = self.env.copy()
        env["SKILL_FINDER_EMBED_MODEL"] = "different-model"
        result = self.run_cli(FIND, "search", "PDF", "--index", str(index), "--json", check=False, env=env)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("query embedding endpoint/model differs", result.stderr)
        self.assertIn("Rebuild", result.stderr)
        self.assertEqual(len(EmbeddingHandler.payloads), before)


if __name__ == "__main__":
    unittest.main()
