CXX      := g++
CXXFLAGS := -O2 -std=c++17 -Wall
LDLIBS   := -larmadillo

HDR  := Multi_Dir.h
EXE1 := Multi_Dir
EXE2 := Multi_Dir_Sphere

all: $(EXE1) $(EXE2)

$(EXE1): $(EXE1).cpp $(HDR)
	$(CXX) $(CXXFLAGS) $< $(LDLIBS) -o $@

$(EXE2): $(EXE2).cpp $(HDR)
	$(CXX) $(CXXFLAGS) $< $(LDLIBS) -o $@

clean:
	rm -f $(EXE1) $(EXE2)

.PHONY: all clean