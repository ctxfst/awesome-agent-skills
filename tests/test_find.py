import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import numpy as np
import yaml

ROOT = Path(__file__).resolve().parents[1]
FIND = ROOT / "find-skill" / "scripts" / "find.py"
HARVEST = ROOT / "find-skill" / "scripts" / "harvest.py"
EXPAND = ROOT / "find-skill" / "scripts" / "expand_sources.py"
RENDER = ROOT / "find-skill" / "scripts" / "render_readme.py"
COMMIT = "a" * 40

SPEC = importlib.util.spec_from_file_location("expand_sources", EXPAND)
expand_sources = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(expand_sources)
RENDER_SPEC = importlib.util.spec_from_file_location("render_readme", RENDER)
render_readme = importlib.util.module_from_spec(RENDER_SPEC)
RENDER_SPEC.loader.exec_module(render_readme)


def write_skill(repo, relative, name, description, encoding="utf-8"):
    directory = repo if relative == "." else repo / relative
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "SKILL.md").write_text(
        f"---\nname: {name}\ndescription: {description}\n---\n# Fixture\n",
        encoding=encoding,
    )


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
        (self.tmp / "home").mkdir()
        EmbeddingHandler.payloads = []
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), EmbeddingHandler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.env = os.environ.copy()
        self.env["HOME"] = str(self.tmp / "home")
        self.env.pop("SKILL_FINDER_ROOT", None)
        self.env["SKILL_FINDER_EMBED_URL"] = f"http://127.0.0.1:{self.server.server_port}/voyage/embeddings"
        self.env["SKILL_FINDER_EMBED_MODEL"] = "fixture-embedding-v1"
        self.env.pop("SKILL_FINDER_EMBED_KEY", None)

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()
        self.temporary.cleanup()

    def run_cli(self, script, *args, check=True, env=None, cwd=None):
        return subprocess.run(
            [sys.executable, str(script), *args], cwd=cwd or ROOT, env=env or self.env,
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
            "raw_url": f"https://raw.githubusercontent.com/vendor/skills/{COMMIT}/skills/{keyword}/SKILL.md",
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

    def run_harvest(self, sources):
        source_path = self.tmp / "sources.yaml"
        source_path.write_text(yaml.safe_dump({"sources": sources}), encoding="utf-8")
        output = self.tmp / "catalog" / "skills.json"
        result = self.run_cli(HARVEST, "--sources", str(source_path), "--out", str(output))
        records = json.loads(output.read_text(encoding="utf-8")) if output.exists() else []
        return result, records

    def test_harvest_fake_repo_skip_rules_and_raw_url(self):
        repo = self.tmp / "repo"
        documented = repo / "skills" / "documented"
        documented.mkdir(parents=True)
        (documented / "SKILL.md").write_text(
            "---\nname: documented-skill\ndescription: Convert a document into a detailed and verified report\n---\n# Documented\n",
            encoding="utf-8",
        )
        scripts = documented / "scripts"
        scripts.mkdir()
        (scripts / "convert.py").write_text("print('fixture')\n", encoding="utf-8")
        missing = repo / "skills" / "missing"
        missing.mkdir(parents=True)
        (missing / "SKILL.md").write_text("---\nname: missing-description\n---\n# Missing\n", encoding="utf-8")
        short = repo / "skills" / "short"
        short.mkdir(parents=True)
        (short / "SKILL.md").write_text(
            "---\nname: short-description\ndescription: Too short\n---\n# Short\n",
            encoding="utf-8",
        )
        name_only = repo / "skills" / "name-only"
        name_only.mkdir(parents=True)
        (name_only / "SKILL.md").write_text(
            "---\nname: pdf-editor\ndescription: PDF Editor\n---\n# Name only\n",
            encoding="utf-8",
        )
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
        self.assertEqual(records[0]["description"], "Convert a document into a detailed and verified report")
        self.assertTrue(records[0]["has_scripts"])
        self.assertIn(COMMIT, records[0]["url"])
        self.assertEqual(
            records[0]["raw_url"],
            f"https://raw.githubusercontent.com/vendor/skills/{COMMIT}/skills/documented/SKILL.md",
        )
        self.assertIn("Skipped 1 Skills without description", result.stdout)
        self.assertIn("Skipped 1 Skills with descriptions under 40", result.stdout)
        self.assertIn("Skipped 1 Skills whose descriptions only restate the name", result.stdout)

    def test_harvest_bad_files_root_paths_encoding_and_script_flags(self):
        repo = self.tmp / "repo"
        write_skill(
            repo, ".", "root-skill",
            "Read a root-level Skill with a BOM and enough descriptive detail",
            encoding="utf-8-sig",
        )
        write_skill(
            repo, "skills/a b#?%中", "encoded-path",
            "Read a Skill from a path containing spaces and reserved characters",
        )
        bad_encoding = repo / "bad-encoding"
        bad_encoding.mkdir()
        (bad_encoding / "SKILL.md").write_bytes(b"\xff\xfe\x00")
        bad_link = repo / "bad-link"
        bad_link.mkdir()
        (bad_link / "SKILL.md").symlink_to(repo / "does-not-exist.md")
        (repo / "bad-directory" / "SKILL.md").mkdir(parents=True)
        (repo / "README.md").write_text("documentation\n", encoding="utf-8")
        (repo / "image.png").write_bytes(b"fixture")
        (repo / "README.md").chmod(0o755)
        (repo / "image.png").chmod(0o755)
        (repo / "SKILL.md").chmod(0o755)
        result, records = self.run_harvest([
            {"repo": "vendor/skills", "commit": COMMIT, "kind": "community", "local_path": str(repo)},
        ])
        self.assertEqual(len(records), 2)
        by_id = {record["id"]: record for record in records}
        root = by_id["vendor/skills"]
        self.assertEqual(root["path"], ".")
        self.assertEqual(root["raw_url"], f"https://raw.githubusercontent.com/vendor/skills/{COMMIT}/SKILL.md")
        self.assertFalse(root["has_scripts"])
        encoded = by_id["vendor/skills/skills/a b#?%中"]
        self.assertIn("/skills/a%20b%23%3F%25%E4%B8%AD/SKILL.md", encoded["raw_url"])
        self.assertIn("/tree/" + COMMIT + "/skills/a%20b%23%3F%25%E4%B8%AD", encoded["url"])
        self.assertIn("Unreadable SKILL.md entries: 3", result.stdout)

    def test_harvest_continues_after_failed_and_empty_sources(self):
        valid = self.tmp / "valid"
        empty = self.tmp / "empty"
        empty.mkdir()
        write_skill(valid, ".", "valid-skill", "A valid Skill with enough description to survive filtering")
        result, records = self.run_harvest([
            {"repo": "vendor/valid", "commit": COMMIT, "kind": "community", "local_path": str(valid)},
            {"repo": "vendor/empty", "commit": COMMIT, "kind": "community", "local_path": str(empty)},
            {"repo": "vendor/missing", "commit": COMMIT, "kind": "community", "local_path": str(self.tmp / "missing")},
        ])
        self.assertEqual([record["id"] for record in records], ["vendor/valid"])
        self.assertIn("Sources with 0 Skills: 1", result.stdout)
        self.assertIn("0 Skills: vendor/empty", result.stdout)
        self.assertIn("Sources that could not be fetched or collected: 1", result.stdout)
        self.assertIn("Fetch/collection failed: vendor/missing", result.stdout)

    def test_harvest_deduplicates_by_description_priority_not_name(self):
        fixtures = [
            ("official/skills", "official", 1, "official-copy", "Shared official capability with enough detail for indexing"),
            ("community/popular", "community", 9999, "popular-copy", " shared   OFFICIAL capability with enough detail for indexing "),
            ("high/stars", "community", 100, "community-copy", "Shared community capability with enough detail for indexing"),
            ("low/stars", "community", 10, "community-copy", "shared community capability with enough detail for indexing"),
            ("zeta/skills", "community", 50, "tie-copy", "Tie breaker capability with enough detail for indexing"),
            ("alpha/skills", "community", 50, "tie-copy", "tie breaker capability with enough detail for indexing"),
            ("same-name/a", "community", 0, "shared-name", "First distinct capability with enough descriptive detail"),
            ("same-name/b", "community", 0, "shared-name", "Second distinct capability with enough descriptive detail"),
        ]
        sources = []
        for repo_name, kind, stars, name, description in fixtures:
            repo = self.tmp / repo_name
            write_skill(repo, ".", name, description)
            sources.append({
                "repo": repo_name, "commit": COMMIT, "kind": kind,
                "stars": stars, "local_path": str(repo),
            })
        result, records = self.run_harvest(sources)
        self.assertEqual(
            {record["id"] for record in records},
            {"official/skills", "high/stars", "alpha/skills", "same-name/a", "same-name/b"},
        )
        self.assertIn("Removed 3 Skills with duplicate normalized descriptions", result.stdout)

    def test_expand_sources_extracts_and_deduplicates_fake_readme(self):
        readme = self.tmp / "README.md"
        readme.write_text(
            "[One](https://github.com/Example/One)\n"
            "[Same repo, path link](https://github.com/example/one/tree/main/skills)\n"
            "[Same repo, issue link](https://github.com/Example/One/issues/1)\n"
            "[Two](https://github.com/Example/Two.git)\n"
            "[Not a repo](https://github.com/topics/skills)\n"
            "[User project](https://github.com/users/example/projects/1)\n"
            "[Advisory](https://github.com/advisories/GHSA-example)\n"
            "[Attachment](https://github.com/user-attachments/assets/example)\n"
            "[Elsewhere](https://example.com/Example/Three)\n",
            encoding="utf-8",
        )
        self.assertEqual(
            expand_sources.extract_repositories(readme.read_text(encoding="utf-8")),
            ["Example/One", "Example/Two"],
        )

    def test_expand_sources_readme_case_and_source_deduplication(self):
        (self.tmp / "rEaDmE.mD").write_text("# Fixture\n", encoding="utf-8")
        self.assertEqual(expand_sources.find_readme(self.tmp), self.tmp / "rEaDmE.mD")
        sources = [
            {"repo": "Example/One", "commit": COMMIT},
            {"repo": "example/one", "commit": "b" * 40},
            {"repo": "Example/Two", "commit": COMMIT},
        ]
        unique, removed = expand_sources.deduplicate_sources(sources)
        self.assertEqual(removed, 1)
        self.assertEqual([source["repo"] for source in unique], ["Example/One", "Example/Two"])

    def test_render_readme_summarizes_sources_in_both_languages(self):
        catalog = self.tmp / "catalog"
        catalog.mkdir()
        (catalog / "skills.json").write_text(json.dumps([
            {"source": "z/repo"}, {"source": "a/repo"}, {"source": "a/repo"},
        ]), encoding="utf-8")
        for name in ("README.md", "README.zh-TW.md"):
            (self.tmp / name).write_text(
                "# Fixture\n<!-- CATALOG:START -->\nold\n<!-- CATALOG:END -->\n",
                encoding="utf-8",
            )
        original_root = render_readme.ROOT
        try:
            render_readme.ROOT = self.tmp
            render_readme.main()
        finally:
            render_readme.ROOT = original_root
        english = (self.tmp / "README.md").read_text(encoding="utf-8")
        chinese = (self.tmp / "README.zh-TW.md").read_text(encoding="utf-8")
        self.assertIn("3 Skills from 2 sources", english)
        self.assertIn("[a/repo](https://github.com/a/repo) — 2 Skills", english)
        self.assertIn("[z/repo](https://github.com/z/repo) — 1 Skill", english)
        self.assertIn("3 個 Skill，來自 2 個來源", chinese)
        self.assertNotIn("old", english)

    def test_build_and_search_catalog(self):
        index = self.build_fixture_index()
        meta = json.loads((index / "meta.json").read_text(encoding="utf-8"))
        self.assertEqual(meta["skill_count"], 3)
        self.assertEqual(meta["format_version"], 4)
        self.assertEqual(meta["dtype"], "float16")
        self.assertEqual(meta["text_source"], "name+description")
        with np.load(index / "vectors.npz", allow_pickle=False) as data:
            self.assertEqual(data["raw"].dtype, np.float16)
        result = self.run_cli(
            FIND, "search", "transform a PDF file", "--index", str(index), "--top", "2", "--json"
        )
        output = json.loads(result.stdout)
        self.assertEqual(output["results"][0]["id"], "vendor/skills/pdf")
        self.assertEqual(output["results"][0]["raw_url"], self.catalog_record("pdf")["raw_url"])
        self.assertEqual(
            set(output["results"][0]),
            {"id", "name", "description", "url", "raw_url", "commit", "kind", "has_scripts", "score"},
        )
        self.assertTrue(all(payload["input_type"] in ("document", "query") for payload in EmbeddingHandler.payloads))
        self.assertTrue(all(COMMIT not in json.dumps(payload["input"]) for payload in EmbeddingHandler.payloads))
        query_cache = self.tmp / "home" / ".cache" / "awesome-agent-skills" / "query-cache.json"
        self.assertTrue(query_cache.is_file())
        self.assertFalse(list(query_cache.parent.glob("*.tmp")))

    def test_symlinked_search_runs_outside_repository(self):
        fake_root = self.tmp / "fake-root"
        catalog = fake_root / "catalog" / "skills.json"
        catalog.parent.mkdir(parents=True)
        catalog.write_text(json.dumps([self.catalog_record("pdf")]), encoding="utf-8")
        index = fake_root / "index"
        self.run_cli(FIND, "build", str(catalog), "--out", str(index))
        script = fake_root / "find-skill" / "scripts" / "find.py"
        script.parent.mkdir(parents=True)
        shutil.copy2(FIND, script)
        installed = self.tmp / "agent" / "find-skill"
        installed.parent.mkdir()
        installed.symlink_to(fake_root / "find-skill", target_is_directory=True)
        outside = self.tmp / "outside"
        outside.mkdir()
        result = self.run_cli(
            installed / "scripts" / "find.py", "search", "transform PDF",
            "--top", "1", "--json", cwd=outside,
        )
        self.assertEqual(json.loads(result.stdout)["results"][0]["id"], "vendor/skills/pdf")

    def test_copied_skill_without_repository_has_clear_error(self):
        script = self.tmp / "copied" / "find-skill" / "scripts" / "find.py"
        script.parent.mkdir(parents=True)
        shutil.copy2(FIND, script)
        outside = self.tmp / "outside"
        outside.mkdir()
        before = len(EmbeddingHandler.payloads)
        result = self.run_cli(script, "search", "PDF", "--json", check=False, cwd=outside)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("SKILL_FINDER_ROOT", result.stderr)
        self.assertIn("symlink", result.stderr)
        self.assertIn("Clone the full", result.stderr)
        self.assertEqual(len(EmbeddingHandler.payloads), before)

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
