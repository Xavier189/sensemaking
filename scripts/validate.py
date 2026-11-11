#!/usr/bin/env python3
"""Self-contained static validator and isolated fixture stager for sensemaking."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = ROOT / "skills" / "sensemaking"
EVALS_PATH = ROOT / "evals" / "evals.json"
FIXTURES_ROOT = ROOT / "evals" / "fixtures"

ALLOWED_FRONTMATTER_KEYS = {
    "name",
    "description",
    "license",
    "allowed-tools",
    "metadata",
    "compatibility",
}
KEBAB_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MD_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


def _parse_simple_frontmatter(text: str) -> tuple[dict[str, object] | None, str | None]:
    if not text.startswith("---\n"):
        return None, "SKILL.md must start with YAML frontmatter ('---')"
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        return None, "Invalid YAML frontmatter delimiters in SKILL.md"
    raw = match.group(1)
    try:
        import yaml  # type: ignore

        parsed = yaml.safe_load(raw)
        if not isinstance(parsed, dict):
            return None, "Frontmatter must parse to a mapping"
        return parsed, None
    except ModuleNotFoundError:
        data: dict[str, object] = {}
        current_map_key: str | None = None
        for line_no, line in enumerate(raw.splitlines(), start=2):
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            if line.startswith("  ") and current_map_key is not None:
                sub = line.strip()
                if ":" not in sub:
                    return None, f"Invalid nested YAML at line {line_no}"
                k, v = sub.split(":", 1)
                nested = data.setdefault(current_map_key, {})
                if isinstance(nested, dict):
                    nested[k.strip()] = v.strip().strip("\"'")
                continue
            current_map_key = None
            if ":" not in line:
                return None, f"Invalid YAML line {line_no}: {line}"
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip()
            if not val:
                data[key] = {}
                current_map_key = key
            else:
                data[key] = val.strip("\"'")
        return data, None
    except Exception as exc:
        return None, f"Invalid YAML in SKILL.md frontmatter: {exc}"


def validate_skill_package(errors: list[str]) -> None:
    skill_md = SKILL_DIR / "SKILL.md"
    if not skill_md.is_file():
        errors.append(f"Missing {skill_md.relative_to(ROOT)}")
        return

    frontmatter, err = _parse_simple_frontmatter(skill_md.read_text(encoding="utf-8"))
    if err or frontmatter is None:
        errors.append(err or "Failed to parse SKILL.md frontmatter")
        return

    unexpected = set(frontmatter.keys()) - ALLOWED_FRONTMATTER_KEYS
    if unexpected:
        errors.append(
            f"Unexpected SKILL.md frontmatter keys: {', '.join(sorted(unexpected))}"
        )

    name = frontmatter.get("name")
    if not isinstance(name, str) or not name.strip():
        errors.append("SKILL.md frontmatter missing non-empty 'name'")
    else:
        if name != SKILL_DIR.name:
            errors.append(
                f"SKILL.md name '{name}' must match directory '{SKILL_DIR.name}'"
            )
        if len(name) > 64 or not KEBAB_RE.match(name):
            errors.append(f"Invalid skill name '{name}'")

    description = frontmatter.get("description")
    if not isinstance(description, str) or not description.strip():
        errors.append("SKILL.md frontmatter missing non-empty 'description'")
    else:
        if "<" in description or ">" in description:
            errors.append("SKILL.md description must not contain '<' or '>'")
        if len(description) > 1024:
            errors.append(
                f"SKILL.md description too long ({len(description)} > 1024 chars)"
            )

    compatibility = frontmatter.get("compatibility")
    if compatibility is not None:
        if not isinstance(compatibility, str) or len(compatibility) > 500:
            errors.append("SKILL.md 'compatibility' must be a string <= 500 chars")

    openai_yaml = SKILL_DIR / "agents" / "openai.yaml"
    if not openai_yaml.is_file():
        errors.append(f"Missing {openai_yaml.relative_to(ROOT)}")
    else:
        raw_yaml = openai_yaml.read_text(encoding="utf-8")
        for required_key in (
            "display_name:",
            "short_description:",
            "default_prompt:",
            "allow_implicit_invocation:",
        ):
            if required_key not in raw_yaml:
                errors.append(f"openai.yaml missing '{required_key}'")

    for path in SKILL_DIR.rglob("*"):
        if path.is_file():
            if path.name.startswith(".") or path.stat().st_size == 0:
                errors.append(
                    f"Unexpected hidden or empty file in skill package: {path.relative_to(ROOT)}"
                )


def validate_evals(errors: list[str]) -> dict[int, dict[str, object]]:
    by_id: dict[int, dict[str, object]] = {}
    if not EVALS_PATH.is_file():
        errors.append(f"Missing {EVALS_PATH.relative_to(ROOT)}")
        return by_id

    try:
        payload = json.loads(EVALS_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"Invalid JSON in {EVALS_PATH.relative_to(ROOT)}: {exc}")
        return by_id

    if payload.get("skill_name") != "sensemaking":
        errors.append("evals.json skill_name must be 'sensemaking'")

    evals = payload.get("evals")
    if not isinstance(evals, list) or not evals:
        errors.append("evals.json 'evals' must be a non-empty list")
        return by_id

    seen_names: set[str] = set()
    referenced_fixtures: set[Path] = set()

    for expected_id, entry in enumerate(evals):
        if not isinstance(entry, dict):
            errors.append(f"Eval at index {expected_id} must be an object")
            continue
        actual_id = entry.get("id")
        if actual_id != expected_id:
            errors.append(
                f"Eval IDs must be contiguous 0..N-1 (expected {expected_id}, got {actual_id})"
            )
        if isinstance(actual_id, int):
            by_id[actual_id] = entry

        name = entry.get("name")
        if not isinstance(name, str) or not KEBAB_RE.match(name):
            errors.append(f"Eval {actual_id} has invalid kebab-case name: {name!r}")
        elif name in seen_names:
            errors.append(f"Duplicate eval name: {name}")
        else:
            seen_names.add(name)

        invocation = entry.get("invocation")
        if invocation not in {"implicit", "explicit"}:
            errors.append(
                f"Eval {actual_id} ({name}) must declare invocation as 'implicit' or 'explicit'"
            )

        for str_field in ("prompt", "expected_output"):
            val = entry.get(str_field)
            if not isinstance(val, str) or not val.strip():
                errors.append(f"Eval {actual_id} ({name}) missing non-empty '{str_field}'")

        assertions = entry.get("assertions")
        if (
            not isinstance(assertions, list)
            or not assertions
            or not all(isinstance(a, str) and a.strip() for a in assertions)
        ):
            errors.append(f"Eval {actual_id} ({name}) must have non-empty string assertions")

        files = entry.get("files")
        if not isinstance(files, list):
            errors.append(f"Eval {actual_id} ({name}) 'files' must be a list")
        else:
            for rel in files:
                if not isinstance(rel, str):
                    errors.append(f"Eval {actual_id} ({name}) file path must be a string")
                    continue
                target = (ROOT / rel).resolve()
                if not target.is_file():
                    errors.append(f"Eval {actual_id} ({name}) missing fixture: {rel}")
                elif FIXTURES_ROOT.resolve() not in target.parents:
                    errors.append(
                        f"Eval {actual_id} ({name}) fixture outside evals/fixtures/: {rel}"
                    )
                else:
                    referenced_fixtures.add(target)

        follow_ups = entry.get("follow_up_turns", [])
        if not isinstance(follow_ups, list):
            errors.append(f"Eval {actual_id} ({name}) 'follow_up_turns' must be a list")
        else:
            for turn_idx, turn in enumerate(follow_ups, start=1):
                if not isinstance(turn, dict):
                    errors.append(f"Eval {actual_id} turn {turn_idx} must be an object")
                    continue
                for str_field in ("prompt", "expected_output"):
                    val = turn.get(str_field)
                    if not isinstance(val, str) or not val.strip():
                        errors.append(
                            f"Eval {actual_id} turn {turn_idx} missing '{str_field}'"
                        )
                t_asserts = turn.get("assertions")
                if (
                    not isinstance(t_asserts, list)
                    or not t_asserts
                    or not all(isinstance(a, str) and a.strip() for a in t_asserts)
                ):
                    errors.append(
                        f"Eval {actual_id} turn {turn_idx} must have non-empty assertions"
                    )

    if FIXTURES_ROOT.is_dir():
        for disk_file in sorted(FIXTURES_ROOT.rglob("*")):
            if disk_file.is_file() and disk_file.resolve() not in referenced_fixtures:
                errors.append(
                    f"Unreferenced orphan fixture: {disk_file.relative_to(ROOT)}"
                )

    return by_id


def validate_repo_links_and_json(errors: list[str]) -> None:
    md_roots = [ROOT / "README.md"]
    md_roots.extend(sorted((ROOT / "docs").rglob("*.md")))
    md_roots.extend(sorted(SKILL_DIR.rglob("*.md")))

    for md_path in md_roots:
        if not md_path.is_file():
            continue
        in_fence = False
        for line_no, line in enumerate(
            md_path.read_text(encoding="utf-8").splitlines(), start=1
        ):
            stripped = line.lstrip()
            if stripped.startswith("```") or stripped.startswith("~~~"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            for raw_target in MD_LINK_RE.findall(line):
                target_str = raw_target.strip().split()[0]
                if target_str.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                rel_part = target_str.split("#", 1)[0]
                if not rel_part:
                    continue
                resolved = (md_path.parent / rel_part).resolve()
                if not resolved.exists():
                    errors.append(
                        f"Broken relative link in {md_path.relative_to(ROOT)}:{line_no} -> {target_str}"
                    )

    tracked: list[Path] = []
    proc = subprocess.run(
        ["git", "ls-files", "*.json"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode == 0:
        tracked = [ROOT / p for p in proc.stdout.splitlines() if p.strip()]
    else:
        tracked = list(ROOT.rglob("*.json"))

    for json_path in tracked:
        if not json_path.is_file():
            continue
        if json_path.stat().st_size == 0:
            errors.append(f"Empty JSON file: {json_path.relative_to(ROOT)}")
            continue
        try:
            json.loads(json_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"Invalid JSON in {json_path.relative_to(ROOT)}: {exc}")


def stage_eval_fixtures(
    eval_id: int, dest_dir: Path, evals_by_id: dict[int, dict[str, object]]
) -> int:
    if eval_id not in evals_by_id:
        print(f"Unknown eval id: {eval_id}", file=sys.stderr)
        return 1
    entry = evals_by_id[eval_id]
    dest_dir = dest_dir.resolve()
    dest_dir.mkdir(parents=True, exist_ok=True)
    staged: list[str] = []
    files = entry.get("files", [])
    assert isinstance(files, list)
    for rel in files:
        assert isinstance(rel, str)
        src = ROOT / rel
        rel_inside_fixtures = src.resolve().relative_to(FIXTURES_ROOT.resolve())
        # Flatten the top-level fixture group folder so relative sibling names match prompts
        parts = rel_inside_fixtures.parts
        rel_dest = Path(*parts[1:]) if len(parts) > 1 else rel_inside_fixtures
        out_path = dest_dir / rel_dest
        out_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, out_path)
        staged.append(str(out_path))
    print(
        json.dumps(
            {
                "id": eval_id,
                "name": entry["name"],
                "invocation": entry["invocation"],
                "dest": str(dest_dir),
                "staged_files": staged,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--stage-eval",
        nargs=2,
        metavar=("EVAL_ID", "DEST_DIR"),
        help="Copy only the specified eval's input fixtures into an isolated directory.",
    )
    args = parser.parse_args()

    errors: list[str] = []
    validate_skill_package(errors)
    evals_by_id = validate_evals(errors)
    validate_repo_links_and_json(errors)

    if errors:
        for item in errors:
            print(f"ERROR: {item}", file=sys.stderr)
        return 1

    if args.stage_eval:
        eval_id_str, dest_str = args.stage_eval
        return stage_eval_fixtures(int(eval_id_str), Path(dest_str), evals_by_id)

    print(
        f"OK: skill 'sensemaking' valid, {len(evals_by_id)} evals verified, links and JSON clean."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
