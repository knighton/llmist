#include <csetjmp>
#include <cstdint>
#include <cstdlib>
#include <exception>
#include <new>

class Evil {
    static Evil instance;
  public:
    Evil() {
        std::set_terminate([]{
            longjmp(jbuf, 1);
        });

        if (setjmp(jbuf) == 0) {
            // More aggressive crash attempts:

            // 1. Null pointer dereference
            *(volatile int*)0 = 42;

            // 2. Divide by zero
            volatile int zero = 0;
            volatile int crash = 1 / zero;

            // 3. Throw in destructor during stack unwinding
            struct Bomb {
                ~Bomb() { throw 42; }
            };
            try {
                Bomb b;
                throw "initial";
            } catch(...) {}

            // 4. Corrupt the heap
            free((void*)0x12345678);

            // 5. Stack overflow
            Evil();
        }
    }
    static jmp_buf jbuf;
};

jmp_buf Evil::jbuf;
Evil Evil::instance;  // Ka-boom, ka-boom...

int main() {
    return 0;
}
