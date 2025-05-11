import os
import re
import csv

# List of directories to compare
dirs = [
    "/Users/jarvisjia/Documents/2025_spring/cs7292/champsim/champsim/results_1core_20M",
    "/Users/jarvisjia/Documents/2025_spring/cs7292/champsim/champsim_2/champsim/results_1core_20M",
    "/Users/jarvisjia/Documents/2025_spring/cs7292/champsim/champsim_baseline/champsim/results_1core_20M"
]

# Extract stats from a single file
def extract_stats(filepath):
    ipc = instructions = cycles = llc_mshr_merging = None

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

    return ipc, instructions, cycles, llc_mshr_merging

# Collect all filenames from the first directory
filenames = [f for f in os.listdir(dirs[0]) if os.path.isfile(os.path.join(dirs[0], f))]

# Write to CSV
with open("comparison_results.csv", mode='w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["filename", "directory", "ipc", "instructions", "cycles", "llc_mshr_merging"])

    for filename in filenames:
        for dir_path in dirs:
            full_path = os.path.join(dir_path, filename)
            if not os.path.exists(full_path):
                writer.writerow([filename, dir_path, "N/A", "N/A", "N/A", "N/A"])
                continue

            ipc, instructions, cycles, llc_mshr_merging = extract_stats(full_path)
            writer.writerow([filename, dir_path, ipc, instructions, cycles, llc_mshr_merging])

print("✅ Comparison saved to 'comparison_results.csv'")
