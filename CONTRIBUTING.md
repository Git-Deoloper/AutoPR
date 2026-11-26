# Contributing to AutoPR / LocalClaw

```bash
git clone https://github.com/Git-Deoloper/AutoPR.git
cd AutoPR
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
python -m pytest -q
python -m build
```

Python 3.10 or later is required. Tests mock the model service and do not download weights. For a live check, follow the [quick start](README.md#quick-start) and describe your Ollama/model versions in the PR.

Keep fixes focused, explain the observed problem, and add a regression test for behavior that could break. Include the command and actual result of validation. Never paste API keys, private source code, or customer data into issues.

Use the existing `localclaw` package/command name for compatibility. See [ARCHITECTURE.md](ARCHITECTURE.md) before changing a module boundary and [API.md](API.md) before changing routes.

Questions and reproducible bug reports belong in [GitHub issues](https://github.com/Git-Deoloper/AutoPR/issues). Contributions use the repository's MIT license.
