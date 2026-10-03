import argparse
import logging
import os
import sys
from pathlib import Path

import yaml

PROJECT_DIR = Path(__file__).resolve().parent
# BRBuild is a sibling checkout by default; BRBUILD_DIR overrides it for another layout.
BRBUILD_DIR = Path(os.environ.get("BRBUILD_DIR") or PROJECT_DIR.parent / "BRBuild").expanduser()

if not BRBUILD_DIR.is_dir():
    raise SystemExit(f"BRBuild directory not found: {BRBUILD_DIR}")

sys.path.insert(0, str(BRBUILD_DIR))
from Builder import Builder  # noqa: E402
from Project import Project  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Build BRTrains3 with BRBuild")
    parser.add_argument("--log", action="store_true", help="Write build.log")
    parser.add_argument("--docs", action="store_true", help="Generate the BRDocs manifest after a successful build")
    args = parser.parse_args()

    handlers = [logging.StreamHandler(sys.stdout)]
    if args.log:
        handlers.append(logging.FileHandler(PROJECT_DIR / "build.log", mode="w"))
    logging.basicConfig(level=logging.INFO, handlers=handlers, format="%(levelname)s %(message)s")

    config = yaml.safe_load((PROJECT_DIR / "BRBuild.yaml").read_text(encoding="utf-8"))
    project_config = config["project"]

    palette = project_config.get("palette", "Sprites/ttd-newgrf-dos.gpl")
    palette_path = Path(palette).expanduser()
    if not palette_path.is_absolute():
        # A relative palette is resolved against the BRBuild checkout so the
        # project manifest stays portable between machines and checkouts.
        palette_path = BRBUILD_DIR / palette_path

    project = Project({
        "path": str(PROJECT_DIR),
        "name": project_config["name"],
        "build": project_config.get("build", True),
        "targetFolders": project_config.get("target_folders", []),
        "grfFolder": project_config.get("grf_folder", "src/grf"),
        "soundFolder": project_config.get("sound_folder", "src/sound"),
        "palette": str(palette_path),
        "template_folder": project_config.get("template_folder"),
    })

    Builder().build(project, docs=args.docs)


if __name__ == "__main__":
    main()
