#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import pathlib
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "out" / "release"


def sha256_file(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    manifest = OUT / "release_manifest.json"
    manifest_sha = OUT / "release_manifest.json.sha256"
    manifest_ots = OUT / "release_manifest.json.ots"

    files = {
        "release_manifest.json": {
            "path": str(manifest.relative_to(ROOT)),
            "sha256": sha256_file(manifest),
        },
        "release_manifest.json.ots": {
            "path": str(manifest_ots.relative_to(ROOT)),
            "sha256": sha256_file(manifest_ots),
        },
        "release_manifest.json.sha256": {
            "path": str(manifest_sha.relative_to(ROOT)),
            "sha256": sha256_file(manifest_sha),
        },
    }

    receipt = {
        "version": 1,
        "stage": "stage265",  # ← ここ修正
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "github_actions": {
            "workflow": os.getenv("GITHUB_WORKFLOW", ""),
            "run_id": os.getenv("GITHUB_RUN_ID", ""),
            "run_attempt": os.getenv("GITHUB_RUN_ATTEMPT", ""),
            "sha": os.getenv("GITHUB_SHA", ""),
            "ref": os.getenv("GITHUB_REF", ""),
            "actor": os.getenv("GITHUB_ACTOR", ""),
            "repository": os.getenv("GITHUB_REPOSITORY", ""),
            "server_url": os.getenv("GITHUB_SERVER_URL", ""),
            "run_url": f"{os.getenv('GITHUB_SERVER_URL','')}/{os.getenv('GITHUB_REPOSITORY','')}/actions/runs/{os.getenv('GITHUB_RUN_ID','')}",
        },
        "files": files,
        "meaning": [
            "This receipt proves that the manifest stamping pipeline ran in GitHub Actions.",
            "The manifest hash, sha256 sidecar, and ots proof are bound to this workflow execution.",
        ],
    }

    out_path = OUT / "github_actions_receipt.json"
    out_path.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n")

    print(f"[OK] wrote receipt: {out_path}")


if __name__ == "__main__":
    main()
