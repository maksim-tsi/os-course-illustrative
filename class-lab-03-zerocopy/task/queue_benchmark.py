import time
import multiprocessing
import resource
import sys
import threading
import numpy as np

# --- Guardrails ---
# Limit memory to ~1.2GB to prevent accidental OOM crashes during the lab
GB = 1024 * 1024 * 1024
try:
    resource.setrlimit(resource.RLIMIT_AS, (int(1.2 * GB), int(1.2 * GB)))
except ValueError:
    pass # macOS might restrict this, ignore if it fails

# --- Helper ---
def progress_spinner(stop_event):
    """A simple background thread to show the system is busy (blocking)."""
    spinner = ['|', '/', '-', '\\']
    i = 0
    while not stop_event.is_set():
        sys.stdout.write(f"\r[System] Pickling and transferring 500MB array... {spinner[i % 4]}")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.write("\r[System] Transfer complete!                           \n")

def producer(q):
    """
    Producer: Generates a massive 500MB NumPy array and sends it via Queue.
    """
    print("[Producer] Generating 500MB NumPy array...")
    # Generate 500MB array (approx 62.5 million 64-bit floats)
    data = np.ones(62500000, dtype=np.float64)
    print(f"[Producer] Array generated. Size in memory: {data.nbytes / (1024**2):.2f} MB")
    
    # TODO: Put the data into the queue.
    # Notice how the program "hangs" here. This is the Pickle Penalty!
    pass

def consumer(q):
    """
    Consumer: Receives the array from the Queue.
    """
    print("[Consumer] Waiting for data from Producer...")
    
    # TODO: Get the data from the queue.
    pass

if __name__ == '__main__':
    print("=== IPC Queue Benchmark (The Pickle Penalty) ===")
    
    # TODO: Create a multiprocessing.Queue
    q = None
    
    # TODO: Create Producer and Consumer processes
    # producer_process = multiprocessing.Process(target=producer, args=(q,))
    # consumer_process = multiprocessing.Process(target=consumer, args=(q,))
    
    print("[Main] Starting processes...")
    start_time = time.time()
    
    # Start the visual spinner to show the blocking behavior
    spinner_stop = threading.Event()
    spinner_thread = threading.Thread(target=progress_spinner, args=(spinner_stop,))
    spinner_thread.start()
    
    # TODO: Start the processes
    
    # TODO: Join the processes
    
    # Stop the spinner
    spinner_stop.set()
    spinner_thread.join()
    
    end_time = time.time()
    
    print(f"\n[Result] Total time taken: {end_time - start_time:.2f} seconds")
    print("[Notice] Did you see the delay? That's the CPU struggling to serialize (pickle)")
    print("         and deserialize 500MB of data through a standard pipe.")
