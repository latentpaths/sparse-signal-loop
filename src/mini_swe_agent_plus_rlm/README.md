# mini-swe-agent-plus-rlm

Installed with the root Sparse Signal Loop distribution. Run `uv sync --locked`
from the repository root before running these commands.

`mini-swe-agent-plus-rlm` solves SWE-style tasks in prime sandboxes using a persistent code REPL and optional sub-LLM tool use.

Upstream workflow reference: [mini-swe-agent-plus](https://github.com/Kwai-Klear/mini-swe-agent-plus).

Supports [R2E-Gym](https://huggingface.co/datasets/R2E-Gym/R2E-Gym-Subset)
and [SWE-bench](https://huggingface.co/datasets/SWE-bench/SWE-bench_Verified) datasets.
Primary reward comes from the test harness. See the [reference](REFERENCE.md)
for dataset variants and task restrictions.

### Iterative LLM judge
Set `in_loop_judge` to **true** to run an LLM judge when the model submits from the REPL (`answer["ready"] = True` or bash `RLM_READY` when required by the harness). The judge sees the declared final answer plus `git diff` and the dataset gold `patch` when present. If the judge says **NO**, feedback is appended to the REPL tool result, `final_answer` is cleared, and the root model can continue until `max_judge_submissions` wrong attempts. **Primary reward remains** test-based `solved` (weight 1.0); `judge_reward` is weight 0.0 for diagnostics. Default is **false** (no judge API).

### Quickstart

Evaluations require configured inference access and consume provider credits;
SWE/RLM environments may also create paid sandboxes.

```bash
prime eval run mini-swe-agent-plus-rlm
```

### Metrics

| Metric | Meaning |
| ------ | ------- |
| `solved` | If SWE task instance was correctly solved |
| `command_timeout_count` | Number of commands that timed out during rollout |
| `rollout_duration_seconds` | Wall-clock duration of the rollout |
| `sandbox_oom` | Sandbox was killed due to out-of-memory |
| `sandbox_timeout` | Sandbox timed out |
| `sandbox_image_pull_error` | Failed to pull sandbox docker image |

[Arguments and evaluation variants](REFERENCE.md) · [Changelog](CHANGELOG.md)
