@echo off
cd /d "%~dp0\.."
python -m src.main configs\package_a.toml
python -m src.main configs\package_b.toml
python -m src.main configs\package_c.toml
