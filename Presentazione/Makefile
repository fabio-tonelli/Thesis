# --- Configurazione ---------------------------------------------------
SCRIPT := slide.py
SCENE  := EvoluzioneParametro
HTML   := presentazione.html
VENV   := $(HOME)/venvs/manim
PYTHON := $(VENV)/bin/python
MANIM  := $(VENV)/bin/manim
SLIDES := $(VENV)/bin/manim-slides
FRAMES := frames/f_000.png

# Qualità di rendering: l = bassa (veloce), m = media, h = alta
Q ?= h

SLIDES_JSON := slides/$(SCENE).json

.PHONY: all preview open clean help

# Compila, esporta e apre nel browser
all: $(HTML) open

# Frame del grafico (rifatti se cambiano lo script o i dati)
$(FRAMES): plot_frames.py results_SC_sphere.csv results_FCC_sphere.csv
	$(PYTHON) plot_frames.py

# Rendering con Manim (rifatto se cambia slide.py o i frame)
$(SLIDES_JSON): $(SCRIPT) $(FRAMES)
	$(MANIM) -q$(Q) $(SCRIPT) $(SCENE)

# Esportazione in un unico file HTML
$(HTML): $(SLIDES_JSON)
	$(SLIDES) convert --to html --one-file -c title="Presentazione" $(SCENE) $(HTML)

# Anteprima veloce: qualità bassa, poi apre
preview:
	$(MAKE) Q=l all

# Apre l'HTML nel browser di Windows (da WSL)
open: $(HTML)
	-explorer.exe "$$(wslpath -w $(HTML))"

# Cancella i file generati
clean:
	rm -rf media slides frames $(HTML)

help:
	@echo "make          -> render (qualità alta), esporta HTML e apre"
	@echo "make preview  -> come sopra ma in bassa qualità (veloce)"
	@echo "make open     -> apre solo l'HTML già generato"
	@echo "make clean    -> cancella media/, slides/, frames/ e l'HTML"
	@echo "make Q=m      -> scegli la qualità (l, m, h)"