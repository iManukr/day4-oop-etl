# Day 4 OOP ETL

A small Python project that demonstrates an object-oriented ETL (extract, transform, load) workflow. It reads order records from a CSV file and user records from a REST API, validates and cleans them, then writes valid and rejected records to files.

## Features

- Extract records from CSV files and REST APIs.
- Validate required fields, email addresses, and positive numeric values.
- Clean configured text fields and normalise email addresses.
- Save valid and rejected records as CSV or JSON.
- Print a summary of the records processed by each pipeline.

## Requirements

- Python 3.15 or newer (as specified in `pyproject.toml`).
- [uv](https://docs.astral.sh/uv/) for dependency and environment management.
- An internet connection to run the user API pipeline.

## Getting started

Clone or download the project, then open a terminal in its root directory. Sync the project dependencies with `uv`:

```bash
uv sync
```

Run the ETL pipelines:

```bash
uv run python main.py
```

The script runs both the orders CSV pipeline and the customer API pipeline, then prints a summary to the terminal. Run it from the project root because the input and output paths are relative to that directory.

## Pipelines

### Orders CSV

Reads `data/orders.csv`. Each order must include `order_id` and `email`; email addresses are checked and normalised, `amount` must be positive, and `city` text is cleaned.

### Customer API

Fetches users from `https://jsonplaceholder.typicode.com/users`. Each user must include `name` and `email`; email addresses are checked and normalised, and names are cleaned. The API request uses a 15-second timeout.

## Output

The loaders create the `output/` directory when needed and write:

| File | Contents |
| --- | --- |
| `output/orders_clean.csv` | Valid, cleaned orders |
| `output/orders_rejected.csv` | Rejected orders and their validation reasons |
| `output/users_clean.json` | Valid, cleaned API users |
| `output/users_rejected.json` | Rejected API users and their validation reasons |

If a pipeline has no records to write to a particular destination, that output file is not created or replaced for that load.

## Project structure

```text
.
├── data/
│   └── orders.csv
├── etl/
│   ├── errors.py
│   ├── extractors.py
│   ├── loader.py
│   └── transformer.py
├── main.py
├── output/
├── pyproject.toml
└── uv.lock
```

`main.py` configures and runs the pipelines. The `etl/` package contains the reusable extraction, transformation, loading, and error-handling classes.

## Dependencies

The project uses [`requests`](https://pypi.org/project/requests/) for the API request. Install it and the other project dependencies through `uv sync`.
