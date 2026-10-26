"""Dataset selection shared by chat and RLM; transformations remain harness-specific."""

import random


def build_lbp_dataset(
    *,
    load_dataset,
    transform_example,
    split,
    language,
    effective_token_length,
    difficulty,
    primary_task,
    effective_secondary_task,
    dataset_start_index,
    shuffle,
    seed,
):
    raw_dataset = load_dataset("caskcsg/LongBench-Pro", split=split)

    raw_dataset = raw_dataset.filter(lambda x: not any(x["secondary_task"].startswith(p) for p in ("T4.",)))

    if language != "all":
        raw_dataset = raw_dataset.filter(lambda x: x["language"] == language)
    if effective_token_length != "all":
        raw_dataset = raw_dataset.filter(lambda x: x["token_length"] == effective_token_length)
    if difficulty != "all":
        raw_dataset = raw_dataset.filter(lambda x: x["difficulty"] == difficulty)
    if primary_task is not None:
        raw_dataset = raw_dataset.filter(lambda x: x["primary_task"] == primary_task)
    if effective_secondary_task is not None:
        raw_dataset = raw_dataset.filter(lambda x: x["secondary_task"] == effective_secondary_task)

    dataset = raw_dataset.map(
        transform_example,
        with_indices=True,
        remove_columns=raw_dataset.column_names,
        writer_batch_size=100,
    )

    if dataset_start_index > 0:
        n_total = len(dataset)
        if dataset_start_index >= n_total:
            raise ValueError(f"dataset_start_index={dataset_start_index} out of range for dataset size {n_total}")
        dataset = dataset.select(range(dataset_start_index, n_total))

    if shuffle:
        _seed = seed if seed is not None else random.randint(1000, 100_000_000)
        dataset = dataset.shuffle(seed=_seed)

    return dataset
