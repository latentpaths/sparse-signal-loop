<p>
  <a href="https://www.latentpaths.com/"><img src="https://raw.githubusercontent.com/latentpaths/.github/main/assets/latent-paths-wordmark.png" alt="Latent Paths" width="280"></a>
</p>

# Sparse Signal Loop

Does feedback about one violated criterion help an LLM revise its answer, and
how does that depend on conversation history, working memory, and carried skills?
This harness compares chat agents with recursive language model (RLM) agents
using a Python workspace on LongBench-Pro and Mini SWE Agent Plus. The recorded comparisons do not establish a consistent
advantage for the RLM harness under single-criterion feedback.

[Experiments and findings](docs/BLOG.md) · [Recorded runs](outputs/) · [Remote compute](#run-on-remote-compute)

[Run evaluations](#run-evaluations) · [Regenerate reports](#results-and-reports) · [Develop](#development)

## Preview a run

With Python 3.11 or later and [uv](https://docs.astral.sh/uv/):

```sh
git clone https://github.com/latentpaths/sparse-signal-loop.git
cd sparse-signal-loop
uv sync --locked
./scripts/smoke.sh --dry-run
```

The preview prints the three LongBench-Pro phase configurations without inference
calls. It writes local logs under `outputs/smoke_logs/`. One root installation
includes all four environments and the experiment CLIs; separate environment
installs are no longer needed. The environment names and arguments are unchanged.

[LongBench-Pro](src/longbenchpro/README.md) ·
[RLM LongBench-Pro](src/longbenchpro_rlm/README.md) ·
[Mini-SWE](src/mini_swe_agent_plus/README.md) ·
[RLM Mini-SWE](src/mini_swe_agent_plus_rlm/README.md)

## What changes between conditions

| Phase | Comparison |
| --- | --- |
| 0 | Total-score versus single-criterion feedback, each with chat and RLM harnesses |
| 1 | Conversation memory versus files in the Python workspace |
| 2 | Carried `SKILL.md` files and chat reinjection controls |

Judge acceptance, environment reward, and task scores are separate measurements.
The [research account](docs/BLOG.md) defines them, links the underlying reports,
and reports recorded rollout counts, errors, and incomplete conditions.
Turn budgets and model settings differ across some conditions and phases.

## Run evaluations

Run commands from the repository root. Retained `outputs/` files are research
evidence; new local output is ignored. Use a separate run directory for fresh
work and regenerate reports on copies when inspecting historical measurements.

Real runs consume inference and sandbox credits. Set `PRIME_API_KEY` in your
shell or local `.env` file before a real run:

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


## Run on remote compute

These helpers create paid Prime compute resources. Configure the CLI and inspect
the chosen SKU before creating a pod.

Upload an SSH public key and configure its local private-key path:

```sh
./scripts/prime_ssh_key_upload.sh ~/.ssh/id_ed25519.pub
prime config set-ssh-key-path ~/.ssh/id_ed25519
```

Create and connect to a pod:

```sh
./scripts/prime_pod.sh create
prime pods list
prime pods ssh <pod-id>
```

On the pod, bootstrap the repository and dependencies:

```sh
export SPARSE_SIGNAL_LOOP_REPO="https://github.com/latentpaths/sparse-signal-loop.git"
./scripts/prime_pod.sh bootstrap
cd ~/sparse-signal-loop
./scripts/smoke.sh --dry-run
```

Run `./scripts/smoke.sh` only when ready to make real evaluation requests.
Terminate the pod when finished:

```sh
prime pods terminate <pod-id>
```

Optional helper settings include `PRIME_POD_SKU`, `PRIME_API_BASE_URL`,
`SSH_KEY_NAME`, and `SPARSE_SIGNAL_LOOP_REPO`. Run the individual scripts with
`--help` for their supported flags.


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
