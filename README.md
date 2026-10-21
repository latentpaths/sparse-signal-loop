# Sparse Signal Loop

Does feedback about one violated criterion help an LLM revise its answer, and
how does that depend on conversation history, working memory, and carried skills?
This harness compares chat agents with recursive language model (RLM) agents
using a Python workspace on LongBench-Pro and Mini SWE Agent Plus. The recorded comparisons do not establish a consistent
advantage for the RLM harness under single-criterion feedback.

- Source: [latentpaths/sparse-signal-loop](https://github.com/latentpaths/sparse-signal-loop)
- Start: [Preview a run](#preview-a-run)
- Check: [Run evaluations](#run-evaluations)

[Experiments and findings](docs/BLOG.md) · [Recorded runs](outputs/) · [Remote setup](docs/remote-runs.md)

## Preview a run

With Python 3.11 or later and [uv](https://docs.astral.sh/uv/):

```sh
git clone https://github.com/latentpaths/sparse-signal-loop.git
cd sparse-signal-loop
uv sync --locked
./scripts/smoke.sh --dry-run
```

The preview prints the three LongBench-Pro phase configurations without inference
calls. It writes local logs under `outputs/smoke_logs/`. The four environment
packages in `src/envs/` are installed as local editable dependencies.

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

Real runs require `PRIME_API_KEY` in the shell or a local `.env` file and consume
inference and sandbox credits:

```sh
./scripts/phase0/lbp.sh -n 4 -r 1
```

Add `--dry-run` to preview settings. See [running and reporting](docs/running.md)
for phase commands, configuration, report regeneration, and development checks.
Retained evidence is tracked under `outputs/`; new local output is ignored.
