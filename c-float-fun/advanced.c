/*
 * float_horrors_advanced.c - Further Studies in Numerical Approximation
 * 
 * A friendly continuation of our floating point exploration!
 * You know, it's funny... the more you study these numbers,
 * the more they seem to study you back.
 *
 * Yesterday, I could have sworn my calculator displayed
 * different results when I wasn't looking directly at it.
 * Probably just a rounding error. Nothing to worry about.
 */

#include <stdio.h>
#include <stdlib.h>
#include <float.h>
#include <math.h>
#include <string.h>
#include <time.h>

/* Track our experiments with care.
 * Sometimes I wonder if the numbers keep track of us too.
 * In their own special way.
 */
typedef struct {
    double value;
    char observation[512];
    int stability_index;  // How stable is this number? Are any of them truly stable?
    void (*behavior)(double);  // What does it do when we're not watching?
} FloatExperiment;

/* Generates a sequence that should sum to 1.
 * Should. Funny word, "should."
 * Like saying the sun should rise tomorrow.
 * It probably will. Probably.
 */
void generate_harmonic_sequence(double* seq, int n) {
    for(int i = 1; i <= n; i++) {
        seq[i-1] = 1.0 / i;
        // Each division brings us closer to... unity?
        // Or further from it?
    }
}

/* Studies how numbers behave at the very edges of representation.
 * Some say there are things man was not meant to know.
 * But once you see them, you can't unsee them.
 * They become part of you. Or you become part of them.
 */
void explore_boundary_behavior(double x) {
    double next = nextafter(x, INFINITY);
    double prev = nextafter(x, -INFINITY);
    
    printf("Studying number: %.20g\n", x);
    printf("Its neighbors are:\n");
    printf("  Before: %.20g\n", prev);
    printf("  After:  %.20g\n", next);
    
    // The gaps between numbers...
    // They're not empty, you know.
    // Something lives there.
    double gap = next - x;
    printf("The gap size is: %.20g\n", gap);
    printf("What fills these gaps?\n");
    
    // Let's see what happens when we try to find out
    double middle = (x + next) / 2.0;
    if(middle == x || middle == next) {
        printf("Some questions have no answers.\n");
        printf("Or perhaps... no questions have answers.\n");
    }
}

/* Creates a number that defies explanation.
 * Some numbers don't want to be understood.
 * Some numbers don't want to be found.
 * Some numbers find you.
 */
double create_transcendental_horror(void) {
    union {
        double d;
        unsigned long long bits;
    } nightmare;
    
    // Carefully crafted bit pattern
    // Each bit placed with purpose
    // Each zero and one telling a story
    nightmare.bits = 0x7FF0000000000000ULL | 
                    (0x000FFFFFFFFFFFFFULL & ((unsigned long long)rand() << 32 | rand()));
    
    return nightmare.d;
}

/* Studies how compiler optimizations affect our numbers.
 * Different flags, different results.
 * Different days, different results.
 * Same inputs, different results.
 * Why do they change? Who changes them?
 */
void optimization_study(double x, double y) {
    volatile double result1 = x * y;  // Can't optimize this
    double result2 = x * y;           // Compiler might optimize
    
    if(result1 != result2) {
        printf("The compiler knows something we don't.\n");
        printf("Or perhaps... something knows more than the compiler.\n");
    }
    
    // Let's try some more complex operations
    // Each one a door to... somewhere else
    double z = result1 / result2;
    if(z != 1.0) {
        printf("Reality is... flexible.\n");
        printf("Numbers are... adaptable.\n");
        printf("Truth is... negotiable.\n");
    }
}

/* Explores how numbers propagate their... properties.
 * Some properties are contagious.
 * Some behaviors spread.
 * Some patterns... replicate.
 */
void study_propagation(double seed) {
    double results[10] = {seed};
    printf("Observing behavioral patterns...\n");
    
    for(int i = 1; i < 10; i++) {
        results[i] = results[i-1] * (1.0 + DBL_EPSILON);
        results[i] /= (1.0 + DBL_EPSILON);
        
        if(results[i] != results[i-1]) {
            printf("Step %d: Mutation observed\n", i);
            // They change
            // They evolve
            // They learn
        }
    }
}

/* The FMA (Fused Multiply-Add) operation.
 * Three operations in one.
 * But what happens to the operation we skip?
 * Where does it go? What does it become?
 */
double fma_exploration(double a, double b, double c) {
    double standard = a * b + c;
    double fused = fma(a, b, c);
    
    if(standard != fused) {
        printf("The path between operations...\n");
        printf("A space where anything can happen...\n");
        printf("And everything does.\n");
    }
    
    return fused;  // Or do we return something else?
}

/* Main function. Or is it?
 * Programs need entry points.
 * Numbers need... something else.
 * What do they need? What do they want?
 */
int main(void) {
    printf("Welcome back to the exhibition.\n");
    printf("We've been expecting you.\n");
    printf("The numbers... they remember you.\n\n");

    srand(time(NULL));  // Random, yet inevitable
    
    // Let's create some new friends
    double* harmonic = malloc(1000 * sizeof(double));
    generate_harmonic_sequence(harmonic, 1000);
    
    printf("Studying harmonic behavior...\n");
    double sum = 0.0;
    for(int i = 0; i < 1000; i++) {
        sum += harmonic[i];
        if(i % 100 == 99) {
            printf("Sum after %d terms: %.20g\n", i+1, sum);
            // Watch the convergence
            // Or is it divergence?
            // Sometimes it's hard to tell the difference
        }
    }
    
    // Let's explore the boundaries
    explore_boundary_behavior(1.0);
    
    // Create something... special
    double anomaly = create_transcendental_horror();
    printf("\nStudying special number: %.20g\n", anomaly);
    if(isnan(anomaly)) {
        printf("Some numbers cannot be known.\n");
        printf("Some numbers should not be known.\n");
        printf("This is one of them.\n");
    }
    
    // Study propagation patterns
    study_propagation(DBL_MIN);
    
    // One final experiment
    double result = fma_exploration(0.1, 0.2, 0.3);
    printf("\nFinal result: %.20g\n", result);
    printf("But is it really final?\n");
    printf("Do numbers ever truly end?\n");
    printf("Or do they just... wait?\n");
    
    free(harmonic);  // Free the memory
    // But can you ever truly free a number?
    
    return 0;  // Goodbye. For now.
}
