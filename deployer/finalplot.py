#!/usr/bin/env python3
"""
plot_group_csvs_grid.py
Plot memory/CPU timelines from one or more aggregated group CSVs (output of plot_timeline.py),
placing each group in its own subplot (grid). Generates two figures:
  <out-prefix>_memory.png
  <out-prefix>_cpu.png

Each CSV must contain columns:
  group, _bin, mem_mb [, cpu_pct_1core or cpu_rate_core]

Examples:
  python plot_group_csvs_grid.py --csv exp1.csv exp2.csv --out-prefix compare --norm-cores 24 --tmax 800
"""

import argparse
import os
import math
import pandas as pd
import matplotlib.pyplot as plt

# --- Style setup ---
plt.style.use("paper.mplstyle")
pt = 1. / 72.27
jour_sizes = {"PRD": {"onecol": 246. * pt, "twocol": 510. * pt}}
my_width = jour_sizes["PRD"]["twocol"]
golden = (1 + 5 ** 0.5) / 1.2
plt.rcParams.update({
    'axes.labelsize': 14,
    'legend.fontsize': 14,
    'xtick.labelsize': 12,
})

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", nargs="+", required=True,
                    help="one or more CSV files (output from plot_timeline.py)")
    ap.add_argument("--out-prefix", default="compare",
                    help="prefix for output images; creates <prefix>_memory.png and <prefix>_cpu.png")
    ap.add_argument("--cpu-metric", choices=["pct","cores"], default="pct",
                    help="read CPU from csv as % of one core (pct) or in cores")
    ap.add_argument("--norm-cores", default="24",
                help="normalize CPU to this many cores (e.g., 24), or 'auto' to detect from data")

    ap.add_argument("--dpi", type=int, default=150,
                    help="output figure DPI")
    ap.add_argument("--tmax", type=float, default=800,
                    help="only plot samples with _bin <= tmax (seconds)")
    args = ap.parse_args()

    # Load and concat
    dfs = []
    for fname in args.csv:
        df_i = pd.read_csv(fname)
        df_i["_source"] = os.path.basename(fname)
        dfs.append(df_i)
    df = pd.concat(dfs, ignore_index=True)

    # Fixed color map per tool/group
    COLOR_MAP = {
        "nez": "tab:blue",
        "makeflow": "tab:orange",
        "nextflow": "tab:green",
        "parsl": "tab:red",
    }

    # Filter time
    if "_bin" not in df.columns:
        raise ValueError("CSV must contain column '_bin'")
    df = df[df["_bin"] <= args.tmax].copy()

    # Check columns
    if "mem_mb" not in df.columns:
        raise ValueError("CSV must contain column 'mem_mb'")
    cpu_col = "cpu_pct_1core" if args.cpu_metric == "pct" else "cpu_rate_core"
    if cpu_col not in df.columns:
        raise ValueError(f"CSV must contain column '{cpu_col}'")

        # --- Prepare normalized CPU (% of N cores) ---
    if args.norm_cores == "auto":
        if "cpu_pct_1core" not in df.columns:
            raise ValueError("Need cpu_pct_1core column to auto-detect cores")
        max_val = df["cpu_pct_1core"].max()
        detected = int(round(max_val / 100))  # e.g. 4725 → 47
        N = detected
        print(f"[INFO] Auto-detected ~{N} logical CPUs (max cpu_pct_1core={max_val:.1f})")
    else:
        N = float(args.norm_cores)

    if args.cpu_metric == "pct":
        # cpu_pct_1core: percent of 1 core → percent of N cores
        df["cpu_pct_norm"] = (df["cpu_pct_1core"] / N).clip(upper=100)
        #df["cpu_pct_norm"] = ((df["cpu_rate_core"] / N) * 100.0).clip(upper=100)
        #df[df["cpu_pct_norm"] > 100] = 100
        print(df["cpu_pct_norm"])    
    else:
        # cpu_rate_core: cores → percent of N cores
        df["cpu_pct_norm"] = (df["cpu_rate_core"] / N) * 100.0


    groups = sorted(df["group"].unique())
    n_groups = len(groups)

    # Grid layout
    ncols = 4
    nrows = 1 #math.ceil(n_groups / ncols)

    # --- MEMORY PLOTS ---
    fig_mem, axes_mem = plt.subplots(nrows, ncols, figsize=(my_width, my_width / golden), sharex=True, sharey=True)
    axes_mem = axes_mem.flatten()

    for idx, group_name in enumerate(groups):
        ax = axes_mem[idx]
        gdf = df[df["group"] == group_name]
        for source, sub in gdf.groupby("_source"):
            sub = sub.sort_values("_bin")
            color = COLOR_MAP.get(group_name, None)  # fallback to auto if not in map
            ax.plot(sub["_bin"], sub["mem_mb"], label=group_name.capitalize(), color=color)
        #ax.set_title(group_name)
        if idx == 0: 
            ax.set_ylabel("Memory (MB)")
        ax.grid(True, linestyle="--", alpha=0.4)
        ax.set_xlim(0, args.tmax)
        #if idx == n_groups - 1:
        #    ax.legend(fontsize=8)

    # Hide unused subplots
    for j in range(idx+1, len(axes_mem)):
        axes_mem[j].axis("off")

    # After plotting all subplots (e.g., memory grid)
    handles, labels = [], []
    for ax in axes_mem:
        h, l = ax.get_legend_handles_labels()
        handles.extend(h)
        labels.extend(l)

    # Remove duplicates
    by_label = dict(zip(labels, handles))

    # Add a single legend to the figure
    fig_mem.legend(by_label.values(), by_label.keys(),
                loc="upper center", ncol=4, frameon=True)

    fig_mem.supxlabel("Time (s)")

    #fig_mem.suptitle("Memory timelines per group", y=0.995)
    fig_mem.tight_layout(rect=[0, 0, 1, 0.97])
    out_mem = f"{args.out_prefix}_memory.png"
    fig_mem.savefig(out_mem, dpi=args.dpi)
    print(f"Saved {out_mem}")

    # --- CPU PLOTS ---
    fig_cpu, axes_cpu = plt.subplots(nrows, ncols, figsize=(my_width, my_width / golden), sharex=True, sharey=True)
    axes_cpu = axes_cpu.flatten()

    for idx, group_name in enumerate(groups):
        ax = axes_cpu[idx]
        gdf = df[df["group"] == group_name]
        for source, sub in gdf.groupby("_source"):
            sub = sub.sort_values("_bin")
            color = COLOR_MAP.get(group_name, None)  # fallback to auto if not in map
            ax.plot(sub["_bin"], sub["cpu_pct_norm"], label=source, color=color)
        #ax.set_title(group_name)
        if idx == 0: 
            ax.set_ylabel(f"CPU (\% of {int(N)} cores)")
        ax.grid(True, linestyle="--", alpha=0.4)
        ax.set_xlim(0, args.tmax)
        ax.set_ylim(0,100)
        #if idx == n_groups - 1:
        #    ax.legend(fontsize=8)

    # Hide unused subplots
    for j in range(idx+1, len(axes_cpu)):
        axes_cpu[j].axis("off")

    fig_cpu.supxlabel("Time (s)")

    #fig_cpu.suptitle("CPU timelines per group", y=0.995)
    fig_cpu.tight_layout(rect=[0, 0, 1, 0.97])
    out_cpu = f"{args.out_prefix}_cpu.png"
    fig_cpu.savefig(out_cpu, dpi=args.dpi)
    print(f"Saved {out_cpu}")

if __name__ == "__main__":
    main()
