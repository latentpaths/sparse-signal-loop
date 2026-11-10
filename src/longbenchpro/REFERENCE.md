# Environment reference

### Environment arguments

| Arg | Type | Default | Description |
| --- | ---- | ------- | ----------- |
| `split` | str | `"test"` | Dataset split |
| `shuffle` | bool | `False` | Shuffle dataset |
| `seed` | int \| None | `None` | Shuffle seed |
| `thinking` | bool | `False` | Use `question_thinking` vs `question_nonthinking` |
| `include_env_tips` | bool | `False` | Append optional reading-strategy tips |
| `prompt_in_context_file` | bool | `False` | If true, user message is JSON `{"query","context"}`; if false, query + `## Long Context` section |
| `language` | str | `"English"` | `"English"`, `"Chinese"`, or `"all"` |
| `token_length` | str | `"all"` | Length bucket filter |
| `difficulty` | str | `"all"` | Difficulty filter |
| `primary_task` | str \| None | `None` | Primary task filter |
| `secondary_task` | str \| None | `None` | Secondary task filter |
| `dataset_start_index` | int | `0` | Skip first N rows after filters and transform |
| `judge_model` | str | `"gpt-4.1-mini"` | Judge model (OpenAI-compatible) |
| `judge_api_key_var` | str | `"PRIME_API_KEY"` | API key env var |
| `judge_base_url` | str \| None | `None` | Default: Prime Inference |
| `judge_sampling_args` | dict \| None | `None` | Judge sampling kwargs |
| `judge_feedback_mode` | str | `"total_score"` | `total_score` or `single_criterion` |
| `in_loop_judge` | bool | `True` | In-loop judge + chat feedback vs single-turn (rubric-only at end) |
| `max_turns` | int | `8` | Max assistant messages when `in_loop_judge` is true |
