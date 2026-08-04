"""Verify that a release tag exactly matches the built wheel version."""

from __future__ import annotations

import argparse
import email.parser
import zipfile
from pathlib import Path


def wheel_version(wheel: Path) -> str:
    with zipfile.ZipFile(wheel) as archive:
        metadata_names = [name for name in archive.namelist() if name.endswith(".dist-info/METADATA")]
        if len(metadata_names) != 1:
            raise ValueError(f"Expected one METADATA file in {wheel}, found {len(metadata_names)}")
        metadata = email.parser.Parser().parsestr(archive.read(metadata_names[0]).decode())
    version = metadata.get("Version")
    if version is None:
        raise ValueError(f"Wheel has no Version metadata: {wheel}")
    return version


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tag")
    parser.add_argument("wheel", type=Path)
    args = parser.parse_args()
    expected = args.tag.removeprefix("v")
    actual = wheel_version(args.wheel)
    if actual != expected:
        raise SystemExit(f"Release tag {args.tag!r} does not match wheel version {actual!r}")
    print(f"Release tag matches wheel version {actual}.")


if __name__ == "__main__":
    main()
