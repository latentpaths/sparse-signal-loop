# longbenchpro-rlm

Installed with the root Sparse Signal Loop distribution. Run `uv sync --locked`
from the repository root before running these commands.

### How it works

This environment runs [LongBench-Pro](https://github.com/caskcsg/longcontext/tree/main/LongBench-Pro) with an interactive REPL so the model can execute code against the context and submit a final answer.

LongBench-Pro contains 1,500 examples spanning 11 primary task categories and 25 secondary tasks, with context lengths from 8k to 256k tokens.

**Note:** Summarization tasks (T4.x) are excluded because their metrics require model-based embeddings that are impractical in this evaluation setting.

### Dataset

- [caskcsg/LongBench-Pro](https://huggingface.co/datasets/caskcsg/LongBench-Pro) — 1,500 bilingual long-context evaluation tasks

By default, **English-only** examples (~750 samples). Set `language: "Chinese"` or `"all"` to change.

Judge prompt templates live in `../sparse_signal_loop/lbp_prompts.py`.


### Quickstart

Evaluations require configured inference access and consume provider credits;
SWE/RLM environments may also create paid sandboxes.

```bash
# Basic evaluation (English samples, default)
uv run vf-eval longbenchpro-rlm -m gpt-5-mini -n 5

# All languages (English + Chinese)
uv run vf-eval longbenchpro-rlm -m gpt-5-mini -n 5 \
  -a '{"language": "all"}'

# With thinking prompts
uv run vf-eval longbenchpro-rlm -m gpt-5-mini -n 5 -a '{"thinking": true}'

# Filter by token length
uv run vf-eval longbenchpro-rlm -m gpt-5-mini -n 5 -a '{"token_length": "32k"}'

# Filter by difficulty
uv run vf-eval longbenchpro-rlm -m gpt-5-mini -n 5 -a '{"difficulty": "Hard"}'

# Filter by secondary task
uv run vf-eval longbenchpro-rlm -m gpt-5-mini -n 5 -a '{"secondary_task": "T3.2 Single-Hop Fact QA"}'
```

### Metrics

| Metric | Meaning |
| ------ | ------- |
| `judge_reward` | 1.0 if judge determines answer is correct (main reward, weight=1.0) |
| `task_metric_reward` | Task-specific metric from LongBench-Pro (Accuracy/F1/SubEM/NDCG/Pairwise Accuracy) (weight=0.0) |
| `contains_answer_reward` | 1.0 if answer contains any ground truth value (weight=0.0) |

[Arguments and evaluation variants](REFERENCE.md) · [Changelog](CHANGELOG.md)
