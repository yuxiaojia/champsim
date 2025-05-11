import os
import subprocess

trace_dir = 'traces'
command_template = './run_1core.sh perceptron-no-no-no-lru-1core 1 80 0 {0}'

if os.path.exists(trace_dir) and os.path.isdir(trace_dir):
    trace_files = [f for f in os.listdir(trace_dir) if os.path.isfile(os.path.join(trace_dir, f))]
    for trace_file in trace_files:
        command = command_template.format(trace_file)
        print(f"Executing: {command}")
        subprocess.run(command, shell=True)
else:
    print(f"Directory {trace_dir} does not exist or is not a directory.")