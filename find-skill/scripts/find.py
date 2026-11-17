#!/usr/bin/env python3
"""Build and search an Agent Skill catalog with embeddings."""

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import sys
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path

try:
    import numpy as np
except ImportError:
    print("Error: numpy required. Install with: python3 -m pip install -r requirements.txt")
    sys.exit(1)

DEFAULT_EMBED_URL = "https://api.voyageai.com/v1/embeddings"
DEFAULT_EMBED_MODEL = "voyage-3.5"
BATCH = 128
FORMAT_VERSION = 4
INSTALL_HELP = (
    "Clone the full awesome-agent-skills repository and install find-skill with a symlink, "
    "or set SKILL_FINDER_ROOT to the repository root."
)


def sha(*parts):
    return hashlib.sha256("\0".join(parts).encode("utf-8")).hexdigest()


def jload(path, default=None):
    path = Path(path)
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default


def jsave(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=path.parent,
            prefix=path.name + ".", suffix=".tmp", delete=False,
        ) as stream:
            temporary = Path(stream.name)
            json.dump(value, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
        os.replace(temporary, path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def repository_root():
    configured = os.environ.get("SKILL_FINDER_ROOT")
    if configured:
        return Path(configured).expanduser().resolve()
    return Path(__file__).resolve().parents[2]


def default_catalog():
    return repository_root() / "catalog" / "skills.json"


def default_index():
    return repository_root() / "index"


def query_cache_path():
    return Path.home() / ".cache" / "awesome-agent-skills" / "query-cache.json"


def load_env(path):
    if not path:
        return
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        match = re.match(r"^([A-Z_][A-Z0-9_]*)=(.*)$", line.strip())
        if match:
            os.environ.setdefault(match.group(1), match.group(2).strip())


def post(url, payload, key=None, timeout=120, tries=3):
    headers = {"Content-Type": "application/json"}
    if key:
        headers["Authorization"] = "Bearer " + key
    error = ""
    for attempt in range(tries):
        try:
            request = urllib.request.Request(
                url, json.dumps(payload).encode("utf-8"), method="POST", headers=headers
            )
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return json.loads(response.read())
        except urllib.error.HTTPError as exc:
            error = f"HTTP {exc.code}: {exc.read().decode('utf-8', errors='replace')[:500]}"
            if 400 <= exc.code < 500 and exc.code != 429:
                break
        except (urllib.error.URLError, TimeoutError, ValueError) as exc:
            error = str(exc)[:500]
        if attempt + 1 < tries:
            time.sleep(attempt + 1)
    raise RuntimeError(f"Embedding request failed: {error}")


def embedding_config(args):
    return {
        "embed_url": getattr(args, "embed_url", None)
        or os.environ.get("SKILL_FINDER_EMBED_URL", DEFAULT_EMBED_URL),
        "embed_model": getattr(args, "embed_model", None)
        or os.environ.get("SKILL_FINDER_EMBED_MODEL", DEFAULT_EMBED_MODEL),
    }


def embed(texts, cache_path, config, input_type):
    cache = jload(cache_path, {})
    url, model = config["embed_url"], config["embed_model"]
    key_for = lambda text: sha(url, model, input_type, text)
    missing = sorted({text for text in texts if key_for(text) not in cache})
    for start in range(0, len(missing), BATCH):
        part = missing[start : start + BATCH]
        payload = {"model": model, "input": part}
        if "voyage" in url.lower():
            payload["input_type"] = input_type
        key = os.environ.get("SKILL_FINDER_EMBED_KEY") or os.environ.get("VOYAGE_API_KEY")
        response = post(url, payload, key)
        rows = sorted(response.get("data", []), key=lambda row: row["index"])
        if len(rows) != len(part):
            raise RuntimeError(f"Embedding endpoint returned {len(rows)} rows for {len(part)} inputs")
        for text, row in zip(part, rows):
            cache[key_for(text)] = row["embedding"]
        jsave(cache_path, cache)
    output = {}
    for text in texts:
        vector = np.asarray(cache[key_for(text)], dtype=np.float32)
        norm = np.linalg.norm(vector)
        if not norm:
            raise RuntimeError("Embedding endpoint returned a zero vector")
        output[text] = vector / norm
    return output


def load_catalog(path):
    records = jload(path)
    if not isinstance(records, list) or not records:
        raise ValueError(f"Catalog must be a non-empty JSON list: {path}")
    required = ("id", "name", "description", "source", "path", "commit", "url", "raw_url", "kind", "has_scripts")
    ids = set()
    for number, record in enumerate(records, 1):
        if not isinstance(record, dict):
            raise ValueError(f"Catalog entry {number} must be an object")
        for field in required:
            if field not in record:
                raise ValueError(f"Catalog entry {number} is missing {field}")
        if record["id"] in ids:
            raise ValueError(f"Duplicate catalog ID: {record['id']}")
        ids.add(record["id"])
        if record["kind"] not in ("official", "community") or not isinstance(record["has_scripts"], bool):
            raise ValueError(f"Invalid kind or has_scripts for {record['id']}")
    return records


def embedded_text(record):
    return f"{record['name']}\n{record['description']}"


def cmd_build(args):
    catalog = Path(args.catalog).expanduser().resolve() if args.catalog else default_catalog()
    if not catalog.is_file():
        raise ValueError(f"Catalog not found: {catalog}. {INSTALL_HELP}")
    records = load_catalog(catalog)
    out = Path(args.out).expanduser().resolve() if args.out else default_index()
    config = embedding_config(args)
    texts = [embedded_text(record) for record in records]
    vectors = embed(texts, out / "cache" / "embeddings.json", config, "document")
    matrix = np.stack([vectors[text] for text in texts])
    np.savez_compressed(
        out / "vectors.npz",
        ids=np.array([record["id"] for record in records]),
        raw=matrix.astype(np.float16),
    )
    jsave(out / "skills.json", records)
    jsave(out / "meta.json", {
        "format_version": FORMAT_VERSION,
        **config,
        "dimension": int(matrix.shape[1]),
        "dtype": "float16",
        "created_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "skill_count": len(records),
        "text_source": "name+description",
    })
    print(f"Indexed {len(records)} Skills with {config['embed_model']} (name+description)")
    print(f"Wrote {out}")


class Index:
    def __init__(self, directory, config=None):
        self.dir = Path(directory).expanduser().resolve()
        if not all((self.dir / name).is_file() for name in ("skills.json", "meta.json", "vectors.npz")):
            sys.exit(f"Error: index not found or incomplete at {self.dir}. {INSTALL_HELP}")
        self.skills = jload(self.dir / "skills.json")
        self.meta = jload(self.dir / "meta.json")
        if self.meta.get("format_version") != FORMAT_VERSION:
            sys.exit(f"Error: unsupported index format in {self.dir}")
        if config and (
            config["embed_model"] != self.meta.get("embed_model")
            or config["embed_url"] != self.meta.get("embed_url")
        ):
            sys.exit(
                "Error: query embedding endpoint/model differs from the index. "
                f"Index: {self.meta.get('embed_url')} / {self.meta.get('embed_model')}; "
                f"query: {config['embed_url']} / {config['embed_model']}. "
                "Rebuild with build --out LOCAL_INDEX and search --index LOCAL_INDEX."
            )
        with np.load(self.dir / "vectors.npz", allow_pickle=False) as data:
            self.ids = [str(item) for item in data["ids"]]
            self.raw = data["raw"].astype(np.float32)
        if self.ids != [record["id"] for record in self.skills] or len(self.ids) != len(self.raw):
            sys.exit(f"Error: inconsistent index files in {self.dir}")
        if self.raw.shape[1] != self.meta.get("dimension"):
            sys.exit(f"Error: vector dimension does not match {self.dir}/meta.json")


def search(index, query, top):
    query_vector = embed(
        [query], query_cache_path(),
        {"embed_url": index.meta["embed_url"], "embed_model": index.meta["embed_model"]}, "query",
    )[query]
    scores = index.raw @ query_vector
    results = []
    for position in np.argsort(-scores, kind="stable")[:top]:
        record = index.skills[position]
        results.append({
            "id": record["id"],
            "name": record["name"],
            "description": record["description"],
            "url": record["url"],
            "raw_url": record["raw_url"],
            "commit": record["commit"],
            "kind": record["kind"],
            "has_scripts": record["has_scripts"],
            "score": round(float(scores[position]), 6),
        })
    return {"results": results}


def cmd_search(args):
    if args.top < 1:
        sys.exit("Error: --top must be positive")
    if not args.query.strip():
        sys.exit("Error: query must not be empty")
    index_path = Path(args.index).expanduser().resolve() if args.index else default_index()
    index = Index(index_path, embedding_config(args))
    output = {"query": args.query, **search(index, args.query, args.top)}
    if args.json:
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return
    for rank, result in enumerate(output["results"], 1):
        print(f"{rank}. {result['name']} ({result['id']}) score={result['score']:.3f}")
        print(result["description"])
        print(f"URL: {result['url']}")
        print(f"Raw URL: {result['raw_url']}")


def main():
    parser = argparse.ArgumentParser(description="Build and search an Agent Skill catalog")
    parser.add_argument("--env", help="file with SKILL_FINDER_* KEY=VALUE settings")
    subparsers = parser.add_subparsers(dest="command", required=True)

    build = subparsers.add_parser("build", help="embed catalog names and descriptions")
    build.add_argument("catalog", nargs="?")
    build.add_argument("--out")
    build.add_argument("--embed-url")
    build.add_argument("--embed-model")
    build.set_defaults(func=cmd_build)

    search_parser = subparsers.add_parser("search", help="retrieve Skills for the agent to judge")
    search_parser.add_argument("query")
    search_parser.add_argument("--index")
    search_parser.add_argument("--top", type=int, default=8)
    search_parser.add_argument("--embed-url")
    search_parser.add_argument("--embed-model")
    search_parser.add_argument("--json", action="store_true")
    search_parser.set_defaults(func=cmd_search)

    args = parser.parse_args()
    load_env(args.env)
    try:
        args.func(args)
    except (ValueError, RuntimeError) as exc:
        sys.exit(f"Error: {exc}")


if __name__ == "__main__":
    main()
