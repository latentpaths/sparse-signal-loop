# Sparse Signal Loop

Experiments on feedback, working memory, and reusable skills for LLM agents.
The harness compares chat-style and RLM-style agents on LongBench-Pro and
Mini SWE Agent Plus while varying the information and persistent artifacts
available during a rollout.

## Experimental structure

| Phase | Comparison |
| --- | --- |
| 0 | Baseline harness and feedback conditions |
| 1 | Working-memory interventions |
| 2 | Carried `SKILL.md` artifacts and chat-reinjection baselines |

The runners retain configuration, measurements, and generated reports under
`outputs/`. Read the [research writeup](docs/BLOG.md) for the experiments and
their interpretation; this README describes how to operate the code.

## Installation

Use Python 3.11 or later and [uv](https://docs.astral.sh/uv/):

```sh
git clone https://github.com/latentpaths/sparse-signal-loop.git
cd sparse-signal-loop
uv sync --locked
```

The environment packages under `src/envs/` are installed as local editable
dependencies. Real runs require Prime API access and can incur inference and
sandbox charges.

## Preview a smoke run

```sh
./scripts/smoke.sh --dry-run
```

This previews the three LongBench-Pro phase runs without making inference calls.
It writes local logs under `outputs/smoke_logs/<timestamp>/`.

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
uv run ssl-experiment-report --root outputs/experiments
```

For one run, pass `--run-dir` instead of `--root`.
The retained [outputs](outputs/) and [research writeup](docs/BLOG.md) provide the
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

## Repository guide

| Location | Contents |
| --- | --- |
| [src/experiments/](src/experiments/) | Phase definitions, runners, and reporting |
| [LongBench-Pro](src/envs/longbenchpro/README.md) · [RLM variant](src/envs/longbenchpro_rlm/README.md) | LongBench-Pro environments |
| [Mini SWE Agent Plus](src/envs/mini_swe_agent_plus/README.md) · [RLM variant](src/envs/mini_swe_agent_plus_rlm/README.md) | Coding-agent environments |
| [scripts/](scripts/) | Smoke runs, phase wrappers, and Prime pod helpers |
| [docs/remote-runs.md](docs/remote-runs.md) | Optional remote-machine setup |

## Development

```sh
uv run ruff check .
uv run ruff format --check .
```
