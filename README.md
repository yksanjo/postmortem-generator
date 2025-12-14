# Incident Post-Mortem Template Generator

Automatically generates structured post-mortem documents from key incident information.

## Features

- Interactive CLI and web form interfaces
- Asks 5 key questions to capture incident details
- Generates Markdown/Confluence-ready documents
- Includes timelines, RCA prompts, and prevention checklists
- Standardizes post-mortem format across teams

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### CLI Mode (Interactive)

```bash
python generate_postmortem.py
```

### CLI Mode (Non-Interactive)

```bash
python generate_postmortem.py \
  --incident "API Outage" \
  --date "2024-01-15" \
  --duration "2 hours" \
  --impact "All users unable to access API" \
  --root-cause "Database connection pool exhaustion" \
  --output postmortem.md
```

### Web Interface

```bash
python app.py
```

Then open http://localhost:5001 in your browser.

### Python API

```python
from generate_postmortem import generate_postmortem

postmortem = generate_postmortem(
    incident_name="API Outage",
    incident_date="2024-01-15",
    duration="2 hours",
    impact="All users unable to access API",
    root_cause="Database connection pool exhaustion"
)

print(postmortem)
```

## Output Format

Generates a structured Markdown document with:
- Executive Summary
- Timeline
- Impact Assessment
- Root Cause Analysis
- Resolution Steps
- Prevention Checklist
- Action Items

## License

MIT
