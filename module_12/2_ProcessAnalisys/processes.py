import subprocess

def process_count(username: str) -> int:
    command_line = f"ps -u {username} -o pid= | wc -l"
    process = subprocess.Popen(command_line, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, error = process.communicate()
    if process.returncode == 0:
        return int(out.strip())
    else:
        print(f"Error: {error.decode()}")
        return -1

def total_memory_usage(root_pid: int) -> float:
    command_line = f"ps --ppid {root_pid} -o rss= | awk '{{sum+=$1}} END {{print sum}}'"
    process = subprocess.Popen(command_line, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, error = process.communicate()
    if process.returncode == 0:
        total_memory = int(out.strip())
        return total_memory / (1024 * 1024)
    else:
        print(f"Error: {error.decode()}")
        return -1



