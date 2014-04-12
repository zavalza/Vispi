CC=g++

all: vm 

vm: vm.o
	$(CC) -o vm vm.o
	@echo ".Linking"

vm.o: vm.cpp 
	$(CC) -c vm.cpp
	@echo ".Compiling"

clean:
	rm vm.o vm