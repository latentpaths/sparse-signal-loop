# Changelog

- 0.1.6: add `custom_instructions` parameter; replace `tool_target` enum with three independent booleans (`tools_on_root`, `tools_in_repl`, `tools_on_sub`); remove redundant tool instructions from prompt (handled by harness scaffolding)
- 0.1.5: simplify timeouts to 3 primary knobs (`sandbox_timeout_minutes`, `code_execution_timeout`, `test_timeout`); remove redundant `sandbox_command_timeout`, `rollout_timeout_seconds`, `total_timeout_minutes` (now derived); rename `max_command_timeouts` → `max_execution_timeouts`; add `max_startup_wait_seconds` power-user override. **Default changes**: sandbox lifetime 360 → 600 min, per-command timeout 90 → 120s (now unified with `code_execution_timeout`), derived rollout timeout 5400 → 34800s
- 0.1.4: add `use_dataset_cache` to opt into HuggingFace disk caching instead of in-memory datasets
- 0.1.3: align arg names with simplified recursive harness (`max_iterations` → `max_turns`, remove `execution_backend`, `sandbox_start_command`, `sandbox_client_max_workers`); `code_execution_timeout` now defaults to `120` instead of falling back to `sandbox_command_timeout`
- 0.1.2: sandbox labels no longer force in the default label
- 0.1.1: add `rlm_metric_weights` parameter with within-group min-max normalized harness metrics as training reward signals
- 0.1.0: initial release with recursive REPL harness
