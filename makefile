CC = clang
CFLAGS = -Wall -std=c99 -pedantic

_molecule.so: molecule_wrap.o libmol.so
	$(CC) molecule_wrap.o -shared -dynamiclib -L/usr/lib/python3.7/config-3.7m-x86_64-linux-gnu -lpython3.7m -L. -lmol -o _molecule.so
libmol.so: mol.o
	$(CC) mol.o -shared -o libmol.so
molecule_wrap.o: molecule_wrap.c
	$(CC) $(CFLAGS) -c molecule_wrap.c -fPIC -I/usr/include/python3.7m -o molecule_wrap.o
molecule_wrap.c molecule.py: mol.o molecule.i
	swig3.0 -python molecule.i
mol.o: mol.c mol.h
	$(CC) $(CFLAGS) -c mol.c -fPIC -o mol.o
clean:
	rm *.o *.so 
