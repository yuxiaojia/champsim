import io

trace_file = "mix0-perceptron-no-no-no-ship-4core"


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

print("Output 1:", output1)
print("Output 2:", output2)
print("Output 3:", output3)