#!/usr/bin/env python3
import subprocess
import time
import matplotlib.pyplot as plt
import numpy as np
import argparse
import statistics
from typing import List, Dict

def run_program(program: str, iterations: int, runs: int = 5) -> List[float]:
    """Run a program multiple times and return execution times in seconds"""
    times = []
    for _ in range(runs):
        start = time.perf_counter()
        subprocess.run(f"for i in $(seq 1 {iterations}); do {program}; done", 
                      shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        end = time.perf_counter()
        times.append(end - start)
    return times

def benchmark(programs: List[str], iteration_counts: List[int]) -> Dict[str, Dict[int, List[float]]]:
    """Benchmark multiple programs with different iteration counts"""
    results = {prog: {} for prog in programs}
    
    for prog in programs:
        print(f"\nBenchmarking: {prog}")
        for n in iteration_counts:
            print(f"  Running {n} iterations...", end=" ", flush=True)
            times = run_program(prog, n)
            results[prog][n] = times
            print(f"Done (avg: {statistics.mean(times):.3f}s)")
    
    return results

def plot_results(results: Dict[str, Dict[int, List[float]]]):
    """Generate comparison plots"""
    # Use available style that looks similar to seaborn
    available_styles = plt.style.available
    preferred_styles = ['seaborn-v0_8', 'seaborn', 'ggplot', 'fast']
    selected_style = next((s for s in preferred_styles if s in available_styles), 'default')
    plt.style.use(selected_style)
    
    iteration_counts = sorted(next(iter(results.values())).keys())
    
    # Box plot
    plt.figure(figsize=(12, 6))
    data = []
    labels = []
    for prog, prog_data in results.items():
        for n, times in prog_data.items():
            data.append(times)
            labels.append(f"{prog.split()[0]}\nn={n}")
    
    plt.boxplot(data, labels=labels)
    plt.title("Execution Time Distribution")
    plt.ylabel("Time (seconds)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("benchmark_boxplot.png", dpi=150, bbox_inches='tight')
    plt.close()
    
    # Line plot (average times)
    plt.figure(figsize=(12, 6))
    markers = ['o', 's', '^', 'D', 'v', '>', '<', 'p', '*']
    for i, (prog, prog_data) in enumerate(results.items()):
        avg_times = [statistics.mean(times) for n, times in sorted(prog_data.items())]
        plt.plot(iteration_counts, avg_times, marker=markers[i % len(markers)], 
                 linestyle='-', label=prog.split()[0])
    
    plt.xscale('log')
    plt.yscale('log')
    plt.title("Average Execution Time vs Iterations")
    plt.xlabel("Number of iterations (log scale)")
    plt.ylabel("Time (seconds, log scale)")
    plt.legend()
    plt.grid(True, which="both", ls="--")
    plt.savefig("benchmark_lineplot.png", dpi=150, bbox_inches='tight')
    plt.close()

def main():
    parser = argparse.ArgumentParser(description="Benchmark command-line programs")
    parser.add_argument("programs", nargs="+", help="Programs to benchmark")
    parser.add_argument("--iterations", nargs="+", type=int, 
                       default=[10, 100, 1000], #, 10000],
                       help="Iteration counts to test")
    parser.add_argument("--runs", type=int, default=5,
                       help="Number of runs per iteration count")
    args = parser.parse_args()
    
    print(f"Benchmarking programs: {', '.join(args.programs)}")
    print(f"Testing iterations: {args.iterations}")
    print(f"Runs per configuration: {args.runs}")
    print(f"Available matplotlib styles: {plt.style.available}")
    
    results = benchmark(args.programs, args.iterations)
    plot_results(results)
    
    print("\nBenchmark completed!")
    print(f"Plots saved as: benchmark_boxplot.png and benchmark_lineplot.png")

if __name__ == "__main__":
    main()
