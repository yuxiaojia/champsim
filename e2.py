import os
import re
import csv

# Directories to compare
dirs = [
    "/Users/jarvisjia/Documents/2025_spring/cs7292/champsim/champsim_stat/champsim/results_8core_10M_16",
    # "/Users/jarvisjia/Documents/2025_spring/cs7292/champsim/champsim_2/champsim/results_1core_20M",
    # "/Users/jarvisjia/Documents/2025_spring/cs7292/champsim/champsim_baseline/champsim/results_1core_20M"
]

# Tags to identify each version in the CSV
dir_tags = ["v1", "v2", "v3"]

# Prefix to remove from filename
prefix_to_strip = "mix0-perceptron-no-no-no-lru-8core"

# Extract stats from a single file
def extract_stats(filepath):
    ipc = instructions = cycles = llc_mshr_merging = mshr_hit_diff = mshr_full_stall = None

    with open(filepath, 'r') as file:
        for line in file:
            if "CPU 0 cumulative IPC" in line:
                match = re.search(r'CPU 0 cumulative IPC: ([\d.]+) instructions: (\d+) cycles: (\d+)', line)
                if match:
                    ipc = float(match.group(1))
                    instructions = int(match.group(2))
                    cycles = int(match.group(3))
            elif "LLC" in line and "mshr" in line and "merging" in line.lower():
                match = re.search(r'LLC mshr merging\s+(\d+)', line, re.IGNORECASE)
                if match:
                    llc_mshr_merging = int(match.group(1))
            elif "whole_llc_mshr_hit_diff_cpu_id" in line:
                match = re.search(r'whole_llc_mshr_hit_diff_cpu_id\s+(\d+)', line)
                if match:
                    mshr_hit_diff = int(match.group(1))
            elif "llc_mshr_full_stall" in line:
                match = re.search(r"llc_mshr_full_stall\s+(\d+)", line)
                if match:
                    mshr_full_stall = int(match.group(1))

    return ipc, instructions, cycles, llc_mshr_merging, mshr_hit_diff, mshr_full_stall

# Get list of files from the first directory
filenames = [f for f in os.listdir(dirs[0]) if os.path.isfile(os.path.join(dirs[0], f))]

# Open CSV and write header
with open("comparison_16.csv", mode='w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    # Header row
    header = ["filename"]
    for tag in dir_tags:
        header += [
            f"ipc_{tag}", f"instructions_{tag}", f"cycles_{tag}",
            f"llc_mshr_merging_{tag}", f"whole_llc_mshr_hit_diff_cpu_id_{tag}",
            f"llc_mshr_full_stall_{tag}"
        ]
    writer.writerow(header)

    # Process each file
    for filename in filenames:
        stripped_name = filename.replace(prefix_to_strip, "")
        row = [stripped_name]

        for dir_path in dirs:
            full_path = os.path.join(dir_path, filename)
            if os.path.exists(full_path):
                ipc, instructions, cycles, llc_mshr_merging, mshr_hit_diff, mshr_full_stall = extract_stats(full_path)
            else:
                ipc = instructions = cycles = llc_mshr_merging = mshr_hit_diff = mshr_full_stall = "N/A"

            row += [ipc, instructions, cycles, llc_mshr_merging, mshr_hit_diff, mshr_full_stall]

        writer.writerow(row)

print("✅ Side-by-side comparison saved to 'comparison_results_side_by_side.csv'")
