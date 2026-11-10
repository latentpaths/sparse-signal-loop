# longbenchpro

Installed with the root Sparse Signal Loop distribution. Run `uv sync --locked`
from the repository root before running these commands.

### Judge feedback modes

`judge_feedback_mode` controls how the judge formats feedback after `NO`:

- `total_score` (default): four 0/1 criterion lines plus `TOTAL: x/4`.
- `single_criterion`: one `VIOLATED:` line plus one sentence.

For in-loop judging (judge feedback between turns), set `in_loop_judge: true` and tune `max_turns` for enough room to revise after feedback.

### Dataset

- [caskcsg/LongBench-Pro](https://huggingface.co/datasets/caskcsg/LongBench-Pro)

Default language filter is **English** (~750 samples). Use `language: "Chinese"` or `"all"` to change.

Rollout `info` includes `dataset_example_id` (the HuggingFace row `id`) for logging.


### Quickstart

Evaluations require configured inference access and consume provider credits;
SWE/RLM environments may also create paid sandboxes.

```bash
uv sync --locked

# Single rollout (in-loop judge on by default)
uv run vf-eval longbenchpro -m gpt-5-mini -n 1 -r1 -d -v

# Single-turn (judge only at end)
uv run vf-eval longbenchpro -m gpt-5-mini -n 5 -a '{"in_loop_judge": false}'

# User message as JSON {"query","context"} instead of markdown long-context section
uv run vf-eval longbenchpro -m gpt-5-mini -n 3 -a '{"prompt_in_context_file": true}'
```

### Metrics

Primary reward is `judge_reward` (weight 1.0); `task_metric_reward` and `contains_answer_reward` at weight 0 for analysis.

[Arguments and evaluation variants](REFERENCE.md) · [Changelog](CHANGELOG.md)
