#!/bin/sh
cd "$(dirname "$0")/.." || exit 1
python3 -m src.main configs/package_a.toml
python3 -m src.main configs/package_b.toml
python3 -m src.main configs/package_c.toml
