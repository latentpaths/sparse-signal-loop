# Sparse Signal Loop

Does feedback about one violated criterion help an LLM revise its answer, and
how does that depend on conversation history, working memory, and carried skills?
This harness compares chat agents with recursive language model (RLM) agents
using a Python workspace on LongBench-Pro and Mini SWE Agent Plus. The recorded comparisons do not establish a consistent
advantage for the RLM harness under single-criterion feedback.

[Experiments and findings](docs/BLOG.md) · [Recorded runs](outputs/) · [Run guide](docs/running.md)

## Preview a run

With Python 3.11 or later and [uv](https://docs.astral.sh/uv/):

```sh
git clone https://github.com/latentpaths/sparse-signal-loop.git
cd sparse-signal-loop
uv sync --locked
./scripts/smoke.sh --dry-run
```

The preview prints the three LongBench-Pro phase configurations without inference
calls. It writes local logs under `outputs/smoke_logs/`. The root installation includes all four environments and experiment CLIs.

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

## Evaluate and inspect

Real evaluations consume inference and sandbox credits. Set `PRIME_API_KEY` in
your shell or local `.env`, then run `./scripts/smoke.sh`. Use `--dry-run` first.
Keep new runs separate from retained `outputs/` evidence.

See the [run guide](docs/running.md) for individual phases, configuration,
report regeneration, and remote compute. The [research account](docs/BLOG.md)
explains the recorded comparisons and incomplete conditions.

## Development

```sh
uv sync --locked --group dev
uv run --locked python -m unittest discover -s tests -v
uv run --locked ruff check src tests
uv run --locked ruff format --check src tests
uv build --wheel
```

## Citation

<!-- BEGIN generated citations -->

```bibtex
@misc{bodadearticlesparsesignalloop,
  author = {Bodade, Ayush},
  title = {{Sparse Signal Loop}},
  year = {2026},
  month = {04},
  day = {11},
  date = {2026-04-11},
  howpublished = {Latent Paths},
  url = {https://www.latentpaths.com/writings/sparse-signal-loop},
  note = {Blog post}
}
```

<!-- END generated citations -->
