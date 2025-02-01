clean:
	rm -rf bin/

all:
	mkdir -p bin/
	clang intro.c -o bin/intro -lm
	clang advanced.c -o bin/advanced -lm
	clang recursive.c -o bin/recursive -lm

run:
	@echo ----------
	./bin/intro
	@echo ----------
	./bin/advanced
	@echo ----------
	./bin/recursive
