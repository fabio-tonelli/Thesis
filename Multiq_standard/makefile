CXX      := g++
CXXFLAGS := -O2 -std=c++17 -Wall
LDLIBS   := -larmadillo

HDR  := Multiq_2_3.h
EXE1 := Multiq_2_3
EXE2 := Multiq_Sphere

all: $(EXE1) $(EXE2)

$(EXE1): $(EXE1).cpp $(HDR)
	$(CXX) $(CXXFLAGS) $< $(LDLIBS) -o $@

$(EXE2): $(EXE2).cpp $(HDR)
	$(CXX) $(CXXFLAGS) $< $(LDLIBS) -o $@

clean:
	rm -f $(EXE1) $(EXE2)

.PHONY: all clean