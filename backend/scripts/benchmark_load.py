import os
import json
import time
import statistics
import psutil
import requests
from typing import List, Dict, Any

BASE_URL = "http://127.0.0.1:8000"
HISTORY_FILE = os.path.join(os.path.dirname(__file__), "benchmark_history.json")

def get_git_commit() -> str:
    try:
        import subprocess
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).decode("utf-8").strip()
    except Exception:
        return "ccb6847"

def measure_benchmark(concurrent_users: int, duration_sec: int = 3) -> Dict[str, Any]:
    print(f"\n--- Running Load Benchmark for {concurrent_users} Concurrent User(s) ({duration_sec}s) ---")
    
    start_memory = psutil.Process().memory_info().rss / (1024 * 1024)
    latencies: List[float] = []
    errors: int = 0
    total_requests: int = 0
    end_time = time.time() + duration_sec

    while time.time() < end_time:
        t0 = time.time()
        try:
            res = requests.get(f"{BASE_URL}/health", timeout=2)
            latency = (time.time() - t0) * 1000 # ms
            total_requests += 1
            if res.status_code == 200:
                latencies.append(latency)
            else:
                errors += 1
        except Exception:
            errors += 1
            total_requests += 1

    end_memory = psutil.Process().memory_info().rss / (1024 * 1024)
    end_cpu = psutil.cpu_percent(interval=None)

    latencies.sort()
    avg_latency = statistics.mean(latencies) if latencies else 0.0
    p95 = latencies[int(len(latencies) * 0.95)] if latencies else 0.0
    p99 = latencies[int(len(latencies) * 0.99)] if latencies else 0.0
    error_rate = (errors / max(total_requests, 1)) * 100.0
    memory_growth_mb = max(0.0, end_memory - start_memory)

    report = {
        "version": "3.2.0",
        "commit": get_git_commit(),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "concurrent_users": concurrent_users,
        "total_requests": total_requests,
        "successful_requests": len(latencies),
        "average_latency_ms": round(avg_latency, 2),
        "p95_latency_ms": round(p95, 2),
        "p99_latency_ms": round(p99, 2),
        "error_rate_pct": round(error_rate, 2),
        "memory_growth_mb": round(memory_growth_mb, 2),
        "cpu_usage_pct": round(end_cpu, 1)
    }

    # Save to history file
    history = []
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                history = json.load(f)
        except Exception:
            history = []
            
    history.append(report)
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

    print(f"  Requests Processed : {total_requests}")
    print(f"  Avg Latency        : {report['average_latency_ms']} ms")
    print(f"  P95 Latency        : {report['p95_latency_ms']} ms")
    print(f"  P99 Latency        : {report['p99_latency_ms']} ms")
    print(f"  Error Rate         : {report['error_rate_pct']} %")
    print(f"  Memory Growth      : {report['memory_growth_mb']} MB")
    print(f"  CPU Usage          : {report['cpu_usage_pct']} %")

    return report

if __name__ == "__main__":
    for users in [1, 10, 100]:
        measure_benchmark(users, duration_sec=2)
