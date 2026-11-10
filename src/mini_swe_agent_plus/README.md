# mini-swe-agent-plus

Installed with the root Sparse Signal Loop distribution. Run `uv sync --locked`
from the repository root before running these commands.

`mini-swe-agent-plus` environment for solving SWE issues inside prime sandboxes.

This environment adapts the [mini-swe-agent-plus](https://github.com/Kwai-Klear/mini-swe-agent-plus). Instead of parsing commands from code ticks this version implements tool use.

Supports [R2E-Gym](https://huggingface.co/datasets/R2E-Gym/R2E-Gym-Subset)
and [SWE-bench](https://huggingface.co/datasets/SWE-bench/SWE-bench_Verified) datasets.
Primary reward comes from the test harness. See the [reference](REFERENCE.md)
for dataset variants and task restrictions.

### Iterative LLM judge
Set `in_loop_judge` to **true** to enable an LLM judge when the agent issues the submission command (`echo MINI_SWE_AGENT_FINAL_OUTPUT`). The judge sees the latest assistant text plus a `git diff` from `/testbed` and the gold `patch` from the dataset when available. If the judge responds **NO**, feedback is appended to the tool output (look for `--- Judge`), `agent_signaled_done` is cleared so the agent can keep editing and **submit again**, up to `max_judge_submissions` incorrect attempts. Use a **generous `max_turns`** (e.g. 80–200): a low cap often prevents any submit before the rollout ends, so you never see judge feedback or recovery. A warning is logged if `in_loop_judge` is on and `max_turns` is under 50. **Primary reward remains the test harness** (`solved`, weight 1.0); `judge_reward` (weight 0.0) reflects last judged submission. Default `in_loop_judge` is **false** (no judge API).

### Quickstart

Evaluations require configured inference access and consume provider credits;
SWE/RLM environments may also create paid sandboxes.

```bash
prime eval run mini-swe-agent-plus
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
