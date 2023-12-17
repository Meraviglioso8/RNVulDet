import subprocess
import time

def run_script(file_path):
    start = time.process_time()
    subprocess.run(["python3", file_path])
    end = time.process_time()
    return end - start

def main():
    file_path = './count.py'  # Replace with your file path
    num_runs = 100
    total_time = 0

    for _ in range(num_runs):
        total_time += run_script(file_path)
        print(total_time)

    avg_time = total_time / num_runs
    print(f"Average CPU run time over {num_runs} runs: {avg_time} seconds")

if __name__ == "__main__":
    main()
