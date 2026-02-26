#!/usr/bin/env python3
"""Package a skill directory into a .skill file.

Usage:
    python package_skill.py <skill-directory> [output-directory]
"""

import argparse
import os
import zipfile
from pathlib import Path


def validate_skill(skill_dir: Path) -> bool:
    """Validate a skill directory before packaging."""
    if not skill_dir.is_dir():
        print(f"ERROR: Not a directory: {skill_dir}")
        return False

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        print(f"ERROR: Missing SKILL.md in: {skill_dir}")
        return False

    with open(skill_md, "r") as f:
        content = f.read()

    if not content.startswith("---"):
        print("ERROR: SKILL.md should start with YAML frontmatter (---)")
        return False

    # Check for name and description in frontmatter
    if "name:" not in content[:200] or "description:" not in content[:200]:
        print("ERROR: SKILL.md frontmatter missing 'name' or 'description'")
        return False

    return True


def package_skill(skill_dir: Path, output_dir: Path) -> Path:
    """Package skill directory into a .skill file."""
    skill_name = skill_dir.name
    output_file = output_dir / f"{skill_name}.skill"

    with zipfile.ZipFile(output_file, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(skill_dir):
            for file in files:
                file_path = Path(root) / file
                arcname = file_path.relative_to(skill_dir.parent)
                zf.write(file_path, arcname)

    return output_file


def main():
    parser = argparse.ArgumentParser(description="Package a skill directory")
    parser.add_argument("skill_dir", help="Skill directory to package")
    parser.add_argument(
        "output_dir", nargs="?", default=".", help="Output directory (default: .)"
    )

    args = parser.parse_args()
    skill_dir = Path(args.skill_dir)
    output_dir = Path(args.output_dir)

    if not validate_skill(skill_dir):
        import sys

        sys.exit(1)

    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = package_skill(skill_dir, output_dir)

    print(f"✓ Skill packaged successfully: {output_file}")
    print(f"  Size: {output_file.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
