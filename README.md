# Wind Rose

Personal life-balance tracker that visualizes monthly self-ratings as radar charts, bar comparisons, and heatmap summaries.

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip setuptools
pip install -U -r requirenments.txt
```

Or use the provided script:

```bash
bash pip_install.sh
```

## Configuration

All settings live in `config/chart_config.json`:

```json
{
    "diagram_name": "Diagram name",
    "measure": 10,
    "year": 2026,
    "data_path": "data/features.json",
    "output_dir": "images/features",
    "font_sizes": {
        "title": 16,
        "subtitle": 14,
        "axis_label": 12,
        "tick_label": 16,
        "stats_text": 16,
        "bar_value": 14
    }
}
```

| Field | Description |
|---|---|
| `diagram_name` | Title shown on the radar chart |
| `measure` | Maximum score on the rating scale |
| `year` | Data year displayed in chart titles |
| `data_path` | Path to the JSON file with monthly ratings |
| `output_dir` | Directory where chart images are saved |
| `font_sizes` | Font sizes for titles, labels, and values |

## Data format

The data file is a JSON object where each key is a month name and the value is a mapping of categories to integer scores:

```json
{
    "January": {
        "Feature_1": 5,
        "Feature_2": 6,
        "Feature_3": 8
    },
    "February": {
        "Feature_1": 5,
        "Feature_2": 3,
        "Feature_3": 8
    }
}
```

## Usage

```bash
python3 main.py
```

Charts are saved to the directory specified by `output_dir` in the config:

- `current_month.png` — radar chart for the latest month
- `month_comparison.png` — grouped bar chart comparing selected months
- `yearly_summary.png` — heatmap and mean-value trend line

## Development

Pre-commit hooks (ruff + mypy) are configured:

```bash
pre-commit install
pre-commit run --all-files
```
