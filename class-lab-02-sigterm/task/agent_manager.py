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
    
    # TODO Step 2: Politely send SIGTERM to the child process using os.kill.
    # Hint: os.kill(worker_process.pid, signal.SIGTERM)
    
    # TODO Step 3: Wait for the process to exit using worker_process.wait(timeout=2). 
    # If it throws subprocess.TimeoutExpired, forcefully send SIGKILL.
    # Hint: Use a try/except block. In the except block, use os.kill(..., signal.SIGKILL)
    
    print("Manager: Shutdown complete. Exiting.")
    sys.exit(0)

def main():
    global worker_process
    print(f"Manager [PID {os.getpid()}]: Starting up...")

    # TODO Step 1: Spawn dummy_ai_worker.py in the background using subprocess.Popen and get its PID.
    # Hint: worker_process = subprocess.Popen(["python3", "dummy_ai_worker.py"])
    # print(f"Manager: Spawned worker with PID {worker_process.pid}")

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
