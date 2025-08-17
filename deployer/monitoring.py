#!/usr/bin/env python3
"""
cadvisor_scrape.py
Scrape cAdvisor's /metrics endpoint periodically and write per-container CPU & memory stats to CSV.

- CPU is computed as a rate from `container_cpu_usage_seconds_total` (seconds/sec).
  cpu_pct_1core = 100 * rate  (approximate % of a single core).
- Memory is taken from `container_memory_working_set_bytes` (bytes).

Usage:
  python cadvisor_scrape.py --endpoint http://localhost:8080/metrics --interval 2 --duration 300 --out metrics.csv
"""

import argparse
import csv
import sys
import time
from urllib.request import urlopen


def split_labels(blob: str):
    """Split labels safely by commas not inside quotes."""
    parts, cur = [], []
    in_quotes, esc = False, False
    for ch in blob:
        if esc:
            cur.append(ch)
            esc = False
            continue
        if ch == "\\":
            esc = True
            continue
        if ch == '"':
            in_quotes = not in_quotes
            cur.append(ch)
            continue
        if ch == "," and not in_quotes:
            parts.append("".join(cur).strip())
            cur = []
        else:
            cur.append(ch)
    if cur:
        parts.append("".join(cur).strip())
    return parts


def parse_prom_text(text: str, metric_name: str):
    """
    Return list of (labels_dict, value_float) for the given metric_name
    from a Prometheus text exposition document.
    """
    out, prefix = [], metric_name
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or not line.startswith(prefix):
            continue
        labels, rest = {}, line[len(prefix):].strip()
        value_str = None
        if rest.startswith("{"):
            end = rest.find("}")
            if end != -1:
                labels_blob = rest[1:end]
                value_str = rest[end + 1:].strip()
                for pair in split_labels(labels_blob):
                    if "=" in pair:
                        k, v = pair.split("=", 1)
                        labels[k.strip()] = v.strip().strip('"')
        else:
            value_str = rest
        if not value_str:
            continue
        tok = value_str.split()
        try:
            val = float(tok[0])
        except ValueError:
            continue
        out.append((labels, val))
    return out


def label_to_container_name(labels: dict):
    candidates = [
        "container_label_io_kubernetes_container_name",
        "container_label_com_docker_swarm_task_name",
        "container_label_com_docker_compose_service",
        "name",
        "container",
        "id",
    ]
    for k in candidates:
        if k in labels and labels[k]:
            return labels[k]
    return labels.get("id", "unknown")


def fetch_text(endpoint: str, timeout: float = 10.0) -> str:
    with urlopen(endpoint, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--endpoint", default="http://localhost:8080/metrics")
    p.add_argument("--interval", type=float, default=2.0, help="sampling interval (seconds)")
    p.add_argument("--duration", type=float, default=300.0, help="total duration (seconds)")
    p.add_argument("--out", default="metrics.csv", help="output CSV path")
    args = p.parse_args()

    header = ["t_sec", "container", "cpu_rate_core", "cpu_pct_1core", "mem_working_set_bytes", "mem_mb"]
    prev_cpu, prev_t = {}, None
    t_start = time.time()

    with open(args.out, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)

        while True:
            now = time.time()
            if now - t_start > args.duration:
                break

            try:
                text = fetch_text(args.endpoint)
            except Exception as e:
                print(f"ERROR fetching metrics: {e}", file=sys.stderr)
                time.sleep(args.interval)
                continue

            cpu_samples = parse_prom_text(text, "container_cpu_usage_seconds_total")
            mem_samples = parse_prom_text(text, "container_memory_working_set_bytes")

            mem_by_container = {label_to_container_name(l): v for l, v in mem_samples}
            cpu_by_container = {label_to_container_name(l): v for l, v in cpu_samples}

            if prev_t is not None:
                dt = now - prev_t
                if dt > 0:
                    for name, cpu_val in cpu_by_container.items():
                        prev_val = prev_cpu.get(name)
                        if prev_val is None:
                            continue
                        d_cpu = cpu_val - prev_val
                        if d_cpu < 0:
                            continue
                        rate = d_cpu / dt
                        cpu_pct = 100.0 * rate
                        mem_bytes = mem_by_container.get(name, 0.0)
                        mem_mb = mem_bytes / (1024.0 * 1024.0)
                        w.writerow([
                            round(now - t_start, 3), name,
                            round(rate, 6), round(cpu_pct, 3),
                            int(mem_bytes), round(mem_mb, 3)
                        ])
                        f.flush()

            prev_cpu, prev_t = cpu_by_container, now
            time.sleep(max(0.0, args.interval - (time.time() - now)))

    print(f"Done. Wrote CSV to {args.out}")


if __name__ == "__main__":
    main()
