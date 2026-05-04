"""
Educational Lab: Operating Systems - Process Management & Signals
This script acts as the "Manager" process. It spawns a worker process and
demonstrates how to gracefully handle signals (like Ctrl+C) to terminate
child processes, with a fallback to forceful termination (SIGKILL) if the
child becomes unresponsive.
"""

import os
import signal
import subprocess
import time
import sys

# Hardcoded absolute timeout to prevent the script from running forever
# This acts as a guardrail in case the lab is left running in a Codespace.
ABSOLUTE_TIMEOUT = 60

# Global process variable so it can be accessed inside signal handlers
worker_process = None

def handle_sigint(signum, frame):
    """
    Signal handler for SIGINT (Ctrl+C).
    """
    print("\nManager: Caught SIGINT (Ctrl+C). Initiating graceful shutdown...")
    
    if worker_process:
        # Step 2: Politely send SIGTERM to the child process using os.kill.
        print(f"Manager: Sending SIGTERM to worker PID {worker_process.pid}...")
        try:
            os.kill(worker_process.pid, signal.SIGTERM)
        except ProcessLookupError:
            print("Manager: Worker process already exited.")
        
        # Step 3: Wait for the process to exit using worker_process.wait(timeout=2). 
        # If it throws subprocess.TimeoutExpired, forcefully send SIGKILL.
        try:
            print("Manager: Waiting for worker to exit...")
            worker_process.wait(timeout=2)
            print("Manager: Worker exited cleanly.")
        except subprocess.TimeoutExpired:
            print("Manager: Worker did not exit in time! It might be hallucinating (deadlocked).")
            print(f"Manager: Sending SIGKILL to forcefully terminate worker PID {worker_process.pid}...")
            try:
                os.kill(worker_process.pid, signal.SIGKILL)
                print("Manager: Worker forcefully terminated.")
            except ProcessLookupError:
                pass
    
    print("Manager: Shutdown complete. Exiting.")
    sys.exit(0)

def main():
    global worker_process
    print(f"Manager [PID {os.getpid()}]: Starting up...")

    # Step 1: Spawn dummy_ai_worker.py in the background using subprocess.Popen and get its PID.
    worker_process = subprocess.Popen(["python3", "dummy_ai_worker.py"])
    print(f"Manager: Spawned worker with PID {worker_process.pid}")

    # Register the SIGINT handler
    signal.signal(signal.SIGINT, handle_sigint)

    print(f"Manager: Running. Press Ctrl+C to stop. Hard timeout in {ABSOLUTE_TIMEOUT} seconds.")
    start_time = time.time()

    # Main loop - waiting for the absolute timeout or a manual interrupt
    while True:
        if time.time() - start_time > ABSOLUTE_TIMEOUT:
            print("Manager: Absolute timeout reached. Forcibly terminating worker.")
            # Guardrail: Forcefully kill the child process if the timeout is reached
            if worker_process:
                worker_process.kill()
            break
        time.sleep(1)
        
    print("Manager: Exiting due to timeout.")

if __name__ == "__main__":
    main()
