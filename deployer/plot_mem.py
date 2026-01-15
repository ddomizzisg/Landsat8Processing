#!/usr/bin/env python3
"""
plot_mem_timeline.py
Plot a timeline of memory consumption per container from the CSV produced by cadvisor_scrape.py.

Expected CSV columns:
  t_sec, container, cpu_rate_core, cpu_pct_1core, mem_working_set_bytes, mem_mb

Usage:
  python plot_mem_timeline.py --in metrics.csv --out mem_timeline.png
Options:
  --containers c1 c2 ...     # optional: only plot these containers (space-separated)
  --downsample 1.0           # optional: bin size in seconds to average samples (default: 1.0)
  --rolling 1                # optional: rolling window (in samples) for smoothing (default: 1=no smoothing)
  --dpi 150                  # output image DPI (default 150)
"""

import argparse
import sys
import pandas as pd
import matplotlib.pyplot as plt

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="infile", required=True, help="input CSV (from cadvisor_scrape.py)")
    ap.add_argument("--out", dest="outfile", default="mem_timeline.png", help="output image path")
    ap.add_argument("--containers", nargs="*", default=None, help="optional list of container names to include")
    ap.add_argument("--downsample", type=float, default=1.0, help="bin width (seconds) to average samples")
    ap.add_argument("--rolling", type=int, default=1, help="rolling window (in samples) for smoothing")
    ap.add_argument("--dpi", type=int, default=150, help="output figure DPI")
    args = ap.parse_args()

    try:
        df = pd.read_csv(args.infile)
    except Exception as e:
        print(f"Error reading CSV: {e}", file=sys.stderr)
        sys.exit(1)

    # Validate columns
    required_cols = {"t_sec", "container", "mem_mb"}
    if not required_cols.issubset(df.columns):
        print(f"CSV must contain columns: {sorted(required_cols)}", file=sys.stderr)
        sys.exit(1)

    # Filter containers if requested
    if args.containers:
        df = df[df["container"].isin(args.containers)]
        if df.empty:
            print("No data after filtering by containers.", file=sys.stderr)
            sys.exit(1)

    # Clean types
    df = df.copy()
    df["t_sec"] = pd.to_numeric(df["t_sec"], errors="coerce")
    df["mem_mb"] = pd.to_numeric(df["mem_mb"], errors="coerce")
    df = df.dropna(subset=["t_sec", "mem_mb"])

    # Keep only first 800 seconds
    df = df[df["t_sec"] <= 800]


    # Optional downsampling: bin by floor(t_sec / bin)*bin and average
    bin_w = max(args.downsample, 0.001)
    df["_bin"] = (df["t_sec"] // bin_w) * bin_w

    # Prepare plot
    plt.figure(figsize=(10, 5))
    ax = plt.gca()

    # Plot each container
    for name, g in df.groupby("container"):
        g = g.sort_values("_bin")
        agg = g.groupby("_bin", as_index=False)["mem_mb"].mean()

        # Optional rolling smoothing
        if args.rolling > 1:
            agg["mem_mb"] = agg["mem_mb"].rolling(args.rolling, min_periods=1).mean()
        
        ax.plot(agg["_bin"], agg["mem_mb"], label=name)

    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Memory (MB)")
    ax.set_title("Memory timeline per container")
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.legend(loc="best", fontsize=8)
    plt.tight_layout()
    plt.savefig(args.outfile, dpi=args.dpi)
    print(f"Saved figure to {args.outfile}")

if __name__ == "__main__":
    main()
