/*
 * SEGFAULT COMPUTER - Computation via memory faults and signal handlers
 * 
 * This demonstrates computation without traditional C execution flow.
 * All logic happens in signal handlers responding to deliberate segfaults.
 * 
 * Architecture:
 * - Memory pages represent "cells" with read/write/execute permissions as state
 * - SIGSEGV handler implements the computational logic
 * - Program counter advances by deliberately faulting on next instruction address
 * - No loops, no conditionals in main execution path - only faults!
 */

#define _GNU_SOURCE
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <unistd.h>
#include <setjmp.h>
#include <errno.h>

// Our "computer" state
static void* computation_memory;
static size_t page_size;
static int computation_result = 0;
static volatile int operation_phase = 0;
static sigjmp_buf fault_return;
static volatile sig_atomic_t in_handler = 0;

// Computation cells (each is a memory page)
#define NUM_CELLS 8
#define CELL_A 0
#define CELL_B 1
#define CELL_RESULT 2
#define CELL_COUNTER 3
#define CELL_TEMP 4

// Get address of computation cell
static void* cell_addr(int cell) {
    return computation_memory + (cell * page_size);
}

// The SIGSEGV handler - this is our CPU!
static void segfault_cpu(int sig, siginfo_t *si, void *unused) {
    // Prevent recursive faults
    if (in_handler) {
        _exit(1);
    }
    in_handler = 1;
    
    void* fault_addr = si->si_addr;
    
    // Determine which cell faulted (if it's one of ours)
    long offset = (char*)fault_addr - (char*)computation_memory;
    if (offset < 0 || offset >= page_size * NUM_CELLS) {
        // Not our fault!
        in_handler = 0;
        _exit(1);
    }
    
    int cell_id = offset / page_size;
    
    printf("[SEGFAULT CPU] Fault on cell %d, phase %d\n", cell_id, operation_phase);
    
    // State machine for different computation phases
    switch(operation_phase) {
        case 0: // Initialize computation
            printf("[SEGFAULT CPU] Initializing computation...\n");
            
            // First make cells writable so we can initialize them
            if (mprotect(cell_addr(CELL_A), page_size, PROT_READ | PROT_WRITE) != 0) {
                perror("mprotect A");
                _exit(1);
            }
            *(int*)cell_addr(CELL_A) = 7;
            mprotect(cell_addr(CELL_A), page_size, PROT_READ); // Now read-only
            
            if (mprotect(cell_addr(CELL_B), page_size, PROT_READ | PROT_WRITE) != 0) {
                perror("mprotect B");
                _exit(1);
            }
            *(int*)cell_addr(CELL_B) = 5;
            mprotect(cell_addr(CELL_B), page_size, PROT_READ); // Now read-only
            
            operation_phase = 1;
            break;
            
        case 1: // Read A
            if (cell_id == CELL_A) {
                // Make it readable temporarily
                mprotect(cell_addr(CELL_A), page_size, PROT_READ);
                computation_result = *(int*)cell_addr(CELL_A);
                printf("[SEGFAULT CPU] Read A = %d\n", computation_result);
                
                // Protect it again
                mprotect(cell_addr(CELL_A), page_size, PROT_NONE);
                operation_phase = 2;
            }
            break;
            
        case 2: // Read B and compute
            if (cell_id == CELL_B) {
                // Make it readable temporarily
                mprotect(cell_addr(CELL_B), page_size, PROT_READ);
                int b_value = *(int*)cell_addr(CELL_B);
                printf("[SEGFAULT CPU] Read B = %d\n", b_value);
                
                // COMPUTE: A * B
                computation_result *= b_value;
                printf("[SEGFAULT CPU] Computed A * B = %d\n", computation_result);
                
                // Protect B again
                mprotect(cell_addr(CELL_B), page_size, PROT_NONE);
                operation_phase = 3;
            }
            break;
            
        case 3: // Write result
            if (cell_id == CELL_RESULT) {
                printf("[SEGFAULT CPU] Writing result = %d\n", computation_result);
                
                // Make writable, write, then make read-only
                mprotect(cell_addr(CELL_RESULT), page_size, PROT_READ | PROT_WRITE);
                *(int*)cell_addr(CELL_RESULT) = computation_result;
                mprotect(cell_addr(CELL_RESULT), page_size, PROT_READ);
                
                operation_phase = 4;
            }
            break;
            
        case 4: // Verify result
            if (cell_id == CELL_RESULT) {
                // Already readable from previous phase
                int final_result = *(int*)cell_addr(CELL_RESULT);
                printf("[SEGFAULT CPU] Computation complete! Result = %d\n", final_result);
                operation_phase = 5;
            }
            break;
            
        default:
            // Done
            break;
    }
    
    in_handler = 0;
    siglongjmp(fault_return, 1);
}

// Trigger a fault on purpose by trying to access protected memory
static void fault_on(int cell) {
    if (sigsetjmp(fault_return, 1) == 0) {
        // Try to read - this WILL segfault if protected
        volatile int dummy = *(volatile int*)cell_addr(cell);
        
        // If read worked, try write to force fault
        *(volatile int*)cell_addr(cell) = 0;
    }
}

int main() {
    printf("=== SEGFAULT COMPUTER ===\n");
    printf("Computing 7 * 5 using only memory faults and signal handlers\n\n");
    
    // Setup
    page_size = sysconf(_SC_PAGE_SIZE);
    
    // Allocate computation memory (aligned to page boundary)
    computation_memory = mmap(NULL, page_size * NUM_CELLS, 
                             PROT_NONE,  // Start with no access!
                             MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    
    if (computation_memory == MAP_FAILED) {
        perror("mmap");
        return 1;
    }
    
    // Install our SIGSEGV handler - this is our CPU!
    struct sigaction sa;
    memset(&sa, 0, sizeof(sa));
    sa.sa_flags = SA_SIGINFO;
    sigemptyset(&sa.sa_mask);
    sa.sa_sigaction = segfault_cpu;
    
    if (sigaction(SIGSEGV, &sa, NULL) == -1) {
        perror("sigaction");
        return 1;
    }
    
    printf("Memory mapped at %p\n", computation_memory);
    printf("Page size: %zu bytes\n", page_size);
    printf("Starting computation...\n\n");
    
    // THE ENTIRE COMPUTATION HAPPENS VIA SEGFAULTS!
    // Each fault_on() triggers our signal handler which advances the computation
    
    // Phase 0: Initialize by faulting on any cell
    fault_on(CELL_A);
    
    // Phase 1: Read A (fault because it's protected after init)
    mprotect(cell_addr(CELL_A), page_size, PROT_NONE);
    fault_on(CELL_A);
    
    // Phase 2: Read B and compute (fault because it's protected)
    mprotect(cell_addr(CELL_B), page_size, PROT_NONE);
    fault_on(CELL_B);
    
    // Phase 3: Write result (fault because it's not writable)
    fault_on(CELL_RESULT);
    
    // Phase 4: Verify result (no fault - it's readable)
    fault_on(CELL_RESULT);
    
    printf("\n=== COMPUTATION COMPLETE ===\n");
    
    // Final check - result should be readable
    if (operation_phase >= 4) {
        int final = *(int*)cell_addr(CELL_RESULT);
        printf("Final result in memory: %d (should be 35)\n", final);
        printf("All computation performed in signal handlers!\n");
    }
    
    // Cleanup
    munmap(computation_memory, page_size * NUM_CELLS);
    
    return 0;
}
