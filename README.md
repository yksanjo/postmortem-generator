# postmortem-generator

Generate structured incident post-mortem documents from a few fields of incident
data. It produces a complete Markdown post-mortem (executive summary, timeline,
impact assessment, root-cause analysis, resolution, and action items) using
fixed templates — there is **no LLM or AI involved**; output is deterministic
string formatting. Use it as a CLI or via a small Flask web form.

## Stack

- Python 3.9+
- [Flask](https://flask.palletsprojects.com/) (web UI)
- python-dateutil
- pytest (tests)

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

### CLI

```bash
python3 generate_postmortem.py \
  --incident "API Outage" \
  --date 2024-01-15 \
  --duration "2 hours" \
  --impact "Checkout unavailable for ~30% of users" \
  --root-cause "Connection pool exhaustion under load" \
  --output postmortem.md
```

`--timeline` and `--resolution` accept either inline text or a file path. If
omitted, sensible placeholder sections are generated. Without `--output` the
document is printed to stdout. `--interactive`/`-i` prompts for fields.

### Web UI

```bash
python3 app.py
# serves a form at http://localhost:5001
```

The `/` route serves the form; `POST /generate` returns the rendered Markdown.

## Project structure

```text
.
|-- generate_postmortem.py   # core generator + CLI entrypoint
|-- app.py                   # Flask web UI (wraps the generator)
|-- tests/                   # pytest suite
|-- requirements.txt
```

## Tests

```bash
pip install -r requirements.txt pytest
pytest
```

## License

MIT — see `LICENSE`.
