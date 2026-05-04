import time
import multiprocessing
from multiprocessing import shared_memory
import resource
import numpy as np

# --- Guardrails ---
# Limit memory to ~1.2GB to prevent accidental OOM crashes
GB = 1024 * 1024 * 1024
try:
    resource.setrlimit(resource.RLIMIT_AS, (int(1.2 * GB), int(1.2 * GB)))
except ValueError:
    pass # macOS might restrict this, ignore if it fails

def producer(shm_name, sync_event, shape, dtype):
    """
    Producer: Maps shared memory, creates a NumPy array backed by it, and fills it.
    """
    print(f"[Producer] Attaching to shared memory block: {shm_name}")
    # TODO Step 3a: Attach to the existing shared memory block using shared_memory.SharedMemory
    # existing_shm = ...
    
    try:
        # TODO Step 3b: Create a NumPy array backed by the shared memory buffer
        # data = np.ndarray(shape, dtype=dtype, buffer=existing_shm.buf)
        
        print("[Producer] Filling 500MB array directly in shared memory...")
        # Fill the array with ones
        # data[:] = 1.0
        
        print("[Producer] Data is ready. Signaling Consumer.")
        # TODO Step 3c: Set the event to signal the Consumer
        # sync_event.set()
        
    finally:
        # Close the local handle to the shared memory block
        # existing_shm.close()
        pass

def consumer(shm_name, sync_event, shape, dtype):
    """
    Consumer: Waits for the signal, then maps the shared memory to read the array.
    """
    print("[Consumer] Waiting for Producer to finish writing (Traffic Light)...")
    # TODO Step 4a: Wait for the sync_event with a 15-second timeout (Guardrail against deadlocks)
    # sync_event.wait(timeout=15)
    
    print(f"[Consumer] Signal received! Attaching to shared memory: {shm_name}")
    # TODO Step 4b: Attach to the shared memory block
    # existing_shm = ...
    
    try:
        # TODO Step 4c: Create a NumPy array backed by the shared memory buffer
        # data = np.ndarray(shape, dtype=dtype, buffer=existing_shm.buf)
        
        # Verify data
        # print(f"[Consumer] Successfully read array. First element: {data[0]}, Last element: {data[-1]}")
        pass
    finally:
        # Close the local handle to the shared memory block
        # existing_shm.close()
        pass

if __name__ == '__main__':
    print("=== Zero-Copy IPC Benchmark (Shared Memory) ===")
    
    # 500MB array (approx 62.5 million 64-bit floats)
    elements = 62500000
    shape = (elements,)
    dtype = np.float64
    bytes_required = elements * np.dtype(dtype).itemsize
    
    print(f"[Main] Requesting {bytes_required / (1024**2):.2f} MB of Shared Memory from OS...")
    
    # TODO Step 1: Create a multiprocessing.shared_memory.SharedMemory block of 500MB.
    # Give it a unique name (or let the OS assign one) and specify `create=True` and `size=bytes_required`
    # shm = ...
    
    # CRITICAL: We use try...finally to ensure cleanup. 
    # Without this, if the script crashes, the OS will permanently leak 500MB of RAM!
    try:
        # TODO Step 2: Create a multiprocessing.Event for synchronization.
        # sync_event = ...
        
        # print(f"[Main] Shared Memory allocated: {shm.name}")
        
        # TODO: Create Producer and Consumer processes, passing shm.name, sync_event, shape, and dtype
        
        print("[Main] Starting processes...")
        start_time = time.time()
        
        # TODO: Start the processes
        
        # TODO: Join the processes
        
        end_time = time.time()
        print(f"\n[Result] Total time taken: {end_time - start_time:.4f} seconds")
        print("[Notice] Look at that speed! No pickling, no serialization overhead.")
        
    finally:
        print("\n[Main] Performing CRITICAL cleanup of Shared Memory...")
        # CRITICAL GUARDRAIL: Close the local handle and unlink (delete) the block from the OS
        # shm.close()
        # shm.unlink()
