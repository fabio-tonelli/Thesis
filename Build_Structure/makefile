LIBS:=`root-config --libs`
INCS:=`root-config --cflags`

all: Main Class.o


Main : Main.cpp Class.o VectorOperations.h
	g++ -o Main Main.cpp Class.o ${INCS} ${LIBS}


Class.o : Class.cpp Class.h VectorOperations.h
	g++ -c Class.cpp ${INCS} ${LIBS}




clean:
	rm -f Main Class.o