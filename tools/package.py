#!/usr/bin/env python3
"""Packages the bundle as target/fair_freecam-<version>.hnmod for a GitHub release.

The archive holds horizon-native.json and mixins/fair_freecam/ (only .rs and .toml
files) with fixed dates, so the same source always gives the same bytes.
"""
import hashlib
import json
import tomllib
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAME = "26.3"


def main():
    compat = json.loads((ROOT / "compatibility.json").read_text())
    bundle = ROOT / "mixins" / "fair_freecam"
    mixin = tomllib.loads((bundle / "horizon-mixin.toml").read_text())
    mod = mixin["mod"]
    if mixin.get("compatibility", {}).get("horizon_revision") != compat["horizon_revision"]:
        raise SystemExit("horizon-mixin.toml and compatibility.json pin different Horizon revisions")
    manifest = dict(schema=1, id=mod["id"], version=mod["version"], game=GAME,
                    horizon=compat["horizon_revision"], mixins=compat["horizon_mixins_revision"])
    files = {"horizon-native.json": (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode()}
    for path in sorted(bundle.iterdir()):
        if path.suffix in (".rs", ".toml"):
            files[f"mixins/{mod['id']}/{path.name}"] = path.read_bytes()
    out = ROOT / "target" / f"{mod['id']}-{mod['version']}.hnmod"
    out.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, content in sorted(files.items()):
            info = zipfile.ZipInfo(name, (2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, content)
    print(json.dumps(dict(file=str(out), size=out.stat().st_size,
                          sha256=hashlib.sha256(out.read_bytes()).hexdigest()), indent=2))


if __name__ == "__main__":
    main()
