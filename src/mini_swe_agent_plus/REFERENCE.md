# Environment reference

### Quickstart
Run an evaluation with default settings:

```bash
prime eval run mini-swe-agent-plus
```

To run SWE-Bench-Verified

```bash
prime eval run mini-swe-agent-plus -n -1 -r 1 -a '{"dataset_name": "SWE-bench/SWE-bench_Verified", "allow_git": true}'
```

To run a quicker version of SWE-Bench-Verified (downsampled to 468 examples which should finish in <30min)

```bash
prime eval run mini-swe-agent-plus -n -1 -r 1 -a '{"dataset_name": "PrimeIntellect/SWE-Bench-Verified-Quick", "allow_git": true}'
```

Notes:
- Use `-a` / `--env-args` to pass environment-specific configuration as a JSON object.



### Environment Arguments

| Arg | Type | Default | Description |
| --- | ---- | ------- | ----------- |
| `dataset_name` | str | `"R2E-Gym/R2E-Gym-Subset"` | Selects dataset |
| `max_turns` | int | `200` | Limits max number of agent turns |
| `total_timeout_minutes` | int | `360` | Timeout of a sandbox in minutes |
| `test_timeout` | int | `900` | Timeout for running tests in seconds |
| `cpu_cores` | int | `4` | Number of CPU cores for the sandbox |
| `memory_gb` | int | `4` | Amount of memory (GB) for the sandbox |
| `disk_size_gb` | int | `2` | Disk size (GB) for the sandbox |
| `labels` | list[str] | `["mini-swe-agent-plus"]` | Labels for the sandbox |
| `sandbox_client_max_workers` | int | `64` | Max workers for sandbox client |
| `rollout_timeout_seconds` | float | `5400.0` | Wall-clock timeout for rollout (90 min) |
| `max_command_timeouts` | int | `5` | Abort rollout after this many command timeouts |
| `allow_git` | bool | `false` | Allow git commands in execute_bash tool |
| `filter_repos` | list[str] | `None` | Exclude these repos from dataset, e.g. `scikit-learn/scikit-learn` |
| `skip_swebench_install` | bool | `true` | Skip SWE-bench eval install step for pure-Python changes |
| `in_loop_judge` | bool | `false` | LLM judge on each submission command when true (requires judge API) |
| `max_judge_submissions` | int | `8` | Max incorrect submissions before the rollout is forced to end |
| `judge_model` | str | `openai/gpt-4.1-mini` | Judge model id (Prime Inference–style) |
| `judge_api_key_var` | str | `PRIME_API_KEY` | Env var for judge API key |
| `judge_base_url` | str | `null` | OpenAI-compatible base URL (default Prime Inference) |
| `judge_sampling_args` | dict | `null` | Optional sampling args for the judge chat call |
| `judge_feedback_mode` | str | `total_score` | When `in_loop_judge` is true: `total_score` (four 0/1 criteria + `TOTAL: x/4`) or `single_criterion` (one `VIOLATED:` line + one sentence). Criteria: `PROBLEM_FIT`, `PATCH_QUALITY`, `SCOPE`, `VERIFICATION`. |


## Datasets and task details

Supported harnesses and datasets:
- all R2E-Gym datasets, incl.
  - [R2E-Gym-Subset](https://huggingface.co/datasets/R2E-Gym/R2E-Gym-Subset)
  - [SWE-Bench-Lite](https://huggingface.co/datasets/R2E-Gym/SWE-Bench-Lite)
  - [SWE-Bench-Verified](https://huggingface.co/datasets/R2E-Gym/SWE-Bench-Verified)
- all SWE-Bench datasets, e.g.
  - [SWE-bench Verified](https://huggingface.co/datasets/SWE-bench/SWE-bench_Verified)

### Datasets
- **Primary dataset(s)**: R2E-Gym/R2E-Gym-Subset, SWE-bench/SWE-bench_Verified
- **Source links**: https://huggingface.co/datasets/R2E-Gym/R2E-Gym-Subset

### Task
- **Type**: multi-turn, tool use
- **Rubric overview**: Reward based on executing repo test-suite
