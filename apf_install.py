#!/usr/bin/env python3
"""
Install / update the agentic framework into the current project folder.

Usage:
    python install_framework.py [--dry-run] [--branch main] [--force]

Place this script in your project root and run it from there.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# ── Configuration ────────────────────────────────────────────────────────────

REPO_URL = "https://github.com/YOUR_USER/YOUR_REPO.git"
DEFAULT_BRANCH = "main"

# Source path inside the cloned repo → destination path relative to project root.
# Directories are copied recursively; files are copied individually.
FILE_MAP: dict[str, str] = {
    "template/.claude/commands": ".claude/commands",
    "template/hooks":            ".claude/hooks",
    "template/CLAUDE.md":        "CLAUDE.md",
    # Add more mappings as needed:
    # "template/some_config.toml": ".config/some_config.toml",
}

# Files where we inject content between markers instead of overwriting.
# These must also appear in FILE_MAP above.
MARKER_MERGE_FILES: set[str] = {
    "CLAUDE.md",
}

MARKER_BEGIN = "<!-- BEGIN APF -->"
MARKER_END = "<!-- END APF -->"
VERSION_FILE = ".apf-version"

# ── Core logic ───────────────────────────────────────────────────────────────


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without touching any files.",
    )
    p.add_argument(
        "--branch",
        default=DEFAULT_BRANCH,
        help=f"Git branch / tag to clone (default: {DEFAULT_BRANCH}).",
    )
    p.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files without prompting.",
    )
    return p.parse_args()


def clone_repo(tmp_dir: Path, branch: str) -> Path:
    """Shallow-clone the framework repo into *tmp_dir* and return the path."""
    dest = tmp_dir / "framework"
    print(f"⏳ Cloning {REPO_URL} (branch: {branch}) …")
    subprocess.run(
        [
            "git", "clone",
            "--depth", "1",
            "--branch", branch,
            REPO_URL,
            str(dest),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    print("✅ Clone complete.")
    return dest


def read_framework_version(repo_dir: Path) -> str:
    """Read the version string shipped with the framework repo."""
    version_path = repo_dir / "VERSION"
    if version_path.exists():
        return version_path.read_text().strip()
    # Fallback: use the short commit hash.
    result = subprocess.run(
        ["git", "-C", str(repo_dir), "rev-parse", "--short", "HEAD"],
        capture_output=True, text=True, check=True,
    )
    return result.stdout.strip()


def merge_with_markers(
    source_content: str,
    dest_path: Path,
    version: str,
    *,
    dry_run: bool,
) -> None:
    """Insert *source_content* between markers in an existing file,
    or append the marked block if the file has no markers yet."""
    managed_block = (
        f"{MARKER_BEGIN}\n"
        f"<!-- managed by agentic-framework {version} — do not edit manually -->\n"
        f"{source_content}\n"
        f"{MARKER_END}"
    )

    if dest_path.exists():
        existing = dest_path.read_text()
        if MARKER_BEGIN in existing and MARKER_END in existing:
            # Replace the existing managed block.
            before = existing[: existing.index(MARKER_BEGIN)]
            after = existing[existing.index(MARKER_END) + len(MARKER_END) :]
            new_content = before + managed_block + after
            action = "update"
        else:
            # Append managed block to the end.
            new_content = existing.rstrip() + "\n\n" + managed_block + "\n"
            action = "append"
    else:
        new_content = managed_block + "\n"
        action = "create"

    if dry_run:
        print(f"  [dry-run] Would {action} managed block in {dest_path}")
    else:
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        dest_path.write_text(new_content)
        print(f"  ✏️  {action.capitalize()}d managed block in {dest_path}")


def copy_entry(
    src: Path,
    dest: Path,
    *,
    dry_run: bool,
    force: bool,
) -> None:
    """Copy a single file or directory tree from *src* to *dest*."""
    if src.is_dir():
        if dry_run:
            print(f"  [dry-run] Would copy directory {src.name}/ → {dest}")
            return
        if dest.exists():
            if force:
                shutil.rmtree(dest)
            else:
                # Merge: copy tree on top of existing dir.
                pass
        shutil.copytree(src, dest, dirs_exist_ok=True)
        print(f"  📁 Copied directory → {dest}")
    else:
        if dest.exists() and not force:
            print(f"  ⚠️  Skipping {dest} (exists; use --force to overwrite)")
            return
        if dry_run:
            print(f"  [dry-run] Would copy {src.name} → {dest}")
            return
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        print(f"  📄 Copied → {dest}")


def install(repo_dir: Path, project_dir: Path, version: str, args: argparse.Namespace) -> None:
    """Walk FILE_MAP and copy / merge everything into the project."""
    print(f"\n📦 Installing framework v{version} into {project_dir}\n")

    for src_rel, dest_rel in FILE_MAP.items():
        src = repo_dir / src_rel
        dest = project_dir / dest_rel

        if not src.exists():
            print(f"  ⚠️  Source not found in repo: {src_rel} — skipping")
            continue

        if dest_rel in MARKER_MERGE_FILES:
            source_content = src.read_text()
            merge_with_markers(source_content, dest, version, dry_run=args.dry_run)
        else:
            copy_entry(src, dest, dry_run=args.dry_run, force=args.force)

    # Write version stamp.
    version_path = project_dir / VERSION_FILE
    if args.dry_run:
        print(f"\n  [dry-run] Would write version {version} → {version_path}")
    else:
        version_path.write_text(version + "\n")
        print(f"\n✅ Installed. Version recorded in {VERSION_FILE}")


# ── Entry point ──────────────────────────────────────────────────────────────


def main() -> None:
    args = parse_args()
    project_dir = Path.cwd()

    # Confirm before proceeding.
    existing_version_path = project_dir / VERSION_FILE
    if existing_version_path.exists():
        action = "update"
    else:
        action = "install"
    print(f"This will {action} the APF framework in {project_dir}")
    if input("Continue? [y/N] ").strip().lower() not in ("y", "yes"):
        print("Aborted.")
        sys.exit(0)

    with tempfile.TemporaryDirectory(prefix="apf-") as tmp:
        tmp_dir = Path(tmp)
        repo_dir = clone_repo(tmp_dir, args.branch)
        version = read_framework_version(repo_dir)

        # Check if already installed at this version.
        existing_version_path = project_dir / VERSION_FILE
        if existing_version_path.exists():
            current = existing_version_path.read_text().strip()
            if current == version and not args.force:
                print(f"ℹ️  Already at version {version}. Use --force to reinstall.")
                sys.exit(0)
            print(f"🔄 Updating {current} → {version}")

        install(repo_dir, project_dir, version, args)


if __name__ == "__main__":
    main()