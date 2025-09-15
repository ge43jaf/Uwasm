#!/usr/bin/env python3
import subprocess
import time
import matplotlib.pyplot as plt
import numpy as np
import argparse
import statistics
import os
import json
from typing import List, Dict, Tuple
import psutil  # For memory monitoring

def get_peak_memory(program: str) -> float:
    """Run a program and return peak memory usage in MB"""
    process = subprocess.Popen(program, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    peak_memory = 0
    
    try:
        while process.poll() is None:
            try:
                mem_info = psutil.Process(process.pid).memory_info()
                peak_memory = max(peak_memory, mem_info.rss / (1024 * 1024))  # Convert to MB
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                break
            time.sleep(0.01)
    finally:
        if process.poll() is None:
            process.terminate()
            process.wait()
    
    return peak_memory

def run_program(program: str, test_file: str, runs: int = 5) -> Tuple[List[float], float]:
    """Run a program with a specific test file and return execution times and peak memory"""
    times = []
    memory_usages = []
    
    for _ in range(runs):
        # Time measurement
        start = time.perf_counter()
        subprocess.run(f"{program} {test_file}", shell=True, check=True, 
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        end = time.perf_counter()
        times.append((end - start) * 1000)  # Convert to milliseconds
        
        # Memory measurement
        memory_usage = get_peak_memory(f"{program} {test_file}")
        memory_usages.append(memory_usage)
    
    avg_time = statistics.mean(times)
    avg_memory = statistics.mean(memory_usages)
    
    return times, avg_time, avg_memory

def categorize_test_file(filename: str) -> str:
    """Categorize test file based on its name"""
    if filename.startswith("test_num_instr"):
        return "Arithmetic"
    elif filename.startswith("test_control_instr"):
        return "Control Flow"
    elif filename.startswith("test_mem_instr"):
        return "Memory Ops"
    elif filename.startswith("test_var_instr"):
        return "Variable Instructions"
    else:
        return "Other"

def benchmark_programs(programs: Dict[str, str], test_dir: str, runs: int = 5) -> Dict[str, Dict[str, Dict]]:
    """Benchmark multiple programs with categorized test files"""
    results = {prog_name: {"categories": {}, "individual": {}} for prog_name in programs.keys()}
    test_files = [f for f in os.listdir(test_dir) if f.endswith('.wat') or f.endswith('.wasm')]
    
    # Group test files by category
    categorized_files = {}
    for test_file in test_files:
        category = categorize_test_file(test_file)
        if category not in categorized_files:
            categorized_files[category] = []
        categorized_files[category].append(test_file)
    
    print(f"Found test categories: {list(categorized_files.keys())}")
    
    for prog_name, prog_cmd in programs.items():
        print(f"\nBenchmarking: {prog_name}")
        
        # Benchmark individual test files
        for category, files in categorized_files.items():
            print(f"  Category: {category}")
            category_times = []
            category_memories = []
            
            for test_file in files:
                full_path = os.path.join(test_dir, test_file)
                print(f"    Testing {test_file}...", end=" ", flush=True)
                
                try:
                    times, avg_time, avg_memory = run_program(prog_cmd, full_path, runs)
                    results[prog_name]["individual"][test_file] = {
                        "times": times,
                        "avg_time": avg_time,
                        "avg_memory": avg_memory,
                        "category": category
                    }
                    
                    category_times.append(avg_time)
                    category_memories.append(avg_memory)
                    print(f"Done (avg: {avg_time:.1f}ms, {avg_memory:.1f}MB)")
                    
                except subprocess.CalledProcessError:
                    print(f"Failed to run {test_file}")
                    continue
            
            # Calculate category averages
            if category_times:
                results[prog_name]["categories"][category] = {
                    "avg_time": statistics.mean(category_times),
                    "avg_memory": statistics.mean(category_memories),
                    "test_count": len(category_times)
                }
    
    return results

def generate_latex_table(results: Dict[str, Dict[str, Dict]]) -> str:
    """Generate LaTeX table from benchmark results"""
    programs = list(results.keys())
    categories = ["Arithmetic", "Control Flow", "Memory Ops", "Variable Instructions"]
    
    latex_table = """\\begin{table}[H]
\\centering
\\caption{Execution time and peak memory usage comparison across runtimes.}
\\label{tab:runtime-comparison}
\\begin{tabular}{lccc}
\\toprule
\\textbf{Benchmark} & \\textbf{This Interpreter} & \\textbf{wat2wasm} & \\textbf{Wasmtime} \\\\
\\midrule
"""
    
    # Add timing results for each category
    for category in categories:
        if category in results[programs[0]]["categories"]:
            row = f"{category} (ms)    & "
            row_parts = []
            for prog_name in programs:
                if category in results[prog_name]["categories"]:
                    time_val = results[prog_name]["categories"][category]["avg_time"]
                    row_parts.append(f"{time_val:.0f}")
                else:
                    row_parts.append("N/A")
            row += "  & ".join(row_parts) + "  \\\\\n"
            latex_table += row
    
    # Add memory results
    latex_table += "\\midrule\nPeak Memory (MB)   & "
    memory_parts = []
    for prog_name in programs:
        # Calculate average memory across all categories
        memories = [cat_data["avg_memory"] for cat_data in results[prog_name]["categories"].values()]
        if memories:
            avg_memory = statistics.mean(memories)
            memory_parts.append(f"{avg_memory:.0f}")
        else:
            memory_parts.append("N/A")
    latex_table += "  & ".join(memory_parts) + "  \\\\\n"
    
    latex_table += """\\bottomrule
\\end{tabular}
\\end{table}"""
    
    return latex_table

def plot_results(results: Dict[str, Dict[str, Dict]]):
    """Generate comparison plots"""
    available_styles = plt.style.available
    preferred_styles = ['seaborn-v0_8', 'seaborn', 'ggplot', 'fast']
    selected_style = next((s for s in preferred_styles if s in available_styles), 'default')
    plt.style.use(selected_style)
    
    programs = list(results.keys())
    categories = ["Arithmetic", "Control Flow", "Memory Ops", "Variable Instructions"]
    
    # Category comparison plot
    plt.figure(figsize=(12, 8))
    
    x = np.arange(len(categories))
    width = 0.25
    
    for i, prog_name in enumerate(programs):
        times = []
        for category in categories:
            if category in results[prog_name]["categories"]:
                times.append(results[prog_name]["categories"][category]["avg_time"])
            else:
                times.append(0)
        
        plt.bar(x + i * width, times, width, label=prog_name)
    
    plt.xlabel('Test Categories')
    plt.ylabel('Average Execution Time (ms)')
    plt.title('Execution Time by Category and Runtime')
    plt.xticks(x + width, categories)
    plt.legend()
    plt.tight_layout()
    plt.savefig("category_comparison.png", dpi=150, bbox_inches='tight')
    plt.close()
    
    # Memory usage plot
    plt.figure(figsize=(10, 6))
    
    memories = []
    for prog_name in programs:
        # Calculate average memory across all categories
        mem_vals = [cat_data["avg_memory"] for cat_data in results[prog_name]["categories"].values()]
        memories.append(statistics.mean(mem_vals) if mem_vals else 0)
    
    plt.bar(programs, memories)
    plt.xlabel('Runtime')
    plt.ylabel('Average Peak Memory (MB)')
    plt.title('Peak Memory Usage Comparison')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("memory_comparison.png", dpi=150, bbox_inches='tight')
    plt.close()

def save_detailed_results(results: Dict[str, Dict[str, Dict]], filename: str = "detailed_results.json"):
    """Save detailed results to JSON file"""
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)

def main():
    parser = argparse.ArgumentParser(description="Benchmark WebAssembly runtimes with categorized tests")
    parser.add_argument("--test-dir", default="../tests/success", 
                       help="Directory containing test files")
    parser.add_argument("--runs", type=int, default=5,
                       help="Number of runs per test file")
    parser.add_argument("--output", default="benchmark_results.tex",
                       help="Output LaTeX table filename")
    
    args = parser.parse_args()
    
    # Define programs to benchmark
    programs = {
        "This Interpreter": "python3 main.py",
        "wat2wasm": "wat2wasm",
        "Wasmtime": "wasmtime"
    }
    
    print(f"Benchmarking programs: {', '.join(programs.keys())}")
    print(f"Test directory: {args.test_dir}")
    print(f"Runs per test: {args.runs}")
    
    if not os.path.exists(args.test_dir):
        print(f"Error: Test directory '{args.test_dir}' does not exist!")
        return
    
    results = benchmark_programs(programs, args.test_dir, args.runs)
    
    # Generate LaTeX table
    latex_table = generate_latex_table(results)
    with open(args.output, 'w') as f:
        f.write(latex_table)
    
    # Generate plots
    plot_results(results)
    
    # Save detailed results
    save_detailed_results(results)
    
    print(f"\nBenchmark completed!")
    print(f"LaTeX table saved as: {args.output}")
    print(f"Plots saved as: category_comparison.png and memory_comparison.png")
    print(f"Detailed results saved as: detailed_results.json")
    
    # Print summary
    print("\n" + "="*50)
    print("SUMMARY RESULTS:")
    print("="*50)
    print(latex_table)

if __name__ == "__main__":
    main()