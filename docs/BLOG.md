# Feedback, memory, and carried skills

Does feedback naming one violated criterion improve answer revision, and does a
Python workspace change that effect? The retained comparisons give different
answers across benchmarks and conditions. They do not establish a general
single-criterion advantage or identify a cause for the differences.

## What the harness changes

The chat agent revises answers through a conversation containing judge feedback.
The recursive language model (RLM) agent works through a Python REPL; the LongBench-Pro environment places
context in workspace files and supports sub-model calls. These are interfaces
and information-access choices, not evidence that the agent learned a different
reasoning strategy. Model weights stay fixed.

Phase 0 crosses harness type with total-score or single-criterion feedback.
Phase 1 adds conversation memory and REPL-file memory conditions. Phase 2 adds
carried `SKILL.md` content and chat controls with or without system reinjection.
The environment READMEs define the [LongBench-Pro](../src/longbenchpro/README.md),
[RLM LongBench-Pro](../src/longbenchpro_rlm/README.md),
[Mini-SWE](../src/mini_swe_agent_plus/README.md), and
[RLM Mini-SWE](../src/mini_swe_agent_plus_rlm/README.md) implementations.

## Reading the measurements

The tables below use the retained batch
[`20260407T090610Z`](../outputs/serious_runs/20260407T090610Z/runs/).
Its policy is `z-ai/glm-4.7` and its judge is `z-ai/glm-4.7-flash`.
Configurations request 15 examples with two rollouts per example. Most cells
retain 30 rollouts; LongBench-Pro Phases 1 and 2 retain only 10 per cell.
Denominators below count recorded rollouts, not independent tasks or requested
runs. Results are descriptive; no uncertainty intervals are supplied here.

**Judge acceptance** is the fraction of retained rollouts accepted by the judge.
Environment reward and the LongBench-Pro task score are separate fields and may
disagree with acceptance. `Success@K` additionally requires acceptance within K
rounds; chat rounds count assistant generations, while RLM rounds count root
REPL calls. These round counts are not equal units of inference work.

LongBench-Pro uses turn caps of 32 for chat and 64 for RLM in this batch.
Mini-SWE uses a 128-turn cap. Phase 1/2 dataset slicing also differs from Phase 0.
Comparisons across phases therefore do not isolate memory or skills alone.

## Phase 0: feedback format

[LongBench-Pro: full report](../outputs/serious_runs/20260407T090610Z/runs/phase0/lbp/REPORT.md)

| Condition | Judge-accepted / recorded rollouts |
| --- | ---: |
| Chat · single criterion | 26/30 |
| Chat · total score | 29/30 |
| RLM · single criterion | 21/30 |
| RLM · total score | 20/30 |

[Mini-SWE: full report](../outputs/serious_runs/20260407T090610Z/runs/phase0/mini_swe/REPORT.md)

| Condition | Judge-accepted / recorded rollouts |
| --- | ---: |
| Chat · single criterion | 19/30 |
| Chat · total score | 10/30 |
| RLM · single criterion | 22/30 |
| RLM · total score | 26/30 |

On LongBench-Pro, chat acceptance decreases from 29/30 to 26/30 with
single-criterion feedback; RLM changes from 20/30 to 21/30. On Mini-SWE, chat
changes from 10/30 to 19/30 while RLM changes from 26/30 to 22/30. The effect of
feedback format changes with the benchmark and harness. Mini-SWE chat with
single-criterion feedback also records a mean error flag of 0.067; these errors
remain in the retained denominator.

## Phase 1: memory location

[LongBench-Pro: full report](../outputs/serious_runs/20260407T090610Z/runs/phase1/lbp/REPORT.md)

| Condition | Judge-accepted / recorded rollouts |
| --- | ---: |
| Chat · single criterion · conversation memory | 3/10 |
| Chat · total score · conversation memory | 4/10 |
| RLM · single criterion · conversation memory | 1/10 |
| RLM · single criterion · REPL-file memory | 1/10 |
| RLM · total score · conversation memory | 2/10 |
| RLM · total score · REPL-file memory | 2/10 |

[Mini-SWE: full report](../outputs/serious_runs/20260407T090610Z/runs/phase1/mini_swe/REPORT.md)

| Condition | Judge-accepted / recorded rollouts |
| --- | ---: |
| Chat · single criterion · conversation memory | 23/30 |
| Chat · total score · conversation memory | 24/30 |
| RLM · single criterion · conversation memory | 26/30 |
| RLM · single criterion · REPL-file memory | 25/30 |
| RLM · total score · conversation memory | 27/30 |
| RLM · total score · REPL-file memory | 27/30 |

The two RLM memory conditions have identical recorded acceptance on LongBench-Pro
for each feedback format. Mini-SWE single-criterion acceptance is 26/30 with
conversation memory and 25/30 with REPL-file memory. These counts do not support
a claim that memory location explains the earlier harness differences. Mini-SWE
RLM total-score/file memory records a mean error flag of 0.033.

## Phase 2: carried skills and reinjection

[LongBench-Pro: full report](../outputs/serious_runs/20260407T090610Z/runs/phase2/lbp/REPORT.md)

| Condition | Judge-accepted / recorded rollouts |
| --- | ---: |
| Chat · single criterion · no file | 3/10 |
| Chat · single criterion · system reinjection | 6/10 |
| Chat · total score · no file | 5/10 |
| Chat · total score · system reinjection | 4/10 |
| RLM · single criterion · skill file | 3/10 |
| RLM · total score · skill file | 2/10 |

[Mini-SWE: full report](../outputs/serious_runs/20260407T090610Z/runs/phase2/mini_swe/REPORT.md)

| Condition | Judge-accepted / recorded rollouts |
| --- | ---: |
| Chat · single criterion · no file | 21/30 |
| Chat · single criterion · system reinjection | 13/30 |
| Chat · total score · no file | 24/30 |
| Chat · total score · system reinjection | 23/30 |
| RLM · single criterion · skill file | 23/30 |
| RLM · total score · skill file | 29/30 |

On LongBench-Pro, single-criterion chat with reinjection records 6/10 acceptance,
compared with 3/10 without a file. On Mini-SWE, the corresponding comparison is
13/30 versus 21/30; the reinjection condition also records a mean error flag of
0.30. RLM skill-file acceptance on Mini-SWE is 29/30 with total-score feedback
and 23/30 with single-criterion feedback. These combined conditions do not isolate
the effect of a skill file from the harness, prompts, and execution settings.
LongBench-Pro chat total-score/no-file and single-criterion/reinjection record
mean error flags of 0.20 and 0.10, respectively.

## Evidence and limits

Each table links its full report and adjacent `summary.json`; underlying rollout
records are retained alongside them. Earlier five-rollout pilots are in
[`outputs/experiments/`](../outputs/experiments/), including GPT-4.1-mini and
GLM-4.7-flash runs. They are separate runs, not additional independent replications
of this batch, and are not pooled into these tables. Archived runs cited by an
earlier version of this writeup are absent from the public checkout and are not
used as evidence here.

Acceptance depends on the retained judge and execution protocol. Repeated
rollouts share examples, model stacks differ between batches, some runs are
incomplete, and errors are nonzero in several conditions. Token totals, partial
reward, or different tool interfaces alone cannot establish why an agent passed
or failed. These experiments do not test weight updates, continual learning, or a
general ceiling on external memory.

A follow-up that estimates a feedback effect would need a fixed task set, model
and judge, complete paired conditions, declared treatment of errors, uncertainty
that accounts for repeated examples, and an explicit comparison of inference
budgets. That is a proposed evaluation, not a result of these records.

See [running and reporting](../README.md#results-and-reports) to inspect configurations and regenerate
reports on copies without starting new inference runs.
