#!/bin/bash

# Check if running in WSL
if grep -qEi "(Microsoft|WSL)" /proc/version &> /dev/null; then
    echo "Running in WSL environment."
else
    echo "This script is intended to run inside WSL. Exiting."
    exit 1
fi

# Define the target CPU utilization percentage
TARGET_CPU_UTILIZATION=75  # Adjust this value based on your performance goals

# Function to display CPU utilization using /proc/stat
function get_cpu_usage() {
    # Read CPU statistics from /proc/stat
    read cpu user nice system idle iowait irq softirq steal guest guest_nice < /proc/stat
    cpu_idle="$idle"
    cpu_total=$((user + nice + system + idle + iowait + irq + softirq + steal))
    echo "$cpu_idle $cpu_total"
}

# Function to calculate CPU usage percentage
function calculate_cpu_usage() {
    local prev_idle=$1
    local prev_total=$2
    local curr_idle=$3
    local curr_total=$4

    local diff_idle=$((curr_idle - prev_idle))
    local diff_total=$((curr_total - prev_total))
    local cpu_usage=$((100 * (diff_total - diff_idle) / diff_total))
    echo "$cpu_usage"
}

# Function to run a dummy CPU-intensive task to simulate load
function simulate_load() {
    local threads=$1
    echo "Running test with $threads threads..."
    
    # Create a background job for each thread to generate CPU load
    for ((i=1; i<=threads; i++)); do
        (while : ; do : ; done) &
    done

    # Let the threads run for a few seconds to simulate workload
    sleep 3
}

# Function to stop all background jobs (cleanup)
function stop_all_jobs() {
    kill $(jobs -p) &> /dev/null
}

# Function to set environment variables persistently in ~/.bashrc
function set_environment_variables() {
    local threads=$1
    echo "Setting environment variables for $threads threads..."

    # Set environment variables for the current session
    export OMP_NUM_THREADS=$threads
    export MKL_NUM_THREADS=$threads
    export NUMEXPR_NUM_THREADS=$threads
    export NUMEXPR_MAX_THREADS=$threads

    # Persist environment variables in ~/.bashrc for future sessions
    sed -i '/^export OMP_NUM_THREADS/d' ~/.bashrc
    sed -i '/^export MKL_NUM_THREADS/d' ~/.bashrc
    sed -i '/^export NUMEXPR_NUM_THREADS/d' ~/.bashrc
    sed -i '/^export NUMEXPR_MAX_THREADS/d' ~/.bashrc
    echo "export OMP_NUM_THREADS=$threads" >> ~/.bashrc
    echo "export MKL_NUM_THREADS=$threads" >> ~/.bashrc
    echo "export NUMEXPR_NUM_THREADS=$threads" >> ~/.bashrc
    echo "export NUMEXPR_MAX_THREADS=$threads" >> ~/.bashrc

    # Display the current session settings
    echo "Environment Variables Set:"
    echo "OMP_NUM_THREADS=$OMP_NUM_THREADS"
    echo "MKL_NUM_THREADS=$MKL_NUM_THREADS"
    echo "NUMEXPR_NUM_THREADS=$NUMEXPR_NUM_THREADS"
    echo "NUMEXPR_MAX_THREADS=$NUMEXPR_MAX_THREADS"
}

# Main script logic to optimize thread count based on target CPU utilization
echo "Starting Ollama optimization script..."
echo "Target CPU Utilization: $TARGET_CPU_UTILIZATION%"
echo "Detected $(nproc) total cores."

# Record baseline CPU usage before running any load
read prev_idle prev_total < <(get_cpu_usage)
echo "Baseline CPU usage recorded."

# Start with a low number of threads and gradually increase until target CPU utilization is reached
optimal_threads=4
step_size=2

while [ $optimal_threads -le $(nproc) ]; do
    echo "Testing with $optimal_threads threads..."

    # Run a test load with the current number of threads
    simulate_load $optimal_threads

    # Capture CPU usage after the test
    read curr_idle curr_total < <(get_cpu_usage)

    # Calculate CPU usage percentage
    cpu_usage=$(calculate_cpu_usage $prev_idle $prev_total $curr_idle $curr_total)

    # Output CPU usage results
    echo "CPU Usage with $optimal_threads threads: $cpu_usage%"

    # Check if the current CPU usage is close to the target
    if [ $cpu_usage -ge $((TARGET_CPU_UTILIZATION - 5)) ] && [ $cpu_usage -le $((TARGET_CPU_UTILIZATION + 5)) ]; then
        echo "Optimal thread count found: $optimal_threads threads with $cpu_usage% CPU usage."
        break
    fi

    # Increase the number of threads for the next iteration
    optimal_threads=$((optimal_threads + step_size))

    # Store baseline for next comparison
    prev_idle=$curr_idle
    prev_total=$curr_total

    # Stop current load before starting a new one
    stop_all_jobs
done

# Cleanup after finding optimal thread count
stop_all_jobs

# Set and persist the environment variables for the optimal thread count
set_environment_variables $optimal_threads

echo "Optimization completed. Optimal threads: $optimal_threads."
echo "To apply these settings in a new terminal session, run: source ~/.bashrc"
