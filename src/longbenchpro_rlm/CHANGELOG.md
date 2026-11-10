# Changelog

- 0.1.5: Removed `lbp_id` loader arg; rollout `info` uses `dataset_example_id`.
- 0.1.4: `dataset_start_index`.
- 0.1.3: `lbp_id` filter.
- 0.1.2: Dedicated `longbenchpro_rlm_prompts.py` in this package.
- 0.1.1: `judge_feedback_mode` for dense vs sparse judge feedback.
- 0.1.0: Initial release (excludes T4.x summarization tasks).
- Judge client uses verifiers `resolve_client` / `ClientConfig` (`openai_chat_completions`). Submit-gated in-loop judge uses `JudgeRubric.judge` in `LongBenchProRLMEnv`.
