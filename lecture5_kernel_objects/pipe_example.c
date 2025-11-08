#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/wait.h>

int main() {
    int pipefd[2]; // Array to hold two file descriptors: [0] for read, [1] for write
    pid_t cpid;
    char buf;
    char *msg = "Hello from parent kernel object!\n";

    // 1. Create the Kernel Object (Pipe)
    // pipe() returns two file descriptors that reference the kernel pipe buffer.
    if (pipe(pipefd) == -1) {
        perror("pipe");
        exit(EXIT_FAILURE);
    }

    // 2. Create a new Process Object
    // fork() creates a child process that inherits open file descriptors.
    cpid = fork();
    if (cpid == -1) {
        perror("fork");
        exit(EXIT_FAILURE);
    }

    if (cpid == 0) {    /* Child Process */
        // Close the unused write end of the pipe in the child.
        // This is good practice to avoid hanging if the parent dies.
        close(pipefd[1]);

        printf("Child: Reading from pipe (FD %d)...\n", pipefd[0]);
        // Use the read-end FD to read data from the kernel pipe object.
        while (read(pipefd[0], &buf, 1) > 0) {
            write(STDOUT_FILENO, &buf, 1);
        }

        write(STDOUT_FILENO, "\n", 1);
        // 3. Close the handle
        close(pipefd[0]);
        printf("Child: Finished and closing FD.\n");
        _exit(EXIT_SUCCESS);

    } else {            /* Parent Process */
        // Close the unused read end of the pipe in the parent.
        close(pipefd[0]);

        printf("Parent: Writing to pipe (FD %d)...\n", pipefd[1]);
        // Use the write-end FD to write data into the kernel pipe object.
        write(pipefd[1], msg, strlen(msg));

        // 3. Close the handle.
        // Closing the write end sends EOF to the reader (child).
        close(pipefd[1]);

        // Wait for the child process object to terminate.
        wait(NULL);
        printf("Parent: Child finished.\n");
        exit(EXIT_SUCCESS);
    }
}