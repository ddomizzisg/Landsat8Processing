#!/usr/bin/env python3
"""
plot_timeline.py
Plot memory/CPU timelines per *group* of containers and save aggregated values to CSV.

Supports grouping with wildcards:
  --group app=frontend,backend,worker
  --group detector=detector*

Examples:
  python plot_timeline.py --in metrics.csv --out timeline.png \
      --metric both --group app=frontend,backend,worker --group detector=detector* \
      --csv-out results.csv
"""

import argparse
import sys
import pandas as pd
import matplotlib.pyplot as plt
import fnmatch

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="infile", required=True,
                    help="input CSV (from cadvisor_scrape.py)")
    ap.add_argument("--out", dest="outfile", default="timeline.png",
                    help="output image path")
    ap.add_argument("--group", action="append", default=[],
                    help="define a group: NAME=pattern1,pattern2,... (supports wildcards, comma-separated)")
    ap.add_argument("--csv-out", dest="csv_out", default=None,
                    help="optional CSV file to save aggregated values (default: same as --out with _groups.csv)")
    ap.add_argument("--downsample", type=float, default=1.0,
                    help="bin width (seconds) to average samples")
    ap.add_argument("--rolling", type=int, default=1,
                    help="rolling window (in samples) for smoothing")
    ap.add_argument("--dpi", type=int, default=150,
                    help="output figure DPI")
    ap.add_argument("--metric", choices=["both","mem","cpu"], default="both",
                    help="metric(s) to plot")
    ap.add_argument("--cpu-metric", choices=["pct","cores"], default="pct",
                    help="CPU unit to plot")
    ap.add_argument("--tmax", type=float, default=10000,
                    help="only plot samples with t_sec <= tmax")
    args = ap.parse_args()

    # Load CSV
    try:
        df = pd.read_csv(args.infile)
    except Exception as e:
        print(f"Error reading CSV: {e}", file=sys.stderr)
        sys.exit(1)

    df = df.copy()
    df["t_sec"] = pd.to_numeric(df.get("t_sec"), errors="coerce")

    want_mem = args.metric in ("both", "mem")
    want_cpu = args.metric in ("both", "cpu")

    if want_mem and "mem_mb" not in df.columns:
        print("CSV must contain 'mem_mb'", file=sys.stderr)
        sys.exit(1)
    if want_cpu:
        cpu_col = "cpu_pct_1core" if args.cpu_metric == "pct" else "cpu_rate_core"
        if cpu_col not in df.columns:
            print(f"CSV must contain '{cpu_col}'", file=sys.stderr)
            sys.exit(1)
    else:
        cpu_col = None

    # Limit by time
    df = df[df["t_sec"] <= args.tmax]

    # Downsample bin
    bin_w = max(args.downsample, 0.001)
    df["_bin"] = (df["t_sec"] // bin_w) * bin_w

    # --- Build groups ---
    groups = {}  # name -> set(containers)
    all_containers = set(df["container"].unique())

    if not args.group:
        print("You must provide at least one --group", file=sys.stderr)
        sys.exit(1)

    for gdef in args.group:
        if "=" not in gdef:
            print(f"Invalid --group {gdef}, expected NAME=pattern1,pattern2,...", file=sys.stderr)
            sys.exit(1)
        gname, patterns = gdef.split("=", 1)
        members = set()
        for pat in patterns.split(","):
            matches = fnmatch.filter(all_containers, pat)
            members.update(matches)
        if not members:
            print(f"Warning: group {gname} matched no containers", file=sys.stderr)
        groups[gname] = members

    # Plot
    if args.metric == "both":
        fig, axes = plt.subplots(2, 1, figsize=(12, 6), sharex=True)
        ax_mem, ax_cpu = axes
    else:
        fig, ax = plt.subplots(1, 1, figsize=(12, 4))
        ax_mem = ax if want_mem else None
        ax_cpu = ax if want_cpu else None

    def plot_series(ax, agg, col, label, ylabel, title=None):
        if args.rolling > 1:
            agg[col] = agg[col].rolling(args.rolling, min_periods=1).mean()
        ax.plot(agg["_bin"], agg[col], label=label)
        if ylabel:
            ax.set_ylabel(ylabel)
        if title:
            ax.set_title(title)
        ax.grid(True, linestyle="--", alpha=0.4)
        ax.set_xlim(0, args.tmax)

    # Collect aggregated data for CSV
    all_aggs = []

    # Plot aggregated groups only
    for gname, members in groups.items():
        sub = df[df["container"].isin(members)]
        if sub.empty:
            continue
        agg = sub.groupby("_bin", as_index=False).agg(
            {"mem_mb": "sum", cpu_col: "sum"} if cpu_col else {"mem_mb": "sum"}
        )

        #if cpu_col:
        #    agg[cpu_col] = agg[cpu_col] * 8
        #    agg[agg[cpu_col] >= 2400] = 2400
             
        #agg["mem_mb"] = agg["mem_mb"] * 20
        agg.insert(0, "group", gname)  # add group column
        all_aggs.append(agg)

        if want_mem:
            plot_series(ax_mem, agg, "mem_mb", gname, "Memory (MB)",
                        "Memory timeline per group" if args.metric != "cpu" else None)
        if want_cpu:
            ylab = "CPU (% of one core)" if args.cpu_metric == "pct" else "CPU (cores)"
            plot_series(ax_cpu, agg, cpu_col, gname, ylab,
                        "CPU timeline per group" if args.metric != "mem" else None)

    # Save aggregated CSV
    if all_aggs:
        df_out = pd.concat(all_aggs, ignore_index=True)
        if args.csv_out:
            out_csv = args.csv_out
        else:
            out_csv = args.outfile.rsplit(".", 1)[0] + "_groups.csv"
        df_out.to_csv(out_csv, index=False)
        print(f"Saved aggregated values to {out_csv}")
    else:
        print("No groups produced data, nothing to save.")

    # Finalize figure
    if args.metric == "both":
        ax_mem.legend(fontsize=8)
        ax_cpu.legend(fontsize=8)
        ax_cpu.set_xlabel("Time (s)")
        fig.suptitle("Resource timelines (grouped)", y=0.98)
        fig.tight_layout(rect=[0, 0, 1, 0.96])
    else:
        ax = ax_mem if want_mem else ax_cpu
        ax.legend(fontsize=8)
        ax.set_xlabel("Time (s)")

    plt.tight_layout()
    plt.savefig(args.outfile, dpi=args.dpi)
    print(f"Saved figure to {args.outfile}")

if __name__ == "__main__":
    main()
