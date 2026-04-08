#!/usr/bin/env python3
"""Manage skills: generate manifest, validate."""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


SKILL_METADATA = {
    "databricks-core": {
        "description": "Core Databricks skill for CLI, auth, and data exploration",
        "experimental": False,
    },
    "databricks-apps": {
        "description": "Databricks Apps development and deployment",
        "experimental": False,
    },
    "databricks-jobs": {
        "description": "Databricks Jobs orchestration and scheduling",
        "experimental": False,
    },
    "databricks-lakebase": {
        "description": "Databricks Lakebase database development",
        "experimental": False,
    },
    "databricks-dabs": {
        "description": "Declarative Automation Bundles (DABs) for deploying and managing Databricks resources",
        "experimental": False,
    },
    "databricks-model-serving": {
        "description": "Databricks Model Serving endpoint management",
        "experimental": True,
    },
    "databricks-pipelines": {
        "description": "Databricks Pipelines (DLT) for ETL and streaming",
        "experimental": False,
    },
}


def iter_skill_dirs(repo_root: Path):
    """Yield skill directories that contain SKILL.md."""
    skills_dir = repo_root / "skills"
    for item in sorted(skills_dir.iterdir()):
        if not item.is_dir():
            continue
        if item.name.startswith(".") or item.name == "scripts":
            continue
        if not (item / "SKILL.md").exists():
            continue
        yield item


def extract_version_from_skill(skill_path: Path) -> str:
    """Extract version from SKILL.md frontmatter metadata."""
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        raise ValueError(f"SKILL.md not found in {skill_path}")

    content = skill_md.read_text(encoding="utf-8")

    if not content.startswith("---"):
        raise ValueError(f"SKILL.md in {skill_path} missing frontmatter")

    end_idx = content.find("---", 3)
    if end_idx == -1:
        raise ValueError(f"SKILL.md in {skill_path} has unclosed frontmatter")

    frontmatter = content[3:end_idx]

    version_match = re.search(r'version:\s*["\']?([^"\'\n]+)["\']?', frontmatter)
    if version_match:
        return version_match.group(1).strip()

    return "0.0.0"


def get_skill_updated_at(skill_path: Path) -> str:
    """Get the most recent modification time of any file in the skill directory."""
    latest_mtime = 0.0
    for file_path in skill_path.rglob("*"):
        if file_path.is_file():
            mtime = file_path.stat().st_mtime
            if mtime > latest_mtime:
                latest_mtime = mtime

    if latest_mtime == 0.0:
        return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    return datetime.fromtimestamp(latest_mtime, timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )


# ---------------------------------------------------------------------------
# Manifest generation
# ---------------------------------------------------------------------------

def generate_manifest(repo_root: Path) -> dict:
    """Generate manifest from skill directories."""
    manifest_path = repo_root / "manifest.json"
    existing_skills = {}
    if manifest_path.exists():
        existing_skills = json.loads(manifest_path.read_text(encoding="utf-8")).get("skills", {})

    skills = {}
    for skill_dir in iter_skill_dirs(repo_root):
        files = sorted(
            str(f.relative_to(skill_dir))
            for f in skill_dir.rglob("*")
            if f.is_file()
        )

        if skill_dir.name not in SKILL_METADATA:
            raise ValueError(
                f"Missing SKILL_METADATA entry for skill '{skill_dir.name}'. "
                "Add it to SKILL_METADATA dict."
            )

        metadata = SKILL_METADATA[skill_dir.name]
        skill_entry = {
            "version": extract_version_from_skill(skill_dir),
            "description": metadata.get("description", ""),
            "experimental": metadata.get("experimental", False),
            "updated_at": get_skill_updated_at(skill_dir),
            "files": files,
        }

        if metadata.get("min_cli_version"):
            skill_entry["min_cli_version"] = metadata["min_cli_version"]

        existing = existing_skills.get(skill_dir.name, {})
        if "base_revision" in existing:
            skill_entry["base_revision"] = existing["base_revision"]

        skills[skill_dir.name] = skill_entry

    return {
        "version": "2",
        "updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "skills": skills,
    }


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def normalize_manifest(manifest: dict) -> dict:
    """Normalize manifest for comparison by excluding volatile fields."""
    normalized = manifest.copy()
    normalized.pop("updated_at", None)

    skills = {}
    for name, skill in manifest.get("skills", {}).items():
        skill_copy = skill.copy()
        skill_copy.pop("updated_at", None)
        skill_copy.pop("base_revision", None)
        skills[name] = skill_copy

    normalized["skills"] = skills
    return normalized


def validate_manifest(repo_root: Path) -> bool:
    """Validate that manifest.json is up to date. Returns True if valid."""
    manifest_path = repo_root / "manifest.json"

    if not manifest_path.exists():
        print("ERROR: manifest.json does not exist", file=sys.stderr)
        return False

    current_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    expected_manifest = generate_manifest(repo_root)

    current_normalized = normalize_manifest(current_manifest)
    expected_normalized = normalize_manifest(expected_manifest)

    if current_normalized != expected_normalized:
        print("ERROR: manifest.json is out of date", file=sys.stderr)
        return False

    return True


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Manage skills: generate manifest, validate."
    )
    parser.add_argument(
        "mode",
        nargs="?",
        default="generate",
        choices=["generate", "validate"],
        help=(
            "generate: create manifest.json (default). "
            "validate: check manifest is up to date."
        ),
    )

    args = parser.parse_args()
    repo_root = Path(__file__).parent.parent

    match args.mode:
        case "generate":
            manifest = generate_manifest(repo_root)
            manifest_path = repo_root / "manifest.json"
            manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
            print(f"Generated {manifest_path}")
            print(
                f"Found {len(manifest['skills'])} skill(s): "
                f"{', '.join(manifest['skills'].keys())}"
            )

        case "validate":
            if not validate_manifest(repo_root):
                print(
                    "\nRun `python3 scripts/skills.py generate` to fix.",
                    file=sys.stderr,
                )
                sys.exit(1)

            print("Everything is up to date.")


if __name__ == "__main__":
    main()
