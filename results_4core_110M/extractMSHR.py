import os

def process_trace_file(trace_file, output_filename):
    output1 = ""
    output2 = ""
    output3 = ""
    try:
        with open(trace_file + ".txt", "r") as f:
            lines = f.readlines()
            core_number = 0
            for line in lines:
                if line.startswith('LLC mshr merging'):
                    output1 += f'Core {core_number} LLC mshr merging:  {line.split()[-1]}\n'
                    core_number += 1
                if line.startswith(f"Core_{core_number}_LLC_total_miss"):
                    output2 += f'Core {core_number} LLC total miss:  {line.split()[-1]}\n'
                if line.startswith(f"CPU {core_number} cumulative IPC:"):
                    output3 += line
                    
    except FileNotFoundError:
        print(f"File not found: {trace_file}.txt")
        return
    
    final_output = output1 + output2 + output3
    with open(output_filename, "a") as f:   # append ('a') instead of overwrite ('w')
        f.write("TRACE FILE: " + trace_file + "\n")
        f.write(final_output)
        f.write("\n\n")   # for spacing between files
        f.flush()

# Main driver
output_filename = "output.txt"

# Clear output file at the beginning
open(output_filename, 'w').close()

meep = sorted(os.listdir('.'))
for filename in meep:
    if filename.endswith('.txt') and not filename.startswith('output'):
        process_trace_file(filename[:-4], output_filename)
        print(f"Processed {filename}")
    else:
        print(f"Skipped {filename}")
