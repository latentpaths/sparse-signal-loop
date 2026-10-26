# Running and reporting

Run commands from the repository root. Retained `outputs/` files are research
evidence; use a separate run directory for fresh work and regenerate reports on
copies when inspecting historical measurements.

## Run evaluations

Set `PRIME_API_KEY` in your shell or local `.env` file before a real run:

```sh
export PRIME_API_KEY="<your-prime-api-key>"
./scripts/smoke.sh
```

Keep credentials out of version control. Run one phase or benchmark explicitly:

```sh
./scripts/phase0/lbp.sh -n 4 -r 1
./scripts/phase1/lbp.sh --smoke
./scripts/phase2/mini_swe.sh --smoke
```

Use `--dry-run` to preview those commands. `./scripts/big_run.sh` launches the
full phase/benchmark matrix; inspect its configuration before starting a run.

## Results and reports

Run directories include `summary.json` and `REPORT.md`. Regenerate reports from
recorded outputs without starting a new evaluation:

```sh
ssl_report_copy=$(mktemp -d)
cp -R outputs/experiments "$ssl_report_copy/experiments"
uv run --locked ssl-experiment-report --root "$ssl_report_copy/experiments"
```

For one run, pass `--run-dir` instead of `--root`.
The retained [outputs](../outputs/) and [research writeup](BLOG.md) provide the
context for interpreting measurements; a successful smoke run is not evidence
of a benchmark improvement.

## Configuration

Common run settings include `POLICY_MODEL`, `JUDGE_MODEL`,
`DATASET_START_INDEX`, `NUM_EXAMPLES`, and `ROLLOUTS`. `ENV_FILE` selects an
explicit dotenv file. Mini-SWE also uses `MSWE_DATASET` and `ALLOW_GIT`.

The installed CLIs mirror the phase/benchmark pairs: `ssl-phase0-lbp`,
`ssl-phase0-msap`, `ssl-phase1-lbp`, `ssl-phase1-msap`, `ssl-phase2-lbp`, and
`ssl-phase2-msap`. Each accepts `--help`; for example:

```sh
uv run ssl-phase0-lbp --help
```


## Development

```sh
uv sync --locked --group dev
uv run --locked python -m unittest discover -s tests -v
uv run --locked ruff check src tests
uv run --locked ruff format --check src tests
uv build --wheel
```

The root wheel includes all four `load_environment` entry points and the shared
sandbox scripts. The offline tests compare prompts with pre-consolidation hashes
and exercise metrics, dataset selection, log parsing and packaged resources.
