"""Offline compatibility checks for the consolidated environment distribution."""

import hashlib
import importlib
import json
import subprocess
import sys
import tempfile
import unittest
from importlib.resources import files
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import verifiers as vf
from datasets import Dataset

from sparse_signal_loop import lbp_metrics, swebench_utils
from sparse_signal_loop.execution_log_parser import decolor_dict_keys, parse_log_pytest
from sparse_signal_loop.lbp_data import build_lbp_dataset
from sparse_signal_loop.swe_judge import judge_reference_from_row, msap_judge_verdict


class SharedEnvironmentTests(unittest.TestCase):
    def test_prompt_bytes_and_errors_match_original_harnesses(self):
        fixtures = json.loads((Path(__file__).parent / "fixtures/prompt_hashes.json").read_text())
        modules = {
            "lbp_chat": "sparse_signal_loop.lbp_prompts",
            "lbp_rlm": "sparse_signal_loop.lbp_prompts",
            "swe_chat": "sparse_signal_loop.swe_memory",
            "swe_rlm": "sparse_signal_loop.swe_memory",
        }
        for harness, records in fixtures.items():
            module = importlib.import_module(modules[harness])
            for record in records:
                with self.subTest(harness=harness, function=record["function"], kwargs=record["kwargs"]):
                    try:
                        kwargs = dict(record["kwargs"])
                        if harness == "swe_rlm" and record["function"] in {
                            "build_phase2_skill_md_template",
                            "phase2_skill_suffix",
                        }:
                            kwargs["repl_workspace"] = True
                        value = {"value": getattr(module, record["function"])(**kwargs)}
                    except ValueError as error:
                        value = {"error": str(error)}
                    digest = hashlib.sha256(json.dumps(value, ensure_ascii=False).encode()).hexdigest()
                    self.assertEqual(digest, record["sha256"])

    def test_metrics_keep_normalization_and_ranking_semantics(self):
        self.assertEqual(lbp_metrics.accuracy([" A  B "], "reason\n[答案] a b"), 1)
        self.assertEqual(lbp_metrics.accuracy([], ""), 0)
        self.assertAlmostEqual(lbp_metrics.f1_score(["a", "b"], "[Answer] a\nc"), 0.5)
        self.assertEqual(lbp_metrics.sub_em(["a", "b"], "a"), 0.5)
        self.assertEqual(lbp_metrics.pairwise_accuracy(["a", "b", "c"], "a\nc\nb"), 2 / 3)
        self.assertEqual(lbp_metrics.ndcg(["a", "b"], "a\nb"), 1)
        self.assertEqual(lbp_metrics.ndcg([], "a"), 0)

    def test_dataset_filters_mapping_offset_and_shuffle(self):
        rows = [
            dict(
                id=i,
                secondary_task=task,
                primary_task="retrieval",
                language=lang,
                token_length="32k",
                difficulty="easy",
            )
            for i, task, lang in [
                (0, "T4.1", "en"),
                (1, "T1.1", "en"),
                (2, "T1.1", "zh"),
                (3, "T1.1", "en"),
                (4, "T1.1", "en"),
            ]
        ]

        def load_fixture(name, *, split):
            self.assertEqual((name, split), ("caskcsg/LongBench-Pro", "test"))
            return Dataset.from_list(rows)

        options = dict(
            load_dataset=load_fixture,
            transform_example=lambda row, index: dict(id=row["id"], filtered_index=index),
            split="test",
            language="en",
            effective_token_length="32k",
            difficulty="easy",
            primary_task="retrieval",
            effective_secondary_task="T1.1",
            dataset_start_index=1,
            shuffle=False,
            seed=17,
        )
        result = build_lbp_dataset(**options)
        self.assertEqual(list(result["id"]), [3, 4])
        self.assertEqual(list(result["filtered_index"]), [1, 2])
        self.assertEqual(
            list(build_lbp_dataset(**{**options, "shuffle": True})["id"]),
            list(result.shuffle(seed=17)["id"]),
        )
        with self.assertRaisesRegex(ValueError, "out of range"):
            build_lbp_dataset(**{**options, "dataset_start_index": 3})

    def test_test_log_parsing_and_patch_failure(self):
        log = "short test summary info\nPASSED test_a.py::test_ok\nFAILED test_a.py::test_bad - nope"
        self.assertEqual(parse_log_pytest(log), {"test_ok": "PASSED", "test_bad": "FAILED"})
        self.assertEqual(parse_log_pytest(None), {})
        self.assertEqual(decolor_dict_keys({"\x1b[31mtest\x1b[0m": "FAILED"}), {"test": "FAILED"})
        spec = SimpleNamespace(repo="fixture", version="1")
        with (
            patch.dict(swebench_utils.MAP_REPO_VERSION_TO_SPECS, {"fixture": {"1": {"test_cmd": "pytest"}}}),
            patch.dict(swebench_utils.MAP_REPO_TO_PARSER, {"fixture": lambda content, _spec: {"tail": content}}),
        ):
            self.assertEqual(swebench_utils.get_logs_eval(spec, "pytest\npassed"), ({"tail": "\npassed"}, True))
            self.assertEqual(swebench_utils.get_logs_eval(spec, swebench_utils.APPLY_PATCH_FAIL), ({}, False))

    def test_swe_judge_reference_and_verdict(self):
        reference = judge_reference_from_row({"problem_statement": " issue ", "patch": "x" * 12_001})
        self.assertIn("x" * 12_000 + "\n... (truncated)", reference)
        self.assertTrue(reference.endswith("Problem statement:\nissue"))
        self.assertTrue(judge_reference_from_row({"problem_statement": " issue "}).endswith("\nissue"))
        self.assertEqual(msap_judge_verdict("YES\naccepted"), (True, "accepted"))
        self.assertEqual(msap_judge_verdict("NO\ntry again"), (False, "try again"))
        self.assertEqual(msap_judge_verdict(""), (False, ""))
        accepted, feedback = msap_judge_verdict("unclear")
        self.assertFalse(accepted)
        self.assertIn("keep iterating", feedback)

    def test_environment_entrypoints_and_packaged_sandbox_tools(self):
        for name in ["longbenchpro", "longbenchpro_rlm", "mini_swe_agent_plus", "mini_swe_agent_plus_rlm"]:
            self.assertTrue(callable(importlib.import_module(name).load_environment))
        resources = files("sparse_signal_loop.tools")
        for tool in ["execute_bash.py", "str_replace.py"]:
            result = subprocess.run([sys.executable, str(resources / tool), "--help"], capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "example.txt"
            target.write_text("before\n")
            result = subprocess.run(
                [sys.executable, str(resources / "str_replace.py"), str(target), "before", "after"],
                capture_output=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(target.read_text(), "after\n")

    def test_verifiers_resolves_existing_environment_ids(self):
        for env_id in ["longbenchpro", "longbenchpro-rlm", "mini-swe-agent-plus", "mini-swe-agent-plus-rlm"]:
            module = importlib.import_module(env_id.replace("-", "_"))
            instance = SimpleNamespace(env_id=None, env_args=None)
            with patch.object(module, "load_environment", return_value=instance) as factory:
                self.assertIs(vf.load_environment(env_id, max_turns=9), instance)
                factory.assert_called_once_with(max_turns=9)
            self.assertEqual(instance.env_id, env_id)
            self.assertEqual(instance.env_args, {"max_turns": 9})


if __name__ == "__main__":
    unittest.main()
