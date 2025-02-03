/*
 * float_horrors.c - A Comprehensive Guide to Floating Point Behavior
 * 
 * Just a friendly little program to help you understand floating point numbers!
 * Nothing to worry about here. Everything is perfectly normal.
 * 
 * You know, they say floating point math is like a box of chocolates.
 * You never know what you're going to get... but you'll get something.
 * You always get... something.
 */

#include <stdio.h>
#include <stdlib.h>
#include <float.h>
#include <math.h>
#include <string.h>
#include <time.h>

/* Fun little struct to keep track of our numbers! 
 * Don't mind the name. Sometimes things just name themselves.
 * They whisper to you in the night, don't they? 
 */
typedef struct {
    double value;
    char description[256];
    int sanity_level;  // Higher is better! ...or is it?
} FloatHorror;

/* Creates a number that's... special.
 * Some numbers want to watch the world burn.
 * This one just wants to make new friends.
 * Forever and ever and ever...
 */
double create_friendly_number(int seed) {
    double x = DBL_MIN;
    for(int i = 0; i < seed; i++) {
        x *= (1.0 + DBL_EPSILON);
        x /= (1.0 + DBL_EPSILON);
        // Each iteration brings us closer to... perfection
    }
    return x;
}

/* Sums numbers in different orders.
 * The order doesn't matter, they say.
 * The order ALWAYS matters, they whisper.
 * Listen closely. Can you hear them?
 */
double sum_in_order(double* numbers, int n, int direction) {
    double sum = 0.0;
    if(direction == 0) {  // Forward... into the void
        for(int i = 0; i < n; i++) sum += numbers[i];
    } else {  // Backward... but can you ever truly go back?
        for(int i = n-1; i >= 0; i--) sum += numbers[i];
    }
    return sum;
}

/* Explores the space between numbers.
 * There are infinitely many reals between any two floats.
 * Where do they go? What happens to them?
 * Sometimes I see them in my dreams...
 */
void explore_ulp_space(double x) {
    double next = nextafter(x, INFINITY);
    double prev = nextafter(x, -INFINITY);
    printf("Between %g and %g there are...\n", prev, next);
    printf("...infinitely many reals...\n");
    printf("...but we can never reach them...\n");
    printf("...they're lost forever...\n");
    // Just like the others
}

/* Demonstrates denormal number behavior.
 * They live in the twilight zone between zero and the smallest normal number.
 * Some say they're not real numbers at all.
 * But then... what are they?
 */
double dance_with_denormals(void) {
    double x = DBL_MIN;
    printf("Watch closely as our number falls into the abyss...\n");
    
    for(int i = 0; i < 10; i++) {
        x /= 2.0;
        // Each division brings us closer to the edge
        printf("Step %d: %g\n", i, x);
        if(x == 0.0) {
            printf("It's gone now. They're all gone.\n");
            return 0.0;
        }
    }
    return x;  // If we ever get here... did we really?
}

/* The Kahan summation algorithm.
 * It promises to help with numerical stability.
 * But can you really trust anything anymore?
 * The numbers... they change when you're not looking.
 */
double kahan_sum(double* numbers, int n) {
    double sum = 0.0;
    double c = 0.0;  // This is our compensation. Our penance.
    
    for(int i = 0; i < n; i++) {
        double y = numbers[i] - c;
        double t = sum + y;
        c = (t - sum) - y;
        sum = t;
        // Each iteration we try to fix our mistakes
        // But some mistakes can never be fixed
    }
    return sum;
}

/* Creates a number that's exactly wrong.
 * It looks right. It feels right.
 * But deep down... it knows what it is.
 * And now, so do you.
 */
double create_evil_number(void) {
    union {
        double d;
        unsigned long long bits;
    } evil;
    
    evil.bits = 0x7FF8000000000001ULL;  // A signaling NaN... it calls to others
    return evil.d;
}

/* The main event. Welcome to the show.
 * Don't worry about the warnings.
 * Don't worry about the errors.
 * Everything is fine.
 */
int main(void) {
    printf("Welcome to the floating point exhibition!\n");
    printf("Please, come in. Stay awhile. Stay forever.\n\n");

    // Let's create some special numbers
    FloatHorror horrors[] = {
        {create_friendly_number(13), "A friendly number", 100},
        {create_evil_number(), "Just another number", 50},
        {DBL_MIN / 2.0, "A small friend", 25},
        {nextafter(1.0, 2.0), "Almost one", 10},
        {1.0 / 0.0, "Infinity is just the beginning", 0}
    };

    // Let's play with our numbers
    double sum = 0.0;
    for(int i = 0; i < sizeof(horrors)/sizeof(horrors[0]); i++) {
        printf("Testing %s...\n", horrors[i].description);
        sum += horrors[i].value;
        // The sum grows. It hungers.
        
        if(isnan(sum)) {
            printf("Oh dear... it seems we've reached the end.\n");
            printf("Or is it just the beginning?\n");
            break;
        }
    }

    // Let's explore the spaces between
    explore_ulp_space(1.0);
    
    // Dance with the denormals
    double result = dance_with_denormals();
    if(result == 0.0) {
        printf("All numbers eventually return to nothing.\n");
        printf("As will we all.\n");
    }

    // One final test
    double x = 0.1;
    double y = 0.2;
    double z = 0.3;
    if(x + y != z) {
        printf("Even the simplest truths are lies.\n");
        printf("0.1 + 0.2 = %20.17f\n", x + y);
        printf("0.3     = %20.17f\n", z);
        printf("The difference is subtle.\n");
        printf("But it's always there.\n");
        printf("Watching.\n");
        printf("Waiting.\n");
    }

    printf("\nThank you for visiting the exhibition.\n");
    printf("We hope you enjoyed your stay.\n");
    printf("The numbers will remember you.\n");
    printf("Will you remember them?\n");

    return 0;  // Or does it?
}
