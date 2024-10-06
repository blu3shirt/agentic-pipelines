import os
from datetime import datetime

def read_seed_file(file_path="seed.txt"):
    """Reads the seed file and returns the content."""
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return file.read().strip()
    else:
        raise FileNotFoundError(f"Seed file '{file_path}' not found.")

def save_output_to_log(output, log_dir="logs"):
    """Saves the given output to a timestamped .txt file in the specified directory."""
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)  # Create logs directory if not exists
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"output_log_{timestamp}.txt")
    with open(log_file, "w") as file:
        file.write(output)
    print(f"Output saved to: {log_file}")
    return log_file
