import asyncio
import os
import json
import pandas as pd
from collections import Counter

from wine_press_lm_evaluation.core.helpers.sources_duplicates_filter import (
    remove_sources_duplicates,
)

# === CONFIG ===
BASE_PATH = "../evaluations"
OUTPUT_BASE = "../results"
os.makedirs(OUTPUT_BASE, exist_ok=True)


def collect_json_files(base_dir):
    """Find JSONs matching pattern <subfolder>/results/<subfolder>.json"""
    json_files = []
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".json"):
                json_files.append(os.path.join(root, file))
    return json_files


def process_json_file(path):
    """Read and extract both evaluation + sources sections from JSON"""
    evals, sources = [], []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for item in data:
            if "evaluation" in item:
                evals.append(item["evaluation"])
            if "sources" in item and isinstance(item["sources"], list):
                sources.extend(item["sources"])
    except Exception as e:
        print(f"⚠️ Skipping {path}: {e}")
    return evals, sources


def compute_evaluation_stats(evaluations):
    """Compute counts of True/False/Null per variable"""
    stats = {}
    for eval_entry in evaluations:
        for key, value in eval_entry.items():
            if key not in stats:
                stats[key] = {"true": 0, "false": 0, "null": 0, "total": 0}
            stats[key]["total"] += 1
            if value is True:
                stats[key]["true"] += 1
            elif value is False:
                stats[key]["false"] += 1
            else:
                stats[key]["null"] += 1

    df = pd.DataFrame.from_dict(stats, orient="index")
    df["true_%"] = (df["true"] / df["total"]) * 100
    df["false_%"] = (df["false"] / df["total"]) * 100
    df["null_%"] = (df["null"] / df["total"]) * 100
    return df[["total", "true", "false", "null", "true_%", "false_%", "null_%"]]


async def compute_source_stats(sources):
    """Count number of occurrences per unique source string"""
    clean_sources = await remove_sources_duplicates(sources)
    counter = Counter(clean_sources)
    df = pd.DataFrame(counter.items(), columns=["source", "count"]).sort_values(
        by="count", ascending=False
    )
    return df


def main():
    json_files = collect_json_files(BASE_PATH)

    for json_path in json_files:
        # extract subfolder name — e.g. "wine_for_aperitif"
        parts = json_path.split(os.sep)
        if "results" not in parts:
            continue
        subfolder_index = parts.index("results") - 1
        subfolder_name = parts[subfolder_index]

        print(f"📄 Processing {subfolder_name}")

        # extract evaluations + sources
        evaluations, sources = process_json_file(json_path)

        # create dedicated results subfolder
        result_dir = os.path.join(OUTPUT_BASE, subfolder_name)
        os.makedirs(result_dir, exist_ok=True)

        # --- EVALUATION STATS ---
        if evaluations:
            eval_df = compute_evaluation_stats(evaluations)
            eval_csv_path = os.path.join(result_dir, "evaluations.csv")
            eval_df.to_csv(eval_csv_path, index_label="variable")
            print(f"✅ Saved evaluation stats: {eval_csv_path}")
        else:
            print(f"⚠️ No evaluations found in {json_path}")

        # --- SOURCE STATS ---
        if sources:
            src_df = asyncio.run(compute_source_stats(sources))
            src_csv_path = os.path.join(result_dir, "sources.csv")
            src_df.to_csv(src_csv_path, index=False)
            print(f"✅ Saved source stats: {src_csv_path}")
        else:
            print(f"⚠️ No sources found in {json_path}")


if __name__ == "__main__":
    main()
