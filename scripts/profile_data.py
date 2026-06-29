#!/usr/bin/env python
"""Lightweight data profiler for scientific figure selection."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence


def _read_table(path: Path):
    try:
        import pandas as pd
    except Exception as exc:
        raise RuntimeError("pandas is required for profile_data.py") from exc
    ext = path.suffix.lower()
    if ext in {".xlsx", ".xls"}:
        return pd.read_excel(path)
    if ext == ".tsv":
        return pd.read_csv(path, sep="\t")
    return pd.read_csv(path)


def _series_type(s) -> str:
    import pandas as pd
    if pd.api.types.is_bool_dtype(s):
        return "binary"
    if pd.api.types.is_numeric_dtype(s):
        non_na = s.dropna()
        unique = non_na.nunique()
        if unique <= 2:
            return "binary"
        if unique <= 12 and unique / max(len(non_na), 1) < 0.2:
            return "ordinal_or_discrete"
        return "continuous"
    if pd.api.types.is_datetime64_any_dtype(s):
        return "time"
    unique = s.dropna().nunique()
    if unique <= 2:
        return "binary"
    return "categorical"


def _continuous_profile(s) -> dict:
    clean = s.dropna()
    q1 = clean.quantile(0.25) if len(clean) else None
    q3 = clean.quantile(0.75) if len(clean) else None
    iqr = (q3 - q1) if q1 is not None and q3 is not None else None
    outliers = 0
    if iqr is not None:
        outliers = int(((clean < q1 - 1.5 * iqr) | (clean > q3 + 1.5 * iqr)).sum())
    ratio = None
    if len(clean) and clean.min() > 0:
        ratio = float(clean.max() / clean.min()) if clean.min() != 0 else None
    return {
        "n": int(clean.count()),
        "missing": int(s.isna().sum()),
        "mean": float(clean.mean()) if len(clean) else None,
        "sd": float(clean.std()) if len(clean) > 1 else None,
        "median": float(clean.median()) if len(clean) else None,
        "min": float(clean.min()) if len(clean) else None,
        "max": float(clean.max()) if len(clean) else None,
        "skew": float(clean.skew()) if len(clean) > 2 else None,
        "iqr_outliers": outliers,
        "suggest_log_axis": bool(ratio is not None and ratio >= 100),
    }


def _categorical_profile(s) -> dict:
    counts = s.fillna("<missing>").astype(str).value_counts().head(20)
    return {
        "n": int(s.notna().sum()),
        "missing": int(s.isna().sum()),
        "levels": int(s.dropna().nunique()),
        "top_levels": counts.to_dict(),
    }


def profile_data(path: str | Path, group_cols: Sequence[str] = ()) -> dict:
    path = Path(path)
    df = _read_table(path)
    columns = {}
    suggestions: list[str] = []
    for name in df.columns:
        s = df[name]
        typ = _series_type(s)
        item = {"type": typ}
        if typ in {"continuous", "ordinal_or_discrete"}:
            item.update(_continuous_profile(s))
            if item.get("n", 0) < 10:
                suggestions.append(f"{name}: n<10; show raw points and avoid mean-only bars.")
            if item.get("skew") is not None and abs(item["skew"]) > 1:
                suggestions.append(f"{name}: skewed distribution; avoid hiding distribution with mean bars.")
            if item.get("suggest_log_axis"):
                suggestions.append(f"{name}: spans >=100x; consider log scale if scientifically meaningful.")
        else:
            item.update(_categorical_profile(s))
            if item.get("levels", 0) > 8:
                suggestions.append(f"{name}: many categories; avoid crowded legends and tiny tick labels.")
        columns[str(name)] = item

    groups = {}
    for col in group_cols:
        if col in df.columns:
            size = df.groupby(col, dropna=False).size()
            groups[col] = {str(k): int(v) for k, v in size.items()}
            if size.min() < 10:
                suggestions.append(f"{col}: at least one group has n<10; show raw points.")

    return {
        "source": str(path),
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "column_profiles": columns,
        "group_sizes": groups,
        "suggestions": suggestions,
    }


def render_markdown(info: dict) -> str:
    lines = [
        f"# Data Profile: {info['source']}",
        "",
        f"- rows: {info['rows']}",
        f"- columns: {info['columns']}",
        "",
        "## Columns",
    ]
    for name, item in info["column_profiles"].items():
        lines.append(f"- `{name}`: {item['type']}, n={item.get('n')}, missing={item.get('missing')}")
        if item["type"] in {"continuous", "ordinal_or_discrete"}:
            lines.append(
                f"  mean={item.get('mean')}, sd={item.get('sd')}, median={item.get('median')}, skew={item.get('skew')}"
            )
        else:
            lines.append(f"  levels={item.get('levels')}, top={item.get('top_levels')}")
    if info.get("group_sizes"):
        lines.extend(["", "## Group Sizes"])
        for col, sizes in info["group_sizes"].items():
            lines.append(f"- `{col}`: {sizes}")
    if info.get("suggestions"):
        lines.extend(["", "## Plotting Warnings"])
        lines.extend(f"- {x}" for x in info["suggestions"])
    return "\n".join(lines) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Profile tabular data before figure selection")
    parser.add_argument("source")
    parser.add_argument("--group", action="append", default=[])
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    info = profile_data(args.source, group_cols=args.group)
    if args.json:
        print(json.dumps(info, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(info))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
