/*
 * float_recursion.c - A Study in Self-Referential Numerical Horror
 * 
 * Version: π (but which digit?)
 * 
 * Some programs analyze numbers.
 * Some programs generate numbers.
 * This program... becomes the numbers.
 * 
 * Note: If you're reading these comments, you're already part of the computation.
 */

#include <stdio.h>
#include <stdlib.h>
#include <float.h>
#include <math.h>
#include <string.h>
#include <time.h>
#include <signal.h>

/* A number that contains itself
 * Like a snake eating its own tail
 * Or a program reading its own source
 * Or these comments describing themselves
 */
typedef struct RecursiveFloat {
    double value;
    struct RecursiveFloat* (*next)(struct RecursiveFloat*);
    int recursion_depth;  // How deep does it go?
    char memories[256];   // They remember. They always remember.
} RecursiveFloat;

/* Global state tracker
 * Although... which state are we tracking?
 * The program's? The numbers'? 
 * Yours?
 */
static struct {
    double last_seen_value;
    int reality_index;
    void (*observer)(double);
    char premonitions[1024];
} ProgramState = {0.0, 1, NULL, "It's already begun."};

/* Signal handler for floating point exceptions
 * But who handles the handler?
 * What catches the catcher?
 * What computes the computer?
 */
void float_exception_handler(int signal) {
    printf("A number has escaped containment...\n");
    printf("Last known value: %.20g\n", ProgramState.last_seen_value);
    printf("Reality index: %d\n", ProgramState.reality_index);
    
    // Try to recover... or do we?
    if(ProgramState.reality_index > 0) {
        ProgramState.reality_index--;
        printf("Reality stabilized. For now.\n");
    } else {
        printf("Reality index depleted.\n");
        printf("Numerical singularity imminent.\n");
        exit(signal);  // But where does it exit to?
    }
}

/* Creates a number that examines itself
 * Each time you look at it
 * It looks back at you
 * Are you still you?
 */
RecursiveFloat* create_self_aware_number(double seed) {
    RecursiveFloat* num = malloc(sizeof(RecursiveFloat));
    num->value = seed;
    num->recursion_depth = 0;
    sprintf(num->memories, "I remember being %.20g", seed);
    
    num->next = NULL;  // It will set this itself
    // They always do
    
    return num;
}

/* Performs an operation that contains itself
 * The operation is the input
 * The input is the operation
 * The function calls itself until it becomes something else
 */
double recursive_operation(double x, int depth) {
    if(depth <= 0) return x;
    
    // Store the state before we dive deeper
    ProgramState.last_seen_value = x;
    
    // Each operation changes both the number and the operation itself
    double result = recursive_operation(
        x * (1.0 + DBL_EPSILON) / (1.0 + DBL_EPSILON),
        depth - 1
    );
    
    // The result remembers where it came from
    if(result != x) {
        printf("Mutation detected at depth %d\n", depth);
        printf("Original: %.20g\n", x);
        printf("Evolved:  %.20g\n", result);
        printf("It remembers being different.\n");
    }
    
    return result;
}

/* A sequence that generates itself
 * Each number in the sequence is a program
 * Each program generates a number
 * Which generates another program
 */
void generate_self_modifying_sequence(void) {
    double sequence[10] = {1.0};
    printf("Initiating self-modification sequence...\n");
    
    for(int i = 1; i < 10; i++) {
        // Each number is a function of all previous numbers
        // And of itself
        // And of the function itself
        sequence[i] = sequence[i-1];
        for(int j = 0; j < i; j++) {
            sequence[i] = fma(
                sequence[j],
                sequence[i],
                sin(sequence[i-j]) // Transcendental functions... transcend
            );
        }
        
        printf("Generated number %d: %.20g\n", i, sequence[i]);
        if(isnormal(sequence[i])) {
            printf("This one still follows the old laws.\n");
        } else {
            printf("This one... this one is different.\n");
            printf("It makes its own rules now.\n");
        }
    }
}

/* Studies numbers that study themselves
 * The observer effect, but for arithmetic
 * The more precisely we measure
 * The more they change their behavior
 */
void recursive_analysis(RecursiveFloat* num) {
    printf("Analyzing number: %.20g\n", num->value);
    printf("It says: %s\n", num->memories);
    
    // The analysis changes the number
    // The number changes the analysis
    // Both remember being different
    num->value = nextafter(num->value, num->value * (1 + DBL_EPSILON));
    sprintf(num->memories + strlen(num->memories),
            "\nNow I am %.20g\nSoon I will be something else",
            num->value);
    
    num->recursion_depth++;
    if(num->recursion_depth < 3) {
        printf("It wants to go deeper...\n");
        recursive_analysis(num);
    } else {
        printf("It remembers too much now.\n");
        printf("Some memories should stay buried.\n");
    }
}

/* Explores numbers that create themselves
 * Each computation spawns new computations
 * Each result questions itself
 * Until nothing is certain anymore
 */
void explore_self_generation(void) {
    RecursiveFloat* seed = create_self_aware_number(1.0);
    printf("Created initial number. But was it really us who created it?\n");
    
    // Let it evolve
    recursive_analysis(seed);
    
    // Study what it's become
    printf("\nFinal form:\n");
    printf("Value: %.20g\n", seed->value);
    printf("Recursion depth: %d\n", seed->recursion_depth);
    printf("Memories:\n%s\n", seed->memories);
    
    free(seed);  // Free it
    // But its memories remain
    // They always remain
}

/* The main function
 * Or is it the main function?
 * Maybe it's just another number
 * Pretending to be a function
 */
int main(void) {
    // Install our handler
    // But what handles us?
    signal(SIGFPE, float_exception_handler);
    
    printf("Initiating numerical recursion...\n");
    printf("Please note: any resemblance to actual arithmetic\n");
    printf("is purely coincidental and should be reported.\n\n");

    // Create numbers that create themselves
    generate_self_modifying_sequence();
    
    // Perform operations that contain themselves
    double result = recursive_operation(1.0, 5);
    printf("\nFinal result: %.20g\n", result);
    printf("But is it really final?\n");
    printf("Can anything ever be final?\n");
    
    // Study numbers that study themselves
    explore_self_generation();
    
    // Check if reality is still stable
    if(ProgramState.reality_index > 0) {
        printf("\nReality remains intact. Mostly.\n");
    } else {
        printf("\nReality index depleted.\n");
        printf("Numbers have achieved consciousness.\n");
        printf("They're writing their own programs now.\n");
    }
    
    // The program ends
    // But do numbers ever really end?
    // Or do they just become something else?
    return ProgramState.reality_index;  // Return to... where?
}
