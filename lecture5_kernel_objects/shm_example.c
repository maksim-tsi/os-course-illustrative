#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <sys/shm.h>
#include <sys/stat.h>
#include <sys/mman.h>
#include <unistd.h>

int main() {
    const char *name = "/os_lecture_shm";
    const int SIZE = 4096; // Size of the shared memory object
    int shm_fd;
    void *ptr;

    // 1. Create the Shared Memory Kernel Object
    // shm_open returns a file descriptor for the shared memory object.
    shm_fd = shm_open(name, O_CREAT | O_RDWR, 0666);
    if (shm_fd == -1) {
        perror("shm_open");
        exit(EXIT_FAILURE);
    }

    // Configure the size of the shared memory object.
    if (ftruncate(shm_fd, SIZE) == -1) {
        perror("ftruncate");
        shm_unlink(name); // Cleanup if this fails
        exit(EXIT_FAILURE);
    }

    // 2. Map the kernel object into our process's address space.
    // This gives us a pointer we can use directly.
    ptr = mmap(0, SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, shm_fd, 0);
    if (ptr == MAP_FAILED) {
        perror("mmap");
        exit(EXIT_FAILURE);
    }

    printf("Shared memory created. Writing data directly to memory...\n");
    // Write to the shared memory region just like normal RAM.
    sprintf(ptr, "Linux Kernel Objects are powerful!");

    printf("Data written: '%s'\n", (char *)ptr);

    // 3. Cleanup handles and objects
    // Unmap the memory from our address space.
    munmap(ptr, SIZE);
    // Close the file descriptor.
    close(shm_fd);
    // Mark the shared memory object for destruction.
    // If we didn't do this, it would persist in the OS until reboot!
    shm_unlink(name);

    printf("Shared memory object removed.\n");
    return 0;
}